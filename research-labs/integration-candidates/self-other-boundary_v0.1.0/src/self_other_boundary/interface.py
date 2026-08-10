from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .model import BoundaryConfiguration, BoundaryState, OtherModel
from .state import BoundaryStateManager, StateSnapshot, StateTransition


@dataclass(frozen=True, slots=True)
class BoundaryInput:
    """Input for boundary processing."""

    subject_ref: str
    config: BoundaryConfiguration
    other_models: tuple[OtherModel, ...]
    seed: int | None = None


@dataclass(frozen=True, slots=True)
class BoundaryOutput:
    """Output from boundary processing."""

    state: BoundaryState
    transitions: tuple[StateTransition, ...]
    canonical_effect: str = "NONE"
    empathy_claim: str = "NOT_ESTABLISHED"
    theory_of_mind_claim: str = "NOT_ESTABLISHED"


class SelfOtherBoundaryInterface(ABC):
    """Abstract interface for self-other boundary candidate integration."""

    MODULE_ID: str = "self-other-boundary"
    MODULE_VERSION: str = "0.1.1"

    @property
    @abstractmethod
    def manager(self) -> BoundaryStateManager:
        """Return the state manager."""

    @abstractmethod
    def process(self, input_data: BoundaryInput) -> BoundaryOutput:
        """Process boundary input and produce state."""

    @abstractmethod
    def reset(self) -> None:
        """Reset module to initial condition."""

    @abstractmethod
    def snapshot(self, snapshot_id: str | None = None) -> StateSnapshot:
        """Create a snapshot of current state."""

    @abstractmethod
    def restore(self, snapshot_id: str, *, allow_subject_switch: bool = False) -> BoundaryState:
        """Restore state, requiring an explicit opt-in for subject switching."""

    @abstractmethod
    def enable(self) -> None:
        """Enable the module."""

    @abstractmethod
    def disable(self) -> None:
        """Disable the module."""

    @abstractmethod
    def ablate(self, distinction: str | None = None) -> None:
        """Ablate a specific distinction or the entire module."""

    @abstractmethod
    def get_integration_points(self) -> dict[str, Any]:
        """Return integration points for downstream consumers."""

    @abstractmethod
    def validate_state(self, state: BoundaryState) -> tuple[bool, list[str]]:
        """Validate a state for consistency."""
