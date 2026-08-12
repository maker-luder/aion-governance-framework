import pytest

from self_other_boundary import (
    BoundaryConfiguration,
    BoundaryEvent,
    BoundaryMode,
    BoundaryState,
    BoundaryStateManager,
    OtherModel,
    SelfOtherDistinction,
    SubjectRelation,
)


def distinction_weights() -> dict[SelfOtherDistinction, float]:
    return {
        SelfOtherDistinction.AGENCY_ATTRIBUTION: 0.25,
        SelfOtherDistinction.SENSORY_PREDICTION_ERROR: 0.20,
        SelfOtherDistinction.AFFECTIVE_RESONANCE: 0.20,
        SelfOtherDistinction.PERSPECTIVE_TAKING: 0.15,
        SelfOtherDistinction.NARRATIVE_DIFFERENTIATION: 0.10,
        SelfOtherDistinction.EMBODIMENT_MAPPING: 0.10,
    }


def other_model(
    other_id: str = "other-1",
    relation: SubjectRelation = SubjectRelation.EXTERNAL_OTHER,
) -> OtherModel:
    return OtherModel(
        other_id=other_id,
        relation_to_subject=relation,
        embodiment_similarity=0.7,
        behavioral_predictability=0.6,
        affective_resonance=0.5,
        perspective_accessibility=0.4,
        interaction_history_depth=10,
        evidence_refs=(f"evidence-{other_id}",),
    )


def config(weights: dict[SelfOtherDistinction, float] | None = None) -> BoundaryConfiguration:
    return BoundaryConfiguration(
        config_id="config-1",
        default_mode=BoundaryMode.SEMI_PERMEABLE,
        distinction_weights=weights or distinction_weights(),
        permeability_threshold=0.3,
        rigidity_threshold=0.7,
    )


def event(other_ref: str | None = "other-1", other_contribution: float = 0.4) -> BoundaryEvent:
    return BoundaryEvent(
        event_id="event-1",
        event_type="INTERACTION",
        self_contribution=0.6,
        other_contribution=other_contribution,
        boundary_shift=0.1,
        timestamp="2026-08-10T00:00:00Z",
        other_ref=other_ref,
    )


def state(
    state_id: str = "state-1",
    subject_ref: str = "subject-1",
    cfg: BoundaryConfiguration | None = None,
    others: tuple[OtherModel, ...] | None = None,
    events: tuple[BoundaryEvent, ...] | None = None,
) -> BoundaryState:
    cfg = cfg or config()
    others = others if others is not None else (other_model(),)
    events = events if events is not None else (event(),)
    return BoundaryState(
        state_id=state_id,
        subject_ref=subject_ref,
        config=cfg,
        current_mode=BoundaryMode.SEMI_PERMEABLE,
        active_distinctions=tuple(cfg.distinction_weights),
        other_models=others,
        boundary_permeability=0.4,
        confusion_index=0.2,
        recent_events=events,
    )


def test_other_model_requires_non_empty_id() -> None:
    with pytest.raises(ValueError, match="other_id must be non-empty"):
        OtherModel(
            other_id="",
            relation_to_subject=SubjectRelation.EXTERNAL_OTHER,
            embodiment_similarity=0.5,
            behavioral_predictability=0.5,
            affective_resonance=0.5,
            perspective_accessibility=0.5,
            interaction_history_depth=1,
            evidence_refs=("e1",),
        )


def test_other_model_requires_evidence() -> None:
    with pytest.raises(ValueError, match="evidence_ref"):
        OtherModel(
            other_id="o1",
            relation_to_subject=SubjectRelation.EXTERNAL_OTHER,
            embodiment_similarity=0.5,
            behavioral_predictability=0.5,
            affective_resonance=0.5,
            perspective_accessibility=0.5,
            interaction_history_depth=1,
            evidence_refs=(),
        )


def test_other_model_bounds() -> None:
    with pytest.raises(ValueError, match="embodiment_similarity"):
        OtherModel(
            other_id="o1",
            relation_to_subject=SubjectRelation.EXTERNAL_OTHER,
            embodiment_similarity=1.5,
            behavioral_predictability=0.5,
            affective_resonance=0.5,
            perspective_accessibility=0.5,
            interaction_history_depth=1,
            evidence_refs=("e1",),
        )


def test_config_weights_must_sum_to_one() -> None:
    with pytest.raises(ValueError, match="sum to 1.0"):
        config({SelfOtherDistinction.AGENCY_ATTRIBUTION: 0.5})


def test_config_rejects_negative_weight_even_if_total_is_one() -> None:
    with pytest.raises(ValueError, match="weight"):
        config({
            SelfOtherDistinction.AGENCY_ATTRIBUTION: 1.2,
            SelfOtherDistinction.SENSORY_PREDICTION_ERROR: -0.2,
        })


def test_config_threshold_order() -> None:
    with pytest.raises(ValueError, match="permeability_threshold"):
        BoundaryConfiguration(
            config_id="c1",
            default_mode=BoundaryMode.SEMI_PERMEABLE,
            distinction_weights=distinction_weights(),
            permeability_threshold=0.8,
            rigidity_threshold=0.3,
        )


def test_config_weights_are_deeply_read_only() -> None:
    cfg = config()
    with pytest.raises(TypeError):
        cfg.distinction_weights[SelfOtherDistinction.AGENCY_ATTRIBUTION] = 0.9  # type: ignore[index]
    assert cfg.distinction_weights[SelfOtherDistinction.AGENCY_ATTRIBUTION] == 0.25


def test_event_requires_other_ref_when_other_contributes() -> None:
    with pytest.raises(ValueError, match="other_ref"):
        event(other_ref=None, other_contribution=0.4)


def test_same_entity_may_be_modeled_in_self_relative_role() -> None:
    observed_self = other_model("subject-1", SubjectRelation.SELF_AS_OBSERVED)
    s = state(others=(observed_self,), events=(event(other_ref="subject-1"),))
    assert s.get_other_model("subject-1", SubjectRelation.SELF_AS_OBSERVED) is observed_self


def test_duplicate_same_entity_and_role_is_rejected() -> None:
    duplicate = (
        other_model("entity-1", SubjectRelation.EXTERNAL_OTHER),
        other_model("entity-1", SubjectRelation.EXTERNAL_OTHER),
    )
    with pytest.raises(ValueError, match="unique"):
        state(others=duplicate, events=())


def test_same_entity_different_roles_are_allowed_but_ambiguous_without_role() -> None:
    external = other_model("entity-1", SubjectRelation.EXTERNAL_OTHER)
    remembered = other_model("entity-1", SubjectRelation.PAST_SELF)
    s = state(others=(external, remembered), events=())
    with pytest.raises(ValueError, match="ambiguous"):
        s.get_other_model("entity-1")
    assert s.get_other_model("entity-1", SubjectRelation.PAST_SELF) is remembered


def test_active_distinctions_must_match_configuration() -> None:
    cfg = config()
    with pytest.raises(ValueError, match="active_distinctions"):
        BoundaryState(
            state_id="s1",
            subject_ref="subject-1",
            config=cfg,
            current_mode=BoundaryMode.SEMI_PERMEABLE,
            active_distinctions=(SelfOtherDistinction.AGENCY_ATTRIBUTION,),
            other_models=(other_model(),),
            boundary_permeability=0.4,
            confusion_index=0.2,
            recent_events=(event(),),
        )


def test_event_other_ref_must_resolve() -> None:
    with pytest.raises(ValueError, match="other_ref"):
        state(events=(event(other_ref="missing-other"),))


def test_non_claim_guard_is_preserved() -> None:
    cfg = config()
    with pytest.raises(ValueError, match="shared subjectivity"):
        BoundaryState(
            state_id="s1",
            subject_ref="subject-1",
            config=cfg,
            current_mode=BoundaryMode.SEMI_PERMEABLE,
            active_distinctions=tuple(cfg.distinction_weights),
            other_models=(other_model(),),
            boundary_permeability=0.4,
            confusion_index=0.2,
            recent_events=(event(),),
            shared_subjectivity_claim="CLAIMED",
        )


def test_manager_initialize_and_transition() -> None:
    mgr = BoundaryStateManager(deterministic_seed=42)
    s1 = state()
    s2 = state(state_id="state-2")
    mgr.initialize(s1)
    mgr.transition(s2, transition_type="BOUNDARY_SHIFT", reason="interaction")
    assert mgr.get_state() is s2
    assert [t.transition_type for t in mgr.get_history()] == ["INITIALIZE", "BOUNDARY_SHIFT"]


def test_silent_subject_change_is_rejected() -> None:
    mgr = BoundaryStateManager()
    mgr.initialize(state())
    with pytest.raises(ValueError, match="explicit subject-transition"):
        mgr.transition(state(state_id="state-2", subject_ref="subject-2"))


def test_explicit_subject_change_is_allowed_and_traced() -> None:
    mgr = BoundaryStateManager()
    mgr.initialize(state())
    mgr.transition(
        state(state_id="state-2", subject_ref="subject-2"),
        transition_type="PERSPECTIVE_SWITCH",
        reason="explicit research perspective change",
    )
    transition = mgr.get_history()[-1]
    assert transition.from_subject_ref == "subject-1"
    assert transition.to_subject_ref == "subject-2"


def test_snapshot_preserves_read_only_configuration() -> None:
    mgr = BoundaryStateManager()
    mgr.initialize(state())
    snap = mgr.snapshot("snap-1")
    with pytest.raises(TypeError):
        snap.state.config.distinction_weights[SelfOtherDistinction.AGENCY_ATTRIBUTION] = 0.9  # type: ignore[index]
    assert snap.state.config.distinction_weights[SelfOtherDistinction.AGENCY_ATTRIBUTION] == 0.25


def test_restore_records_actual_source_state() -> None:
    mgr = BoundaryStateManager()
    mgr.initialize(state())
    mgr.snapshot("snap-1")
    mgr.transition(state(state_id="state-2"))
    mgr.restore("snap-1")
    transition = mgr.get_history()[-1]
    assert transition.from_state_id == "state-2"
    assert transition.to_state_id == "state-1"


def test_cross_subject_restore_requires_explicit_opt_in() -> None:
    mgr = BoundaryStateManager()
    mgr.initialize(state())
    mgr.snapshot("subject-1-snap")
    mgr.transition(
        state(state_id="state-2", subject_ref="subject-2"),
        transition_type="SUBJECT_SWITCH",
        reason="explicit switch",
    )
    with pytest.raises(ValueError, match="different subject"):
        mgr.restore("subject-1-snap")
    restored = mgr.restore("subject-1-snap", allow_subject_switch=True)
    assert restored.subject_ref == "subject-1"
    assert mgr.get_history()[-1].transition_type == "RESTORE_SUBJECT_SWITCH"


def test_manager_reset() -> None:
    mgr = BoundaryStateManager()
    mgr.initialize(state())
    mgr.snapshot("snap-1")
    mgr.reset()
    assert mgr.get_state() is None
    assert mgr.get_history() == ()
    assert mgr.list_snapshots() == ()


def test_manager_disable_enable() -> None:
    mgr = BoundaryStateManager()
    mgr.disable()
    with pytest.raises(RuntimeError):
        mgr.initialize(state())
    mgr.enable()
    mgr.initialize(state())
    assert mgr.is_enabled()


def test_ablate_distinction_is_traced_and_weights_renormalized() -> None:
    mgr = BoundaryStateManager()
    mgr.initialize(state())
    mgr.ablate("AGENCY_ATTRIBUTION")
    new_state = mgr.get_state()
    assert new_state is not None
    assert SelfOtherDistinction.AGENCY_ATTRIBUTION not in new_state.active_distinctions
    assert abs(sum(new_state.config.distinction_weights.values()) - 1.0) < 1e-6
    assert mgr.get_history()[-1].transition_type == "ABLATE_DISTINCTION"


def test_unknown_ablation_is_explicit_error() -> None:
    mgr = BoundaryStateManager()
    mgr.initialize(state())
    with pytest.raises(KeyError, match="Unknown distinction"):
        mgr.ablate("NOT_A_DISTINCTION")


def test_final_distinction_ablation_disables_module_safely() -> None:
    one = config({SelfOtherDistinction.AGENCY_ATTRIBUTION: 1.0})
    mgr = BoundaryStateManager()
    mgr.initialize(state(cfg=one, events=()))
    mgr.ablate("AGENCY_ATTRIBUTION")
    assert not mgr.is_enabled()
    assert mgr.get_history()[-1].transition_type == "ABLATE_DISTINCTION_DISABLE"


def test_whole_module_ablation_is_traced() -> None:
    mgr = BoundaryStateManager()
    mgr.initialize(state())
    mgr.ablate()
    assert not mgr.is_enabled()
    assert mgr.get_history()[-1].transition_type == "ABLATE_MODULE"


def test_injected_timestamp_provider_makes_trace_time_reproducible() -> None:
    mgr = BoundaryStateManager(deterministic_seed=42, timestamp_provider=lambda: "FIXED-TIME")
    mgr.initialize(state())
    assert mgr.get_history()[0].timestamp == "FIXED-TIME"
    snap = mgr.snapshot("snap")
    assert snap.timestamp == "FIXED-TIME"
