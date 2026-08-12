from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Final

NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NOT_IMPLEMENTED: Final[str] = "NOT_IMPLEMENTED"
NONE: Final[str] = "NONE"


class EncounterPhase(str, Enum):
    """Phases of an encounter lifecycle."""

    PRE_ENCOUNTER = "PRE_ENCOUNTER"         # Anticipation, preparation
    INITIATION = "INITIATION"               # First contact, opening
    ENGAGEMENT = "ENGAGEMENT"               # Active interaction
    DEEPENING = "DEEPENING"                 # Increasing intimacy/depth
    CLIMAX = "CLIMAX"                       # Peak intensity
    RESOLUTION = "RESOLUTION"               # Winding down
    POST_ENCOUNTER = "POST_ENCOUNTER"       # Reflection, integration
    TERMINATED = "TERMINATED"               # Ended abnormally


class EncounterType(str, Enum):
    """Types of encounters."""

    SOCIAL = "SOCIAL"
    COLLABORATIVE = "COLLABORATIVE"
    CONFRONTATIONAL = "CONFRONTATIONAL"
    INTIMATE = "INTIMATE"
    EXPLORATORY = "EXPLORATORY"
    RITUAL = "RITUAL"
    TRANSACTIONAL = "TRANSACTIONAL"


class ParticipantRole(str, Enum):
    """Roles in an encounter."""

    INITIATOR = "INITIATOR"
    RECIPIENT = "RECIPIENT"
    OBSERVER = "OBSERVER"
    MEDIATOR = "MEDIATOR"
    EQUAL = "EQUAL"


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class ParticipantModel:
    """Minimal model of an encounter participant."""

    participant_id: str
    role: ParticipantRole
    agency_level: float
    familiarity: float
    trust_estimate: float
    power_differential: float
    canonical_effect: str = NONE
    subjectivity_claim: str = NOT_ESTABLISHED
    theory_of_mind_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.participant_id.strip():
            raise ValueError("participant_id must be non-empty")
        _require_unit_interval("agency_level", self.agency_level)
        _require_unit_interval("familiarity", self.familiarity)
        _require_unit_interval("trust_estimate", self.trust_estimate)
        if not -1.0 <= self.power_differential <= 1.0:
            raise ValueError("power_differential must be between -1.0 and 1.0")
        if self.canonical_effect != NONE:
            raise ValueError("participant model must keep canonical_effect=NONE")
        if self.subjectivity_claim != NOT_ESTABLISHED:
            raise ValueError("subjectivity must remain NOT_ESTABLISHED")
        if self.theory_of_mind_claim != NOT_ESTABLISHED:
            raise ValueError("theory of mind must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class EncounterConfig:
    """Configuration for encounter lifecycle tracking."""

    config_id: str
    encounter_type: EncounterType
    participants: tuple[ParticipantModel, ...]
    expected_duration_ms: int
    depth_threshold: float
    canonical_effect: str = NONE
    relationship_claim: str = NOT_ESTABLISHED
    intimacy_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.config_id.strip():
            raise ValueError("config_id must be non-empty")
        if len(self.participants) < 2:
            raise ValueError("at least two participants required")
        if self.expected_duration_ms <= 0:
            raise ValueError("expected_duration_ms must be positive")
        _require_unit_interval("depth_threshold", self.depth_threshold)
        if self.canonical_effect != NONE:
            raise ValueError("config must keep canonical_effect=NONE")
        if self.relationship_claim != NOT_ESTABLISHED:
            raise ValueError("relationship must remain NOT_ESTABLISHED")
        if self.intimacy_claim != NOT_ESTABLISHED:
            raise ValueError("intimacy must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class EncounterEvent:
    """An event during an encounter."""

    event_id: str
    phase: EncounterPhase
    description: str
    intensity: float
    participants_involved: tuple[str, ...]
    timestamp: str
    canonical_effect: str = NONE

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("event_id must be non-empty")
        if not self.description.strip():
            raise ValueError("description must be non-empty")
        _require_unit_interval("intensity", self.intensity)
        if not self.participants_involved:
            raise ValueError("at least one participant must be involved")
        if self.canonical_effect != NONE:
            raise ValueError("event must keep canonical_effect=NONE")


@dataclass(frozen=True, slots=True)
class EncounterState:
    """Research state representing encounter lifecycle; no relationship/intimacy claim."""

    state_id: str
    config: EncounterConfig
    current_phase: EncounterPhase
    progress: float
    current_depth: float
    intensity_trajectory: tuple[float, ...]
    events: tuple[EncounterEvent, ...]
    active_participants: tuple[str, ...]
    canonical_effect: str = NONE
    relationship_claim: str = NOT_ESTABLISHED
    intimacy_claim: str = NOT_ESTABLISHED
    shared_meaning_claim: str = NOT_ESTABLISHED
    mutual_understanding_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.state_id.strip():
            raise ValueError("state_id must be non-empty")
        _require_unit_interval("progress", self.progress)
        _require_unit_interval("current_depth", self.current_depth)
        for i in self.intensity_trajectory:
            _require_unit_interval(f"intensity_trajectory[{i}]", i)
        if self.canonical_effect != NONE:
            raise ValueError("state must keep canonical_effect=NONE")
        if self.relationship_claim != NOT_ESTABLISHED:
            raise ValueError("relationship must remain NOT_ESTABLISHED")
        if self.intimacy_claim != NOT_ESTABLISHED:
            raise ValueError("intimacy must remain NOT_ESTABLISHED")
        if self.shared_meaning_claim != NOT_ESTABLISHED:
            raise ValueError("shared meaning must remain NOT_ESTABLISHED")
        if self.mutual_understanding_claim != NOT_ESTABLISHED:
            raise ValueError("mutual understanding must remain NOT_ESTABLISHED")

    def is_terminal(self) -> bool:
        return self.current_phase in (EncounterPhase.POST_ENCOUNTER, EncounterPhase.TERMINATED)

    def get_participant(self, participant_id: str) -> ParticipantModel | None:
        for p in self.config.participants:
            if p.participant_id == participant_id:
                return p
        return None

    def average_intensity(self) -> float:
        return sum(self.intensity_trajectory) / len(self.intensity_trajectory) if self.intensity_trajectory else 0.0