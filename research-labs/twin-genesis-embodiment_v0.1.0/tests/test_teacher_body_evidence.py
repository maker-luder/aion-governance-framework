from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.teacher_body_evidence import (
    build_evidence_receipts,
    build_teacher_body_evidence_manifest,
    run_teacher_body_evidence_probe,
    verify_evidence_receipts,
)


def test_teacher_evidence_manifest_binds_existing_reference_assets():
    manifest = build_teacher_body_evidence_manifest()
    assert manifest.anthropometry_slots == 67
    assert manifest.reference_mesh_materialized is True
    assert manifest.production_asset_established is False
    assert manifest.physical_body_established is False
    assert manifest.as_built_measurement_verified is False
    assert manifest.action_authority == "NONE"
    assert manifest.subjectivity == "NOT_ESTABLISHED"


def test_teacher_evidence_receipts_are_deterministic_and_tamper_evident():
    manifest = build_teacher_body_evidence_manifest()
    first = build_evidence_receipts(manifest)
    second = build_evidence_receipts(manifest)
    assert first == second
    assert verify_evidence_receipts(manifest, first)
    tampered = list(first)
    tampered[2] = replace(tampered[2], payload_sha256="f" * 64)
    assert not verify_evidence_receipts(manifest, tuple(tampered))


def test_teacher_reference_evidence_cannot_be_promoted_to_physical_body():
    manifest = build_teacher_body_evidence_manifest()
    with pytest.raises(ValueError, match="cannot promote"):
        replace(manifest, physical_body_established=True)


def test_teacher_evidence_probe_preserves_nonclaims():
    probe = run_teacher_body_evidence_probe()
    assert probe["anthropometry_slots"] == 67
    assert probe["reference_assets"]["reference_mesh_materialized"] is True
    assert probe["evidence_chain"]["verified"] is True
    assert probe["nonclaims"]["physical_body_established"] is False
    assert probe["nonclaims"]["biological_body"] is False
    assert probe["nonclaims"]["felt_body_sensation"] == "NOT_ESTABLISHED"
    assert probe["nonclaims"]["subjectivity"] == "NOT_ESTABLISHED"
