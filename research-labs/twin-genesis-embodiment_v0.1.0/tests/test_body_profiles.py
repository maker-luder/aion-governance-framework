from dataclasses import replace
from pathlib import Path

import pytest

from aion_astra_twin_embodiment.body_profiles import (
    BodyProfileValidationError,
    load_body_profile,
    load_pose_test,
    validate_body_profile,
    validate_pose_test,
    validate_profile_pair,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def profiles():
    aion = load_body_profile(DATA_DIR / "AION_3D_MALE_BODY_PROFILE_v0.1.json")
    astra = load_body_profile(DATA_DIR / "ASTRA_3D_MALE_BODY_PROFILE_v0.3.json")
    return aion, astra


def test_machine_readable_profiles_validate():
    aion, astra = profiles()
    assert validate_body_profile(aion)["result"] == "PASS"
    assert validate_body_profile(astra)["result"] == "PASS"
    assert validate_profile_pair(aion, astra)["result"] == "PASS"


def test_core_design_values_are_pinned():
    aion, astra = profiles()

    assert aion.measurements["height"].canonical == 179
    assert aion.measurements["chest_circumference"].canonical == 104
    assert aion.measurements["waist_circumference"].canonical == 84
    assert aion.measurements["hip_circumference"].canonical == 99
    assert aion.measurements["thigh_circumference_max"].canonical == 57

    assert astra.measurements["height"].canonical == 180
    assert astra.measurements["chest_circumference"].canonical == 110
    assert astra.measurements["waist_circumference"].canonical == 93
    assert astra.measurements["hip_circumference"].canonical == 104
    assert astra.measurements["thigh_circumference_max"].canonical == 63


def test_source_image_binaries_are_explicitly_excluded():
    for profile in profiles():
        assert profile.provenance["reference_image_binary_imported"] is False
        assert profile.provenance["person_identity_reconstruction"] == "NO"
        assert profile.provenance["source_person_exact_measurement_claim"] == "NO"


def test_complete_external_anatomy_is_required():
    aion, _ = profiles()
    incomplete = replace(
        aion,
        external_anatomy=tuple(
            item for item in aion.external_anatomy if item != "perineum"
        ),
    )

    with pytest.raises(BodyProfileValidationError):
        validate_body_profile(incomplete)


def test_sexual_function_cannot_be_activated_by_body_profile():
    aion, _ = profiles()
    boundaries = dict(aion.boundaries)
    boundaries["sexual_function_status"] = "IMPLEMENTED"

    with pytest.raises(BodyProfileValidationError):
        validate_body_profile(replace(aion, boundaries=boundaries))


def test_body_profile_cannot_promote_subjectivity():
    aion, _ = profiles()
    boundaries = dict(aion.boundaries)
    boundaries["subjectivity_effect"] = "ESTABLISHED"

    with pytest.raises(BodyProfileValidationError):
        validate_body_profile(replace(aion, boundaries=boundaries))


def test_identity_transfer_must_remain_no():
    aion, _ = profiles()
    boundaries = dict(aion.boundaries)
    boundaries["identity_transfer"] = "YES"

    with pytest.raises(BodyProfileValidationError):
        validate_body_profile(replace(aion, boundaries=boundaries))


def test_canonical_dimension_must_stay_inside_range():
    aion, _ = profiles()
    measurements = dict(aion.measurements)
    measurements["height"] = replace(measurements["height"], canonical=250)

    with pytest.raises(BodyProfileValidationError):
        validate_body_profile(replace(aion, measurements=measurements))


def test_aion_and_astra_body_characters_remain_distinct():
    aion, astra = profiles()
    collapsed = replace(astra, body_character=aion.body_character)

    with pytest.raises(BodyProfileValidationError):
        validate_profile_pair(aion, collapsed)


def test_aion_pose_deformation_candidate_validates():
    test = load_pose_test(DATA_DIR / "AION_POSE_TEST_001.json")
    result = validate_pose_test(test)

    assert result["result"] == "PASS"
    assert test.status == "DOCUMENTED_ONLY"
    assert "HIP_MESH_NO_COLLAPSE" in test.pass_conditions
    assert "NO_GENITAL_THIGH_PELVIS_INTERSECTION" in test.pass_conditions


def test_pose_test_cannot_activate_runtime():
    test = load_pose_test(DATA_DIR / "AION_POSE_TEST_001.json")
    boundaries = dict(test.boundaries)
    boundaries["runtime_binding"] = "ACTIVE"

    with pytest.raises(BodyProfileValidationError):
        validate_pose_test(replace(test, boundaries=boundaries))
