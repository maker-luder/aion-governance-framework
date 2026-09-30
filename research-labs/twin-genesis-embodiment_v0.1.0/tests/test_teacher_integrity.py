from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.teacher_integrity import (
    TeacherAssetEvidenceStatus,
    build_teacher_asset_evidence_status,
    build_teacher_evidence_receipts,
    teacher_integrity_probe,
    verify_teacher_evidence_receipts,
)


def test_teacher_probe_preserves_teacher_specific_fixed_candidate():
    result = teacher_integrity_probe()
    assert result["measurement_count"] == 62
    assert result["height_cm"] == 183.0
    assert result["mass_kg"] == 84.0
    assert result["reference_bundle_materialized"] is True
    assert result["production_asset_verified"] is False
    assert result["physical_body_present"] is False
    assert result["biological_realization"] is False
    assert result["felt_body_sensation"] == "NOT_ESTABLISHED"
    assert result["subjectivity"] == "NOT_ESTABLISHED"
    assert result["action_authority"] == "NONE"
    assert result["deployment"] is False


def test_reference_asset_cannot_be_promoted_to_physical_body():
    asset = build_teacher_asset_evidence_status()
    with pytest.raises(ValueError, match="physical/production"):
        replace(asset, physical_body_present=True)


def test_reference_asset_cannot_be_promoted_to_as_built():
    asset = build_teacher_asset_evidence_status()
    with pytest.raises(ValueError, match="physical/production"):
        replace(asset, as_built_verified=True)


def test_reference_body_cannot_grant_action_authority():
    asset = build_teacher_asset_evidence_status()
    with pytest.raises(ValueError, match="action authority"):
        replace(asset, action_authority="GRANTED")


def test_teacher_receipt_chain_detects_tampering():
    payloads = ({"a": 1}, {"b": 2}, {"c": 3})
    receipts = build_teacher_evidence_receipts(payloads)
    assert verify_teacher_evidence_receipts(payloads, receipts)
    assert not verify_teacher_evidence_receipts(({"a": 1}, {"b": 9}, {"c": 3}), receipts)


def test_invalid_asset_hash_is_rejected():
    with pytest.raises(ValueError, match="sha256"):
        TeacherAssetEvidenceStatus(
            reference_bundle_materialized=True,
            reference_file_count=1,
            reference_bundle_sha256="bad",
        )
