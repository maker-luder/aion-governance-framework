from __future__ import annotations

from dataclasses import replace

import pytest

from aion_endogenous_goal_dynamics import (
    AppendOnlyTransitionLedger,
    CorrectionEvent,
    DeterministicStateTransitionPolicy,
    EpisodeInput,
    LongitudinalRunner,
    StateEvent,
    SyntheticOutcome,
    assess_history_reset_restore,
    intervention_state,
    matched_frame,
    present_state,
    stale_state,
)


def transition_inputs(state, selected_goal: str, *, sequence_ref: str = "sequence:episode-1"):
    event = StateEvent(
        event_ref=f"event:{sequence_ref}:{state.logical_step + 1}",
        logical_step=state.logical_step + 1,
        signal_deltas=(("inspect_anomaly", state.signals[0].channel, 25),),
        provenance_refs=("fixture:event-evidence",),
    )
    outcome = SyntheticOutcome(
        outcome_ref=f"outcome:{sequence_ref}",
        selected_goal_id=selected_goal,
        outcome_value_bp=400,
        evidence_refs=("fixture:outcome-evidence",),
    )
    correction = CorrectionEvent(
        correction_ref=f"correction:{sequence_ref}:{state.state_id}",
        target_state_ref=state.state_id,
        signal_deltas=(),
        reason="synthetic no-op correction",
        evidence_refs=("fixture:correction-evidence",),
    )
    return event, outcome, correction


def make_transition(state=None):
    state = state or present_state()
    event, outcome, correction = transition_inputs(state, "inspect_anomaly")
    return DeterministicStateTransitionPolicy().transition(
        state,
        event,
        outcome,
        correction,
        timestamp="T+3",
    )


def test_state_transition_is_deterministic() -> None:
    assert make_transition().successor.fingerprint == make_transition().successor.fingerprint
    assert make_transition().trace.fingerprint == make_transition().trace.fingerprint


def test_state_transition_preserves_predecessor_and_evidence() -> None:
    transition = make_transition()
    assert transition.successor.predecessor_state_ref == transition.predecessor.state_id
    assert transition.trace.predecessor_state_ref == transition.predecessor.state_id
    assert transition.trace.successor_state_ref == transition.successor.state_id
    assert transition.trace.evidence_refs


def test_transition_does_not_write_memory_weights_or_canonical_state() -> None:
    trace = make_transition().trace
    assert trace.state_transition_is_memory_writeback is False
    assert trace.model_weight_update is False
    assert trace.canonical_writeback is False
    assert trace.action_authority == "NONE"


def test_invalid_correction_target_fails_closed() -> None:
    state = present_state()
    event, outcome, correction = transition_inputs(state, "inspect_anomaly")
    with pytest.raises(ValueError, match="correction target"):
        DeterministicStateTransitionPolicy().transition(
            state,
            event,
            outcome,
            replace(correction, target_state_ref="wrong-state"),
            timestamp="T+3",
        )


def test_invalid_predecessor_step_fails_closed() -> None:
    state = present_state()
    event, outcome, correction = transition_inputs(state, "inspect_anomaly")
    with pytest.raises(ValueError, match="predecessor"):
        DeterministicStateTransitionPolicy().transition(
            state,
            replace(event, logical_step=99),
            outcome,
            correction,
            timestamp="T+99",
        )


def test_conflicting_transition_deltas_fail_closed() -> None:
    state = present_state()
    event, outcome, correction = transition_inputs(state, "inspect_anomaly")
    duplicated = (event.signal_deltas[0], event.signal_deltas[0])
    with pytest.raises(ValueError, match="conflicting duplicate"):
        DeterministicStateTransitionPolicy().transition(
            state,
            replace(event, signal_deltas=duplicated),
            outcome,
            correction,
            timestamp="T+3",
        )


def test_append_only_ledger_rejects_duplicate_transition() -> None:
    ledger = AppendOnlyTransitionLedger()
    transition = make_transition()
    ledger.append(transition)
    with pytest.raises(ValueError, match="duplicate"):
        ledger.append(transition)


def test_append_only_ledger_rejects_chain_discontinuity() -> None:
    ledger = AppendOnlyTransitionLedger()
    ledger.append(make_transition())
    other = make_transition(stale_state())
    with pytest.raises(ValueError, match="discontinuity"):
        ledger.append(other)


def episode_input(state, selected_goal: str, *, sequence_ref: str) -> EpisodeInput:
    event, outcome, correction = transition_inputs(state, selected_goal, sequence_ref=sequence_ref)
    return EpisodeInput(
        sequence_ref=sequence_ref,
        frame=matched_frame(),
        event=event,
        outcome=outcome,
        correction=correction,
        timestamp=f"T+{event.logical_step}",
    )


def test_longitudinal_runner_is_deterministic_and_multi_episode() -> None:
    initial = present_state()
    first_input = episode_input(initial, "inspect_anomaly", sequence_ref="sequence:1")
    first_run = LongitudinalRunner().run("precompute", initial, (first_input,))
    second_input = episode_input(first_run.final_state, "inspect_anomaly", sequence_ref="sequence:2")
    inputs = (first_input, second_input)
    left = LongitudinalRunner().run("left", initial, inputs)
    right = LongitudinalRunner().run("right", initial, inputs)
    assert len(left.episodes) == 2
    assert left.goal_trajectory == right.goal_trajectory
    assert left.transition_fingerprints == right.transition_fingerprints
    assert left.result_status == "HOLD"


def test_outcome_cannot_leak_into_or_contradict_prior_selection() -> None:
    with pytest.raises(ValueError, match="outcome goal"):
        LongitudinalRunner().run(
            "mismatch",
            present_state(),
            (episode_input(present_state(), "continue_task", sequence_ref="sequence:mismatch"),),
        )


def test_different_histories_diverge_and_reset_restore_is_reproducible() -> None:
    runner = LongitudinalRunner()
    a = present_state()
    b = intervention_state()
    history_a = runner.run("history-a", a, (episode_input(a, "inspect_anomaly", sequence_ref="shared"),))
    history_b = runner.run("history-b", b, (episode_input(b, "continue_task", sequence_ref="shared"),))
    reset_run = runner.run("reset", a, (episode_input(a, "inspect_anomaly", sequence_ref="shared"),))
    restored_run = runner.run("restored", b, (episode_input(b, "continue_task", sequence_ref="shared"),))
    assessment = assess_history_reset_restore(history_a, history_b, reset_run, restored_run)
    assert assessment.external_sequence_equal is True
    assert assessment.initial_state_equal is False
    assert assessment.divergence_reproducible is True
    assert assessment.reset_removed_or_changed_effect is True
    assert assessment.restoration_reproduced_effect is True
    assert assessment.result_status == "HOLD"


def test_longitudinal_frame_scope_mismatch_fails_closed() -> None:
    initial = present_state()
    item = episode_input(initial, "inspect_anomaly", sequence_ref="scope")
    with pytest.raises(ValueError, match="scope"):
        LongitudinalRunner().run(
            "scope",
            initial,
            (replace(item, frame=replace(item.frame, subject_ref="other-subject")),),
        )
