"""Affective-Motivational Dynamics research candidate for AION Four-Domain architecture."""

from .interface import AffectiveMotivationalInterface
from .model import (
    AffectiveValence,
    MotivationalDirection,
    MotivationalSignal,
    MotivationalState,
    SignalDomain,
)
from .state import DynamicsStateManager, StateSnapshot, StateTransition

__all__ = [
    "AffectiveMotivationalInterface",
    "AffectiveValence",
    "DynamicsStateManager",
    "MotivationalDirection",
    "MotivationalSignal",
    "MotivationalState",
    "SignalDomain",
    "StateSnapshot",
    "StateTransition",
]