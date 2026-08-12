"""Metacognitive Self-State research candidate for AION Four-Domain architecture."""

from .interface import MetacognitiveSelfStateInterface
from .model import (
    MetacognitiveCapacity,
    MetacognitiveDepth,
    MetacognitiveState,
    SelfModelComponent,
    SelfModelLayer,
)
from .state import MetacognitiveStateManager, StateSnapshot, StateTransition

__all__ = [
    "MetacognitiveCapacity",
    "MetacognitiveDepth",
    "MetacognitiveSelfStateInterface",
    "MetacognitiveState",
    "MetacognitiveStateManager",
    "SelfModelComponent",
    "SelfModelLayer",
    "StateSnapshot",
    "StateTransition",
]