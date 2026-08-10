#!/usr/bin/env python3
"""Demo for self-other-boundary module."""

from self_other_boundary import (
    BoundaryConfiguration,
    BoundaryEvent,
    BoundaryMode,
    BoundaryState,
    BoundaryStateManager,
    OtherModel,
    SelfOtherDistinction,
)


def build_initial_config() -> BoundaryConfiguration:
    return BoundaryConfiguration(
        config_id="boundary-config-001",
        default_mode=BoundaryMode.SEMI_PERMEABLE,
        distinction_weights={
            SelfOtherDistinction.AGENCY_ATTRIBUTION: 0.25,
            SelfOtherDistinction.SENSORY_PREDICTION_ERROR: 0.20,
            SelfOtherDistinction.AFFECTIVE_RESONANCE: 0.20,
            SelfOtherDistinction.PERSPECTIVE_TAKING: 0.15,
            SelfOtherDistinction.NARRATIVE_DIFFERENTIATION: 0.10,
            SelfOtherDistinction.EMBODIMENT_MAPPING: 0.10,
        },
        permeability_threshold=0.3,
        rigidity_threshold=0.7,
    )


def build_initial_state(config: BoundaryConfiguration) -> BoundaryState:
    others = (
        OtherModel(
            other_id="astra-agent",
            embodiment_similarity=0.85,
            behavioral_predictability=0.70,
            affective_resonance=0.60,
            perspective_accessibility=0.50,
            interaction_history_depth=100,
        ),
        OtherModel(
            other_id="human-user",
            embodiment_similarity=0.30,
            behavioral_predictability=0.40,
            affective_resonance=0.75,
            perspective_accessibility=0.60,
            interaction_history_depth=50,
        ),
    )
    return BoundaryState(
        state_id="initial-boundary-state-001",
        subject_ref="aion-research-agent",
        config=config,
        current_mode=BoundaryMode.SEMI_PERMEABLE,
        active_distinctions=tuple(SelfOtherDistinction),
        other_models=others,
        boundary_permeability=0.4,
        confusion_index=0.15,
        recent_events=(),
    )


def demo() -> None:
    print("=" * 60)
    print("SELF-OTHER BOUNDARY DEMO")
    print("=" * 60)

    mgr = BoundaryStateManager(deterministic_seed=12345)

    print("\n1. Building configuration...")
    config = build_initial_config()
    print(f"   Config ID: {config.config_id}")
    print(f"   Default mode: {config.default_mode}")
    print(f"   Distinction weights: { {k.value: v for k, v in config.distinction_weights.items()} }")
    print(f"   Permeability threshold: {config.permeability_threshold}")
    print(f"   Rigidity threshold: {config.rigidity_threshold}")

    print("\n2. Initializing state...")
    initial = build_initial_state(config)
    mgr.initialize(initial)
    print(f"   State ID: {mgr.get_state().state_id}")
    print(f"   Current mode: {mgr.get_state().current_mode}")
    print(f"   Active distinctions: {[d.value for d in mgr.get_state().active_distinctions]}")
    print(f"   Other models: {len(mgr.get_state().other_models)}")
    for om in mgr.get_state().other_models:
        print(f"     - {om.other_id}: embodiment_sim={om.embodiment_similarity}, "
              f"predictability={om.behavioral_predictability}, resonance={om.affective_resonance}")
    print(f"   Boundary permeability: {mgr.get_state().boundary_permeability}")
    print(f"   Confusion index: {mgr.get_state().confusion_index}")

    print("\n3. Creating snapshot...")
    snap = mgr.snapshot("demo-snapshot-1")
    print(f"   Snapshot ID: {snap.snapshot_id}")

    print("\n4. Simulating interaction event (boundary shift)...")
    interaction_event = BoundaryEvent(
        event_id="interaction-001",
        event_type="AFFECTIVE_EXCHANGE",
        self_contribution=0.55,
        other_contribution=0.45,
        boundary_shift=0.15,  # Boundary becomes more permeable
        timestamp="2024-01-01T00:00:10Z",
    )
    shifted_state = BoundaryState(
        state_id="shifted-boundary-state-002",
        subject_ref=initial.subject_ref,
        config=config,
        current_mode=BoundaryMode.PERMEABLE,
        active_distinctions=initial.active_distinctions,
        other_models=initial.other_models,
        boundary_permeability=0.55,  # Increased permeability
        confusion_index=0.25,        # Increased confusion
        recent_events=initial.recent_events + (interaction_event,),
    )
    mgr.transition(shifted_state, transition_type="BOUNDARY_SHIFT", reason="Affective exchange with astra-agent")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Current mode: {mgr.get_state().current_mode}")
    print(f"   Boundary permeability: {mgr.get_state().boundary_permeability}")
    print(f"   Confusion index: {mgr.get_state().confusion_index}")

    print("\n5. Simulating perspective taking (boundary restoration)...")
    perspective_event = BoundaryEvent(
        event_id="perspective-001",
        event_type="PERSPECTIVE_TAKING",
        self_contribution=0.70,
        other_contribution=0.30,
        boundary_shift=-0.10,  # Boundary becomes less permeable (more distinct)
        timestamp="2024-01-01T00:00:20Z",
    )
    restored_state = BoundaryState(
        state_id="restored-boundary-state-003",
        subject_ref=initial.subject_ref,
        config=config,
        current_mode=BoundaryMode.SEMI_PERMEABLE,
        active_distinctions=initial.active_distinctions,
        other_models=initial.other_models,
        boundary_permeability=0.45,
        confusion_index=0.18,
        recent_events=shifted_state.recent_events + (perspective_event,),
    )
    mgr.transition(restored_state, transition_type="BOUNDARY_RESTORATION", reason="Perspective taking engaged")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Current mode: {mgr.get_state().current_mode}")
    print(f"   Boundary permeability: {mgr.get_state().boundary_permeability}")

    print("\n6. History trace:")
    for i, t in enumerate(mgr.get_history()):
        print(f"   {i}: {t.transition_type} | {t.from_state_id} -> {t.to_state_id} | {t.reason}")

    print("\n7. Restoring from snapshot...")
    restored = mgr.restore("demo-snapshot-1")
    print(f"   Restored state ID: {restored.state_id}")
    print(f"   Current mode: {restored.current_mode}")
    print(f"   Boundary permeability: {restored.boundary_permeability}")
    print(f"   Confusion index: {restored.confusion_index}")

    print("\n8. Ablating AFFECTIVE_RESONANCE distinction...")
    mgr.ablate("AFFECTIVE_RESONANCE")
    ablated = mgr.get_state()
    distinctions = {d.value for d in ablated.active_distinctions}
    print(f"   Remaining distinctions: {distinctions}")
    assert "AFFECTIVE_RESONANCE" not in distinctions
    print(f"   Renormalized weights: { {k.value: v for k, v in ablated.config.distinction_weights.items()} }")

    print("\n9. Disabling module...")
    mgr.disable()
    print(f"   Enabled: {mgr.is_enabled()}")
    try:
        mgr.initialize(build_initial_state(build_initial_config()))
    except RuntimeError as e:
        print(f"   Expected error: {e}")

    print("\n10. Re-enabling and final reset...")
    mgr.enable()
    mgr.reset()
    print(f"   State after reset: {mgr.get_state()}")
    print(f"   History length: {len(mgr.get_history())}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE - Module operates in isolation")
    print("Canonical effect: NONE")
    print("Empathy claim: NOT_ESTABLISHED")
    print("Theory of mind claim: NOT_ESTABLISHED")
    print("Shared subjectivity claim: NOT_ESTABLISHED")
    print("=" * 60)


if __name__ == "__main__":
    demo()