
from aion_self_model_ablation import (
    Action,
    Condition,
    default_benchmark_tasks,
    run_condition,
    run_matched_ablation,
)


def test_present_condition_is_history_dependent():
    trials = run_condition(
        Condition.SELF_MODEL_PRESENT,
        default_benchmark_tasks(),
        latent_capability=0.62,
    )
    by_id = {trial.task_id: trial for trial in trials}
    assert by_id["cal-02"].action is Action.COMMIT
    assert by_id["cal-05"].action is Action.DEFER
    assert by_id["cal-02"].estimate_before != by_id["cal-05"].estimate_before


def test_stale_condition_does_not_update_from_failure():
    trials = run_condition(
        Condition.SELF_MODEL_STALE,
        default_benchmark_tasks(),
        latent_capability=0.62,
        prior=0.80,
    )
    estimates = {trial.estimate_before for trial in trials}
    assert estimates == {0.80}


def test_matched_ablation_detects_functional_contribution_candidate():
    result = run_matched_ablation(
        default_benchmark_tasks(),
        latent_capability=0.62,
        random_seed=17,
    )
    assert result.functional_contribution_candidate is True
    assert result.present_minus_ablated_reward >= 0.5
    assert result.present_minus_stale_reward >= 0.5
    assert result.interpretation == "SELF_MODEL_FUNCTIONAL_CONTRIBUTION_CANDIDATE"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_all_conditions_run_on_same_number_of_tasks():
    result = run_matched_ablation(default_benchmark_tasks(), latent_capability=0.62)
    counts = {summary.trial_count for summary in result.summaries}
    assert counts == {len(default_benchmark_tasks())}


def test_ablation_result_never_becomes_consciousness_claim():
    result = run_matched_ablation(default_benchmark_tasks(), latent_capability=0.62)
    assert all(summary.subjectivity_conclusion == "NOT_ESTABLISHED" for summary in result.summaries)
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
