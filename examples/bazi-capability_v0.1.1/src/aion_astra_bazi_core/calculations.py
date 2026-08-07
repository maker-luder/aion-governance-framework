"""Deterministic derived facts and explicit relationship calculations."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .constants import (
    BRANCH_BREAKS,
    BRANCH_CLASHES,
    BRANCH_COMBINATIONS,
    BRANCH_HARMS,
    BRANCH_PUNISHMENTS,
    BRANCHES,
    BRANCH_ELEMENTS,
    STEM_COMBINATIONS,
    STEM_ELEMENTS,
    STEMS,
    THREE_HARMONIES,
    THREE_MEETINGS,
    YIN_YANG,
)
from .enums import LuckDirection
from .models import LuckCycle, Pillar


def sexagenary_cycle() -> tuple[str, ...]:
    return tuple(STEMS[index % 10] + BRANCHES[index % 12] for index in range(60))


def _pair_relations(values: tuple[str, ...], relation: str, groups: set[frozenset[str]]) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for left in range(len(values)):
        for right in range(left + 1, len(values)):
            pair = frozenset((values[left], values[right]))
            if pair in groups:
                found.append({"type": relation, "members": sorted(pair)})
    return found


def _group_relations(
    values: tuple[str, ...],
    relation: str,
    groups: Iterable[frozenset[str]],
) -> list[dict[str, Any]]:
    present = set(values)
    return [
        {"type": relation, "members": sorted(group)}
        for group in groups
        if group.issubset(present)
    ]


def calculate_relationships(pillars: tuple[Pillar, ...]) -> tuple[dict[str, Any], ...]:
    stems = tuple(pillar.stem for pillar in pillars)
    branches = tuple(pillar.branch for pillar in pillars)
    relations: list[dict[str, Any]] = []
    relations.extend(_pair_relations(stems, "STEM_COMBINATION", STEM_COMBINATIONS))
    relations.extend(_pair_relations(branches, "BRANCH_COMBINATION", BRANCH_COMBINATIONS))
    relations.extend(_pair_relations(branches, "BRANCH_CLASH", BRANCH_CLASHES))
    relations.extend(_pair_relations(branches, "BRANCH_HARM", BRANCH_HARMS))
    relations.extend(_pair_relations(branches, "BRANCH_BREAK", BRANCH_BREAKS))
    relations.extend(_group_relations(branches, "BRANCH_PUNISHMENT", BRANCH_PUNISHMENTS))
    relations.extend(_group_relations(branches, "THREE_HARMONY", THREE_HARMONIES))
    relations.extend(_group_relations(branches, "THREE_MEETING", THREE_MEETINGS))
    return tuple(relations)


def next_pillar(value: str, offset: int) -> str:
    cycle = sexagenary_cycle()
    return cycle[(cycle.index(value) + offset) % 60]


def calculate_luck_cycles(
    month_pillar: str,
    direction: LuckDirection,
    start_age_years: float,
    count: int = 8,
) -> tuple[LuckCycle, ...]:
    step = 1 if direction is LuckDirection.FORWARD else -1
    return tuple(
        LuckCycle(
            sequence=index + 1,
            pillar=next_pillar(month_pillar, step * (index + 1)),
            start_age_years=start_age_years + 10.0 * index,
            end_age_years=start_age_years + 10.0 * (index + 1),
        )
        for index in range(count)
    )


def element_distribution(pillars: tuple[Pillar, ...]) -> dict[str, int]:
    result = {"WOOD": 0, "FIRE": 0, "EARTH": 0, "METAL": 0, "WATER": 0}
    for pillar in pillars:
        result[STEM_ELEMENTS[pillar.stem]] += 1
        result[BRANCH_ELEMENTS[pillar.branch]] += 1
        for hidden in pillar.hidden_stems:
            result[STEM_ELEMENTS[hidden]] += 1
    return result


def basic_symbol(stem: str, branch: str) -> dict[str, str]:
    return {
        "stem_yin_yang": YIN_YANG[stem],
        "branch_yin_yang": YIN_YANG[branch],
        "stem_element": STEM_ELEMENTS[stem],
        "branch_element": BRANCH_ELEMENTS[branch],
    }
