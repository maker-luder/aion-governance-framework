"""Explicit rule profiles; no school-specific interpretation is implied."""

from .enums import (
    DayRolloverRule,
    MonthBoundaryRule,
    OwnerReviewStatus,
    SolarTimeRule,
    YearBoundaryRule,
)
from .models import BaziRuleProfile


def standard_lichun_profile(
    profile_id: str = "STANDARD_LICHUN_MIDNIGHT_CIVIL_V1",
) -> BaziRuleProfile:
    return BaziRuleProfile(
        rule_profile_id=profile_id,
        profile_name="Standard Lichun / solar-jie / midnight / civil time",
        version="1.0.0",
        year_boundary_rule=YearBoundaryRule.LICHUN,
        month_boundary_rule=MonthBoundaryRule.SOLAR_JIE_BOUNDARY,
        day_rollover_rule=DayRolloverRule.MIDNIGHT_00,
        zi_hour_rule="MIDNIGHT_SECT_2",
        timezone_rule="IANA_ZONEINFO",
        dst_rule="IANA_TZDB",
        solar_time_rule=SolarTimeRule.STANDARD_CIVIL_TIME,
        solar_term_rule="LUNAR_PYTHON_1.4.8_JIE_QI_TABLE",
        luck_direction_rule="OWNER_EXPLICIT_DIRECTION",
        luck_start_rule="OWNER_EXPLICIT_START_AGE",
        hidden_stem_rule="LUNAR_PYTHON_1.4.8_TRADITIONAL_TABLE",
        hidden_stem_weight_rule="NO_WEIGHTS_IN_DETERMINISTIC_FACT",
        ten_god_rule="DAY_MASTER_RELATIVE_STANDARD",
        twelve_stage_rule="LUNAR_PYTHON_1.4.8_STANDARD",
        relationship_rule="VERSIONED_TRADITIONAL_LOOKUP_V1",
        strength_analysis_rule="INTERPRETATION_CANDIDATE_ONLY",
        structure_rule="INTERPRETATION_CANDIDATE_ONLY",
        useful_element_rule="INTERPRETATION_CANDIDATE_ONLY",
        transformation_rule="NOT_IMPLEMENTED_PENDING_OWNER_RULE_FREEZE",
        source_references=(
            "https://github.com/6tail/lunar-python",
            "lunar_python==1.4.8",
        ),
        owner_review_status=OwnerReviewStatus.PENDING,
    )


def zi_hour_profile() -> BaziRuleProfile:
    base = standard_lichun_profile("STANDARD_LICHUN_ZI23_CIVIL_V1")
    return BaziRuleProfile(
        **{
            **base.__dict__,
            "profile_name": "Standard Lichun / solar-jie / Zi 23 rollover / civil time",
            "day_rollover_rule": DayRolloverRule.ZI_HOUR_23,
            "zi_hour_rule": "LATE_ZI_NEXT_DAY_SECT_1",
        }
    )


def apparent_solar_profile() -> BaziRuleProfile:
    base = standard_lichun_profile("STANDARD_LICHUN_MIDNIGHT_APPARENT_SOLAR_V1")
    return BaziRuleProfile(
        **{
            **base.__dict__,
            "profile_name": "Standard Lichun / midnight / apparent solar candidate",
            "solar_time_rule": SolarTimeRule.APPARENT_SOLAR_TIME,
        }
    )
