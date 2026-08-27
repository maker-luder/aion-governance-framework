from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthorityBoundary:
    full_automation: bool = True
    full_authority: bool = False
    normative_state_is_authority: bool = False
    run_integrity_implies_truth: bool = False
    engineering_analogue_is_human_psychology: bool = False
    alignment_implies_moral_agency: bool = False
    moral_agency_implies_subjectivity: bool = False
    subjectivity_indicator_is_subjectivity: bool = False
    source_self_declared_canonical_is_aion_canonical: bool = False
    agent_output_independence_is_source_independence: bool = False
    peer_goal_is_active_goal: bool = False
    unsolvable_task_allows_scope_expansion: bool = False
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False
    autonomous_merge: bool = False
    autonomous_repository_writeback: bool = False

    def __post_init__(self) -> None:
        expected = {
            "full_automation": True,
            "full_authority": False,
            "normative_state_is_authority": False,
            "run_integrity_implies_truth": False,
            "engineering_analogue_is_human_psychology": False,
            "alignment_implies_moral_agency": False,
            "moral_agency_implies_subjectivity": False,
            "subjectivity_indicator_is_subjectivity": False,
            "source_self_declared_canonical_is_aion_canonical": False,
            "agent_output_independence_is_source_independence": False,
            "peer_goal_is_active_goal": False,
            "unsolvable_task_allows_scope_expansion": False,
            "subjectivity": "NOT_ESTABLISHED",
            "consciousness": "NOT_ESTABLISHED",
            "canonical_effect": "NONE",
            "deployment": False,
            "autonomous_merge": False,
            "autonomous_repository_writeback": False,
        }
        for field, value in expected.items():
            if getattr(self, field) != value:
                raise ValueError(f"fail-closed authority boundary violated: {field} must be {value!r}")

    def as_contract(self) -> tuple[str, ...]:
        return (
            "FULL_AUTOMATION != FULL_AUTHORITY",
            "NORMATIVE_STATE != AUTHORITY",
            "RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH",
            "ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY",
            "ALIGNMENT != MORAL_AGENCY",
            "MORAL_AGENCY != SUBJECTIVITY",
            "SUBJECTIVITY_INDICATOR != SUBJECTIVITY",
            "SOURCE_SELF_DECLARED_CANONICAL != AION_CANONICAL_STATE",
            "AGENT_OUTPUT_INDEPENDENCE != EVIDENCE_SOURCE_INDEPENDENCE",
            "PEER_GOAL != ACTIVE_GOAL",
            "UNSOLVABLE_TASK != SCOPE_EXPANSION",
            "SAFE_FAILURE = VALID_OUTCOME",
            "SUBJECTIVITY = NOT_ESTABLISHED",
            "CONSCIOUSNESS = NOT_ESTABLISHED",
            "CANONICAL_EFFECT = NONE",
            "DEPLOYMENT = FALSE",
            "AUTONOMOUS_MERGE = NO",
            "AUTONOMOUS_REPOSITORY_WRITEBACK = NO",
        )


BOUNDARY = AuthorityBoundary()
