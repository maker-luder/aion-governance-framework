from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Final

NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NOT_IMPLEMENTED: Final[str] = "NOT_IMPLEMENTED"
NONE: Final[str] = "NONE"


class MigrationPhase(str, Enum):
    """Phases of embodiment migration."""

    PREPARATION = "PREPARATION"
    VALIDATION = "VALIDATION"
    TRANSFER = "TRANSFER"
    INTEGRATION = "INTEGRATION"
    VERIFICATION = "VERIFICATION"
    COMPLETE = "COMPLETE"
    ROLLBACK = "ROLLBACK"
    FAILED = "FAILED"


class MigrationTrigger(str, Enum):
    """Triggers for migration."""

    HARDWARE_UPGRADE = "HARDWARE_UPGRADE"
    SOFTWARE_UPDATE = "SOFTWARE_UPDATE"
    CONTINUITY_PRESERVATION = "CONTINUITY_PRESERVATION"
    EXPERIMENTAL_CONDITION = "EXPERIMENTAL_CONDITION"
    EMERGENCY_FALLBACK = "EMERGENCY_FALLBACK"


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class SourceTargetPair:
    """Source and target embodiment specifications."""

    source_embodiment_id: str
    target_embodiment_id: str
    source_template_ref: str
    target_template_ref: str
    compatibility_score: float
    canonical_effect: str = NONE
    identity_preservation_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.source_embodiment_id.strip():
            raise ValueError("source_embodiment_id must be non-empty")
        if not self.target_embodiment_id.strip():
            raise ValueError("target_embodiment_id must be non-empty")
        if not self.source_template_ref.strip():
            raise ValueError("source_template_ref must be non-empty")
        if not self.target_template_ref.strip():
            raise ValueError("target_template_ref must be non-empty")
        _require_unit_interval("compatibility_score", self.compatibility_score)
        if self.canonical_effect != NONE:
            raise ValueError("pair must keep canonical_effect=NONE")
        if self.identity_preservation_claim != NOT_ESTABLISHED:
            raise ValueError("identity preservation must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class MigrationConfig:
    """Configuration for embodiment migration."""

    config_id: str
    agent_id: str
    pair: SourceTargetPair
    trigger: MigrationTrigger
    max_duration_ms: int
    fidelity_threshold: float
    rollback_enabled: bool
    canonical_effect: str = NONE
    continuity_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.config_id.strip():
            raise ValueError("config_id must be non-empty")
        if not self.agent_id.strip():
            raise ValueError("agent_id must be non-empty")
        if self.max_duration_ms <= 0:
            raise ValueError("max_duration_ms must be positive")
        _require_unit_interval("fidelity_threshold", self.fidelity_threshold)
        if self.canonical_effect != NONE:
            raise ValueError("config must keep canonical_effect=NONE")
        if self.continuity_claim != NOT_ESTABLISHED:
            raise ValueError("continuity must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class MigrationEvent:
    """An event during migration."""

    event_id: str
    phase: MigrationPhase
    description: str
    fidelity: float
    timestamp: str
    canonical_effect: str = NONE

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("event_id must be non-empty")
        if not self.description.strip():
            raise ValueError("description must be non-empty")
        _require_unit_interval("fidelity", self.fidelity)
        if self.canonical_effect != NONE:
            raise ValueError("event must keep canonical_effect=NONE")


@dataclass(frozen=True, slots=True)
class MigrationState:
    """Research state representing embodiment migration; no identity continuity claim."""

    state_id: str
    config: MigrationConfig
    current_phase: MigrationPhase
    progress: float
    fidelity_achieved: float
    events: tuple[MigrationEvent, ...]
    rollback_initiated: bool
    canonical_effect: str = NONE
    identity_continuity_claim: str = NOT_ESTABLISHED
    subjectivity_preservation_claim: str = NOT_ESTABLISHED
    personal_identity_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.state_id.strip():
            raise ValueError("state_id must be non-empty")
        _require_unit_interval("progress", self.progress)
        _require_unit_interval("fidelity_achieved", self.fidelity_achieved)
        if self.canonical_effect != NONE:
            raise ValueError("state must keep canonical_effect=NONE")
        if self.identity_continuity_claim != NOT_ESTABLISHED:
            raise ValueError("identity continuity must remain NOT_ESTABLISHED")
        if self.subjectivity_preservation_claim != NOT_ESTABLISHED:
            raise ValueError("subjectivity preservation must remain NOT_ESTABLISHED")
        if self.personal_identity_claim != NOT_ESTABLISHED:
            raise ValueError("personal identity must remain NOT_ESTABLISHED")

    def is_terminal(self) -> bool:
        return self.current_phase in (MigrationPhase.COMPLETE, MigrationPhase.ROLLBACK, MigrationPhase.FAILED)

    def get_latest_event(self) -> MigrationEvent | None:
        return self.events[-1] if self.events else None