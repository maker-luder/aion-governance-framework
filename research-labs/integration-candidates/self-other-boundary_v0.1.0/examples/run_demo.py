#!/usr/bin/env python3
"""Demo for self-other-boundary module."""

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


def build_initial_config() -> BoundaryConfiguration:
    return BoundaryConfiguration(
        config_id="boundary-config-001",
        default_mode=BoundaryMode.SEMI_PERMEABLE,
        distinction_weights={
            SelfOtherDistinction.AGENCY_ATTRIBUTION: 0.25,
            SelfOtherDistinction.SENSORY_PREDICTION_ERROR: 0.20,
            SelfOtherDistinction.AFFECTIVE_RESONANCE: 0.20,
            SelfOtherDistinction.PERSPECTIVE_TAKING: 0.15,
            SelfOtherDistinction.NARRATIVE_DIFFERENTIATION: 0.10,
            SelfOtherDistinction.EMBODIMENT_MAPPING: 0.10,
        },
        permeability_threshold=0.3,
        rigidity_threshold=0.7,
    )


def build_initial_state(config: BoundaryConfiguration) -> BoundaryState:
    others = (
        OtherModel(
            other_id="astra-agent",
            relation_to_subject=SubjectRelation.EXTERNAL_OTHER,
            embodiment_similarity=0.85,
            behavioral_predictability=0.70,
            affective_resonance=0.60,
            perspective_accessibility=0.50,
            interaction_history_depth=100,
            evidence_refs=("demo-observation-astra-001",),
        ),
        OtherModel(
            other_id="human-user",
            relation_to_subject=SubjectRelation.EXTERNAL_OTHER,
            embodiment_similarity=0.30,
            behavioral_predictability=0.40,
            affective_resonance=0.75,
            perspective_accessibility=0.60,
            interaction_history_depth=50,
            evidence_refs=("demo-observation-human-001",),
        ),
    )
    return BoundaryState(
        state_id="initial-boundary-state-001",
        subject_ref="aion-research-agent",
        config=config,
        current_mode=BoundaryMode.SEMI_PERMEABLE,
        active_distinctions=tuple(config.distinction_weights),
        other_models=others,
        boundary_permeability=0.4,
        confusion_index=0.15,
        recent_events=(),
    )


def demo() -> None:
    print("=" * 60)
    print("SELF-OTHER BOUNDARY DEMO")
    print("=" * 60)

    mgr = BoundaryStateManager(deterministic_seed=12345)
    config = build_initial_config()
    initial = build_initial_state(config)
    mgr.initialize(initial)

    print(f"Initial state: {mgr.get_state().state_id}")
    print(f"Subject: {mgr.get_state().subject_ref}")
    print(f"Other models: {[om.other_id for om in mgr.get_state().other_models]}")

    snap = mgr.snapshot("demo-snapshot-1")
    print(f"Snapshot: {snap.snapshot_id}")

    interaction_event = BoundaryEvent(
        event_id="interaction-001",
        event_type="AFFECTIVE_EXCHANGE",
        self_contribution=0.55,
        other_contribution=0.45,
        boundary_shift=0.15,
        timestamp="2026-08-10T00:00:10Z",
        other_ref="astra-agent",
    )
    shifted_state = BoundaryState(
        state_id="shifted-boundary-state-002",
        subject_ref=initial.subject_ref,
        config=config,
        current_mode=BoundaryMode.PERMEABLE,
        active_distinctions=initial.active_distinctions,
        other_models=initial.other_models,
        boundary_permeability=0.55,
        confusion_index=0.25,
        recent_events=(interaction_event,),
    )
    mgr.transition(shifted_state, transition_type="BOUNDARY_SHIFT", reason="interaction with astra-agent")
    print(f"Shifted permeability: {mgr.get_state().boundary_permeability}")

    mgr.restore("demo-snapshot-1")
    print(f"Restored state: {mgr.get_state().state_id}")

    mgr.ablate("AFFECTIVE_RESONANCE")
    ablated = mgr.get_state()
    print(f"Remaining distinctions: {[d.value for d in ablated.active_distinctions]}")
    print(f"Last transition: {mgr.get_history()[-1].transition_type}")

    mgr.ablate()
    print(f"Enabled after whole-module ablation: {mgr.is_enabled()}")

    print("Canonical effect: NONE")
    print("Empathy claim: NOT_ESTABLISHED")
    print("Theory of mind claim: NOT_ESTABLISHED")
    print("Shared subjectivity claim: NOT_ESTABLISHED")


if __name__ == "__main__":
    demo()
