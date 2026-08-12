#!/usr/bin/env python3
"""Demo for metacognitive-self-state module."""

from metacognitive_self_state import (
    MetacognitiveCapacity,
    MetacognitiveDepth,
    MetacognitiveState,
    MetacognitiveStateManager,
    SelfModelComponent,
    SelfModelLayer,
)


def build_initial_state() -> MetacognitiveState:
    components = (
        SelfModelComponent(
            component_id="proprioceptive-base",
            layer=SelfModelLayer.IMPLICIT_PROPRIOCEPTIVE,
            capacity=MetacognitiveCapacity.EMBODIMENT_AWARENESS,
            confidence=0.85,
            evidence_refs=("sensorimotor-loop-001",),
        ),
        SelfModelComponent(
            component_id="interoceptive-base",
            layer=SelfModelLayer.IMPLICIT_INTEROCEPTIVE,
            capacity=MetacognitiveCapacity.UNCERTAINTY_MONITORING,
            confidence=0.70,
            evidence_refs=("visceral-signal-002",),
        ),
        SelfModelComponent(
            component_id="pre-reflective-self",
            layer=SelfModelLayer.PRE_REFLECTIVE,
            capacity=MetacognitiveCapacity.SELF_ATTRIBUTION,
            confidence=0.65,
            evidence_refs=("minimal-self-003",),
        ),
        SelfModelComponent(
            component_id="reflective-monitor",
            layer=SelfModelLayer.REFLECTIVE,
            capacity=MetacognitiveCapacity.CONFLICT_DETECTION,
            confidence=0.60,
            evidence_refs=("conflict-signal-004",),
        ),
        SelfModelComponent(
            component_id="metacognitive-eval",
            layer=SelfModelLayer.METACOGNITIVE,
            capacity=MetacognitiveCapacity.STRATEGY_EVALUATION,
            confidence=0.55,
            evidence_refs=("strategy-review-005",),
        ),
    )
    return MetacognitiveState(
        state_id="initial-metacognitive-state-001",
        subject_ref="aion-research-agent",
        context_ref="integration-candidate-demo",
        components=components,
        current_depth=MetacognitiveDepth.LEVEL_2_CONFIDENCE_ESTIMATION,
        active_layers=(
            SelfModelLayer.IMPLICIT_PROPRIOCEPTIVE,
            SelfModelLayer.IMPLICIT_INTEROCEPTIVE,
            SelfModelLayer.PRE_REFLECTIVE,
            SelfModelLayer.REFLECTIVE,
            SelfModelLayer.METACOGNITIVE,
        ),
        uncertainty_estimate=0.35,
        conflict_detected=False,
    )


def demo() -> None:
    print("=" * 60)
    print("METACOGNITIVE SELF-STATE DEMO")
    print("=" * 60)

    mgr = MetacognitiveStateManager(deterministic_seed=12345)

    print("\n1. Initializing state...")
    initial = build_initial_state()
    mgr.initialize(initial)
    print(f"   State ID: {mgr.get_state().state_id}")
    print(f"   Components: {len(mgr.get_state().components)}")
    print(f"   Current depth: {mgr.get_state().current_depth}")
    print(f"   Active layers: {[l.value for l in mgr.get_state().active_layers]}")
    print(f"   Uncertainty: {mgr.get_state().uncertainty_estimate}")
    print(f"   Conflict detected: {mgr.get_state().conflict_detected}")

    print("\n2. Creating snapshot...")
    snap = mgr.snapshot("demo-snapshot-1")
    print(f"   Snapshot ID: {snap.snapshot_id}")
    print(f"   Timestamp: {snap.timestamp}")

    print("\n3. Transitioning to deeper metacognitive state...")
    deeper_components = list(initial.components) + [
        SelfModelComponent(
            component_id="narrative-integration",
            layer=SelfModelLayer.NARRATIVE,
            capacity=MetacognitiveCapacity.SIMULATION_OF_SELF,
            confidence=0.50,
            evidence_refs=("narrative-trace-006",),
        ),
        SelfModelComponent(
            component_id="other-simulation",
            layer=SelfModelLayer.METACOGNITIVE,
            capacity=MetacognitiveCapacity.SIMULATION_OF_OTHER,
            confidence=0.45,
            evidence_refs=("theory-of-mind-007",),
        ),
    ]
    deeper_state = MetacognitiveState(
        state_id="deeper-metacognitive-state-002",
        subject_ref=initial.subject_ref,
        context_ref=initial.context_ref,
        components=tuple(deeper_components),
        current_depth=MetacognitiveDepth.LEVEL_3_STRATEGY_SELECTION,
        active_layers=initial.active_layers + (SelfModelLayer.NARRATIVE,),
        uncertainty_estimate=0.25,
        conflict_detected=True,
    )
    mgr.transition(deeper_state, transition_type="DEEPEN", reason="Narrative integration engaged")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Components: {len(mgr.get_state().components)}")
    print(f"   Current depth: {mgr.get_state().current_depth}")
    print(f"   Conflict detected: {mgr.get_state().conflict_detected}")

    print("\n4. History trace:")
    for i, t in enumerate(mgr.get_history()):
        print(f"   {i}: {t.transition_type} | {t.from_state_id} -> {t.to_state_id} | {t.reason}")

    print("\n5. Restoring from snapshot...")
    restored = mgr.restore("demo-snapshot-1")
    print(f"   Restored state ID: {restored.state_id}")
    print(f"   Components: {len(restored.components)}")
    print(f"   Current depth: {restored.current_depth}")

    print("\n6. Ablating SELF_ATTRIBUTION capacity...")
    mgr.ablate("SELF_ATTRIBUTION")
    ablated = mgr.get_state()
    capacities = {c.capacity for c in ablated.components}
    print(f"   Remaining capacities: {[c.value for c in capacities]}")
    assert MetacognitiveCapacity.SELF_ATTRIBUTION not in capacities

    print("\n7. Disabling module...")
    mgr.disable()
    print(f"   Enabled: {mgr.is_enabled()}")
    try:
        mgr.initialize(build_initial_state())
    except RuntimeError as e:
        print(f"   Expected error: {e}")

    print("\n8. Re-enabling and final reset...")
    mgr.enable()
    mgr.reset()
    print(f"   State after reset: {mgr.get_state()}")
    print(f"   History length: {len(mgr.get_history())}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE - Module operates in isolation")
    print("Canonical effect: NONE")
    print("Subjectivity conclusion: NOT_ESTABLISHED")
    print("=" * 60)


if __name__ == "__main__":
    demo()