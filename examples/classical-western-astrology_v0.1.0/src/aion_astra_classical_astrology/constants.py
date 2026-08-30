"""Explicit v0.1.0 classical rule tables."""

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
