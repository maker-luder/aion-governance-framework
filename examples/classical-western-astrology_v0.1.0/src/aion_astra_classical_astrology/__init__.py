"""Bounded classical Western astrology fact derivation."""

from .engine import build_chart, derive_aspects, derive_planet_facts
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
    "ChartInput",
    "ClassicalChart",
    "ClassicalRuleProfile",
    "PlanetFact",
    "PlanetPosition",
    "build_chart",
    "derive_aspects",
    "derive_planet_facts",
    "hellenistic_medieval_profile",
    "integrated_classical_modern_profile",
    "synthetic_reference_input",
]
