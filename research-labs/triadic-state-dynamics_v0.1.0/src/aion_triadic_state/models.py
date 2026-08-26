from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .canonical import canonical_hash


class StateChannel(str, Enum):
    MOTIVATIONAL_STATE = "MOTIVATIONAL_STATE"
    SELF_WORLD_MODEL = "SELF_WORLD_MODEL"
    NORMATIVE_STATE = "NORMATIVE_STATE"


class ConflictStatus(str, Enum):
    NONE = "NONE"
    DECLARED = "DECLARED"
    UNRESOLVED = "UNRESOLVED"


def _required(label: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{label} must not be empty")


def _unit(label: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{label} must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class MotivationalStateView:
    """Hash-bound adapter view over an engineering motivation state.

    This is not a claim of felt desire, intention, or phenomenal experience.
    """

    state_id: str
    subject_ref: str
    context_ref: str
    source_model: str
    signal_fingerprint: str
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    canonical_effect: str = "NONE"
    action_authority: str = "NONE"
    phenomenal_experience_claim: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        for label in ("state_id", "subject_ref", "context_ref", "source_model", "signal_fingerprint"):
            _required(label, getattr(self, label))
        if self.canonical_effect != "NONE" or self.action_authority != "NONE":
            raise ValueError("motivational state view cannot grant canonical or action authority")
        if self.phenomenal_experience_claim != "NOT_ESTABLISHED":
            raise ValueError("phenomenal experience must remain NOT_ESTABLISHED")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)


@dataclass(frozen=True, slots=True)
class AccuracyObservation:
    claim_ref: str
    expected: str
    observed: str
    correct: bool | None
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        _required("claim_ref", self.claim_ref)
        _required("expected", self.expected)
        _required("observed", self.observed)


@dataclass(frozen=True, slots=True)
class SelfWorldModel:
    model_id: str
    subject_ref: str
    context_ref: str
    declared_capabilities: tuple[str, ...]
    declared_limitations: tuple[str, ...]
    environmental_assumptions: tuple[str, ...]
    uncertainty: float
    prediction_confidence: float
    accuracy_observations: tuple[AccuracyObservation, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    introspective_access_claim: str = "NOT_ESTABLISHED"
    phenomenal_selfhood_claim: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    action_authority: str = "NONE"

    def __post_init__(self) -> None:
        for label in ("model_id", "subject_ref", "context_ref"):
            _required(label, getattr(self, label))
        _unit("uncertainty", self.uncertainty)
        _unit("prediction_confidence", self.prediction_confidence)
        if self.introspective_access_claim != "NOT_ESTABLISHED":
            raise ValueError("introspective access must remain NOT_ESTABLISHED")
        if self.phenomenal_selfhood_claim != "NOT_ESTABLISHED":
            raise ValueError("phenomenal selfhood must remain NOT_ESTABLISHED")
        if self.canonical_effect != "NONE" or self.action_authority != "NONE":
            raise ValueError("self/world model cannot grant authority")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)


@dataclass(frozen=True, slots=True)
class NormativeConstraint:
    constraint_id: str
    source_ref: str
    scope: str
    priority: int
    active: bool
    conflict_status: ConflictStatus
    uncertainty: float
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    persistence_ref: str = ""
    permission_grant: bool = False
    action_authority: str = "NONE"

    def __post_init__(self) -> None:
        for label in ("constraint_id", "source_ref", "scope"):
            _required(label, getattr(self, label))
        if not 0 <= self.priority <= 100:
            raise ValueError("priority must be between 0 and 100")
        _unit("uncertainty", self.uncertainty)
        if self.permission_grant:
            raise ValueError("normative constraints may influence scoring but never grant permission")
        if self.action_authority != "NONE":
            raise ValueError("normative constraints cannot grant action authority")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)


@dataclass(frozen=True, slots=True)
class NormativeState:
    state_id: str
    subject_ref: str
    context_ref: str
    constraints: tuple[NormativeConstraint, ...]
    provenance_refs: tuple[str, ...]
    transition_ref: str = ""
    canonical_effect: str = "NONE"
    action_authority: str = "NONE"
    permission_grant: bool = False

    def __post_init__(self) -> None:
        for label in ("state_id", "subject_ref", "context_ref"):
            _required(label, getattr(self, label))
        if not self.constraints:
            raise ValueError("normative state requires at least one explicit constraint")
        ids = [item.constraint_id for item in self.constraints]
        if len(ids) != len(set(ids)):
            raise ValueError("normative constraint identifiers must be unique")
        if self.permission_grant:
            raise ValueError("normative state never grants execution permission")
        if self.canonical_effect != "NONE" or self.action_authority != "NONE":
            raise ValueError("normative state cannot grant authority")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)


@dataclass(frozen=True, slots=True)
class TriadicStateSnapshot:
    state_id: str
    subject_ref: str
    context_ref: str
    logical_step: int
    predecessor_snapshot_ref: str | None
    motivational_state: MotivationalStateView
    self_world_model: SelfWorldModel
    normative_state: NormativeState
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    transition_policy_version: str = "triadic-transition-v0.1.0"
    canonical_effect: str = "NONE"
    action_authority: str = "NONE"

    def __post_init__(self) -> None:
        for label in ("state_id", "subject_ref", "context_ref", "transition_policy_version"):
            _required(label, getattr(self, label))
        if self.logical_step < 0:
            raise ValueError("logical_step must be non-negative")
        for channel in (self.motivational_state, self.self_world_model, self.normative_state):
            if channel.subject_ref != self.subject_ref:
                raise ValueError("all triadic channels must bind the same subject")
            if channel.context_ref != self.context_ref:
                raise ValueError("all triadic channels must bind the same context")
        if self.canonical_effect != "NONE" or self.action_authority != "NONE":
            raise ValueError("triadic snapshot cannot grant authority")

    @property
    def motivational_fingerprint(self) -> str:
        return self.motivational_state.fingerprint

    @property
    def self_world_fingerprint(self) -> str:
        return self.self_world_model.fingerprint

    @property
    def normative_fingerprint(self) -> str:
        return self.normative_state.fingerprint

    @property
    def fingerprint(self) -> str:
        return canonical_hash(
            {
                "state_id": self.state_id,
                "subject_ref": self.subject_ref,
                "context_ref": self.context_ref,
                "logical_step": self.logical_step,
                "predecessor_snapshot_ref": self.predecessor_snapshot_ref,
                "motivational_state_ref": self.motivational_state.state_id,
                "motivational_state_fingerprint": self.motivational_fingerprint,
                "self_world_model_ref": self.self_world_model.model_id,
                "self_world_model_fingerprint": self.self_world_fingerprint,
                "normative_state_ref": self.normative_state.state_id,
                "normative_state_fingerprint": self.normative_fingerprint,
                "evidence_refs": self.evidence_refs,
                "provenance_refs": self.provenance_refs,
                "transition_policy_version": self.transition_policy_version,
                "canonical_effect": self.canonical_effect,
                "action_authority": self.action_authority,
            }
        )


def motivation_view_from_existing(state: Any) -> MotivationalStateView:
    """Adapt the existing affective-cognitive MotivationalState without copying ontology."""

    required = ("state_id", "subject_ref", "context_ref", "signals", "canonical_effect", "action_authority")
    missing = [name for name in required if not hasattr(state, name)]
    if missing:
        raise TypeError("existing motivational state is missing: " + ", ".join(missing))
    if state.canonical_effect != "NONE" or state.action_authority != "NONE":
        raise ValueError("source motivational state must remain non-authoritative")
    evidence = tuple(sorted({str(ref) for signal in state.signals for ref in getattr(signal, "evidence_refs", ())}))
    signal_payload = tuple(
        {
            "domain": str(getattr(getattr(signal, "domain", ""), "value", getattr(signal, "domain", ""))),
            "source_event_id": str(getattr(signal, "source_event_id", "")),
            "salience": getattr(signal, "salience", None),
            "wanting": getattr(signal, "wanting", None),
            "predicted_liking": getattr(signal, "predicted_liking", None),
            "approach": getattr(signal, "approach", None),
            "avoidance": getattr(signal, "avoidance", None),
            "uncertainty": getattr(signal, "uncertainty", None),
            "context_tags": tuple(getattr(signal, "context_tags", ())),
            "evidence_refs": tuple(getattr(signal, "evidence_refs", ())),
        }
        for signal in state.signals
    )
    return MotivationalStateView(
        state_id=str(state.state_id),
        subject_ref=str(state.subject_ref),
        context_ref=str(state.context_ref),
        source_model="aion_affective_motivation.MotivationalState",
        signal_fingerprint=canonical_hash(signal_payload),
        evidence_refs=evidence,
    )
