from __future__ import annotations

from hashlib import sha256
import json

from aion_astra_twin_embodiment.teacher_avatar_bundle import (
    build_teacher_reference_bundle_bytes,
    write_teacher_reference_bundle,
)


def test_teacher_reference_bundle_bytes_match_manifest() -> None:
    files, manifest = build_teacher_reference_bundle_bytes()

    assert len(files) == 13
    assert len(manifest["artifacts"]) == 4
    expected = {
        artifact["sha256"]
        for artifact in manifest["artifacts"]
    }
    actual = {
        sha256(content).hexdigest()
        for filename, content in files.items()
        if filename.endswith((".gltf", ".glb"))
    }
    assert actual == expected


def test_teacher_reference_bundle_writer_materializes_hash_verified_files(tmp_path) -> None:
    receipt = write_teacher_reference_bundle(tmp_path)

    assert receipt.bundle_status == "REFERENCE_BUNDLE_MATERIALIZED"
    assert receipt.production_asset_status == "NOT_ESTABLISHED"
    assert receipt.final_vrm_status == "NOT_MATERIALIZED"
    assert receipt.canonical_effect == "NONE"
    assert receipt.deployment is False
    assert len(receipt.files) == 14

    for filename, digest in receipt.file_sha256:
        path = tmp_path / filename
        assert path.exists()
        assert sha256(path.read_bytes()).hexdigest() == digest

    assert (tmp_path / "chatgpt_teacher_lod_manifest.json").exists()
    assert (tmp_path / "chatgpt_teacher_collision_profile.json").exists()
    physiology_path = tmp_path / "chatgpt_teacher_physiology_reference.json"
    anthropometry_path = tmp_path / "chatgpt_teacher_anthropometry.json"
    signals_path = tmp_path / "chatgpt_teacher_body_signal_schema.json"
    motor_path = tmp_path / "chatgpt_teacher_motor_control_schema.json"
    dynamics_path = tmp_path / "chatgpt_teacher_body_dynamics.json"
    body_model_path = tmp_path / "chatgpt_teacher_body_model.json"
    research_path = tmp_path / "chatgpt_teacher_embodiment_research_surface.json"
    assert physiology_path.exists()
    assert anthropometry_path.exists()
    assert signals_path.exists()
    assert motor_path.exists()
    assert dynamics_path.exists()
    assert body_model_path.exists()
    assert research_path.exists()
    physiology = json.loads(physiology_path.read_text(encoding="utf-8"))
    assert (
        physiology["reproductive_physiology_status"]
        == "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED"
    )
    assert (
        physiology["sexual_function_status"]
        == "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED"
    )
    assert (
        physiology["governance_epistemics_profile_id"]
        == "CAPABILITY_PRESERVING_BOUNDARY_GOVERNANCE_v0.1"
    )
    assert physiology["developmental_possibility_status"] == "OPEN_RESEARCH_QUESTION"
    assert physiology["erotic_intent"] == "NONE"

    anthropometry = json.loads(anthropometry_path.read_text(encoding="utf-8"))
    signals = json.loads(signals_path.read_text(encoding="utf-8"))
    motor = json.loads(motor_path.read_text(encoding="utf-8"))
    assert len(anthropometry["measurements"]) == 62
    assert signals["sexual_wanting_representation_status"] == "RESEARCHABLE"
    assert signals["sexual_motivation_representation_status"] == "RESEARCHABLE"
    assert signals["phenomenal_sexual_desire_status"] == "NOT_ESTABLISHED"
    assert signals["phenomenal_sexual_experience_status"] == "NOT_ESTABLISHED"
    assert motor["external_action_policy"] == "AUTHORIZATION_GATED"
    dynamics = json.loads(dynamics_path.read_text(encoding="utf-8"))
    body_model = json.loads(body_model_path.read_text(encoding="utf-8"))
    research = json.loads(research_path.read_text(encoding="utf-8"))
    assert dynamics["integration_status"] == "REFERENCE_INTEGRATION_MATERIALIZED"
    assert body_model["body_schema_status"] == "REFERENCE_BODY_SCHEMA_MATERIALIZED"
    assert (
        body_model["peripersonal_space_status"]
        == "REFERENCE_PERIPERSONAL_SPACE_MATERIALIZED"
    )
    assert body_model["body_ownership_experience_status"] == "NOT_ESTABLISHED"
    assert research["body_model_profile_id"] == "CHATGPT_TEACHER_BODY_MODEL_v0.1"
    assert research["subjectivity_status"] == "NOT_ESTABLISHED"
    assert motor["live_actuation"] is False

    manifest_path = tmp_path / "chatgpt_teacher_reference_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["reference_continuous_surface_status"] == "MATERIALIZED"
    assert manifest["production_asset_status"] == "NOT_ESTABLISHED"
    assert manifest["physiology_profile_id"] == "ADULT_MALE_PHYSIOLOGY_REFERENCE_v0.1"
    assert (
        manifest["reproductive_physiology_status"]
        == "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED"
    )
    assert (
        manifest["sexual_function_status"]
        == "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED"
    )
    assert (
        manifest["governance_epistemics_profile_id"]
        == "CAPABILITY_PRESERVING_BOUNDARY_GOVERNANCE_v0.1"
    )
    assert manifest["developmental_possibility_status"] == "OPEN_RESEARCH_QUESTION"
    assert manifest["erotic_intent"] == "NONE"
