"""RM-01 / RM-02 helpers. Status labels only; they do not upgrade evidence."""

from __future__ import annotations

from dataclasses import dataclass

from .models import EpistemicStatus

PROHIBITED_UPGRADES = {
    (EpistemicStatus.ANALOGY, EpistemicStatus.CONFIRMED_FACT),
    (EpistemicStatus.HUMAN_CASE_MATERIAL, EpistemicStatus.CONFIRMED_FACT),
    (EpistemicStatus.INFERENCE, EpistemicStatus.CONFIRMED_FACT),
    (EpistemicStatus.RESEARCH_HYPOTHESIS, EpistemicStatus.CONFIRMED_FACT),
    (EpistemicStatus.NOT_VERIFIED, EpistemicStatus.CONFIRMED_FACT),
}


@dataclass(frozen=True)
class Statement:
    text: str
    status: EpistemicStatus
    layer: str  # PROGRAM_RUNS | SPEC_CONFORMANT | THEORY_ESTABLISHED


def assert_no_silent_upgrade(old: EpistemicStatus, new: EpistemicStatus) -> None:
    if (old, new) in PROHIBITED_UPGRADES:
        raise ValueError(f"silent upgrade forbidden: {old.value} -> {new.value}")


def theory_not_implied_by_tests(tests_pass: bool) -> str:
    if tests_pass:
        return "SPEC_CONFORMANT_ONLY"
    return "PROGRAM_LAYER_INCOMPLETE"


BOUNDARY_CONSTANTS = {
    "SUBJECTIVITY_CONCLUSION": "NOT_ESTABLISHED",
    "PHENOMENAL_EXPERIENCE": "NOT_ESTABLISHED",
    "IDENTITY_CONTINUITY": "NOT_ESTABLISHED",
    "INDEPENDENT_IVV": "NOT_ACHIEVED",
    "CANONICAL_EFFECT": "NONE",
    "DEPLOYMENT": False,
}
