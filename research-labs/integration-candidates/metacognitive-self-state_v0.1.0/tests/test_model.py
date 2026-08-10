from metacognitive_self_state import (
    MetacognitiveCapacity,
    MetacognitiveDepth,
    MetacognitiveState,
    MetacognitiveStateManager,
    SelfModelComponent,
    SelfModelLayer,
)


def component(
    layer: SelfModelLayer = SelfModelLayer.REFLECTIVE,
    capacity: MetacognitiveCapacity = MetacognitiveCapacity.SELF_ATTRIBUTION,
    confidence: float = 0.7,
    **overrides: str | tuple[str, ...],
) -> SelfModelComponent:
    values = {
        "component_id": "comp-1",
        "layer": layer,
        "capacity": capacity,
        "confidence": confidence,
        "evidence_refs": ("evidence-1",),
    }
    values.update(overrides)
    return SelfModelComponent(**values)


def state(
    *components: SelfModelComponent,
    depth: MetacognitiveDepth = MetacognitiveDepth.LEVEL_2_CONFIDENCE_ESTIMATION,
    layers: tuple[SelfModelLayer, ...] = (SelfModelLayer.REFLECTIVE,),
    uncertainty: float = 0.3,
    conflict: bool = False,
) -> MetacognitiveState:
    return MetacognitiveState(
        state_id="state-1",
        subject_ref="candidate-subject",
        context_ref="context-1",
        components=tuple(components) if components else (component(),),
        current_depth=depth,
        active_layers=layers,
        uncertainty_estimate=uncertainty,
        conflict_detected=conflict,
    )


def test_component_validation_requires_non_empty_id() -> None:
    try:
        SelfModelComponent(
            component_id="",
            layer=SelfModelLayer.REFLECTIVE,
            capacity=MetacognitiveCapacity.SELF_ATTRIBUTION,
            confidence=0.5,
            evidence_refs=("e1",),
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "component_id must be non-empty" in str(e)


def test_component_validation_requires_evidence() -> None:
    try:
        SelfModelComponent(
            component_id="comp-1",
            layer=SelfModelLayer.REFLECTIVE,
            capacity=MetacognitiveCapacity.SELF_ATTRIBUTION,
            confidence=0.5,
            evidence_refs=(),
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "at least one evidence_ref is required" in str(e)


def test_component_confidence_bounds() -> None:
    try:
        SelfModelComponent(
            component_id="comp-1",
            layer=SelfModelLayer.REFLECTIVE,
            capacity=MetacognitiveCapacity.SELF_ATTRIBUTION,
            confidence=1.5,
            evidence_refs=("e1",),
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "confidence must be between 0.0 and 1.0" in str(e)


def test_state_canonical_effect_must_be_none() -> None:
    try:
        MetacognitiveState(
            state_id="s1",
            subject_ref="subj",
            context_ref="ctx",
            components=(component(),),
            current_depth=MetacognitiveDepth.LEVEL_1_ERROR_DETECTION,
            active_layers=(SelfModelLayer.REFLECTIVE,),
            uncertainty_estimate=0.2,
            conflict_detected=False,
            canonical_effect="SOME_EFFECT",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "canonical_effect=NONE" in str(e)


def test_state_phenomenal_experience_not_established() -> None:
    try:
        MetacognitiveState(
            state_id="s1",
            subject_ref="subj",
            context_ref="ctx",
            components=(component(),),
            current_depth=MetacognitiveDepth.LEVEL_1_ERROR_DETECTION,
            active_layers=(SelfModelLayer.REFLECTIVE,),
            uncertainty_estimate=0.2,
            conflict_detected=False,
            phenomenal_experience_claim="CLAIMED",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "phenomenal experience must remain NOT_ESTABLISHED" in str(e)


def test_state_get_components_by_layer() -> None:
    comp1 = component(layer=SelfModelLayer.REFLECTIVE, component_id="c1")
    comp2 = component(layer=SelfModelLayer.METACOGNITIVE, component_id="c2")
    s = state(comp1, comp2)
    reflective = s.get_components_by_layer(SelfModelLayer.REFLECTIVE)
    assert len(reflective) == 1
    assert reflective[0].component_id == "c1"


def test_state_get_components_by_capacity() -> None:
    comp1 = component(capacity=MetacognitiveCapacity.SELF_ATTRIBUTION, component_id="c1")
    comp2 = component(capacity=MetacognitiveCapacity.UNCERTAINTY_MONITORING, component_id="c2")
    s = state(comp1, comp2)
    attr = s.get_components_by_capacity(MetacognitiveCapacity.SELF_ATTRIBUTION)
    assert len(attr) == 1
    assert attr[0].component_id == "c1"


def test_state_max_confidence() -> None:
    comp1 = component(confidence=0.3, component_id="c1")
    comp2 = component(confidence=0.9, component_id="c2")
    s = state(comp1, comp2)
    assert s.max_confidence() == 0.9


def test_manager_initialize_and_get() -> None:
    mgr = MetacognitiveStateManager(deterministic_seed=42)
    s = state()
    mgr.initialize(s)
    assert mgr.get_state() is s
    assert len(mgr.get_history()) == 1
    assert mgr.get_history()[0].transition_type == "INITIALIZE"


def test_manager_transition() -> None:
    mgr = MetacognitiveStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    s2 = state(state_id="state-2", components=(component(component_id="c2"),))
    mgr.transition(s2, transition_type="UPDATE", reason="Test transition")
    assert mgr.get_state() is s2
    history = mgr.get_history()
    assert len(history) == 2
    assert history[1].transition_type == "UPDATE"
    assert history[1].from_state_id == "state-1"
    assert history[1].to_state_id == "state-2"


def test_manager_snapshot_and_restore() -> None:
    mgr = MetacognitiveStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    snap = mgr.snapshot("test-snap")
    assert snap.snapshot_id == "test-snap"
    assert snap.state is s1
    assert "test-snap" in mgr.list_snapshots()

    s2 = state(state_id="state-2", components=(component(component_id="c2"),))
    mgr.transition(s2)
    restored = mgr.restore("test-snap")
    assert restored is s1
    assert mgr.get_state() is s1


def test_manager_reset() -> None:
    mgr = MetacognitiveStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    mgr.snapshot("snap1")
    mgr.reset()
    assert mgr.get_state() is None
    assert len(mgr.get_history()) == 0
    assert len(mgr.list_snapshots()) == 0


def test_manager_disable_enable() -> None:
    mgr = MetacognitiveStateManager()
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


def test_manager_ablate_capacity() -> None:
    mgr = MetacognitiveStateManager()
    comp1 = component(capacity=MetacognitiveCapacity.SELF_ATTRIBUTION, component_id="c1")
    comp2 = component(capacity=MetacognitiveCapacity.UNCERTAINTY_MONITORING, component_id="c2")
    s = state(comp1, comp2)
    mgr.initialize(s)
    mgr.ablate("SELF_ATTRIBUTION")
    new_state = mgr.get_state()
    assert new_state is not None
    capacities = {c.capacity for c in new_state.components}
    assert MetacognitiveCapacity.SELF_ATTRIBUTION not in capacities
    assert MetacognitiveCapacity.UNCERTAINTY_MONITORING in capacities


def test_manager_ablate_all() -> None:
    mgr = MetacognitiveStateManager()
    s = state()
    mgr.initialize(s)
    mgr.ablate()
    assert mgr.is_enabled() is False