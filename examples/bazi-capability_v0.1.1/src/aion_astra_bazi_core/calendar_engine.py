"""Offline calendar normalization and reviewed lunar-python adapter."""

from __future__ import annotations

import math
from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from lunar_python import Solar  # type: ignore[import-untyped]

from .enums import DayRolloverRule, MonthBoundaryRule, SolarTimeRule, YearBoundaryRule
from .errors import RuleProfileError, UnsupportedRangeError, ValidationError
from .models import BaziRuleProfile, BaziSourceInput, CalendarContext

ALGORITHM_VERSION = "AION_BAZI_CALENDAR_ADAPTER_0.1.0"
EPHEMERIS_VERSION = "lunar_python-1.4.8"
SUPPORTED_YEAR_MIN = 1900
SUPPORTED_YEAR_MAX = 2100


def _offset_text(value: timedelta | None) -> str:
    if value is None:
        raise ValidationError("timezone offset is unavailable")
    total = int(value.total_seconds())
    sign = "+" if total >= 0 else "-"
    total = abs(total)
    return f"{sign}{total // 3600:02d}:{(total % 3600) // 60:02d}"


def equation_of_time_minutes(value: datetime) -> float:
    day = value.timetuple().tm_yday
    b = math.radians((360.0 / 365.0) * (day - 81))
    return 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)


def normalize_source_time(source: BaziSourceInput, profile: BaziRuleProfile) -> tuple[datetime, datetime]:
    try:
        timezone = ZoneInfo(source.timezone_id)
    except ZoneInfoNotFoundError as exc:
        raise ValidationError(f"unknown IANA timezone: {source.timezone_id}") from exc
    parsed = datetime.fromisoformat(source.local_datetime)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone)
    else:
        parsed = parsed.astimezone(timezone)
    if not SUPPORTED_YEAR_MIN <= parsed.year <= SUPPORTED_YEAR_MAX:
        raise UnsupportedRangeError(
            f"supported Gregorian years are {SUPPORTED_YEAR_MIN}..{SUPPORTED_YEAR_MAX}"
        )
    actual_offset = _offset_text(parsed.utcoffset())
    if actual_offset != source.utc_offset_at_event:
        raise ValidationError(
            f"recorded UTC offset {source.utc_offset_at_event} does not match "
            f"IANA timezone offset {actual_offset}"
        )
    if not -180 <= source.longitude <= 180 or not -90 <= source.latitude <= 90:
        raise ValidationError("latitude or longitude is outside valid range")
    calculation = parsed
    if profile.solar_time_rule is not SolarTimeRule.STANDARD_CIVIL_TIME:
        parsed_offset = parsed.utcoffset()
        offset_hours = parsed_offset.total_seconds() / 3600 if parsed_offset else 0.0
        standard_meridian = offset_hours * 15.0
        longitude_minutes = 4.0 * (source.longitude - standard_meridian)
        if profile.solar_time_rule is SolarTimeRule.LONGITUDE_CORRECTION:
            calculation = parsed + timedelta(minutes=longitude_minutes)
        elif profile.solar_time_rule is SolarTimeRule.APPARENT_SOLAR_TIME:
            calculation = parsed + timedelta(
                minutes=longitude_minutes + equation_of_time_minutes(parsed)
            )
    return parsed, calculation


def calendar_context(
    source: BaziSourceInput,
    profile: BaziRuleProfile,
) -> tuple[CalendarContext, Any, Any]:
    if profile.month_boundary_rule is MonthBoundaryRule.OWNER_DEFINED:
        raise RuleProfileError("OWNER_DEFINED month boundary is not frozen")
    if profile.year_boundary_rule is YearBoundaryRule.OWNER_DEFINED:
        raise RuleProfileError("OWNER_DEFINED year boundary is not frozen")
    if profile.day_rollover_rule is DayRolloverRule.EARLY_LATE_ZI_PROFILE:
        raise RuleProfileError("EARLY_LATE_ZI_PROFILE requires an Owner-frozen subprofile")
    civil, calculation = normalize_source_time(source, profile)
    solar = Solar.fromYmdHms(
        calculation.year,
        calculation.month,
        calculation.day,
        calculation.hour,
        calculation.minute,
        calculation.second,
    )
    lunar = solar.getLunar()
    eight_char = lunar.getEightChar()
    eight_char.setSect(1 if profile.day_rollover_rule is DayRolloverRule.ZI_HOUR_23 else 2)
    previous_jie = lunar.getPrevJieQi(True)
    next_jie = lunar.getNextJieQi(True)
    actual_offset = civil.utcoffset()
    offset_hours = actual_offset.total_seconds() / 3600 if actual_offset else 0.0
    longitude_minutes = 4.0 * (source.longitude - offset_hours * 15.0)
    eot = equation_of_time_minutes(civil)
    context = CalendarContext(
        civil_local_datetime=civil.isoformat(),
        calculation_local_datetime=calculation.isoformat(),
        utc_datetime=civil.astimezone(ZoneInfo("UTC")).isoformat(),
        utc_offset=_offset_text(actual_offset),
        timezone_id=source.timezone_id,
        longitude_correction_minutes=round(longitude_minutes, 6),
        equation_of_time_minutes=round(eot, 6),
        previous_jie=str(previous_jie.getName()),
        previous_jie_datetime=str(previous_jie.getSolar().toYmdHms()),
        next_jie=str(next_jie.getName()),
        next_jie_datetime=str(next_jie.getSolar().toYmdHms()),
    )
    return context, lunar, eight_char
