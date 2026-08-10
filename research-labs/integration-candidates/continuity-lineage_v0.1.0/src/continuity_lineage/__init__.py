"""Continuity Lineage research candidate for AION Four-Domain architecture."""

from .interface import ContinuityLineageInterface
from .model import (
    LineageConfig,
    LineageEvent,
    LineageNode,
    LineageState,
    LineageType,
)
from .state import LineageStateManager, StateSnapshot, StateTransition

__all__ = [
    "ContinuityLineageInterface",
    "LineageConfig",
    "LineageEvent",
    "LineageNode",
    "LineageState",
    "LineageStateManager",
    "LineageType",
    "StateSnapshot",
    "StateTransition",
]