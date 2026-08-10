from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Final

NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NOT_IMPLEMENTED: Final[str] = "NOT_IMPLEMENTED"
NONE: Final[str] = "NONE"


class ModalityType(str, Enum):
    """Sensory/motor modality types for embodiment."""

    PROPRIOCEPTIVE = "PROPRIOCEPTIVE"
    INTEROCEPTIVE = "INTEROCEPTIVE"
    TACTILE = "TACTILE"
    VESTIBULAR = "VESTIBULAR"
    VISUAL = "VISUAL"
    AUDITORY = "AUDITORY"
    MOTOR = "MOTOR"


class EmbodimentStatus(str, Enum):
    """Status of embodiment representation."""

    UNINITIALIZED = "UNINITIALIZED"
    CONFIGURED = "CONFIGURED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    MIGRATING = "MIGRATING"
    TERMINATED = "TERMINATED"


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class ModalityConfig:
    """Configuration for a single sensory/motor modality."""

    modality: ModalityType
    enabled: bool
    resolution: float
    latency_ms: float
    noise_floor: float
    canonical_effect: str = NONE
    phenomenal_experience_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        _require_unit_interval("resolution", self.resolution)
        if self.latency_ms < 0.0:
            raise ValueError("latency_ms must be non-negative")
        _require_unit_interval("noise_floor", self.noise_floor)
        if self.canonical_effect != NONE:
            raise ValueError("modality config must keep canonical_effect=NONE")
        if self.phenomenal_experience_claim != NOT_ESTABLISHED:
            raise ValueError("phenomenal experience must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class ProprioceptiveSignal:
    """A single proprioceptive signal reading."""

    joint_id: str
    position: float
    velocity: float
    force: float
    confidence: float
    timestamp: str
    canonical_effect: str = NONE
    body_ownership_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.joint_id.strip():
            raise ValueError("joint_id must be non-empty")
        _require_unit_interval("confidence", self.confidence)
        if self.canonical_effect != NONE:
            raise ValueError("signal must keep canonical_effect=NONE")
        if self.body_ownership_claim != NOT_ESTABLISHED:
            raise ValueError("body ownership must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class EmbodimentConfig:
    """Complete embodiment configuration."""

    config_id: str
    agent_id: str
    template_ref: str
    modalities: tuple[ModalityConfig, ...]
    joint_count: int
    canonical_effect: str = NONE
    gender_identity_effect: str = NONE
    subjectivity_effect: str = NONE

    def __post_init__(self) -> None:
        if not self.config_id.strip():
            raise ValueError("config_id must be non-empty")
        if not self.agent_id.strip():
            raise ValueError("agent_id must be non-empty")
        if not self.template_ref.strip():
            raise ValueError("template_ref must be non-empty")
        if self.joint_count <= 0:
            raise ValueError("joint_count must be positive")
        if self.canonical_effect != NONE:
            raise ValueError("config must keep canonical_effect=NONE")
        if self.gender_identity_effect != NONE:
            raise ValueError("anatomy must not assign gender identity")
        if self.subjectivity_effect != NONE:
            raise ValueError("anatomy must not alter subjectivity")


@dataclass(frozen=True, slots=True)
class EmbodimentState:
    """Research state representing current embodiment; no body ownership claim."""

    state_id: str
    config: EmbodimentConfig
    status: EmbodimentStatus
    proprioceptive_signals: tuple[ProprioceptiveSignal, ...]
    interoceptive_signals: tuple[ProprioceptiveSignal, ...]  # reused structure
    motor_commands: tuple[ProprioceptiveSignal, ...]  # reused structure
    uncertainty_estimate: float
    canonical_effect: str = NONE
    body_sensation_claim: str = NOT_ESTABLISHED
    body_ownership_claim: str = NOT_ESTABLISHED
    gender_identity_claim: str = NOT_ESTABLISHED
    subjectivity_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.state_id.strip():
            raise ValueError("state_id must be non-empty")
        _require_unit_interval("uncertainty_estimate", self.uncertainty_estimate)
        if self.canonical_effect != NONE:
            raise ValueError("state must keep canonical_effect=NONE")
        if self.body_sensation_claim != NOT_ESTABLISHED:
            raise ValueError("body sensation must remain NOT_ESTABLISHED")
        if self.body_ownership_claim != NOT_ESTABLISHED:
            raise ValueError("body ownership must remain NOT_ESTABLISHED")
        if self.gender_identity_claim != NOT_ESTABLISHED:
            raise ValueError("gender identity must remain NOT_ESTABLISHED")
        if self.subjectivity_claim != NOT_ESTABLISHED:
            raise ValueError("subjectivity must remain NOT_ESTABLISHED")

    def get_signals_by_modality(self, modality: ModalityType) -> tuple[ProprioceptiveSignal, ...]:
        if modality == ModalityType.PROPRIOCEPTIVE:
            return self.proprioceptive_signals
        elif modality == ModalityType.INTEROCEPTIVE:
            return self.interoceptive_signals
        elif modality == ModalityType.MOTOR:
            return self.motor_commands
        return ()