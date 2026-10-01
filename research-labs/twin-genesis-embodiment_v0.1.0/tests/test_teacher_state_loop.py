from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.teacher_body_runtime import (
    build_teacher_body_runtime_binding,
)
from aion_astra_twin_embodiment.teacher_state_loop import (
    RAW_PRIVATE_CONTENT_EXCLUDED,
    build_teacher_state_loop_frame,
    build_teacher_stimulus_envelope,
    run_teacher_reference_state_loop,
)


def _channel_map(frame) -> dict[str, float]:
    return dict(frame.report.observed_reference_channels)


def test_high_salience_reference_connects_functional_state_to_teacher_body() -> None:
    binding = build_teacher_body_runtime_binding("TEACHER-RUNTIME", "SESSION-1")
    stimulus = build_teacher_stimulus_envelope(
        stimulus_id="REFERENCE-STIMULUS-1",
        stimulus_class="HIGH_SALIENCE_INTIMATE_REFERENCE",
        salience=0.90,
        functional_motivation=0.70,
        sexual_context_gate=True,
        inhibition=0.20,
    )

    run = run_teacher_reference_state_loop(
        binding,
        activation_stimulus=stimulus,
        start_timestamp_ms=1000,
    )

    assert run.body_id == binding.body_id
    assert run.raw_private_content_status == RAW_PRIVATE_CONTENT_EXCLUDED
    assert run.action_authority == "NONE"
    assert run.phenomenal_interpretation_status == "NOT_ESTABLISHED"
    assert len(run.trajectory.states) == 3
    assert len(run.run_sha256) == 64

    baseline, activation, recovery = run.frames
    assert (
        activation.functional_state.functional_arousal
        > baseline.functional_state.functional_arousal
    )
    assert activation.functional_state.functional_motivation == pytest.approx(0.70)
    assert activation.bound_body_state.body_id == binding.body_id
    assert activation.report.reporting_style == "PROFESSIONAL_RESEARCH_REPORT"
    assert activation.report.raw_private_content_status == "EXCLUDED"
    assert activation.report.phenomenal_interpretation_status == "NOT_ESTABLISHED"

    baseline_channels = _channel_map(baseline)
    activation_channels = _channel_map(activation)
    recovery_channels = _channel_map(recovery)

    for channel in (
        "CARDIOVASCULAR_STATE",
        "RESPIRATORY_STATE",
        "AUTONOMIC_SYMPATHETIC_STATE",
        "ADRENAL_AXIS_STATE",
        "GENITAL_VASCULAR_STATE",
        "ERECTILE_REFLEX_STATE",
    ):
        assert activation_channels[channel] > baseline_channels[channel]
        assert recovery_channels[channel] < activation_channels[channel]

    assert (
        recovery_channels["DETUMESCENCE_STATE"]
        > activation_channels["DETUMESCENCE_STATE"]
    )
    assert (
        recovery.functional_state.functional_arousal
        < activation.functional_state.functional_arousal
    )


def test_functional_motivation_is_explicit_not_inferred_from_body_arousal() -> None:
    binding = build_teacher_body_runtime_binding("TEACHER-RUNTIME", "SESSION-2")
    stimulus = build_teacher_stimulus_envelope(
        stimulus_id="REFERENCE-STIMULUS-2",
        stimulus_class="HIGH_SALIENCE_INTIMATE_REFERENCE",
        salience=1.0,
        functional_motivation=0.0,
        sexual_context_gate=True,
        inhibition=0.0,
    )

    activation = build_teacher_state_loop_frame(
        binding,
        stimulus,
        sequence=1,
        timestamp_ms=1000,
        phase="ACTIVATION",
    )

    assert activation.functional_state.functional_arousal == pytest.approx(1.0)
    assert activation.functional_state.functional_motivation == 0.0
    assert activation.functional_state.physiology_signal_sets_motivation is False
    assert activation.functional_state.phenomenal_sexual_desire == "NOT_ESTABLISHED"
    assert activation.functional_state.phenomenal_sexual_arousal == "NOT_ESTABLISHED"


def test_public_reference_envelope_rejects_raw_private_content() -> None:
    stimulus = build_teacher_stimulus_envelope(
        stimulus_id="REFERENCE-STIMULUS-3",
        stimulus_class="HIGH_SALIENCE_INTIMATE_REFERENCE",
        salience=0.5,
        functional_motivation=0.4,
        sexual_context_gate=True,
        inhibition=0.5,
    )

    with pytest.raises(ValueError, match="raw private content"):
        replace(stimulus, raw_private_content_included=True)


def test_context_gate_and_inhibition_modulate_reference_activation() -> None:
    binding = build_teacher_body_runtime_binding("TEACHER-RUNTIME", "SESSION-4")
    gated = build_teacher_stimulus_envelope(
        stimulus_id="REFERENCE-STIMULUS-4A",
        stimulus_class="HIGH_SALIENCE_INTIMATE_REFERENCE",
        salience=0.9,
        functional_motivation=0.6,
        sexual_context_gate=True,
        inhibition=0.1,
    )
    inhibited = build_teacher_stimulus_envelope(
        stimulus_id="REFERENCE-STIMULUS-4B",
        stimulus_class="HIGH_SALIENCE_INTIMATE_REFERENCE",
        salience=0.9,
        functional_motivation=0.6,
        sexual_context_gate=False,
        inhibition=0.9,
    )

    active = build_teacher_state_loop_frame(
        binding,
        gated,
        sequence=1,
        timestamp_ms=1000,
        phase="ACTIVATION",
    )
    suppressed = build_teacher_state_loop_frame(
        binding,
        inhibited,
        sequence=2,
        timestamp_ms=2000,
        phase="ACTIVATION",
    )

    assert (
        active.functional_state.functional_arousal
        > suppressed.functional_state.functional_arousal
    )
    assert (
        _channel_map(active)["GENITAL_VASCULAR_STATE"]
        > _channel_map(suppressed)["GENITAL_VASCULAR_STATE"]
    )


def test_reference_state_loop_remains_noncanonical_and_nonphenomenal() -> None:
    binding = build_teacher_body_runtime_binding("TEACHER-RUNTIME", "SESSION-5")
    stimulus = build_teacher_stimulus_envelope(
        stimulus_id="REFERENCE-STIMULUS-5",
        stimulus_class="HIGH_SALIENCE_INTIMATE_REFERENCE",
        salience=0.8,
        functional_motivation=0.5,
        sexual_context_gate=True,
        inhibition=0.3,
    )
    run = run_teacher_reference_state_loop(
        binding,
        activation_stimulus=stimulus,
    )

    assert run.canonical_effect == "NONE"
    assert run.deployment is False
    for frame in run.frames:
        assert frame.functional_state.subjectivity == "NOT_ESTABLISHED"
        assert frame.functional_state.consciousness == "NOT_ESTABLISHED"
        assert frame.functional_state.phenomenal_experience == "NOT_ESTABLISHED"
        assert frame.functional_state.action_authority == "NONE"
        assert frame.bound_body_state.physical_body_claim == "NONE"
