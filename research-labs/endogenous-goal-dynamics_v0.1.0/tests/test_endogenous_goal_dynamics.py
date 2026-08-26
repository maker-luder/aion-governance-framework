from __future__ import annotations

from aion_endogenous_goal_dynamics import (
    ExperimentCondition,
    GoalSelector,
    PREREGISTERED_FALSIFIERS,
    assess_causal_pattern,
    canonical_hash,
    endogenous_goal_dynamics_mapping,
    intervention_state,
    matched_frame,
    present_state,
    run_matched_experiment,
    stale_state,
)

START = "77eda1ecd7b96a9aa8ea8bd62038759636be819d"


def experiment():
    return run_matched_experiment(
        matched_frame(),
        present_state=present_state(),
        intervention_state=intervention_state(),
        stale_state=stale_state(),
        experiment_id="experiment:smoke",
        hypothesis_id="hypothesis:endogenous-role-001",
        repository_commit=START,
        fixture_hash=canonical_hash("smoke"),
    )


def test_present_ablated_intervened_have_expected_selection() -> None:
    value = experiment()
    assert value.one(ExperimentCondition.PRESENT).decision.selected_goal_id == "inspect_anomaly"
    assert value.one(ExperimentCondition.ABLATED).decision.selected_goal_id == "continue_task"
    assert value.one(ExperimentCondition.INTERVENED).decision.selected_goal_id == "continue_task"


def test_selector_is_explicit_research_mechanism() -> None:
    assert GoalSelector().policy.policy_id == "EGD_ADDITIVE_BP_V0.1.0"
    assert GoalSelector().policy.tie_rule == "HOLD"


def test_causal_assessment_preserves_scientific_hold() -> None:
    assessment = assess_causal_pattern(experiment())
    assert assessment.result_status == "HOLD"
    assert assessment.consciousness_conclusion == "NOT_ESTABLISHED"


def test_four_domain_construct_remains_central_research_row() -> None:
    assert endogenous_goal_dynamics_mapping().construct == "ENDOGENOUS_GOAL_DYNAMICS"


def test_all_falsifiers_are_preregistered() -> None:
    assert tuple(item.falsifier_id for item in PREREGISTERED_FALSIFIERS) == tuple(
        f"F{index}" for index in range(1, 13)
    )


def test_action_authority_and_canonical_effect_remain_none() -> None:
    for trial in experiment().trials:
        assert trial.decision.action_authority == "NONE"
        assert trial.decision.canonical_effect == "NONE"
