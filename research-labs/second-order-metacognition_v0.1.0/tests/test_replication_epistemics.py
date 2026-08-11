from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from aion_second_order import (
    FixtureProvenance,
    ReplicationAssessment,
    ReplicationAttempt,
    ReplicationInterpretation,
    ReplicationMode,
    ReplicationOutcome,
    ReplicationRunner,
    ReplicationValidity,
    evaluator_drift_detected,
)


def attempt(
    attempt_id: str,
    outcome: ReplicationOutcome,
    *,
    validity: ReplicationValidity = ReplicationValidity.VALID,
    mode: ReplicationMode = ReplicationMode.REPLICATION,
    group: str = "group-a",
    evaluator: str = "eval:v1",
) -> ReplicationAttempt:
    fixture = FixtureProvenance(
        fixture_author="fixture-author",
        fixture_version="v1",
        fixture_hash="a" * 64,
        experiment_run=f"run:{attempt_id}",
        implementation_version="impl-v1",
        seed=17,
        mode=mode,
    )
    return ReplicationAttempt(
        attempt_id=attempt_id,
        claim_ref="claim:functional-effect",
        fixture_ref="fixture:matched-v1",
        fixture=fixture,
        protocol_ref="protocol:replication",
        protocol_version="v1",
        implementation_ref="implementation:reference",
        implementation_version="impl-v1",
        evaluator_ref="evaluator:contract",
        evaluator_version=evaluator,
        evaluation_contract_ref="contract:binary-outcome-v1",
        independent_group_ref=group,
        seed=17,
        outcome=outcome,
        validity=validity,
        provenance_refs=("fixture:public", "implementation:codex-research"),
        executed_at="2026-08-11T00:00:00Z",
        observation_ref=f"observation:{attempt_id}",
        preregistered=True,
    )


def test_attempt_round_trip_preserves_raw_outcome_validity_and_evaluator_provenance():
    source = attempt("attempt-1", ReplicationOutcome.FAILED)
    payload = source.to_json()
    restored = ReplicationAttempt.from_json(payload)
    assert restored == source
    assert restored.to_json() == payload
    assert restored.outcome is ReplicationOutcome.FAILED
    assert restored.validity is ReplicationValidity.VALID
    assert restored.evaluation_contract_ref == "contract:binary-outcome-v1"


def test_assessment_is_separate_and_cannot_overwrite_frozen_raw_attempt():
    raw = attempt("attempt-raw", ReplicationOutcome.FAILED)
    assessment = ReplicationAssessment(
        assessment_id="assessment-raw",
        attempt_ref=raw.attempt_id,
        interpretation=ReplicationInterpretation.EVALUATOR_DRIFT,
        reason="Outcome differs only after evaluator version changed.",
        evaluator_ref="evaluator:review",
        evaluator_version="review-v1",
        evaluation_contract_ref="contract:replication-assessment-v1",
        provenance_refs=("review:chatgpt", "implementation:codex-research"),
    )
    assert assessment.attempt_ref == raw.attempt_id
    assert raw.outcome is ReplicationOutcome.FAILED
    with pytest.raises(FrozenInstanceError):
        raw.outcome = ReplicationOutcome.CONFIRMED  # type: ignore[misc]


def test_record_preserves_all_attempt_counts_including_mixed_and_inconclusive():
    runner = ReplicationRunner()
    for item in (
        attempt("a-confirm", ReplicationOutcome.CONFIRMED, group="g1"),
        attempt("a-fail", ReplicationOutcome.FAILED, group="g2"),
        attempt("a-mixed", ReplicationOutcome.MIXED, group="g3"),
        attempt("a-inconclusive", ReplicationOutcome.INCONCLUSIVE, group="g4"),
    ):
        runner.register(item)
    record = runner.record("record-1", provenance_refs=("record:fixture",))
    assert record.attempt_count == 4
    assert record.confirmed_count == record.failed_count == 1
    assert record.mixed_count == record.inconclusive_count == 1
    assert record.independent_group_count == 4
    assert record.attempt_refs == ("a-confirm", "a-fail", "a-mixed", "a-inconclusive")
    assert record.automatic_evidence_level_override == "NONE"


def test_same_seed_reproduction_is_not_counted_as_independent_replication():
    runner = ReplicationRunner()
    runner.register(
        attempt(
            "same-seed-rerun",
            ReplicationOutcome.CONFIRMED,
            mode=ReplicationMode.REPRODUCTION,
        )
    )
    record = runner.record("reproduction-record", provenance_refs=("record:test",))
    assert record.independent_group_count == 0


def test_evaluator_drift_comparison_reports_drift_without_selecting_correct_evaluator():
    left = attempt("eval-left", ReplicationOutcome.CONFIRMED, evaluator="v1")
    right = attempt("eval-right", ReplicationOutcome.FAILED, evaluator="v2")
    assert evaluator_drift_detected(left, right) is True
    assert not hasattr(left, "evaluator_is_correct")
    assert not hasattr(right, "evaluator_is_correct")


def test_invalid_failed_attempt_remains_failed_observation_with_separate_validity():
    raw = attempt(
        "invalid-failure",
        ReplicationOutcome.FAILED,
        validity=ReplicationValidity.INVALID,
    )
    assert raw.outcome is ReplicationOutcome.FAILED
    assert raw.validity is ReplicationValidity.INVALID
