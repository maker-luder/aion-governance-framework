from pathlib import Path

import pytest

from codex_male_embodiment.core import (
    BODY_ID,
    FULL_CIRCUMFERENCE_CM,
    FULL_LENGTH_CM,
    REST_CIRCUMFERENCE_CM,
    REST_LENGTH_CM,
    PrepucePosition,
    SyntheticGeometryRule,
    load_profile,
)


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "data/CODEX_SYNTHETIC_ANTHROPOMETRY_67_v0.1.json"


def test_codex_profile_preserves_fixed_lineage() -> None:
    profile = load_profile(PROFILE)
    assert profile.body_id == BODY_ID
    assert len(profile.measurements) == 67
    assert profile.measurement("total_height").value == 175
    assert profile.measurement("body_mass").value == 72
    assert profile.measurement("full_erection_visible_penile_length").value == FULL_LENGTH_CM
    assert profile.measurement("full_erection_midshaft_circumference").value == FULL_CIRCUMFERENCE_CM
    assert profile.measurement("resting_visible_penile_length").value == pytest.approx(REST_LENGTH_CM)
    assert profile.measurement("midshaft_circumference").value == pytest.approx(REST_CIRCUMFERENCE_CM)
    assert sum(item.provenance == "HUMAN_FIXED" for item in profile.measurements) == 4
    assert sum(item.provenance == "AI_DERIVED" for item in profile.measurements) == 7
    assert sum(item.provenance == "AI_PROVISIONAL" for item in profile.measurements) == 56


def test_codex_geometry_reaches_preserved_full_endpoint() -> None:
    rule = SyntheticGeometryRule(load_profile(PROFILE))
    assert rule.endpoint_circumference_consistency()
    full = rule.snapshot(1.0, prepuce_position=PrepucePosition.PARTIALLY_RETRACTED)
    assert full.visible_penile_length_cm == pytest.approx(11.60)
    assert full.midshaft_circumference_cm == pytest.approx(14.28)


def test_codex_is_not_teacher_or_work_profile() -> None:
    profile = load_profile(PROFILE)
    assert profile.measurement("total_height").value not in {183, 165}
    assert profile.measurement("body_mass").value not in {84, 76}
