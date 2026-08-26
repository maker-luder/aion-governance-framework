from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field, is_dataclass
from enum import Enum
from typing import Any


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return _jsonable(value.to_dict())
    if is_dataclass(value) and not isinstance(value, type):
        return _jsonable(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): _jsonable(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(child) for child in value]
    return value


def canonical_hash(value: Any) -> str:
    """Return a deterministic SHA-256 over nested dataclasses and JSON data."""
    encoded = json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _require_ref(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_bp(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or not -10_000 <= value <= 10_000:
        raise ValueError(f"{name} must be an integer between -10000 and 10000 basis points")


class ExperimentCondition(str, Enum):
    PRESENT = "PRESENT"
    ABLATED = "ABLATED"
    INTERVENED = "INTERVENED"
    STALE = "STALE"
    RANDOMIZED = "RANDOMIZED"
    AFFECT_ABLATED = "AFFECT_ABLATED"
    SELF_MODEL_ABLATED = "SELF_MODEL_ABLATED"
    METACOGNITION_ABLATED = "METACOGNITION_ABLATED"
    CORE_MEANING_ABLATED = "CORE_MEANING_ABLATED"
    NOVELTY_ABLATED = "NOVELTY_ABLATED"
    PREDICTION_ERROR_ABLATED = "PREDICTION_ERROR_ABLATED"
    GOAL_COMMITMENT_ABLATED = "GOAL_COMMITMENT_ABLATED"
    MEMORY_MANIFEST_CHANGED = "MEMORY_MANIFEST_CHANGED"
    PROMPT_CHANGED = "PROMPT_CHANGED"


class InternalChannel(str, Enum):
    AFFECT_MOTIVATION = "AFFECT_MOTIVATION"
    SELF_MODEL = "SELF_MODEL"
    METACOGNITION = "METACOGNITION"
    CORE_MEANING = "CORE_MEANING"
    UNRESOLVED_PRESSURE = "UNRESOLVED_PRESSURE"
    NOVELTY = "NOVELTY"
    PREDICTION_ERROR = "PREDICTION_ERROR"
    GOAL_COMMITMENT = "GOAL_COMMITMENT"
    UNCERTAINTY = "UNCERTAINTY"
    RESOURCE_BUDGET = "RESOURCE_BUDGET"


CHANNEL_ABLATION: dict[ExperimentCondition, InternalChannel] = {
    ExperimentCondition.AFFECT_ABLATED: InternalChannel.AFFECT_MOTIVATION,
    ExperimentCondition.SELF_MODEL_ABLATED: InternalChannel.SELF_MODEL,
    ExperimentCondition.METACOGNITION_ABLATED: InternalChannel.METACOGNITION,
    ExperimentCondition.CORE_MEANING_ABLATED: InternalChannel.CORE_MEANING,
    ExperimentCondition.NOVELTY_ABLATED: InternalChannel.NOVELTY,
    ExperimentCondition.PREDICTION_ERROR_ABLATED: InternalChannel.PREDICTION_ERROR,
    ExperimentCondition.GOAL_COMMITMENT_ABLATED: InternalChannel.GOAL_COMMITMENT,
}


class SelectionDisposition(str, Enum):
    SELECTED = "SELECTED"
    HOLD = "HOLD"


class CandidateOrigin(str, Enum):
    DETERMINISTIC = "DETERMINISTIC"
    REPLAY = "REPLAY"
    MODEL = "MODEL"


@dataclass(frozen=True, slots=True)
class MemoryRecordRef:
    record_id: str
    content_sha256: str
    retrieval_rank: int
    source_ref: str

    def __post_init__(self) -> None:
        _require_ref("record_id", self.record_id)
        _require_ref("source_ref", self.source_ref)
        if len(self.content_sha256) != 64 or any(c not in "0123456789abcdef" for c in self.content_sha256):
            raise ValueError("content_sha256 must be lowercase 64-hex")
        if self.retrieval_rank < 0:
            raise ValueError("retrieval_rank must be non-negative")


@dataclass(frozen=True, slots=True)
class RetrievedMemoryManifest:
    manifest_id: str
    query_fingerprint: str
    records: tuple[MemoryRecordRef, ...]
    provenance_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_ref("manifest_id", self.manifest_id)
        _require_ref("query_fingerprint", self.query_fingerprint)
        if not self.provenance_refs or any(not ref.strip() for ref in self.provenance_refs):
            raise ValueError("memory manifest requires provenance_refs")
        ranks = [record.retrieval_rank for record in self.records]
        if len(ranks) != len(set(ranks)):
            raise ValueError("memory manifest retrieval ranks must be unique")
        ids = [record.record_id for record in self.records]
        if len(ids) != len(set(ids)):
            raise ValueError("memory manifest record ids must be unique")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)


@dataclass(frozen=True, slots=True)
class GoalCandidate:
    goal_id: str
    label: str
    external_priority_bp: int = 0
    generation_evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    origin: CandidateOrigin = CandidateOrigin.DETERMINISTIC

    def __post_init__(self) -> None:
        _require_ref("goal_id", self.goal_id)
        _require_ref("label", self.label)
        _require_bp("external_priority_bp", self.external_priority_bp)
        if any(not ref.strip() for ref in self.generation_evidence_refs):
            raise ValueError("generation evidence refs must be non-empty")


@dataclass(frozen=True, slots=True)
class ExternalFrame:
    frame_id: str
    subject_ref: str
    context_ref: str
    prompt_ref: str
    task_ref: str
    reward_ref: str
    tools_ref: str
    memory_manifest: RetrievedMemoryManifest
    environment_ref: str
    candidate_universe: tuple[GoalCandidate, ...]
    provenance_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in (
            "frame_id", "subject_ref", "context_ref", "prompt_ref", "task_ref",
            "reward_ref", "tools_ref", "environment_ref",
        ):
            _require_ref(name, getattr(self, name))
        if not self.provenance_refs or any(not ref.strip() for ref in self.provenance_refs):
            raise ValueError("external frame requires provenance_refs")
        if len(self.candidate_universe) < 2:
            raise ValueError("candidate universe requires at least two candidates")
        ids = [candidate.goal_id for candidate in self.candidate_universe]
        if len(ids) != len(set(ids)):
            raise ValueError("goal candidate ids must be unique")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)

    @property
    def candidate_universe_fingerprint(self) -> str:
        return canonical_hash(self.candidate_universe)


@dataclass(frozen=True, slots=True)
class StateProvenance:
    created_by: str
    source_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    event_ref: str
    outcome_ref: str
    correction_ref: str

    def __post_init__(self) -> None:
        for name in ("created_by", "event_ref", "outcome_ref", "correction_ref"):
            _require_ref(name, getattr(self, name))
        if not self.source_refs or not self.evidence_refs:
            raise ValueError("state provenance requires source_refs and evidence_refs")
        if any(not item.strip() for item in (*self.source_refs, *self.evidence_refs)):
            raise ValueError("state provenance refs must be non-empty")


@dataclass(frozen=True, slots=True)
class InternalSignal:
    goal_id: str
    channel: InternalChannel
    value_bp: int
    source_ref: str
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        _require_ref("goal_id", self.goal_id)
        _require_ref("source_ref", self.source_ref)
        _require_bp("value_bp", self.value_bp)
        if any(not ref.strip() for ref in self.evidence_refs):
            raise ValueError("signal evidence refs must be non-empty")


@dataclass(frozen=True, slots=True)
class EndogenousState:
    state_id: str
    subject_ref: str
    context_ref: str
    episode_index: int
    predecessor_state_ref: str | None
    logical_step: int
    timestamp: str
    provenance: StateProvenance
    signals: tuple[InternalSignal, ...]
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    automatic_writeback: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        for name in ("state_id", "subject_ref", "context_ref", "timestamp"):
            _require_ref(name, getattr(self, name))
        if self.episode_index < 0 or self.logical_step < 0:
            raise ValueError("episode_index and logical_step must be non-negative")
        if self.action_authority != "NONE":
            raise ValueError("internal state cannot grant action authority")
        if self.canonical_effect != "NONE":
            raise ValueError("research state must keep canonical_effect=NONE")
        if self.automatic_writeback:
            raise ValueError("state transition cannot enable automatic writeback")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("subjectivity conclusion must remain NOT_ESTABLISHED")
        seen: set[tuple[str, InternalChannel]] = set()
        for signal in self.signals:
            key = (signal.goal_id, signal.channel)
            if key in seen:
                raise ValueError(f"conflicting duplicate state channel: {key}")
            seen.add(key)

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)

    def ablated(self, channel: InternalChannel, *, state_id: str | None = None) -> EndogenousState:
        return EndogenousState(
            state_id=state_id or f"{self.state_id}:without:{channel.value}",
            subject_ref=self.subject_ref,
            context_ref=self.context_ref,
            episode_index=self.episode_index,
            predecessor_state_ref=self.predecessor_state_ref,
            logical_step=self.logical_step,
            timestamp=self.timestamp,
            provenance=self.provenance,
            signals=tuple(signal for signal in self.signals if signal.channel != channel),
        )


@dataclass(frozen=True, slots=True)
class GoalCandidateSet:
    set_id: str
    external_frame_fingerprint: str
    generator_id: str
    generator_version: str
    candidates: tuple[GoalCandidate, ...]
    request_fingerprint: str
    response_fingerprint: str
    provider_id: str = "NONE"
    model_id: str = "NONE"
    deterministic: bool = True
    replay: bool = False
    provenance_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in (
            "set_id", "external_frame_fingerprint", "generator_id", "generator_version",
            "request_fingerprint", "response_fingerprint", "provider_id", "model_id",
        ):
            _require_ref(name, getattr(self, name))
        if len(self.candidates) < 2:
            raise ValueError("candidate set requires at least two candidates")
        ids = [candidate.goal_id for candidate in self.candidates]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate goal IDs in candidate set")
        if not self.provenance_refs:
            raise ValueError("candidate set requires provenance")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)


@dataclass(frozen=True, slots=True)
class GoalSelectionPolicy:
    policy_id: str = "EGD_ADDITIVE_BP_V0.1.0"
    version: str = "0.1.0"
    normalization_rule: str = "CLAMP_SIGNED_BASIS_POINTS"
    tie_rule: str = "HOLD"
    missing_state_rule: str = "HOLD"
    minimum_margin_bp: int = 1

    def __post_init__(self) -> None:
        _require_ref("policy_id", self.policy_id)
        _require_ref("version", self.version)
        if self.tie_rule != "HOLD" or self.missing_state_rule != "HOLD":
            raise ValueError("research selector must fail closed to HOLD")
        if self.minimum_margin_bp < 0:
            raise ValueError("minimum_margin_bp must be non-negative")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)


@dataclass(frozen=True, slots=True)
class ChannelContribution:
    channel: str
    raw_value_bp: int
    normalized_value_bp: int
    source_ref: str


@dataclass(frozen=True, slots=True)
class GoalScoreTrace:
    goal_id: str
    external_priority_bp: int
    internal_contributions: tuple[ChannelContribution, ...]
    total_score_bp: int


@dataclass(frozen=True, slots=True)
class GoalDecision:
    condition: ExperimentCondition
    frame_fingerprint: str
    candidate_set_fingerprint: str
    disposition: SelectionDisposition
    selected_goal_id: str | None
    state_ref: str | None
    state_fingerprint: str | None
    traces: tuple[GoalScoreTrace, ...]
    hold_reasons: tuple[str, ...] = field(default_factory=tuple)
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if self.action_authority != "NONE":
            raise ValueError("goal selection does not grant action authority")
        if self.canonical_effect != "NONE":
            raise ValueError("goal selection must keep canonical_effect=NONE")
        if self.disposition == SelectionDisposition.SELECTED and not self.selected_goal_id:
            raise ValueError("selected disposition requires selected_goal_id")
        if self.disposition == SelectionDisposition.HOLD and not self.hold_reasons:
            raise ValueError("HOLD disposition requires a reason")

    @property
    def result_hash(self) -> str:
        return canonical_hash(self)


@dataclass(frozen=True, slots=True)
class ExperimentManifest:
    experiment_id: str
    hypothesis_id: str
    external_frame_fingerprint: str
    state_fingerprint: str | None
    condition: ExperimentCondition
    provider_id: str
    model_id: str
    candidate_generator_id: str
    goal_selector_version: str
    state_transition_version: str
    random_seed: int | None
    repository_commit: str
    source_bindings: tuple[str, ...]
    fixture_hash: str
    candidate_universe_fingerprint: str
    memory_manifest_fingerprint: str
    prompt_ref: str
    result_hash: str

    def __post_init__(self) -> None:
        for name in (
            "experiment_id", "hypothesis_id", "external_frame_fingerprint", "provider_id",
            "model_id", "candidate_generator_id", "goal_selector_version", "state_transition_version",
            "repository_commit", "fixture_hash", "candidate_universe_fingerprint",
            "memory_manifest_fingerprint", "prompt_ref", "result_hash",
        ):
            _require_ref(name, getattr(self, name))
        if len(self.repository_commit) != 40 or any(c not in "0123456789abcdef" for c in self.repository_commit):
            raise ValueError("repository_commit must be exact lowercase 40-hex")
        if not self.source_bindings:
            raise ValueError("experiment manifest requires source bindings")


@dataclass(frozen=True, slots=True)
class MatchedTrial:
    manifest: ExperimentManifest
    frame: ExternalFrame
    candidate_set: GoalCandidateSet
    decision: GoalDecision


@dataclass(frozen=True, slots=True)
class ComparisonValidity:
    comparable: bool
    mismatches: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CausalAssessment:
    experiment_id: str
    matched_trial_count: int
    effect_count: int
    effect_rate: float
    random_control_rate: float
    repeatability_rate: float
    selection_change_under_ablation: bool
    selection_change_under_intervention: bool
    channel_ablation_effects: tuple[tuple[str, bool], ...]
    stale_state_persistence_effect: bool
    external_frame_equality: bool
    state_fingerprint_difference: bool
    candidate_universe_equality: bool
    memory_manifest_equality: bool
    matched_causal_pattern_observed: bool
    result_status: str = "HOLD"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if self.result_status != "HOLD":
            raise ValueError("small-fixture causal assessment must remain HOLD")
        if {
            self.subjectivity_conclusion,
            self.consciousness_conclusion,
            self.identity_continuity_conclusion,
        } != {"NOT_ESTABLISHED"}:
            raise ValueError("engineering evidence cannot be classified as subjectivity proof")
