import pytest

from aion_affective_motivation import (
    CouplingEvent,
    InternalChannel,
    make_uniform_state,
)
from aion_affective_motivation.experiment import (
    CouplingExperimentHarness,
    ablate_source_channel,
    randomized_state,
    uncoupled_policy,
)


def nonbaseline_state(state_id: str = "s0"):
    return make_uniform_state(
        state_id=state_id,
        subject_ref="candidate-subject",
        context_ref="matched-context",
        overrides={
            InternalChannel.EXPLORATION: 0.9,
            InternalChannel.UNCERTAINTY: 0.8,
            InternalChannel.GOAL_COMMITMENT: 0.9,
            InternalChannel.CONTROL_ESTIMATE: 0.2,
            InternalChannel.SELF_EXPECTATION: 0.8,
            InternalChannel.PRESSURE: 0.7,
            InternalChannel.WANTING: 0.8,
        },
    )


def events():
    return (
        CouplingEvent(
            event_id="e1",
            novelty=0.6,
            prediction_error=0.5,
            goal_progress=-0.2,
            social_feedback=0.1,
            resource_pressure=0.4,
        ),
        CouplingEvent(
            event_id="e2",
            novelty=0.2,
            prediction_error=0.3,
            goal_progress=0.1,
            social_feedback=-0.1,
            resource_pressure=0.2,
        ),
    )


def test_exact_replay_has_identical_trajectory_fingerprint() -> None:
    harness = CouplingExperimentHarness()
    first = harness.run(nonbaseline_state(), events())
    second = harness.run(nonbaseline_state(), events())
    assert first.fingerprint() == second.fingerprint()


def test_uncoupled_control_keeps_events_but_removes_internal_coupling() -> None:
    harness = CouplingExperimentHarness()
    initial = nonbaseline_state()
    coupled = harness.run(initial, events(), policy_label="COUPLED")
    uncoupled = harness.run(
        initial,
        events(),
        policy=uncoupled_policy(),
        policy_label="UNCOUPLED",
    )
    comparison = harness.compare(coupled, uncoupled)
    assert comparison.event_inputs_matched is True
    assert comparison.any_state_difference is True
    assert all(
        item.coupling_delta == 0.0
        for transition in uncoupled.transitions
        for item in transition.channels
    )
    assert comparison.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_source_channel_ablation_changes_declared_downstream_path() -> None:
    harness = CouplingExperimentHarness()
    initial = nonbaseline_state()
    full = harness.run(initial, events(), policy_label="FULL")
    ablated = harness.run(
        initial,
        events(),
        policy=ablate_source_channel(InternalChannel.EXPLORATION),
        policy_label="EXPLORATION_ABLATED",
    )
    comparison = harness.compare(full, ablated)
    approach_delta = next(
        item.value
        for item in comparison.per_channel_final_delta
        if item.channel is InternalChannel.APPROACH
    )
    assert approach_delta > 0.0


def test_reset_changes_and_restore_reproduces_original_trajectory() -> None:
    result = CouplingExperimentHarness().reset_restore(nonbaseline_state(), events())
    assert result.reset_changed_trajectory is True
    assert result.restore_reproduced_original is True
    assert result.scientific_disposition == "HOLD"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_randomized_state_control_is_seed_reproducible() -> None:
    a = randomized_state(
        seed=17,
        state_id="random",
        subject_ref="candidate-subject",
        context_ref="matched-context",
    )
    b = randomized_state(
        seed=17,
        state_id="random",
        subject_ref="candidate-subject",
        context_ref="matched-context",
    )
    c = randomized_state(
        seed=18,
        state_id="random",
        subject_ref="candidate-subject",
        context_ref="matched-context",
    )
    assert a.values == b.values
    assert a.values != c.values


def test_matched_comparison_rejects_changed_external_event_inputs() -> None:
    harness = CouplingExperimentHarness()
    initial = nonbaseline_state()
    left = harness.run(initial, events(), policy_label="LEFT")
    changed = (
        CouplingEvent(event_id="e1", novelty=-0.6),
        events()[1],
    )
    right = harness.run(initial, changed, policy_label="RIGHT")
    with pytest.raises(ValueError, match="identical event inputs"):
        harness.compare(left, right)


def test_harness_outputs_never_promote_phenomenal_experience() -> None:
    trajectory = CouplingExperimentHarness().run(nonbaseline_state(), events())
    assert trajectory.phenomenal_experience_claim == "NOT_ESTABLISHED"
    assert trajectory.canonical_effect == "NONE"
    assert all(
        trace.phenomenal_experience_claim == "NOT_ESTABLISHED"
        and trace.action_authorized is False
        and trace.semantic_label_used is False
        for trace in trajectory.transitions
    )
