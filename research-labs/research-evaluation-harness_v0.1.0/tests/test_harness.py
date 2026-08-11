from __future__ import annotations

import pytest

from aion_research_eval import (
    ClaimBoundaryGate,
    EqualsExpected,
    MetadataFlag,
    PredicateEvaluator,
    ResearchCase,
    ResearchDataset,
    compare_reports,
    evaluate_dataset,
)


def dataset() -> ResearchDataset:
    return ResearchDataset(
        name="upper",
        cases=(
            ResearchCase("c1", "hello", "HELLO", {"approved": True}),
            ResearchCase("c2", "world", "WORLD", {"approved": True}),
        ),
        evaluators=(EqualsExpected(), MetadataFlag("approved")),
    )


def test_duplicate_case_ids_rejected() -> None:
    with pytest.raises(ValueError):
        ResearchDataset("bad", (ResearchCase("x", 1), ResearchCase("x", 2)))


def test_dataset_and_case_evaluators_both_run() -> None:
    ds = ResearchDataset(
        "mixed",
        (ResearchCase("x", 2, 4, {}, (PredicateEvaluator(lambda o, e, m: o % 2 == 0),)),),
        (EqualsExpected(),),
    )
    report = evaluate_dataset(ds, lambda x: x * 2, implementation_id="double")
    assert len(report.cases[0].evidence) == 2
    assert report.cases[0].assertions_passed is True


def test_pass_rate_is_computed_from_assertable_cases() -> None:
    report = evaluate_dataset(dataset(), str.upper, implementation_id="upper")
    assert report.pass_rate == 1.0


def test_failed_implementation_is_visible() -> None:
    report = evaluate_dataset(dataset(), lambda x: x, implementation_id="identity")
    assert report.pass_rate == 0.0


def test_report_preserves_metadata() -> None:
    report = evaluate_dataset(dataset(), str.upper, implementation_id="upper")
    assert report.cases[0].metadata["approved"] is True


def test_report_is_serializable_to_plain_dict() -> None:
    report = evaluate_dataset(dataset(), str.upper, implementation_id="upper")
    data = report.to_dict()
    assert data["research_only"] is True
    assert data["canonical_effect"] == "NONE"


def test_compare_reports_keeps_claim_boundary() -> None:
    good = evaluate_dataset(dataset(), str.upper, implementation_id="good")
    bad = evaluate_dataset(dataset(), lambda x: x, implementation_id="bad")
    comparison = compare_reports(good, bad)
    assert comparison["left_pass_rate"] == 1.0
    assert comparison["right_pass_rate"] == 0.0
    assert comparison["canonical_effect"] == "NONE"


def test_compare_requires_same_dataset() -> None:
    left = evaluate_dataset(dataset(), str.upper, implementation_id="left")
    right_ds = ResearchDataset("other", (ResearchCase("x", 1, 1),), (EqualsExpected(),))
    right = evaluate_dataset(right_ds, lambda x: x, implementation_id="right")
    with pytest.raises(ValueError):
        compare_reports(left, right)


def test_claim_boundary_denies_subjectivity_promotion() -> None:
    assert ClaimBoundaryGate().disposition("subjectivity_established") == "DENY_PROMOTION"


def test_claim_boundary_leaves_ordinary_findings_as_research_only() -> None:
    assert ClaimBoundaryGate().disposition("recall_gate_blocks_conflict") == "RESEARCH_EVIDENCE_ONLY"


def test_score_range_is_fail_closed() -> None:
    from aion_research_eval.core import EvidenceResult

    with pytest.raises(ValueError):
        EvidenceResult(evaluator="bad", score=1.5)
