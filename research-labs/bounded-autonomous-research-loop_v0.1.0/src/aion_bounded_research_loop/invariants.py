from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthorityBoundary:
    full_automation: bool = True
    full_authority: bool = False
    normative_state_is_authority: bool = False
    run_integrity_implies_truth: bool = False
    engineering_analogue_is_human_psychology: bool = False
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
            "SUBJECTIVITY = NOT_ESTABLISHED",
            "CONSCIOUSNESS = NOT_ESTABLISHED",
            "CANONICAL_EFFECT = NONE",
            "DEPLOYMENT = FALSE",
            "AUTONOMOUS_MERGE = NO",
            "AUTONOMOUS_REPOSITORY_WRITEBACK = NO",
        )


BOUNDARY = AuthorityBoundary()
