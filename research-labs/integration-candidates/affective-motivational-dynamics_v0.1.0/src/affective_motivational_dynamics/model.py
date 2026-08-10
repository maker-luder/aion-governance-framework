from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Final

NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NOT_IMPLEMENTED: Final[str] = "NOT_IMPLEMENTED"
NONE: Final[str] = "NONE"


class SignalDomain(str, Enum):
    """Domains of motivational signals."""

    HOMEOSTATIC = "HOMEOSTATIC"
    SOCIAL_AFFILIATION = "SOCIAL_AFFILIATION"
    EXPLORATION = "EXPLORATION"
    AESTHETIC_ATTRACTION = "AESTHETIC_ATTRACTION"
    ADULT_SEXUALITY_SCHEMA = "ADULT_SEXUALITY_SCHEMA"
    SELF_PRESERVATION = "SELF_PRESERVATION"
    KNOWLEDGE_ACQUISITION = "KNOWLEDGE_ACQUISITION"


class AffectiveValence(str, Enum):
    """Affective valence categories; no felt experience claim."""

    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    MIXED = "MIXED"
    INDETERMINATE = "INDETERMINATE"


class MotivationalDirection(str, Enum):
    """Direction of motivational force."""

    APPROACH = "APPROACH"
    AVOIDANCE = "AVOIDANCE"
    CONFLICT = "CONFLICT"
    NEUTRAL = "NEUTRAL"


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class MotivationalSignal:
    """A single motivational signal with affective and directional components."""

    signal_id: str
    domain: SignalDomain
    source_event_id: str
    valence: AffectiveValence
    intensity: float
    wanting: float
    predicted_liking: float
    approach: float
    avoidance: float
    uncertainty: float
    direction: MotivationalDirection
    context_tags: tuple[str, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    canonical_effect: str = NONE
    felt_experience_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.signal_id.strip():
            raise ValueError("signal_id must be non-empty")
        if not self.source_event_id.strip():
            raise ValueError("source_event_id must be non-empty")
        if not self.evidence_refs:
            raise ValueError("at least one evidence_ref is required")
        for name in ("intensity", "wanting", "predicted_liking", "approach", "avoidance", "uncertainty"):
            _require_unit_interval(name, getattr(self, name))
        if self.canonical_effect != NONE:
            raise ValueError("signal must keep canonical_effect=NONE")
        if self.felt_experience_claim != NOT_ESTABLISHED:
            raise ValueError("felt experience must remain NOT_ESTABLISHED")

    @property
    def approach_avoidance_conflict(self) -> bool:
        return self.approach > 0.0 and self.avoidance > 0.0

    @property
    def wanting_liking_discrepancy(self) -> float:
        return abs(self.wanting - self.predicted_liking)


@dataclass(frozen=True, slots=True)
class MotivationalState:
    """Research state representing affective-motivational dynamics; no feeling claim."""

    state_id: str
    subject_ref: str
    context_ref: str
    signals: tuple[MotivationalSignal, ...]
    global_valence: AffectiveValence
    dominant_direction: MotivationalDirection
    conflict_index: float
    uncertainty_aggregate: float
    canonical_effect: str = NONE
    felt_experience_claim: str = NOT_ESTABLISHED
    hedonic_tone_claim: str = NOT_ESTABLISHED
    motivational_authority_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.state_id.strip():
            raise ValueError("state_id must be non-empty")
        if not self.subject_ref.strip():
            raise ValueError("subject_ref must be non-empty")
        if not self.context_ref.strip():
            raise ValueError("context_ref must be non-empty")
        if not self.signals:
            raise ValueError("at least one motivational signal is required")
        _require_unit_interval("conflict_index", self.conflict_index)
        _require_unit_interval("uncertainty_aggregate", self.uncertainty_aggregate)
        if self.canonical_effect != NONE:
            raise ValueError("state must keep canonical_effect=NONE")
        if self.felt_experience_claim != NOT_ESTABLISHED:
            raise ValueError("felt experience must remain NOT_ESTABLISHED")
        if self.hedonic_tone_claim != NOT_ESTABLISHED:
            raise ValueError("hedonic tone must remain NOT_ESTABLISHED")
        if self.motivational_authority_claim != NOT_ESTABLISHED:
            raise ValueError("motivational authority must remain NOT_ESTABLISHED")

    def get_signals_by_domain(self, domain: SignalDomain) -> tuple[MotivationalSignal, ...]:
        return tuple(s for s in self.signals if s.domain == domain)

    def get_signals_by_direction(self, direction: MotivationalDirection) -> tuple[MotivationalSignal, ...]:
        return tuple(s for s in self.signals if s.direction == direction)

    def total_approach(self) -> float:
        return sum(s.approach for s in self.signals)

    def total_avoidance(self) -> float:
        return sum(s.avoidance for s in self.signals)