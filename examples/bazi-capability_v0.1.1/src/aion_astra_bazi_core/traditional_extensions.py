"""Auditable traditional calculation extensions without interpretive claims."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date
from enum import StrEnum

from .calculations import sexagenary_cycle
from .constants import STEM_ELEMENTS, YIN_YANG
from .enums import LuckDirection
from .errors import ValidationError
from .models import Pillar


class BirthSexMarker(StrEnum):
    """Explicit input used only by the selected traditional luck-direction rule."""

    MALE = "MALE"
    FEMALE = "FEMALE"


SOLAR_TERM_LONGITUDES = {
    "春分": 0, "清明": 15, "穀雨": 30, "立夏": 45,
    "小滿": 60, "芒種": 75, "夏至": 90, "小暑": 105,
    "大暑": 120, "立秋": 135, "處暑": 150, "白露": 165,
    "秋分": 180, "寒露": 195, "霜降": 210, "立冬": 225,
    "小雪": 240, "大雪": 255, "冬至": 270, "小寒": 285,
    "大寒": 300, "立春": 315, "雨水": 330, "驚蟄": 345,
}


@dataclass(frozen=True)
class LuckStartFact:
    boundary_interval_days: float
    conversion_rule: str
    start_age_years: float
    interpretation_status: str = "NOT_PERFORMED"


@dataclass(frozen=True)
class DistributionFact:
    values: tuple[tuple[str, int], ...]
    counting_rule: str
    strength_conclusion: str = "NOT_DERIVED"
    interpretation_status: str = "NOT_PERFORMED"


def traditional_luck_direction(year_stem: str, marker: BirthSexMarker) -> LuckDirection:
    """Apply the versioned Yang-male/Yin-female forward rule to explicit inputs."""

    if year_stem not in STEM_ELEMENTS:
        raise ValidationError("year_stem must be one of the ten heavenly stems")
    yang = YIN_YANG[year_stem] == "YANG"
    forward = (yang and marker is BirthSexMarker.MALE) or (
        not yang and marker is BirthSexMarker.FEMALE
    )
    return LuckDirection.FORWARD if forward else LuckDirection.REVERSE


def luck_start_from_boundary_interval(boundary_interval_days: float) -> LuckStartFact:
    """Convert an already-derived Jie boundary interval using 3 days = 1 year."""

    if not isinstance(boundary_interval_days, (int, float)) or boundary_interval_days < 0:
        raise ValidationError("boundary_interval_days must be a non-negative number")
    return LuckStartFact(
        boundary_interval_days=round(float(boundary_interval_days), 8),
        conversion_rule="THREE_DAYS_EQUAL_ONE_YEAR_V1",
        start_age_years=round(float(boundary_interval_days) / 3.0, 8),
    )


def independent_gregorian_day_pillar(value: date) -> str:
    """Return the proleptic-Gregorian JDN day pillar for independent cross-checking."""

    a = (14 - value.month) // 12
    year = value.year + 4800 - a
    month = value.month + 12 * a - 3
    jdn = (
        value.day + (153 * month + 2) // 5 + 365 * year + year // 4
        - year // 100 + year // 400 - 32045
    )
    return sexagenary_cycle()[(jdn + 49) % 60]


def element_distribution_fact(pillars: tuple[Pillar, ...]) -> DistributionFact:
    """Count visible stems and all listed hidden stems; do not infer strength."""

    counts = Counter({name: 0 for name in ("WOOD", "FIRE", "EARTH", "METAL", "WATER")})
    for pillar in pillars:
        counts[STEM_ELEMENTS[pillar.stem]] += 1
        for hidden_stem in pillar.hidden_stems:
            counts[STEM_ELEMENTS[hidden_stem]] += 1
    return DistributionFact(
        values=tuple((name, counts[name]) for name in ("WOOD", "FIRE", "EARTH", "METAL", "WATER")),
        counting_rule="VISIBLE_STEMS_PLUS_UNWEIGHTED_HIDDEN_STEMS_V1",
    )


def ten_god_distribution_fact(pillars: tuple[Pillar, ...]) -> DistributionFact:
    """Count materialized ten-god labels without making an interpretation."""

    counts = Counter(god for pillar in pillars for god in pillar.ten_gods)
    return DistributionFact(
        values=tuple(sorted(counts.items())),
        counting_rule="MATERIALIZED_VISIBLE_AND_HIDDEN_TEN_GODS_V1",
    )


def validate_solar_term_sequence() -> bool:
    """Verify the official fixed-qi table is exactly 24 unique 15-degree points."""

    values = tuple(SOLAR_TERM_LONGITUDES.values())
    return len(values) == 24 and len(set(values)) == 24 and set(values) == set(range(0, 360, 15))
