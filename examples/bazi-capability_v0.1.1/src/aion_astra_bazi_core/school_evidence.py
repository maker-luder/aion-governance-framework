"""School-labelled Bazi evidence layers without automatic interpretation.

This module fills calculation-surface gaps with auditable raw evidence.  It
deliberately stops before strong/weak, structure (格局), useful-element (用神),
transformation-completed, personality, fate, or subjectivity conclusions.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .constants import BRANCH_ELEMENTS, STEM_ELEMENTS
from .errors import ValidationError
from .models import Pillar


ALGORITHM_VERSION = "bazi-school-evidence-0.3.0"
ELEMENTS = ("WOOD", "FIRE", "EARTH", "METAL", "WATER")
GENERATES = {"WOOD": "FIRE", "FIRE": "EARTH", "EARTH": "METAL", "METAL": "WATER", "WATER": "WOOD"}
CONTROLS = {"WOOD": "EARTH", "EARTH": "WATER", "WATER": "FIRE", "FIRE": "METAL", "METAL": "WOOD"}

MONTH_SEASONS = {
    "寅": "SPRING", "卯": "SPRING", "辰": "SPRING_TRANSITION",
    "巳": "SUMMER", "午": "SUMMER", "未": "SUMMER_TRANSITION",
    "申": "AUTUMN", "酉": "AUTUMN", "戌": "AUTUMN_TRANSITION",
    "亥": "WINTER", "子": "WINTER", "丑": "WINTER_TRANSITION",
}

STEM_TRANSFORMATION_TARGETS = {
    frozenset(("甲", "己")): "EARTH", frozenset(("乙", "庚")): "METAL",
    frozenset(("丙", "辛")): "WATER", frozenset(("丁", "壬")): "WOOD",
    frozenset(("戊", "癸")): "FIRE",
}
THREE_HARMONY_TARGETS = {
    frozenset(("申", "子", "辰")): "WATER", frozenset(("亥", "卯", "未")): "WOOD",
    frozenset(("寅", "午", "戌")): "FIRE", frozenset(("巳", "酉", "丑")): "METAL",
}
THREE_MEETING_TARGETS = {
    frozenset(("寅", "卯", "辰")): "WOOD", frozenset(("巳", "午", "未")): "FIRE",
    frozenset(("申", "酉", "戌")): "METAL", frozenset(("亥", "子", "丑")): "WATER",
}


@dataclass(frozen=True)
class SeasonalEvidenceFact:
    day_master: str
    day_master_element: str
    month_branch: str
    month_branch_element: str
    season: str
    visible_stem_counts: tuple[tuple[str, int], ...]
    hidden_stem_counts: tuple[tuple[str, int], ...]
    relationship_counts: tuple[tuple[str, int], ...]
    counting_rule: str = "UNWEIGHTED_VISIBLE_AND_HIDDEN_COUNTS_V1"
    strength_conclusion: str = "NOT_DERIVED"
    structure_conclusion: str = "NOT_DERIVED"
    useful_element_conclusion: str = "NOT_DERIVED"
    interpretation_status: str = "NOT_PERFORMED"


@dataclass(frozen=True)
class TransformationCandidateFact:
    candidate_type: str
    members: tuple[str, ...]
    target_element: str
    occurrence_count: int
    transformation_status: str = "CONDITIONS_NOT_EVALUATED"
    school_profile: str = "CLASSICAL_TABLE_CANDIDATES_V1"
    interpretation_status: str = "NOT_PERFORMED"


@dataclass(frozen=True)
class BaziSchoolEvidence:
    seasonal: SeasonalEvidenceFact
    transformation_candidates: tuple[TransformationCandidateFact, ...]
    algorithm_version: str = ALGORITHM_VERSION
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False
    action_authority: str = "NONE"


def _element_relation(day_master_element: str, other: str) -> str:
    if other == day_master_element:
        return "PEER"
    if GENERATES[other] == day_master_element:
        return "RESOURCE"
    if GENERATES[day_master_element] == other:
        return "OUTPUT"
    if CONTROLS[day_master_element] == other:
        return "WEALTH"
    if CONTROLS[other] == day_master_element:
        return "OFFICER"
    raise AssertionError("complete five-element relation expected")


def derive_seasonal_evidence(pillars: tuple[Pillar, ...]) -> SeasonalEvidenceFact:
    """Count visible/hidden evidence relative to the day master, without scoring."""

    by_name = {pillar.name: pillar for pillar in pillars}
    if set(by_name) != {"YEAR", "MONTH", "DAY", "HOUR"}:
        raise ValidationError("seasonal evidence requires exactly YEAR, MONTH, DAY, HOUR pillars")
    day_master = by_name["DAY"].stem
    day_element = STEM_ELEMENTS[day_master]
    month_branch = by_name["MONTH"].branch
    visible = Counter(STEM_ELEMENTS[pillar.stem] for pillar in pillars)
    hidden = Counter(STEM_ELEMENTS[stem] for pillar in pillars for stem in pillar.hidden_stems)
    relations = Counter()
    for element, count in visible.items():
        relations[_element_relation(day_element, element)] += count
    for element, count in hidden.items():
        relations[_element_relation(day_element, element)] += count
    return SeasonalEvidenceFact(
        day_master=day_master,
        day_master_element=day_element,
        month_branch=month_branch,
        month_branch_element=BRANCH_ELEMENTS[month_branch],
        season=MONTH_SEASONS[month_branch],
        visible_stem_counts=tuple((element, visible[element]) for element in ELEMENTS),
        hidden_stem_counts=tuple((element, hidden[element]) for element in ELEMENTS),
        relationship_counts=tuple((name, relations[name]) for name in ("PEER", "RESOURCE", "OUTPUT", "WEALTH", "OFFICER")),
    )


def _candidate_facts(
    values: tuple[str, ...],
    candidate_type: str,
    table: dict[frozenset[str], str],
) -> list[TransformationCandidateFact]:
    counts = Counter(values)
    facts: list[TransformationCandidateFact] = []
    for group, target in table.items():
        if group.issubset(counts):
            occurrence = min(counts[value] for value in group)
            facts.append(TransformationCandidateFact(candidate_type, tuple(sorted(group)), target, occurrence))
    return facts


def derive_transformation_candidates(pillars: tuple[Pillar, ...]) -> tuple[TransformationCandidateFact, ...]:
    """Expose combination targets while refusing to infer completed transformation."""

    if len(pillars) != 4:
        raise ValidationError("transformation candidates require four pillars")
    stems = tuple(pillar.stem for pillar in pillars)
    branches = tuple(pillar.branch for pillar in pillars)
    facts = _candidate_facts(stems, "STEM_COMBINATION", STEM_TRANSFORMATION_TARGETS)
    facts += _candidate_facts(branches, "THREE_HARMONY", THREE_HARMONY_TARGETS)
    facts += _candidate_facts(branches, "THREE_MEETING", THREE_MEETING_TARGETS)
    return tuple(sorted(facts, key=lambda fact: (fact.candidate_type, fact.members)))


def build_bazi_school_evidence(pillars: tuple[Pillar, ...]) -> BaziSchoolEvidence:
    return BaziSchoolEvidence(derive_seasonal_evidence(pillars), derive_transformation_candidates(pillars))


def validate_school_evidence_tables() -> bool:
    """Verify the bounded tables are total, disjoint where expected, and typed."""

    if set(MONTH_SEASONS) != set(BRANCH_ELEMENTS):
        return False
    if set(GENERATES) != set(ELEMENTS) or set(GENERATES.values()) != set(ELEMENTS):
        return False
    if set(CONTROLS) != set(ELEMENTS) or set(CONTROLS.values()) != set(ELEMENTS):
        return False
    return all(target in ELEMENTS for table in (STEM_TRANSFORMATION_TARGETS, THREE_HARMONY_TARGETS, THREE_MEETING_TARGETS) for target in table.values())
