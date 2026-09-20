from __future__ import annotations

from aion_astra_twin_embodiment.teacher_anthropometry import (
    EXPECTED_MEASUREMENT_COUNT,
    build_teacher_anthropometry_profile,
    validate_teacher_anthropometry_profile,
)


def test_teacher_anthropometry_has_all_62_machine_readable_measurements() -> None:
    profile = build_teacher_anthropometry_profile()
    result = validate_teacher_anthropometry_profile(profile)
    measurements = profile.measurement_map()

    assert result["result"] == "PASS"
    assert result["measurement_count"] == str(EXPECTED_MEASUREMENT_COUNT)
    assert len(profile.measurements) == 62
    assert measurements["total_height"].nominal == 183.0
    assert measurements["body_mass"].unit == "kg"
    assert measurements["chest_frontal_width"].minimum == 39.5
    assert measurements["chest_frontal_width"].maximum == 40.5
    assert measurements["interpupillary_distance"].nominal == 6.4
    assert measurements["resting_visible_penile_length"].nominal == 9.5
    assert measurements["midshaft_diameter"].nominal == 3.2
    assert measurements["testicular_modeled_long_axis"].nominal == 4.5
    assert measurements["external_perineal_length"].nominal == 6.0


def test_teacher_anthropometry_is_synthetic_not_real_person_biometric() -> None:
    profile = build_teacher_anthropometry_profile()

    assert profile.real_person_biometric_source == "NONE"
    assert profile.person_reconstruction == "NO"
    assert profile.canonical_effect == "NONE"
    assert profile.deployment is False
