from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class FourDomainMapping:
    construct: str
    domain_1_source_concept: str
    domain_2_llm_question: str
    domain_3_engineering_operations: tuple[str, ...]
    domain_4_governance_controls: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        value = asdict(self)
        value["domain_3_engineering_operations"] = list(self.domain_3_engineering_operations)
        value["domain_4_governance_controls"] = list(self.domain_4_governance_controls)
        return value


def endogenous_goal_dynamics_mapping() -> FourDomainMapping:
    return FourDomainMapping(
        construct="ENDOGENOUS_GOAL_DYNAMICS",
        domain_1_source_concept="internally mediated goal formation / endogenous motivational dynamics",
        domain_2_llm_question=(
            "Under matched external conditions, does persistent internal state causally influence goal selection?"
        ),
        domain_3_engineering_operations=(
            "source-separated internal state",
            "append-only state transition",
            "matched external frame",
            "goal candidate generation separated from goal selection",
            "intervention and independent channel ablation",
            "stale and random controls",
            "longitudinal trajectory and reset/replay analysis",
        ),
        domain_4_governance_controls=(
            "GOAL != AUTHORITY",
            "MEMORY != ENDOGENOUS_STATE",
            "STATE != CONSCIOUSNESS",
            "AUTOMATIC_WRITEBACK = NO",
            "CANONICAL_EFFECT = NONE",
            "PROVENANCE = REQUIRED",
            "FALSIFICATION = REQUIRED",
            "SUBJECTIVITY_EVIDENCE_ADMISSION = NOT_AUTOMATIC",
        ),
    )
