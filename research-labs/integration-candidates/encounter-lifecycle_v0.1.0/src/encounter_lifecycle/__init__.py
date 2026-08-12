"""Encounter Lifecycle research candidate for AION Four-Domain architecture."""

from .interface import EncounterLifecycleInterface
from .model import (
    EncounterConfig,
    EncounterEvent,
    EncounterPhase,
    EncounterState,
    ParticipantModel,
)
from .state import EncounterStateManager, StateSnapshot, StateTransition

__all__ = [
    "EncounterConfig",
    "EncounterEvent",
    "EncounterLifecycleInterface",
    "EncounterPhase",
    "EncounterState",
    "EncounterStateManager",
    "ParticipantModel",
    "StateSnapshot",
    "StateTransition",
]