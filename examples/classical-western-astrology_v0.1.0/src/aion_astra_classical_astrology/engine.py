"""Deterministic derivation of bounded classical chart facts."""

from __future__ import annotations

from itertools import combinations

from .constants import (
    ASPECT_ANGLES,
    DOMICILE_RULERS,
    EXALTATION_SIGNS,
    OPPOSITE_SIGN,
    SIGNS,
    TRADITIONAL_PLANETS,
)
from .errors import ValidationError
from .models import (
    AspectFact,
    ChartInput,
    ClassicalChart,
    ClassicalRuleProfile,
    PlanetFact,
)
from .serialization import derivation_hash

ALGORITHM_VERSION = "classical-western-fact-derivation-0.1.0"


def normalize_longitude(value: float) -> float:
    if not isinstance(value, (int, float)) or not 0.0 <= float(value) < 360.0:
        raise ValidationError("longitude must be within [0, 360)")
    return float(value)


def sign_for_longitude(value: float) -> str:
    return SIGNS[int(normalize_longitude(value) // 30)]


def whole_sign_house(planet_longitude: float, ascendant_longitude: float) -> int:
    planet_sign = int(normalize_longitude(planet_longitude) // 30)
    ascendant_sign = int(normalize_longitude(ascendant_longitude) // 30)
    return ((planet_sign - ascendant_sign) % 12) + 1


def _validate(source: ChartInput, profile: ClassicalRuleProfile) -> None:
    if not source.synthetic_fixture:
        raise ValidationError("v0.1.0 accepts synthetic fixtures only")
    if not source.input_id.startswith("SYNTHETIC_") or not source.location_label.startswith("SYNTHETIC_"):
        raise ValidationError("synthetic input and location labels are required")
    if not source.event_datetime_utc.endswith("Z"):
        raise ValidationError("event_datetime_utc must be an explicit UTC value ending in Z")
    if source.coordinate_frame != "GEOCENTRIC_TROPICAL_ECLIPTIC_OF_DATE":
        raise ValidationError("unsupported coordinate frame")
    if profile.zodiac != "TROPICAL" or profile.house_system != "WHOLE_SIGN":
        raise ValidationError("v0.1.0 requires tropical zodiac and whole-sign houses")
    if profile.planet_set != TRADITIONAL_PLANETS:
        raise ValidationError("v0.1.0 requires exactly the traditional seven planets")
    if dict(profile.aspect_angles) != ASPECT_ANGLES:
        raise ValidationError("v0.1.0 requires exactly the five classical aspects")
    if profile.dignity_scheme != "TRADITIONAL_SIGN_BASED_DOMICILE_EXALTATION_DETRIMENT_FALL":
        raise ValidationError("unsupported dignity scheme")
    if not source.ephemeris_source or not source.ephemeris_version:
        raise ValidationError("ephemeris source and version are required")
    if not -90.0 <= source.latitude <= 90.0 or not -180.0 <= source.longitude <= 180.0:
        raise ValidationError("invalid geographic coordinates")
    normalize_longitude(source.ascendant_longitude)
    normalize_longitude(source.midheaven_longitude)
    names = tuple(position.planet for position in source.positions)
    if len(names) != len(set(names)):
        raise ValidationError("each planet must appear exactly once")
    if set(names) != set(profile.planet_set):
        raise ValidationError("positions must contain exactly the profile planet set")
    for position in source.positions:
        normalize_longitude(position.longitude)


def _dignities(planet: str, sign: str) -> tuple[str, ...]:
    dignities: list[str] = []
    domicile_signs = {name for name, ruler in DOMICILE_RULERS.items() if ruler == planet}
    if sign in domicile_signs:
        dignities.append("DOMICILE")
    if EXALTATION_SIGNS[planet] == sign:
        dignities.append("EXALTATION")
    if OPPOSITE_SIGN[sign] in domicile_signs:
        dignities.append("DETRIMENT")
    if OPPOSITE_SIGN[sign] == EXALTATION_SIGNS[planet]:
        dignities.append("FALL")
    return tuple(dignities) or ("PEREGRINE_BY_MAJOR_SIGN_DIGNITIES",)


def _sect_status(planet: str, is_day_chart: bool) -> str:
    if planet == "MERCURY":
        return "VARIABLE_NOT_DERIVED_WITHOUT_SOLAR_PHASE"
    diurnal = {"SUN", "JUPITER", "SATURN"}
    nocturnal = {"MOON", "VENUS", "MARS"}
    if (is_day_chart and planet in diurnal) or (not is_day_chart and planet in nocturnal):
        return "OF_SECT"
    return "CONTRARY_TO_SECT"


def derive_planet_facts(
    source: ChartInput,
    profile: ClassicalRuleProfile,
) -> tuple[PlanetFact, ...]:
    _validate(source, profile)
    facts = []
    for position in source.positions:
        sign = sign_for_longitude(position.longitude)
        facts.append(
            PlanetFact(
                planet=position.planet,
                longitude=position.longitude,
                sign=sign,
                sign_degree=round(position.longitude % 30.0, 8),
                whole_sign_house=whole_sign_house(position.longitude, source.ascendant_longitude),
                domicile_ruler=DOMICILE_RULERS[sign],
                essential_dignities=_dignities(position.planet, sign),
                sect_status=_sect_status(position.planet, source.is_day_chart),
            )
        )
    return tuple(facts)


def _separation(first: float, second: float) -> float:
    raw = abs(first - second) % 360.0
    return min(raw, 360.0 - raw)


def derive_aspects(source: ChartInput, profile: ClassicalRuleProfile) -> tuple[AspectFact, ...]:
    _validate(source, profile)
    angles = dict(profile.aspect_angles)
    orbs = dict(profile.aspect_orbs)
    aspects: list[AspectFact] = []
    for first, second in combinations(source.positions, 2):
        separation = _separation(first.longitude, second.longitude)
        candidates = sorted(
            (
                (abs(separation - angle), name, angle)
                for name, angle in angles.items()
                if abs(separation - angle) <= orbs[name]
            ),
            key=lambda item: (item[0], item[2]),
        )
        if candidates:
            orb, name, exact = candidates[0]
            aspects.append(
                AspectFact(
                    first_planet=first.planet,
                    second_planet=second.planet,
                    aspect=name,
                    exact_angle=exact,
                    separation=round(separation, 8),
                    orb=round(orb, 8),
                    phase="NOT_DERIVED_WITHOUT_SPEED_VECTORS",
                )
            )
    return tuple(aspects)


def build_chart(
    source: ChartInput,
    profile: ClassicalRuleProfile,
    *,
    chart_id: str,
) -> ClassicalChart:
    if not chart_id:
        raise ValidationError("chart_id is required")
    planets = derive_planet_facts(source, profile)
    aspects = derive_aspects(source, profile)
    trace: tuple[dict[str, object], ...] = (
        {"step": 1, "operation": "VALIDATE_VERSIONED_EPHEMERIS_INPUT", "result": source.ephemeris_version},
        {"step": 2, "operation": "MAP_TROPICAL_SIGNS", "result": len(planets)},
        {"step": 3, "operation": "ASSIGN_WHOLE_SIGN_HOUSES", "result": sign_for_longitude(source.ascendant_longitude)},
        {"step": 4, "operation": "DERIVE_MAJOR_SIGN_DIGNITIES", "result": profile.dignity_scheme},
        {"step": 5, "operation": "DERIVE_PTOLEMAIC_ASPECTS", "result": len(aspects)},
        {"step": 6, "operation": "PRESERVE_INTERPRETATION_BOUNDARY", "result": "NOT_PERFORMED"},
    )
    payload = {
        "source": source,
        "profile": profile,
        "planets": planets,
        "aspects": aspects,
        "trace": trace,
        "algorithm_version": ALGORITHM_VERSION,
    }
    return ClassicalChart(
        chart_id=chart_id,
        input_id=source.input_id,
        rule_profile_id=profile.profile_id,
        algorithm_version=ALGORITHM_VERSION,
        ephemeris_source=source.ephemeris_source,
        ephemeris_version=source.ephemeris_version,
        sect="DIURNAL" if source.is_day_chart else "NOCTURNAL",
        ascendant_sign=sign_for_longitude(source.ascendant_longitude),
        midheaven_sign=sign_for_longitude(source.midheaven_longitude),
        planets=planets,
        aspects=aspects,
        derivation_trace=trace,
        derivation_hash=derivation_hash(payload),
        interpretation_status="NOT_PERFORMED",
        canonical_effect="NONE",
        deployment=False,
        action_authority="NONE",
    )
