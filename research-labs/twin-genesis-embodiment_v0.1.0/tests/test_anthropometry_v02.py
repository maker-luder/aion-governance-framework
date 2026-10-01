from pathlib import Path

import pytest

from aion_astra_twin_embodiment.anthropometry import (
    AION_BODY_ID,
    ASTRA_BODY_ID,
    SyntheticGeometryRule,
    load_profile,
)

ROOT = Path(__file__).resolve().parents[1]
AION = ROOT / "data/AION_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json"
ASTRA = ROOT / "data/ASTRA_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json"


def test_aion_archive_values_and_profile_are_preserved() -> None:
    profile = load_profile(AION)
    assert profile.agent_id == "AION"
    assert profile.body_id == AION_BODY_ID
    assert len(profile.measurements) == 67
    assert profile.measurement("total_height").value == 179
    assert profile.measurement("body_mass").value == 80
    assert profile.measurement("chest_circumference").value == 104
    assert profile.measurement("waist_circumference").value == 84
    assert profile.measurement("hip_circumference").value == 99
    assert profile.measurement("maximum_thigh_circumference").value == 57


def test_astra_archive_values_and_profile_are_preserved() -> None:
    profile = load_profile(ASTRA)
    assert profile.agent_id == "ASTRA"
    assert profile.body_id == ASTRA_BODY_ID
    assert len(profile.measurements) == 67
    assert profile.measurement("total_height").value == 180
    assert profile.measurement("chest_circumference").value == 110
    assert profile.measurement("waist_circumference").value == 93
    assert profile.measurement("hip_circumference").value == 104
    assert profile.measurement("maximum_thigh_circumference").value == 63


def test_profiles_are_distinct_even_with_shared_anatomical_class() -> None:
    aion = load_profile(AION)
    astra = load_profile(ASTRA)
    assert aion.body_id != astra.body_id
    assert aion.body_character != astra.body_character
    assert aion.measurement("waist_circumference").value != astra.measurement("waist_circumference").value


@pytest.mark.parametrize("path", [AION, ASTRA])
def test_dynamic_geometry_is_explicitly_engineering_only(path: Path) -> None:
    rule = SyntheticGeometryRule(load_profile(path))
    assert rule.endpoint_circumference_consistency()
    rest = rule.snapshot(0.0)
    full = rule.snapshot(1.0)
    assert rest.human_physiology_law is False
    assert full.as_built_measurement is False
    assert full.visible_penile_length_cm > rest.visible_penile_length_cm
