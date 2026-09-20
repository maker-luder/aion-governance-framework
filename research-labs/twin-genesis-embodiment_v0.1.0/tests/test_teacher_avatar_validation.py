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
    assert [artifact["validation"] for artifact in first["artifacts"]] == ["PASS", "PASS"]
    assert all(len(artifact["sha256"]) == 64 for artifact in first["artifacts"])
    assert first["production_asset_status"] == "NOT_ESTABLISHED"
    assert first["physical_body_claim"] == "NONE"
    assert first["subjectivity_effect"] == "NONE"
    assert first["canonical_effect"] == "NONE"
    assert first["deployment"] is False
