from longitudinal_state_transition import (
    LongitudinalConfig,
    LongitudinalState,
    LongitudinalStateManager,
    TransitionEvent,
    TransitionType,
    TransitionDirection,
)


def config(**overrides: str | int | float | tuple[str, ...]) -> LongitudinalConfig:
    values = {
        "config_id": "config-1",
        "subject_ref": "subject-1",
        "tracked_dimensions": ("metacognitive_depth", "embodiment_stability", "affective_tone"),
        "window_size": 10,
        "sensitivity_threshold": 0.3,
    }
    values.update(overrides)
    return LongitudinalConfig(**values)


def event(
    event_id: str = "event-1",
    transition_type: TransitionType = TransitionType.GRADUAL_DRIFT,
    **overrides: str | float | TransitionDirection | int,
) -> TransitionEvent:
    values = {
        "event_id": event_id,
        "transition_type": transition_type,
        "direction": TransitionDirection.FORWARD,
        "magnitude": 0.2,
        "from_state_signature": "sig-1",
        "to_state_signature": "sig-2",
        "timestamp": "2024-01-01T00:00:00Z",
    }
    values.update(overrides)
    return TransitionEvent(**values)


def state(
    state_id: str = "state-1",
    **overrides: str | float | dict[str, float] | tuple[dict[str, float], ...] | tuple[TransitionEvent, ...] | TransitionDirection,
) -> LongitudinalState:
    cfg = config()
    values = {
        "state_id": state_id,
        "config": cfg,
        "current_signature": "sig-1",
        "dimension_values": {"metacognitive_depth": 0.5, "embodiment_stability": 0.7, "affective_tone": 0.4},
        "trajectory_history": (),
        "transition_events": (),
        "stability_index": 0.8,
        "trend_direction": TransitionDirection.FORWARD,
    }
    values.update(overrides)
    return LongitudinalState(**values)


def test_config_validation() -> None:
    try:
        LongitudinalConfig(
            config_id="c1",
            subject_ref="s1",
            tracked_dimensions=(),
            window_size=10,
            sensitivity_threshold=0.5,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "at least one dimension must be tracked" in str(e)


def test_config_window_size() -> None:
    try:
        LongitudinalConfig(
            config_id="c1",
            subject_ref="s1",
            tracked_dimensions=("dim1",),
            window_size=0,
            sensitivity_threshold=0.5,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "window_size must be positive" in str(e)


def test_event_validation() -> None:
    try:
        TransitionEvent(
            event_id="",
            transition_type=TransitionType.GRADUAL_DRIFT,
            direction=TransitionDirection.FORWARD,
            magnitude=0.5,
            from_state_signature="sig1",
            to_state_signature="sig2",
            timestamp="2024-01-01T00:00:00Z",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "event_id must be non-empty" in str(e)


def test_event_magnitude_bounds() -> None:
    try:
        TransitionEvent(
            event_id="e1",
            transition_type=TransitionType.GRADUAL_DRIFT,
            direction=TransitionDirection.FORWARD,
            magnitude=1.5,
            from_state_signature="sig1",
            to_state_signature="sig2",
            timestamp="2024-01-01T00:00:00Z",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "magnitude must be between 0.0 and 1.0" in str(e)


def test_state_validation() -> None:
    try:
        LongitudinalState(
            state_id="s1",
            config=config(),
            current_signature="sig1",
            dimension_values={"dim1": 0.5},
            trajectory_history=(),
            transition_events=(),
            stability_index=0.8,
            trend_direction=TransitionDirection.FORWARD,
            trajectory_identity_claim="CLAIMED",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "trajectory identity must remain NOT_ESTABLISHED" in str(e)


def test_state_dimension_bounds() -> None:
    try:
        LongitudinalState(
            state_id="s1",
            config=config(),
            current_signature="sig1",
            dimension_values={"dim1": 1.5},
            trajectory_history=(),
            transition_events=(),
            stability_index=0.8,
            trend_direction=TransitionDirection.FORWARD,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "dimension_values[dim1] must be between 0.0 and 1.0" in str(e)


def test_state_history_bounds() -> None:
    try:
        LongitudinalState(
            state_id="s1",
            config=config(),
            current_signature="sig1",
            dimension_values={"dim1": 0.5},
            trajectory_history=({"dim1": 1.5},),
            transition_events=(),
            stability_index=0.8,
            trend_direction=TransitionDirection.FORWARD,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "trajectory_history point [dim1] must be between 0.0 and 1.0" in str(e)


def test_state_get_latest_event() -> None:
    s1 = state(transition_events=())
    assert s1.get_latest_event() is None

    e1 = event(event_id="e1")
    e2 = event(event_id="e2", transition_type=TransitionType.PHASE_SHIFT)
    s2 = state(transition_events=(e1, e2))
    assert s2.get_latest_event() is e2


def test_state_get_events_by_type() -> None:
    e1 = event(event_id="e1", transition_type=TransitionType.GRADUAL_DRIFT)
    e2 = event(event_id="e2", transition_type=TransitionType.PHASE_SHIFT)
    e3 = event(event_id="e3", transition_type=TransitionType.GRADUAL_DRIFT)
    s = state(transition_events=(e1, e2, e3))
    drift_events = s.get_events_by_type(TransitionType.GRADUAL_DRIFT)
    assert len(drift_events) == 2
    phase_events = s.get_events_by_type(TransitionType.PHASE_SHIFT)
    assert len(phase_events) == 1


def test_state_dimension_trend() -> None:
    s = state(
        trajectory_history=(
            {"metacognitive_depth": 0.3},
            {"metacognitive_depth": 0.5},
            {"metacognitive_depth": 0.7},
        ),
        dimension_values={"metacognitive_depth": 0.7},
    )
    trend = s.dimension_trend("metacognitive_depth")
    assert abs(trend - 0.1333) < 0.01  # (0.7 - 0.3) / 3

    trend_window = s.dimension_trend("metacognitive_depth", window=2)
    assert abs(trend_window - 0.1) < 0.01  # (0.7 - 0.5) / 2


def test_state_is_stable() -> None:
    cfg = config(sensitivity_threshold=0.5)
    s1 = state(config=cfg, stability_index=0.8)
    assert s1.is_stable() is True

    s2 = state(config=cfg, stability_index=0.3)
    assert s2.is_stable() is False


def test_manager_initialize_and_get() -> None:
    mgr = LongitudinalStateManager(deterministic_seed=42)
    s = state()
    mgr.initialize(s)
    assert mgr.get_state() is s
    assert len(mgr.get_history()) == 1
    assert mgr.get_history()[0].transition_type == "INITIALIZE"


def test_manager_transition() -> None:
    mgr = LongitudinalStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    s2 = state(state_id="state-2", current_signature="sig-2", dimension_values={"metacognitive_depth": 0.6})
    mgr.transition(s2, transition_type="DRIFT", reason="Gradual drift detected")
    assert mgr.get_state() is s2
    history = mgr.get_history()
    assert len(history) == 2
    assert history[1].transition_type == "DRIFT"


def test_manager_snapshot_and_restore() -> None:
    mgr = LongitudinalStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    snap = mgr.snapshot("test-snap")
    assert snap.snapshot_id == "test-snap"

    s2 = state(state_id="state-2")
    mgr.transition(s2)
    restored = mgr.restore("test-snap")
    assert restored is s1


def test_manager_reset() -> None:
    mgr = LongitudinalStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    mgr.snapshot("snap1")
    mgr.reset()
    assert mgr.get_state() is None
    assert len(mgr.get_history()) == 0
    assert len(mgr.list_snapshots()) == 0


def test_manager_disable_enable() -> None:
    mgr = LongitudinalStateManager()
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


def test_manager_ablate_dimension() -> None:
    mgr = LongitudinalStateManager()
    s = state()
    mgr.initialize(s)
    mgr.ablate("affective_tone")
    new_state = mgr.get_state()
    assert new_state is not None
    assert "affective_tone" not in new_state.config.tracked_dimensions
    assert "affective_tone" not in new_state.dimension_values
    assert all("affective_tone" not in h for h in new_state.trajectory_history)


def test_manager_ablate_last_dimension() -> None:
    mgr = LongitudinalStateManager()
    cfg = config(tracked_dimensions=("only_dim",))
    s = state(config=cfg, dimension_values={"only_dim": 0.5})
    mgr.initialize(s)
    mgr.ablate("only_dim")
    assert mgr.is_enabled() is False


def test_manager_ablate_all() -> None:
    mgr = LongitudinalStateManager()
    s = state()
    mgr.initialize(s)
    mgr.ablate()
    assert mgr.is_enabled() is False