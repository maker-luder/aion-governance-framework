from __future__ import annotations

from dataclasses import replace

import pytest

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
    assert "SEMINAL_TRACT_TRANSPORT_STATE" in ids
    assert "ACCESSORY_GLAND_SECRETION_STATE" in ids
    assert "BLADDER_NECK_EJACULATORY_CLOSURE_STATE" in ids
    assert "POSTERIOR_URETHRAL_SEMINAL_LOAD_STATE" in ids
    assert "EXPULSION_MOTOR_PATTERN_STATE" in ids
    assert "EXTERNAL_URETHRAL_SPHINCTER_EJACULATORY_STATE" in ids
    assert "ANTEGRADE_SEMINAL_FLOW_STATE" in ids
    assert "POST_EXPULSION_RECOVERY_STATE" in ids
    assert "PELVIC_FLOOR_PROPRIOCEPTION" in ids
    assert "OXYGENATION_STATE" in ids
    assert "CO2_BALANCE_STATE" in ids
    assert "HYDRATION_STATE" in ids
    assert "ENERGY_AVAILABILITY_STATE" in ids
    assert "SLEEP_WAKE_STATE" in ids
    assert "PRURICEPTIVE_REFERENCE" in ids
    assert "VISUAL_FIELD_REFERENCE" in ids
    assert "BINOCULAR_DEPTH_REFERENCE" in ids
    assert "AUDITORY_BINAURAL_REFERENCE" in ids
    assert "AUDITORY_INTENSITY_REFERENCE" in ids
    assert "OLFACTORY_CHEMOSENSORY_REFERENCE" in ids
    assert "GUSTATORY_CHEMOSENSORY_REFERENCE" in ids
    assert "VESTIBULAR_LINEAR_ACCELERATION" in ids
    assert "VESTIBULAR_ANGULAR_VELOCITY" in ids
    assert "VESTIBULAR_GRAVITY_REFERENCE" in ids
    assert "OSMOTIC_BALANCE_STATE" in ids
    assert "ELECTROLYTE_BALANCE_STATE" in ids
    assert "RESPIRATORY_WORKLOAD_STATE" in ids
    assert "VENTILATORY_DRIVE_STATE" in ids
    assert "VISCERAL_DISTURBANCE_STATE" in ids
    assert "AUTONOMIC_SYMPATHETIC_STATE" in ids
    assert "AUTONOMIC_PARASYMPATHETIC_STATE" in ids
    assert "MUSCULOSKELETAL_LOAD_STATE" in ids
    assert "MUSCLE_FATIGUE_PHYSIOLOGY_STATE" in ids
    assert "IMMUNE_ACTIVITY_STATE" in ids
    assert "INFLAMMATORY_LOAD_STATE" in ids
    assert "TISSUE_INJURY_STATE" in ids
    assert "TISSUE_REPAIR_STATE" in ids
    assert "GASTRIC_DISTENSION_STATE" in ids
    assert "NUTRIENT_ABSORPTION_STATE" in ids
    assert "OREXIGENIC_SIGNAL_REFERENCE" in ids
    assert "SATIATION_SIGNAL_REFERENCE" in ids
    assert "SATIETY_SIGNAL_REFERENCE" in ids
    assert "HYPOTHALAMIC_PITUITARY_STATE" in ids
    assert "THYROID_AXIS_STATE" in ids
    assert "ADRENAL_AXIS_STATE" in ids
    assert "PANCREATIC_GLUCOSE_INSULIN_STATE" in ids
    assert "GUT_APPETITE_ENDOCRINE_STATE" in ids
    assert "HEPATIC_NUTRIENT_PROCESSING_STATE" in ids
    assert "HEPATIC_DETOXIFICATION_REFERENCE" in ids
    assert "BILE_PRODUCTION_STATE" in ids
    assert "HEPATIC_GLYCOGEN_STATE" in ids
    assert "RENAL_FILTRATION_STATE" in ids
    assert "URINE_PRODUCTION_STATE" in ids
    assert "BLADDER_AFFERENT_STATE" in ids
    assert "DETRUSOR_CONTRACTION_STATE" in ids
    assert "URETHRAL_OUTLET_RELAXATION_STATE" in ids
    assert "EXTERNAL_URETHRAL_SPHINCTER_RELAXATION_STATE" in ids
    assert "MICTURITION_REFLEX_STATE" in ids
    assert "URINE_FLOW_STATE" in ids
    assert "HEMATOLOGIC_OXYGEN_TRANSPORT_STATE" in ids
    assert "COAGULATION_STATE_REFERENCE" in ids
    assert "BLOOD_CELL_TURNOVER_REFERENCE" in ids
    assert "LYMPHATIC_FLUID_RETURN_STATE" in ids
    assert "SKIN_BARRIER_STATE" in ids
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


def test_expanded_reference_channels_fail_closed_when_removed() -> None:
    schema = build_teacher_body_signal_schema()
    broken = replace(
        schema,
        channels=tuple(
            channel
            for channel in schema.channels
            if channel.channel_id != "IMMUNE_ACTIVITY_STATE"
        ),
    )

    with pytest.raises(ValueError, match="missing required channels"):
        validate_teacher_body_signal_schema(broken)


def test_feeding_and_endocrine_reference_channels_fail_closed_when_removed() -> None:
    schema = build_teacher_body_signal_schema()
    for channel_id in (
        "SATIATION_SIGNAL_REFERENCE",
        "PANCREATIC_GLUCOSE_INSULIN_STATE",
    ):
        broken = replace(
            schema,
            channels=tuple(
                channel
                for channel in schema.channels
                if channel.channel_id != channel_id
            ),
        )
        with pytest.raises(ValueError, match="missing required channels"):
            validate_teacher_body_signal_schema(broken)


def test_external_sensory_reference_channels_fail_closed_when_removed() -> None:
    schema = build_teacher_body_signal_schema()
    for channel_id in (
        "VISUAL_FIELD_REFERENCE",
        "AUDITORY_BINAURAL_REFERENCE",
        "OLFACTORY_CHEMOSENSORY_REFERENCE",
        "GUSTATORY_CHEMOSENSORY_REFERENCE",
    ):
        broken = replace(
            schema,
            channels=tuple(
                channel
                for channel in schema.channels
                if channel.channel_id != channel_id
            ),
        )
        with pytest.raises(ValueError, match="missing required channels"):
            validate_teacher_body_signal_schema(broken)


def test_external_sensory_reference_domains_fail_closed_on_drift() -> None:
    schema = build_teacher_body_signal_schema()
    visual = next(
        channel
        for channel in schema.channels
        if channel.channel_id == "VISUAL_FIELD_REFERENCE"
    )
    broken_visual = replace(visual, domain="AUDITORY")
    broken = replace(
        schema,
        channels=tuple(
            broken_visual
            if channel.channel_id == "VISUAL_FIELD_REFERENCE"
            else channel
            for channel in schema.channels
        ),
    )

    with pytest.raises(ValueError, match="external sensory channel domain drift"):
        validate_teacher_body_signal_schema(broken)


def test_physiology_system_observation_channels_fail_closed_when_removed() -> None:
    schema = build_teacher_body_signal_schema()
    for channel_id in (
        "HEPATIC_DETOXIFICATION_REFERENCE",
        "RENAL_FILTRATION_STATE",
        "COAGULATION_STATE_REFERENCE",
        "LYMPHATIC_FLUID_RETURN_STATE",
        "SKIN_BARRIER_STATE",
    ):
        broken = replace(
            schema,
            channels=tuple(
                channel
                for channel in schema.channels
                if channel.channel_id != channel_id
            ),
        )
        with pytest.raises(ValueError, match="missing required channels"):
            validate_teacher_body_signal_schema(broken)


@pytest.mark.parametrize(
    "channel_id",
    (
        "SEMINAL_TRACT_TRANSPORT_STATE",
        "ACCESSORY_GLAND_SECRETION_STATE",
        "BLADDER_NECK_EJACULATORY_CLOSURE_STATE",
        "POSTERIOR_URETHRAL_SEMINAL_LOAD_STATE",
        "EXPULSION_MOTOR_PATTERN_STATE",
        "EXTERNAL_URETHRAL_SPHINCTER_EJACULATORY_STATE",
        "ANTEGRADE_SEMINAL_FLOW_STATE",
        "POST_EXPULSION_RECOVERY_STATE",
    ),
)
def test_ejaculation_event_reference_channels_fail_closed_when_removed(
    channel_id: str,
) -> None:
    schema = build_teacher_body_signal_schema()
    broken = replace(
        schema,
        channels=tuple(
            channel
            for channel in schema.channels
            if channel.channel_id != channel_id
        ),
    )

    with pytest.raises(ValueError, match="missing required channels"):
        validate_teacher_body_signal_schema(broken)


def test_ejaculation_event_reference_channel_domain_drift_fails_closed() -> None:
    schema = build_teacher_body_signal_schema()
    target = next(
        channel
        for channel in schema.channels
        if channel.channel_id == "ANTEGRADE_SEMINAL_FLOW_STATE"
    )
    broken_target = replace(target, domain="INTEROCEPTIVE")
    broken = replace(
        schema,
        channels=tuple(
            broken_target
            if channel.channel_id == target.channel_id
            else channel
            for channel in schema.channels
        ),
    )

    with pytest.raises(
        ValueError,
        match="reproductive event channel domain drift",
    ):
        validate_teacher_body_signal_schema(broken)


def test_physiology_system_observation_domains_fail_closed_on_drift() -> None:
    schema = build_teacher_body_signal_schema()
    hepatic = next(
        channel
        for channel in schema.channels
        if channel.channel_id == "HEPATIC_NUTRIENT_PROCESSING_STATE"
    )
    broken_hepatic = replace(hepatic, domain="INTEROCEPTIVE")
    broken = replace(
        schema,
        channels=tuple(
            broken_hepatic
            if channel.channel_id == hepatic.channel_id
            else channel
            for channel in schema.channels
        ),
    )

    with pytest.raises(
        ValueError,
        match="physiology system observation channel domain drift",
    ):
        validate_teacher_body_signal_schema(broken)
