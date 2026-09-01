"""Bounded classical Western astrology fact derivation."""

from .engine import build_chart, derive_aspects, derive_planet_facts
from .completion import (
    EGYPTIAN_BOUNDS,
    FACE_RULERS,
    MODERN_POINT_SET,
    PLANETARY_JOYS,
    TRIPLICITY_RULERS,
    ExtendedDignityFact,
    IntegratedAstrologyCompletion,
    ModernPointFact,
    build_integrated_completion,
    derive_extended_dignities,
    derive_modern_point_aspects,
    derive_modern_points,
    validate_classical_completion_tables,
)
from .fixtures import synthetic_reference_input
from .models import (
    AspectFact,
    ChartInput,
    ClassicalChart,
    ClassicalRuleProfile,
    PlanetFact,
    PlanetPosition,
)
from .profiles import hellenistic_medieval_profile, integrated_classical_modern_profile

__all__ = [
    "AspectFact",
    "EGYPTIAN_BOUNDS",
    "ExtendedDignityFact",
    "FACE_RULERS",
    "IntegratedAstrologyCompletion",
    "MODERN_POINT_SET",
    "ModernPointFact",
    "PLANETARY_JOYS",
    "TRIPLICITY_RULERS",
    "ChartInput",
    "ClassicalChart",
    "ClassicalRuleProfile",
    "PlanetFact",
    "PlanetPosition",
    "build_chart",
    "build_integrated_completion",
    "derive_aspects",
    "derive_planet_facts",
    "derive_extended_dignities",
    "derive_modern_point_aspects",
    "derive_modern_points",
    "hellenistic_medieval_profile",
    "integrated_classical_modern_profile",
    "synthetic_reference_input",
    "validate_classical_completion_tables",
]
