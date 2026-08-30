from __future__ import annotations

from datetime import date

import pytest

from aion_astra_bazi_core.enums import LuckDirection
from aion_astra_bazi_core.errors import ValidationError
from aion_astra_bazi_core.models import Pillar
from aion_astra_bazi_core.traditional_extensions import (
    BirthSexMarker,
    SOLAR_TERM_LONGITUDES,
    element_distribution_fact,
    independent_gregorian_day_pillar,
    luck_start_from_boundary_interval,
    ten_god_distribution_fact,
    traditional_luck_direction,
    validate_solar_term_sequence,
)


def pillar(name: str, stem: str, hidden: tuple[str, ...], gods: tuple[str, ...]) -> Pillar:
    return Pillar(name, stem, "子", "YANG", "WOOD", "WATER", hidden, gods, "X", "X", ("戌", "亥"))


def test_traditional_luck_direction_four_combinations() -> None:
    assert traditional_luck_direction("甲", BirthSexMarker.MALE) is LuckDirection.FORWARD
    assert traditional_luck_direction("甲", BirthSexMarker.FEMALE) is LuckDirection.REVERSE
    assert traditional_luck_direction("乙", BirthSexMarker.FEMALE) is LuckDirection.FORWARD
    assert traditional_luck_direction("乙", BirthSexMarker.MALE) is LuckDirection.REVERSE


def test_traditional_luck_direction_validates_stem() -> None:
    with pytest.raises(ValidationError, match="ten heavenly stems"):
        traditional_luck_direction("X", BirthSexMarker.MALE)


def test_three_days_equal_one_year_is_explicit() -> None:
    fact = luck_start_from_boundary_interval(9.0)
    assert fact.start_age_years == 3.0
    assert fact.conversion_rule == "THREE_DAYS_EQUAL_ONE_YEAR_V1"
    assert fact.interpretation_status == "NOT_PERFORMED"


@pytest.mark.parametrize("value", [-1, "three"])
def test_luck_start_rejects_invalid_interval(value) -> None:
    with pytest.raises(ValidationError):
        luck_start_from_boundary_interval(value)


def test_independent_day_pillar_reference_vectors() -> None:
    assert independent_gregorian_day_pillar(date(1986, 5, 29)) == "癸酉"
    assert independent_gregorian_day_pillar(date(2000, 2, 29)) == "丁巳"


def test_fixed_qi_solar_term_table_is_complete() -> None:
    assert validate_solar_term_sequence()
    assert len(SOLAR_TERM_LONGITUDES) == 24
    assert SOLAR_TERM_LONGITUDES["春分"] == 0
    assert SOLAR_TERM_LONGITUDES["立春"] == 315


def test_distribution_facts_do_not_infer_strength() -> None:
    pillars = (
        pillar("YEAR", "甲", ("癸",), ("比肩", "正印")),
        pillar("MONTH", "丙", ("己", "辛"), ("食神", "正財", "正官")),
    )
    elements = element_distribution_fact(pillars)
    gods = ten_god_distribution_fact(pillars)
    assert dict(elements.values) == {"WOOD": 1, "FIRE": 1, "EARTH": 1, "METAL": 1, "WATER": 1}
    assert elements.strength_conclusion == gods.strength_conclusion == "NOT_DERIVED"
    assert gods.interpretation_status == "NOT_PERFORMED"

