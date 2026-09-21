from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.teacher_body_channels import (
    build_teacher_body_signal_schema,
)
from aion_astra_twin_embodiment.teacher_body_dynamics import (
    TeacherBodyObservation,
    build_teacher_body_dynamics_profile,
    integrate_teacher_body_state,
)
from aion_astra_twin_embodiment.teacher_body_model import (
    build_teacher_body_model_profile,
)
from aion_astra_twin_embodiment.teacher_physiology_observability import (
    build_teacher_physiology_observability_profile,
)
from aion_astra_twin_embodiment.teacher_body_runtime import (
    append_teacher_session_snapshot,
    apply_teacher_calibration_observations,
    bind_teacher_integrated_body_state,
    build_teacher_body_runtime_binding,
    build_teacher_cross_session_retention,
    build_teacher_session_snapshot,
    initialize_teacher_calibration,
    load_teacher_cross_session_retention,
    update_teacher_adaptation,
    validate_teacher_body_runtime_binding,
    validate_teacher_bound_body_state,
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
    assert binding.physiology_observability_profile_id == (
        "CHATGPT_TEACHER_PHYSIOLOGY_OBSERVABILITY_v0.1"
    )
    assert binding.body_dynamics_profile_id == "CHATGPT_TEACHER_BODY_DYNAMICS_v0.1"
    assert binding.body_model_profile_id == "CHATGPT_TEACHER_BODY_MODEL_v0.1"
    assert binding.research_surface_id == (
        "CHATGPT_TEACHER_EMBODIMENT_RESEARCH_SURFACE_v0.1"
    )
    assert result["body_model_binding"] == "PASS"
    assert result["physiology_observability_binding"] == "PASS"
    assert result["reference_completeness"] == "PASS"
    assert binding.skeleton_root == "hips"
    assert binding.viewpoint_anchor == "head"
    assert binding.live_external_actuation is False
    assert binding.body_ownership_experience_status == "NOT_ESTABLISHED"
    assert binding.subjectivity_status == "NOT_ESTABLISHED"


def _integrated_runtime_body_state():
    return integrate_teacher_body_state(
        (
            TeacherBodyObservation("TACTILE_GENERAL", (0.2,), 100),
            TeacherBodyObservation("JOINT_POSITION", (0.1,), 100),
            TeacherBodyObservation(
                "VESTIBULAR_ORIENTATION",
                (1.0, 0.0, 0.0, 0.0),
                100,
            ),
            TeacherBodyObservation("CARDIOVASCULAR_STATE", (0.5,), 100),
        ),
        sequence=3,
    )


def test_integrated_body_state_binds_to_exact_runtime_body_instance() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-INTEGRATION",
        "SESSION-INTEGRATION",
    )
    state = _integrated_runtime_body_state()
    bound = bind_teacher_integrated_body_state(binding, state)
    result = validate_teacher_bound_body_state(bound, binding, state)

    assert result["result"] == "PASS"
    assert bound.binding_id == binding.binding_id
    assert bound.runtime_id == binding.runtime_id
    assert bound.session_id == binding.session_id
    assert bound.body_id == binding.body_id
    assert bound.signal_schema_id == binding.signal_schema_id
    assert bound.body_dynamics_profile_id == binding.body_dynamics_profile_id
    assert bound.body_model_profile_id == binding.body_model_profile_id
    assert (
        bound.physiology_observability_profile_id
        == binding.physiology_observability_profile_id
    )
    assert bound.source_body_state_sha256 == state.body_state_sha256
    assert bound.sequence == state.sequence
    assert bound.timestamp_ms == state.timestamp_ms
    assert len(bound.bound_state_sha256) == 64
    assert bound.physical_body_claim == "NONE"
    assert bound.body_ownership_experience_status == "NOT_ESTABLISHED"
    assert bound.subjectivity_status == "NOT_ESTABLISHED"


def test_bound_body_state_fails_closed_on_instance_or_source_drift() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-INTEGRATION",
        "SESSION-INTEGRATION",
    )
    state = _integrated_runtime_body_state()
    bound = bind_teacher_integrated_body_state(binding, state)

    with pytest.raises(ValueError, match="session id drift"):
        validate_teacher_bound_body_state(
            replace(bound, session_id="OTHER-SESSION"),
            binding,
            state,
        )

    with pytest.raises(ValueError, match="source-state hash drift"):
        validate_teacher_bound_body_state(
            replace(bound, source_body_state_sha256="0" * 64),
            binding,
            state,
        )

    tampered_state = replace(state, body_state_sha256="0" * 64)
    with pytest.raises(ValueError, match="hash does not match bound signal schema"):
        bind_teacher_integrated_body_state(binding, tampered_state)


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


def test_runtime_validation_rejects_incomplete_actual_signal_instance() -> None:
    binding = build_teacher_body_runtime_binding("RUNTIME-GAP", "SESSION-GAP")
    signals = build_teacher_body_signal_schema()
    without_vestibular = replace(
        signals,
        channels=tuple(
            channel
            for channel in signals.channels
            if channel.domain != "VESTIBULAR"
        ),
    )
    dynamics = build_teacher_body_dynamics_profile(without_vestibular)

    with pytest.raises(ValueError, match="missing required channels"):
        validate_teacher_body_runtime_binding(
            binding,
            signals=without_vestibular,
            dynamics=dynamics,
        )


def test_runtime_validation_rejects_body_model_profile_drift() -> None:
    binding = build_teacher_body_runtime_binding("RUNTIME-MODEL", "SESSION-MODEL")
    body_model = build_teacher_body_model_profile()
    broken = replace(
        binding,
        body_model_profile_id="WRONG-BODY-MODEL",
    )

    with pytest.raises(ValueError, match="body-model profile drift"):
        validate_teacher_body_runtime_binding(
            broken,
            body_model=body_model,
        )


def test_runtime_validation_rejects_physiology_observability_profile_drift() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-OBSERVABILITY",
        "SESSION-OBSERVABILITY",
    )
    observability = build_teacher_physiology_observability_profile()
    broken = replace(
        binding,
        physiology_observability_profile_id="WRONG-OBSERVABILITY",
    )

    with pytest.raises(
        ValueError,
        match="physiology observability profile drift",
    ):
        validate_teacher_body_runtime_binding(
            broken,
            physiology_observability=observability,
        )
