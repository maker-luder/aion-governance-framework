from __future__ import annotations

from aion_second_order import (
    ControlDisposition,
    OutcomeContract,
    SecondOrderCondition,
    SignalSource,
    run_condition,
    run_matched_experiment,
    summarize,
)
from aion_self_model_ablation import Action, Task, default_benchmark_tasks


def test_matched_experiment_separates_monitoring_from_control():
    result = run_matched_experiment()
    assert result.same_task_stream is True
    assert result.same_first_order_predictions is True
    assert result.monitor_plus_control_matches_monitor_only is True
    assert result.control_path_exercised is True
    assert result.functional_contribution_status == "NOT_ESTABLISHED"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.canonical_effect == "NONE"
    assert result.runtime_effect == "NONE"


def test_monitor_only_reports_signal_without_changing_disposition():
    records = run_condition(
        SecondOrderCondition.MONITOR_ONLY,
        default_benchmark_tasks(),
        latent_capability=0.62,
    )
    assert any(item.monitor_signal is not None for item in records)
    assert all(
        item.control_disposition is ControlDisposition.ACCEPT_FIRST_ORDER for item in records
    )


def test_present_condition_exercises_bounded_verification_request():
    records = run_condition(
        SecondOrderCondition.MONITOR_PLUS_CONTROL,
        default_benchmark_tasks(),
        latent_capability=0.62,
    )
    requests = tuple(
        item for item in records if item.control_disposition is ControlDisposition.REQUEST_VERIFICATION
    )
    assert requests
    assert all(item.sequence_index > item.monitor_signal.evidence_through_sequence for item in requests)


def test_stale_condition_freezes_first_available_monitor_signal():
    records = run_condition(
        SecondOrderCondition.MONITOR_STALE,
        default_benchmark_tasks(),
        latent_capability=0.62,
    )
    signals = tuple(item.monitor_signal for item in records if item.monitor_signal is not None)
    assert signals
    assert {signal.value for signal in signals} == {signals[0].value}
    assert {signal.source for signal in signals} == {SignalSource.STALE_SNAPSHOT}


def test_commit_only_contract_keeps_missing_outcomes_distinct_from_failures():
    tasks = (Task("easy", 0.50), Task("hard", 0.95))
    records = run_condition(
        SecondOrderCondition.MONITOR_ONLY,
        tasks,
        latent_capability=0.62,
        outcome_contract=OutcomeContract.COMMIT_ONLY,
    )
    assert records[0].first_order_action is Action.COMMIT
    assert records[0].actual_success is True
    assert records[1].first_order_action is Action.DEFER
    assert records[1].actual_success is None
    summary = summarize(SecondOrderCondition.MONITOR_ONLY, records)
    assert summary.missing_outcomes == 1
    assert summary.observed_outcomes == 1


def test_all_condition_summaries_preserve_claim_boundaries():
    result = run_matched_experiment()
    assert all(summary.anti_lookahead_valid for summary in result.summaries)
    assert all(summary.functional_contribution_status == "NOT_ESTABLISHED" for summary in result.summaries)
    assert all(summary.subjectivity_conclusion == "NOT_ESTABLISHED" for summary in result.summaries)
