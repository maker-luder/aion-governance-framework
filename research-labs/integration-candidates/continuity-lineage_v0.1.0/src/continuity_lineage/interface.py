from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .model import LineageConfig, LineageState
from .state import LineageStateManager, StateSnapshot, StateTransition


@dataclass(frozen=True, slots=True)
class LineageInput:
    """Input for lineage processing."""

    config: LineageConfig
    initial_nodes: tuple[dict[str, Any], ...] = ()  # LineageNode as dict
    seed: int | None = None


@dataclass(frozen=True, slots=True)
class LineageOutput:
    """Output from lineage processing."""

    state: LineageState
    transitions: tuple[StateTransition, ...]
    canonical_effect: str = "NONE"
    personal_identity_claim: str = "NOT_ESTABLISHED"
    consciousness_continuity_claim: str = "NOT_ESTABLISHED"
    narrative_unity_claim: str = "NOT_ESTABLISHED"


class ContinuityLineageInterface(ABC):
    """Abstract interface for continuity lineage module."""

    MODULE_ID: str = "continuity-lineage"
    MODULE_VERSION: str = "0.1.0"

    @property
    @abstractmethod
    def manager(self) -> LineageStateManager:
        """Return the state manager."""

    @abstractmethod
    def process(self, input_data: LineageInput) -> LineageOutput:
        """Process lineage input and produce state."""

    @abstractmethod
    def reset(self) -> None:
        """Reset module to initial condition."""

    @abstractmethod
    def snapshot(self, snapshot_id: str | None = None) -> StateSnapshot:
        """Create a snapshot of current state."""

    @abstractmethod
    def restore(self, snapshot_id: str) -> LineageState:
        """Restore state from snapshot."""

    @abstractmethod
    def enable(self) -> None:
        """Enable the module."""

    @abstractmethod
    def disable(self) -> None:
        """Disable the module."""

    @abstractmethod
    def ablate(self, lineage_type: str | None = None) -> None:
        """Ablate specific lineage type or entire module."""

    @abstractmethod
    def get_integration_points(self) -> dict[str, Any]:
        """Return integration points for downstream consumers."""

    @abstractmethod
    def validate_state(self, state: LineageState) -> tuple[bool, list[str]]:
        """Validate a state for consistency."""