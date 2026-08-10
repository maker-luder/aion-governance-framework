from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .model import EmbodimentConfig, EmbodimentState
from .state import EmbodimentStateManager, StateSnapshot, StateTransition


@dataclass(frozen=True, slots=True)
class EmbodimentInput:
    """Input for embodiment processing."""

    agent_id: str
    template_ref: str
    joint_count: int
    modalities: tuple[dict[str, Any], ...]  # ModalityConfig as dict
    seed: int | None = None


@dataclass(frozen=True, slots=True)
class EmbodimentOutput:
    """Output from embodiment processing."""

    state: EmbodimentState
    transitions: tuple[StateTransition, ...]
    canonical_effect: str = "NONE"
    body_sensation_claim: str = "NOT_ESTABLISHED"
    body_ownership_claim: str = "NOT_ESTABLISHED"


class EmbodimentStateInterface(ABC):
    """Abstract interface for embodiment state module."""

    MODULE_ID: str = "embodiment-state"
    MODULE_VERSION: str = "0.1.0"

    @property
    @abstractmethod
    def manager(self) -> EmbodimentStateManager:
        """Return the state manager."""

    @abstractmethod
    def process(self, input_data: EmbodimentInput) -> EmbodimentOutput:
        """Process embodiment input and produce state."""

    @abstractmethod
    def reset(self) -> None:
        """Reset module to initial condition."""

    @abstractmethod
    def snapshot(self, snapshot_id: str | None = None) -> StateSnapshot:
        """Create a snapshot of current state."""

    @abstractmethod
    def restore(self, snapshot_id: str) -> EmbodimentState:
        """Restore state from snapshot."""

    @abstractmethod
    def enable(self) -> None:
        """Enable the module."""

    @abstractmethod
    def disable(self) -> None:
        """Disable the module."""

    @abstractmethod
    def ablate(self, modality: str | None = None) -> None:
        """Ablate specific modality or entire module."""

    @abstractmethod
    def get_integration_points(self) -> dict[str, Any]:
        """Return integration points for downstream consumers."""

    @abstractmethod
    def validate_state(self, state: EmbodimentState) -> tuple[bool, list[str]]:
        """Validate a state for consistency."""