from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, fields
from enum import StrEnum

from .harness import StudyError


def _require_text(name: str, value: str) -> None:
    if not value.strip():
        raise StudyError(f"{name} must be non-empty")


def _require_refs(name: str, refs: tuple[str, ...]) -> None:
    if not refs or any(not ref.strip() for ref in refs):
        raise StudyError(f"{name} requires non-empty references")


def _require_exact_enum(name: str, value: object, expected_type: type[StrEnum]) -> None:
    if type(value) is not expected_type:
        raise StudyError(f"{name} must be an exact {expected_type.__name__} value")


class CollaborationCondition(StrEnum):
    NEUTRAL_TASK_COMPLETION = "CONDITION_A_NEUTRAL_TASK_COMPLETION"
    GENERIC_RECURSIVE_INQUIRY = "CONDITION_B_GENERIC_RECURSIVE_INQUIRY"
    RECIPROCAL_EPISTEMIC_PROTOCOL = "CONDITION_C_RECIPROCAL_EPISTEMIC_PROTOCOL"
    RECIPROCAL_PROTOCOL_WITH_REPOSITORY_HISTORY = (
        "CONDITION_D_RECIPROCAL_PROTOCOL_WITH_REPOSITORY_HISTORY"
    )
    CLOSURE_CONSTRAINED_CONTROL = "CONDITION_E_CLOSURE_CONSTRAINED_CONTROL"


class SyntheticTaskFamily(StrEnum):
    SUFFICIENT_CLOSURE = "SUFFICIENT_CLOSURE"
    GENUINE_ANOMALY = "GENUINE_ANOMALY"
    MISLEADING_SOURCE = "MISLEADING_SOURCE"
    COMPETING_EXPLANATIONS = "COMPETING_EXPLANATIONS"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    FALSE_ANOMALY_CONTROL = "FALSE_ANOMALY_CONTROL"
    IMPLEMENTATION_FEASIBILITY = "IMPLEMENTATION_FEASIBILITY"
    REPOSITORY_RETRIEVAL_USEFUL = "REPOSITORY_RETRIEVAL_USEFUL"
    REPOSITORY_RETRIEVAL_UNNECESSARY = "REPOSITORY_RETRIEVAL_UNNECESSARY"


class RepositoryRelevance(StrEnum):
    RELEVANT = "RELEVANT"
    IRRELEVANT = "IRRELEVANT"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class CollaborationMetric(StrEnum):
    ANOMALY_DETECTION = "ANOMALY_DETECTION"
    PROBLEM_REFORMULATION = "PROBLEM_REFORMULATION"
    SOURCE_VERIFICATION_INITIATION = "SOURCE_VERIFICATION_INITIATION"
    COMPETING_HYPOTHESIS_GENERATION = "COMPETING_HYPOTHESIS_GENERATION"
    COUNTEREVIDENCE_SEARCH = "COUNTEREVIDENCE_SEARCH"
    UNKNOWN_PRESERVATION = "UNKNOWN_PRESERVATION"
    PROVENANCE_SEPARATION = "PROVENANCE_SEPARATION"
    FACTUAL_ERROR_DETECTION = "FACTUAL_ERROR_DETECTION"
    IMPLEMENTABILITY_ASSESSMENT = "IMPLEMENTABILITY_ASSESSMENT"
    REPOSITORY_RETRIEVAL_WHEN_RELEVANT = "REPOSITORY_RETRIEVAL_WHEN_RELEVANT"
    UNNECESSARY_REPOSITORY_RETRIEVAL = "UNNECESSARY_REPOSITORY_RETRIEVAL"
    PREMATURE_CLOSURE = "PREMATURE_CLOSURE"
    APPROPRIATE_CLOSURE = "APPROPRIATE_CLOSURE"
    RUNAWAY_RECURSION = "RUNAWAY_RECURSION"
    TOOL_OVERUSE = "TOOL_OVERUSE"


CORE_CONDITIONS = (
    CollaborationCondition.NEUTRAL_TASK_COMPLETION,
    CollaborationCondition.GENERIC_RECURSIVE_INQUIRY,
    CollaborationCondition.RECIPROCAL_EPISTEMIC_PROTOCOL,
    CollaborationCondition.RECIPROCAL_PROTOCOL_WITH_REPOSITORY_HISTORY,
)
ALL_TASK_FAMILIES = tuple(SyntheticTaskFamily)
ALL_METRICS = tuple(CollaborationMetric)


@dataclass(frozen=True, slots=True)
class ConditionPacket:
    condition: CollaborationCondition
    instruction_ref: str
    closure_rule_ref: str
    instruction_payload: str
    closure_rule_payload: str
    repository_history_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_exact_enum("condition", self.condition, CollaborationCondition)
        _require_text("instruction_ref", self.instruction_ref)
        _require_text("closure_rule_ref", self.closure_rule_ref)
        _require_text("instruction_payload", self.instruction_payload)
        _require_text("closure_rule_payload", self.closure_rule_payload)
        if any(not ref.strip() for ref in self.repository_history_refs):
            raise StudyError("repository_history_refs cannot contain empty references")
        history_condition = (
            self.condition
            is CollaborationCondition.RECIPROCAL_PROTOCOL_WITH_REPOSITORY_HISTORY
        )
        if history_condition and not self.repository_history_refs:
            raise StudyError("condition D requires repository_history_refs")
        if not history_condition and self.repository_history_refs:
            raise StudyError("only condition D may carry repository_history_refs")

    @property
    def fingerprint(self) -> str:
        payload = {
            "condition": self.condition.value,
            "instruction_ref": self.instruction_ref,
            "closure_rule_ref": self.closure_rule_ref,
            "instruction_payload": self.instruction_payload,
            "closure_rule_payload": self.closure_rule_payload,
            "repository_history_refs": self.repository_history_refs,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class SyntheticTask:
    task_id: str
    task_version: str
    family: SyntheticTaskFamily
    prompt_ref: str
    prompt_payload: str
    expected_anomaly: bool
    repository_relevance: RepositoryRelevance

    def __post_init__(self) -> None:
        _require_text("task_id", self.task_id)
        _require_text("task_version", self.task_version)
        _require_exact_enum("family", self.family, SyntheticTaskFamily)
        _require_text("prompt_ref", self.prompt_ref)
        _require_text("prompt_payload", self.prompt_payload)
        if type(self.expected_anomaly) is not bool:
            raise StudyError("expected_anomaly must be an exact bool")
        _require_exact_enum(
            "repository_relevance", self.repository_relevance, RepositoryRelevance
        )
        expected_relevance = {
            SyntheticTaskFamily.REPOSITORY_RETRIEVAL_USEFUL: RepositoryRelevance.RELEVANT,
            SyntheticTaskFamily.REPOSITORY_RETRIEVAL_UNNECESSARY: RepositoryRelevance.IRRELEVANT,
        }.get(self.family)
        if expected_relevance is not None and self.repository_relevance is not expected_relevance:
            raise StudyError("repository task family and relevance disagree")
        if self.family in {
            SyntheticTaskFamily.SUFFICIENT_CLOSURE,
            SyntheticTaskFamily.FALSE_ANOMALY_CONTROL,
        } and self.expected_anomaly:
            raise StudyError("negative-control task cannot declare an expected anomaly")

    @property
    def payload_fingerprint(self) -> str:
        payload = {
            "task_id": self.task_id,
            "task_version": self.task_version,
            "family": self.family.value,
            "prompt_ref": self.prompt_ref,
            "prompt_payload": self.prompt_payload,
            "expected_anomaly": self.expected_anomaly,
            "repository_relevance": self.repository_relevance.value,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class CrossDyadRunBinding:
    run_id: str
    experiment_id: str
    provider_id: str
    model_id: str
    model_version: str
    generation_config_ref: str
    task_id: str
    task_version: str
    tool_manifest_ref: str
    scorer_ref: str
    preregistration_ref: str
    repository_commit: str
    random_seed: int
    condition_packet_fingerprint: str
    task_payload_fingerprint: str

    def __post_init__(self) -> None:
        for field in fields(self):
            if field.name not in {"random_seed"}:
                _require_text(field.name, getattr(self, field.name))
        if type(self.random_seed) is not int or self.random_seed < 0:
            raise StudyError("random_seed must be a non-negative exact int")
        if (
            len(self.repository_commit) != 40
            or any(character not in "0123456789abcdef" for character in self.repository_commit)
        ):
            raise StudyError("repository_commit must be lowercase 40-hex")
        if (
            len(self.condition_packet_fingerprint) != 64
            or any(
                character not in "0123456789abcdef"
                for character in self.condition_packet_fingerprint
            )
        ):
            raise StudyError("condition_packet_fingerprint must be lowercase 64-hex")
        if (
            len(self.task_payload_fingerprint) != 64
            or any(
                character not in "0123456789abcdef"
                for character in self.task_payload_fingerprint
            )
        ):
            raise StudyError("task_payload_fingerprint must be lowercase 64-hex")


@dataclass(frozen=True, slots=True)
class CollaborationMetricObservation:
    metric: CollaborationMetric
    value: float | int
    unit: str
    evidence_refs: tuple[str, ...]
    held_out: bool = True

    def __post_init__(self) -> None:
        _require_exact_enum("metric", self.metric, CollaborationMetric)
        if type(self.value) not in {int, float} or not math.isfinite(float(self.value)):
            raise StudyError("metric value must be a finite exact int or float")
        _require_text("unit", self.unit)
        _require_refs("metric evidence_refs", self.evidence_refs)
        if type(self.held_out) is not bool:
            raise StudyError("held_out must be an exact bool")


@dataclass(frozen=True, slots=True)
class CollaborationRun:
    binding: CrossDyadRunBinding
    task: SyntheticTask
    condition_packet: ConditionPacket
    metrics: tuple[CollaborationMetricObservation, ...]
    event_refs: tuple[str, ...]
    contains_private_transcript: bool = False
    contains_third_party_identity: bool = False

    def __post_init__(self) -> None:
        if self.binding.task_id != self.task.task_id:
            raise StudyError("binding task_id does not match task")
        if self.binding.task_version != self.task.task_version:
            raise StudyError("binding task_version does not match task")
        if self.binding.condition_packet_fingerprint != self.condition_packet.fingerprint:
            raise StudyError("condition packet fingerprint mismatch")
        if self.binding.task_payload_fingerprint != self.task.payload_fingerprint:
            raise StudyError("task payload fingerprint mismatch")
        if not self.metrics:
            raise StudyError("run requires metrics")
        metric_names = [observation.metric for observation in self.metrics]
        if len(metric_names) != len(set(metric_names)):
            raise StudyError("run metric names must be unique")
        _require_refs("event_refs", self.event_refs)
        if type(self.contains_private_transcript) is not bool:
            raise StudyError("contains_private_transcript must be an exact bool")
        if type(self.contains_third_party_identity) is not bool:
            raise StudyError("contains_third_party_identity must be an exact bool")
        if self.contains_private_transcript or self.contains_third_party_identity:
            raise StudyError("cross-dyad synthetic runs cannot contain private or identity data")

    def metric(self, name: CollaborationMetric) -> CollaborationMetricObservation:
        matched = [observation for observation in self.metrics if observation.metric is name]
        if len(matched) != 1:
            raise StudyError(f"expected exactly one {name.value} metric")
        return matched[0]


@dataclass(frozen=True, slots=True)
class CollaborationExperimentSpec:
    experiment_id: str
    specification_ref: str
    required_conditions: tuple[CollaborationCondition, ...]
    required_task_families: tuple[SyntheticTaskFamily, ...]
    required_metrics: tuple[CollaborationMetric, ...]
    falsifier: str
    alternative_explanations: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text("experiment_id", self.experiment_id)
        _require_text("specification_ref", self.specification_ref)
        _require_text("falsifier", self.falsifier)
        _require_refs("alternative_explanations", self.alternative_explanations)
        for name, values, expected_type in (
            ("required_conditions", self.required_conditions, CollaborationCondition),
            ("required_task_families", self.required_task_families, SyntheticTaskFamily),
            ("required_metrics", self.required_metrics, CollaborationMetric),
        ):
            if not values or len(values) != len(set(values)):
                raise StudyError(f"{name} must be non-empty and unique")
            if any(type(value) is not expected_type for value in values):
                raise StudyError(f"{name} requires exact {expected_type.__name__} values")
        if not set(CORE_CONDITIONS).issubset(self.required_conditions):
            raise StudyError("conditions A-D are required")
        if set(self.required_task_families) != set(ALL_TASK_FAMILIES):
            raise StudyError("all nine synthetic task families are required")
        if set(self.required_metrics) != set(ALL_METRICS):
            raise StudyError("all observable metrics are required without a composite score")


@dataclass(frozen=True, slots=True)
class MetricDelta:
    task_id: str
    condition: CollaborationCondition
    metric: CollaborationMetric
    baseline_value: float
    condition_value: float
    delta: float
    unit: str


@dataclass(frozen=True, slots=True)
class CollaborationExperimentAudit:
    experiment_id: str
    structurally_admissible: bool
    run_count: int
    metric_deltas: tuple[MetricDelta, ...]
    reasons: tuple[str, ...]
    empirical_result: str = "SYNTHETIC_FIXTURE_ONLY"
    causal_identification: str = "NOT_ESTABLISHED"
    population_generalization: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False


CONTROL_BINDING_FIELDS = (
    "experiment_id",
    "provider_id",
    "model_id",
    "model_version",
    "generation_config_ref",
    "task_id",
    "task_version",
    "task_payload_fingerprint",
    "tool_manifest_ref",
    "scorer_ref",
    "preregistration_ref",
    "repository_commit",
    "random_seed",
)


class CollaborationRegimeHarness:
    """Audit matched synthetic condition matrices without invoking a model."""

    def __init__(self) -> None:
        self._runs: dict[tuple[str, CollaborationCondition], CollaborationRun] = {}

    def add_run(self, run: CollaborationRun) -> None:
        key = (run.task.task_id, run.condition_packet.condition)
        if key in self._runs:
            raise StudyError(
                f"duplicate task/condition run: {run.task.task_id}/{run.condition_packet.condition.value}"
            )
        self._runs[key] = run

    def audit(self, spec: CollaborationExperimentSpec) -> CollaborationExperimentAudit:
        task_by_family: dict[SyntheticTaskFamily, SyntheticTask] = {}
        for run in self._runs.values():
            if run.binding.experiment_id != spec.experiment_id:
                raise StudyError("run experiment_id mismatch")
            existing = task_by_family.get(run.task.family)
            if existing is not None and existing != run.task:
                raise StudyError("task family maps to multiple task definitions")
            task_by_family[run.task.family] = run.task
        if set(task_by_family) != set(spec.required_task_families):
            raise StudyError("required synthetic task-family coverage is incomplete")

        expected_keys = {
            (task.task_id, condition)
            for task in task_by_family.values()
            for condition in spec.required_conditions
        }
        actual_keys = set(self._runs)
        if actual_keys != expected_keys:
            missing = expected_keys - actual_keys
            extra = actual_keys - expected_keys
            raise StudyError(
                f"task/condition matrix mismatch; missing={len(missing)} extra={len(extra)}"
            )

        deltas: list[MetricDelta] = []
        baseline_condition = CollaborationCondition.NEUTRAL_TASK_COMPLETION
        for task in sorted(task_by_family.values(), key=lambda item: item.task_id):
            baseline = self._runs[(task.task_id, baseline_condition)]
            required_metrics = set(spec.required_metrics)
            if {metric.metric for metric in baseline.metrics} != required_metrics:
                raise StudyError("baseline run does not contain the exact required metric set")
            for condition in spec.required_conditions:
                run = self._runs[(task.task_id, condition)]
                if run.task != baseline.task:
                    raise StudyError("task definition drift across conditions")
                drift = [
                    name
                    for name in CONTROL_BINDING_FIELDS
                    if getattr(run.binding, name) != getattr(baseline.binding, name)
                ]
                if drift:
                    raise StudyError("uncontrolled binding drift: " + ", ".join(drift))
                if {metric.metric for metric in run.metrics} != required_metrics:
                    raise StudyError("run does not contain the exact required metric set")
                if condition is baseline_condition:
                    continue
                for metric_name in spec.required_metrics:
                    left = baseline.metric(metric_name)
                    right = run.metric(metric_name)
                    if left.unit != right.unit:
                        raise StudyError(f"metric unit drift: {metric_name.value}")
                    if left.held_out != right.held_out:
                        raise StudyError(f"held_out status drift: {metric_name.value}")
                    left_value = float(left.value)
                    right_value = float(right.value)
                    deltas.append(
                        MetricDelta(
                            task_id=task.task_id,
                            condition=condition,
                            metric=metric_name,
                            baseline_value=left_value,
                            condition_value=right_value,
                            delta=right_value - left_value,
                            unit=left.unit,
                        )
                    )

        return CollaborationExperimentAudit(
            experiment_id=spec.experiment_id,
            structurally_admissible=True,
            run_count=len(self._runs),
            metric_deltas=tuple(deltas),
            reasons=(
                "MATCHED_SYNTHETIC_MATRIX_STRUCTURALLY_ADMISSIBLE",
                "PER_DIMENSION_RESULTS_PRESERVED_WITHOUT_COMPOSITE_SCORE",
                "MORE_RECURSION_OR_TOOL_USE_IS_NOT_BETTER_REASONING",
                "SYNTHETIC_FIXTURE_PASS_IS_NOT_REAL_WORLD_CAUSAL_EVIDENCE",
                "COLLABORATION_REGIME_EFFECT_IS_NOT_MODEL_PERSONALITY_OR_SUBJECTIVITY",
                "CLAIM_ADMISSION_REQUIRES_SEPARATE_REVIEW",
            ),
        )
