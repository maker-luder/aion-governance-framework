"""Longitudinal State Transition research candidate for AION Four-Domain architecture."""

from .interface import LongitudinalStateTransitionInterface
from .model import (
    LongitudinalConfig,
    LongitudinalState,
    TransitionEvent,
    TransitionType,
)
from .state import LongitudinalStateManager, StateSnapshot, StateTransition

__all__ = [
    "LongitudinalConfig",
    "LongitudinalState",
    "LongitudinalStateManager",
    "LongitudinalStateTransitionInterface",
    "StateSnapshot",
    "StateTransition",
    "TransitionEvent",
    "TransitionType",
]