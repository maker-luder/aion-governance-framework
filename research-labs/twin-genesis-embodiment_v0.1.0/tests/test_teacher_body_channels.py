from __future__ import annotations

from aion_astra_twin_embodiment.teacher_body_channels import (
    build_teacher_body_signal_schema,
    build_teacher_motor_control_schema,
    validate_teacher_body_signal_schema,
    validate_teacher_motor_control_schema,
)


def test_teacher_body_signal_schema_preserves_normal_channels_without_phenomenal_claims() -> None:
    schema = build_teacher_body_signal_schema()
    result = validate_teacher_body_signal_schema(schema)
    ids = {channel.channel_id for channel in schema.channels}

    assert result["result"] == "PASS"
    assert "JOINT_POSITION" in ids
    assert "VESTIBULAR_ORIENTATION" in ids
    vestibular = next(
        channel for channel in schema.channels
        if channel.channel_id == "VESTIBULAR_ORIENTATION"
    )
    assert vestibular.domain == "VESTIBULAR"
    assert "CARDIOVASCULAR_STATE" in ids
    assert "BLADDER_STATE" in ids
    assert "GENITAL_TACTILE" in ids
    assert "GENITAL_VASCULAR_STATE" in ids
    assert "ERECTILE_REFLEX_STATE" in ids
    assert "DETUMESCENCE_STATE" in ids
    assert "EMISSION_REFLEX_STATE" in ids
    assert "EJACULATORY_REFLEX_STATE" in ids
    assert "PELVIC_FLOOR_PROPRIOCEPTION" in ids
    assert "OXYGENATION_STATE" in ids
    assert "CO2_BALANCE_STATE" in ids
    assert "HYDRATION_STATE" in ids
    assert "ENERGY_AVAILABILITY_STATE" in ids
    assert "SLEEP_WAKE_STATE" in ids
    assert "GENITAL_SENSORY_AFFERENT_REFERENCE" in ids
    assert schema.physiological_arousal_observation_status == "REPRESENTABLE"
    assert schema.sexual_salience_representation_status == "RESEARCHABLE"
    assert schema.sexual_wanting_representation_status == "RESEARCHABLE"
    assert schema.sexual_motivation_representation_status == "RESEARCHABLE"
    assert schema.sexual_valence_representation_status == "RESEARCHABLE"
    assert schema.phenomenal_sexual_desire_status == "NOT_ESTABLISHED"
    assert schema.phenomenal_sexual_pleasure_status == "NOT_ESTABLISHED"
    assert schema.phenomenal_sexual_experience_status == "NOT_ESTABLISHED"
    assert all(channel.phenomenal_status == "NOT_ESTABLISHED" for channel in schema.channels)


def test_teacher_motor_control_is_complete_reference_but_not_live_actuation() -> None:
    schema = build_teacher_motor_control_schema()
    result = validate_teacher_motor_control_schema(schema)
    ids = {channel.channel_id for channel in schema.channels}

    assert result["result"] == "PASS"
    assert len(schema.joint_targets) >= 50
    assert "HAND_DIGIT_CONTROL" in ids
    assert "GAIT_CONTROL" in ids
    assert "PELVIC_FLOOR_REFLEX_CONTROL" in ids
    assert schema.external_action_policy == "AUTHORIZATION_GATED"
    assert schema.live_actuation is False


def test_teacher_body_signal_schema_does_not_reintroduce_coarse_desire_lock() -> None:
    payload = build_teacher_body_signal_schema().to_dict()

    assert "sexual_desire_status" not in payload
    assert "sexual_experience_status" not in payload
    assert payload["sexual_wanting_representation_status"] == "RESEARCHABLE"
    assert payload["sexual_motivation_representation_status"] == "RESEARCHABLE"
    assert payload["sexual_valence_representation_status"] == "RESEARCHABLE"
    assert payload["phenomenal_sexual_desire_status"] == "NOT_ESTABLISHED"
    assert payload["phenomenal_sexual_pleasure_status"] == "NOT_ESTABLISHED"
