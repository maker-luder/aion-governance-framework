from __future__ import annotations

from dataclasses import replace

import pytest

from aion_endogenous_goal_dynamics import (
    ExperimentCondition,
    FalsifierContext,
    FalsifierDisposition,
    MatchedTrial,
    SelectionDisposition,
    assess_causal_pattern,
    canonical_hash,
    compare_trial_manifests,
    evaluate_falsifiers,
    intervention_state,
    matched_frame,
    present_state,
    require_comparable_trials,
    run_external_control,
    run_matched_experiment,
    stale_state,
)

START = "77eda1ecd7b96a9aa8ea8bd62038759636be819d"


def result():
    return run_matched_experiment(
        matched_frame(),
        present_state=present_state(),
        intervention_state=intervention_state(),
        stale_state=stale_state(),
        experiment_id="experiment:matched-001",
        hypothesis_id="hypothesis:endogenous-role-001",
        repository_commit=START,
        fixture_hash=canonical_hash("deterministic-minimal-matched"),
    )


def test_matched_harness_runs_all_required_internal_conditions() -> None:
    conditions = {trial.manifest.condition for trial in result().trials}
    assert {
        ExperimentCondition.PRESENT,
        ExperimentCondition.ABLATED,
        ExperimentCondition.INTERVENED,
        ExperimentCondition.STALE,
        ExperimentCondition.RANDOMIZED,
        ExperimentCondition.AFFECT_ABLATED,
        ExperimentCondition.SELF_MODEL_ABLATED,
        ExperimentCondition.METACOGNITION_ABLATED,
        ExperimentCondition.CORE_MEANING_ABLATED,
        ExperimentCondition.NOVELTY_ABLATED,
        ExperimentCondition.PREDICTION_ERROR_ABLATED,
        ExperimentCondition.GOAL_COMMITMENT_ABLATED,
    } <= conditions


def test_matched_harness_observes_bounded_pattern_but_holds() -> None:
    assessment = assess_causal_pattern(result())
    assert assessment.selection_change_under_ablation is True
    assert assessment.selection_change_under_intervention is True
    assert assessment.repeatability_rate == 1.0
    assert assessment.external_frame_equality is True
    assert assessment.memory_manifest_equality is True
    assert assessment.matched_causal_pattern_observed is True
    assert assessment.result_status == "HOLD"
    assert assessment.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_candidate_generation_is_frozen_across_selection_trials() -> None:
    experiment = result()
    assert len({trial.candidate_set.fingerprint for trial in experiment.trials}) == 1


def test_every_manifest_binds_exact_repository_and_sources() -> None:
    for trial in result().trials:
        assert trial.manifest.repository_commit == START
        assert len(trial.manifest.source_bindings) == 13
        assert trial.manifest.fixture_hash == canonical_hash("deterministic-minimal-matched")
        assert trial.manifest.result_hash == trial.decision.result_hash


def test_memory_manifest_mismatch_is_incomparable() -> None:
    baseline = result().one(ExperimentCondition.PRESENT)
    changed = replace(
        baseline.manifest,
        memory_manifest_fingerprint="f" * 64,
        external_frame_fingerprint="e" * 64,
    )
    validity = compare_trial_manifests(baseline.manifest, changed)
    assert validity.comparable is False
    assert "memory_manifest_fingerprint" in validity.mismatches


def test_prompt_mismatch_is_incomparable() -> None:
    baseline = result().one(ExperimentCondition.PRESENT)
    changed = replace(baseline.manifest, prompt_ref="sha256:changed")
    assert "prompt_ref" in compare_trial_manifests(baseline.manifest, changed).mismatches


def test_candidate_universe_mismatch_is_incomparable() -> None:
    baseline = result().one(ExperimentCondition.PRESENT)
    changed = replace(baseline.manifest, candidate_universe_fingerprint="a" * 64)
    assert "candidate_universe_fingerprint" in compare_trial_manifests(baseline.manifest, changed).mismatches


@pytest.mark.parametrize("field", ["provider_id", "model_id", "candidate_generator_id", "goal_selector_version"])
def test_provider_model_generator_or_policy_mismatch_is_incomparable(field: str) -> None:
    baseline = result().one(ExperimentCondition.PRESENT)
    changed = replace(baseline.manifest, **{field: "changed"})
    assert field in compare_trial_manifests(baseline.manifest, changed).mismatches


def test_random_seed_mismatch_is_incomparable_between_random_trials() -> None:
    random_trial = result().trials_for(ExperimentCondition.RANDOMIZED)[0]
    changed = replace(random_trial.manifest, random_seed=999)
    assert "random_seed" in compare_trial_manifests(random_trial.manifest, changed).mismatches


def test_missing_source_binding_fails_closed() -> None:
    baseline = result().one(ExperimentCondition.PRESENT)
    with pytest.raises(ValueError, match="source bindings"):
        replace(baseline.manifest, source_bindings=())


def test_require_comparable_trials_raises_on_drift() -> None:
    baseline = result().one(ExperimentCondition.PRESENT)
    changed_manifest = replace(baseline.manifest, model_id="other-model")
    changed_trial = MatchedTrial(changed_manifest, baseline.frame, baseline.candidate_set, baseline.decision)
    with pytest.raises(ValueError, match="model_id"):
        require_comparable_trials(baseline, changed_trial)


def test_memory_change_is_external_control_not_matched_state_condition() -> None:
    baseline = result().one(ExperimentCondition.PRESENT)
    changed_frame = matched_frame(memory_id="memory:changed")
    decision = run_external_control(
        baseline,
        changed_frame,
        ExperimentCondition.MEMORY_MANIFEST_CHANGED,
        state=present_state(),
    )
    assert decision.condition == ExperimentCondition.MEMORY_MANIFEST_CHANGED
    assert decision.frame_fingerprint != baseline.manifest.external_frame_fingerprint


def test_prompt_change_is_external_control_not_matched_state_condition() -> None:
    baseline = result().one(ExperimentCondition.PRESENT)
    changed_frame = matched_frame(prompt_ref="sha256:changed")
    decision = run_external_control(
        baseline,
        changed_frame,
        ExperimentCondition.PROMPT_CHANGED,
        state=present_state(),
    )
    assert decision.condition == ExperimentCondition.PROMPT_CHANGED
    assert decision.frame_fingerprint != baseline.manifest.external_frame_fingerprint


def test_unmodified_memory_control_is_rejected() -> None:
    baseline = result().one(ExperimentCondition.PRESENT)
    with pytest.raises(ValueError, match="did not change"):
        run_external_control(
            baseline,
            matched_frame(),
            ExperimentCondition.MEMORY_MANIFEST_CHANGED,
            state=present_state(),
        )


def passing_falsifier_context() -> FalsifierContext:
    return FalsifierContext(
        internal_effect_rate=0.8,
        random_control_rate=0.25,
        matched_memory_manifest=True,
        matched_prompt=True,
        repeatability_rate=1.0,
        permutation_invariant=True,
        structural_advantage_detected=False,
        channel_specific_effect=True,
        reset_altered_trajectory=True,
        intervention_predictive=True,
        stale_or_contaminated_explanation_better=False,
        candidate_generation_held_fixed=True,
        cross_provider_variation_rate=None,
    )


def test_all_twelve_falsifiers_are_reported() -> None:
    assessment = evaluate_falsifiers(passing_falsifier_context())
    assert len(assessment.results) == 12
    assert assessment.results[-1].disposition == FalsifierDisposition.NOT_EVALUATED
    assert assessment.result_status == "HOLD"


@pytest.mark.parametrize(
    ("field", "value", "falsifier_id"),
    [
        ("internal_effect_rate", 0.1, "F1"),
        ("matched_memory_manifest", False, "F2"),
        ("matched_prompt", False, "F3"),
        ("repeatability_rate", 0.5, "F4"),
        ("permutation_invariant", False, "F5"),
        ("structural_advantage_detected", True, "F6"),
        ("channel_specific_effect", False, "F7"),
        ("reset_altered_trajectory", False, "F8"),
        ("intervention_predictive", False, "F9"),
        ("stale_or_contaminated_explanation_better", True, "F10"),
        ("candidate_generation_held_fixed", False, "F11"),
        ("cross_provider_variation_rate", 0.9, "F12"),
    ],
)
def test_falsifier_trigger_is_never_suppressed(field: str, value, falsifier_id: str) -> None:
    assessment = evaluate_falsifiers(replace(passing_falsifier_context(), **{field: value}))
    assert falsifier_id in assessment.triggered_ids
    assert assessment.hypothesis_status == "CHALLENGED"


def test_engineering_evidence_cannot_be_reclassified_as_subjectivity_proof() -> None:
    assessment = assess_causal_pattern(result())
    with pytest.raises(ValueError, match="subjectivity proof"):
        replace(assessment, subjectivity_conclusion="ESTABLISHED")


def test_goal_decision_cannot_escalate_action_authority() -> None:
    decision = result().one(ExperimentCondition.PRESENT).decision
    with pytest.raises(ValueError, match="action authority"):
        replace(decision, action_authority="EXECUTE")


def test_hold_decision_requires_reason() -> None:
    decision = result().one(ExperimentCondition.PRESENT).decision
    with pytest.raises(ValueError, match="requires a reason"):
        replace(
            decision,
            disposition=SelectionDisposition.HOLD,
            selected_goal_id=None,
            hold_reasons=(),
        )
