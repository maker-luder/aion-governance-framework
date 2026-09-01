from __future__ import annotations

import pytest

from aion_astra_bazi_core.constants import BRANCH_ELEMENTS, HIDDEN_STEMS, STEM_ELEMENTS, YIN_YANG
from aion_astra_bazi_core.errors import ValidationError
from aion_astra_bazi_core.models import Pillar
from aion_astra_bazi_core.school_evidence import (
    build_bazi_school_evidence,
    derive_seasonal_evidence,
    derive_transformation_candidates,
    validate_school_evidence_tables,
)


def pillar(name: str, stem: str, branch: str) -> Pillar:
    hidden = HIDDEN_STEMS[branch]
    return Pillar(
        name=name,
        stem=stem,
        branch=branch,
        yin_yang=YIN_YANG[stem],
        stem_element=STEM_ELEMENTS[stem],
        branch_element=BRANCH_ELEMENTS[branch],
        hidden_stems=hidden,
        ten_gods=tuple("UNSPECIFIED" for _ in hidden),
        nayin="TEST_ONLY",
        twelve_stage="TEST_ONLY",
        void_branches=(),
    )


def synthetic_pillars() -> tuple[Pillar, ...]:
    return (
        pillar("YEAR", "甲", "申"),
        pillar("MONTH", "己", "子"),
        pillar("DAY", "丙", "辰"),
        pillar("HOUR", "辛", "酉"),
    )


def test_school_evidence_tables_are_total() -> None:
    assert validate_school_evidence_tables()


def test_seasonal_evidence_exposes_month_and_day_master_without_strength_label() -> None:
    fact = derive_seasonal_evidence(synthetic_pillars())
    assert fact.day_master == "丙"
    assert fact.day_master_element == "FIRE"
    assert fact.month_branch == "子"
    assert fact.month_branch_element == "WATER"
    assert fact.season == "WINTER"
    assert fact.strength_conclusion == "NOT_DERIVED"
    assert fact.structure_conclusion == "NOT_DERIVED"
    assert fact.useful_element_conclusion == "NOT_DERIVED"
    assert fact.interpretation_status == "NOT_PERFORMED"


def test_seasonal_counts_are_complete_raw_evidence() -> None:
    fact = derive_seasonal_evidence(synthetic_pillars())
    assert sum(value for _, value in fact.visible_stem_counts) == 4
    assert sum(value for _, value in fact.hidden_stem_counts) == sum(len(p.hidden_stems) for p in synthetic_pillars())
    assert sum(value for _, value in fact.relationship_counts) == 4 + sum(len(p.hidden_stems) for p in synthetic_pillars())


def test_transformation_candidates_name_target_but_do_not_assert_completion() -> None:
    facts = derive_transformation_candidates(synthetic_pillars())
    keyed = {(fact.candidate_type, frozenset(fact.members)): fact for fact in facts}
    stem = keyed[("STEM_COMBINATION", frozenset(("甲", "己")))]
    harmony = keyed[("THREE_HARMONY", frozenset(("申", "子", "辰")))]
    assert stem.target_element == "EARTH"
    assert harmony.target_element == "WATER"
    assert all(fact.transformation_status == "CONDITIONS_NOT_EVALUATED" for fact in facts)
    assert all(fact.interpretation_status == "NOT_PERFORMED" for fact in facts)


def test_duplicate_member_does_not_invent_multiple_group_transformations() -> None:
    pillars = (
        pillar("YEAR", "甲", "申"), pillar("MONTH", "己", "子"),
        pillar("DAY", "甲", "辰"), pillar("HOUR", "己", "子"),
    )
    facts = derive_transformation_candidates(pillars)
    stem = next(fact for fact in facts if fact.candidate_type == "STEM_COMBINATION")
    assert stem.occurrence_count == 2
    harmony = next(fact for fact in facts if fact.candidate_type == "THREE_HARMONY")
    assert harmony.occurrence_count == 1


def test_invalid_pillar_shapes_fail_closed() -> None:
    with pytest.raises(ValidationError, match="exactly"):
        derive_seasonal_evidence(synthetic_pillars()[:3])
    with pytest.raises(ValidationError, match="four pillars"):
        derive_transformation_candidates(synthetic_pillars()[:3])


def test_composed_school_evidence_preserves_subjectivity_core_boundary() -> None:
    evidence = build_bazi_school_evidence(synthetic_pillars())
    assert evidence.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert evidence.consciousness_conclusion == "NOT_ESTABLISHED"
    assert evidence.canonical_effect == "NONE"
    assert evidence.deployment is False
    assert evidence.action_authority == "NONE"
