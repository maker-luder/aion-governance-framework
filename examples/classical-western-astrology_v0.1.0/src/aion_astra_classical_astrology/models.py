"""Immutable source, rule-profile, and derived-fact records."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlanetPosition:
    planet: str
    longitude: float


@dataclass(frozen=True)
class ChartInput:
    input_id: str
    event_datetime_utc: str
    location_label: str
    latitude: float
    longitude: float
    ascendant_longitude: float
    midheaven_longitude: float
    is_day_chart: bool
    positions: tuple[PlanetPosition, ...]
    ephemeris_source: str
    ephemeris_version: str
    coordinate_frame: str
    synthetic_fixture: bool


@dataclass(frozen=True)
class ClassicalRuleProfile:
    profile_id: str
    version: str
    tradition_scope: str
    zodiac: str
    house_system: str
    planet_set: tuple[str, ...]
    aspect_angles: tuple[tuple[str, float], ...]
    aspect_orbs: tuple[tuple[str, float], ...]
    dignity_scheme: str
    sect_rule: str
    source_references: tuple[str, ...]


@dataclass(frozen=True)
class PlanetFact:
    planet: str
    longitude: float
    sign: str
    sign_degree: float
    whole_sign_house: int
    domicile_ruler: str
    essential_dignities: tuple[str, ...]
    sect_status: str


@dataclass(frozen=True)
class AspectFact:
    first_planet: str
    second_planet: str
    aspect: str
    exact_angle: float
    separation: float
    orb: float
    phase: str


@dataclass(frozen=True)
class ClassicalChart:
    chart_id: str
    input_id: str
    rule_profile_id: str
    algorithm_version: str
    ephemeris_source: str
    ephemeris_version: str
    sect: str
    ascendant_sign: str
    midheaven_sign: str
    planets: tuple[PlanetFact, ...]
    aspects: tuple[AspectFact, ...]
    derivation_trace: tuple[dict[str, object], ...]
    derivation_hash: str
    interpretation_status: str
    canonical_effect: str
    deployment: bool
    action_authority: str
