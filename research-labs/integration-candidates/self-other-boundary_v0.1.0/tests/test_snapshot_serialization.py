from self_other_boundary import (
    BoundaryConfiguration,
    BoundaryMode,
    BoundaryState,
    BoundaryStateManager,
    OtherModel,
    SelfOtherDistinction,
    SubjectRelation,
)


def test_snapshot_to_dict_serializes_read_only_weights() -> None:
    config = BoundaryConfiguration(
        config_id="config-serialization",
        default_mode=BoundaryMode.SEMI_PERMEABLE,
        distinction_weights={SelfOtherDistinction.AGENCY_ATTRIBUTION: 1.0},
        permeability_threshold=0.3,
        rigidity_threshold=0.7,
    )
    other = OtherModel(
        other_id="other-serialization",
        relation_to_subject=SubjectRelation.EXTERNAL_OTHER,
        embodiment_similarity=0.5,
        behavioral_predictability=0.5,
        affective_resonance=0.5,
        perspective_accessibility=0.5,
        interaction_history_depth=1,
        evidence_refs=("serialization-evidence",),
    )
    state = BoundaryState(
        state_id="state-serialization",
        subject_ref="subject-serialization",
        config=config,
        current_mode=BoundaryMode.SEMI_PERMEABLE,
        active_distinctions=(SelfOtherDistinction.AGENCY_ATTRIBUTION,),
        other_models=(other,),
        boundary_permeability=0.4,
        confusion_index=0.2,
        recent_events=(),
    )
    manager = BoundaryStateManager(timestamp_provider=lambda: "FIXED-TIME")
    manager.initialize(state)
    result = manager.snapshot("snapshot-serialization").to_dict()

    assert result["snapshot_id"] == "snapshot-serialization"
    assert result["state"]["config"]["distinction_weights"] == {"AGENCY_ATTRIBUTION": 1.0}
