"""Versioned classical rule profiles."""

from .constants import (
    ASPECT_ANGLES,
    INTEGRATED_ASPECT_ANGLES,
    INTEGRATED_PLANETS,
    TRADITIONAL_PLANETS,
)
from .models import ClassicalRuleProfile


def hellenistic_medieval_profile() -> ClassicalRuleProfile:
    """Return the narrow v0.1.0 Hellenistic/medieval common-core profile."""

    return ClassicalRuleProfile(
        profile_id="CLASSICAL_HELLENISTIC_MEDIEVAL_COMMON_V1",
        version="0.1.0",
        tradition_scope="HELLENISTIC_MEDIEVAL_COMMON_CORE",
        zodiac="TROPICAL",
        house_system="WHOLE_SIGN",
        planet_set=TRADITIONAL_PLANETS,
        aspect_angles=tuple(ASPECT_ANGLES.items()),
        aspect_orbs=(
            ("CONJUNCTION", 8.0),
            ("SEXTILE", 6.0),
            ("SQUARE", 7.0),
            ("TRINE", 7.0),
            ("OPPOSITION", 8.0),
        ),
        dignity_scheme="TRADITIONAL_SIGN_BASED_DOMICILE_EXALTATION_DETRIMENT_FALL",
        sect_rule="SOURCE_DECLARED_ABOVE_BELOW_HORIZON",
        source_references=(
            "PTOLEMY_TETRABIBLOS_BOOK_I",
            "DOROTHEUS_CARMEN_ASTROLOGICUM",
            "VALENS_ANTHOLOGY",
        ),
    )


def integrated_classical_modern_profile() -> ClassicalRuleProfile:
    """Return a classical-primary profile with a separately labelled modern overlay."""

    return ClassicalRuleProfile(
        profile_id="CLASSICAL_PRIMARY_MODERN_OVERLAY_V2",
        version="0.2.0",
        tradition_scope="CLASSICAL_PRIMARY_WITH_MODERN_OVERLAY",
        zodiac="TROPICAL",
        house_system="WHOLE_SIGN",
        planet_set=INTEGRATED_PLANETS,
        aspect_angles=tuple(INTEGRATED_ASPECT_ANGLES.items()),
        aspect_orbs=(
            ("CONJUNCTION", 8.0), ("SEXTILE", 6.0), ("SQUARE", 7.0),
            ("TRINE", 7.0), ("OPPOSITION", 8.0),
            ("SEMISEXTILE", 2.0), ("SEMISQUARE", 2.0), ("QUINTILE", 2.0),
            ("SESQUISQUARE", 2.0), ("BIQUINTILE", 2.0), ("QUINCUNX", 3.0),
        ),
        dignity_scheme="TRADITIONAL_SIGN_BASED_DOMICILE_EXALTATION_DETRIMENT_FALL",
        sect_rule="SOURCE_DECLARED_ABOVE_BELOW_HORIZON_TRADITIONAL_PLANETS_ONLY",
        source_references=(
            "PTOLEMY_TETRABIBLOS_BOOK_I",
            "SEPHARIAL_ASTROLOGY_1920_PUBLIC_DOMAIN",
            "ASTRODIENST_MODERN_RULERS_AND_ASPECTS",
        ),
    )
