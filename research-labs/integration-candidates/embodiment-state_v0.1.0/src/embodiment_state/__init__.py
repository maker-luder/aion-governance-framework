"""Embodiment State research candidate for AION Four-Domain architecture."""

from .interface import EmbodimentStateInterface
from .model import (
    EmbodimentConfig,
    EmbodimentState,
    ModalityConfig,
    ProprioceptiveSignal,
)
from .state import EmbodimentStateManager, StateSnapshot, StateTransition

__all__ = [
    "EmbodimentConfig",
    "EmbodimentState",
    "EmbodimentStateInterface",
    "EmbodimentStateManager",
    "ModalityConfig",
    "ProprioceptiveSignal",
    "StateSnapshot",
    "StateTransition",
]