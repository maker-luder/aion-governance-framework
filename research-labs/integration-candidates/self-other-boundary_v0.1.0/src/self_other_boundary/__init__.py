"""Self-Other Boundary research candidate for AION Four-Domain architecture."""

from .interface import SelfOtherBoundaryInterface
from .model import (
    BoundaryConfiguration,
    BoundaryEvent,
    BoundaryMode,
    BoundaryState,
    OtherModel,
    SelfOtherDistinction,
    SubjectRelation,
)
from .state import BoundaryStateManager, StateSnapshot, StateTransition

__all__ = [
    "BoundaryConfiguration",
    "BoundaryEvent",
    "BoundaryMode",
    "BoundaryState",
    "BoundaryStateManager",
    "OtherModel",
    "SelfOtherBoundaryInterface",
    "SelfOtherDistinction",
    "SubjectRelation",
    "StateSnapshot",
    "StateTransition",
]
