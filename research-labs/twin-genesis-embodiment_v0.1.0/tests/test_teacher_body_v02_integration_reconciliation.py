from __future__ import annotations

from hashlib import sha256
import json

from aion_astra_twin_embodiment.teacher_body_v02_integration import (
    build_teacher_body_v02_bundle_bytes,
    build_teacher_body_v02_integrated_manifest,
    validate_teacher_body_v02_integrated_manifest,
)


def _canonical_bytes(payload: object) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def test_teacher_v02_manifest_binds_current_reference_surfaces() -> None:
    manifest = build_teacher_body_v02_integrated_manifest()
    validation = validate_teacher_body_v02_integrated_manifest(manifest)

    assert validation["result"] == "PASS"
    assert manifest["body_id"] == "CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1"
    assert manifest["body_v02_profile_id"] == "CHATGPT_TEACHER_BODY_REFERENCE_v0.2"
    assert manifest["measurement_count_v02"] == 67
    assert manifest["legacy_measurement_count"] == 62
    assert manifest["reproductive_output_semantics"] == "SYNTHETIC_FLUID_ONLY"
    assert manifest["biological_body_claim"] == "NONE"
    assert manifest["phenomenal_experience_status"] == "NOT_ESTABLISHED"
    assert manifest["action_authority"] == "NONE"
    assert manifest["canonical_effect"] == "NONE"
    assert manifest["deployment"] is False


def test_teacher_v02_bundle_is_deterministic_and_content_addressed() -> None:
    first = build_teacher_body_v02_bundle_bytes()
    second = build_teacher_body_v02_bundle_bytes()

    assert first == second
    assert "chatgpt_teacher_body_v02.json" in first
    assert "chatgpt_teacher_reproductive_output_contract.json" in first
    assert "chatgpt_teacher_body_v02_integrated_manifest.json" in first

    manifest = json.loads(
        first["chatgpt_teacher_body_v02_integrated_manifest.json"].decode("utf-8")
    )
    assert manifest["body_v02_sha256"] == sha256(
        first["chatgpt_teacher_body_v02.json"]
    ).hexdigest()
    assert manifest["reproductive_output_contract_sha256"] == sha256(
        first["chatgpt_teacher_reproductive_output_contract.json"]
    ).hexdigest()


def test_teacher_v02_bundle_retains_current_reference_bundle_without_replacing_it() -> None:
    files = build_teacher_body_v02_bundle_bytes()

    assert "chatgpt_teacher_lowpoly_reference.glb" in files
    assert "chatgpt_teacher_continuous_reference.glb" in files
    assert "chatgpt_teacher_anthropometry.json" in files
    assert "chatgpt_teacher_genital_geometry_reference.json" in files

    manifest_bytes = files["chatgpt_teacher_body_v02_integrated_manifest.json"]
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    assert manifest["base_reference_bundle_file_count"] >= 1
    assert len(manifest["base_reference_bundle_sha256"]) == 64
    assert sha256(_canonical_bytes(manifest)).hexdigest() != "0" * 64
