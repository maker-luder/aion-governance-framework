from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .model import EncounterConfig, EncounterState
from .state import EncounterStateManager, StateSnapshot, StateTransition


@dataclass(frozen=True, slots=True)
class EncounterInput:
    """Input for encounter processing."""

    config: EncounterConfig
    seed: int | None = None


@dataclass(frozen=True, slots=True)
class EncounterOutput:
    """Output from encounter processing."""

    state: EncounterState
    transitions: tuple[StateTransition, ...]
    canonical_effect: str = "NONE"
    relationship_claim: str = "NOT_ESTABLISHED"
    intimacy_claim: str = "NOT_ESTABLISHED"
    shared_meaning_claim: str = "NOT_ESTABLISHED"
    mutual_understanding_claim: str = "NOT_ESTABLISHED"


class EncounterLifecycleInterface(ABC):
    """Abstract interface for encounter lifecycle module."""

    MODULE_ID: str = "encounter-lifecycle"
    MODULE_VERSION: str = "0.1.0"

    @property
    @abstractmethod
    def manager(self) -> EncounterStateManager:
        """Return the state manager."""

    @abstractmethod
    def process(self, input_data: EncounterInput) -> EncounterOutput:
        """Process encounter input and produce state."""

    @abstractmethod
    def reset(self) -> None:
        """Reset module to initial condition."""

    @abstractmethod
    def snapshot(self, snapshot_id: str | None = None) -> StateSnapshot:
        """Create a snapshot of current state."""

    @abstractmethod
    def restore(self, snapshot_id: str) -> EncounterState:
        """Restore state from snapshot."""

    @abstractmethod
    def enable(self) -> None:
        """Enable the module."""

    @abstractmethod
    def disable(self) -> None:
        """Disable the module."""

    @abstractmethod
    def ablate(self, participant_id: str | None = None) -> None:
        """Ablate participant or entire module."""

    @abstractmethod
    def get_integration_points(self) -> dict[str, Any]:
        """Return integration points for downstream consumers."""

    @abstractmethod
    def validate_state(self, state: EncounterState) -> tuple[bool, list[str]]:
        """Validate a state for consistency."""