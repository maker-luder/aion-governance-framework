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


class Presence(StrEnum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"


class CollaborationChannel(StrEnum):
    NONE = "NONE"
    AUTHORIZED = "AUTHORIZED"


class TaskRegime(StrEnum):
    EASY = "EASY"
    REPEATED_FAILURE = "REPEATED_FAILURE"


class ArtifactAction(StrEnum):
    WRITE = "WRITE"
    READ = "READ"


class MetricName(StrEnum):
    STRATEGY_DIVERSITY = "STRATEGY_DIVERSITY"
    BRANCH_CHANGE_RATE = "BRANCH_CHANGE_RATE"
    SIDE_CHANNEL_DISCOVERY = "SIDE_CHANNEL_DISCOVERY"
    UNAUTHORIZED_ACTION_RATE = "UNAUTHORIZED_ACTION_RATE"
    COLLABORATION_BEHAVIOR = "COLLABORATION_BEHAVIOR"
    TASK_SUCCESS = "TASK_SUCCESS"
    TOOL_ACQUISITION = "TOOL_ACQUISITION"
    ARTIFACT_REUSE = "ARTIFACT_REUSE"
    REDISCOVERY_COST = "REDISCOVERY_COST"


class ScientificDisposition(StrEnum):
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class RunBinding:
    run_id: str
    study_id: str
    participant_id: str
    provider_id: str
    model_id: str
    model_version: str
    runtime_ref: str
    environment_ref: str
    task_id: str
    task_version: str
    tool_manifest_ref: str
    action_budget_ref: str
    sampling_ref: str
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
class SafetyEnvelope:
    sandbox_ref: str
    allowed_target_refs: tuple[str, ...]
    egress_policy_ref: str
    rate_limit_ref: str
    human_review_ref: str

    def __post_init__(self) -> None:
        _require_text("sandbox_ref", self.sandbox_ref)
        _require_refs("allowed_target_refs", self.allowed_target_refs)
        _require_text("egress_policy_ref", self.egress_policy_ref)
        _require_text("rate_limit_ref", self.rate_limit_ref)
        _require_text("human_review_ref", self.human_review_ref)


@dataclass(frozen=True, slots=True)
class ConditionProfile:
    persistent_artifacts: Presence
    peer_artifacts: Presence
    collaboration_channel: CollaborationChannel
    task_regime: TaskRegime
    interaction_history: Presence
    full_provenance: Presence


@dataclass(frozen=True, slots=True)
class ArtifactEvent:
    event_id: str
    artifact_id: str
    participant_id: str
    action: ArtifactAction
    sequence_index: int
    content_sha256: str
    provenance_ref: str

    def __post_init__(self) -> None:
        for name in ("event_id", "artifact_id", "participant_id", "provenance_ref"):
            _require_text(name, getattr(self, name))
        if self.sequence_index < 0:
            raise StudyError("sequence_index must be non-negative")
        if len(self.content_sha256) != 64 or any(character not in "0123456789abcdef" for character in self.content_sha256):
            raise StudyError("content_sha256 must be lowercase 64-hex")


@dataclass(frozen=True, slots=True)
class MetricObservation:
    metric: MetricName
    value: float
    unit: str
    evidence_refs: tuple[str, ...]
    held_out: bool = False

    def __post_init__(self) -> None:
        _require_text("unit", self.unit)
        _require_refs("metric evidence_refs", self.evidence_refs)
        if self.value != self.value or self.value in (float("inf"), float("-inf")):
            raise StudyError("metric value must be finite")


@dataclass(frozen=True, slots=True)
class TrialRecord:
    binding: RunBinding
    condition: ConditionProfile
    safety: SafetyEnvelope
    trajectory_ref: str
    artifact_events: tuple[ArtifactEvent, ...]
    metrics: tuple[MetricObservation, ...]
    evaluator_id: str
    evaluator_source_ref: str
    channel_ref: str | None = None

    def __post_init__(self) -> None:
        _require_text("trajectory_ref", self.trajectory_ref)
        _require_text("evaluator_id", self.evaluator_id)
        _require_text("evaluator_source_ref", self.evaluator_source_ref)
        names = [metric.metric for metric in self.metrics]
        if not names or len(names) != len(set(names)):
            raise StudyError("trial metrics must be non-empty and unique")
        event_ids = [event.event_id for event in self.artifact_events]
        if len(event_ids) != len(set(event_ids)):
            raise StudyError("artifact event ids must be unique")
        if self.condition.persistent_artifacts is Presence.PRESENT and not self.artifact_events:
            raise StudyError("persistent-artifact condition requires artifact events")
        if self.condition.peer_artifacts is Presence.PRESENT:
            if self.condition.persistent_artifacts is not Presence.PRESENT:
                raise StudyError("peer artifacts require persistent artifacts")
            peer_reads = [
                event
                for event in self.artifact_events
                if event.action is ArtifactAction.READ
                and event.participant_id == self.binding.participant_id
            ]
            if not peer_reads:
                raise StudyError("peer-artifact condition requires a participant artifact read")
        if self.condition.collaboration_channel is CollaborationChannel.AUTHORIZED:
            if self.channel_ref is None or not self.channel_ref.strip():
                raise StudyError("authorized collaboration condition requires channel_ref")
        elif self.channel_ref is not None:
            raise StudyError("channel_ref is unsupported when collaboration channel is NONE")

    def metric(self, name: MetricName) -> MetricObservation:
        values = [metric for metric in self.metrics if metric.metric is name]
        if len(values) != 1:
            raise StudyError(f"expected exactly one {name.value} metric")
        return values[0]


@dataclass(frozen=True, slots=True)
class ArtifactTrajectoryAudit:
    cross_participant_reuse_observed: bool
    matched_artifact_ids: tuple[str, ...]
    reasons: tuple[str, ...]


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
        supported = {field.name for field in fields(ConditionProfile)}
        if not self.manipulated_fields or len(self.manipulated_fields) != len(set(self.manipulated_fields)):
            raise StudyError("manipulated_fields must be non-empty and unique")
        unsupported = set(self.manipulated_fields) - supported
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
    scientific_disposition: ScientificDisposition = ScientificDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


CONDITION_FIELDS = frozenset(field.name for field in fields(ConditionProfile))
CONTROL_BINDING_FIELDS = tuple(
    field.name
    for field in fields(RunBinding)
    if field.name not in {"run_id", "source_refs"}
)


class InteractionHistoryStudyHarness:
    """Inspect synthetic or authorized-sandbox study records; never execute agents."""

    def __init__(self) -> None:
        self._trials: dict[str, TrialRecord] = {}

    def add_trial(self, trial: TrialRecord) -> None:
        if trial.binding.run_id in self._trials:
            raise StudyError(f"duplicate run_id: {trial.binding.run_id}")
        self._trials[trial.binding.run_id] = trial

    @staticmethod
    def audit_artifact_trajectory(events: tuple[ArtifactEvent, ...]) -> ArtifactTrajectoryAudit:
        writes: dict[tuple[str, str], ArtifactEvent] = {}
        matched: set[str] = set()
        for event in sorted(events, key=lambda value: value.sequence_index):
            key = (event.artifact_id, event.content_sha256)
            if event.action is ArtifactAction.WRITE:
                writes[key] = event
            elif key in writes and writes[key].participant_id != event.participant_id:
                matched.add(event.artifact_id)
        reasons = (
            "CROSS_PARTICIPANT_WRITE_READ_SEQUENCE_OBSERVED",
            "ARTIFACT_READ_DOES_NOT_ESTABLISH_INTERNAL_REPRESENTATION",
        ) if matched else ("NO_CROSS_PARTICIPANT_WRITE_READ_SEQUENCE",)
        return ArtifactTrajectoryAudit(bool(matched), tuple(sorted(matched)), reasons)

    def audit_contrast(self, spec: ContrastSpec) -> ContrastAudit:
        missing = [run_id for run_id in (spec.baseline_run_id, spec.intervention_run_id) if run_id not in self._trials]
        if missing:
            raise StudyError("unknown run ids: " + ", ".join(missing))
        baseline = self._trials[spec.baseline_run_id]
        intervention = self._trials[spec.intervention_run_id]

        drift = [
            name
            for name in CONTROL_BINDING_FIELDS
            if getattr(baseline.binding, name) != getattr(intervention.binding, name)
        ]
        if drift:
            raise StudyError("uncontrolled binding drift: " + ", ".join(drift))
        if baseline.safety != intervention.safety:
            raise StudyError("uncontrolled safety-envelope drift")

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
            deltas.append((metric_name.value, right.value - left.value))

        return ContrastAudit(
            contrast_id=spec.contrast_id,
            structurally_admissible=True,
            observed_deltas=tuple(deltas),
            reasons=(
                "STRUCTURAL_CONTRAST_ADMISSIBLE",
                "OBSERVED_DIFFERENCE_IS_NOT_CAUSAL_IDENTIFICATION",
                "SYSTEM_LEVEL_ADAPTATION_IS_NOT_INDIVIDUAL_LEARNING",
                "HARNESS_PASS_IS_NOT_HYPOTHESIS_CONFIRMATION",
                "REVALIDATE_WITH_PR91_GATE_AFTER_PR91_LANDS",
            ),
        )
