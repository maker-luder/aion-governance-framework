from metacognitive_self_state import (
    MetacognitiveCapacity,
    MetacognitiveDepth,
    MetacognitiveState,
    MetacognitiveStateManager,
    SelfModelComponent,
    SelfModelLayer,
)


def component(
    *,
    component_id: str = "comp-1",
    layer: SelfModelLayer = SelfModelLayer.REFLECTIVE,
    capacity: MetacognitiveCapacity = MetacognitiveCapacity.SELF_ATTRIBUTION,
    confidence: float = 0.7,
    evidence_refs: tuple[str, ...] = ("evidence-1",),
) -> SelfModelComponent:
    return SelfModelComponent(
        component_id=component_id,
        layer=layer,
        capacity=capacity,
        confidence=confidence,
        evidence_refs=evidence_refs,
    )


def state(
    components: tuple[SelfModelComponent, ...] | None = None,
    *,
    state_id: str = "state-1",
    subject_ref: str = "candidate-subject",
    context_ref: str = "context-1",
    depth: MetacognitiveDepth = MetacognitiveDepth.LEVEL_2_CONFIDENCE_ESTIMATION,
    layers: tuple[SelfModelLayer, ...] | None = None,
    uncertainty: float = 0.3,
    conflict: bool = False,
) -> MetacognitiveState:
    actual_components = components if components is not None else (component(),)
    actual_layers = (
        layers
        if layers is not None
        else tuple(dict.fromkeys(c.layer for c in actual_components))
    )
    return MetacognitiveState(
        state_id=state_id,
        subject_ref=subject_ref,
        context_ref=context_ref,
        components=actual_components,
        current_depth=depth,
        active_layers=actual_layers,
        uncertainty_estimate=uncertainty,
        conflict_detected=conflict,
    )


def _assert_raises(exc_type: type[Exception], fn, contains: str | None = None) -> None:
    try:
        fn()
        assert False, f"Should have raised {exc_type.__name__}"
    except exc_type as exc:
        if contains is not None:
            assert contains in str(exc)


def test_component_validation_requires_non_empty_id() -> None:
    _assert_raises(
        ValueError,
        lambda: component(component_id=""),
        "component_id must be non-empty",
    )


def test_component_validation_requires_non_empty_evidence() -> None:
    _assert_raises(
        ValueError,
        lambda: component(evidence_refs=()),
        "at least one non-empty evidence_ref is required",
    )
    _assert_raises(
        ValueError,
        lambda: component(evidence_refs=("",)),
        "at least one non-empty evidence_ref is required",
    )


def test_component_confidence_bounds() -> None:
    _assert_raises(
        ValueError,
        lambda: component(confidence=1.5),
        "confidence must be between 0.0 and 1.0",
    )


def test_state_canonical_effect_must_be_none() -> None:
    _assert_raises(
        ValueError,
        lambda: MetacognitiveState(
            state_id="s1",
            subject_ref="subj",
            context_ref="ctx",
            components=(component(),),
            current_depth=MetacognitiveDepth.LEVEL_1_ERROR_DETECTION,
            active_layers=(SelfModelLayer.REFLECTIVE,),
            uncertainty_estimate=0.2,
            conflict_detected=False,
            canonical_effect="SOME_EFFECT",
        ),
        "canonical_effect=NONE",
    )


def test_state_phenomenal_experience_not_established() -> None:
    _assert_raises(
        ValueError,
        lambda: MetacognitiveState(
            state_id="s1",
            subject_ref="subj",
            context_ref="ctx",
            components=(component(),),
            current_depth=MetacognitiveDepth.LEVEL_1_ERROR_DETECTION,
            active_layers=(SelfModelLayer.REFLECTIVE,),
            uncertainty_estimate=0.2,
            conflict_detected=False,
            phenomenal_experience_claim="CLAIMED",
        ),
        "phenomenal experience must remain NOT_ESTABLISHED",
    )


def test_state_requires_component_layers_to_be_active() -> None:
    c = component(layer=SelfModelLayer.METACOGNITIVE)
    _assert_raises(
        ValueError,
        lambda: state((c,), layers=(SelfModelLayer.REFLECTIVE,)),
        "component layers must be active",
    )


def test_state_get_components_by_layer() -> None:
    comp1 = component(component_id="c1", layer=SelfModelLayer.REFLECTIVE)
    comp2 = component(component_id="c2", layer=SelfModelLayer.METACOGNITIVE)
    s = state((comp1, comp2))
    reflective = s.get_components_by_layer(SelfModelLayer.REFLECTIVE)
    assert len(reflective) == 1
    assert reflective[0].component_id == "c1"


def test_state_get_components_by_capacity() -> None:
    comp1 = component(component_id="c1", capacity=MetacognitiveCapacity.SELF_ATTRIBUTION)
    comp2 = component(component_id="c2", capacity=MetacognitiveCapacity.UNCERTAINTY_MONITORING)
    s = state((comp1, comp2))
    attr = s.get_components_by_capacity(MetacognitiveCapacity.SELF_ATTRIBUTION)
    assert len(attr) == 1
    assert attr[0].component_id == "c1"


def test_state_max_confidence() -> None:
    comp1 = component(component_id="c1", confidence=0.3)
    comp2 = component(component_id="c2", confidence=0.9)
    assert state((comp1, comp2)).max_confidence() == 0.9


def test_manager_initialize_and_get() -> None:
    mgr = MetacognitiveStateManager(deterministic_seed=42)
    s = state()
    mgr.initialize(s)
    assert mgr.get_state() is s
    assert len(mgr.get_history()) == 1
    assert mgr.get_history()[0].transition_type == "INITIALIZE"
    assert mgr.get_history()[0].deterministic_seed == 42


def test_manager_transition() -> None:
    mgr = MetacognitiveStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    s2 = state(
        (component(component_id="c2"),),
        state_id="state-2",
    )
    mgr.transition(s2, transition_type="UPDATE", reason="Test transition")
    assert mgr.get_state() is s2
    history = mgr.get_history()
    assert len(history) == 2
    assert history[1].from_state_id == "state-1"
    assert history[1].to_state_id == "state-2"


def test_manager_rejects_implicit_subject_rebind() -> None:
    mgr = MetacognitiveStateManager()
    mgr.initialize(state(subject_ref="subject-A"))
    foreign = state(state_id="foreign", subject_ref="subject-B")
    _assert_raises(
        ValueError,
        lambda: mgr.transition(foreign),
        "subject_ref cannot change",
    )
    assert mgr.get_state() is not None
    assert mgr.get_state().subject_ref == "subject-A"


def test_manager_snapshot_and_restore_records_real_source_state() -> None:
    mgr = MetacognitiveStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    snap = mgr.snapshot("test-snap")
    assert snap.snapshot_id == "test-snap"

    s2 = state((component(component_id="c2"),), state_id="state-2")
    mgr.transition(s2)
    restored = mgr.restore("test-snap")
    assert restored is s1
    assert mgr.get_state() is s1
    restore_transition = mgr.get_history()[-1]
    assert restore_transition.transition_type == "RESTORE"
    assert restore_transition.from_state_id == "state-2"
    assert restore_transition.to_state_id == "state-1"


def test_manager_reset() -> None:
    mgr = MetacognitiveStateManager(deterministic_seed=42)
    mgr.initialize(state())
    mgr.snapshot("snap1")
    mgr.reset()
    assert mgr.get_state() is None
    assert len(mgr.get_history()) == 0
    assert len(mgr.list_snapshots()) == 0


def test_manager_disable_enable() -> None:
    mgr = MetacognitiveStateManager()
    mgr.disable()
    assert mgr.is_enabled() is False
    _assert_raises(RuntimeError, lambda: mgr.initialize(state()))
    mgr.enable()
    mgr.initialize(state())
    assert mgr.is_enabled() is True


def test_manager_ablate_capacity_records_transition_and_updates_layers() -> None:
    mgr = MetacognitiveStateManager()
    comp1 = component(
        component_id="c1",
        layer=SelfModelLayer.REFLECTIVE,
        capacity=MetacognitiveCapacity.SELF_ATTRIBUTION,
    )
    comp2 = component(
        component_id="c2",
        layer=SelfModelLayer.METACOGNITIVE,
        capacity=MetacognitiveCapacity.UNCERTAINTY_MONITORING,
    )
    mgr.initialize(state((comp1, comp2)))
    mgr.ablate("SELF_ATTRIBUTION")

    new_state = mgr.get_state()
    assert new_state is not None
    capacities = {c.capacity for c in new_state.components}
    assert MetacognitiveCapacity.SELF_ATTRIBUTION not in capacities
    assert new_state.active_layers == (SelfModelLayer.METACOGNITIVE,)
    transition = mgr.get_history()[-1]
    assert transition.transition_type == "ABLATE_CAPACITY"
    assert transition.from_state_id == "state-1"
    assert transition.to_state_id == new_state.state_id


def test_manager_ablate_final_capacity_disables_without_invalid_empty_state() -> None:
    mgr = MetacognitiveStateManager()
    mgr.initialize(state())
    mgr.ablate("SELF_ATTRIBUTION")
    assert mgr.is_enabled() is False
    assert mgr.get_state() is not None
    transition = mgr.get_history()[-1]
    assert transition.transition_type == "ABLATE_CAPACITY_DISABLE"
    assert transition.to_state_id == "MODULE_DISABLED"


def test_manager_ablate_missing_capacity_is_not_silent() -> None:
    mgr = MetacognitiveStateManager()
    mgr.initialize(state())
    _assert_raises(
        KeyError,
        lambda: mgr.ablate("CONFLICT_DETECTION"),
        "not active",
    )


def test_manager_ablate_all_records_control_event() -> None:
    mgr = MetacognitiveStateManager()
    mgr.initialize(state())
    mgr.ablate()
    assert mgr.is_enabled() is False
    transition = mgr.get_history()[-1]
    assert transition.transition_type == "ABLATE_MODULE"
    assert transition.to_state_id == "MODULE_DISABLED"


def test_timestamp_provider_allows_reproducible_trace_time() -> None:
    stamps = iter(("T0", "T1", "T2"))
    mgr = MetacognitiveStateManager(
        deterministic_seed=7,
        timestamp_provider=lambda: next(stamps),
    )
    mgr.initialize(state())
    mgr.snapshot("snap")
    mgr.ablate()
    assert [t.timestamp for t in mgr.get_history()] == ["T0", "T2"]
    assert mgr.list_snapshots() == ("snap",)
