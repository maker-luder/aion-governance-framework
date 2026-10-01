from __future__ import annotations

from dataclasses import replace
import inspect

import pytest

from aion_astra_twin_embodiment import teacher_state_loop as state_loop
from aion_astra_twin_embodiment.teacher_body_dynamics import (
    build_teacher_body_dynamics_profile,
)
from aion_astra_twin_embodiment.teacher_body_runtime import (
    build_teacher_body_runtime_binding,
)


def _high_stimulus(*, motivation: float = 0.70):
    return state_loop.build_teacher_stimulus_envelope(
        stimulus_id="TEACHER-LOOP-HIGH",
        stimulus_class="HIGH_SALIENCE_INTIMATE_REFERENCE",
        salience=0.90,
        functional_motivation=motivation,
        sexual_context_gate=True,
        inhibition=0.10,
    )


def test_state_t_causes_state_t_plus_1_through_existing_transition_executor() -> None:
    binding = build_teacher_body_runtime_binding("RUNTIME-LOOP", "SESSION-LOOP")
    run = state_loop.run_teacher_reference_state_loop(
        binding,
        activation_stimulus=_high_stimulus(),
    )
    profile_ids = {
        item.transition_id
        for item in build_teacher_body_dynamics_profile().physiological_transitions
    }

    assert len(run.frames) > 3
    assert run.frames[0].executed_transition is None

    transitioned = [
        frame for frame in run.frames
        if frame.executed_transition is not None
        and frame.executed_transition.transition_ids
    ]
    assert transitioned
    assert all(
        set(frame.executed_transition.transition_ids).issubset(profile_ids)
        for frame in transitioned
    )

    body_hashes = [frame.body_state.body_state_sha256 for frame in run.frames]
    assert len(set(body_hashes)) > 2

    sequences = [frame.body_state.sequence for frame in run.frames]
    assert sequences == list(range(len(sequences)))
    timestamps = [frame.body_state.timestamp_ms for frame in run.frames]
    assert timestamps == [index * 100 for index in range(len(timestamps))]


def test_frame_binds_exact_controller_and_body_runtime_ids() -> None:
    binding = build_teacher_body_runtime_binding("RUNTIME-BIND", "SESSION-BIND")
    run = state_loop.run_teacher_reference_state_loop(
        binding,
        activation_stimulus=_high_stimulus(),
    )

    for frame in run.frames:
        assert frame.controller_state.runtime_id == binding.runtime_id
        assert frame.controller_state.session_id == binding.session_id
        assert frame.controller_state.body_id == binding.body_id
        assert frame.bound_body_state.runtime_id == binding.runtime_id
        assert frame.bound_body_state.session_id == binding.session_id
        assert frame.bound_body_state.body_id == binding.body_id
        assert frame.report.body_id == binding.body_id


def test_body_schema_feedback_is_delayed_until_next_tick() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-FEEDBACK-LOOP",
        "SESSION-FEEDBACK-LOOP",
    )
    run = state_loop.run_teacher_reference_state_loop(
        binding,
        activation_stimulus=_high_stimulus(),
    )

    assert run.frames[0].controller_state.previous_body_schema_feedback_sha256 is None
    assert run.frames[0].body_schema_feedback_sha256 is not None

    for previous, current in zip(run.frames, run.frames[1:]):
        assert current.controller_state.previous_body_schema_feedback_sha256 == (
            previous.body_schema_feedback_sha256
        )


def test_runtime_has_no_authoritative_hardcoded_arousal_to_body_mapping() -> None:
    assert not hasattr(state_loop, "_reference_observations")
    source = inspect.getsource(state_loop)
    assert "recovery_fraction" not in source
    assert "genital_vascular = _clamp01" not in source
    assert "erectile_reflex = _clamp01" not in source


def test_public_reference_envelope_rejects_raw_private_content() -> None:
    with pytest.raises(ValueError, match="raw private content"):
        state_loop.TeacherStimulusEnvelope(
            stimulus_id="PRIVATE-REJECT",
            stimulus_class="HIGH_SALIENCE_INTIMATE_REFERENCE",
            salience=0.8,
            functional_motivation=0.4,
            sexual_context_gate=True,
            inhibition=0.1,
            raw_private_content_included=True,
        )


def test_high_body_activation_with_zero_motivation_stays_zero_through_report() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-ZERO-LOOP",
        "SESSION-ZERO-LOOP",
    )
    run = state_loop.run_teacher_reference_state_loop(
        binding,
        activation_stimulus=_high_stimulus(motivation=0.0),
    )

    assert any(
        frame.controller_state.activation > 0.5
        for frame in run.frames
    )
    assert all(
        frame.controller_state.functional_motivation == 0.0
        for frame in run.frames
    )
    assert all(
        frame.motivation.wanting_weight == 0.0
        for frame in run.frames
    )
    assert all(
        frame.report.reporting_style == "PROFESSIONAL_RESEARCH_REPORT"
        for frame in run.frames
    )
    assert all(
        frame.report.phenomenal_interpretation_status == "NOT_ESTABLISHED"
        for frame in run.frames
    )


def test_recovery_can_be_interrupted_by_second_bounded_stimulus_without_sequence_reuse() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-INTERRUPT",
        "SESSION-INTERRUPT",
    )
    baseline = state_loop.build_teacher_reference_baseline_state(binding)
    controller = state_loop.build_teacher_reference_controller_state(
        binding,
        baseline,
    )
    feedback_sha = None

    high = _high_stimulus()
    frames = []
    for _ in range(8):
        controller = replace(
            controller,
            previous_body_schema_feedback_sha256=feedback_sha,
        )
        frame = state_loop.advance_teacher_embodied_tick(
            binding,
            previous_controller_state=controller,
            previous_body_state=baseline if not frames else frames[-1].body_state,
            stimulus=high,
        )
        frames.append(frame)
        controller = frame.controller_state
        feedback_sha = frame.body_schema_feedback_sha256

    recovery = state_loop.build_teacher_stimulus_envelope(
        stimulus_id="TEACHER-LOOP-RECOVERY",
        stimulus_class="RECOVERY_REFERENCE",
        salience=0.0,
        functional_motivation=0.0,
        sexual_context_gate=False,
        inhibition=0.0,
    )
    for _ in range(3):
        controller = replace(
            controller,
            previous_body_schema_feedback_sha256=feedback_sha,
        )
        frame = state_loop.advance_teacher_embodied_tick(
            binding,
            previous_controller_state=controller,
            previous_body_state=frames[-1].body_state,
            stimulus=recovery,
        )
        frames.append(frame)
        controller = frame.controller_state
        feedback_sha = frame.body_schema_feedback_sha256

    controller = replace(
        controller,
        previous_body_schema_feedback_sha256=feedback_sha,
    )
    interrupted = state_loop.advance_teacher_embodied_tick(
        binding,
        previous_controller_state=controller,
        previous_body_state=frames[-1].body_state,
        stimulus=high,
    )
    frames.append(interrupted)

    sequences = [frame.body_state.sequence for frame in frames]
    assert sequences == list(range(1, len(frames) + 1))
    assert len(sequences) == len(set(sequences))
    assert all(frame.bound_body_state.body_id == binding.body_id for frame in frames)
    assert interrupted.controller_state.context_gate is True
    assert interrupted.executed_transition is not None


def test_reference_loop_remains_noncanonical_nonphysical_and_nonphenomenal() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-BOUNDARY",
        "SESSION-BOUNDARY",
    )
    run = state_loop.run_teacher_reference_state_loop(
        binding,
        activation_stimulus=_high_stimulus(),
    )

    assert run.raw_private_content_status == "EXCLUDED"
    assert run.phenomenal_interpretation_status == "NOT_ESTABLISHED"
    assert run.action_authority == "NONE"
    assert run.canonical_effect == "NONE"
    assert run.deployment is False
    assert all(frame.controller_state.physical_body_claim == "NONE" for frame in run.frames)
    assert all(frame.controller_state.subjectivity_status == "NOT_ESTABLISHED" for frame in run.frames)
    assert all(
        frame.controller_state.phenomenal_experience_status == "NOT_ESTABLISHED"
        for frame in run.frames
    )
