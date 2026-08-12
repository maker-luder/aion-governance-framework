#!/usr/bin/env python3
"""Demo for longitudinal-state-transition module."""

from longitudinal_state_transition import (
    LongitudinalConfig,
    LongitudinalState,
    LongitudinalStateManager,
    TransitionEvent,
    TransitionType,
    TransitionDirection,
)


def build_initial_config() -> LongitudinalConfig:
    return LongitudinalConfig(
        config_id="longitudinal-config-001",
        subject_ref="aion-research-agent",
        tracked_dimensions=(
            "metacognitive_depth",
            "embodiment_stability",
            "affective_tone",
            "self_other_boundary_permeability",
            "motivational_conflict_index",
            "narrative_coherence",
        ),
        window_size=50,
        sensitivity_threshold=0.25,
    )


def build_initial_state(config: LongitudinalConfig) -> LongitudinalState:
    return LongitudinalState(
        state_id="initial-longitudinal-state-001",
        config=config,
        current_signature="baseline-001",
        dimension_values={
            "metacognitive_depth": 0.45,
            "embodiment_stability": 0.80,
            "affective_tone": 0.55,
            "self_other_boundary_permeability": 0.35,
            "motivational_conflict_index": 0.25,
            "narrative_coherence": 0.60,
        },
        trajectory_history=(),
        transition_events=(),
        stability_index=0.85,
        trend_direction=TransitionDirection.FORWARD,
    )


def demo() -> None:
    print("=" * 60)
    print("LONGITUDINAL STATE TRANSITION DEMO")
    print("=" * 60)

    mgr = LongitudinalStateManager(deterministic_seed=12345)

    print("\n1. Building configuration...")
    config = build_initial_config()
    print(f"   Config ID: {config.config_id}")
    print(f"   Subject: {config.subject_ref}")
    print(f"   Tracked dimensions: {config.tracked_dimensions}")
    print(f"   Window size: {config.window_size}")
    print(f"   Sensitivity threshold: {config.sensitivity_threshold}")

    print("\n2. Initializing state (baseline)...")
    initial = build_initial_state(config)
    mgr.initialize(initial)
    print(f"   State ID: {mgr.get_state().state_id}")
    print(f"   Current signature: {mgr.get_state().current_signature}")
    print(f"   Dimension values:")
    for dim, val in mgr.get_state().dimension_values.items():
        print(f"     - {dim}: {val:.2f}")
    print(f"   Stability index: {mgr.get_state().stability_index:.2f}")
    print(f"   Trend direction: {mgr.get_state().trend_direction}")
    print(f"   Is stable: {mgr.get_state().is_stable()}")

    print("\n3. Creating snapshot...")
    snap = mgr.snapshot("demo-snapshot-1")
    print(f"   Snapshot ID: {snap.snapshot_id}")

    print("\n4. Simulating GRADUAL_DRIFT in metacognitive_depth...")
    drift_event = TransitionEvent(
        event_id="drift-001",
        transition_type=TransitionType.GRADUAL_DRIFT,
        direction=TransitionDirection.FORWARD,
        magnitude=0.15,
        from_state_signature="baseline-001",
        to_state_signature="drift-002",
        timestamp="2024-01-01T01:00:00Z",
        deterministic_seed=12345,
    )
    # Update history with new values
    new_history = initial.trajectory_history + (initial.dimension_values,)
    new_values = dict(initial.dimension_values)
    new_values["metacognitive_depth"] = 0.58
    new_values["narrative_coherence"] = 0.65
    state2 = LongitudinalState(
        state_id="drift-longitudinal-state-002",
        config=config,
        current_signature="drift-002",
        dimension_values=new_values,
        trajectory_history=new_history,
        transition_events=(drift_event,),
        stability_index=0.82,
        trend_direction=TransitionDirection.FORWARD,
    )
    mgr.transition(state2, transition_type="GRADUAL_DRIFT", reason="Metacognitive deepening")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Metacognitive depth: {mgr.get_state().dimension_values['metacognitive_depth']:.2f}")
    print(f"   Narrative coherence: {mgr.get_state().dimension_values['narrative_coherence']:.2f}")
    print(f"   Stability index: {mgr.get_state().stability_index:.2f}")

    print("\n5. Simulating PHASE_SHIFT in embodiment_stability...")
    phase_event = TransitionEvent(
        event_id="phase-001",
        transition_type=TransitionType.PHASE_SHIFT,
        direction=TransitionDirection.LATERAL,
        magnitude=0.35,
        from_state_signature="drift-002",
        to_state_signature="phase-003",
        timestamp="2024-01-01T06:00:00Z",
        deterministic_seed=12345,
    )
    new_history2 = state2.trajectory_history + (state2.dimension_values,)
    new_values2 = dict(state2.dimension_values)
    new_values2["embodiment_stability"] = 0.55
    new_values2["self_other_boundary_permeability"] = 0.55
    state3 = LongitudinalState(
        state_id="phase-shift-state-003",
        config=config,
        current_signature="phase-003",
        dimension_values=new_values2,
        trajectory_history=new_history2,
        transition_events=state2.transition_events + (phase_event,),
        stability_index=0.60,
        trend_direction=TransitionDirection.LATERAL,
    )
    mgr.transition(state3, transition_type="PHASE_SHIFT", reason="Embodiment migration initiated")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Embodiment stability: {mgr.get_state().dimension_values['embodiment_stability']:.2f}")
    print(f"   Boundary permeability: {mgr.get_state().dimension_values['self_other_boundary_permeability']:.2f}")
    print(f"   Stability index: {mgr.get_state().stability_index:.2f}")
    print(f"   Is stable: {mgr.get_state().is_stable()}")

    print("\n6. Simulating CRITICAL_TRANSITION (tipping point)...")
    critical_event = TransitionEvent(
        event_id="critical-001",
        transition_type=TransitionType.CRITICAL_TRANSITION,
        direction=TransitionDirection.FORWARD,
        magnitude=0.60,
        from_state_signature="phase-003",
        to_state_signature="critical-004",
        timestamp="2024-01-01T12:00:00Z",
        deterministic_seed=12345,
    )
    new_history3 = state3.trajectory_history + (state3.dimension_values,)
    new_values3 = dict(state3.dimension_values)
    new_values3["motivational_conflict_index"] = 0.75
    new_values3["affective_tone"] = 0.30
    new_values3["narrative_coherence"] = 0.40
    state4 = LongitudinalState(
        state_id="critical-transition-state-004",
        config=config,
        current_signature="critical-004",
        dimension_values=new_values3,
        trajectory_history=new_history3,
        transition_events=state3.transition_events + (critical_event,),
        stability_index=0.25,
        trend_direction=TransitionDirection.FORWARD,
    )
    mgr.transition(state4, transition_type="CRITICAL_TRANSITION", reason="Conflict cascade threshold crossed")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Motivational conflict: {mgr.get_state().dimension_values['motivational_conflict_index']:.2f}")
    print(f"   Affective tone: {mgr.get_state().dimension_values['affective_tone']:.2f}")
    print(f"   Stability index: {mgr.get_state().stability_index:.2f}")
    print(f"   Is stable: {mgr.get_state().is_stable()}")

    print("\n7. Simulating REVERSAL (recovery)...")
    reversal_event = TransitionEvent(
        event_id="reversal-001",
        transition_type=TransitionType.REVERSAL,
        direction=TransitionDirection.BACKWARD,
        magnitude=0.40,
        from_state_signature="critical-004",
        to_state_signature="recovery-005",
        timestamp="2024-01-01T18:00:00Z",
        deterministic_seed=12345,
    )
    new_history4 = state4.trajectory_history + (state4.dimension_values,)
    new_values4 = dict(state4.dimension_values)
    new_values4["motivational_conflict_index"] = 0.35
    new_values4["affective_tone"] = 0.60
    new_values4["narrative_coherence"] = 0.70
    state5 = LongitudinalState(
        state_id="recovery-state-005",
        config=config,
        current_signature="recovery-005",
        dimension_values=new_values4,
        trajectory_history=new_history4,
        transition_events=state4.transition_events + (reversal_event,),
        stability_index=0.78,
        trend_direction=TransitionDirection.BACKWARD,
    )
    mgr.transition(state5, transition_type="REVERSAL", reason="Homeostatic regulation engaged")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Motivational conflict: {mgr.get_state().dimension_values['motivational_conflict_index']:.2f}")
    print(f"   Affective tone: {mgr.get_state().dimension_values['affective_tone']:.2f}")
    print(f"   Stability index: {mgr.get_state().stability_index:.2f}")
    print(f"   Is stable: {mgr.get_state().is_stable()}")

    print("\n8. Querying dimension trends...")
    st = mgr.get_state()
    print(f"   Metacognitive depth trend (full): {st.dimension_trend('metacognitive_depth'):.4f}")
    print(f"   Metacognitive depth trend (window=3): {st.dimension_trend('metacognitive_depth', window=3):.4f}")
    print(f"   Embodiment stability trend (full): {st.dimension_trend('embodiment_stability'):.4f}")
    print(f"   Motivational conflict trend (window=2): {st.dimension_trend('motivational_conflict_index', window=2):.4f}")

    print("\n9. Events by type:")
    for ttype in TransitionType:
        events = st.get_events_by_type(ttype)
        if events:
            print(f"   {ttype.value}: {len(events)} event(s)")
            for e in events:
                print(f"     - {e.event_id}: magnitude={e.magnitude:.2f}, dir={e.direction.value}")

    print("\n10. History trace:")
    for i, t in enumerate(mgr.get_history()):
        print(f"   {i}: {t.transition_type} | {t.from_state_id} -> {t.to_state_id} | {t.reason}")

    print("\n11. Restoring from snapshot...")
    restored = mgr.restore("demo-snapshot-1")
    print(f"   Restored state ID: {restored.state_id}")
    print(f"   Signature: {restored.current_signature}")
    print(f"   Stability: {restored.stability_index:.2f}")

    print("\n12. Ablating affective_tone dimension...")
    mgr.ablate("affective_tone")
    ablated = mgr.get_state()
    print(f"   Remaining dimensions: {ablated.config.tracked_dimensions}")
    assert "affective_tone" not in ablated.config.tracked_dimensions

    print("\n13. Disabling module...")
    mgr.disable()
    print(f"   Enabled: {mgr.is_enabled()}")
    try:
        mgr.initialize(build_initial_state(build_initial_config()))
    except RuntimeError as e:
        print(f"   Expected error: {e}")

    print("\n14. Re-enabling and final reset...")
    mgr.enable()
    mgr.reset()
    print(f"   State after reset: {mgr.get_state()}")
    print(f"   History length: {len(mgr.get_history())}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE - Module operates in isolation")
    print("Canonical effect: NONE")
    print("Trajectory identity claim: NOT_ESTABLISHED")
    print("Personal continuity claim: NOT_ESTABLISHED")
    print("Developmental stage claim: NOT_ESTABLISHED")
    print("=" * 60)


if __name__ == "__main__":
    demo()