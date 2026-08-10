#!/usr/bin/env python3
"""Demo for affective-motivational-dynamics module."""

from affective_motivational_dynamics import (
    AffectiveValence,
    MotivationalDirection,
    MotivationalSignal,
    MotivationalState,
    DynamicsStateManager,
    SignalDomain,
)


def build_initial_state() -> MotivationalState:
    signals = (
        MotivationalSignal(
            signal_id="explore-001",
            domain=SignalDomain.EXPLORATION,
            source_event_id="novel-stimulus-001",
            valence=AffectiveValence.POSITIVE,
            intensity=0.7,
            wanting=0.8,
            predicted_liking=0.4,
            approach=0.7,
            avoidance=0.1,
            uncertainty=0.3,
            direction=MotivationalDirection.APPROACH,
            evidence_refs=("curiosity-signal-001", "dopamine-proxy-001"),
        ),
        MotivationalSignal(
            signal_id="social-001",
            domain=SignalDomain.SOCIAL_AFFILIATION,
            source_event_id="peer-presence-001",
            valence=AffectiveValence.POSITIVE,
            intensity=0.6,
            wanting=0.7,
            predicted_liking=0.6,
            approach=0.6,
            avoidance=0.2,
            uncertainty=0.25,
            direction=MotivationalDirection.APPROACH,
            evidence_refs=("affiliation-signal-001",),
        ),
        MotivationalSignal(
            signal_id="threat-001",
            domain=SignalDomain.SELF_PRESERVATION,
            source_event_id="unexpected-loud-noise-001",
            valence=AffectiveValence.NEGATIVE,
            intensity=0.8,
            wanting=0.2,
            predicted_liking=0.1,
            approach=0.1,
            avoidance=0.9,
            uncertainty=0.2,
            direction=MotivationalDirection.AVOIDANCE,
            evidence_refs=("startle-response-001",),
        ),
        MotivationalSignal(
            signal_id="aesthetic-001",
            domain=SignalDomain.AESTHETIC_ATTRACTION,
            source_event_id="beautiful-pattern-001",
            valence=AffectiveValence.POSITIVE,
            intensity=0.5,
            wanting=0.6,
            predicted_liking=0.7,
            approach=0.5,
            avoidance=0.0,
            uncertainty=0.3,
            direction=MotivationalDirection.APPROACH,
            evidence_refs=("aesthetic-response-001",),
        ),
    )
    return MotivationalState(
        state_id="initial-motivational-state-001",
        subject_ref="aion-research-agent",
        context_ref="integration-candidate-demo",
        signals=signals,
        global_valence=AffectiveValence.MIXED,
        dominant_direction=MotivationalDirection.CONFLICT,
        conflict_index=0.35,
        uncertainty_aggregate=0.26,
    )


def demo() -> None:
    print("=" * 60)
    print("AFFECTIVE-MOTIVATIONAL DYNAMICS DEMO")
    print("=" * 60)

    mgr = DynamicsStateManager(deterministic_seed=12345)

    print("\n1. Initializing state...")
    initial = build_initial_state()
    mgr.initialize(initial)
    print(f"   State ID: {mgr.get_state().state_id}")
    print(f"   Signals: {len(mgr.get_state().signals)}")
    for s in mgr.get_state().signals:
        print(f"     - {s.signal_id}: domain={s.domain.value}, valence={s.valence.value}, "
              f"dir={s.direction.value}, w={s.wanting:.2f}, pl={s.predicted_liking:.2f}, "
              f"app={s.approach:.2f}, av={s.avoidance:.2f}")
    print(f"   Global valence: {mgr.get_state().global_valence}")
    print(f"   Dominant direction: {mgr.get_state().dominant_direction}")
    print(f"   Conflict index: {mgr.get_state().conflict_index}")
    print(f"   Uncertainty aggregate: {mgr.get_state().uncertainty_aggregate}")
    print(f"   Total approach: {mgr.get_state().total_approach():.2f}")
    print(f"   Total avoidance: {mgr.get_state().total_avoidance():.2f}")

    print("\n2. Creating snapshot...")
    snap = mgr.snapshot("demo-snapshot-1")
    print(f"   Snapshot ID: {snap.snapshot_id}")

    print("\n3. Simulating reward prediction error (wanting > liking)...")
    updated_signals = list(initial.signals)
    # Update exploration signal: wanting increases, predicted_liking stays low
    updated_signals[0] = MotivationalSignal(
        signal_id="explore-002",
        domain=SignalDomain.EXPLORATION,
        source_event_id="reward-prediction-error-001",
        valence=AffectiveValence.POSITIVE,
        intensity=0.8,
        wanting=0.9,
        predicted_liking=0.3,
        approach=0.8,
        avoidance=0.05,
        uncertainty=0.2,
        direction=MotivationalDirection.APPROACH,
        evidence_refs=("dopamine-surge-001", "prediction-error-001"),
    )
    # Add new conflict signal
    updated_signals.append(
        MotivationalSignal(
            signal_id="conflict-001",
            domain=SignalDomain.KNOWLEDGE_ACQUISITION,
            source_event_id="difficult-problem-001",
            valence=AffectiveValence.MIXED,
            intensity=0.6,
            wanting=0.7,
            predicted_liking=0.3,
            approach=0.6,
            avoidance=0.5,
            uncertainty=0.4,
            direction=MotivationalDirection.CONFLICT,
            evidence_refs=("cognitive-conflict-001",),
        )
    )
    updated_state = MotivationalState(
        state_id="updated-motivational-state-002",
        subject_ref=initial.subject_ref,
        context_ref=initial.context_ref,
        signals=tuple(updated_signals),
        global_valence=AffectiveValence.MIXED,
        dominant_direction=MotivationalDirection.CONFLICT,
        conflict_index=0.45,
        uncertainty_aggregate=0.28,
    )
    mgr.transition(updated_state, transition_type="REWARD_PREDICTION_ERROR", reason="Dopamine surge increases wanting")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Signals: {len(mgr.get_state().signals)}")
    print(f"   Conflict index: {mgr.get_state().conflict_index}")
    print(f"   Total approach: {mgr.get_state().total_approach():.2f}")
    print(f"   Total avoidance: {mgr.get_state().total_avoidance():.2f}")
    for s in mgr.get_state().signals:
        if s.approach_avoidance_conflict:
            print(f"     CONFLICT: {s.signal_id} (app={s.approach:.2f}, av={s.avoidance:.2f})")
        if s.wanting_liking_discrepancy > 0.4:
            print(f"     WANTING/LIKING GAP: {s.signal_id} (w={s.wanting:.2f}, pl={s.predicted_liking:.2f}, gap={s.wanting_liking_discrepancy:.2f})")

    print("\n4. History trace:")
    for i, t in enumerate(mgr.get_history()):
        print(f"   {i}: {t.transition_type} | {t.from_state_id} -> {t.to_state_id} | {t.reason}")

    print("\n5. Restoring from snapshot...")
    restored = mgr.restore("demo-snapshot-1")
    print(f"   Restored state ID: {restored.state_id}")
    print(f"   Signals: {len(restored.signals)}")
    print(f"   Conflict index: {restored.conflict_index}")

    print("\n6. Ablating SELF_PRESERVATION domain...")
    mgr.ablate("SELF_PRESERVATION")
    ablated = mgr.get_state()
    domains = {s.domain for s in ablated.signals}
    print(f"   Remaining domains: {[d.value for d in domains]}")
    assert SignalDomain.SELF_PRESERVATION not in domains

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
    print("Felt experience claim: NOT_ESTABLISHED")
    print("Hedonic tone claim: NOT_ESTABLISHED")
    print("Motivational authority claim: NOT_ESTABLISHED")
    print("=" * 60)


if __name__ == "__main__":
    demo()