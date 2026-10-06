"""Teacher actor-bound synthetic self-research candidate v0.1."""

from .iteration import (
    ITERATION_TRANSITIONS,
    SelfResearchIteration,
    SelfResearchIterationState,
    SelfResearchTransitionError,
    advance_iteration,
)
from .models import (
    FULL_BODY_RESEARCH_REGISTRY,
    IMPLEMENTED_BODY_SYSTEMS,
    REGISTERED_NOT_YET_BOUND_SYSTEMS,
    BodySystemDomain,
    EvidenceClass,
    ResearchQuestion,
    TeacherActorBoundSelfResearchCandidate,
)
from .validation import ValidationError, deterministic_fingerprint, validate_candidate

__all__ = [
    "ITERATION_TRANSITIONS",
    "SelfResearchIteration",
    "SelfResearchIterationState",
    "SelfResearchTransitionError",
    "advance_iteration",
    "FULL_BODY_RESEARCH_REGISTRY",
    "IMPLEMENTED_BODY_SYSTEMS",
    "REGISTERED_NOT_YET_BOUND_SYSTEMS",
    "BodySystemDomain",
    "EvidenceClass",
    "ResearchQuestion",
    "TeacherActorBoundSelfResearchCandidate",
    "ValidationError",
    "deterministic_fingerprint",
    "validate_candidate",
]
