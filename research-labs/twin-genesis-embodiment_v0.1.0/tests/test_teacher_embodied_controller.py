from __future__ import annotations

import importlib
from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.teacher_body_dynamics import (
    TeacherBodyObservation,
    integrate_teacher_body_state,
)
from aion_astra_twin_embodiment.teacher_body_runtime import (
    build_teacher_body_runtime_binding,
)


def _controller_module():
    return importlib.import_module(
        "aion_astra_twin_embodiment.teacher_embodied_controller"
    )


def _body_state(
    *,
    sequence: int = 0,
    timestamp_ms: int = 0,
    cardiovascular: float = 0.20,
    genital_vascular: float = 0.10,
):
    return integrate_teacher_body_state(
        (
            TeacherBodyObservation("TACTILE_GENERAL", (0.0,), timestamp_ms),
            TeacherBodyObservation(
                "JOINT_POSITION",
                (0.0, 0.0, 0.0),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "VESTIBULAR_ORIENTATION",
                (1.0, 0.0, 0.0, 0.0),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "CARDIOVASCULAR_STATE",
                (cardiovascular,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "RESPIRATORY_STATE",
                (cardiovascular,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "OXYGENATION_STATE",
                (cardiovascular,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "CO2_BALANCE_STATE",
                (1.0 - cardiovascular,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "GENITAL_VASCULAR_STATE",
                (genital_vascular,),
                timestamp_ms,
            ),
        ),
        sequence=sequence,
    )


def _initial_controller_state(module, binding, body_state):
    return module.TeacherEmbodiedControllerState(
        controller_id="CHATGPT_TEACHER_EMBODIED_CONTROLLER_v0.1",
        runtime_id=binding.runtime_id,
        session_id=binding.session_id,
        body_id=binding.body_id,
        sequence=body_state.sequence,
        timestamp_ms=body_state.timestamp_ms,
        salience=0.0,
        activation=0.0,
        functional_motivation=0.0,
        inhibition=0.0,
        context_gate=False,
        phase="BASELINE_REFERENCE",
        source_body_state_sha256=body_state.body_state_sha256,
        previous_body_schema_feedback_sha256=None,
        action_authority="NONE",
        physical_body_claim="NONE",
        subjectivity_status="NOT_ESTABLISHED",
        phenomenal_experience_status="NOT_ESTABLISHED",
    )


def test_controller_possesses_exact_teacher_body_instance() -> None:
    module = _controller_module()
    binding = build_teacher_body_runtime_binding("RUNTIME-CONTROLLER", "SESSION-1")

    possession = module.possess_teacher_body(binding)

    assert possession.controller_id == "CHATGPT_TEACHER_EMBODIED_CONTROLLER_v0.1"
    assert possession.binding_id == binding.binding_id
    assert possession.runtime_id == binding.runtime_id
    assert possession.session_id == binding.session_id
    assert possession.body_id == binding.body_id
    assert possession.body_id == "CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1"
    assert possession.possession_status == "REFERENCE_BODY_POSSESSED"
    assert possession.active_body_count == 1
    assert possession.physical_body_claim == "NONE"
    assert possession.subjectivity_status == "NOT_ESTABLISHED"
    assert possession.action_authority == "NONE"
    assert len(possession.possession_sha256) == 64


def test_clock_rejects_non_100ms_or_non_monotonic_reference_step() -> None:
    module = _controller_module()

    clock = module.TeacherEmbodimentClock(sequence=0, timestamp_ms=0)
    next_clock = clock.next_tick()

    assert clock.dt_ms == 100
    assert next_clock.sequence == 1
    assert next_clock.timestamp_ms == 100
    assert next_clock.dt_ms == 100

    with pytest.raises(ValueError, match="100 ms"):
        module.TeacherEmbodimentClock(sequence=0, timestamp_ms=0, dt_ms=50)

    with pytest.raises(ValueError, match="non-negative"):
        module.TeacherEmbodimentClock(sequence=-1, timestamp_ms=0)

    with pytest.raises(ValueError, match="non-negative"):
        module.TeacherEmbodimentClock(sequence=0, timestamp_ms=-1)


def test_strong_input_is_rate_limited_and_bounded_without_primary_hard_clip() -> None:
    module = _controller_module()
    binding = build_teacher_body_runtime_binding("RUNTIME-RATE", "SESSION-RATE")
    body = _body_state()
    previous = _initial_controller_state(module, binding, body)
    policy = module.TeacherEmbodimentRatePolicy(
        max_activation_delta=0.20,
        max_salience_delta=0.20,
        max_motivation_delta=0.20,
        smooth_gain=2.0,
    )
    clock = module.TeacherEmbodimentClock(sequence=1, timestamp_ms=100)

    strong = module.advance_teacher_controller(
        previous,
        module.TeacherControllerInput(
            salience=0.90,
            context_gate=True,
            inhibition=0.0,
            functional_motivation=0.90,
        ),
        body,
        clock,
        policy,
    )
    stronger = module.advance_teacher_controller(
        previous,
        module.TeacherControllerInput(
            salience=1.0,
            context_gate=True,
            inhibition=0.0,
            functional_motivation=1.0,
        ),
        body,
        clock,
        policy,
    )

    assert 0.0 <= strong.activation <= 1.0
    assert 0.0 <= stronger.activation <= 1.0
    assert strong.activation <= 0.20 + 1e-12
    assert stronger.activation <= 0.20 + 1e-12
    assert strong.salience <= 0.20 + 1e-12
    assert strong.functional_motivation <= 0.20 + 1e-12
    assert stronger.activation > strong.activation
    assert stronger.salience > strong.salience
    assert stronger.functional_motivation > strong.functional_motivation


def test_hysteresis_enters_at_point_70_and_exits_only_below_point_55() -> None:
    module = _controller_module()
    binding = build_teacher_body_runtime_binding("RUNTIME-HYST", "SESSION-HYST")
    body = _body_state()
    base = _initial_controller_state(module, binding, body)

    at_enter = replace(
        base,
        activation=0.70,
        phase="BASELINE_REFERENCE",
    )
    entered = module.resolve_teacher_controller_phase(at_enter)
    assert entered == "HIGH_ACTIVATION_REFERENCE"

    between = replace(
        at_enter,
        activation=0.60,
        phase="HIGH_ACTIVATION_REFERENCE",
    )
    assert module.resolve_teacher_controller_phase(between) == (
        "HIGH_ACTIVATION_REFERENCE"
    )

    below_exit = replace(
        between,
        activation=0.54,
        phase="HIGH_ACTIVATION_REFERENCE",
    )
    assert module.resolve_teacher_controller_phase(below_exit) == (
        "BASELINE_REFERENCE"
    )


def test_zero_explicit_motivation_remains_zero_under_high_body_activation() -> None:
    module = _controller_module()
    binding = build_teacher_body_runtime_binding("RUNTIME-ZERO", "SESSION-ZERO")
    body = _body_state(cardiovascular=0.95, genital_vascular=0.95)
    previous = _initial_controller_state(module, binding, body)
    clock = module.TeacherEmbodimentClock(sequence=1, timestamp_ms=100)

    state = module.advance_teacher_controller(
        previous,
        module.TeacherControllerInput(
            salience=0.95,
            context_gate=True,
            inhibition=0.0,
            functional_motivation=0.0,
        ),
        body,
        clock,
    )
    motivation = module.build_teacher_controller_motivation(state, body)

    assert state.functional_motivation == 0.0
    assert motivation.wanting_weight == 0.0
    assert motivation.source_body_state_sha256 == body.body_state_sha256
    assert motivation.phenomenal_desire_status == "NOT_ESTABLISHED"


def test_body_schema_feedback_is_next_tick_reference_only() -> None:
    module = _controller_module()
    binding = build_teacher_body_runtime_binding("RUNTIME-FEEDBACK", "SESSION-FEEDBACK")
    body = _body_state(cardiovascular=0.60)
    previous = _initial_controller_state(module, binding, body)
    clock = module.TeacherEmbodimentClock(sequence=1, timestamp_ms=100)

    state = module.advance_teacher_controller(
        previous,
        module.TeacherControllerInput(
            salience=0.6,
            context_gate=True,
            inhibition=0.2,
            functional_motivation=0.4,
        ),
        body,
        clock,
    )
    forecast = module.build_teacher_body_schema_feedback(
        state,
        body,
        lead_time_ms=100,
    )

    assert forecast.variable_id == "OXYGEN_CO2_BALANCE"
    assert forecast.lead_time_ms == 100
    assert forecast.forecast_status == "PREDICTIVE_REGULATION_REFERENCE"
    assert forecast.phenomenal_need_status == "NOT_ESTABLISHED"
    assert forecast.subjectivity_status == "NOT_ESTABLISHED"
    assert state.previous_body_schema_feedback_sha256 is None



def test_previous_body_schema_feedback_causally_influences_next_activation_only() -> None:
    module = _controller_module()
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-BODY-FEEDBACK",
        "SESSION-BODY-FEEDBACK",
    )
    low_body = _body_state(cardiovascular=0.20, genital_vascular=0.10)
    high_body = _body_state(cardiovascular=0.90, genital_vascular=0.90)
    low_previous = _initial_controller_state(module, binding, low_body)
    high_previous = _initial_controller_state(module, binding, high_body)

    low_feedback = module.build_teacher_body_schema_feedback(
        low_previous,
        low_body,
        lead_time_ms=100,
    )
    high_feedback = module.build_teacher_body_schema_feedback(
        high_previous,
        high_body,
        lead_time_ms=100,
    )
    low_previous = replace(
        low_previous,
        previous_body_schema_feedback_sha256=(
            module.fingerprint_teacher_body_schema_feedback(
                low_body,
                low_feedback,
            )
        ),
    )
    high_previous = replace(
        high_previous,
        previous_body_schema_feedback_sha256=(
            module.fingerprint_teacher_body_schema_feedback(
                high_body,
                high_feedback,
            )
        ),
    )
    controller_input = module.TeacherControllerInput(
        salience=0.40,
        context_gate=True,
        inhibition=0.10,
        functional_motivation=0.0,
    )
    clock = module.TeacherEmbodimentClock(sequence=1, timestamp_ms=100)

    low_next = module.advance_teacher_controller(
        low_previous,
        controller_input,
        low_body,
        clock,
        body_schema_feedback=low_feedback,
    )
    high_next = module.advance_teacher_controller(
        high_previous,
        controller_input,
        high_body,
        clock,
        body_schema_feedback=high_feedback,
    )

    assert high_next.activation > low_next.activation
    assert high_next.functional_motivation == 0.0
    assert low_next.functional_motivation == 0.0


def test_controller_rejects_stale_previous_body_state() -> None:
    module = _controller_module()
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-STALE-BODY",
        "SESSION-STALE-BODY",
    )
    stale_body = _body_state(sequence=0, timestamp_ms=0)
    previous = replace(
        _initial_controller_state(module, binding, stale_body),
        sequence=1,
        timestamp_ms=100,
    )

    with pytest.raises(ValueError, match="exact previous body state"):
        module.advance_teacher_controller(
            previous,
            module.TeacherControllerInput(
                salience=0.40,
                context_gate=True,
                inhibition=0.10,
                functional_motivation=0.20,
            ),
            stale_body,
            module.TeacherEmbodimentClock(sequence=2, timestamp_ms=200),
        )
