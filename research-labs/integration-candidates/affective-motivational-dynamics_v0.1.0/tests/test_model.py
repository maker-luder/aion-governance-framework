from affective_motivational_dynamics import (
    AffectiveValence,
    MotivationalDirection,
    MotivationalSignal,
    MotivationalState,
    DynamicsStateManager,
    SignalDomain,
)


def signal(
    signal_id: str = "sig-1",
    domain: SignalDomain = SignalDomain.EXPLORATION,
    valence: AffectiveValence = AffectiveValence.POSITIVE,
    direction: MotivationalDirection = MotivationalDirection.APPROACH,
    **overrides: float | str | tuple[str, ...],
) -> MotivationalSignal:
    values = {
        "signal_id": signal_id,
        "domain": domain,
        "source_event_id": "event-1",
        "valence": valence,
        "intensity": 0.7,
        "wanting": 0.8,
        "predicted_liking": 0.3,
        "approach": 0.6,
        "avoidance": 0.2,
        "uncertainty": 0.3,
        "direction": direction,
        "evidence_refs": ("evidence-1",),
    }
    values.update(overrides)
    return MotivationalSignal(**values)


def state(
    state_id: str = "state-1",
    **overrides: str | float | tuple[MotivationalSignal, ...] | AffectiveValence | MotivationalDirection,
) -> MotivationalState:
    values = {
        "state_id": state_id,
        "subject_ref": "subject-1",
        "context_ref": "context-1",
        "signals": (signal(),),
        "global_valence": AffectiveValence.POSITIVE,
        "dominant_direction": MotivationalDirection.APPROACH,
        "conflict_index": 0.2,
        "uncertainty_aggregate": 0.3,
    }
    values.update(overrides)
    return MotivationalState(**values)


def test_signal_validation() -> None:
    try:
        MotivationalSignal(
            signal_id="",
            domain=SignalDomain.EXPLORATION,
            source_event_id="e1",
            valence=AffectiveValence.POSITIVE,
            intensity=0.5,
            wanting=0.5,
            predicted_liking=0.5,
            approach=0.5,
            avoidance=0.5,
            uncertainty=0.5,
            direction=MotivationalDirection.APPROACH,
            evidence_refs=("e1",),
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "signal_id must be non-empty" in str(e)


def test_signal_evidence_required() -> None:
    try:
        MotivationalSignal(
            signal_id="s1",
            domain=SignalDomain.EXPLORATION,
            source_event_id="e1",
            valence=AffectiveValence.POSITIVE,
            intensity=0.5,
            wanting=0.5,
            predicted_liking=0.5,
            approach=0.5,
            avoidance=0.5,
            uncertainty=0.5,
            direction=MotivationalDirection.APPROACH,
            evidence_refs=(),
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "at least one evidence_ref is required" in str(e)


def test_signal_bounds() -> None:
    try:
        MotivationalSignal(
            signal_id="s1",
            domain=SignalDomain.EXPLORATION,
            source_event_id="e1",
            valence=AffectiveValence.POSITIVE,
            intensity=1.5,
            wanting=0.5,
            predicted_liking=0.5,
            approach=0.5,
            avoidance=0.5,
            uncertainty=0.5,
            direction=MotivationalDirection.APPROACH,
            evidence_refs=("e1",),
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "intensity must be between 0.0 and 1.0" in str(e)


def test_signal_canonical_effect() -> None:
    try:
        MotivationalSignal(
            signal_id="s1",
            domain=SignalDomain.EXPLORATION,
            source_event_id="e1",
            valence=AffectiveValence.POSITIVE,
            intensity=0.5,
            wanting=0.5,
            predicted_liking=0.5,
            approach=0.5,
            avoidance=0.5,
            uncertainty=0.5,
            direction=MotivationalDirection.APPROACH,
            evidence_refs=("e1",),
            canonical_effect="EFFECT",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "canonical_effect=NONE" in str(e)


def test_signal_approach_avoidance_conflict() -> None:
    s = signal(approach=0.6, avoidance=0.4)
    assert s.approach_avoidance_conflict is True

    s2 = signal(approach=0.6, avoidance=0.0)
    assert s2.approach_avoidance_conflict is False


def test_signal_wanting_liking_discrepancy() -> None:
    s = signal(wanting=0.8, predicted_liking=0.3)
    assert s.wanting_liking_discrepancy == 0.5

    s2 = signal(wanting=0.5, predicted_liking=0.5)
    assert s2.wanting_liking_discrepancy == 0.0


def test_state_validation() -> None:
    try:
        MotivationalState(
            state_id="s1",
            subject_ref="subj",
            context_ref="ctx",
            signals=(signal(),),
            global_valence=AffectiveValence.POSITIVE,
            dominant_direction=MotivationalDirection.APPROACH,
            conflict_index=0.2,
            uncertainty_aggregate=0.3,
            felt_experience_claim="CLAIMED",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "felt experience must remain NOT_ESTABLISHED" in str(e)


def test_state_get_signals_by_domain() -> None:
    s1 = signal(domain=SignalDomain.EXPLORATION, signal_id="s1")
    s2 = signal(domain=SignalDomain.SOCIAL_AFFILIATION, signal_id="s2")
    st = state(signals=(s1, s2))
    exploration = st.get_signals_by_domain(SignalDomain.EXPLORATION)
    assert len(exploration) == 1
    assert exploration[0].signal_id == "s1"


def test_state_get_signals_by_direction() -> None:
    s1 = signal(direction=MotivationalDirection.APPROACH, signal_id="s1")
    s2 = signal(direction=MotivationalDirection.AVOIDANCE, signal_id="s2")
    st = state(signals=(s1, s2))
    approach = st.get_signals_by_direction(MotivationalDirection.APPROACH)
    assert len(approach) == 1
    assert approach[0].signal_id == "s1"


def test_state_total_approach_avoidance() -> None:
    s1 = signal(approach=0.6, avoidance=0.2, signal_id="s1")
    s2 = signal(approach=0.4, avoidance=0.5, signal_id="s2")
    st = state(signals=(s1, s2))
    assert st.total_approach() == 1.0
    assert st.total_avoidance() == 0.7


def test_manager_initialize_and_get() -> None:
    mgr = DynamicsStateManager(deterministic_seed=42)
    s = state()
    mgr.initialize(s)
    assert mgr.get_state() is s
    assert len(mgr.get_history()) == 1
    assert mgr.get_history()[0].transition_type == "INITIALIZE"


def test_manager_transition() -> None:
    mgr = DynamicsStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    s2 = state(state_id="state-2", signals=(signal(signal_id="s2"),))
    mgr.transition(s2, transition_type="DYNAMICS_SHIFT", reason="New signal")
    assert mgr.get_state() is s2
    history = mgr.get_history()
    assert len(history) == 2
    assert history[1].transition_type == "DYNAMICS_SHIFT"


def test_manager_snapshot_and_restore() -> None:
    mgr = DynamicsStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    snap = mgr.snapshot("test-snap")
    assert snap.snapshot_id == "test-snap"

    s2 = state(state_id="state-2")
    mgr.transition(s2)
    restored = mgr.restore("test-snap")
    assert restored is s1


def test_manager_reset() -> None:
    mgr = DynamicsStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    mgr.snapshot("snap1")
    mgr.reset()
    assert mgr.get_state() is None
    assert len(mgr.get_history()) == 0
    assert len(mgr.list_snapshots()) == 0


def test_manager_disable_enable() -> None:
    mgr = DynamicsStateManager()
    assert mgr.is_enabled() is True
    mgr.disable()
    assert mgr.is_enabled() is False
    try:
        mgr.initialize(state())
        assert False, "Should have raised RuntimeError"
    except RuntimeError:
        pass
    mgr.enable()
    assert mgr.is_enabled() is True
    mgr.initialize(state())


def test_manager_ablate_domain() -> None:
    mgr = DynamicsStateManager()
    s1 = signal(domain=SignalDomain.EXPLORATION, signal_id="s1")
    s2 = signal(domain=SignalDomain.SOCIAL_AFFILIATION, signal_id="s2")
    st = state(signals=(s1, s2))
    mgr.initialize(st)
    mgr.ablate("SOCIAL_AFFILIATION")
    new_state = mgr.get_state()
    assert new_state is not None
    domains = {s.domain for s in new_state.signals}
    assert SignalDomain.EXPLORATION in domains
    assert SignalDomain.SOCIAL_AFFILIATION not in domains


def test_manager_ablate_all() -> None:
    mgr = DynamicsStateManager()
    s = state()
    mgr.initialize(s)
    mgr.ablate()
    assert mgr.is_enabled() is False