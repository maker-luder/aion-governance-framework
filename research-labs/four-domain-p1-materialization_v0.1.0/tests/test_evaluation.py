import pytest

from aion_four_domain_p1 import EvaluationCase, EvaluationHarness, TrialObservation


def test_integrated_memory_metrics() -> None:
    case = EvaluationCase(
        case_id="case-1",
        relevant_record_ids=frozenset({"new", "context"}),
        expected_source_ids=frozenset({"source-new"}),
        expected_version_id="v2",
        corrected_old_ids=frozenset({"old"}),
        corrected_new_ids=frozenset({"new"}),
        should_abstain=False,
        required_provenance_fields=frozenset({"source", "recorded_at", "lineage"}),
        supported_claim_ids=frozenset({"claim-ok"}),
    )
    observation = TrialObservation(
        case_id="case-1",
        selected_record_ids=("new", "context"),
        attributed_source_ids=("source-new",),
        resolved_version_id="v2",
        answer_claim_ids=("claim-ok",),
        abstained=False,
        provenance_fields=frozenset({"source", "recorded_at", "lineage"}),
    )

    metrics = EvaluationHarness().evaluate(case, observation).by_name()
    assert metrics["retrieval_precision"].value == 1.0
    assert metrics["retrieval_recall"].value == 1.0
    assert metrics["correction_recovery"].value == 1.0
    assert metrics["stale_memory_influence"].value == 0.0
    assert metrics["unsupported_inference_rate"].value == 0.0


def test_stale_memory_and_unsupported_inference_are_detected() -> None:
    case = EvaluationCase(
        case_id="case-2",
        relevant_record_ids=frozenset({"new"}),
        corrected_old_ids=frozenset({"old"}),
        corrected_new_ids=frozenset({"new"}),
        supported_claim_ids=frozenset({"supported"}),
    )
    observation = TrialObservation(
        case_id="case-2",
        selected_record_ids=("old",),
        answer_claim_ids=("unsupported",),
    )

    metrics = EvaluationHarness().evaluate(case, observation).by_name()
    assert metrics["correction_recovery"].value == 0.0
    assert metrics["stale_memory_influence"].value == pytest.approx(0.5)
    assert metrics["unsupported_inference_rate"].value == 1.0


def test_undefined_metric_is_none_not_synthetic_zero() -> None:
    report = EvaluationHarness().evaluate(EvaluationCase(case_id="empty"), TrialObservation(case_id="empty"))
    metrics = report.by_name()
    assert metrics["retrieval_precision"].value is None
    assert metrics["retrieval_recall"].value is None
    assert metrics["temporal_version_accuracy"].value is None


def test_aggregate_skips_undefined_metrics() -> None:
    harness = EvaluationHarness()
    one = harness.evaluate(
        EvaluationCase(case_id="a", should_abstain=True),
        TrialObservation(case_id="a", abstained=True),
    )
    two = harness.evaluate(EvaluationCase(case_id="b"), TrialObservation(case_id="b"))
    aggregate = harness.aggregate((one, two))
    assert aggregate["abstention_accuracy"] == 1.0
    assert aggregate["temporal_version_accuracy"] is None


def test_case_ids_must_match() -> None:
    with pytest.raises(ValueError, match="case_id mismatch"):
        EvaluationHarness().evaluate(EvaluationCase(case_id="a"), TrialObservation(case_id="b"))
