from __future__ import annotations

import inspect

import pytest

from aion_second_order import (
    ControlDisposition,
    DeterministicVerificationProvider,
    OutcomeContract,
    SecondOrderCondition,
    SecondOrderRunner,
    VerificationAssessment,
    VerificationFixture,
    VerificationInterventionCondition,
    VerificationRejection,
    materialize_intervention,
    run_intervention_condition,
    run_matched_intervention_experiment,
)
from aion_self_model_ablation import Task, default_benchmark_tasks


def pending_with_trace(assessment: VerificationAssessment, *, run_id: str = "intervene"):
    runner = SecondOrderRunner(SecondOrderCondition.MONITOR_PLUS_CONTROL, run_id=run_id)
    for task, outcome in ((Task("t0", 0.50), True), (Task("t1", 0.75), False)):
        pending = runner.decide(task)
        runner.record_outcome(
            pending,
            actual_success=outcome,
            evidence_refs=(f"label:{task.task_id}",),
            provenance_refs=("fixture:intervention-test",),
        )
    pending = runner.decide(Task("t2", 0.60))
    trace = runner.verify_pending(
        DeterministicVerificationProvider((VerificationFixture(assessment),))
    )
    return runner, pending, trace


def test_intervention_api_has_no_outcome_channel_and_preserves_first_order_trace():
    assert "actual_success" not in inspect.signature(SecondOrderRunner.intervene_pending).parameters
    runner, pending, _ = pending_with_trace(VerificationAssessment.INCORRECT)
    before = (
        pending.first_order_prediction,
        pending.first_order_action,
        pending.first_order_estimate,
        pending.control_disposition,
    )
    intervention = runner.intervene_pending(VerificationInterventionCondition.APPLIED)
    after = (
        pending.first_order_prediction,
        pending.first_order_action,
        pending.first_order_estimate,
        pending.control_disposition,
    )
    assert after == before
    assert intervention.target.target_snapshot is pending.first_order_prediction


def test_trace_only_and_ablation_do_not_intervene():
    for condition in (
        VerificationInterventionCondition.TRACE_ONLY,
        VerificationInterventionCondition.ABLATED,
    ):
        runner, pending, _ = pending_with_trace(VerificationAssessment.INCORRECT)
        intervention = runner.intervene_pending(condition)
        assert intervention.post_verification_disposition is pending.control_disposition
        assert intervention.affected_disposition is False


@pytest.mark.parametrize(
    ("assessment", "expected"),
    (
        (VerificationAssessment.CORRECT, ControlDisposition.ACCEPT_FIRST_ORDER),
        (VerificationAssessment.INCORRECT, ControlDisposition.DEFER),
        (VerificationAssessment.AMBIGUOUS, ControlDisposition.DEFER),
        (VerificationAssessment.UNAVAILABLE, ControlDisposition.DEFER),
        (VerificationAssessment.INSUFFICIENT, ControlDisposition.DEFER),
    ),
)
def test_applied_policy_is_conservative_and_never_flips_prediction(assessment, expected):
    runner, pending, _ = pending_with_trace(assessment)
    original_prediction = pending.first_order_prediction
    intervention = runner.intervene_pending(VerificationInterventionCondition.APPLIED)
    assert intervention.post_verification_disposition is expected
    assert intervention.target.target_snapshot is original_prediction
    assert pending.first_order_prediction is original_prediction


def test_rejected_verification_defers_under_applied_policy():
    runner, pending, trace = pending_with_trace(VerificationAssessment.CORRECT)
    rejected = type(trace)(
        request=trace.request,
        provider_ref=trace.provider_ref,
        evidence=trace.evidence,
        result=type(trace.result)(False, None, VerificationRejection.ORACLE_LEAKAGE),
        original_disposition=trace.original_disposition,
        post_verification_disposition=trace.post_verification_disposition,
    )
    intervention = materialize_intervention(
        rejected,
        VerificationInterventionCondition.APPLIED,
    )
    assert intervention.post_verification_disposition is ControlDisposition.DEFER
    assert pending.first_order_prediction is rejected.request.target.target_snapshot


def test_randomized_intervention_is_independent_of_assessment():
    _, _, correct = pending_with_trace(VerificationAssessment.CORRECT, run_id="same-random")
    _, _, incorrect = pending_with_trace(VerificationAssessment.INCORRECT, run_id="same-random")
    left = materialize_intervention(
        correct,
        VerificationInterventionCondition.RANDOMIZED,
        random_seed=7,
    )
    right = materialize_intervention(
        incorrect,
        VerificationInterventionCondition.RANDOMIZED,
        random_seed=7,
    )
    assert left.post_verification_disposition is right.post_verification_disposition
    assert left.random_seed == right.random_seed == 7
    assert left.randomized_source == right.randomized_source == "SHA256_SEED_RUN_REQUEST"


def test_intervention_requires_verification_trace():
    runner = SecondOrderRunner(SecondOrderCondition.MONITOR_PLUS_CONTROL, run_id="missing-trace")
    for task, outcome in ((Task("t0", 0.50), True), (Task("t1", 0.75), False)):
        pending = runner.decide(task)
        runner.record_outcome(
            pending,
            actual_success=outcome,
            evidence_refs=("label",),
            provenance_refs=("fixture:test",),
        )
    runner.decide(Task("t2", 0.60))
    with pytest.raises(ValueError, match="exactly one verification trace"):
        runner.intervene_pending(VerificationInterventionCondition.APPLIED)


def test_matched_intervention_conditions_preserve_task_and_first_order_trace():
    result = run_matched_intervention_experiment()
    assert result.same_task_stream is True
    assert result.same_first_order_trace is True
    assert result.outcome_contract is OutcomeContract.EXTERNAL_BENCHMARK_FULL_LABELS
    assert {item.condition for item in result.conditions} == set(VerificationInterventionCondition)
    assert result.stale_condition_status == "DEFERRED"
    assert result.functional_contribution_status == "NOT_ESTABLISHED"
    assert result.verification_benefit == "NOT_ESTABLISHED"


def test_raw_metrics_keep_operational_tradeoffs_separate():
    result = run_matched_intervention_experiment()
    applied = next(
        item
        for item in result.conditions
        if item.condition is VerificationInterventionCondition.APPLIED
    )
    metrics = applied.intervention_diagnostics
    assert metrics.identifiability_status == "SYNTHETIC_FULL_LABEL_OPERATIONAL_MEASURE"
    assert metrics.intervention_opportunities == len(applied.verification_traces)
    assert metrics.interventions_applied == len(applied.interventions)
    assert metrics.prevented_failed_commit is not None
    assert metrics.unnecessary_defer is not None
    assert metrics.retained_successful_commit is not None
    assert not hasattr(metrics, "benefit_score")


def test_commit_only_counterfactual_metrics_remain_not_identifiable():
    result = run_intervention_condition(
        VerificationInterventionCondition.APPLIED,
        default_benchmark_tasks(),
        outcome_contract=OutcomeContract.COMMIT_ONLY,
    )
    metrics = result.intervention_diagnostics
    assert metrics.identifiability_status == "NOT_IDENTIFIABLE"
    assert metrics.prevented_failed_commit is None
    assert metrics.unnecessary_defer is None
    assert metrics.retained_successful_commit is None
