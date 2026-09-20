from __future__ import annotations

import pytest

from aion_astra_twin_embodiment.teacher_body_channels import (
    build_teacher_body_signal_schema,
)
from aion_astra_twin_embodiment.teacher_body_dynamics import (
    SensorimotorExpectation,
    TeacherBodyObservation,
    append_teacher_body_state,
    build_teacher_body_dynamics_profile,
    build_teacher_motivational_representation,
    build_teacher_within_session_trajectory,
    evaluate_teacher_sensorimotor_prediction,
    integrate_teacher_body_state,
    validate_teacher_body_dynamics_profile,
)


def _integrated_state(sequence: int, timestamp_ms: int):
    return integrate_teacher_body_state(
        (
            TeacherBodyObservation("TACTILE_GENERAL", (0.2,), timestamp_ms),
            TeacherBodyObservation("JOINT_POSITION", (0.1, 0.2), timestamp_ms),
            TeacherBodyObservation(
                "VESTIBULAR_ORIENTATION",
                (1.0, 0.0, 0.0, 0.0),
                timestamp_ms,
            ),
            TeacherBodyObservation("CARDIOVASCULAR_STATE", (0.5,), timestamp_ms),
        ),
        sequence=sequence,
    )


def test_every_body_signal_has_runtime_semantics_and_homeostatic_binding() -> None:
    schema = build_teacher_body_signal_schema()
    profile = build_teacher_body_dynamics_profile(schema)
    result = validate_teacher_body_dynamics_profile(profile, schema)

    assert result["result"] == "PASS"
    assert len(profile.signal_semantics) == len(schema.channels)
    semantic_ids = {item.channel_id for item in profile.signal_semantics}
    assert "HYDRATION_STATE" in semantic_ids
    assert "ENERGY_AVAILABILITY_STATE" in semantic_ids
    assert "SLEEP_WAKE_STATE" in semantic_ids
    assert "GENITAL_SENSORY_AFFERENT_REFERENCE" in semantic_ids
    assert "PRURICEPTIVE_REFERENCE" in semantic_ids
    assert "VESTIBULAR_LINEAR_ACCELERATION" in semantic_ids
    assert "VESTIBULAR_ANGULAR_VELOCITY" in semantic_ids
    assert "OSMOTIC_BALANCE_STATE" in semantic_ids
    assert "MUSCLE_FATIGUE_PHYSIOLOGY_STATE" in semantic_ids
    assert "IMMUNE_ACTIVITY_STATE" in semantic_ids
    assert "TISSUE_INJURY_STATE" in semantic_ids
    assert all(
        item.missing_value_policy == "MISSING_IS_UNKNOWN_NOT_ZERO"
        for item in profile.signal_semantics
    )
    transition_ids = {
        item.transition_id for item in profile.physiological_transitions
    }
    assert "MUSCULOSKELETAL_BASELINE_TO_LOAD" in transition_ids
    assert "FLUID_BALANCE_TO_OSMOTIC_LOAD" in transition_ids
    assert "RESPIRATORY_BASELINE_TO_WORKLOAD" in transition_ids
    assert "IMMUNE_BASELINE_TO_INFLAMMATORY_RESPONSE" in transition_ids
    assert "TISSUE_BASELINE_TO_INJURY" in transition_ids
    assert "TISSUE_INJURY_TO_REPAIR" in transition_ids
    assert "SEXUAL_BASELINE_TO_VASCULAR_RESPONSE" in transition_ids
    assert "DETUMESCENCE_TO_RECOVERY" in transition_ids
    homeostatic_ids = {
        item.variable_id for item in profile.homeostatic_variables
    }
    assert "OSMOTIC_ELECTROLYTE_BALANCE" in homeostatic_ids
    assert "AUTONOMIC_REGULATION" in homeostatic_ids
    assert "MUSCULOSKELETAL_LOAD_RECOVERY" in homeostatic_ids
    assert "IMMUNE_INFLAMMATORY_BALANCE" in homeostatic_ids
    assert "TISSUE_INJURY_REPAIR" in homeostatic_ids
    assert profile.phenomenal_experience_status == "NOT_ESTABLISHED"


def test_integrated_body_state_requires_all_core_body_signal_domains() -> None:
    with pytest.raises(ValueError, match="all core body observation domains"):
        integrate_teacher_body_state(
            (
                TeacherBodyObservation("TACTILE_GENERAL", (0.2,), 100),
                TeacherBodyObservation("JOINT_POSITION", (0.1,), 100),
                TeacherBodyObservation("CARDIOVASCULAR_STATE", (0.5,), 100),
            ),
            sequence=0,
        )

    state = _integrated_state(0, 100)
    assert state.integration_status == "INTEGRATED_REFERENCE_STATE"
    assert "VESTIBULAR" in state.domain_coverage
    assert "REPRODUCTIVE_SEXUAL_PHYSIOLOGY" not in state.domain_coverage
    assert len(state.body_state_sha256) == 64
    assert state.felt_body_status == "NOT_ESTABLISHED"


def test_reproductive_observation_is_available_but_not_mandatory_in_every_body_state() -> None:
    state = integrate_teacher_body_state(
        (
            TeacherBodyObservation("TACTILE_GENERAL", (0.2,), 100),
            TeacherBodyObservation("JOINT_POSITION", (0.1,), 100),
            TeacherBodyObservation(
                "VESTIBULAR_ORIENTATION",
                (1.0, 0.0, 0.0, 0.0),
                100,
            ),
            TeacherBodyObservation("CARDIOVASCULAR_STATE", (0.5,), 100),
            TeacherBodyObservation("GENITAL_VASCULAR_STATE", (0.3,), 100),
        ),
        sequence=0,
    )

    assert "REPRODUCTIVE_SEXUAL_PHYSIOLOGY" in state.domain_coverage


def test_sensorimotor_prediction_error_is_observable_without_felt_agency_claim() -> None:
    state = _integrated_state(0, 100)
    evaluation = evaluate_teacher_sensorimotor_prediction(
        state,
        motor_channel_id="POSTURE_CONTROL",
        expectations=(
            SensorimotorExpectation("JOINT_POSITION", (0.2, 0.3)),
        ),
        observations=(
            TeacherBodyObservation("JOINT_POSITION", (0.21, 0.29), 110),
        ),
    )

    assert evaluation.mean_absolute_error == pytest.approx(0.01)
    assert evaluation.correction_status == "WITHIN_REFERENCE_TOLERANCE"
    assert evaluation.felt_agency_status == "NOT_ESTABLISHED"
    assert len(evaluation.evaluation_sha256) == 64


def test_motivational_representation_stays_distinct_from_phenomenal_desire() -> None:
    state = _integrated_state(0, 100)
    representation = build_teacher_motivational_representation(
        representation_id="BODY-MOTIVATION-1",
        representation_domain="REPRODUCTIVE_SEXUAL_PHYSIOLOGY",
        source_body_state_sha256=state.body_state_sha256,
        salience=0.4,
        approach_weight=0.2,
        avoidance_weight=-0.1,
        wanting_weight=0.3,
        predicted_liking=0.1,
        valence=0.2,
    )

    assert representation.representation_status == "REPRESENTATIONAL_STATE_ONLY"
    assert representation.wanting_weight == pytest.approx(0.3)
    assert representation.phenomenal_desire_status == "NOT_ESTABLISHED"
    assert representation.phenomenal_pleasure_status == "NOT_ESTABLISHED"


def test_within_session_body_trajectory_is_content_addressed_and_ordered() -> None:
    trajectory = build_teacher_within_session_trajectory("TRAJECTORY-1")
    first = _integrated_state(0, 100)
    second = _integrated_state(1, 200)

    trajectory = append_teacher_body_state(trajectory, first)
    digest_after_first = trajectory.trajectory_sha256
    trajectory = append_teacher_body_state(trajectory, second)

    assert len(trajectory.states) == 2
    assert trajectory.trajectory_sha256 != digest_after_first

    with pytest.raises(ValueError, match="sequence must increase"):
        append_teacher_body_state(trajectory, first)


def test_sensorimotor_prediction_rejects_unknown_body_channel() -> None:
    state = _integrated_state(0, 100)

    with pytest.raises(ValueError, match="unknown body signal channel"):
        evaluate_teacher_sensorimotor_prediction(
            state,
            motor_channel_id="POSTURE_CONTROL",
            expectations=(
                SensorimotorExpectation("UNKNOWN_BODY_CHANNEL", (0.1,)),
            ),
            observations=(
                TeacherBodyObservation("UNKNOWN_BODY_CHANNEL", (0.1,), 110),
            ),
        )
