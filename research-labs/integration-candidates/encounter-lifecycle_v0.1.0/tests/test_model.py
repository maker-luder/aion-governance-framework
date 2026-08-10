from encounter_lifecycle import (
    EncounterConfig,
    EncounterEvent,
    EncounterPhase,
    EncounterState,
    EncounterStateManager,
    EncounterType,
    ParticipantModel,
    ParticipantRole,
)


def participant(
    participant_id: str = "p1",
    role: ParticipantRole = ParticipantRole.EQUAL,
    **overrides: float,
) -> ParticipantModel:
    values = {
        "participant_id": participant_id,
        "role": role,
        "agency_level": 0.7,
        "familiarity": 0.5,
        "trust_estimate": 0.6,
        "power_differential": 0.0,
    }
    values.update(overrides)
    return ParticipantModel(**values)


def config(
    config_id: str = "config-1",
    **overrides: str | int | float | EncounterType | tuple[ParticipantModel, ...],
) -> EncounterConfig:
    values = {
        "config_id": config_id,
        "encounter_type": EncounterType.SOCIAL,
        "participants": (participant("p1"), participant("p2", role=ParticipantRole.RECIPIENT)),
        "expected_duration_ms": 3600000,
        "depth_threshold": 0.7,
    }
    values.update(overrides)
    return EncounterConfig(**values)


def event(
    event_id: str = "event-1",
    phase: EncounterPhase = EncounterPhase.INITIATION,
    **overrides: str | float | tuple[str, ...],
) -> EncounterEvent:
    values = {
        "event_id": event_id,
        "phase": phase,
        "description": "Test event",
        "intensity": 0.5,
        "participants_involved": ("p1", "p2"),
        "timestamp": "2024-01-01T00:00:00Z",
    }
    values.update(overrides)
    return EncounterEvent(**values)


def state(
    state_id: str = "state-1",
    **overrides: str | float | EncounterPhase | EncounterConfig | tuple[EncounterEvent, ...] | tuple[str, ...] | tuple[float, ...],
) -> EncounterState:
    cfg = config()
    values = {
        "state_id": state_id,
        "config": cfg,
        "current_phase": EncounterPhase.PRE_ENCOUNTER,
        "progress": 0.0,
        "current_depth": 0.0,
        "intensity_trajectory": (),
        "events": (),
        "active_participants": ("p1", "p2"),
    }
    values.update(overrides)
    return EncounterState(**values)


def test_participant_validation() -> None:
    try:
        ParticipantModel(
            participant_id="",
            role=ParticipantRole.EQUAL,
            agency_level=0.5,
            familiarity=0.5,
            trust_estimate=0.5,
            power_differential=0.0,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "participant_id must be non-empty" in str(e)


def test_participant_bounds() -> None:
    try:
        ParticipantModel(
            participant_id="p1",
            role=ParticipantRole.EQUAL,
            agency_level=1.5,
            familiarity=0.5,
            trust_estimate=0.5,
            power_differential=0.0,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "agency_level must be between 0.0 and 1.0" in str(e)


def test_participant_power_differential() -> None:
    try:
        ParticipantModel(
            participant_id="p1",
            role=ParticipantRole.EQUAL,
            agency_level=0.5,
            familiarity=0.5,
            trust_estimate=0.5,
            power_differential=1.5,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "power_differential must be between -1.0 and 1.0" in str(e)


def test_config_min_participants() -> None:
    try:
        EncounterConfig(
            config_id="c1",
            encounter_type=EncounterType.SOCIAL,
            participants=(participant("p1"),),
            expected_duration_ms=1000,
            depth_threshold=0.5,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "at least two participants required" in str(e)


def test_event_validation() -> None:
    try:
        EncounterEvent(
            event_id="",
            phase=EncounterPhase.INITIATION,
            description="Test",
            intensity=0.5,
            participants_involved=("p1",),
            timestamp="2024-01-01T00:00:00Z",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "event_id must be non-empty" in str(e)


def test_event_no_participants() -> None:
    try:
        EncounterEvent(
            event_id="e1",
            phase=EncounterPhase.INITIATION,
            description="Test",
            intensity=0.5,
            participants_involved=(),
            timestamp="2024-01-01T00:00:00Z",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "at least one participant must be involved" in str(e)


def test_state_validation() -> None:
    try:
        EncounterState(
            state_id="s1",
            config=config(),
            current_phase=EncounterPhase.PRE_ENCOUNTER,
            progress=0.0,
            current_depth=0.0,
            intensity_trajectory=(),
            events=(),
            active_participants=("p1", "p2"),
            relationship_claim="CLAIMED",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "relationship must remain NOT_ESTABLISHED" in str(e)


def test_state_is_terminal() -> None:
    s1 = state(current_phase=EncounterPhase.ENGAGEMENT)
    assert s1.is_terminal() is False

    s2 = state(current_phase=EncounterPhase.POST_ENCOUNTER)
    assert s2.is_terminal() is True

    s3 = state(current_phase=EncounterPhase.TERMINATED)
    assert s3.is_terminal() is True


def test_state_get_participant() -> None:
    st = state()
    p = st.get_participant("p1")
    assert p is not None
    assert p.participant_id == "p1"
    assert st.get_participant("p3") is None


def test_state_average_intensity() -> None:
    s1 = state(intensity_trajectory=())
    assert s1.average_intensity() == 0.0

    s2 = state(intensity_trajectory=(0.3, 0.5, 0.7, 0.6))
    assert abs(s2.average_intensity() - 0.525) < 0.001


def test_manager_initialize_and_get() -> None:
    mgr = EncounterStateManager(deterministic_seed=42)
    s = state()
    mgr.initialize(s)
    assert mgr.get_state() is s
    assert len(mgr.get_history()) == 1
    assert mgr.get_history()[0].transition_type == "INITIALIZE"


def test_manager_transition() -> None:
    mgr = EncounterStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    s2 = state(state_id="state-2", current_phase=EncounterPhase.INITIATION, progress=0.1)
    mgr.transition(s2, transition_type="PHASE_ADVANCE", reason="Encounter initiated")
    assert mgr.get_state() is s2
    history = mgr.get_history()
    assert len(history) == 2
    assert history[1].transition_type == "PHASE_ADVANCE"


def test_manager_snapshot_and_restore() -> None:
    mgr = EncounterStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    snap = mgr.snapshot("test-snap")
    assert snap.snapshot_id == "test-snap"

    s2 = state(state_id="state-2")
    mgr.transition(s2)
    restored = mgr.restore("test-snap")
    assert restored is s1


def test_manager_reset() -> None:
    mgr = EncounterStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    mgr.snapshot("snap1")
    mgr.reset()
    assert mgr.get_state() is None
    assert len(mgr.get_history()) == 0
    assert len(mgr.list_snapshots()) == 0


def test_manager_disable_enable() -> None:
    mgr = EncounterStateManager()
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


def test_manager_ablate_participant() -> None:
    mgr = EncounterStateManager()
    p1 = participant("p1")
    p2 = participant("p2")
    p3 = participant("p3")
    cfg = config(participants=(p1, p2, p3))
    s = state(config=cfg, active_participants=("p1", "p2", "p3"))
    mgr.initialize(s)
    mgr.ablate("p3")
    new_state = mgr.get_state()
    assert new_state is not None
    participants = {p.participant_id for p in new_state.config.participants}
    assert "p1" in participants
    assert "p2" in participants
    assert "p3" not in participants


def test_manager_ablate_too_few() -> None:
    mgr = EncounterStateManager()
    p1 = participant("p1")
    p2 = participant("p2")
    cfg = config(participants=(p1, p2))
    s = state(config=cfg)
    mgr.initialize(s)
    mgr.ablate("p2")
    assert mgr.is_enabled() is False


def test_manager_ablate_all() -> None:
    mgr = EncounterStateManager()
    s = state()
    mgr.initialize(s)
    mgr.ablate()
    assert mgr.is_enabled() is False