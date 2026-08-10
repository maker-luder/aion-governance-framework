from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Final

NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NOT_IMPLEMENTED: Final[str] = "NOT_IMPLEMENTED"
NONE: Final[str] = "NONE"


class TransitionType(str, Enum):
    """Types of longitudinal state transitions."""

    GRADUAL_DRIFT = "GRADUAL_DRIFT"           # Slow continuous change
    PHASE_SHIFT = "PHASE_SHIFT"               # Discrete phase change
    CRITICAL_TRANSITION = "CRITICAL_TRANSITION"  # Tipping point
    REVERSAL = "REVERSAL"                     # Direction reversal
    BIFURCATION = "BIFURCATION"               # Branching into alternatives
    CONVERGENCE = "CONVERGENCE"               # Merging of trajectories
    RESET = "RESET"                           # Return to baseline
    PERTURBATION = "PERTURBATION"             # External disruption


class TransitionDirection(str, Enum):
    """Direction of transition."""

    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"
    LATERAL = "LATERAL"
    OSCILLATORY = "OSCILLATORY"


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class TransitionEvent:
    """An event marking a state transition."""

    event_id: str
    transition_type: TransitionType
    direction: TransitionDirection
    magnitude: float
    from_state_signature: str
    to_state_signature: str
    timestamp: str
    deterministic_seed: int | None = None
    canonical_effect: str = NONE

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("event_id must be non-empty")
        if not self.from_state_signature.strip():
            raise ValueError("from_state_signature must be non-empty")
        if not self.to_state_signature.strip():
            raise ValueError("to_state_signature must be non-empty")
        _require_unit_interval("magnitude", self.magnitude)
        if self.canonical_effect != NONE:
            raise ValueError("event must keep canonical_effect=NONE")


@dataclass(frozen=True, slots=True)
class LongitudinalConfig:
    """Configuration for longitudinal state tracking."""

    config_id: str
    subject_ref: str
    tracked_dimensions: tuple[str, ...]
    window_size: int
    sensitivity_threshold: float
    canonical_effect: str = NONE
    trajectory_identity_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.config_id.strip():
            raise ValueError("config_id must be non-empty")
        if not self.subject_ref.strip():
            raise ValueError("subject_ref must be non-empty")
        if not self.tracked_dimensions:
            raise ValueError("at least one dimension must be tracked")
        if self.window_size <= 0:
            raise ValueError("window_size must be positive")
        _require_unit_interval("sensitivity_threshold", self.sensitivity_threshold)
        if self.canonical_effect != NONE:
            raise ValueError("config must keep canonical_effect=NONE")
        if self.trajectory_identity_claim != NOT_ESTABLISHED:
            raise ValueError("trajectory identity must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class LongitudinalState:
    """Research state representing longitudinal trajectory; no trajectory identity claim."""

    state_id: str
    config: LongitudinalConfig
    current_signature: str
    dimension_values: dict[str, float]
    trajectory_history: tuple[dict[str, float], ...]
    transition_events: tuple[TransitionEvent, ...]
    stability_index: float
    trend_direction: TransitionDirection
    canonical_effect: str = NONE
    trajectory_identity_claim: str = NOT_ESTABLISHED
    personal_continuity_claim: str = NOT_ESTABLISHED
    developmental_stage_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.state_id.strip():
            raise ValueError("state_id must be non-empty")
        if not self.current_signature.strip():
            raise ValueError("current_signature must be non-empty")
        for dim, val in self.dimension_values.items():
            if not 0.0 <= val <= 1.0:
                raise ValueError(f"dimension_values[{dim}] must be between 0.0 and 1.0")
        for point in self.trajectory_history:
            for dim, val in point.items():
                if not 0.0 <= val <= 1.0:
                    raise ValueError(f"trajectory_history point [{dim}] must be between 0.0 and 1.0")
        _require_unit_interval("stability_index", self.stability_index)
        if self.canonical_effect != NONE:
            raise ValueError("state must keep canonical_effect=NONE")
        if self.trajectory_identity_claim != NOT_ESTABLISHED:
            raise ValueError("trajectory identity must remain NOT_ESTABLISHED")
        if self.personal_continuity_claim != NOT_ESTABLISHED:
            raise ValueError("personal continuity must remain NOT_ESTABLISHED")
        if self.developmental_stage_claim != NOT_ESTABLISHED:
            raise ValueError("developmental stage must remain NOT_ESTABLISHED")

    def get_latest_event(self) -> TransitionEvent | None:
        return self.transition_events[-1] if self.transition_events else None

    def get_events_by_type(self, transition_type: TransitionType) -> tuple[TransitionEvent, ...]:
        return tuple(e for e in self.transition_events if e.transition_type == transition_type)

    def dimension_trend(self, dimension: str, window: int | None = None) -> float:
        if dimension not in self.dimension_values:
            return 0.0
        history = self.trajectory_history
        if window and window > 0:
            history = history[-window:]
        if len(history) < 2:
            return 0.0
        values = [h.get(dimension, 0.0) for h in history]
        return (values[-1] - values[0]) / len(values)

    def is_stable(self) -> bool:
        return self.stability_index >= self.config.sensitivity_threshold