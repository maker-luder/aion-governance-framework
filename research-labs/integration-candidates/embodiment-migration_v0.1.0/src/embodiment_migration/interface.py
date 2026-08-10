from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .model import MigrationConfig, MigrationState
from .state import MigrationStateManager, StateSnapshot, StateTransition


@dataclass(frozen=True, slots=True)
class MigrationInput:
    """Input for migration processing."""

    config: MigrationConfig
    seed: int | None = None


@dataclass(frozen=True, slots=True)
class MigrationOutput:
    """Output from migration processing."""

    state: MigrationState
    transitions: tuple[StateTransition, ...]
    canonical_effect: str = "NONE"
    identity_continuity_claim: str = "NOT_ESTABLISHED"
    subjectivity_preservation_claim: str = "NOT_ESTABLISHED"
    personal_identity_claim: str = "NOT_ESTABLISHED"


class EmbodimentMigrationInterface(ABC):
    """Abstract interface for embodiment migration module."""

    MODULE_ID: str = "embodiment-migration"
    MODULE_VERSION: str = "0.1.0"

    @property
    @abstractmethod
    def manager(self) -> MigrationStateManager:
        """Return the state manager."""

    @abstractmethod
    def process(self, input_data: MigrationInput) -> MigrationOutput:
        """Process migration input and produce state."""

    @abstractmethod
    def reset(self) -> None:
        """Reset module to initial condition."""

    @abstractmethod
    def snapshot(self, snapshot_id: str | None = None) -> StateSnapshot:
        """Create a snapshot of current state."""

    @abstractmethod
    def restore(self, snapshot_id: str) -> MigrationState:
        """Restore state from snapshot."""

    @abstractmethod
    def enable(self) -> None:
        """Enable the module."""

    @abstractmethod
    def disable(self) -> None:
        """Disable the module."""

    @abstractmethod
    def ablate(self, phase: str | None = None) -> None:
        """Ablate specific phase or entire module."""

    @abstractmethod
    def get_integration_points(self) -> dict[str, Any]:
        """Return integration points for downstream consumers."""

    @abstractmethod
    def validate_state(self, state: MigrationState) -> tuple[bool, list[str]]:
        """Validate a state for consistency."""