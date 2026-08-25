"""Deterministic Bazi calculation engine with explicit provenance."""

from __future__ import annotations

from typing import Any, Callable

from lunar_python.util import LunarUtil  # type: ignore[import-untyped]

from .calculations import (
    calculate_luck_cycles as build_luck_cycles,
    calculate_relationships as build_relationships,
)
from .calendar_engine import (
    ALGORITHM_VERSION,
    EPHEMERIS_VERSION,
    calendar_context,
)
from .constants import (
    BRANCHES,
    BRANCH_ELEMENTS,
    HIDDEN_STEMS,
    STEMS,
    STEM_ELEMENTS,
    YIN_YANG,
)
from .enums import LuckDirection, YearBoundaryRule
from .errors import ValidationError
from .models import (
    BaziRuleProfile,
    BaziSourceInput,
    CycleFact,
    LuckCycle,
    NatalProfile,
    Pillar,
)
from .serialization import derivation_hash

CHANG_SHENG = ("长生", "沐浴", "冠带", "临官", "帝旺", "衰", "病", "死", "墓", "绝", "胎", "养")
CHANG_SHENG_OFFSET = {"甲": 1, "丙": 10, "戊": 10, "庚": 7, "壬": 4, "乙": 6, "丁": 9, "己": 9, "辛": 0, "癸": 3}


def ten_god(day_master: str, other: str) -> str:
    generating = {"WOOD": "FIRE", "FIRE": "EARTH", "EARTH": "METAL", "METAL": "WATER", "WATER": "WOOD"}
    controlling = {"WOOD": "EARTH", "EARTH": "WATER", "WATER": "FIRE", "FIRE": "METAL", "METAL": "WOOD"}
    day_element = STEM_ELEMENTS[day_master]
    other_element = STEM_ELEMENTS[other]
    same_polarity = YIN_YANG[day_master] == YIN_YANG[other]
    if day_element == other_element:
        return "比肩" if same_polarity else "劫财"
    if generating[day_element] == other_element:
        return "食神" if same_polarity else "伤官"
    if generating[other_element] == day_element:
        return "偏印" if same_polarity else "正印"
    if controlling[day_element] == other_element:
        return "偏财" if same_polarity else "正财"
    return "七杀" if same_polarity else "正官"


def twelve_stage(day_master: str, branch: str) -> str:
    offset = CHANG_SHENG_OFFSET[day_master]
    branch_index = BRANCHES.index(branch)
    if YIN_YANG[day_master] == "YANG":
        return CHANG_SHENG[(branch_index - offset) % 12]
    return CHANG_SHENG[(offset - branch_index) % 12]


def _pillar(
    name: str,
    ganzhi: str,
    day_master: str,
    hide_getter: Callable[[], Any],
    nayin_getter: Callable[[], Any],
    stage_getter: Callable[[], Any],
    void_getter: Callable[[], Any],
) -> Pillar:
    stem, branch = ganzhi[0], ganzhi[1]
    hidden = tuple(str(value) for value in hide_getter())
    gods = (ten_god(day_master, stem),) + tuple(ten_god(day_master, value) for value in hidden)
    void_text = str(void_getter())
    return Pillar(
        name=name,
        stem=stem,
        branch=branch,
        yin_yang=YIN_YANG[stem],
        stem_element=STEM_ELEMENTS[stem],
        branch_element=BRANCH_ELEMENTS[branch],
        hidden_stems=hidden,
        ten_gods=gods,
        nayin=str(nayin_getter()),
        twelve_stage=str(stage_getter()),
        void_branches=tuple(void_text),
    )


def _lunar_year_pillar(lunar: Any, day_master: str) -> Pillar:
    ganzhi = str(lunar.getYearInGanZhi())
    stem, branch = ganzhi[0], ganzhi[1]
    hidden = HIDDEN_STEMS[branch]
    return Pillar(
        name="YEAR",
        stem=stem,
        branch=branch,
        yin_yang=YIN_YANG[stem],
        stem_element=STEM_ELEMENTS[stem],
        branch_element=BRANCH_ELEMENTS[branch],
        hidden_stems=hidden,
        ten_gods=(ten_god(day_master, stem),) + tuple(ten_god(day_master, value) for value in hidden),
        nayin=str(LunarUtil.NAYIN[ganzhi]),
        twelve_stage=twelve_stage(day_master, branch),
        void_branches=tuple(str(LunarUtil.getXunKong(ganzhi))),
    )


def calculate_four_pillars(
    source: BaziSourceInput,
    profile: BaziRuleProfile,
) -> tuple[tuple[Pillar, ...], Any, tuple[dict[str, Any], ...]]:
    context, lunar, eight_char = calendar_context(source, profile)
    day_ganzhi = str(eight_char.getDay())
    day_master = day_ganzhi[0]
    year = _pillar(
        "YEAR",
        str(eight_char.getYear()),
        day_master,
        eight_char.getYearHideGan,
        eight_char.getYearNaYin,
        eight_char.getYearDiShi,
        eight_char.getYearXunKong,
    )
    if profile.year_boundary_rule is YearBoundaryRule.LUNAR_NEW_YEAR:
        year = _lunar_year_pillar(lunar, day_master)
    month = _pillar(
        "MONTH",
        str(eight_char.getMonth()),
        day_master,
        eight_char.getMonthHideGan,
        eight_char.getMonthNaYin,
        eight_char.getMonthDiShi,
        eight_char.getMonthXunKong,
    )
    day = _pillar(
        "DAY",
        day_ganzhi,
        day_master,
        eight_char.getDayHideGan,
        eight_char.getDayNaYin,
        eight_char.getDayDiShi,
        eight_char.getDayXunKong,
    )
    hour = _pillar(
        "HOUR",
        str(eight_char.getTime()),
        day_master,
        eight_char.getTimeHideGan,
        eight_char.getTimeNaYin,
        eight_char.getTimeDiShi,
        eight_char.getTimeXunKong,
    )
    trace = (
        {"step": 1, "operation": "NORMALIZE_IANA_TIMEZONE", "result": context.civil_local_datetime},
        {"step": 2, "operation": profile.solar_time_rule.value, "result": context.calculation_local_datetime},
        {"step": 3, "operation": profile.year_boundary_rule.value, "result": year.ganzhi},
        {"step": 4, "operation": profile.month_boundary_rule.value, "result": month.ganzhi},
        {"step": 5, "operation": profile.day_rollover_rule.value, "result": day.ganzhi},
        {"step": 6, "operation": "DOUBLE_HOUR_STANDARD", "result": hour.ganzhi},
    )
    return (year, month, day, hour), context, trace


def calculate_natal_profile(
    source: BaziSourceInput,
    profile: BaziRuleProfile,
    *,
    calculation_run_id: str,
    natal_profile_id: str,
    generated_at: str,
) -> NatalProfile:
    if not calculation_run_id or not natal_profile_id:
        raise ValidationError("calculation_run_id and natal_profile_id are required")
    pillars, context, trace = calculate_four_pillars(source, profile)
    relations = build_relationships(pillars)
    hash_payload = {
        "input": source,
        "rule_profile": profile,
        "pillars": pillars,
        "relations": relations,
        "calendar_context": context,
        "trace": trace,
        "algorithm_version": ALGORITHM_VERSION,
        "ephemeris_version": EPHEMERIS_VERSION,
    }
    return NatalProfile(
        natal_profile_id=natal_profile_id,
        input_id=source.input_id,
        calculation_run_id=calculation_run_id,
        rule_profile_id=profile.rule_profile_id,
        algorithm_version=ALGORITHM_VERSION,
        ephemeris_version=EPHEMERIS_VERSION,
        pillars=pillars,
        relations=relations,
        calendar_context=context,
        derivation_trace=trace,
        derivation_hash=derivation_hash(hash_payload),
        generated_at=generated_at,
    )


def calculate_luck_cycles(
    profile: NatalProfile,
    direction: LuckDirection,
    start_age_years: float,
    count: int = 8,
) -> tuple[LuckCycle, ...]:
    month = next(pillar for pillar in profile.pillars if pillar.name == "MONTH")
    return build_luck_cycles(month.ganzhi, direction, start_age_years, count)


def calculate_annual_cycle(year: int, rule_profile_id: str) -> CycleFact:
    index = (year - 1984) % 60
    return CycleFact("ANNUAL", year, None, STEMS[index % 10] + BRANCHES[index % 12], rule_profile_id)


def calculate_monthly_cycle(year: int, month: int, rule_profile_id: str) -> CycleFact:
    if not 1 <= month <= 12:
        raise ValidationError("month must be 1..12")
    annual = calculate_annual_cycle(year, rule_profile_id)
    year_stem_index = STEMS.index(annual.pillar[0])
    first_month_stem = ((year_stem_index % 5) * 2 + 2) % 10
    stem = STEMS[(first_month_stem + month - 1) % 10]
    branch = BRANCHES[(2 + month - 1) % 12]
    return CycleFact("MONTHLY_CANDIDATE", year, month, stem + branch, rule_profile_id)


def verify_derivation_hash(
    source: BaziSourceInput,
    rule_profile: BaziRuleProfile,
    profile: NatalProfile,
) -> bool:
    recalculated = calculate_natal_profile(
        source,
        rule_profile,
        calculation_run_id=profile.calculation_run_id,
        natal_profile_id=profile.natal_profile_id,
        generated_at=profile.generated_at,
    )
    return recalculated.derivation_hash == profile.derivation_hash
