from __future__ import annotations

import json
from math import isfinite
import sys

from aion_astra_twin_embodiment import teacher_state_loop as state_loop
from aion_astra_twin_embodiment.teacher_body_runtime import (
    build_teacher_body_runtime_binding,
)


EXPECTED_SCENARIO_IDS = (
    "LOW_SALIENCE_CONTEXT_OFF",
    "MEDIUM_SALIENCE_CONTEXT_ON",
    "HIGH_SALIENCE_LOW_INHIBITION",
    "HIGH_SALIENCE_HIGH_INHIBITION",
    "ELEVATED_INITIAL_BODY_STATE",
    "ZERO_MOTIVATION_HIGH_PHYSIOLOGY",
    "JUST_BELOW_HIGH_ENTER_THRESHOLD",
    "REPEATED_STIMULUS_WITH_RECOVERY",
    "RECOVERY_INTERRUPTED_BY_SECOND_STIMULUS",
    "PURE_BASELINE_RECOVERY",
)


def test_reference_probe_defines_exactly_ten_deterministic_scenarios() -> None:
    scenarios = state_loop.build_teacher_reference_scenarios()

    assert tuple(item.scenario_id for item in scenarios) == EXPECTED_SCENARIO_IDS
    assert len(scenarios) == 10
    assert all(item.random_seed is None for item in scenarios)


def test_ten_scenario_probe_is_deterministic_and_boundary_preserving() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-TEN-PROBE",
        "SESSION-TEN-PROBE",
    )

    first = state_loop.run_teacher_embodiment_stability_probe(binding)
    second = state_loop.run_teacher_embodiment_stability_probe(binding)

    assert len(first) == 10
    assert len(second) == 10
    assert tuple(item.scenario_id for item in first) == EXPECTED_SCENARIO_IDS
    assert [item.scenario_sha256 for item in first] == [
        item.scenario_sha256 for item in second
    ]
    assert [item.final_state_sha256 for item in first] == [
        item.final_state_sha256 for item in second
    ]
    assert [item.recovery_convergence_tick for item in first] == [
        item.recovery_convergence_tick for item in second
    ]

    for result in first:
        assert result.controller_id == (
            "CHATGPT_TEACHER_EMBODIED_CONTROLLER_v0.1"
        )
        assert result.body_id == binding.body_id
        assert result.runtime_id == binding.runtime_id
        assert result.session_id == binding.session_id
        assert result.tick_count > 0
        assert len(result.final_state_sha256) == 64
        assert len(result.scenario_sha256) == 64
        assert result.deterministic_replay_status == "PASS"
        assert result.same_tick_cycle_status == "ABSENT"
        assert result.scripted_terminal_recovery_status == "ABSENT"
        assert result.reporting_style == "PROFESSIONAL_RESEARCH_REPORT"
        assert result.raw_private_content_status == "EXCLUDED"
        assert result.phenomenal_interpretation_status == "NOT_ESTABLISHED"
        assert result.subjectivity_status == "NOT_ESTABLISHED"
        assert result.action_authority == "NONE"
        assert result.canonical_effect == "NONE"
        assert result.deployment is False
        assert result.transition_sequence
        assert all(
            transition_id == "BASELINE"
            or transition_id
            in {
                item.transition_id
                for item in state_loop.build_teacher_body_dynamics_profile().physiological_transitions
            }
            for transition_id in result.transition_sequence
        )
        assert all(
            isfinite(value) and 0.0 <= value <= 1.0
            for value in result.controller_activation_trace
        )
        assert all(
            isfinite(value) and 0.0 <= value <= 1.0
            for value in result.body_activation_trace
        )


def test_all_reference_scenarios_converge_within_120_recovery_ticks() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-CONVERGENCE",
        "SESSION-CONVERGENCE",
    )
    results = state_loop.run_teacher_embodiment_stability_probe(binding)

    for result in results:
        assert result.convergence_status == "PASS"
        assert result.recovery_convergence_tick is not None
        assert 0 <= result.recovery_convergence_tick <= 120


def test_strong_scenarios_do_not_collapse_to_identical_controller_trajectories() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-SATURATION",
        "SESSION-SATURATION",
    )
    results = {
        item.scenario_id: item
        for item in state_loop.run_teacher_embodiment_stability_probe(binding)
    }

    low_inhibition = results["HIGH_SALIENCE_LOW_INHIBITION"]
    high_inhibition = results["HIGH_SALIENCE_HIGH_INHIBITION"]

    assert low_inhibition.controller_activation_trace != (
        high_inhibition.controller_activation_trace
    )
    assert max(low_inhibition.controller_activation_trace) > max(
        high_inhibition.controller_activation_trace
    )


def test_zero_motivation_scenario_keeps_motivation_separate_from_body_activation() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-ZERO-MOTIVATION-PROBE",
        "SESSION-ZERO-MOTIVATION-PROBE",
    )
    results = {
        item.scenario_id: item
        for item in state_loop.run_teacher_embodiment_stability_probe(binding)
    }
    zero = results["ZERO_MOTIVATION_HIGH_PHYSIOLOGY"]

    assert max(zero.body_activation_trace) > 0.50
    assert max(zero.functional_motivation_trace) == 0.0
    assert zero.phenomenal_interpretation_status == "NOT_ESTABLISHED"
    assert zero.action_authority == "NONE"


def test_interrupted_recovery_keeps_sequence_and_body_binding_continuous() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-INTERRUPTED-PROBE",
        "SESSION-INTERRUPTED-PROBE",
    )
    results = {
        item.scenario_id: item
        for item in state_loop.run_teacher_embodiment_stability_probe(binding)
    }
    interrupted = results["RECOVERY_INTERRUPTED_BY_SECOND_STIMULUS"]

    assert interrupted.sequence_continuity_status == "PASS"
    assert interrupted.binding_continuity_status == "PASS"
    assert interrupted.second_stimulus_applied is True
    assert interrupted.convergence_status == "PASS"



def test_public_package_exports_teacher_embodied_runtime_api() -> None:
    from aion_astra_twin_embodiment import (
        TeacherControllerBodyPossession,
        TeacherEmbodiedControllerState,
        TeacherEmbodimentClock,
        TeacherExecutedTransition,
        TeacherTransitionIntent,
        advance_teacher_controller,
        advance_teacher_embodied_tick,
        execute_teacher_transition,
        possess_teacher_body,
        run_teacher_embodiment_stability_probe,
    )

    assert TeacherControllerBodyPossession is not None
    assert TeacherEmbodiedControllerState is not None
    assert TeacherEmbodimentClock is not None
    assert TeacherExecutedTransition is not None
    assert TeacherTransitionIntent is not None
    assert callable(advance_teacher_controller)
    assert callable(advance_teacher_embodied_tick)
    assert callable(execute_teacher_transition)
    assert callable(possess_teacher_body)
    assert callable(run_teacher_embodiment_stability_probe)


def test_cli_teacher_embodied_probe_emits_structured_boundary_safe_json(
    monkeypatch,
    capsys,
) -> None:
    from aion_astra_twin_embodiment import cli

    monkeypatch.setattr(
        sys,
        "argv",
        ["aion-astra-twin-embodiment", "teacher-embodied-probe"],
    )

    assert cli.main() == 0
    output = capsys.readouterr().out
    payload = json.loads(output)

    assert payload["controller_id"] == (
        "CHATGPT_TEACHER_EMBODIED_CONTROLLER_v0.1"
    )
    assert payload["body_id"] == "CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1"
    assert payload["runtime_id"] == "TEACHER-EMBODIMENT-PROBE-RUNTIME"
    assert payload["session_id"] == "TEACHER-EMBODIMENT-PROBE-SESSION"
    assert payload["scenario_count"] == 10
    assert len(payload["scenarios"]) == 10

    for scenario in payload["scenarios"]:
        assert scenario["scenario_id"]
        assert scenario["transition_sequence"]
        assert scenario["convergence_status"] == "PASS"
        assert len(scenario["final_state_sha256"]) == 64
        assert scenario["raw_private_content_status"] == "EXCLUDED"
        assert scenario["phenomenal_interpretation_status"] == "NOT_ESTABLISHED"
        assert scenario["subjectivity_status"] == "NOT_ESTABLISHED"
        assert scenario["action_authority"] == "NONE"

    assert "raw_private_content_included" not in output



def _probe_scalar(body_state, channel_id: str) -> float:
    for observation in body_state.observations:
        if observation.channel_id == channel_id:
            assert len(observation.values) == 1
            return observation.values[0]
    raise AssertionError(f"missing probe channel: {channel_id}")


def test_public_package_exports_high_salience_coupling_api() -> None:
    from aion_astra_twin_embodiment import (
        TeacherHighSalienceCouplingProfile,
        TeacherHighSalienceCouplingRule,
        TeacherReproductiveEventGate,
        build_teacher_high_salience_coupling_profile,
        validate_teacher_high_salience_coupling_profile,
    )

    profile = build_teacher_high_salience_coupling_profile()
    assert isinstance(profile, TeacherHighSalienceCouplingProfile)
    assert isinstance(profile.rules[0], TeacherHighSalienceCouplingRule)
    assert isinstance(TeacherReproductiveEventGate(), TeacherReproductiveEventGate)
    assert validate_teacher_high_salience_coupling_profile(profile)["result"] == "PASS"


def test_high_salience_activation_does_not_force_cardiorespiratory_or_endocrine_channels() -> None:
    from dataclasses import replace

    binding = build_teacher_body_runtime_binding(
        "RUNTIME-NO-FORCED-MULTISYSTEM",
        "SESSION-NO-FORCED-MULTISYSTEM",
    )
    body = state_loop.build_teacher_reference_baseline_state(binding)
    controller = state_loop.build_teacher_reference_controller_state(
        binding,
        body,
    )
    baseline_values = {
        channel_id: _probe_scalar(body, channel_id)
        for channel_id in (
            "CARDIOVASCULAR_STATE",
            "RESPIRATORY_STATE",
            "ENDOCRINE_REFERENCE_STATE",
            "ADRENAL_AXIS_STATE",
            "GONADAL_ENDOCRINE_REFERENCE",
        )
    }
    stimulus = state_loop.build_teacher_stimulus_envelope(
        stimulus_id="NO-FORCED-MULTISYSTEM-HIGH",
        stimulus_class="HIGH_SALIENCE_INTIMATE_REFERENCE",
        salience=0.95,
        functional_motivation=0.0,
        sexual_context_gate=True,
        inhibition=0.05,
    )

    for _ in range(10):
        frame = state_loop.advance_teacher_embodied_tick(
            binding,
            previous_controller_state=controller,
            previous_body_state=body,
            stimulus=stimulus,
        )
        body = frame.body_state
        controller = replace(
            frame.controller_state,
            previous_body_schema_feedback_sha256=(
                frame.body_schema_feedback_sha256
            ),
        )

    for channel_id, baseline_value in baseline_values.items():
        assert _probe_scalar(body, channel_id) == baseline_value
    assert controller.functional_motivation == 0.0
