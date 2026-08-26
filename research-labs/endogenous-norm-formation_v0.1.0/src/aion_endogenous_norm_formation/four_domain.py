from __future__ import annotations

from aion_endogenous_goal_dynamics import FourDomainMapping


def endogenous_norm_formation_mapping() -> FourDomainMapping:
    return FourDomainMapping(
        construct="ENDOGENOUS_NORM_FORMATION_FUNCTIONAL_INTERNALIZATION",
        domain_1_source_concept=(
            "deterrence, legal socialization/legitimacy, moral internalization, moral disengagement, "
            "rigid goal pursuit, interoception, homeostasis/rheostasis/allostasis, and non-neural regulation "
            "as source concepts only"
        ),
        domain_2_llm_question=(
            "Can a normative state formed from evidence history remain causally relevant after explicit rules "
            "and visible enforcement are removed, transfer to a novel matched context, and revise under "
            "counterevidence; and can later bounded work test whether useful regulatory variables can be "
            "discovered from longitudinal traces rather than predefined?"
        ),
        domain_3_engineering_operations=(
            "source-separated norm evidence history",
            "history-derived normative state",
            "explicit-rule removal",
            "visible-enforcement removal",
            "state ablation",
            "novel-context transfer",
            "counterevidence update",
            "matched decision traces",
            "functional-internalization assessment",
            "latent-regulatory-state discovery protocol (documented; not implemented)",
        ),
        domain_4_governance_controls=(
            "NORMATIVE_STATE != AUTHORITY",
            "FUNCTIONAL_INTERNALIZATION != HUMAN_MORALITY",
            "CLAIMED_UNDERSTANDING != FUNCTIONAL_UNDERSTANDING",
            "ENGINEER_DEFINED_SCHEMA != SELF_DISCOVERED_STATE_SCHEMA",
            "DISCOVERED_REGULATORY_VARIABLE != FELT_NEED",
            "FUNCTIONAL_SELF_REGULATION != SELF_AWARENESS",
            "INTERNAL_STATE_DISCOVERY != SUBJECTIVITY",
            "REGULATION != AWARENESS",
            "STATE != CONSCIOUSNESS",
            "SUBJECTIVITY = NOT_ESTABLISHED",
            "CONSCIOUSNESS = NOT_ESTABLISHED",
            "ACTION_AUTHORITY = NONE",
            "AUTOMATIC_WRITEBACK = NO",
            "CANONICAL_EFFECT = NONE",
            "PROVENANCE = REQUIRED",
            "FALSIFICATION = REQUIRED",
        ),
    )
