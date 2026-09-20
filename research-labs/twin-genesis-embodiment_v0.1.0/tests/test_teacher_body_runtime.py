from __future__ import annotations

import pytest

from aion_astra_twin_embodiment.teacher_body_runtime import (
    append_teacher_session_snapshot,
    apply_teacher_calibration_observations,
    build_teacher_body_runtime_binding,
    build_teacher_cross_session_retention,
    build_teacher_session_snapshot,
    initialize_teacher_calibration,
    update_teacher_adaptation,
    validate_teacher_body_runtime_binding,
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
    assert retention.subjective_continuity_status == "NOT_ESTABLISHED"
