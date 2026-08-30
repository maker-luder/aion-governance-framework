"""Versioned classical core and additive modern-overlay rule tables."""

SIGNS = (
    "ARIES",
    "TAURUS",
    "GEMINI",
    "CANCER",
    "LEO",
    "VIRGO",
    "LIBRA",
    "SCORPIO",
    "SAGITTARIUS",
    "CAPRICORN",
    "AQUARIUS",
    "PISCES",
)

TRADITIONAL_PLANETS = (
    "SUN",
    "MOON",
    "MERCURY",
    "VENUS",
    "MARS",
    "JUPITER",
    "SATURN",
)

MODERN_OUTER_PLANETS = ("URANUS", "NEPTUNE", "PLUTO")
INTEGRATED_PLANETS = TRADITIONAL_PLANETS + MODERN_OUTER_PLANETS

DOMICILE_RULERS = {
    "ARIES": "MARS",
    "TAURUS": "VENUS",
    "GEMINI": "MERCURY",
    "CANCER": "MOON",
    "LEO": "SUN",
    "VIRGO": "MERCURY",
    "LIBRA": "VENUS",
    "SCORPIO": "MARS",
    "SAGITTARIUS": "JUPITER",
    "CAPRICORN": "SATURN",
    "AQUARIUS": "SATURN",
    "PISCES": "JUPITER",
}

# The modern layer is deliberately additive: it never overwrites the
# traditional domicile ruler used by the classical dignity calculation.
MODERN_RULERS = {
    **DOMICILE_RULERS,
    "SCORPIO": "PLUTO",
    "AQUARIUS": "URANUS",
    "PISCES": "NEPTUNE",
}

SIGN_ELEMENTS = dict(zip(SIGNS, (
    "FIRE", "EARTH", "AIR", "WATER", "FIRE", "EARTH",
    "AIR", "WATER", "FIRE", "EARTH", "AIR", "WATER",
), strict=True))
SIGN_MODALITIES = dict(zip(SIGNS, (
    "CARDINAL", "FIXED", "MUTABLE", "CARDINAL", "FIXED", "MUTABLE",
    "CARDINAL", "FIXED", "MUTABLE", "CARDINAL", "FIXED", "MUTABLE",
), strict=True))
SIGN_POLARITIES = {
    sign: ("POSITIVE" if index % 2 == 0 else "NEGATIVE")
    for index, sign in enumerate(SIGNS)
}

EXALTATION_SIGNS = {
    "SUN": "ARIES",
    "MOON": "TAURUS",
    "MERCURY": "VIRGO",
    "VENUS": "PISCES",
    "MARS": "CAPRICORN",
    "JUPITER": "CANCER",
    "SATURN": "LIBRA",
}

OPPOSITE_SIGN = {sign: SIGNS[(index + 6) % 12] for index, sign in enumerate(SIGNS)}

ASPECT_ANGLES = {
    "CONJUNCTION": 0.0,
    "SEXTILE": 60.0,
    "SQUARE": 90.0,
    "TRINE": 120.0,
    "OPPOSITION": 180.0,
}

MODERN_MINOR_ASPECT_ANGLES = {
    "SEMISEXTILE": 30.0,
    "SEMISQUARE": 45.0,
    "QUINTILE": 72.0,
    "SESQUISQUARE": 135.0,
    "BIQUINTILE": 144.0,
    "QUINCUNX": 150.0,
}
INTEGRATED_ASPECT_ANGLES = {**ASPECT_ANGLES, **MODERN_MINOR_ASPECT_ANGLES}
