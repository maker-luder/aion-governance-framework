from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_classical_astrology.constants import SIGNS, TRADITIONAL_PLANETS
from aion_astra_classical_astrology.engine import (
    build_chart,
    derive_aspects,
    derive_planet_facts,
    sign_for_longitude,
    whole_sign_house,
)
from aion_astra_classical_astrology.errors import ValidationError
from aion_astra_classical_astrology.fixtures import synthetic_reference_input
from aion_astra_classical_astrology.models import PlanetPosition
from aion_astra_classical_astrology.profiles import hellenistic_medieval_profile


def test_profile_is_classical_primary() -> None:
    profile = hellenistic_medieval_profile()
    assert profile.tradition_scope == "HELLENISTIC_MEDIEVAL_COMMON_CORE"
    assert profile.zodiac == "TROPICAL"
    assert profile.house_system == "WHOLE_SIGN"
    assert profile.planet_set == TRADITIONAL_PLANETS


def test_public_synthetic_reference_builds_same_chart(synthetic_input) -> None:
    assert synthetic_reference_input() == synthetic_input
    chart = build_chart(
        synthetic_reference_input(),
        hellenistic_medieval_profile(),
        chart_id="C1",
    )
    assert chart.input_id == "SYNTHETIC_CLASSICAL_CHART_001"


def test_twelve_tropical_signs() -> None:
    assert len(SIGNS) == 12
    assert sign_for_longitude(0.0) == "ARIES"
    assert sign_for_longitude(359.999) == "PISCES"


def test_whole_sign_houses_wrap() -> None:
    assert whole_sign_house(15.0, 15.0) == 1
    assert whole_sign_house(345.0, 15.0) == 12
    assert whole_sign_house(195.0, 15.0) == 7


def test_planet_facts_cover_traditional_seven(synthetic_input) -> None:
    facts = derive_planet_facts(synthetic_input, hellenistic_medieval_profile())
    assert tuple(fact.planet for fact in facts) == TRADITIONAL_PLANETS


def test_major_sign_dignities(synthetic_input) -> None:
    facts = {fact.planet: fact for fact in derive_planet_facts(synthetic_input, hellenistic_medieval_profile())}
    assert "EXALTATION" in facts["SUN"].essential_dignities
    assert "EXALTATION" in facts["MOON"].essential_dignities
    assert "DOMICILE" in facts["JUPITER"].essential_dignities
    assert "DOMICILE" in facts["SATURN"].essential_dignities


def test_detriment_and_fall() -> None:
    from aion_astra_classical_astrology.models import ChartInput

    profile = hellenistic_medieval_profile()
    source = ChartInput(
        "SYNTHETIC_S",
        "2000-01-01T12:00:00Z",
        "SYNTHETIC_LOCATION",
        0,
        0,
        0,
        0,
        True,
        (
            PlanetPosition("SUN", 310),
            PlanetPosition("MOON", 220),
            PlanetPosition("MERCURY", 250),
            PlanetPosition("VENUS", 160),
            PlanetPosition("MARS", 100),
            PlanetPosition("JUPITER", 280),
            PlanetPosition("SATURN", 10),
        ),
        "SYNTHETIC",
        "1",
        "GEOCENTRIC_TROPICAL_ECLIPTIC_OF_DATE",
        True,
    )
    facts = {fact.planet: fact for fact in derive_planet_facts(source, profile)}
    assert "DETRIMENT" in facts["SUN"].essential_dignities
    assert "FALL" in facts["MOON"].essential_dignities
    assert "FALL" in facts["MARS"].essential_dignities
    assert "FALL" in facts["SATURN"].essential_dignities


def test_sect_is_explicit_and_mercury_is_not_guessed(synthetic_input) -> None:
    facts = {fact.planet: fact for fact in derive_planet_facts(synthetic_input, hellenistic_medieval_profile())}
    assert facts["SUN"].sect_status == "OF_SECT"
    assert facts["MARS"].sect_status == "CONTRARY_TO_SECT"
    assert facts["MERCURY"].sect_status == "VARIABLE_NOT_DERIVED_WITHOUT_SOLAR_PHASE"


def test_five_classical_aspects_only(synthetic_input) -> None:
    profile = hellenistic_medieval_profile()
    assert dict(profile.aspect_angles) == {
        "CONJUNCTION": 0.0,
        "SEXTILE": 60.0,
        "SQUARE": 90.0,
        "TRINE": 120.0,
        "OPPOSITION": 180.0,
    }
    assert {fact.aspect for fact in derive_aspects(synthetic_input, profile)} <= set(dict(profile.aspect_angles))


def test_aspect_phase_is_not_invented_without_speed(synthetic_input) -> None:
    aspects = derive_aspects(synthetic_input, hellenistic_medieval_profile())
    assert aspects
    assert all(fact.phase == "NOT_DERIVED_WITHOUT_SPEED_VECTORS" for fact in aspects)


def test_chart_is_deterministic(synthetic_input) -> None:
    profile = hellenistic_medieval_profile()
    first = build_chart(synthetic_input, profile, chart_id="C1")
    second = build_chart(synthetic_input, profile, chart_id="C1")
    assert first == second
    assert len(first.derivation_hash) == 64


def test_ephemeris_provenance_is_preserved(synthetic_input) -> None:
    chart = build_chart(synthetic_input, hellenistic_medieval_profile(), chart_id="C1")
    assert chart.ephemeris_source == "SYNTHETIC_GOLDEN_VECTOR"
    assert chart.ephemeris_version == "SYNTHETIC-1"
    assert chart.derivation_trace[0]["operation"] == "VALIDATE_VERSIONED_EPHEMERIS_INPUT"


def test_interpretation_and_authority_boundaries(synthetic_input) -> None:
    chart = build_chart(synthetic_input, hellenistic_medieval_profile(), chart_id="C1")
    assert chart.interpretation_status == "NOT_PERFORMED"
    assert chart.canonical_effect == "NONE"
    assert chart.deployment is False
    assert chart.action_authority == "NONE"


def test_real_person_fixture_is_rejected(synthetic_input) -> None:
    with pytest.raises(ValidationError, match="synthetic fixtures only"):
        build_chart(
            replace(synthetic_input, synthetic_fixture=False),
            hellenistic_medieval_profile(),
            chart_id="C1",
        )


def test_non_synthetic_labels_are_rejected(synthetic_input) -> None:
    with pytest.raises(ValidationError, match="synthetic input and location labels"):
        build_chart(
            replace(synthetic_input, location_label="REAL_LOCATION"),
            hellenistic_medieval_profile(),
            chart_id="C1",
        )


def test_non_utc_timestamp_is_rejected(synthetic_input) -> None:
    with pytest.raises(ValidationError, match="explicit UTC"):
        build_chart(
            replace(synthetic_input, event_datetime_utc="2000-01-01T12:00:00+08:00"),
            hellenistic_medieval_profile(),
            chart_id="C1",
        )


def test_missing_ephemeris_provenance_is_rejected(synthetic_input) -> None:
    with pytest.raises(ValidationError, match="ephemeris source"):
        build_chart(
            replace(synthetic_input, ephemeris_version=""),
            hellenistic_medieval_profile(),
            chart_id="C1",
        )


def test_outer_planet_is_rejected(synthetic_input) -> None:
    positions = synthetic_input.positions[:-1] + (PlanetPosition("URANUS", 310.0),)
    with pytest.raises(ValidationError, match="exactly the profile planet set"):
        build_chart(
            replace(synthetic_input, positions=positions),
            hellenistic_medieval_profile(),
            chart_id="C1",
        )


def test_profile_cannot_replace_traditional_planet_set(synthetic_input) -> None:
    profile = replace(
        hellenistic_medieval_profile(),
        planet_set=TRADITIONAL_PLANETS[:-1] + ("URANUS",),
    )
    with pytest.raises(ValidationError, match="traditional seven planets"):
        build_chart(synthetic_input, profile, chart_id="C1")


def test_profile_cannot_add_modern_aspects(synthetic_input) -> None:
    profile = replace(
        hellenistic_medieval_profile(),
        aspect_angles=hellenistic_medieval_profile().aspect_angles + (("QUINCUNX", 150.0),),
    )
    with pytest.raises(ValidationError, match="five classical aspects"):
        build_chart(synthetic_input, profile, chart_id="C1")


def test_duplicate_planet_is_rejected(synthetic_input) -> None:
    positions = synthetic_input.positions[:-1] + (PlanetPosition("SUN", 310.0),)
    with pytest.raises(ValidationError, match="exactly once"):
        build_chart(
            replace(synthetic_input, positions=positions),
            hellenistic_medieval_profile(),
            chart_id="C1",
        )


@pytest.mark.parametrize("longitude", [-0.01, 360.0, 999.0])
def test_invalid_ecliptic_longitude_fails_closed(synthetic_input, longitude: float) -> None:
    positions = (PlanetPosition("SUN", longitude),) + synthetic_input.positions[1:]
    with pytest.raises(ValidationError, match="longitude"):
        build_chart(
            replace(synthetic_input, positions=positions),
            hellenistic_medieval_profile(),
            chart_id="C1",
        )


def test_unsupported_coordinate_frame_fails_closed(synthetic_input) -> None:
    with pytest.raises(ValidationError, match="coordinate frame"):
        build_chart(
            replace(synthetic_input, coordinate_frame="SIDEREAL"),
            hellenistic_medieval_profile(),
            chart_id="C1",
        )


def test_empty_chart_id_fails_closed(synthetic_input) -> None:
    with pytest.raises(ValidationError, match="chart_id"):
        build_chart(synthetic_input, hellenistic_medieval_profile(), chart_id="")
