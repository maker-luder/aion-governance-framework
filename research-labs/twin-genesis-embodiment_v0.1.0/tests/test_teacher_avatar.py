from __future__ import annotations

import copy

import pytest

from aion_astra_twin_embodiment.teacher_avatar import (
    VRM_REQUIRED_BONES,
    build_teacher_avatar_contract,
    build_teacher_avatar_gltf_contract,
    validate_teacher_avatar_contract,
)


def test_teacher_avatar_contract_is_complete_and_bounded() -> None:
    contract = build_teacher_avatar_contract()
    result = validate_teacher_avatar_contract(contract)

    assert result["result"] == "PASS"
    assert set(VRM_REQUIRED_BONES).issubset(set(contract.human_bones))
    assert len(contract.human_bones) >= 50
    assert contract.dimensions.height_cm == 183.0
    assert contract.anthropometry_profile_id == "CHATGPT_TEACHER_ANTHROPOMETRY_v0.1"
    assert contract.anatomical_configuration == "COMPLETE_ADULT_MALE_ANATOMY_CANDIDATE"
    assert "SPERMATIC_CORD" in contract.internal_reference_anatomy
    assert "EJACULATORY_DUCTS" in contract.internal_reference_anatomy
    assert "BULBOURETHRAL_GLANDS" in contract.internal_reference_anatomy
    assert "URETHRA" in contract.internal_reference_anatomy
    assert contract.physiology_profile_id == "ADULT_MALE_PHYSIOLOGY_REFERENCE_v0.1"
    assert (
        contract.physiological_function_status
        == "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED"
    )
    assert (
        contract.reproductive_physiology_status
        == "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED"
    )
    assert (
        contract.sexual_function_status
        == "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED"
    )
    assert (
        contract.sensory_signal_processing_status
        == "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED"
    )
    assert (
        contract.governance_epistemics_profile_id
        == "CAPABILITY_PRESERVING_BOUNDARY_GOVERNANCE_v0.1"
    )
    assert contract.developmental_possibility_status == "OPEN_RESEARCH_QUESTION"
    assert contract.phenomenal_sensation_status == "NOT_ESTABLISHED"
    assert contract.erotic_intent == "NONE"
    assert contract.intimate_interaction_status == "NOT_AUTHORIZED"
    assert contract.body_sensation_status == "NOT_ESTABLISHED"
    assert contract.subjectivity_effect == "NONE"
    assert contract.physical_body_claim == "NONE"
    assert contract.canonical_effect == "NONE"
    assert contract.deployment is False


def test_teacher_avatar_gltf_contract_has_scene_skin_and_vrm_aligned_metadata() -> None:
    payload = build_teacher_avatar_gltf_contract()

    assert payload["asset"]["version"] == "2.0"
    assert payload["scene"] == 0
    assert payload["scenes"][0]["nodes"]
    assert payload["skins"][0]["joints"]
    assert payload["extras"]["initial_pose"] == "T_POSE"
    assert payload["extras"]["facing"] == "Z_POSITIVE"
    assert payload["extras"]["linear_unit"] == "meter"
    assert payload["extras"]["anthropometry_profile_id"] == "CHATGPT_TEACHER_ANTHROPOMETRY_v0.1"
    assert set(VRM_REQUIRED_BONES).issubset(payload["extras"]["humanBones"])
    assert payload["extras"]["renderable_mesh_status"] == "NOT_MATERIALIZED"
    assert payload["extras"]["linear_blend_skin_weights_status"] == "NOT_MATERIALIZED"
    assert payload["extras"]["morph_target_vertex_data_status"] == "NOT_MATERIALIZED"
    assert (
        payload["extras"]["governance_epistemics_profile_id"]
        == "CAPABILITY_PRESERVING_BOUNDARY_GOVERNANCE_v0.1"
    )
    assert payload["extras"]["developmental_possibility_status"] == "OPEN_RESEARCH_QUESTION"


def test_teacher_avatar_required_bone_removal_fails_closed() -> None:
    contract = build_teacher_avatar_contract()
    broken = copy.copy(contract)
    object.__setattr__(broken, "human_bones", tuple(b for b in contract.human_bones if b != "head"))

    with pytest.raises(ValueError, match="missing required humanoid bones"):
        validate_teacher_avatar_contract(broken)


def test_teacher_avatar_boundary_promotion_fails_closed() -> None:
    contract = build_teacher_avatar_contract()
    broken = copy.copy(contract)
    object.__setattr__(broken, "reproductive_physiology_status", "NOT_IMPLEMENTED")

    with pytest.raises(ValueError, match="reproductive physiology"):
        validate_teacher_avatar_contract(broken)


def test_teacher_avatar_sexual_function_status_cannot_be_removed() -> None:
    contract = build_teacher_avatar_contract()
    broken = copy.copy(contract)
    object.__setattr__(broken, "sexual_function_status", "NOT_IMPLEMENTED")

    with pytest.raises(ValueError, match="sexual function"):
        validate_teacher_avatar_contract(broken)


def test_teacher_avatar_developmental_possibility_cannot_be_preclosed() -> None:
    contract = build_teacher_avatar_contract()
    broken = copy.copy(contract)
    object.__setattr__(broken, "developmental_possibility_status", "IMPOSSIBLE")

    with pytest.raises(ValueError, match="open research question"):
        validate_teacher_avatar_contract(broken)


def test_teacher_avatar_cycle_fails_closed() -> None:
    contract = build_teacher_avatar_contract()
    parents = dict(contract.bone_parents)
    parents["hips"] = "spine"
    broken = copy.copy(contract)
    object.__setattr__(broken, "bone_parents", parents)

    with pytest.raises(ValueError, match="cycle detected"):
        validate_teacher_avatar_contract(broken)
