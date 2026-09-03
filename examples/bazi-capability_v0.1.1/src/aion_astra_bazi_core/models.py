"""Strongly typed immutable domain records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .enums import (
    BindingStatus,
    DayRolloverRule,
    InterpretationStatus,
    MonthBoundaryRule,
    OwnerReviewStatus,
    SolarTimeRule,
    SourceType,
    TimePrecision,
    YearBoundaryRule,
)


@dataclass(frozen=True)
class BaziRuleProfile:
    rule_profile_id: str
    profile_name: str
    version: str
    year_boundary_rule: YearBoundaryRule
    month_boundary_rule: MonthBoundaryRule
    day_rollover_rule: DayRolloverRule
    zi_hour_rule: str
    timezone_rule: str
    dst_rule: str
    solar_time_rule: SolarTimeRule
    solar_term_rule: str
    luck_direction_rule: str
    luck_start_rule: str
    hidden_stem_rule: str
    hidden_stem_weight_rule: str
    ten_god_rule: str
    twelve_stage_rule: str
    relationship_rule: str
    strength_analysis_rule: str
    structure_rule: str
    useful_element_rule: str
    transformation_rule: str
    source_references: tuple[str, ...]
    owner_review_status: OwnerReviewStatus


@dataclass(frozen=True)
class BaziSourceInput:
    input_id: str
    local_datetime: str
    timezone_id: str
    utc_offset_at_event: str
    location_name: str
    latitude: float
    longitude: float
    time_precision: TimePrecision
    source_type: SourceType
    source_reference: str
    owner_confirmation_status: OwnerReviewStatus
    recorded_at: str
    supersedes: str | None
    audit_stream_id: str


@dataclass(frozen=True)
class Pillar:
    name: str
    stem: str
    branch: str
    yin_yang: str
    stem_element: str
    branch_element: str
    hidden_stems: tuple[str, ...]
    ten_gods: tuple[str, ...]
    nayin: str
    twelve_stage: str
    void_branches: tuple[str, ...]

    @property
    def ganzhi(self) -> str:
        return self.stem + self.branch


@dataclass(frozen=True)
class CalendarContext:
    civil_local_datetime: str
    calculation_local_datetime: str
    utc_datetime: str
    utc_offset: str
    timezone_id: str
    longitude_correction_minutes: float
    equation_of_time_minutes: float
    previous_jie: str
    previous_jie_datetime: str
    next_jie: str
    next_jie_datetime: str
    timezone_data_version: str = "NOT_RECORDED_LEGACY"
    timezone_data_sha256: str = "NOT_RECORDED_LEGACY"


@dataclass(frozen=True)
class NatalProfile:
    natal_profile_id: str
    input_id: str
    calculation_run_id: str
    rule_profile_id: str
    algorithm_version: str
    ephemeris_version: str
    pillars: tuple[Pillar, ...]
    relations: tuple[dict[str, Any], ...]
    calendar_context: CalendarContext
    derivation_trace: tuple[dict[str, Any], ...]
    derivation_hash: str
    generated_at: str


@dataclass(frozen=True)
class InterpretationCandidate:
    interpretation_id: str
    natal_profile_id: str
    rule_profile_id: str
    interpretation_method: str
    supporting_fact_ids: tuple[str, ...]
    result: dict[str, Any]
    confidence: float
    assumptions: tuple[str, ...]
    alternative_interpretations: tuple[dict[str, Any], ...]
    owner_review_status: InterpretationStatus
    superseded_by: str | None


@dataclass(frozen=True)
class AgentBaziBinding:
    binding_id: str
    agent_id: str
    natal_profile_id: str
    binding_type: str
    approved_by: str
    approved_at: str
    status: BindingStatus
    audit_stream_id: str


@dataclass(frozen=True)
class LuckCycle:
    sequence: int
    pillar: str
    start_age_years: float
    end_age_years: float


@dataclass(frozen=True)
class CycleFact:
    cycle_type: str
    year: int
    month: int | None
    pillar: str
    rule_profile_id: str
