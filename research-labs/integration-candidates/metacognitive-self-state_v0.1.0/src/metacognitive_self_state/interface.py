from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .model import MetacognitiveState, SelfModelComponent
from .state import MetacognitiveStateManager, StateSnapshot, StateTransition


@dataclass(frozen=True, slots=True)
class MetacognitiveInput:
    """Input for metacognitive processing."""

    subject_ref: str
    context_ref: str
    layer: str
    capacity: str
    confidence: float
    evidence_refs: tuple[str, ...]
    seed: int | None = None


@dataclass(frozen=True, slots=True)
class MetacognitiveOutput:
    """Output from metacognitive processing."""

    state: MetacognitiveState
    transitions: tuple[StateTransition, ...]
    canonical_effect: str = "NONE"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"


class MetacognitiveSelfStateInterface(ABC):
    """Abstract interface for metacognitive self-state module."""

    MODULE_ID: str = "metacognitive-self-state"
    MODULE_VERSION: str = "0.1.0"

    @property
    @abstractmethod
    def manager(self) -> MetacognitiveStateManager:
        """Return the state manager."""

    @abstractmethod
    def process(self, input_data: MetacognitiveInput) -> MetacognitiveOutput:
        """Process metacognitive input and produce state."""

    @abstractmethod
    def reset(self) -> None:
        """Reset module to initial condition."""

    @abstractmethod
    def snapshot(self, snapshot_id: str | None = None) -> StateSnapshot:
        """Create a snapshot of current state."""

    @abstractmethod
    def restore(self, snapshot_id: str) -> MetacognitiveState:
        """Restore state from snapshot."""

    @abstractmethod
    def enable(self) -> None:
        """Enable the module."""

    @abstractmethod
    def disable(self) -> None:
        """Disable the module."""

    @abstractmethod
    def ablate(self, capacity: str | None = None) -> None:
        """Ablate specific capacity or entire module."""

    @abstractmethod
    def get_integration_points(self) -> dict[str, Any]:
        """Return integration points for downstream consumers."""

    @abstractmethod
    def validate_state(self, state: MetacognitiveState) -> tuple[bool, list[str]]:
        """Validate a state for consistency."""