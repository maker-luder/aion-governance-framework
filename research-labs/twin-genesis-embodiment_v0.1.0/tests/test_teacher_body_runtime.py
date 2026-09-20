from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.teacher_body_runtime import (
    append_teacher_session_snapshot,
    apply_teacher_calibration_observations,
    build_teacher_body_runtime_binding,
    build_teacher_cross_session_retention,
    build_teacher_session_snapshot,
    initialize_teacher_calibration,
    load_teacher_cross_session_retention,
    update_teacher_adaptation,
    validate_teacher_body_runtime_binding,
    validate_teacher_cross_session_retention,
    validate_teacher_session_snapshot,
    write_teacher_cross_session_retention,
)


def _target_observations(state, offset: float = 0.0) -> dict[str, float]:
    return {
        probe.measurement_id: probe.target + offset
        for probe in state.probes
    }


def test_teacher_body_runtime_binding_is_materialized_without_live_external_actuation() -> None:
    binding = build_teacher_body_runtime_binding("RUNTIME-1", "SESSION-1")
    result = validate_teacher_body_runtime_binding(binding)

    assert result["result"] == "PASS"
    assert binding.binding_status == "REFERENCE_BINDING_MATERIALIZED"
    assert binding.physiology_profile_id == "ADULT_MALE_PHYSIOLOGY_REFERENCE_v0.1"
    assert binding.skeleton_root == "hips"
    assert binding.viewpoint_anchor == "head"
    assert binding.live_external_actuation is False
    assert binding.body_ownership_experience_status == "NOT_ESTABLISHED"
    assert binding.subjectivity_status == "NOT_ESTABLISHED"


def test_initial_calibration_requires_complete_observation_set() -> None:
    binding = build_teacher_body_runtime_binding("RUNTIME-1", "SESSION-1")
    state = initialize_teacher_calibration(binding)

    with pytest.raises(ValueError, match="every probe"):
        apply_teacher_calibration_observations(state, {"total_height": 183.0})


def test_calibration_adaptation_and_retention_are_content_addressed() -> None:
    binding = build_teacher_body_runtime_binding("RUNTIME-1", "SESSION-1")
    initial = initialize_teacher_calibration(binding)
    calibrated = apply_teacher_calibration_observations(
        initial,
        _target_observations(initial, offset=0.25),
    )
    adaptation = update_teacher_adaptation(calibrated)
    snapshot = build_teacher_session_snapshot(calibrated, adaptation)
    retention = append_teacher_session_snapshot(
        build_teacher_cross_session_retention(),
        snapshot,
    )

    assert calibrated.stage == "CALIBRATED_REFERENCE"
    assert calibrated.mean_absolute_error == pytest.approx(0.25)
    assert len(calibrated.receipt_sha256) == 64
    assert adaptation.sequence == 1
    assert adaptation.mechanism_status == "NOT_ESTABLISHED"
    assert len(snapshot.snapshot_sha256) == 64
    assert len(retention.snapshots) == 1
    assert retention.retention_status == "MATERIALIZED_DURABLE_REFERENCE"
    assert retention.subjective_continuity_status == "NOT_ESTABLISHED"


def test_cross_session_retention_roundtrips_as_hash_verified_json(tmp_path) -> None:
    binding = build_teacher_body_runtime_binding("RUNTIME-2", "SESSION-2")
    initial = initialize_teacher_calibration(binding)
    calibrated = apply_teacher_calibration_observations(
        initial,
        _target_observations(initial, offset=0.1),
    )
    adaptation = update_teacher_adaptation(calibrated)
    snapshot = build_teacher_session_snapshot(calibrated, adaptation)
    retention = append_teacher_session_snapshot(
        build_teacher_cross_session_retention(),
        snapshot,
    )

    path = tmp_path / "teacher-retention.json"
    receipt = write_teacher_cross_session_retention(retention, path)
    loaded = load_teacher_cross_session_retention(path)

    assert receipt.snapshot_count == 1
    assert len(receipt.file_sha256) == 64
    assert len(receipt.payload_sha256) == 64
    assert loaded.to_dict() == retention.to_dict()



def test_runtime_binding_rejects_physiology_profile_drift() -> None:
    binding = build_teacher_body_runtime_binding("RUNTIME-PHYS", "SESSION-PHYS")
    broken = replace(binding, physiology_profile_id="WRONG-PHYSIOLOGY")

    with pytest.raises(ValueError, match="physiology profile drift"):
        validate_teacher_body_runtime_binding(broken)


def test_retained_snapshot_hash_is_recomputed_and_verified() -> None:
    binding = build_teacher_body_runtime_binding("RUNTIME-HASH", "SESSION-HASH")
    initial = initialize_teacher_calibration(binding)
    calibrated = apply_teacher_calibration_observations(
        initial,
        _target_observations(initial, offset=0.15),
    )
    adaptation = update_teacher_adaptation(calibrated)
    snapshot = build_teacher_session_snapshot(calibrated, adaptation)

    assert validate_teacher_session_snapshot(snapshot)["result"] == "PASS"

    broken = replace(snapshot, snapshot_sha256="0" * 64)
    retention = replace(
        build_teacher_cross_session_retention(),
        snapshots=(broken,),
    )

    with pytest.raises(ValueError, match="snapshot hash mismatch"):
        validate_teacher_cross_session_retention(retention)
