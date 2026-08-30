from __future__ import annotations

from dataclasses import replace

from aion_astra_classical_astrology.constants import (
    DOMICILE_RULERS,
    INTEGRATED_ASPECT_ANGLES,
    INTEGRATED_PLANETS,
)
from aion_astra_classical_astrology.engine import build_chart, derive_aspects, derive_planet_facts
from aion_astra_classical_astrology.models import PlanetPosition
from aion_astra_classical_astrology.profiles import integrated_classical_modern_profile


def integrated_input(synthetic_input):
    traditional = tuple(
        replace(position, speed_longitude=1.0 if position.planet != "SATURN" else -0.05)
        for position in synthetic_input.positions
    )
    return replace(
        synthetic_input,
        input_id="SYNTHETIC_INTEGRATED_CHART_001",
        positions=traditional + (
            PlanetPosition("URANUS", 315.0, -0.03),
            PlanetPosition("NEPTUNE", 345.0, 0.01),
            PlanetPosition("PLUTO", 225.0, 0.0),
        ),
    )


def test_integrated_profile_is_classical_primary_and_additive() -> None:
    profile = integrated_classical_modern_profile()
    assert profile.tradition_scope == "CLASSICAL_PRIMARY_WITH_MODERN_OVERLAY"
    assert profile.planet_set == INTEGRATED_PLANETS
    assert dict(profile.aspect_angles) == INTEGRATED_ASPECT_ANGLES


def test_integrated_planets_preserve_traditional_rulers(synthetic_input) -> None:
    facts = derive_planet_facts(integrated_input(synthetic_input), integrated_classical_modern_profile())
    aquarius = next(fact for fact in facts if fact.planet == "URANUS")
    assert aquarius.domicile_ruler == DOMICILE_RULERS["AQUARIUS"] == "SATURN"
    assert aquarius.modern_ruler == "URANUS"


def test_outer_planets_do_not_acquire_classical_dignity_or_sect(synthetic_input) -> None:
    facts = derive_planet_facts(integrated_input(synthetic_input), integrated_classical_modern_profile())
    outer = [fact for fact in facts if fact.planet in {"URANUS", "NEPTUNE", "PLUTO"}]
    assert all(fact.essential_dignities == ("NOT_APPLICABLE_TO_CLASSICAL_DIGNITY",) for fact in outer)
    assert all(fact.sect_status == "NOT_APPLICABLE_TO_CLASSICAL_SECT" for fact in outer)


def test_sign_element_modality_and_polarity_are_materialized(synthetic_input) -> None:
    sun = derive_planet_facts(integrated_input(synthetic_input), integrated_classical_modern_profile())[0]
    assert (sun.sign, sun.element, sun.modality, sun.polarity) == (
        "ARIES", "FIRE", "CARDINAL", "POSITIVE"
    )


def test_motion_status_is_separate_from_symbolic_rules(synthetic_input) -> None:
    facts = {fact.planet: fact for fact in derive_planet_facts(
        integrated_input(synthetic_input), integrated_classical_modern_profile()
    )}
    assert facts["SATURN"].motion_status == "RETROGRADE"
    assert facts["SUN"].motion_status == "DIRECT"
    assert facts["PLUTO"].motion_status == "STATIONARY"


def test_minor_aspects_are_labelled_by_versioned_overlay(synthetic_input) -> None:
    aspects = derive_aspects(integrated_input(synthetic_input), integrated_classical_modern_profile())
    assert any(fact.aspect in {"SEMISEXTILE", "SEMISQUARE", "QUINCUNX"} for fact in aspects)


def test_aspect_phase_uses_speed_vectors(synthetic_input) -> None:
    aspects = derive_aspects(integrated_input(synthetic_input), integrated_classical_modern_profile())
    assert aspects
    assert all(fact.phase != "NOT_DERIVED_WITHOUT_SPEED_VECTORS" for fact in aspects)


def test_integrated_chart_keeps_no_effect_boundary(synthetic_input) -> None:
    chart = build_chart(
        integrated_input(synthetic_input), integrated_classical_modern_profile(), chart_id="INTEGRATED_1"
    )
    assert len(chart.planets) == 10
    assert chart.interpretation_status == "NOT_PERFORMED"
    assert chart.canonical_effect == "NONE"
    assert chart.deployment is False

