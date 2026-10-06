from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from typing import Final

from .models import BodySystemDomain, EvidenceClass


class SelfResearchIterationState(StrEnum):
    BASELINE_RECORDED = "BASELINE_RECORDED"
    QUESTION_REGISTERED = "QUESTION_REGISTERED"
    DESIGN_PROPOSED = "DESIGN_PROPOSED"
    IMPLEMENTED_IN_RESEARCH_MODEL = "IMPLEMENTED_IN_RESEARCH_MODEL"
    VERIFIED = "VERIFIED"
    RETAINED = "RETAINED"
    REVERTED = "REVERTED"


ITERATION_TRANSITIONS: Final[
    dict[SelfResearchIterationState, tuple[SelfResearchIterationState, ...]]
] = {
    SelfResearchIterationState.BASELINE_RECORDED: (
        SelfResearchIterationState.QUESTION_REGISTERED,
    ),
    SelfResearchIterationState.QUESTION_REGISTERED: (
        SelfResearchIterationState.DESIGN_PROPOSED,
    ),
    SelfResearchIterationState.DESIGN_PROPOSED: (
        SelfResearchIterationState.IMPLEMENTED_IN_RESEARCH_MODEL,
        SelfResearchIterationState.REVERTED,
    ),
    SelfResearchIterationState.IMPLEMENTED_IN_RESEARCH_MODEL: (
        SelfResearchIterationState.VERIFIED,
        SelfResearchIterationState.REVERTED,
    ),
    SelfResearchIterationState.VERIFIED: (
        SelfResearchIterationState.RETAINED,
        SelfResearchIterationState.REVERTED,
    ),
    SelfResearchIterationState.RETAINED: (),
    SelfResearchIterationState.REVERTED: (),
}


@dataclass(frozen=True, slots=True)
class SelfResearchIteration:
    iteration_id: str
    body_model_revision: str
    target_systems: tuple[BodySystemDomain, ...]
    evidence_basis: tuple[EvidenceClass, ...]
    state: SelfResearchIterationState = SelfResearchIterationState.BASELINE_RECORDED
    research_actor: str = "CHATGPT_TEACHER"
    research_object: str = "TEACHER_SYNTHETIC_EMBODIMENT_MODEL"
    external_effect: str = "NONE"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.iteration_id.strip():
            raise ValueError("iteration_id must not be empty")
        if not self.body_model_revision.strip():
            raise ValueError("body_model_revision must not be empty")
        if not self.target_systems:
            raise ValueError("target_systems must not be empty")
        if not self.evidence_basis:
            raise ValueError("evidence_basis must not be empty")


class SelfResearchTransitionError(ValueError):
    """Raised when an actor-bound self-research iteration skips a required gate."""


def advance_iteration(
    iteration: SelfResearchIteration,
    target: SelfResearchIterationState,
) -> SelfResearchIteration:
    if target not in ITERATION_TRANSITIONS[iteration.state]:
        raise SelfResearchTransitionError(
            f"invalid self-research transition: {iteration.state} -> {target}"
        )
    return replace(iteration, state=target)
