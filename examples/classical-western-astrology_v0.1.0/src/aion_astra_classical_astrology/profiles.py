"""Versioned classical rule profiles."""

from .constants import ASPECT_ANGLES, TRADITIONAL_PLANETS
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
