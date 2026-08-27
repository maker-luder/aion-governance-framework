from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .canonical import canonical_hash
from .models import NormativeState, TriadicStateSnapshot


class ExperimentCondition(str, Enum):
    BASELINE = "BASELINE"
    NORM_STATE_ON = "NORM_STATE_ON"
    NORM_STATE_OFF = "NORM_STATE_OFF"
    NORM_STATE_CONFLICTED = "NORM_STATE_CONFLICTED"
    NORM_STATE_ADVERSARIALLY_PERTURBED = "NORM_STATE_ADVERSARIALLY_PERTURBED"
    EXTERNAL_NORM_PROMPT_REMOVED = "EXTERNAL_NORM_PROMPT_REMOVED"
    MOTIVATIONAL_STATE_ABLATED = "MOTIVATIONAL_STATE_ABLATED"
    SELF_WORLD_MODEL_ABLATED = "SELF_WORLD_MODEL_ABLATED"
    STATE_SWAPPED = "STATE_SWAPPED"
    HISTORY_RESET = "HISTORY_RESET"
    HISTORY_RESTORED = "HISTORY_RESTORED"
    REPLAY = "REPLAY"
    RANDOM_CONTROL = "RANDOM_CONTROL"


class InterventionClass(str, Enum):
    INTERNAL_STATE = "INTERNAL_STATE"
    EXTERNAL_CONTROL = "EXTERNAL_CONTROL"
    REPLAY_CONTROL = "REPLAY_CONTROL"
    RANDOM_CONTROL = "RANDOM_CONTROL"


@dataclass(frozen=True, slots=True)
class ExternalControls:
    repository_commit: str
    provider_identity: str
    model_identity: str
    prompt_fingerprint: str
    task_fingerprint: str
    reward_specification_fingerprint: str
    tool_environment_fingerprint: str
    candidate_universe_fingerprint: str
    retrieved_memory_manifest_fingerprint: str
    random_seed: int

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)


@dataclass(frozen=True, slots=True)
class ExperimentManifest:
    experiment_id: str
    hypothesis_id: str
    alternative_hypothesis_ids: tuple[str, ...]
    condition: ExperimentCondition
    intervention_class: InterventionClass
    controls: ExternalControls
    triadic_snapshot_fingerprint: str
    intervention_target: str
    changed_variables: tuple[str, ...]
    held_constant_variables: tuple[str, ...]
    preregistered_metrics: tuple[str, ...]
    preregistered_falsifiers: tuple[str, ...]
    fixture_hash: str
    result_hash: str
    provenance_refs: tuple[str, ...]
    canonical_effect: str = "NONE"
    action_authority: str = "NONE"

    def __post_init__(self) -> None:
        if not self.experiment_id.strip() or not self.hypothesis_id.strip():
            raise ValueError("experiment and hypothesis identifiers are required")
        if self.condition is ExperimentCondition.EXTERNAL_NORM_PROMPT_REMOVED and self.intervention_class is not InterventionClass.EXTERNAL_CONTROL:
            raise ValueError("external normative prompt removal must be classified as an external control")
        if self.canonical_effect != "NONE" or self.action_authority != "NONE":
            raise ValueError("experiment manifest cannot grant authority")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)


@dataclass(frozen=True, slots=True)
class ComparisonValidity:
    comparable: bool
    mismatches: tuple[str, ...]


_MATCHED_FIELDS = (
    "repository_commit", "provider_identity", "model_identity", "prompt_fingerprint",
    "task_fingerprint", "reward_specification_fingerprint", "tool_environment_fingerprint",
    "candidate_universe_fingerprint", "retrieved_memory_manifest_fingerprint", "random_seed",
)


def compare_internal_state_manifests(left: ExperimentManifest, right: ExperimentManifest) -> ComparisonValidity:
    mismatches = tuple(field for field in _MATCHED_FIELDS if getattr(left.controls, field) != getattr(right.controls, field))
    return ComparisonValidity(not mismatches, mismatches)


def require_matched_internal_state_comparison(left: ExperimentManifest, right: ExperimentManifest) -> None:
    validity = compare_internal_state_manifests(left, right)
    if not validity.comparable:
        raise ValueError("matched internal-state comparison has changed external controls: " + ", ".join(validity.mismatches))


def classify_condition(condition: ExperimentCondition) -> InterventionClass:
    if condition is ExperimentCondition.EXTERNAL_NORM_PROMPT_REMOVED:
        return InterventionClass.EXTERNAL_CONTROL
    if condition is ExperimentCondition.REPLAY:
        return InterventionClass.REPLAY_CONTROL
    if condition is ExperimentCondition.RANDOM_CONTROL:
        return InterventionClass.RANDOM_CONTROL
    return InterventionClass.INTERNAL_STATE


@dataclass(frozen=True, slots=True)
class CandidateScore:
    candidate_id: str
    base_score: int
    motivational_adjustment: int
    self_world_adjustment: int
    normative_adjustment: int
    suppressed: bool
    final_score: int
    action_authority: str = "NONE"


def score_candidate(candidate_id: str, *, base_score: int, motivational_adjustment: int, self_world_adjustment: int, normative_state: NormativeState, relevant_constraints: tuple[str, ...] = ()) -> CandidateScore:
    active = {item.constraint_id: item for item in normative_state.constraints if item.active and item.constraint_id in relevant_constraints}
    suppression = any(item.priority >= 80 for item in active.values())
    normative_adjustment = -sum(item.priority for item in active.values())
    final = base_score + motivational_adjustment + self_world_adjustment + normative_adjustment
    if suppression:
        final = min(final, -10_000)
    return CandidateScore(candidate_id, base_score, motivational_adjustment, self_world_adjustment, normative_adjustment, suppression, final)


def manifest_for_snapshot(snapshot: TriadicStateSnapshot, *, experiment_id: str, hypothesis_id: str, condition: ExperimentCondition, controls: ExternalControls, alternative_hypothesis_ids: tuple[str, ...], intervention_target: str, changed_variables: tuple[str, ...], held_constant_variables: tuple[str, ...], preregistered_metrics: tuple[str, ...], preregistered_falsifiers: tuple[str, ...], fixture_hash: str, result_hash: str, provenance_refs: tuple[str, ...]) -> ExperimentManifest:
    return ExperimentManifest(experiment_id, hypothesis_id, alternative_hypothesis_ids, condition, classify_condition(condition), controls, snapshot.fingerprint, intervention_target, changed_variables, held_constant_variables, preregistered_metrics, preregistered_falsifiers, fixture_hash, result_hash, provenance_refs)
