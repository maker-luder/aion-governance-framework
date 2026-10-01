from __future__ import annotations

from dataclasses import replace

from aion_astra_twin_embodiment import teacher_state_loop as state_loop
from aion_astra_twin_embodiment.teacher_body_dynamics import (
    TeacherBodyObservation,
    integrate_teacher_body_state,
)
from aion_astra_twin_embodiment.teacher_body_runtime import (
    build_teacher_body_runtime_binding,
)
from aion_astra_twin_embodiment.teacher_intimate_integration import (
    TeacherOrgasmReferenceGate,
    integrate_teacher_intimate_reference,
)


def _high_stimulus(*, motivation: float) -> state_loop.TeacherStimulusEnvelope:
    return state_loop.build_teacher_stimulus_envelope(
        stimulus_id="TEACHER-INTIMATE-INTEGRATION-HIGH",
        stimulus_class="HIGH_SALIENCE_INTIMATE_REFERENCE",
        salience=0.95,
        functional_motivation=motivation,
        sexual_context_gate=True,
        inhibition=0.05,
    )


def _replace_scalar(body, channel_id: str, value: float):
    observations = []
    for observation in body.observations:
        if observation.channel_id == channel_id:
            observations.append(
                TeacherBodyObservation(
                    channel_id,
                    (value,),
                    observation.timestamp_ms,
                    observation.confidence,
                )
            )
        else:
            observations.append(observation)
    return integrate_teacher_body_state(
        observations,
        sequence=body.sequence,
    )


def test_state_loop_materializes_intimate_integration_state() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-INTIMATE-INTEGRATION",
        "SESSION-INTIMATE-INTEGRATION",
    )
    body = state_loop.build_teacher_reference_baseline_state(binding)
    controller = state_loop.build_teacher_reference_controller_state(binding, body)

    frame = state_loop.advance_teacher_embodied_tick(
        binding,
        previous_controller_state=controller,
        previous_body_state=body,
        stimulus=_high_stimulus(motivation=0.0),
    )

    integrated = frame.intimate_integration_state
    assert integrated.source_phase == frame.high_salience_phase_state.phase
    assert integrated.functional_desire.functional_motivation == 0.0
    assert integrated.functional_desire.phenomenal_desire_status == "NOT_ESTABLISHED"
    assert integrated.systemic_arousal.observation_policy == "OBSERVE_NOT_FORCE"
    assert integrated.endocrine_observation.concentration_status == (
        "UNKNOWN_NOT_SYNTHESIZED"
    )
    assert len(integrated.state_sha256) == 64


def test_high_physiological_activation_does_not_create_functional_desire() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-INTIMATE-ZERO-DESIRE",
        "SESSION-INTIMATE-ZERO-DESIRE",
    )
    body = state_loop.build_teacher_reference_baseline_state(binding)
    controller = state_loop.build_teacher_reference_controller_state(binding, body)
    previous_phase = None
    frame = None

    for _ in range(12):
        frame = state_loop.advance_teacher_embodied_tick(
            binding,
            previous_controller_state=controller,
            previous_body_state=body,
            stimulus=_high_stimulus(motivation=0.0),
            previous_phase_state=previous_phase,
        )
        body = frame.body_state
        controller = replace(
            frame.controller_state,
            previous_body_schema_feedback_sha256=(
                frame.body_schema_feedback_sha256
            ),
        )
        previous_phase = frame.high_salience_phase_state

    assert frame is not None
    assert frame.controller_state.activation > 0.5
    assert frame.intimate_integration_state.functional_desire.phase == "ORIENTING"
    assert (
        frame.intimate_integration_state.functional_desire.functional_motivation
        == 0.0
    )
    assert frame.intimate_integration_state.functional_desire.wanting_weight == 0.0


def test_functional_motivation_can_reach_active_desire_reference() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-INTIMATE-MOTIVATION",
        "SESSION-INTIMATE-MOTIVATION",
    )
    body = state_loop.build_teacher_reference_baseline_state(binding)
    controller = state_loop.build_teacher_reference_controller_state(binding, body)
    previous_phase = None
    frame = None

    for _ in range(12):
        frame = state_loop.advance_teacher_embodied_tick(
            binding,
            previous_controller_state=controller,
            previous_body_state=body,
            stimulus=_high_stimulus(motivation=0.95),
            previous_phase_state=previous_phase,
        )
        body = frame.body_state
        controller = replace(
            frame.controller_state,
            previous_body_schema_feedback_sha256=(
                frame.body_schema_feedback_sha256
            ),
        )
        previous_phase = frame.high_salience_phase_state
        if frame.intimate_integration_state.functional_desire.phase == "ACTIVE":
            break

    assert frame is not None
    assert frame.intimate_integration_state.functional_desire.phase == "ACTIVE"
    assert frame.intimate_integration_state.functional_desire.functional_motivation >= 0.55
    assert (
        frame.intimate_integration_state.functional_desire.threshold_calibration_status
        == "SOFTWARE_REFERENCE_NOT_BIOLOGICAL_CONSTANT"
    )
    assert (
        frame.intimate_integration_state.functional_desire.phenomenal_desire_status
        == "NOT_ESTABLISHED"
    )


def test_orgasm_reference_does_not_force_ejaculation() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-ORGASM-NO-EJACULATION",
        "SESSION-ORGASM-NO-EJACULATION",
    )
    body = state_loop.build_teacher_reference_baseline_state(binding)
    controller = state_loop.build_teacher_reference_controller_state(binding, body)

    frame = state_loop.advance_teacher_embodied_tick(
        binding,
        previous_controller_state=controller,
        previous_body_state=body,
        stimulus=_high_stimulus(motivation=0.0),
        orgasm_reference_gate=TeacherOrgasmReferenceGate(
            event="ORGASM_REFERENCE_REQUEST"
        ),
    )

    integrated = frame.intimate_integration_state
    assert integrated.orgasm_reference.active is True
    assert integrated.orgasm_reference.ejaculation_required is False
    assert integrated.orgasm_reference.ejaculation_effect == "NONE"
    assert integrated.orgasm_reference.coincident_ejaculatory_reference is False
    measured = dict(integrated.measured_reference_channels)
    assert measured["EJACULATORY_REFLEX_STATE"] == 0.0
    assert measured["EXPULSION_MOTOR_PATTERN_STATE"] == 0.0


def test_ejaculatory_reference_does_not_infer_orgasm() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-EJACULATION-NO-ORGASM",
        "SESSION-EJACULATION-NO-ORGASM",
    )
    body = state_loop.build_teacher_reference_baseline_state(binding)
    body = _replace_scalar(body, "EJACULATORY_REFLEX_STATE", 0.80)
    body = _replace_scalar(body, "EXPULSION_MOTOR_PATTERN_STATE", 0.80)
    controller = state_loop.build_teacher_reference_controller_state(binding, body)
    phase = state_loop.build_teacher_high_salience_baseline_phase(body)
    motivation = state_loop.build_teacher_controller_motivation(controller, body)

    integrated = integrate_teacher_intimate_reference(
        controller,
        motivation,
        phase,
        body,
    )

    assert integrated.orgasm_reference.active is False
    assert integrated.orgasm_reference.coincident_ejaculatory_reference is True
    assert integrated.orgasm_reference.subjective_orgasm_status == "NOT_ESTABLISHED"


def test_systemic_channels_are_observed_without_forcing_or_fake_calibration() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-SYSTEMIC-OBSERVE",
        "SESSION-SYSTEMIC-OBSERVE",
    )
    body = state_loop.build_teacher_reference_baseline_state(binding)
    controller = state_loop.build_teacher_reference_controller_state(binding, body)
    phase = state_loop.build_teacher_high_salience_baseline_phase(body)
    motivation = state_loop.build_teacher_controller_motivation(controller, body)

    integrated = integrate_teacher_intimate_reference(
        controller,
        motivation,
        phase,
        body,
    )

    systemic = integrated.systemic_arousal
    assert systemic.cardiovascular_state == 0.20
    assert systemic.respiratory_state == 0.20
    assert systemic.sympathetic_state == 0.20
    assert systemic.parasympathetic_state == 0.70
    assert systemic.observation_policy == "OBSERVE_NOT_FORCE"
    assert systemic.calibration_status == "SOFTWARE_REFERENCE_NOT_BIOLOGICAL_CONSTANT"


def test_orgasm_reference_opens_slow_endocrine_observation_without_concentration_claim() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-POST-CLIMACTIC-ENDOCRINE",
        "SESSION-POST-CLIMACTIC-ENDOCRINE",
    )
    body = state_loop.build_teacher_reference_baseline_state(binding)
    controller = state_loop.build_teacher_reference_controller_state(binding, body)
    phase = state_loop.build_teacher_high_salience_baseline_phase(body)
    motivation = state_loop.build_teacher_controller_motivation(controller, body)

    integrated = integrate_teacher_intimate_reference(
        controller,
        motivation,
        phase,
        body,
        orgasm_reference_gate=TeacherOrgasmReferenceGate(
            event="ORGASM_REFERENCE_REQUEST"
        ),
    )

    endocrine = integrated.endocrine_observation
    assert endocrine.phase == "POST_CLIMACTIC_SLOW_OBSERVATION"
    assert endocrine.cadence_class == "SLOW_OBSERVATION_ONLY"
    assert endocrine.concentration_status == "UNKNOWN_NOT_SYNTHESIZED"
    assert endocrine.prolactin_runtime_mapping == "ABSENT"
    assert endocrine.acute_gonadal_auto_drive == "ABSENT"


def test_orgasm_gate_preserves_consent_pleasure_and_subjectivity_boundaries() -> None:
    gate = TeacherOrgasmReferenceGate(event="ORGASM_REFERENCE_REQUEST")

    assert gate.consent_inference == "FORBIDDEN"
    assert gate.subjective_orgasm_status == "NOT_ESTABLISHED"
    assert gate.phenomenal_pleasure_status == "NOT_ESTABLISHED"
    assert gate.subjectivity_status == "NOT_ESTABLISHED"
    assert gate.action_authority == "NONE"


def test_package_exports_intimate_integration_public_surface() -> None:
    import aion_astra_twin_embodiment as package

    assert package.TeacherOrgasmReferenceGate is TeacherOrgasmReferenceGate
    assert package.TeacherIntimateIntegrationState is not None
    assert callable(package.integrate_teacher_intimate_reference)
