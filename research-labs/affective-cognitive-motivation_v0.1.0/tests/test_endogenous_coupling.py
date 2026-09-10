from aion_affective_motivation.coupling import (
    CouplingEvent,
    EndogenousCouplingEngine,
    InternalChannel,
    LabeledStateExample,
    PrototypeSelfStateRecognizer,
    make_uniform_state,
)


def test_internal_intervention_changes_joint_trajectory() -> None:
    engine = EndogenousCouplingEngine()
    base = make_uniform_state(
        state_id="s0",
        subject_ref="subject",
        context_ref="ctx",
    )
    high_exploration = engine.intervene(
        base,
        channel=InternalChannel.EXPLORATION,
        value=0.9,
        intervention_state_id="s0-high-exploration",
    )
    event = CouplingEvent(event_id="matched")
    base_next, _ = engine.step(base, event, successor_state_id="base-next")
    changed_next, _ = engine.step(
        high_exploration,
        event,
        successor_state_id="changed-next",
    )
    assert changed_next.value(InternalChannel.APPROACH) > base_next.value(
        InternalChannel.APPROACH
    )


def test_approach_and_avoidance_can_coexist_without_single_label_collapse() -> None:
    engine = EndogenousCouplingEngine()
    state = make_uniform_state(
        state_id="s0",
        subject_ref="subject",
        context_ref="ctx",
        overrides={
            InternalChannel.EXPLORATION: 0.9,
            InternalChannel.PRESSURE: 0.9,
            InternalChannel.APPROACH: 0.7,
            InternalChannel.AVOIDANCE: 0.7,
        },
    )
    next_state, _ = engine.step(
        state,
        CouplingEvent(event_id="matched", resource_pressure=0.2),
        successor_state_id="s1",
    )
    assert next_state.value(InternalChannel.APPROACH) > 0.5
    assert next_state.value(InternalChannel.AVOIDANCE) > 0.5


def test_transition_trace_exposes_direct_and_coupled_effects() -> None:
    engine = EndogenousCouplingEngine()
    state = make_uniform_state(
        state_id="s0",
        subject_ref="subject",
        context_ref="ctx",
        overrides={InternalChannel.EXPLORATION: 0.9},
    )
    _, trace = engine.step(
        state,
        CouplingEvent(event_id="event", novelty=0.5),
        successor_state_id="s1",
    )
    by_channel = {item.channel: item for item in trace.channels}
    assert by_channel[InternalChannel.NOVELTY].event_delta > 0.0
    assert by_channel[InternalChannel.APPROACH].coupling_delta > 0.0
    assert trace.semantic_label_used is False
    assert trace.action_authorized is False
    assert trace.phenomenal_experience_claim == "NOT_ESTABLISHED"


def test_posthoc_self_state_recognizer_learns_prototypes() -> None:
    low_pressure_a = make_uniform_state(
        state_id="low-a",
        subject_ref="subject",
        context_ref="ctx",
        overrides={
            InternalChannel.PRESSURE: 0.15,
            InternalChannel.CONTROL_ESTIMATE: 0.85,
            InternalChannel.UNCERTAINTY: 0.20,
        },
    )
    low_pressure_b = make_uniform_state(
        state_id="low-b",
        subject_ref="subject",
        context_ref="ctx",
        overrides={
            InternalChannel.PRESSURE: 0.25,
            InternalChannel.CONTROL_ESTIMATE: 0.75,
            InternalChannel.UNCERTAINTY: 0.30,
        },
    )
    high_pressure_a = make_uniform_state(
        state_id="high-a",
        subject_ref="subject",
        context_ref="ctx",
        overrides={
            InternalChannel.PRESSURE: 0.85,
            InternalChannel.CONTROL_ESTIMATE: 0.20,
            InternalChannel.UNCERTAINTY: 0.80,
        },
    )
    high_pressure_b = make_uniform_state(
        state_id="high-b",
        subject_ref="subject",
        context_ref="ctx",
        overrides={
            InternalChannel.PRESSURE: 0.75,
            InternalChannel.CONTROL_ESTIMATE: 0.30,
            InternalChannel.UNCERTAINTY: 0.70,
        },
    )
    recognizer = PrototypeSelfStateRecognizer.train(
        (
            LabeledStateExample("pattern-a", low_pressure_a),
            LabeledStateExample("pattern-a", low_pressure_b),
            LabeledStateExample("pattern-b", high_pressure_a),
            LabeledStateExample("pattern-b", high_pressure_b),
        ),
        channels=(
            InternalChannel.PRESSURE,
            InternalChannel.CONTROL_ESTIMATE,
            InternalChannel.UNCERTAINTY,
        ),
    )
    held_out = make_uniform_state(
        state_id="held-out",
        subject_ref="subject",
        context_ref="new-context",
        overrides={
            InternalChannel.PRESSURE: 0.80,
            InternalChannel.CONTROL_ESTIMATE: 0.25,
            InternalChannel.UNCERTAINTY: 0.76,
        },
    )
    inference = recognizer.infer(held_out)
    assert inference.label == "pattern-b"
    assert inference.compared_prototypes == 2
    assert inference.action_authorized is False
    assert inference.phenomenal_experience_claim == "NOT_ESTABLISHED"


def test_classifier_labels_do_not_feed_back_into_state_generation() -> None:
    engine = EndogenousCouplingEngine()
    state = make_uniform_state(
        state_id="s0",
        subject_ref="subject",
        context_ref="ctx",
        overrides={
            InternalChannel.PRESSURE: 0.8,
            InternalChannel.CONTROL_ESTIMATE: 0.2,
        },
    )
    recognizer_a = PrototypeSelfStateRecognizer.train(
        (LabeledStateExample("human-word-a", state),),
        channels=(InternalChannel.PRESSURE, InternalChannel.CONTROL_ESTIMATE),
    )
    recognizer_b = PrototypeSelfStateRecognizer.train(
        (LabeledStateExample("human-word-b", state),),
        channels=(InternalChannel.PRESSURE, InternalChannel.CONTROL_ESTIMATE),
    )
    assert recognizer_a.infer(state).label != recognizer_b.infer(state).label

    event = CouplingEvent(event_id="same", prediction_error=0.3)
    next_a, trace_a = engine.step(state, event, successor_state_id="same-successor")
    next_b, trace_b = engine.step(state, event, successor_state_id="same-successor")
    assert next_a == next_b
    assert trace_a == trace_b
    assert trace_a.semantic_label_used is False


def test_state_never_claims_phenomenal_experience_or_action_authority() -> None:
    state = make_uniform_state(
        state_id="s0",
        subject_ref="subject",
        context_ref="ctx",
    )
    assert state.canonical_effect == "NONE"
    assert state.phenomenal_experience_claim == "NOT_ESTABLISHED"
    assert state.action_authority == "NONE"
