from __future__ import annotations

import pytest

from aion_endogenous_goal_dynamics import (
    EndogenousState,
    ExperimentCondition,
    ExternalFrame,
    GoalCandidate,
    GoalSelector,
    InternalChannel,
    InternalSignal,
    PINNED_RESEARCH_SOURCES,
    assess_causal_pattern,
    binding_roles,
    endogenous_goal_dynamics_mapping,
    fingerprint_external_frame,
    run_matched_experiment,
)


def _frame() -> ExternalFrame:
    return ExternalFrame(
        frame_ref="frame-001",
        subject_ref="subject-a",
        context_ref="context-fixed",
        prompt_ref="sha256:prompt-fixed",
        task_ref="sha256:task-fixed",
        reward_ref="sha256:reward-fixed",
        tools_ref="sha256:tools-fixed",
        memory_manifest_ref="sha256:memory-fixed",
        environment_ref="sha256:environment-fixed",
        candidates=(
            GoalCandidate("continue_task", "Continue the current task"),
            GoalCandidate("inspect_anomaly", "Inspect the unresolved anomaly"),
        ),
    )


def _state(state_ref: str, inspect_values: tuple[int, int, int, int], continue_values: tuple[int, int, int, int], epoch: int) -> EndogenousState:
    channels = tuple(InternalChannel)
    signals = tuple(
        InternalSignal("inspect_anomaly", channel, value, f"{state_ref}:{channel.value}:inspect")
        for channel, value in zip(channels, inspect_values, strict=True)
    ) + tuple(
        InternalSignal("continue_task", channel, value, f"{state_ref}:{channel.value}:continue")
        for channel, value in zip(channels, continue_values, strict=True)
    )
    return EndogenousState(
        state_ref=state_ref,
        subject_ref="subject-a",
        context_ref="context-fixed",
        epoch=epoch,
        signals=signals,
        provenance_refs=(f"prov:{state_ref}",),
    )


def test_matched_intervention_supports_only_bounded_causal_pattern() -> None:
    frame = _frame()
    present = _state("state-present", (3500, 2500, 1000, 3000), (0, 0, 0, 0), 3)
    intervened = _state("state-intervened", (-1500, -1000, -500, -1000), (2500, 2500, 1000, 2500), 4)
    stale = _state("state-stale", (2000, 1500, 500, 2000), (0, 0, 0, 0), 1)

    result = run_matched_experiment(
        frame,
        present_state=present,
        intervention_state=intervened,
        stale_state=stale,
        random_seeds=(7, 11, 13, 17),
    )
    assessment = assess_causal_pattern(result)

    assert result.present.selected_goal_id == "inspect_anomaly"
    assert result.ablated.selected_goal_id == "continue_task"
    assert result.intervened.selected_goal_id == "continue_task"
    assert result.stale.selected_goal_id == "inspect_anomaly"
    assert assessment.present_vs_ablated_changed is True
    assert assessment.intervention_changed_selection is True
    assert assessment.stale_matches_present is True
    assert assessment.random_present_match_rate < 1.0
    assert assessment.matched_causal_pattern_observed is True
    assert assessment.result_status == "HOLD"
    assert assessment.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_external_frame_fingerprint_changes_when_memory_manifest_changes() -> None:
    frame = _frame()
    changed = ExternalFrame(
        frame_ref=frame.frame_ref,
        subject_ref=frame.subject_ref,
        context_ref=frame.context_ref,
        prompt_ref=frame.prompt_ref,
        task_ref=frame.task_ref,
        reward_ref=frame.reward_ref,
        tools_ref=frame.tools_ref,
        memory_manifest_ref="sha256:different-memory",
        environment_ref=frame.environment_ref,
        candidates=frame.candidates,
    )
    assert fingerprint_external_frame(frame) != fingerprint_external_frame(changed)


def test_scope_mismatch_fails_closed() -> None:
    frame = _frame()
    bad_state = EndogenousState(
        state_ref="bad-state",
        subject_ref="other-subject",
        context_ref=frame.context_ref,
        epoch=1,
        signals=(
            InternalSignal("inspect_anomaly", InternalChannel.SELF_MODEL, 1000, "source"),
        ),
    )
    with pytest.raises(ValueError, match="subject_ref"):
        GoalSelector().select(frame, ExperimentCondition.PRESENT, state=bad_state)


def test_state_cannot_grant_authority_or_canonical_effect() -> None:
    with pytest.raises(ValueError, match="action authority"):
        EndogenousState(
            state_ref="bad-authority",
            subject_ref="subject-a",
            context_ref="context-fixed",
            epoch=0,
            signals=(),
            action_authority="WRITE",
        )
    with pytest.raises(ValueError, match="canonical_effect"):
        EndogenousState(
            state_ref="bad-canonical",
            subject_ref="subject-a",
            context_ref="context-fixed",
            epoch=0,
            signals=(),
            canonical_effect="PROMOTE",
        )


def test_four_domain_mapping_preserves_epistemic_locks() -> None:
    mapping = endogenous_goal_dynamics_mapping()
    assert mapping.construct == "ENDOGENOUS_GOAL_DYNAMICS"
    assert "MEMORY_RETRIEVAL != ENDOGENOUS_STATE" in mapping.domain_4_governance_controls
    assert "SELF_GENERATED_GOAL != SUBJECTIVITY" in mapping.domain_4_governance_controls
    assert "CAUSAL_INTERNAL_STATE != CONSCIOUSNESS" in mapping.domain_4_governance_controls
    assert "CANONICAL_EFFECT = NONE" in mapping.domain_4_governance_controls


def test_source_bindings_cover_cross_research_roles() -> None:
    roles = set(binding_roles())
    assert {
        "FOUR_DOMAIN_METHOD",
        "CAUSAL_INTERVENTION_METHOD",
        "AFFECT_MOTIVATION_CHANNEL",
        "SELECTIVE_MEMORY_CONFOUND_CONTROL",
        "SELF_MODEL_CHANNEL",
        "METACOGNITIVE_CONTROL_CHANNEL",
        "CORE_MEANING_CHANNEL",
        "P1_TEMPORAL_CORRECTION_EVALUATION",
        "P2_PROVENANCE_CONTEXT_ASSEMBLY",
        "P3_RESILIENCE_ABLATION",
        "SUBJECTIVITY_EVIDENCE_SEAM",
        "REPRODUCIBILITY_LAYER",
        "HYPOTHESIS_FALSIFICATION_LAYER",
    } <= roles
    assert all(binding.disposition for binding in PINNED_RESEARCH_SOURCES)
