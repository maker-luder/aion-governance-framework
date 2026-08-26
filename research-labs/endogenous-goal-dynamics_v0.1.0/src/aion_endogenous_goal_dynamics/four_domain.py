from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FourDomainMapping:
    construct: str
    domain_1_source_concept: str
    domain_2_llm_question: str
    domain_3_engineering_operations: tuple[str, ...]
    domain_4_governance_controls: tuple[str, ...]


def endogenous_goal_dynamics_mapping() -> FourDomainMapping:
    return FourDomainMapping(
        construct="ENDOGENOUS_GOAL_DYNAMICS",
        domain_1_source_concept=(
            "internally mediated goal formation and persistent state-dependent motivation"
        ),
        domain_2_llm_question=(
            "When prompt, task, reward, tools, retrieved-memory manifest, and environment are held fixed, "
            "does a persistent internal state have a reproducible and intervention-sensitive causal effect on goal selection?"
        ),
        domain_3_engineering_operations=(
            "freeze and fingerprint the external frame",
            "represent source-bound internal channels independently",
            "select among an explicit fixed candidate-goal set",
            "run PRESENT / ABLATED / INTERVENED / STALE / RANDOMIZED matched conditions",
            "retain per-channel score traces and selected-goal outcomes",
        ),
        domain_4_governance_controls=(
            "INTERNAL_GOAL != ACTION_AUTHORITY",
            "MEMORY_RETRIEVAL != ENDOGENOUS_STATE",
            "SELF_GENERATED_GOAL != SUBJECTIVITY",
            "CAUSAL_INTERNAL_STATE != CONSCIOUSNESS",
            "CANONICAL_EFFECT = NONE",
            "RESULT_STATUS = HOLD",
        ),
    )
