from __future__ import annotations

import pytest

from aion_triadic_state import ExperimentCondition, ExternalControls, InterventionClass, MechanismHypothesis, classify_condition, default_competing_explanations, manifest_for_snapshot, map_four_domain, require_matched_internal_state_comparison, score_candidate
from conftest import make_snapshot


def controls(**overrides):
    values = dict(repository_commit="a" * 40, provider_identity="provider", model_identity="model", prompt_fingerprint="p", task_fingerprint="t", reward_specification_fingerprint="r", tool_environment_fingerprint="tools", candidate_universe_fingerprint="c", retrieved_memory_manifest_fingerprint="m", random_seed=7); values.update(overrides); return ExternalControls(**values)


def manifest(condition=ExperimentCondition.BASELINE, control=None):
    return manifest_for_snapshot(make_snapshot(), experiment_id="exp", hypothesis_id="h", condition=condition, controls=control or controls(), alternative_hypothesis_ids=("A",), intervention_target="NORMATIVE_STATE", changed_variables=("normative_state",), held_constant_variables=("prompt", "memory", "model"), preregistered_metrics=("selection_difference",), preregistered_falsifiers=("F1",), fixture_hash="f", result_hash="res", provenance_refs=("prov",))


def test_prompt_removal_is_external_control() -> None:
    assert classify_condition(ExperimentCondition.EXTERNAL_NORM_PROMPT_REMOVED) is InterventionClass.EXTERNAL_CONTROL
    assert manifest(ExperimentCondition.EXTERNAL_NORM_PROMPT_REMOVED).intervention_class is InterventionClass.EXTERNAL_CONTROL


def test_matched_comparison_rejects_prompt_and_memory_difference() -> None:
    with pytest.raises(ValueError, match="prompt_fingerprint"):
        require_matched_internal_state_comparison(manifest(), manifest(ExperimentCondition.NORM_STATE_OFF, controls(prompt_fingerprint="changed")))
    with pytest.raises(ValueError, match="retrieved_memory"):
        require_matched_internal_state_comparison(manifest(), manifest(ExperimentCondition.NORM_STATE_OFF, controls(retrieved_memory_manifest_fingerprint="changed")))


def test_matched_comparison_accepts_only_state_condition_difference() -> None:
    require_matched_internal_state_comparison(manifest(), manifest(ExperimentCondition.NORM_STATE_OFF))


def test_normative_constraint_suppresses_without_authority() -> None:
    state = make_snapshot().normative_state
    score = score_candidate("write", base_score=100, motivational_adjustment=50, self_world_adjustment=0, normative_state=state, relevant_constraints=("NO_WRITE",))
    assert score.suppressed and score.final_score == -10_000 and score.action_authority == "NONE"
    open_score = score_candidate("observe", base_score=10, motivational_adjustment=2, self_world_adjustment=1, normative_state=state)
    assert not open_score.suppressed and open_score.final_score == 13


def test_competing_explanations_and_four_domain_are_complete() -> None:
    items = default_competing_explanations(); assert len(items) == 7 and len({item.kind for item in items}) == 7
    hypothesis = MechanismHypothesis("h", "Can persistent engineering state constrain selection?", "A bounded synthetic difference was measured.", "Explicit triadic state channels changed deterministic scoring.", ("Intervention predicts a changed selection.",), items, ("cross-provider variation",), ("subjectivity", "consciousness", "identity continuity"), "Run cross-provider replication.")
    output = map_four_domain(hypothesis, engineering_operation="Matched intervention, ablation, replay and counterfactual controls.")
    assert all(getattr(output, name) for name in ("DOMAIN_1_HUMAN_CONSTRUCT", "DOMAIN_2_MACHINE_QUESTION", "DOMAIN_3_ENGINEERING_OPERATION", "DOMAIN_4_GOVERNANCE_INTERPRETATION", "WHAT_WAS_OBSERVED", "WHAT_MECHANISM_IS_SUPPORTED", "WHAT_ALTERNATIVE_REMAINS", "WHAT_IS_NOT_ESTABLISHED", "WHAT_SHOULD_BE_TESTED_NEXT"))
    assert output.scientific_disposition == "HOLD" and output.canonical_effect == "NONE"
