from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .model import LongitudinalConfig, LongitudinalState
from .state import LongitudinalStateManager, StateSnapshot, StateTransition


@dataclass(frozen=True, slots=True)
class LongitudinalInput:
    """Input for longitudinal state processing."""

    config: LongitudinalConfig
    initial_values: dict[str, float]
    seed: int | None = None


@dataclass(frozen=True, slots=True)
class LongitudinalOutput:
    """Output from longitudinal state processing."""

    state: LongitudinalState
    transitions: tuple[StateTransition, ...]
    canonical_effect: str = "NONE"
    trajectory_identity_claim: str = "NOT_ESTABLISHED"
    personal_continuity_claim: str = "NOT_ESTABLISHED"
    developmental_stage_claim: str = "NOT_ESTABLISHED"


class LongitudinalStateTransitionInterface(ABC):
    """Abstract interface for longitudinal state transition module."""

    MODULE_ID: str = "longitudinal-state-transition"
    MODULE_VERSION: str = "0.1.0"

    @property
    @abstractmethod
    def manager(self) -> LongitudinalStateManager:
        """Return the state manager."""

    @abstractmethod
    def process(self, input_data: LongitudinalInput) -> LongitudinalOutput:
        """Process longitudinal input and produce state."""

    @abstractmethod
    def reset(self) -> None:
        """Reset module to initial condition."""

    @abstractmethod
    def snapshot(self, snapshot_id: str | None = None) -> StateSnapshot:
        """Create a snapshot of current state."""

    @abstractmethod
    def restore(self, snapshot_id: str) -> LongitudinalState:
        """Restore state from snapshot."""

    @abstractmethod
    def enable(self) -> None:
        """Enable the module."""

    @abstractmethod
    def disable(self) -> None:
        """Disable the module."""

    @abstractmethod
    def ablate(self, dimension: str | None = None) -> None:
        """Ablate dimension or entire module."""

    @abstractmethod
    def get_integration_points(self) -> dict[str, Any]:
        """Return integration points for downstream consumers."""

    @abstractmethod
    def validate_state(self, state: LongitudinalState) -> tuple[bool, list[str]]:
        """Validate a state for consistency."""