from embodiment_migration import (
    MigrationConfig,
    MigrationEvent,
    MigrationPhase,
    MigrationState,
    MigrationStateManager,
    MigrationTrigger,
    SourceTargetPair,
)


def source_target_pair(**overrides: str | float) -> SourceTargetPair:
    values = {
        "source_embodiment_id": "source-001",
        "target_embodiment_id": "target-001",
        "source_template_ref": "template-v1",
        "target_template_ref": "template-v2",
        "compatibility_score": 0.85,
    }
    values.update(overrides)
    return SourceTargetPair(**values)


def config(**overrides: str | int | float | MigrationTrigger | SourceTargetPair) -> MigrationConfig:
    values = {
        "config_id": "config-1",
        "agent_id": "agent-1",
        "pair": source_target_pair(),
        "trigger": MigrationTrigger.HARDWARE_UPGRADE,
        "max_duration_ms": 300000,
        "fidelity_threshold": 0.95,
        "rollback_enabled": True,
    }
    values.update(overrides)
    return MigrationConfig(**values)


def event(
    event_id: str = "event-1",
    phase: MigrationPhase = MigrationPhase.PREPARATION,
    **overrides: str | float,
) -> MigrationEvent:
    values = {
        "event_id": event_id,
        "phase": phase,
        "description": "Test event",
        "fidelity": 0.0,
        "timestamp": "2024-01-01T00:00:00Z",
    }
    values.update(overrides)
    return MigrationEvent(**values)


def state(
    state_id: str = "state-1",
    **overrides: str | float | MigrationPhase | MigrationConfig | tuple[MigrationEvent, ...] | bool,
) -> MigrationState:
    cfg = config()
    values = {
        "state_id": state_id,
        "config": cfg,
        "current_phase": MigrationPhase.PREPARATION,
        "progress": 0.0,
        "fidelity_achieved": 0.0,
        "events": (),
        "rollback_initiated": False,
    }
    values.update(overrides)
    return MigrationState(**values)


def test_source_target_pair_validation() -> None:
    try:
        SourceTargetPair(
            source_embodiment_id="",
            target_embodiment_id="t1",
            source_template_ref="tmpl1",
            target_template_ref="tmpl2",
            compatibility_score=0.5,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "source_embodiment_id must be non-empty" in str(e)


def test_source_target_pair_bounds() -> None:
    try:
        SourceTargetPair(
            source_embodiment_id="s1",
            target_embodiment_id="t1",
            source_template_ref="tmpl1",
            target_template_ref="tmpl2",
            compatibility_score=1.5,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "compatibility_score must be between 0.0 and 1.0" in str(e)


def test_config_validation() -> None:
    try:
        MigrationConfig(
            config_id="c1",
            agent_id="a1",
            pair=source_target_pair(),
            trigger=MigrationTrigger.HARDWARE_UPGRADE,
            max_duration_ms=-1,
            fidelity_threshold=0.95,
            rollback_enabled=True,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "max_duration_ms must be positive" in str(e)


def test_config_fidelity_threshold() -> None:
    try:
        MigrationConfig(
            config_id="c1",
            agent_id="a1",
            pair=source_target_pair(),
            trigger=MigrationTrigger.HARDWARE_UPGRADE,
            max_duration_ms=1000,
            fidelity_threshold=1.5,
            rollback_enabled=True,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "fidelity_threshold must be between 0.0 and 1.0" in str(e)


def test_event_validation() -> None:
    try:
        MigrationEvent(
            event_id="",
            phase=MigrationPhase.PREPARATION,
            description="Test",
            fidelity=0.5,
            timestamp="2024-01-01T00:00:00Z",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "event_id must be non-empty" in str(e)


def test_state_validation() -> None:
    try:
        MigrationState(
            state_id="s1",
            config=config(),
            current_phase=MigrationPhase.PREPARATION,
            progress=0.0,
            fidelity_achieved=0.0,
            events=(),
            rollback_initiated=False,
            identity_continuity_claim="CLAIMED",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "identity continuity must remain NOT_ESTABLISHED" in str(e)


def test_state_is_terminal() -> None:
    s1 = state(current_phase=MigrationPhase.PREPARATION)
    assert s1.is_terminal() is False

    s2 = state(current_phase=MigrationPhase.COMPLETE)
    assert s2.is_terminal() is True

    s3 = state(current_phase=MigrationPhase.ROLLBACK)
    assert s3.is_terminal() is True

    s4 = state(current_phase=MigrationPhase.FAILED)
    assert s4.is_terminal() is True


def test_state_get_latest_event() -> None:
    s1 = state(events=())
    assert s1.get_latest_event() is None

    e1 = event(event_id="e1", phase=MigrationPhase.PREPARATION)
    e2 = event(event_id="e2", phase=MigrationPhase.VALIDATION)
    s2 = state(events=(e1, e2))
    assert s2.get_latest_event() is e2


def test_manager_initialize_and_get() -> None:
    mgr = MigrationStateManager(deterministic_seed=42)
    s = state()
    mgr.initialize(s)
    assert mgr.get_state() is s
    assert len(mgr.get_history()) == 1
    assert mgr.get_history()[0].transition_type == "INITIALIZE"


def test_manager_transition() -> None:
    mgr = MigrationStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    s2 = state(state_id="state-2", current_phase=MigrationPhase.VALIDATION, progress=0.2)
    mgr.transition(s2, transition_type="PHASE_ADVANCE", reason="Validation started")
    assert mgr.get_state() is s2
    history = mgr.get_history()
    assert len(history) == 2
    assert history[1].transition_type == "PHASE_ADVANCE"


def test_manager_snapshot_and_restore() -> None:
    mgr = MigrationStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    snap = mgr.snapshot("test-snap")
    assert snap.snapshot_id == "test-snap"

    s2 = state(state_id="state-2")
    mgr.transition(s2)
    restored = mgr.restore("test-snap")
    assert restored is s1


def test_manager_reset() -> None:
    mgr = MigrationStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    mgr.snapshot("snap1")
    mgr.reset()
    assert mgr.get_state() is None
    assert len(mgr.get_history()) == 0
    assert len(mgr.list_snapshots()) == 0


def test_manager_disable_enable() -> None:
    mgr = MigrationStateManager()
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


def test_manager_ablate() -> None:
    mgr = MigrationStateManager()
    s = state()
    mgr.initialize(s)
    mgr.ablate("VALIDATION")
    assert mgr.is_enabled() is False