from __future__ import annotations

from dataclasses import replace
import importlib
from math import isfinite

import pytest

from aion_astra_twin_embodiment.teacher_body_dynamics import (
    TeacherBodyObservation,
    build_teacher_body_dynamics_profile,
    integrate_teacher_body_state,
)
from aion_astra_twin_embodiment.teacher_embodied_controller import (
    TeacherEmbodiedControllerState,
    TeacherEmbodimentClock,
    build_teacher_controller_motivation,
)


def _executor_module():
    return importlib.import_module(
        "aion_astra_twin_embodiment.teacher_transition_executor"
    )


def _body_state(
    *,
    sequence: int = 0,
    timestamp_ms: int = 0,
    genital_vascular: float = 0.10,
    erectile_reflex: float = 0.10,
    include_erectile_reflex: bool = True,
):
    observations = [
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
        TeacherBodyObservation("CARDIOVASCULAR_STATE", (0.30,), timestamp_ms),
        TeacherBodyObservation(
            "GENITAL_SENSORY_AFFERENT_REFERENCE",
            (genital_vascular,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "GENITAL_VASCULAR_STATE",
            (genital_vascular,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "PELVIC_FLOOR_PROPRIOCEPTION",
            (0.10,),
            timestamp_ms,
        ),
        TeacherBodyObservation("DETUMESCENCE_STATE", (0.0,), timestamp_ms),
        TeacherBodyObservation(
            "GONADAL_ENDOCRINE_REFERENCE",
            (0.20,),
            timestamp_ms,
        ),
        TeacherBodyObservation("EMISSION_REFLEX_STATE", (0.0,), timestamp_ms),
        TeacherBodyObservation(
            "EJACULATORY_REFLEX_STATE",
            (0.0,),
            timestamp_ms,
        ),
    ]
    if include_erectile_reflex:
        observations.append(
            TeacherBodyObservation(
                "ERECTILE_REFLEX_STATE",
                (erectile_reflex,),
                timestamp_ms,
            )
        )
    return integrate_teacher_body_state(observations, sequence=sequence)


def _controller(
    body_state,
    *,
    activation: float,
    phase: str,
    motivation: float = 0.0,
):
    return TeacherEmbodiedControllerState(
        controller_id="CHATGPT_TEACHER_EMBODIED_CONTROLLER_v0.1",
        runtime_id="RUNTIME-EXECUTOR",
        session_id="SESSION-EXECUTOR",
        body_id="CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1",
        sequence=body_state.sequence,
        timestamp_ms=body_state.timestamp_ms,
        salience=activation,
        activation=activation,
        functional_motivation=motivation,
        inhibition=0.0,
        context_gate=activation > 0.0,
        phase=phase,
        source_body_state_sha256=body_state.body_state_sha256,
        previous_body_schema_feedback_sha256=None,
    )


def _channel_map(observations) -> dict[str, tuple[float, ...]]:
    return {item.channel_id: item.values for item in observations}


def test_executor_uses_transition_records_from_existing_profile() -> None:
    module = _executor_module()
    profile = build_teacher_body_dynamics_profile()
    body = _body_state()
    controller = _controller(
        body,
        activation=0.85,
        phase="HIGH_ACTIVATION_REFERENCE",
    )

    intent = module.select_teacher_transition_intent(controller, body, profile)
    profile_ids = {item.transition_id for item in profile.physiological_transitions}

    assert intent.mode == "ACTIVATION"
    assert intent.transition_ids == ("SEXUAL_BASELINE_TO_VASCULAR_RESPONSE",)
    assert set(intent.transition_ids).issubset(profile_ids)
    assert "MAINTENANCE_TO_EMISSION" not in intent.transition_ids
    assert "EMISSION_TO_EJACULATORY_REFLEX" not in intent.transition_ids


def test_recovery_uses_explicit_profile_path_without_forcing_ejaculation() -> None:
    module = _executor_module()
    profile = build_teacher_body_dynamics_profile()
    body = _body_state(genital_vascular=0.80, erectile_reflex=0.75)
    controller = _controller(
        body,
        activation=0.20,
        phase="BASELINE_REFERENCE",
    )

    intent = module.select_teacher_transition_intent(controller, body, profile)
    profile_ids = {item.transition_id for item in profile.physiological_transitions}

    assert intent.mode == "RECOVERY"
    assert intent.transition_ids == ("VASCULAR_RESPONSE_TO_BASELINE_RECOVERY",)
    assert set(intent.transition_ids).issubset(profile_ids)
    assert "MAINTENANCE_TO_EMISSION" not in intent.transition_ids
    assert "EMISSION_TO_EJACULATORY_REFLEX" not in intent.transition_ids


def test_invalid_transition_id_fails_closed() -> None:
    module = _executor_module()
    body = _body_state()
    controller = _controller(
        body,
        activation=0.80,
        phase="HIGH_ACTIVATION_REFERENCE",
    )
    motivation = build_teacher_controller_motivation(controller, body)
    intent = module.TeacherTransitionIntent(
        transition_ids=("NOT_A_TRANSITION",),
        mode="ACTIVATION",
    )

    with pytest.raises(ValueError, match="unknown physiological transition"):
        module.execute_teacher_transition(
            body,
            controller,
            motivation,
            intent,
            TeacherEmbodimentClock(sequence=1, timestamp_ms=100),
        )


def test_executor_updates_only_transition_channels_and_carries_other_observations() -> None:
    module = _executor_module()
    body = _body_state(genital_vascular=0.10, erectile_reflex=0.10)
    controller = _controller(
        body,
        activation=0.85,
        phase="HIGH_ACTIVATION_REFERENCE",
    )
    motivation = build_teacher_controller_motivation(controller, body)
    intent = module.TeacherTransitionIntent(
        transition_ids=("SEXUAL_BASELINE_TO_VASCULAR_RESPONSE",),
        mode="ACTIVATION",
    )

    executed = module.execute_teacher_transition(
        body,
        controller,
        motivation,
        intent,
        TeacherEmbodimentClock(sequence=1, timestamp_ms=100),
    )
    before = _channel_map(body.observations)
    after = _channel_map(executed.observations)

    assert set(executed.touched_channel_ids) == {
        "GENITAL_SENSORY_AFFERENT_REFERENCE",
        "GENITAL_VASCULAR_STATE",
        "ERECTILE_REFLEX_STATE",
    }
    assert after["CARDIOVASCULAR_STATE"] == before["CARDIOVASCULAR_STATE"]
    assert after["GENITAL_VASCULAR_STATE"][0] > before["GENITAL_VASCULAR_STATE"][0]
    assert after["ERECTILE_REFLEX_STATE"][0] > before["ERECTILE_REFLEX_STATE"][0]


def test_missing_required_transition_channel_is_unknown_not_zero() -> None:
    module = _executor_module()
    body = _body_state(include_erectile_reflex=False)
    controller = _controller(
        body,
        activation=0.85,
        phase="HIGH_ACTIVATION_REFERENCE",
    )
    motivation = build_teacher_controller_motivation(controller, body)
    intent = module.TeacherTransitionIntent(
        transition_ids=("SEXUAL_BASELINE_TO_VASCULAR_RESPONSE",),
        mode="ACTIVATION",
    )

    with pytest.raises(ValueError, match="missing required transition channel"):
        module.execute_teacher_transition(
            body,
            controller,
            motivation,
            intent,
            TeacherEmbodimentClock(sequence=1, timestamp_ms=100),
        )


def test_transition_output_is_finite_rate_limited_and_content_addressed() -> None:
    module = _executor_module()
    body = _body_state(genital_vascular=0.10, erectile_reflex=0.10)
    controller = _controller(
        body,
        activation=1.0,
        phase="HIGH_ACTIVATION_REFERENCE",
    )
    motivation = build_teacher_controller_motivation(controller, body)
    intent = module.TeacherTransitionIntent(
        transition_ids=("SEXUAL_BASELINE_TO_VASCULAR_RESPONSE",),
        mode="ACTIVATION",
    )

    executed = module.execute_teacher_transition(
        body,
        controller,
        motivation,
        intent,
        TeacherEmbodimentClock(sequence=1, timestamp_ms=100),
    )

    assert executed.sequence == 1
    assert executed.timestamp_ms == 100
    assert len(executed.transition_sha256) == 64
    assert all(
        isfinite(value) and 0.0 <= value <= 1.0
        for observation in executed.observations
        for value in observation.values
    )
    before = _channel_map(body.observations)
    after = _channel_map(executed.observations)
    assert (
        after["GENITAL_VASCULAR_STATE"][0]
        - before["GENITAL_VASCULAR_STATE"][0]
        <= 0.12 + 1e-12
    )


def test_recovery_is_state_evolution_not_terminal_fraction_override() -> None:
    module = _executor_module()
    body = _body_state(genital_vascular=0.90, erectile_reflex=0.85)
    initial = _channel_map(body.observations)["GENITAL_VASCULAR_STATE"][0]
    previous = body
    values: list[float] = []

    for sequence in range(1, 21):
        controller = _controller(
            previous,
            activation=0.0,
            phase="BASELINE_REFERENCE",
        )
        motivation = build_teacher_controller_motivation(controller, previous)
        executed = module.execute_teacher_transition(
            previous,
            controller,
            motivation,
            module.TeacherTransitionIntent(
                transition_ids=("VASCULAR_RESPONSE_TO_BASELINE_RECOVERY",),
                mode="RECOVERY",
            ),
            TeacherEmbodimentClock(
                sequence=sequence,
                timestamp_ms=sequence * 100,
            ),
        )
        values.append(
            _channel_map(executed.observations)["GENITAL_VASCULAR_STATE"][0]
        )
        previous = integrate_teacher_body_state(
            executed.observations,
            sequence=sequence,
        )

    assert "recovery_fraction" not in module.execute_teacher_transition.__annotations__
    assert values[0] < initial
    assert all(next_value <= value for value, next_value in zip(values, values[1:]))
    assert values[-1] < 0.10


def test_executor_rejects_future_or_reused_clock_sequence() -> None:
    module = _executor_module()
    body = _body_state(sequence=2, timestamp_ms=200)
    controller = _controller(
        body,
        activation=0.8,
        phase="HIGH_ACTIVATION_REFERENCE",
    )
    motivation = build_teacher_controller_motivation(controller, body)
    intent = module.TeacherTransitionIntent(
        transition_ids=("SEXUAL_BASELINE_TO_VASCULAR_RESPONSE",),
        mode="ACTIVATION",
    )

    with pytest.raises(ValueError, match="exactly one tick"):
        module.execute_teacher_transition(
            body,
            controller,
            motivation,
            intent,
            TeacherEmbodimentClock(sequence=2, timestamp_ms=200),
        )

    future_controller = replace(controller, sequence=4, timestamp_ms=400)
    with pytest.raises(ValueError, match="controller/body sequence"):
        module.execute_teacher_transition(
            body,
            future_controller,
            build_teacher_controller_motivation(
                replace(
                    future_controller,
                    source_body_state_sha256=body.body_state_sha256,
                ),
                body,
            ),
            intent,
            TeacherEmbodimentClock(sequence=3, timestamp_ms=300),
        )
