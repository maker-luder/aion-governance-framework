from __future__ import annotations

from hashlib import sha256
import json

from aion_astra_twin_embodiment.teacher_avatar_bundle import (
    build_teacher_reference_bundle_bytes,
    write_teacher_reference_bundle,
)


def test_teacher_reference_bundle_bytes_match_manifest() -> None:
    files, manifest = build_teacher_reference_bundle_bytes()

    assert len(files) == 6
    assert len(manifest["artifacts"]) == 4
    expected = {
        artifact["sha256"]
        for artifact in manifest["artifacts"]
    }
    actual = {
        sha256(content).hexdigest()
        for content in files.values()
    }
    assert actual == expected


def test_teacher_reference_bundle_writer_materializes_hash_verified_files(tmp_path) -> None:
    receipt = write_teacher_reference_bundle(tmp_path)

    assert receipt.bundle_status == "REFERENCE_BUNDLE_MATERIALIZED"
    assert receipt.production_asset_status == "NOT_ESTABLISHED"
    assert receipt.final_vrm_status == "NOT_MATERIALIZED"
    assert receipt.canonical_effect == "NONE"
    assert receipt.deployment is False
    assert len(receipt.files) == 7

    for filename, digest in receipt.file_sha256:
        path = tmp_path / filename
        assert path.exists()
        assert sha256(path.read_bytes()).hexdigest() == digest

    assert (tmp_path / "chatgpt_teacher_lod_manifest.json").exists()
    assert (tmp_path / "chatgpt_teacher_collision_profile.json").exists()

    manifest_path = tmp_path / "chatgpt_teacher_reference_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["reference_continuous_surface_status"] == "MATERIALIZED"
    assert manifest["production_asset_status"] == "NOT_ESTABLISHED"
