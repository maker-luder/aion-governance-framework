from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_classical_astrology import (
    MODERN_POINT_SET,
    ChartInput,
    PlanetPosition,
    build_integrated_completion,
    derive_extended_dignities,
    derive_modern_points,
    validate_classical_completion_tables,
)
from aion_astra_classical_astrology.completion import EGYPTIAN_BOUNDS, FACE_RULERS
from aion_astra_classical_astrology.errors import ValidationError
from aion_astra_classical_astrology.fixtures import synthetic_reference_input


def integrated_source(*, day: bool = True) -> ChartInput:
    base = synthetic_reference_input()
    return replace(
        base,
        input_id="SYNTHETIC_INTEGRATED_COMPLETION_001",
        is_day_chart=day,
        positions=base.positions + (
            PlanetPosition("URANUS", 130.0, 0.01),
            PlanetPosition("NEPTUNE", 220.0, -0.01),
            PlanetPosition("PLUTO", 310.0, 0.0),
        ),
    )


def test_completion_tables_are_total_and_gap_free() -> None:
    assert validate_classical_completion_tables()
    assert all(sum(end - start for start, end, _ in EGYPTIAN_BOUNDS[sign]) == 30 for sign in EGYPTIAN_BOUNDS)
    assert all(len(rulers) == 3 for rulers in FACE_RULERS.values())


def test_egyptian_bound_boundaries_are_half_open() -> None:
    source = integrated_source()
    positions = tuple(
        PlanetPosition(p.planet, 5.999999 if p.planet == "SUN" else p.longitude, p.speed_longitude)
        for p in source.positions
    )
    before = derive_extended_dignities(replace(source, positions=positions))[0]
    positions = tuple(
        PlanetPosition(p.planet, 6.0 if p.planet == "SUN" else p.longitude, p.speed_longitude)
        for p in source.positions
    )
    after = derive_extended_dignities(replace(source, positions=positions))[0]
    assert before.egyptian_bound_ruler == "JUPITER"
    assert after.egyptian_bound_ruler == "VENUS"


def test_triplicity_ruler_changes_by_sect_without_changing_element() -> None:
    day = derive_extended_dignities(integrated_source(day=True))[0]
    night = derive_extended_dignities(integrated_source(day=False))[0]
    assert day.triplicity_element == night.triplicity_element == "FIRE"
    assert day.sect_triplicity_ruler == "SUN"
    assert night.sect_triplicity_ruler == "JUPITER"
    assert day.participating_triplicity_ruler == night.participating_triplicity_ruler == "SATURN"


def test_chaldean_faces_cover_each_ten_degree_segment() -> None:
    source = integrated_source()
    observed = []
    for longitude in (0.0, 10.0, 20.0):
        positions = tuple(
            PlanetPosition(p.planet, longitude if p.planet == "SUN" else p.longitude, p.speed_longitude)
            for p in source.positions
        )
        observed.append(derive_extended_dignities(replace(source, positions=positions))[0].chaldean_face_ruler)
    assert observed == ["MARS", "SUN", "VENUS"]


def test_planetary_joy_is_a_house_fact_not_an_interpretation() -> None:
    facts = {fact.planet: fact for fact in derive_extended_dignities(integrated_source())}
    assert facts["MERCURY"].planetary_joy_house == 1
    assert isinstance(facts["MERCURY"].is_in_planetary_joy, bool)
    assert all(fact.rule_profile.endswith("_V1") for fact in facts.values())


def test_modern_points_are_not_promoted_to_planets_or_rulers() -> None:
    facts = derive_modern_points(
        integrated_source(),
        (PlanetPosition("TRUE_NORTH_NODE", 42.0, -0.0529), PlanetPosition("CHIRON", 252.0, 0.02)),
    )
    assert [fact.point for fact in facts] == ["TRUE_NORTH_NODE", "CHIRON", "TRUE_SOUTH_NODE"]
    assert facts[2].longitude == 222.0
    assert all(fact.classical_dignity_status == "NOT_APPLICABLE" for fact in facts)
    assert all(fact.rulership_status == "NO_RULERSHIP_ASSIGNED" for fact in facts)


def test_modern_point_input_is_versioned_and_ordered() -> None:
    with pytest.raises(ValidationError, match="ordered exactly"):
        derive_modern_points(
            integrated_source(),
            (PlanetPosition("CHIRON", 252.0), PlanetPosition("TRUE_NORTH_NODE", 42.0)),
        )
    assert MODERN_POINT_SET == ("TRUE_NORTH_NODE", "CHIRON")


def test_integrated_completion_preserves_nonclaim_and_no_effect_boundaries() -> None:
    result = build_integrated_completion(
        integrated_source(),
        (PlanetPosition("TRUE_NORTH_NODE", 42.0, -0.0529), PlanetPosition("CHIRON", 252.0, 0.02)),
        chart_id="SYNTHETIC_COMPLETION_CHART_001",
    )
    assert len(result.extended_dignities) == 7
    assert len(result.modern_points) == 3
    assert result.derivation_hash == build_integrated_completion(
        integrated_source(),
        (PlanetPosition("TRUE_NORTH_NODE", 42.0, -0.0529), PlanetPosition("CHIRON", 252.0, 0.02)),
        chart_id="SYNTHETIC_COMPLETION_CHART_001",
    ).derivation_hash
    assert result.interpretation_status == "NOT_PERFORMED"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.consciousness_conclusion == "NOT_ESTABLISHED"
    assert result.canonical_effect == "NONE"
    assert result.deployment is False
    assert result.action_authority == "NONE"
