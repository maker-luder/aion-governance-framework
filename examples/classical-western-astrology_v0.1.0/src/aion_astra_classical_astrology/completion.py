"""Classical-completion facts and a strictly labelled modern-point overlay.

The functions in this module extend the existing v0.2 chart without replacing
its classical core.  They derive inspectable historical rule-table facts only;
they do not produce personality, fate, subjectivity, consciousness, or action
recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .constants import (
    INTEGRATED_ASPECT_ANGLES,
    SIGN_ELEMENTS,
    SIGNS,
    TRADITIONAL_PLANETS,
)
from .engine import build_chart, normalize_longitude, sign_for_longitude, whole_sign_house
from .errors import ValidationError
from .models import AspectFact, ChartInput, ClassicalChart, PlanetPosition
from .profiles import integrated_classical_modern_profile
from .serialization import derivation_hash


ALGORITHM_VERSION = "classical-completion-modern-points-0.3.0"

# Dorothean day/night/participating triplicity rulers.  The participating ruler
# is retained as a separate fact and never substituted for the sect ruler.
TRIPLICITY_RULERS = {
    "FIRE": ("SUN", "JUPITER", "SATURN"),
    "EARTH": ("VENUS", "MOON", "MARS"),
    "AIR": ("SATURN", "MERCURY", "JUPITER"),
    "WATER": ("VENUS", "MARS", "MOON"),
}

# Egyptian bounds/terms as half-open [start, end) degree intervals.  A named
# profile makes the school choice machine-visible; no generic "the bounds" is
# implied.
EGYPTIAN_BOUNDS = {
    "ARIES": ((0, 6, "JUPITER"), (6, 14, "VENUS"), (14, 21, "MERCURY"), (21, 26, "MARS"), (26, 30, "SATURN")),
    "TAURUS": ((0, 8, "VENUS"), (8, 14, "MERCURY"), (14, 22, "JUPITER"), (22, 27, "SATURN"), (27, 30, "MARS")),
    "GEMINI": ((0, 6, "MERCURY"), (6, 12, "JUPITER"), (12, 17, "VENUS"), (17, 24, "MARS"), (24, 30, "SATURN")),
    "CANCER": ((0, 7, "MARS"), (7, 13, "VENUS"), (13, 19, "MERCURY"), (19, 26, "JUPITER"), (26, 30, "SATURN")),
    "LEO": ((0, 6, "JUPITER"), (6, 11, "VENUS"), (11, 18, "SATURN"), (18, 24, "MERCURY"), (24, 30, "MARS")),
    "VIRGO": ((0, 7, "MERCURY"), (7, 17, "VENUS"), (17, 21, "JUPITER"), (21, 28, "MARS"), (28, 30, "SATURN")),
    "LIBRA": ((0, 6, "SATURN"), (6, 14, "MERCURY"), (14, 21, "JUPITER"), (21, 28, "VENUS"), (28, 30, "MARS")),
    "SCORPIO": ((0, 7, "MARS"), (7, 11, "VENUS"), (11, 19, "MERCURY"), (19, 24, "JUPITER"), (24, 30, "SATURN")),
    "SAGITTARIUS": ((0, 12, "JUPITER"), (12, 17, "VENUS"), (17, 21, "MERCURY"), (21, 26, "SATURN"), (26, 30, "MARS")),
    "CAPRICORN": ((0, 7, "MERCURY"), (7, 14, "JUPITER"), (14, 22, "VENUS"), (22, 26, "SATURN"), (26, 30, "MARS")),
    "AQUARIUS": ((0, 7, "MERCURY"), (7, 13, "VENUS"), (13, 20, "JUPITER"), (20, 25, "MARS"), (25, 30, "SATURN")),
    "PISCES": ((0, 12, "VENUS"), (12, 16, "JUPITER"), (16, 19, "MERCURY"), (19, 28, "MARS"), (28, 30, "SATURN")),
}

# Chaldean face/decan sequence, three ten-degree faces per sign.
FACE_RULERS = {
    "ARIES": ("MARS", "SUN", "VENUS"), "TAURUS": ("MERCURY", "MOON", "SATURN"),
    "GEMINI": ("JUPITER", "MARS", "SUN"), "CANCER": ("VENUS", "MERCURY", "MOON"),
    "LEO": ("SATURN", "JUPITER", "MARS"), "VIRGO": ("SUN", "VENUS", "MERCURY"),
    "LIBRA": ("MOON", "SATURN", "JUPITER"), "SCORPIO": ("MARS", "SUN", "VENUS"),
    "SAGITTARIUS": ("MERCURY", "MOON", "SATURN"), "CAPRICORN": ("JUPITER", "MARS", "SUN"),
    "AQUARIUS": ("VENUS", "MERCURY", "MOON"), "PISCES": ("SATURN", "JUPITER", "MARS"),
}

PLANETARY_JOYS = {"MERCURY": 1, "MOON": 3, "VENUS": 5, "MARS": 6, "SUN": 9, "JUPITER": 11, "SATURN": 12}
MODERN_POINT_SET = ("TRUE_NORTH_NODE", "CHIRON")


@dataclass(frozen=True)
class ExtendedDignityFact:
    planet: str
    triplicity_element: str
    sect_triplicity_ruler: str
    participating_triplicity_ruler: str
    planet_is_sect_triplicity_ruler: bool
    egyptian_bound_ruler: str
    chaldean_face_ruler: str
    planetary_joy_house: int
    is_in_planetary_joy: bool
    rule_profile: str = "DOROTHEAN_TRIPLICITY_EGYPTIAN_BOUNDS_CHALDEAN_FACES_V1"


@dataclass(frozen=True)
class ModernPointFact:
    point: str
    longitude: float
    sign: str
    sign_degree: float
    whole_sign_house: int
    motion_status: str
    classical_dignity_status: str = "NOT_APPLICABLE"
    classical_sect_status: str = "NOT_APPLICABLE"
    rulership_status: str = "NO_RULERSHIP_ASSIGNED"


@dataclass(frozen=True)
class IntegratedAstrologyCompletion:
    base_chart: ClassicalChart
    extended_dignities: tuple[ExtendedDignityFact, ...]
    modern_points: tuple[ModernPointFact, ...]
    modern_point_aspects: tuple[AspectFact, ...]
    algorithm_version: str
    derivation_hash: str
    interpretation_status: str = "NOT_PERFORMED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False
    action_authority: str = "NONE"


def _bound_ruler(sign: str, sign_degree: float) -> str:
    for start, end, ruler in EGYPTIAN_BOUNDS[sign]:
        if start <= sign_degree < end:
            return ruler
    raise ValidationError("sign_degree must be within [0, 30)")


def derive_extended_dignities(source: ChartInput) -> tuple[ExtendedDignityFact, ...]:
    """Derive the three omitted classical dignity layers plus planetary joys."""

    traditional = {position.planet: position for position in source.positions if position.planet in TRADITIONAL_PLANETS}
    if set(traditional) != set(TRADITIONAL_PLANETS):
        raise ValidationError("extended dignities require the traditional seven planet positions")
    result = []
    for planet in TRADITIONAL_PLANETS:
        position = traditional[planet]
        sign = sign_for_longitude(position.longitude)
        degree = position.longitude % 30.0
        day_ruler, night_ruler, participating = TRIPLICITY_RULERS[SIGN_ELEMENTS[sign]]
        sect_ruler = day_ruler if source.is_day_chart else night_ruler
        house = whole_sign_house(position.longitude, source.ascendant_longitude)
        result.append(ExtendedDignityFact(
            planet=planet,
            triplicity_element=SIGN_ELEMENTS[sign],
            sect_triplicity_ruler=sect_ruler,
            participating_triplicity_ruler=participating,
            planet_is_sect_triplicity_ruler=planet == sect_ruler,
            egyptian_bound_ruler=_bound_ruler(sign, degree),
            chaldean_face_ruler=FACE_RULERS[sign][min(int(degree // 10), 2)],
            planetary_joy_house=PLANETARY_JOYS[planet],
            is_in_planetary_joy=house == PLANETARY_JOYS[planet],
        ))
    return tuple(result)


def _motion_status(speed: float | None) -> str:
    if speed is None:
        return "NOT_DERIVED_WITHOUT_SPEED_VECTOR"
    if speed < 0:
        return "RETROGRADE"
    if speed > 0:
        return "DIRECT"
    return "STATIONARY"


def derive_modern_points(source: ChartInput, points: tuple[PlanetPosition, ...]) -> tuple[ModernPointFact, ...]:
    """Derive a labelled node/Chiron overlay without treating either as a planet."""

    names = tuple(point.planet for point in points)
    if names != MODERN_POINT_SET:
        raise ValidationError(f"modern points must be ordered exactly as {MODERN_POINT_SET!r}")
    if len(set(names)) != len(names):
        raise ValidationError("modern point names must be unique")
    facts: list[ModernPointFact] = []
    for point in points:
        longitude = normalize_longitude(point.longitude)
        facts.append(ModernPointFact(
            point=point.planet,
            longitude=longitude,
            sign=sign_for_longitude(longitude),
            sign_degree=round(longitude % 30.0, 8),
            whole_sign_house=whole_sign_house(longitude, source.ascendant_longitude),
            motion_status=_motion_status(point.speed_longitude),
        ))
    north = facts[0]
    south_longitude = (north.longitude + 180.0) % 360.0
    facts.append(ModernPointFact(
        point="TRUE_SOUTH_NODE",
        longitude=south_longitude,
        sign=sign_for_longitude(south_longitude),
        sign_degree=round(south_longitude % 30.0, 8),
        whole_sign_house=whole_sign_house(south_longitude, source.ascendant_longitude),
        motion_status=north.motion_status,
    ))
    return tuple(facts)


def _separation(left: float, right: float) -> float:
    raw = abs(left - right) % 360.0
    return min(raw, 360.0 - raw)


def derive_modern_point_aspects(
    source: ChartInput,
    point_facts: tuple[ModernPointFact, ...],
) -> tuple[AspectFact, ...]:
    """Aspect modern points to chart bodies under the explicit v0.2 orb table."""

    profile = integrated_classical_modern_profile()
    orbs = dict(profile.aspect_orbs)
    angles = INTEGRATED_ASPECT_ANGLES
    bodies = tuple((position.planet, position.longitude) for position in source.positions)
    points = tuple((point.point, point.longitude) for point in point_facts)
    pairs = [(point, body) for point in points for body in bodies] + list(combinations(points, 2))
    result: list[AspectFact] = []
    for (first_name, first_longitude), (second_name, second_longitude) in pairs:
        separation = _separation(first_longitude, second_longitude)
        candidates = sorted(
            (abs(separation - angle), name, angle)
            for name, angle in angles.items()
            if abs(separation - angle) <= orbs[name]
        )
        if candidates:
            orb, name, exact = candidates[0]
            result.append(AspectFact(first_name, second_name, name, exact, round(separation, 8), round(orb, 8), "NOT_DERIVED_FOR_POINT_OVERLAY"))
    return tuple(result)


def build_integrated_completion(
    source: ChartInput,
    modern_points: tuple[PlanetPosition, ...],
    *,
    chart_id: str,
) -> IntegratedAstrologyCompletion:
    """Compose the v0.2 chart, completed classical facts, and modern points."""

    base = build_chart(source, integrated_classical_modern_profile(), chart_id=chart_id)
    dignities = derive_extended_dignities(source)
    points = derive_modern_points(source, modern_points)
    aspects = derive_modern_point_aspects(source, points)
    payload = {"base": base, "dignities": dignities, "points": points, "aspects": aspects, "algorithm": ALGORITHM_VERSION}
    return IntegratedAstrologyCompletion(base, dignities, points, aspects, ALGORITHM_VERSION, derivation_hash(payload))


def validate_classical_completion_tables() -> bool:
    """Fail closed unless every sign has complete, gap-free classical tables."""

    if set(EGYPTIAN_BOUNDS) != set(SIGNS) or set(FACE_RULERS) != set(SIGNS):
        return False
    for sign in SIGNS:
        bounds = EGYPTIAN_BOUNDS[sign]
        if bounds[0][0] != 0 or bounds[-1][1] != 30:
            return False
        if any(left[1] != right[0] for left, right in zip(bounds, bounds[1:], strict=False)):
            return False
        if len(FACE_RULERS[sign]) != 3:
            return False
    return set(PLANETARY_JOYS) == set(TRADITIONAL_PLANETS)
