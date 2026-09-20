from __future__ import annotations

import copy

import pytest

from aion_astra_twin_embodiment.teacher_avatar_asset import (
    build_teacher_low_poly_glb,
    build_teacher_low_poly_gltf,
)
from aion_astra_twin_embodiment.teacher_avatar_validation import (
    TeacherAvatarAssetValidationError,
    build_teacher_asset_manifest,
    validate_teacher_low_poly_glb,
    validate_teacher_low_poly_gltf,
)


def test_teacher_reference_gltf_validator_passes_current_asset() -> None:
    result = validate_teacher_low_poly_gltf(build_teacher_low_poly_gltf())

    assert result == {
        "result": "PASS",
        "gltf_structure": "PASS",
        "buffer_bounds": "PASS",
        "morph_targets": "PASS",
        "reference_skinning": "PASS",
        "governance_boundaries": "PASS",
    }


def test_teacher_reference_glb_validator_passes_current_asset() -> None:
    result = validate_teacher_low_poly_glb(build_teacher_low_poly_glb())

    assert result["result"] == "PASS"
    assert result["glb_container"] == "PASS"
    assert result["embedded_gltf"] == "PASS"


def test_teacher_reference_validator_rejects_mismatched_morph_count() -> None:
    payload = copy.deepcopy(build_teacher_low_poly_gltf())
    payload["accessors"][3]["count"] -= 1

    with pytest.raises(TeacherAvatarAssetValidationError, match="morph target vertex count"):
        validate_teacher_low_poly_gltf(payload)


def test_teacher_reference_validator_rejects_bad_skin_weights() -> None:
    payload = copy.deepcopy(build_teacher_low_poly_gltf())
    payload["accessors"][6]["count"] -= 1

    with pytest.raises(TeacherAvatarAssetValidationError, match="skinning attribute counts"):
        validate_teacher_low_poly_gltf(payload)


def test_teacher_reference_asset_manifest_is_deterministic_and_bounded() -> None:
    first = build_teacher_asset_manifest()
    second = build_teacher_asset_manifest()

    assert first == second
    assert len(first["artifacts"]) == 4
    assert [artifact["validation"] for artifact in first["artifacts"]] == [
        "PASS",
        "PASS",
        "PASS",
        "PASS",
    ]
    assert all(len(artifact["sha256"]) == 64 for artifact in first["artifacts"])
    continuous = [
        artifact
        for artifact in first["artifacts"]
        if artifact["kind"].startswith("CONTINUOUS_SKINNED")
    ]
    assert len(continuous) == 2
    assert all(artifact["mesh_validation"] == "PASS" for artifact in continuous)
    assert all(artifact["connected_components"] == 1 for artifact in continuous)
    assert first["reference_continuous_surface_status"] == "MATERIALIZED"
    assert first["reference_continuous_skinning_status"] == "MATERIALIZED"
    assert (
        first["sexual_function_status"]
        == "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED"
    )
    assert (
        first["governance_epistemics_profile_id"]
        == "CAPABILITY_PRESERVING_BOUNDARY_GOVERNANCE_v0.1"
    )
    assert first["developmental_possibility_status"] == "OPEN_RESEARCH_QUESTION"
    assert first["production_asset_status"] == "NOT_ESTABLISHED"
    assert first["physical_body_claim"] == "NONE"
    assert first["subjectivity_effect"] == "NONE"
    assert first["canonical_effect"] == "NONE"
    assert first["deployment"] is False
