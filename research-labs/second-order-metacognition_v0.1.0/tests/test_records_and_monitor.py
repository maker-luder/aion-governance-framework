from __future__ import annotations

import inspect

import pytest

from aion_second_order import (
    ControlDisposition,
    OutcomeStatus,
    SecondOrderCondition,
    SecondOrderRunner,
    SignalSource,
    TrialLedger,
    randomized_control_signal,
    recompute_monitor_signal,
)
from aion_self_model_ablation import Task


def complete(runner: SecondOrderRunner, task: Task, success: bool):
    pending = runner.decide(task)
    return runner.record_outcome(
        pending,
        actual_success=success,
        evidence_refs=(f"label:{task.task_id}",),
        provenance_refs=("fixture:test",),
    )


def test_decide_api_has_no_outcome_parameter_and_signal_uses_only_prior_trials():
    assert "actual_success" not in inspect.signature(SecondOrderRunner.decide).parameters
    runner = SecondOrderRunner(
        SecondOrderCondition.MONITOR_PLUS_CONTROL,
        run_id="anti-lookahead",
    )
    complete(runner, Task("t0", 0.50), True)
    complete(runner, Task("t1", 0.75), False)
    pending = runner.decide(Task("t2", 0.60))
    assert pending.sequence_index == 2
    assert pending.monitor_signal is not None
    assert pending.monitor_signal.evidence_through_sequence == 1
    assert pending.monitor_signal.source_trial_ids == ("t0", "t1")
    assert pending.control_disposition is ControlDisposition.REQUEST_VERIFICATION


def test_monitor_is_recomputed_from_immutable_trial_evidence():
    runner = SecondOrderRunner(SecondOrderCondition.MONITOR_ONLY, run_id="recompute")
    complete(runner, Task("t0", 0.50), True)
    complete(runner, Task("t1", 0.75), False)
    signal = recompute_monitor_signal(runner.ledger.records)
    assert signal is not None
    assert signal.value == 0.5
    assert signal.observations == 2
    assert signal.source is SignalSource.PRIOR_TRIAL_EVIDENCE


@pytest.mark.parametrize(
    ("override", "field"),
    (
        ({"run_id": "other-run"}, "run_id"),
        ({"subject_ref": "other-subject"}, "subject_ref"),
        ({"context_ref": "other-context"}, "context_ref"),
        ({"model_ref": "other-model"}, "model_ref"),
    ),
)
def test_monitor_rejects_mixed_experimental_scope_even_when_outcome_is_missing(
    override,
    field,
):
    first_runner = SecondOrderRunner(SecondOrderCondition.MONITOR_ONLY, run_id="scope")
    first = complete(first_runner, Task("t0", 0.50), True)
    other_runner = SecondOrderRunner(
        SecondOrderCondition.MONITOR_ONLY,
        run_id=override.get("run_id", "scope"),
        subject_ref=override.get("subject_ref", "synthetic-subject"),
        context_ref=override.get("context_ref", "level3-matched-benchmark"),
        model_ref=override.get("model_ref", "finite-predictive-self-model-v0.1.0"),
    )
    pending = other_runner.decide(Task("t1", 0.75))
    missing = other_runner.record_outcome(
        pending,
        actual_success=None,
        evidence_refs=("label:t1",),
        provenance_refs=("fixture:test",),
    )
    with pytest.raises(ValueError, match=field):
        recompute_monitor_signal((first, missing))


def test_ledger_serialization_round_trip_preserves_evidence():
    runner = SecondOrderRunner(SecondOrderCondition.MONITOR_ONLY, run_id="roundtrip")
    complete(runner, Task("t0", 0.50), True)
    complete(runner, Task("t1", 0.75), False)
    complete(runner, Task("t2", 0.60), True)
    restored = TrialLedger.from_json(runner.ledger.to_json())
    assert restored.records == runner.ledger.records
    assert restored.records[-1].outcome_status is OutcomeStatus.OBSERVED


def test_ledger_rejects_duplicate_or_noncontiguous_trials():
    runner = SecondOrderRunner(SecondOrderCondition.MONITOR_ONLY, run_id="ordering")
    record = complete(runner, Task("t0", 0.50), True)
    with pytest.raises(ValueError, match="unique"):
        runner.ledger.append(record)


def test_outcome_must_bind_to_active_pending_decision():
    runner = SecondOrderRunner(SecondOrderCondition.MONITOR_ONLY, run_id="binding")
    pending = runner.decide(Task("t0", 0.50))
    other = SecondOrderRunner(SecondOrderCondition.MONITOR_ONLY, run_id="other").decide(
        Task("t0", 0.50)
    )
    with pytest.raises(ValueError, match="active pending"):
        runner.record_outcome(
            other,
            actual_success=True,
            evidence_refs=("label:t0",),
            provenance_refs=("fixture:test",),
        )
    runner.record_outcome(
        pending,
        actual_success=True,
        evidence_refs=("label:t0",),
        provenance_refs=("fixture:test",),
    )


def test_randomized_control_is_deterministic_and_not_evidence_derived():
    first = randomized_control_signal(seed=3, run_id="r", trial_id="t")
    second = randomized_control_signal(seed=3, run_id="r", trial_id="t")
    assert first == second
    assert first.source is SignalSource.RANDOMIZED_CONTROL
    assert first.observations == 0
    assert first.source_trial_ids == ()
