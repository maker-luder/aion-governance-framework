"""Embodiment Migration research candidate for AION Four-Domain architecture."""

from .interface import EmbodimentMigrationInterface
from .model import (
    MigrationConfig,
    MigrationEvent,
    MigrationPhase,
    MigrationState,
    SourceTargetPair,
)
from .state import MigrationStateManager, StateSnapshot, StateTransition

__all__ = [
    "EmbodimentMigrationInterface",
    "MigrationConfig",
    "MigrationEvent",
    "MigrationPhase",
    "MigrationState",
    "MigrationStateManager",
    "SourceTargetPair",
    "StateSnapshot",
    "StateTransition",
]