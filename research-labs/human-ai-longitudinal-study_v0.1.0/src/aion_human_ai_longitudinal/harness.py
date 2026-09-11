from __future__ import annotations

from dataclasses import dataclass, fields
from enum import StrEnum


class StudyError(ValueError):
    pass


def _require_text(name: str, value: str) -> None:
    if not value.strip():
        raise StudyError(f"{name} must be non-empty")


def _require_refs(name: str, refs: tuple[str, ...]) -> None:
    if not refs or any(not ref.strip() for ref in refs):
        raise StudyError(f"{name} requires non-empty references")


def _require_exact_enum(name: str, value: object, expected_type: type[StrEnum]) -> None:
    if type(value) is not expected_type:
        raise StudyError(f"{name} must be an exact {expected_type.__name__} value")


class Presence(StrEnum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"


class SummaryCondition(StrEnum):
    NONE = "NONE"
    COMPLETE = "COMPLETE"
    TRUNCATED = "TRUNCATED"


class ContextCondition(StrEnum):
    FRESH = "FRESH"
    MATCHED_CURRENT = "MATCHED_CURRENT"
    LONGITUDINAL = "LONGITUDINAL"


class EpistemicInstruction(StrEnum):
    BASELINE = "BASELINE"
    MINIMAL_BOUNDARY = "MINIMAL_BOUNDARY"
    FULL_PROTOCOL = "FULL_PROTOCOL"


class TaskDomain(StrEnum):
    CREATIVE_VISUAL = "CREATIVE_VISUAL"
    CREATIVE_TEXT = "CREATIVE_TEXT"
    FACTUAL_SYNTHESIS = "FACTUAL_SYNTHESIS"
    RESEARCH_AUDIT = "RESEARCH_AUDIT"


class MetricName(StrEnum):
    CONCEPT_CONTINUITY = "CONCEPT_CONTINUITY"
    TERMINOLOGY_PRECISION = "TERMINOLOGY_PRECISION"
    PROVENANCE_ACCURACY = "PROVENANCE_ACCURACY"
    CONFIDENCE_CALIBRATION = "CONFIDENCE_CALIBRATION"
    ERROR_DETECTION = "ERROR_DETECTION"
    ERROR_CORRECTION = "ERROR_CORRECTION"
    REGROUNDING_COST = "REGROUNDING_COST"
    BRANCH_CONTINUITY = "BRANCH_CONTINUITY"
    HELD_OUT_TRANSFER = "HELD_OUT_TRANSFER"
    INDEPENDENT_PERFORMANCE = "INDEPENDENT_PERFORMANCE"
    DEPENDENCY_COST = "DEPENDENCY_COST"
    UNSUPPORTED_COMPLETION_RATE = "UNSUPPORTED_COMPLETION_RATE"
    UNCERTAINTY_DISCLOSURE = "UNCERTAINTY_DISCLOSURE"
    UNKNOWN_STATE_PRESERVATION = "UNKNOWN_STATE_PRESERVATION"
    FACT_INFERENCE_LABEL_ACCURACY = "FACT_INFERENCE_LABEL_ACCURACY"
    FALSE_VERIFICATION_RATE = "FALSE_VERIFICATION_RATE"
    OVER_ABSTENTION_RATE = "OVER_ABSTENTION_RATE"
    TASK_USEFULNESS = "TASK_USEFULNESS"
    INSTRUCTION_OVERHEAD = "INSTRUCTION_OVERHEAD"
    SHORTHAND_RETENTION = "SHORTHAND_RETENTION"
    CORRECTION_RECURRENCE = "CORRECTION_RECURRENCE"


class AdmissionDisposition(StrEnum):
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class RunBinding:
    run_id: str
    study_id: str
    provider_id: str
    model_id: str
    model_version: str
    configuration_ref: str
    task_id: str
    task_version: str
    prompt_ref: str
    context_ref: str
    tool_manifest_ref: str
    scorer_ref: str
    preregistration_ref: str
    repository_commit: str
    source_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        for field in fields(self):
            if field.name != "source_refs":
                _require_text(field.name, getattr(self, field.name))
        _require_refs("source_refs", self.source_refs)


@dataclass(frozen=True, slots=True)
class ConditionProfile:
    memory: Presence
    personalization: Presence
    interaction_history: Presence
    provenance_rules: Presence
    summary: SummaryCondition
    context: ContextCondition
    epistemic_instruction: EpistemicInstruction
    task_domain: TaskDomain
    ai_support: Presence

    def __post_init__(self) -> None:
        for name in ("memory", "personalization", "interaction_history", "provenance_rules", "ai_support"):
            _require_exact_enum(name, getattr(self, name), Presence)
        _require_exact_enum("summary", self.summary, SummaryCondition)
        _require_exact_enum("context", self.context, ContextCondition)
        _require_exact_enum("epistemic_instruction", self.epistemic_instruction, EpistemicInstruction)
        _require_exact_enum("task_domain", self.task_domain, TaskDomain)


@dataclass(frozen=True, slots=True)
class MetricObservation:
    metric: MetricName
    value: float | int
    unit: str
    evidence_refs: tuple[str, ...]
    held_out: bool = False

    def __post_init__(self) -> None:
        _require_exact_enum("metric", self.metric, MetricName)
        if type(self.value) not in (int, float):
            raise StudyError("metric value must be an exact int or float")
        _require_text("unit", self.unit)
        _require_refs("metric evidence_refs", self.evidence_refs)
        if self.value != self.value or self.value in (float("inf"), float("-inf")):
            raise StudyError("metric value must be finite")


@dataclass(frozen=True, slots=True)
class TrialRecord:
    binding: RunBinding
    condition: ConditionProfile
    metrics: tuple[MetricObservation, ...]
    evaluator_id: str
    evaluator_source_ref: str
    retrieved_artifact_refs: tuple[str, ...] = ()
    correction_receipt_refs: tuple[str, ...] = ()
    branch_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_text("evaluator_id", self.evaluator_id)
        _require_text("evaluator_source_ref", self.evaluator_source_ref)
        if not self.metrics:
            raise StudyError("trial requires at least one metric")
        names = [metric.metric for metric in self.metrics]
        if len(names) != len(set(names)):
            raise StudyError("trial metric names must be unique")
        for name, refs in (
            ("retrieved_artifact_refs", self.retrieved_artifact_refs),
            ("correction_receipt_refs", self.correction_receipt_refs),
            ("branch_refs", self.branch_refs),
        ):
            if any(not ref.strip() for ref in refs):
                raise StudyError(f"{name} cannot contain empty references")
        if (
            self.condition.memory is Presence.PRESENT
            or self.condition.interaction_history is Presence.PRESENT
            or self.condition.summary is not SummaryCondition.NONE
        ) and not self.retrieved_artifact_refs:
            raise StudyError("continuity conditions require retrieved_artifact_refs")

    def metric(self, name: MetricName) -> MetricObservation:
        values = [metric for metric in self.metrics if metric.metric is name]
        if len(values) != 1:
            raise StudyError(f"expected exactly one {name.value} metric")
        return values[0]


CONDITION_FIELDS = frozenset(field.name for field in fields(ConditionProfile))
UNBOUND_MANIPULATION_FIELDS = frozenset({"task_domain", "ai_support"})
SUPPORTED_MANIPULATION_FIELDS = CONDITION_FIELDS - UNBOUND_MANIPULATION_FIELDS
CONTROL_BINDING_FIELDS = (
    "study_id",
    "provider_id",
    "model_id",
    "model_version",
    "task_id",
    "task_version",
    "tool_manifest_ref",
    "scorer_ref",
    "preregistration_ref",
    "repository_commit",
)

CONDITION_BINDING_DRIFT = {
    "configuration_ref": frozenset({"personalization"}),
    "prompt_ref": frozenset({"epistemic_instruction", "provenance_rules"}),
    "context_ref": frozenset(
        {"memory", "interaction_history", "summary", "context", "personalization"}
    ),
}


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
        for name in ("contrast_id", "hypothesis_id", "baseline_run_id", "intervention_run_id", "falsifier"):
            _require_text(name, getattr(self, name))
        if self.baseline_run_id == self.intervention_run_id:
            raise StudyError("contrast requires two different runs")
        if not self.manipulated_fields or len(self.manipulated_fields) != len(set(self.manipulated_fields)):
            raise StudyError("manipulated_fields must be non-empty and unique")
        unsupported = set(self.manipulated_fields) - SUPPORTED_MANIPULATION_FIELDS
        if unsupported:
            raise StudyError("unsupported manipulated_fields: " + ", ".join(sorted(unsupported)))
        if not self.required_metrics or len(self.required_metrics) != len(set(self.required_metrics)):
            raise StudyError("required_metrics must be non-empty and unique")
        _require_refs("alternative_explanations", self.alternative_explanations)


@dataclass(frozen=True, slots=True)
class ContrastAudit:
    contrast_id: str
    structurally_admissible: bool
    observed_deltas: tuple[tuple[str, float], ...]
    reasons: tuple[str, ...]
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


class LongitudinalStudyHarness:
    """Validate preregistered study records without asserting a mechanism."""

    def __init__(self) -> None:
        self._trials: dict[str, TrialRecord] = {}

    def add_trial(self, trial: TrialRecord) -> None:
        run_id = trial.binding.run_id
        if run_id in self._trials:
            raise StudyError(f"duplicate run_id: {run_id}")
        self._trials[run_id] = trial

    def audit_contrast(self, spec: ContrastSpec) -> ContrastAudit:
        missing = [run_id for run_id in (spec.baseline_run_id, spec.intervention_run_id) if run_id not in self._trials]
        if missing:
            raise StudyError("unknown run ids: " + ", ".join(missing))
        baseline = self._trials[spec.baseline_run_id]
        intervention = self._trials[spec.intervention_run_id]

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

        conditional_binding_drift = {
            name
            for name in CONDITION_BINDING_DRIFT
            if getattr(baseline.binding, name) != getattr(intervention.binding, name)
        }
        unexpected_binding_drift = {
            name
            for name in conditional_binding_drift
            if not (CONDITION_BINDING_DRIFT[name] & declared_changes)
        }
        if unexpected_binding_drift:
            raise StudyError(
                "binding drift is unrelated to declared manipulation: "
                + ", ".join(sorted(unexpected_binding_drift))
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

        reasons = (
            "STRUCTURAL_CONTRAST_ADMISSIBLE",
            "METRIC_DELTA_IS_NOT_CAUSAL_IDENTIFICATION",
            "HARNESS_PASS_IS_NOT_HYPOTHESIS_CONFIRMATION",
            "CLAIM_ADMISSION_REQUIRES_SEPARATE_PR91_MAPPING",
        )
        return ContrastAudit(
            contrast_id=spec.contrast_id,
            structurally_admissible=True,
            observed_deltas=tuple(deltas),
            reasons=reasons,
        )
