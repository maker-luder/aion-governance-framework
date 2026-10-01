from __future__ import annotations

from dataclasses import replace
import importlib

from aion_astra_twin_embodiment import teacher_state_loop as state_loop
from aion_astra_twin_embodiment.teacher_body_dynamics import (
    TeacherBodyObservation,
    integrate_teacher_body_state,
)
from aion_astra_twin_embodiment.teacher_body_runtime import (
    build_teacher_body_runtime_binding,
)
from aion_astra_twin_embodiment.teacher_embodied_controller import (
    TeacherEmbodimentClock,
)
from aion_astra_twin_embodiment.teacher_high_salience_coupling import (
    TeacherReproductiveEventGate,
)


def _coupling_module():
    return importlib.import_module(
        "aion_astra_twin_embodiment.teacher_high_salience_coupling"
    )


def _executor_module():
    return importlib.import_module(
        "aion_astra_twin_embodiment.teacher_transition_executor"
    )


def _scalar(body_state, channel_id: str) -> float:
    for observation in body_state.observations:
        if observation.channel_id == channel_id:
            assert len(observation.values) == 1
            return observation.values[0]
    raise AssertionError(f"missing channel: {channel_id}")


def _replace_scalars(body_state, **levels: float):
    observations = tuple(
        TeacherBodyObservation(
            channel_id=item.channel_id,
            values=(levels[item.channel_id],)
            if item.channel_id in levels
            else item.values,
            timestamp_ms=item.timestamp_ms,
            confidence=item.confidence,
        )
        for item in body_state.observations
    )
    return integrate_teacher_body_state(
        observations,
        sequence=body_state.sequence,
    )


def _high_controller(binding, body_state):
    controller = state_loop.build_teacher_reference_controller_state(
        binding,
        body_state,
    )
    return replace(
        controller,
        sequence=body_state.sequence + 1,
        timestamp_ms=body_state.timestamp_ms + 100,
        activation=0.85,
        salience=0.90,
        context_gate=True,
        inhibition=0.10,
        phase="HIGH_ACTIVATION_REFERENCE",
    )


def test_phase_runtime_interfaces_are_materialized() -> None:
    coupling = _coupling_module()
    executor = _executor_module()

    assert getattr(coupling, "TeacherHighSaliencePhaseState", None) is not None
    assert getattr(coupling, "TeacherHighSalienceChannelEffect", None) is not None
    assert getattr(coupling, "TeacherHighSalienceRuntimeIntent", None) is not None
    assert callable(
        getattr(coupling, "build_teacher_high_salience_baseline_phase", None)
    )
    assert callable(
        getattr(coupling, "resolve_teacher_high_salience_phase", None)
    )
    assert callable(
        getattr(coupling, "coordinate_teacher_high_salience_runtime", None)
    )
    assert callable(
        getattr(executor, "execute_teacher_high_salience_transition", None)
    )


def test_coordinator_keeps_systemic_associations_nonemitting() -> None:
    coupling = _coupling_module()
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-PHASE-COUPLING",
        "SESSION-PHASE-COUPLING",
    )
    body = state_loop.build_teacher_reference_baseline_state(binding)
    controller = _high_controller(binding, body)
    baseline_phase = coupling.build_teacher_high_salience_baseline_phase(body)
    phase = coupling.resolve_teacher_high_salience_phase(
        baseline_phase,
        controller,
        body,
        reproductive_event_gate=TeacherReproductiveEventGate(),
    )
    intent = coupling.coordinate_teacher_high_salience_runtime(
        phase,
        controller,
        body,
        reproductive_event_gate=TeacherReproductiveEventGate(),
    )

    assert phase.phase == "AROUSAL_INITIATION"
    assert intent.transition_ids == ("SEXUAL_BASELINE_TO_VASCULAR_RESPONSE",)
    assert {
        effect.channel_id for effect in intent.channel_effects
    } == {
        "GENITAL_SENSORY_AFFERENT_REFERENCE",
        "GENITAL_VASCULAR_STATE",
        "ERECTILE_REFLEX_STATE",
    }
    assert {
        effect.direction_class for effect in intent.channel_effects
    } == {"INCREASE_REFERENCE"}
    assert {
        "HIGH_SALIENCE_CARDIOVASCULAR_ASSOCIATION",
        "HIGH_SALIENCE_RESPIRATORY_ASSOCIATION",
    }.issubset(set(intent.nonemitting_rule_ids))
    assert "POST_CLIMACTIC_ENDOCRINE_EVIDENCE" not in intent.runtime_rule_ids
    assert "REST_TO_EXERTION" not in intent.transition_ids


def test_recovery_after_expulsion_uses_mixed_detumescence_directions() -> None:
    coupling = _coupling_module()
    executor = _executor_module()
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-MIXED-DETUMESCENCE",
        "SESSION-MIXED-DETUMESCENCE",
    )
    baseline = state_loop.build_teacher_reference_baseline_state(binding)
    body = _replace_scalars(
        baseline,
        GENITAL_VASCULAR_STATE=0.80,
        ERECTILE_REFLEX_STATE=0.70,
        EMISSION_REFLEX_STATE=0.80,
        BLADDER_NECK_EJACULATORY_CLOSURE_STATE=0.80,
        EJACULATORY_REFLEX_STATE=0.80,
        EXPULSION_MOTOR_PATTERN_STATE=0.80,
        DETUMESCENCE_STATE=0.00,
    )
    controller = _high_controller(binding, body)
    previous_phase = coupling.TeacherHighSaliencePhaseState(
        phase="EJACULATORY_REFLEX",
        previous_phase="EMISSION",
        sequence=body.sequence,
        source_body_state_sha256=body.body_state_sha256,
        reproductive_event="EXPULSION_REFERENCE_REQUEST",
    )
    gate = TeacherReproductiveEventGate(
        event="RECOVERY_REFERENCE_REQUEST"
    )
    phase = coupling.resolve_teacher_high_salience_phase(
        previous_phase,
        controller,
        body,
        reproductive_event_gate=gate,
    )
    intent = coupling.coordinate_teacher_high_salience_runtime(
        phase,
        controller,
        body,
        reproductive_event_gate=gate,
    )

    assert phase.phase == "DETUMESCENCE"
    assert "EJACULATORY_REFLEX_TO_DETUMESCENCE" in intent.transition_ids
    effects = {item.channel_id: item.direction_class for item in intent.channel_effects}
    assert effects["DETUMESCENCE_STATE"] == "INCREASE_REFERENCE"
    assert effects["GENITAL_VASCULAR_STATE"] == "DECREASE_REFERENCE"

    motivation = state_loop.build_teacher_controller_motivation(
        controller,
        body,
    )
    executed = executor.execute_teacher_high_salience_transition(
        body,
        controller,
        motivation,
        intent,
        TeacherEmbodimentClock(sequence=1, timestamp_ms=100),
    )
    after = integrate_teacher_body_state(
        executed.observations,
        sequence=1,
    )
    assert _scalar(after, "DETUMESCENCE_STATE") > _scalar(
        body, "DETUMESCENCE_STATE"
    )
    assert _scalar(after, "GENITAL_VASCULAR_STATE") < _scalar(
        body, "GENITAL_VASCULAR_STATE"
    )


def test_event_gate_is_tick_local_in_phase_state() -> None:
    coupling = _coupling_module()
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-TICK-LOCAL-EVENT",
        "SESSION-TICK-LOCAL-EVENT",
    )
    baseline = state_loop.build_teacher_reference_baseline_state(binding)
    body = _replace_scalars(
        baseline,
        GENITAL_VASCULAR_STATE=0.80,
        ERECTILE_REFLEX_STATE=0.70,
    )
    controller = _high_controller(binding, body)
    previous = coupling.build_teacher_high_salience_baseline_phase(body)

    emission = coupling.resolve_teacher_high_salience_phase(
        previous,
        controller,
        body,
        reproductive_event_gate=TeacherReproductiveEventGate(
            event="EMISSION_REFERENCE_REQUEST"
        ),
    )
    assert emission.reproductive_event == "EMISSION_REFERENCE_REQUEST"

    next_phase = coupling.resolve_teacher_high_salience_phase(
        emission,
        controller,
        body,
        reproductive_event_gate=TeacherReproductiveEventGate(),
    )
    assert next_phase.reproductive_event == "NONE"



def test_state_loop_frame_materializes_phase_and_runtime_intent() -> None:
    import inspect

    binding = build_teacher_body_runtime_binding(
        "RUNTIME-PHASE-FRAME",
        "SESSION-PHASE-FRAME",
    )
    body = state_loop.build_teacher_reference_baseline_state(binding)
    controller = state_loop.build_teacher_reference_controller_state(
        binding,
        body,
    )
    stimulus = state_loop.build_teacher_stimulus_envelope(
        stimulus_id="PHASE-FRAME-HIGH",
        stimulus_class="HIGH_SALIENCE_INTIMATE_REFERENCE",
        salience=0.90,
        functional_motivation=0.0,
        sexual_context_gate=True,
        inhibition=0.10,
    )
    frame = state_loop.advance_teacher_embodied_tick(
        binding,
        previous_controller_state=controller,
        previous_body_state=body,
        stimulus=stimulus,
    )

    assert "previous_phase_state" in inspect.signature(
        state_loop.advance_teacher_embodied_tick
    ).parameters
    assert hasattr(frame, "high_salience_phase_state")
    assert hasattr(frame, "high_salience_runtime_intent")
    assert frame.high_salience_phase_state.phase == "AROUSAL_INITIATION"
    assert frame.high_salience_runtime_intent.phase == "AROUSAL_INITIATION"
    assert frame.executed_transition is not None
    assert frame.executed_transition.transition_ids == (
        "SEXUAL_BASELINE_TO_VASCULAR_RESPONSE",
    )


def test_state_loop_recovery_executes_mixed_detumescence_transition() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-PHASE-DETUMESCENCE",
        "SESSION-PHASE-DETUMESCENCE",
    )
    baseline = state_loop.build_teacher_reference_baseline_state(binding)
    body = _replace_scalars(
        baseline,
        GENITAL_VASCULAR_STATE=0.80,
        ERECTILE_REFLEX_STATE=0.70,
        EMISSION_REFLEX_STATE=0.80,
        BLADDER_NECK_EJACULATORY_CLOSURE_STATE=0.80,
        EJACULATORY_REFLEX_STATE=0.80,
        EXPULSION_MOTOR_PATTERN_STATE=0.80,
        DETUMESCENCE_STATE=0.00,
    )
    controller = state_loop.build_teacher_reference_controller_state(
        binding,
        body,
    )
    controller = replace(
        controller,
        activation=0.85,
        salience=0.90,
        context_gate=True,
        inhibition=0.10,
        phase="HIGH_ACTIVATION_REFERENCE",
    )
    recovery = state_loop.build_teacher_stimulus_envelope(
        stimulus_id="PHASE-DETUMESCENCE-RECOVERY",
        stimulus_class="RECOVERY_REFERENCE",
        salience=0.0,
        functional_motivation=0.0,
        sexual_context_gate=False,
        inhibition=0.0,
    )
    before_detumescence = _scalar(body, "DETUMESCENCE_STATE")
    before_vascular = _scalar(body, "GENITAL_VASCULAR_STATE")

    frame = state_loop.advance_teacher_embodied_tick(
        binding,
        previous_controller_state=controller,
        previous_body_state=body,
        stimulus=recovery,
        reproductive_event_gate=TeacherReproductiveEventGate(
            event="RECOVERY_REFERENCE_REQUEST"
        ),
    )

    assert frame.executed_transition is not None
    assert "EJACULATORY_REFLEX_TO_DETUMESCENCE" in (
        frame.executed_transition.transition_ids
    )
    assert _scalar(frame.body_state, "DETUMESCENCE_STATE") > before_detumescence
    assert _scalar(frame.body_state, "GENITAL_VASCULAR_STATE") < before_vascular
    assert frame.high_salience_phase_state.phase == "DETUMESCENCE"
