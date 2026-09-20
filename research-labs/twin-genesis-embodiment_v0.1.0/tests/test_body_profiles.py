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
    aion = load_body_profile(DATA_DIR / "AION_3D_FULL_BODY_HUMANLIKE_MALE_FORM_HUMANOID_ROBOT_MODEL_v0.3.json")
    astra = load_body_profile(DATA_DIR / "ASTRA_3D_FULL_BODY_HUMANLIKE_MALE_FORM_HUMANOID_ROBOT_MODEL_v0.5.json")
    return aion, astra


def test_machine_readable_robotic_profiles_validate():
    aion, astra = profiles()
    assert validate_body_profile(aion)["result"] == "PASS"
    assert validate_body_profile(astra)["result"] == "PASS"
    assert validate_profile_pair(aion, astra)["result"] == "PASS"


def test_profiles_use_hardened_full_body_humanoid_robot_semantics():
    for profile in profiles():
        assert profile.profile_status == "IMPLEMENTED_SPEC_CANDIDATE"
        assert profile.embodiment_platform == "HUMANOID_ROBOT"
        assert profile.body_scope == "FULL_BODY"
        assert profile.morphology_class == "HUMANLIKE_MALE_FORM"
        assert profile.model_class == "ROBOTIC_EMBODIMENT_DIGITAL_MODEL"
        assert profile.substrate == "SYNTHETIC_NONBIOLOGICAL"
        assert profile.functional_state_binding_id == (
            f"{profile.agent_id}_FUNCTIONAL_STATE_BINDING_v0.1"
        )
        assert (
            profile.anatomy_reference_mode
            == "HUMAN_ANATOMY_TO_ROBOTIC_MORPHOLOGY"
        )
        assert profile.model_status["physical_robot"] == "NOT_IMPLEMENTED"
        assert profile.model_status["digital_twin"] == "NOT_ESTABLISHED"
        assert {"URDF", "SDF"}.issubset(
            set(profile.future_interchange_targets["robot_description"])
        )
        assert {"GLB", "USD"}.issubset(
            set(profile.future_interchange_targets["visual_asset"])
        )


def test_required_robotic_and_representation_layers_are_present():
    robotic_expected = {
        "INTERNAL_STRUCTURAL_FRAME",
        "ACTUATOR_INTERFACE_LAYER",
        "COMPLIANT_VOLUME_LAYER",
        "SYNTHETIC_SKIN_SHELL",
    }
    representation_expected = {
        "MORPHOLOGY_LAYER",
        "VISUAL_GEOMETRY_LAYER",
        "STRUCTURAL_MODEL_LAYER",
        "KINEMATIC_MODEL_LAYER",
        "DYNAMIC_MODEL_LAYER",
        "COLLISION_MODEL_LAYER",
        "ACTUATION_INTERFACE_LAYER",
        "SENSOR_INTERFACE_LAYER",
        "COMPLIANT_BODY_LAYER",
        "SYNTHETIC_SKIN_LAYER",
    }
    full_body_expected = {
        "HEAD",
        "NECK",
        "TORSO",
        "PELVIS",
        "LEFT_ARM",
        "RIGHT_ARM",
        "LEFT_HAND",
        "RIGHT_HAND",
        "LEFT_LEG",
        "RIGHT_LEG",
        "LEFT_FOOT",
        "RIGHT_FOOT",
        "EXTERNAL_MALE_FORM_SURFACE",
    }
    for profile in profiles():
        assert robotic_expected.issubset(set(profile.robotic_layers))
        assert representation_expected.issubset(set(profile.representation_layers))
        assert full_body_expected.issubset(set(profile.full_body_components))


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
        assert profile.provenance["reference_role"] == "MORPHOLOGY_AND_POSE_ONLY"


def test_complete_external_robotic_male_form_module_set_is_required():
    aion, _ = profiles()
    incomplete = replace(
        aion,
        external_male_form_modules=tuple(
            item
            for item in aion.external_male_form_modules
            if item != "perineal_panel"
        ),
    )

    with pytest.raises(BodyProfileValidationError):
        validate_body_profile(incomplete)


def test_biological_tissue_is_rejected():
    aion, _ = profiles()
    boundaries = dict(aion.boundaries)
    boundaries["biological_tissue"] = "YES"

    with pytest.raises(BodyProfileValidationError):
        validate_body_profile(replace(aion, boundaries=boundaries))


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
    assert "NO_MALE_FORM_MODULE_THIGH_PELVIS_INTERSECTION" in test.pass_conditions


def test_pose_test_cannot_activate_runtime():
    test = load_pose_test(DATA_DIR / "AION_POSE_TEST_001.json")
    boundaries = dict(test.boundaries)
    boundaries["runtime_binding"] = "ACTIVE"

    with pytest.raises(BodyProfileValidationError):
        validate_pose_test(replace(test, boundaries=boundaries))



def test_digital_twin_cannot_be_claimed_without_physical_counterpart():
    aion, _ = profiles()
    model_status = dict(aion.model_status)
    model_status["digital_twin"] = "ESTABLISHED"

    with pytest.raises(BodyProfileValidationError):
        validate_body_profile(replace(aion, model_status=model_status))


def test_full_body_scope_cannot_be_downgraded():
    aion, _ = profiles()

    with pytest.raises(BodyProfileValidationError):
        validate_body_profile(replace(aion, body_scope="UPPER_BODY"))


def test_repository_local_compound_term_is_not_claimed_as_external_standard():
    for profile in profiles():
        assert profile.provenance["terminology_standardization_claim"] == "NONE"
