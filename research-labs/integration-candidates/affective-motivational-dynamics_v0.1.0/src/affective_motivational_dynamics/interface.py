from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .model import MotivationalState
from .state import DynamicsStateManager, StateSnapshot, StateTransition


@dataclass(frozen=True, slots=True)
class DynamicsInput:
    """Input for affective-motivational processing."""

    subject_ref: str
    context_ref: str
    signals: tuple[dict[str, Any], ...]  # MotivationalSignal as dict
    seed: int | None = None


@dataclass(frozen=True, slots=True)
class DynamicsOutput:
    """Output from affective-motivational processing."""

    state: MotivationalState
    transitions: tuple[StateTransition, ...]
    canonical_effect: str = "NONE"
    felt_experience_claim: str = "NOT_ESTABLISHED"
    hedonic_tone_claim: str = "NOT_ESTABLISHED"


class AffectiveMotivationalInterface(ABC):
    """Abstract interface for affective-motivational dynamics module."""

    MODULE_ID: str = "affective-motivational-dynamics"
    MODULE_VERSION: str = "0.1.0"

    @property
    @abstractmethod
    def manager(self) -> DynamicsStateManager:
        """Return the state manager."""

    @abstractmethod
    def process(self, input_data: DynamicsInput) -> DynamicsOutput:
        """Process dynamics input and produce state."""

    @abstractmethod
    def reset(self) -> None:
        """Reset module to initial condition."""

    @abstractmethod
    def snapshot(self, snapshot_id: str | None = None) -> StateSnapshot:
        """Create a snapshot of current state."""

    @abstractmethod
    def restore(self, snapshot_id: str) -> MotivationalState:
        """Restore state from snapshot."""

    @abstractmethod
    def enable(self) -> None:
        """Enable the module."""

    @abstractmethod
    def disable(self) -> None:
        """Disable the module."""

    @abstractmethod
    def ablate(self, domain: str | None = None) -> None:
        """Ablate specific domain or entire module."""

    @abstractmethod
    def get_integration_points(self) -> dict[str, Any]:
        """Return integration points for downstream consumers."""

    @abstractmethod
    def validate_state(self, state: MotivationalState) -> tuple[bool, list[str]]:
        """Validate a state for consistency."""