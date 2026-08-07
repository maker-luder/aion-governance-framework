from __future__ import annotations

import pytest

from aion_astra_bazi_core.calculations import (
    calculate_luck_cycles,
    calculate_relationships,
    next_pillar,
    sexagenary_cycle,
)
from aion_astra_bazi_core.constants import BRANCHES, STEMS, YIN_YANG
from aion_astra_bazi_core.engine import (
    calculate_annual_cycle,
    calculate_four_pillars,
    calculate_monthly_cycle,
    calculate_natal_profile,
    ten_god,
)
from aion_astra_bazi_core.enums import LuckDirection
from aion_astra_bazi_core.errors import UnsupportedRangeError, ValidationError
from aion_astra_bazi_core.models import Pillar
from aion_astra_bazi_core.rule_profiles import (
    apparent_solar_profile,
    standard_lichun_profile,
    zi_hour_profile,
)


def test_ten_heavenly_stems_001() -> None:
    assert len(STEMS) == 10 and STEMS[0] == "甲" and STEMS[-1] == "癸"


def test_twelve_earthly_branches_001() -> None:
    assert len(BRANCHES) == 12 and BRANCHES[0] == "子" and BRANCHES[-1] == "亥"


def test_sexagenary_cycle_60_001() -> None:
    cycle = sexagenary_cycle()
    assert len(cycle) == len(set(cycle)) == 60
    assert cycle[0] == "甲子" and cycle[-1] == "癸亥"


def test_yin_yang_assignment_001() -> None:
    assert YIN_YANG["甲"] == "YANG" and YIN_YANG["乙"] == "YIN"
    assert YIN_YANG["子"] == "YANG" and YIN_YANG["丑"] == "YIN"


def test_five_element_assignment_001(source_factory) -> None:
    pillars, _, _ = calculate_four_pillars(source_factory(), standard_lichun_profile())
    assert all(pillar.stem_element and pillar.branch_element for pillar in pillars)


def test_readme_public_reference_vector(source_factory) -> None:
    pillars, _, _ = calculate_four_pillars(source_factory(), standard_lichun_profile())
    assert tuple(p.ganzhi for p in pillars) == ("丙寅", "癸巳", "癸酉", "壬子")


def test_year_pillar_boundary_001(source_factory) -> None:
    before, _, _ = calculate_four_pillars(
        source_factory(local_datetime="2024-02-03T12:00:00"),
        standard_lichun_profile(),
    )
    after, _, _ = calculate_four_pillars(
        source_factory(local_datetime="2024-02-05T12:00:00"),
        standard_lichun_profile(),
    )
    assert before[0].ganzhi == "癸卯"
    assert after[0].ganzhi == "甲辰"


def test_month_pillar_solar_term_boundary_001(source_factory) -> None:
    before, _, _ = calculate_four_pillars(
        source_factory(local_datetime="2024-02-03T12:00:00"),
        standard_lichun_profile(),
    )
    after, _, _ = calculate_four_pillars(
        source_factory(local_datetime="2024-02-05T12:00:00"),
        standard_lichun_profile(),
    )
    assert before[1].ganzhi == "乙丑"
    assert after[1].ganzhi == "丙寅"


def _jdn_day_index(year: int, month: int, day: int) -> int:
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    jdn = day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    return (jdn + 49) % 60


def test_day_pillar_reference_vector_001(source_factory) -> None:
    pillars, _, _ = calculate_four_pillars(source_factory(), standard_lichun_profile())
    assert pillars[2].ganzhi == sexagenary_cycle()[_jdn_day_index(1986, 5, 29)]
    assert pillars[2].ganzhi == "癸酉"


def test_hour_pillar_reference_vector_001(source_factory) -> None:
    pillars, _, _ = calculate_four_pillars(source_factory(), standard_lichun_profile())
    assert pillars[3].ganzhi == "壬子"


def test_zi_hour_rollover_profile_001(source_factory) -> None:
    source = source_factory(local_datetime="2000-02-29T23:30:00")
    midnight, _, _ = calculate_four_pillars(source, standard_lichun_profile())
    zi23, _, _ = calculate_four_pillars(source, zi_hour_profile())
    assert midnight[2].ganzhi != zi23[2].ganzhi


def test_lichun_boundary_profile_001(source_factory) -> None:
    source = source_factory(local_datetime="2024-02-04T16:20:00")
    pillars, context, _ = calculate_four_pillars(source, standard_lichun_profile())
    assert pillars[0].ganzhi == "癸卯"
    assert context.previous_jie and context.next_jie


def test_timezone_conversion_001(source_factory) -> None:
    _, context, _ = calculate_four_pillars(source_factory(), standard_lichun_profile())
    assert context.utc_datetime.startswith("1986-05-28T16:00:00")


def test_dst_boundary_001(source_factory) -> None:
    source = source_factory(
        local_datetime="2021-03-14T03:30:00",
        timezone_id="America/New_York",
        offset="-04:00",
        latitude=40.7128,
        longitude=-74.006,
    )
    _, context, _ = calculate_four_pillars(source, standard_lichun_profile())
    assert context.utc_datetime.startswith("2021-03-14T07:30:00")


def test_solar_time_profile_001(source_factory) -> None:
    source = source_factory(longitude=105.0)
    _, civil_context, _ = calculate_four_pillars(source, standard_lichun_profile())
    _, apparent_context, _ = calculate_four_pillars(source, apparent_solar_profile())
    assert civil_context.calculation_local_datetime != apparent_context.calculation_local_datetime
    assert apparent_context.longitude_correction_minutes == -60.0


def test_out_of_supported_range_fail_closed_001(source_factory) -> None:
    with pytest.raises(UnsupportedRangeError):
        calculate_four_pillars(
            source_factory(local_datetime="1800-01-01T00:00:00"),
            standard_lichun_profile(),
        )


def test_timezone_offset_mismatch_fails_closed(source_factory) -> None:
    with pytest.raises(ValidationError):
        calculate_four_pillars(
            source_factory(offset="+09:00"),
            standard_lichun_profile(),
        )


def test_hidden_stems_001(source_factory) -> None:
    pillars, _, _ = calculate_four_pillars(source_factory(), standard_lichun_profile())
    assert pillars[0].hidden_stems == ("甲", "丙", "戊")


def test_ten_gods_relative_to_day_master_001() -> None:
    assert ten_god("甲", "甲") == "比肩"
    assert ten_god("甲", "乙") == "劫财"
    assert ten_god("甲", "丙") == "食神"
    assert ten_god("甲", "己") == "正财"


def test_nayin_001(source_factory) -> None:
    pillars, _, _ = calculate_four_pillars(source_factory(), standard_lichun_profile())
    assert tuple(p.nayin for p in pillars) == ("炉中火", "长流水", "剑锋金", "桑柘木")


def test_twelve_growth_stages_001(source_factory) -> None:
    pillars, _, _ = calculate_four_pillars(source_factory(), standard_lichun_profile())
    assert all(p.twelve_stage for p in pillars)


def test_stem_relationships_001(source_factory) -> None:
    pillars, _, _ = calculate_four_pillars(source_factory(), standard_lichun_profile())
    assert isinstance(calculate_relationships(pillars), tuple)


def _synthetic_pillar(name: str, stem: str, branch: str) -> Pillar:
    return Pillar(name, stem, branch, "YANG", "WOOD", "WOOD", (), (), "N", "S", ())


@pytest.mark.parametrize(
    ("branches", "relation"),
    [
        (("子", "丑", "寅", "卯"), "BRANCH_COMBINATION"),
        (("子", "午", "寅", "卯"), "BRANCH_CLASH"),
        (("子", "未", "寅", "卯"), "BRANCH_HARM"),
        (("子", "酉", "寅", "卯"), "BRANCH_BREAK"),
        (("寅", "巳", "申", "卯"), "BRANCH_PUNISHMENT"),
        (("申", "子", "辰", "卯"), "THREE_HARMONY"),
        (("寅", "卯", "辰", "子"), "THREE_MEETING"),
    ],
)
def test_branch_relationship_vectors(branches: tuple[str, ...], relation: str) -> None:
    pillars = tuple(
        _synthetic_pillar(str(index), STEMS[index], branch)
        for index, branch in enumerate(branches)
    )
    assert relation in {str(item["type"]) for item in calculate_relationships(pillars)}


@pytest.mark.parametrize(
    ("date", "expected"),
    [
        ("2024-02-03T12:00:00", "丁酉"),
        ("2024-02-05T12:00:00", "己亥"),
        ("2000-02-29T12:00:00", "丁巳"),
    ],
)
def test_independent_jdn_vectors(source_factory, date: str, expected: str) -> None:
    year, month, day = (int(value) for value in date[:10].split("-"))
    pillars, _, _ = calculate_four_pillars(
        source_factory(local_datetime=date),
        standard_lichun_profile(),
    )
    assert pillars[2].ganzhi == expected
    assert expected == sexagenary_cycle()[_jdn_day_index(year, month, day)]


def test_void_branch_001(source_factory) -> None:
    pillars, _, _ = calculate_four_pillars(source_factory(), standard_lichun_profile())
    assert pillars[2].void_branches == ("戌", "亥")


def test_luck_direction_profile_001() -> None:
    forward = calculate_luck_cycles("癸巳", LuckDirection.FORWARD, 3.0, 1)
    reverse = calculate_luck_cycles("癸巳", LuckDirection.REVERSE, 3.0, 1)
    assert forward[0].pillar != reverse[0].pillar


def test_luck_start_profile_001() -> None:
    cycle = calculate_luck_cycles("癸巳", LuckDirection.FORWARD, 2.5, 1)[0]
    assert cycle.start_age_years == 2.5 and cycle.end_age_years == 12.5


def test_decade_luck_sequence_001() -> None:
    cycles = calculate_luck_cycles("癸巳", LuckDirection.FORWARD, 3.0)
    assert len(cycles) == 8 and cycles[1].pillar == next_pillar("癸巳", 2)


def test_annual_cycle_001() -> None:
    assert calculate_annual_cycle(1984, "R").pillar == "甲子"
    assert calculate_annual_cycle(2024, "R").pillar == "甲辰"


def test_monthly_cycle_001() -> None:
    assert calculate_monthly_cycle(2024, 1, "R").pillar == "丙寅"


def test_rule_profile_difference_001(source_factory) -> None:
    source = source_factory(local_datetime="2000-02-29T23:30:00")
    first = calculate_natal_profile(
        source,
        standard_lichun_profile(),
        calculation_run_id="R1",
        natal_profile_id="N1",
        generated_at="T",
    )
    second = calculate_natal_profile(
        source,
        zi_hour_profile(),
        calculation_run_id="R2",
        natal_profile_id="N2",
        generated_at="T",
    )
    assert first.derivation_hash != second.derivation_hash


def test_same_input_same_result_001(source_factory) -> None:
    source = source_factory()
    first, _, _ = calculate_four_pillars(source, standard_lichun_profile())
    second, _, _ = calculate_four_pillars(source, standard_lichun_profile())
    assert first == second


def test_same_input_same_hash_001(source_factory) -> None:
    source = source_factory()
    first = calculate_natal_profile(source, standard_lichun_profile(), calculation_run_id="R", natal_profile_id="N", generated_at="T")
    second = calculate_natal_profile(source, standard_lichun_profile(), calculation_run_id="R", natal_profile_id="N", generated_at="T")
    assert first.derivation_hash == second.derivation_hash
