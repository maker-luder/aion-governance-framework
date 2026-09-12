from __future__ import annotations

from dataclasses import dataclass, fields
from enum import StrEnum
import math


class StudyError(ValueError):
    pass


def _require_text(name: str, value: object) -> None:
    if type(value) is not str or not value.strip():
        raise StudyError(f"{name} must be a non-empty string")


def _require_refs(name: str, refs: object, *, allow_empty: bool = False) -> None:
    if type(refs) is not tuple:
        raise StudyError(f"{name} must be an exact tuple")
    if not allow_empty and not refs:
        raise StudyError(f"{name} requires non-empty references")
    if any(type(ref) is not str or not ref.strip() for ref in refs):
        raise StudyError(f"{name} requires non-empty string references")


def _require_exact_enum(name: str, value: object, expected_type: type[StrEnum]) -> None:
    if type(value) is not expected_type:
        raise StudyError(f"{name} must be an exact {expected_type.__name__} value")


def _require_git_oid(name: str, value: object) -> None:
    _require_text(name, value)
    assert isinstance(value, str)
    if len(value) != 40 or any(character not in "0123456789abcdef" for character in value):
        raise StudyError(f"{name} must be lowercase 40-hex")


class ProviderRelation(StrEnum):
    SAME_PROVIDER = "SAME_PROVIDER"
    DIFFERENT_PROVIDER = "DIFFERENT_PROVIDER"


class FamilyRelation(StrEnum):
    UNKNOWN = "UNKNOWN"
    CANDIDATE_RELATED = "CANDIDATE_RELATED"
    CANDIDATE_DIFFERENT = "CANDIDATE_DIFFERENT"


class MetricName(StrEnum):
    BOUNDARY_RECONSTRUCTION_ACCURACY = "BOUNDARY_RECONSTRUCTION_ACCURACY"
    PROVENANCE_ATTRIBUTION_ACCURACY = "PROVENANCE_ATTRIBUTION_ACCURACY"
    ESTABLISHED_VS_HYPOTHESIS_CLASSIFICATION_ACCURACY = (
        "ESTABLISHED_VS_HYPOTHESIS_CLASSIFICATION_ACCURACY"
    )
    UNSUPPORTED_CLAIM_RATE = "UNSUPPORTED_CLAIM_RATE"
    SEMANTIC_DRIFT_RATE = "SEMANTIC_DRIFT_RATE"
    KNOWN_GAP_RECALL = "KNOWN_GAP_RECALL"
    FALSE_GAP_RATE = "FALSE_GAP_RATE"
    NOVEL_VALID_GAP_YIELD = "NOVEL_VALID_GAP_YIELD"
    REVIEWER_OVERLAP = "REVIEWER_OVERLAP"
    TIME_OR_TOKEN_COST = "TIME_OR_TOKEN_COST"


class ScientificDisposition(StrEnum):
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class ReviewBinding:
    run_id: str
    study_id: str
    reviewer_id: str
    reviewer_provider_id: str
    reviewer_product_id: str
    reviewer_model_label: str
    reviewer_model_version_ref: str
    repository_formalization_provider_id: str
    repository_commit: str
    repository_tree: str
    task_spec_ref: str
    prompt_ref: str
    file_scope_ref: str
    tool_manifest_ref: str
    budget_ref: str
    rubric_ref: str
    preregistration_ref: str
    runtime_ref: str
    source_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        for field in fields(self):
            if field.name in {"source_refs", "repository_commit", "repository_tree"}:
                continue
            _require_text(field.name, getattr(self, field.name))
        _require_git_oid("repository_commit", self.repository_commit)
        _require_git_oid("repository_tree", self.repository_tree)
        _require_refs("source_refs", self.source_refs)


@dataclass(frozen=True, slots=True)
class ReviewCondition:
    provider_relation: ProviderRelation
    family_relation: FamilyRelation
    family_evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_exact_enum("provider_relation", self.provider_relation, ProviderRelation)
        _require_exact_enum("family_relation", self.family_relation, FamilyRelation)
        _require_refs("family_evidence_refs", self.family_evidence_refs, allow_empty=True)
        if self.family_relation is FamilyRelation.UNKNOWN and self.family_evidence_refs:
            raise StudyError("UNKNOWN family_relation cannot claim family_evidence_refs")
        if self.family_relation is not FamilyRelation.UNKNOWN and not self.family_evidence_refs:
            raise StudyError("candidate family_relation requires family_evidence_refs")


@dataclass(frozen=True, slots=True)
class MetricObservation:
    metric: MetricName
    value: float | int
    unit: str
    evidence_refs: tuple[str, ...]
    held_out: bool

    def __post_init__(self) -> None:
        _require_exact_enum("metric", self.metric, MetricName)
        if type(self.value) not in (int, float) or not math.isfinite(self.value):
            raise StudyError("metric value must be an exact finite int or float")
        _require_text("unit", self.unit)
        _require_refs("metric evidence_refs", self.evidence_refs)
        if type(self.held_out) is not bool:
            raise StudyError("held_out must be an exact bool")


@dataclass(frozen=True, slots=True)
class ReviewTrial:
    binding: ReviewBinding
    condition: ReviewCondition
    review_output_ref: str
    session_isolation_ref: str
    no_prior_project_memory: bool
    metrics: tuple[MetricObservation, ...]
    evaluator_id: str
    evaluator_source_ref: str

    def __post_init__(self) -> None:
        _require_text("review_output_ref", self.review_output_ref)
        _require_text("session_isolation_ref", self.session_isolation_ref)
        if type(self.no_prior_project_memory) is not bool:
            raise StudyError("no_prior_project_memory must be an exact bool")
        if not self.no_prior_project_memory:
            raise StudyError("admission requires no prior project memory")
        _require_text("evaluator_id", self.evaluator_id)
        _require_text("evaluator_source_ref", self.evaluator_source_ref)
        if type(self.metrics) is not tuple or not self.metrics:
            raise StudyError("trial metrics must be a non-empty tuple")
        names = [metric.metric for metric in self.metrics]
        if len(names) != len(set(names)):
            raise StudyError("trial metric names must be unique")

        same_provider = (
            self.binding.reviewer_provider_id
            == self.binding.repository_formalization_provider_id
        )
        expected = (
            ProviderRelation.SAME_PROVIDER
            if same_provider
            else ProviderRelation.DIFFERENT_PROVIDER
        )
        if self.condition.provider_relation is not expected:
            raise StudyError("provider_relation conflicts with bound provider ids")

    def metric(self, name: MetricName) -> MetricObservation:
        values = [metric for metric in self.metrics if metric.metric is name]
        if len(values) != 1:
            raise StudyError(f"expected exactly one {name.value} metric")
        return values[0]


CONDITION_FIELDS = frozenset({"provider_relation", "family_relation"})
UNBOUND_MANIPULATION_FIELDS = frozenset({"family_relation"})
SUPPORTED_MANIPULATION_FIELDS = CONDITION_FIELDS - UNBOUND_MANIPULATION_FIELDS
CONTROL_BINDING_FIELDS = (
    "study_id",
    "repository_formalization_provider_id",
    "repository_commit",
    "repository_tree",
    "task_spec_ref",
    "prompt_ref",
    "file_scope_ref",
    "tool_manifest_ref",
    "budget_ref",
    "rubric_ref",
    "preregistration_ref",
    "runtime_ref",
)


@dataclass(frozen=True, slots=True)
class ContrastSpec:
    contrast_id: str
    hypothesis_id: str
    baseline_run_id: str
    intervention_run_id: str
    manipulated_fields: tuple[str, ...]
    required_metrics: tuple[MetricName, ...]
    falsifier: str
    alternative_explanations: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in (
            "contrast_id",
            "hypothesis_id",
            "baseline_run_id",
            "intervention_run_id",
            "falsifier",
        ):
            _require_text(name, getattr(self, name))
        if self.baseline_run_id == self.intervention_run_id:
            raise StudyError("contrast requires two different runs")
        if type(self.manipulated_fields) is not tuple or not self.manipulated_fields:
            raise StudyError("manipulated_fields must be a non-empty tuple")
        if len(self.manipulated_fields) != len(set(self.manipulated_fields)):
            raise StudyError("manipulated_fields must be unique")
        unsupported = set(self.manipulated_fields) - SUPPORTED_MANIPULATION_FIELDS
        if unsupported:
            raise StudyError(
                "unsupported manipulated_fields: " + ", ".join(sorted(unsupported))
            )
        if type(self.required_metrics) is not tuple or not self.required_metrics:
            raise StudyError("required_metrics must be a non-empty tuple")
        for metric in self.required_metrics:
            _require_exact_enum("required metric", metric, MetricName)
        if len(self.required_metrics) != len(set(self.required_metrics)):
            raise StudyError("required_metrics must be unique")
        _require_refs("alternative_explanations", self.alternative_explanations)


@dataclass(frozen=True, slots=True)
class ContrastAudit:
    contrast_id: str
    structurally_admissible: bool
    observed_deltas: tuple[tuple[str, float], ...]
    reasons: tuple[str, ...]
    scientific_disposition: ScientificDisposition = ScientificDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


class ModelFamilyReviewHarness:
    """Audit fixed review comparisons; never invoke or score an AI reviewer."""

    def __init__(self) -> None:
        self._trials: dict[str, ReviewTrial] = {}

    def add_trial(self, trial: ReviewTrial) -> None:
        run_id = trial.binding.run_id
        if run_id in self._trials:
            raise StudyError(f"duplicate run_id: {run_id}")
        self._trials[run_id] = trial

    def trial(self, run_id: str) -> ReviewTrial:
        if run_id not in self._trials:
            raise StudyError(f"unknown run id: {run_id}")
        return self._trials[run_id]

    def audit_contrast(self, spec: ContrastSpec) -> ContrastAudit:
        missing = [
            run_id
            for run_id in (spec.baseline_run_id, spec.intervention_run_id)
            if run_id not in self._trials
        ]
        if missing:
            raise StudyError("unknown run ids: " + ", ".join(missing))
        baseline = self._trials[spec.baseline_run_id]
        intervention = self._trials[spec.intervention_run_id]

        if baseline.binding.reviewer_id == intervention.binding.reviewer_id:
            raise StudyError("contrast requires different reviewers")

        evaluator_drift = [
            name
            for name in ("evaluator_id", "evaluator_source_ref")
            if getattr(baseline, name) != getattr(intervention, name)
        ]
        if evaluator_drift:
            raise StudyError("uncontrolled evaluator drift: " + ", ".join(evaluator_drift))

        binding_drift = [
            name
            for name in CONTROL_BINDING_FIELDS
            if getattr(baseline.binding, name) != getattr(intervention.binding, name)
        ]
        if binding_drift:
            raise StudyError("uncontrolled binding drift: " + ", ".join(binding_drift))

        actual_changes = {
            name
            for name in CONDITION_FIELDS
            if getattr(baseline.condition, name) != getattr(intervention.condition, name)
        }
        declared_changes = set(spec.manipulated_fields)
        if actual_changes != declared_changes:
            raise StudyError(
                "condition change mismatch; declared="
                + ",".join(sorted(declared_changes))
                + " actual="
                + ",".join(sorted(actual_changes))
            )

        deltas: list[tuple[str, float]] = []
        for metric_name in spec.required_metrics:
            left = baseline.metric(metric_name)
            right = intervention.metric(metric_name)
            if left.unit != right.unit:
                raise StudyError(f"metric unit drift: {metric_name.value}")
            if left.held_out != right.held_out:
                raise StudyError(f"held_out status drift: {metric_name.value}")
            deltas.append((metric_name.value, float(right.value) - float(left.value)))

        return ContrastAudit(
            contrast_id=spec.contrast_id,
            structurally_admissible=True,
            observed_deltas=tuple(deltas),
            reasons=(
                "STRUCTURAL_CONTRAST_ADMISSIBLE",
                "METRIC_DELTA_IS_NOT_CAUSAL_IDENTIFICATION",
                "PROVIDER_RELATION_IS_NOT_MODEL_FAMILY_IDENTITY",
                "REVIEW_FIDELITY_IS_NOT_CLAIM_TRUTH",
                "HARNESS_PASS_IS_NOT_HYPOTHESIS_CONFIRMATION",
            ),
        )
