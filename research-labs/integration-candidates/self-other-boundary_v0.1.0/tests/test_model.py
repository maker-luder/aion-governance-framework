from self_other_boundary import (
    BoundaryConfiguration,
    BoundaryEvent,
    BoundaryMode,
    BoundaryState,
    BoundaryStateManager,
    OtherModel,
    SelfOtherDistinction,
)


def distinction_weights(**overrides: float) -> dict[SelfOtherDistinction, float]:
    base = {
        SelfOtherDistinction.AGENCY_ATTRIBUTION: 0.25,
        SelfOtherDistinction.SENSORY_PREDICTION_ERROR: 0.20,
        SelfOtherDistinction.AFFECTIVE_RESONANCE: 0.20,
        SelfOtherDistinction.PERSPECTIVE_TAKING: 0.15,
        SelfOtherDistinction.NARRATIVE_DIFFERENTIATION: 0.10,
        SelfOtherDistinction.EMBODIMENT_MAPPING: 0.10,
    }
    base.update(overrides)
    return base


def other_model(
    other_id: str = "other-1",
    **overrides: float | int,
) -> OtherModel:
    values = {
        "other_id": other_id,
        "embodiment_similarity": 0.7,
        "behavioral_predictability": 0.6,
        "affective_resonance": 0.5,
        "perspective_accessibility": 0.4,
        "interaction_history_depth": 10,
    }
    values.update(overrides)
    return OtherModel(**values)


def config(
    config_id: str = "config-1",
    **overrides: BoundaryMode | dict[SelfOtherDistinction, float] | float,
) -> BoundaryConfiguration:
    values = {
        "config_id": config_id,
        "default_mode": BoundaryMode.SEMI_PERMEABLE,
        "distinction_weights": distinction_weights(),
        "permeability_threshold": 0.3,
        "rigidity_threshold": 0.7,
    }
    values.update(overrides)
    return BoundaryConfiguration(**values)


def event(
    event_id: str = "event-1",
    **overrides: str | float,
) -> BoundaryEvent:
    values = {
        "event_id": event_id,
        "event_type": "INTERACTION",
        "self_contribution": 0.6,
        "other_contribution": 0.4,
        "boundary_shift": 0.1,
        "timestamp": "2024-01-01T00:00:00Z",
    }
    values.update(overrides)
    return BoundaryEvent(**values)


def state(
    state_id: str = "state-1",
    **overrides: str | float | tuple[OtherModel, ...] | tuple[SelfOtherDistinction, ...] | BoundaryMode | BoundaryConfiguration | tuple[BoundaryEvent, ...],
) -> BoundaryState:
    cfg = config()
    values = {
        "state_id": state_id,
        "subject_ref": "subject-1",
        "config": cfg,
        "current_mode": BoundaryMode.SEMI_PERMEABLE,
        "active_distinctions": tuple(SelfOtherDistinction),
        "other_models": (other_model(),),
        "boundary_permeability": 0.4,
        "confusion_index": 0.2,
        "recent_events": (event(),),
    }
    values.update(overrides)
    return BoundaryState(**values)


def test_other_model_validation() -> None:
    try:
        OtherModel(
            other_id="",
            embodiment_similarity=0.5,
            behavioral_predictability=0.5,
            affective_resonance=0.5,
            perspective_accessibility=0.5,
            interaction_history_depth=10,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "other_id must be non-empty" in str(e)


def test_other_model_bounds() -> None:
    try:
        OtherModel(
            other_id="o1",
            embodiment_similarity=1.5,
            behavioral_predictability=0.5,
            affective_resonance=0.5,
            perspective_accessibility=0.5,
            interaction_history_depth=10,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "embodiment_similarity must be between 0.0 and 1.0" in str(e)


def test_config_weights_sum_to_one() -> None:
    try:
        BoundaryConfiguration(
            config_id="c1",
            default_mode=BoundaryMode.SEMI_PERMEABLE,
            distinction_weights={SelfOtherDistinction.AGENCY_ATTRIBUTION: 0.5},
            permeability_threshold=0.3,
            rigidity_threshold=0.7,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "distinction_weights must sum to 1.0" in str(e)


def test_config_threshold_order() -> None:
    try:
        BoundaryConfiguration(
            config_id="c1",
            default_mode=BoundaryMode.SEMI_PERMEABLE,
            distinction_weights=distinction_weights(),
            permeability_threshold=0.8,
            rigidity_threshold=0.3,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "permeability_threshold must be < rigidity_threshold" in str(e)


def test_config_canonical_effect() -> None:
    try:
        BoundaryConfiguration(
            config_id="c1",
            default_mode=BoundaryMode.SEMI_PERMEABLE,
            distinction_weights=distinction_weights(),
            permeability_threshold=0.3,
            rigidity_threshold=0.7,
            canonical_effect="EFFECT",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "canonical_effect=NONE" in str(e)


def test_event_bounds() -> None:
    try:
        BoundaryEvent(
            event_id="e1",
            event_type="TEST",
            self_contribution=0.5,
            other_contribution=0.5,
            boundary_shift=1.5,
            timestamp="2024-01-01T00:00:00Z",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "boundary_shift must be between -1.0 and 1.0" in str(e)


def test_state_validation() -> None:
    try:
        BoundaryState(
            state_id="s1",
            subject_ref="subj",
            config=config(),
            current_mode=BoundaryMode.SEMI_PERMEABLE,
            active_distinctions=tuple(SelfOtherDistinction),
            other_models=(other_model(),),
            boundary_permeability=0.4,
            confusion_index=0.2,
            recent_events=(event(),),
            empathy_claim="CLAIMED",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "empathy must remain NOT_ESTABLISHED" in str(e)


def test_state_get_other_model() -> None:
    om1 = other_model("other-1")
    om2 = other_model("other-2")
    s = state(other_models=(om1, om2))
    found = s.get_other_model("other-1")
    assert found is om1
    assert s.get_other_model("other-3") is None


def test_state_distinction_strength() -> None:
    s = state()
    strength = s.distinction_strength(SelfOtherDistinction.AGENCY_ATTRIBUTION)
    assert strength == 0.25


def test_manager_initialize_and_get() -> None:
    mgr = BoundaryStateManager(deterministic_seed=42)
    s = state()
    mgr.initialize(s)
    assert mgr.get_state() is s
    assert len(mgr.get_history()) == 1
    assert mgr.get_history()[0].transition_type == "INITIALIZE"


def test_manager_transition() -> None:
    mgr = BoundaryStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    s2 = state(state_id="state-2")
    mgr.transition(s2, transition_type="BOUNDARY_SHIFT", reason="Interaction event")
    assert mgr.get_state() is s2
    history = mgr.get_history()
    assert len(history) == 2
    assert history[1].transition_type == "BOUNDARY_SHIFT"


def test_manager_snapshot_and_restore() -> None:
    mgr = BoundaryStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    snap = mgr.snapshot("test-snap")
    assert snap.snapshot_id == "test-snap"

    s2 = state(state_id="state-2")
    mgr.transition(s2)
    restored = mgr.restore("test-snap")
    assert restored is s1


def test_manager_reset() -> None:
    mgr = BoundaryStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    mgr.snapshot("snap1")
    mgr.reset()
    assert mgr.get_state() is None
    assert len(mgr.get_history()) == 0
    assert len(mgr.list_snapshots()) == 0


def test_manager_disable_enable() -> None:
    mgr = BoundaryStateManager()
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


def test_manager_ablate_distinction() -> None:
    mgr = BoundaryStateManager()
    s = state()
    mgr.initialize(s)
    mgr.ablate("AGENCY_ATTRIBUTION")
    new_state = mgr.get_state()
    assert new_state is not None
    distinctions = set(new_state.active_distinctions)
    assert SelfOtherDistinction.AGENCY_ATTRIBUTION not in distinctions
    assert SelfOtherDistinction.SENSORY_PREDICTION_ERROR in distinctions
    # Weights should be renormalized
    total = sum(new_state.config.distinction_weights.values())
    assert abs(total - 1.0) < 1e-6


def test_manager_ablate_all() -> None:
    mgr = BoundaryStateManager()
    s = state()
    mgr.initialize(s)
    mgr.ablate()
    assert mgr.is_enabled() is False