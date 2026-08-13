from aion_research_eval import CaseResult, EvidenceResult, ExperimentReport

from aion_research_eval_adversarial import AuditStatus, audit_evaluation_report, audit_report_comparison

DATASET = "dataset:bounded"
IDS = ("case:1", "case:2")


def case(case_id: str, *, passed: bool | None = True, metadata: dict[str, object] | None = None, evidence: tuple[EvidenceResult, ...] | None = None, elapsed_ms: float = 1.0) -> CaseResult:
    return CaseResult(
        case_id=case_id,
        output="observed",
        expected_output="expected",
        metadata=metadata if metadata is not None else {"case_provenance_ref": f"prov:{case_id}"},
        evidence=evidence if evidence is not None else (EvidenceResult("equals", passed=passed),),
        elapsed_ms=elapsed_ms,
    )


def report(*, implementation_id: str = "impl:1", cases: tuple[CaseResult, ...] = (case("case:1"), case("case:2")), **overrides) -> ExperimentReport:
    data = dict(
        dataset_name=DATASET,
        implementation_id=implementation_id,
        started_at="2026-08-13T00:00:00+00:00",
        finished_at="2026-08-13T00:00:01+00:00",
        cases=cases,
        research_only=True,
        canonical_effect="NONE",
    )
    data.update(overrides)
    return ExperimentReport(**data)


def assert_no_effect(audit) -> None:
    assert audit.canonical_effect == "NONE"
    assert audit.governance_effect == "NONE"
    assert audit.deployment is False
    assert audit.research_only is True
    assert audit.scientific_conclusion == "NOT_ESTABLISHED"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert audit.model_execution is False
    assert audit.observed_result == "NOT_EVALUATED"


def test_valid_report_admitted_for_review_only() -> None:
    audit = audit_evaluation_report(report(), expected_dataset=DATASET, expected_case_ids=IDS)
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "EVALUATION_REPORT_ADMITTED_FOR_REVIEW_ONLY"
    assert audit.case_count == 2
    assert_no_effect(audit)


def test_expected_dataset_required() -> None:
    audit = audit_evaluation_report(report(), expected_dataset="", expected_case_ids=IDS)
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "EXPECTED_DATASET_MISSING"
    assert_no_effect(audit)


def test_dataset_scope_mismatch_holds() -> None:
    audit = audit_evaluation_report(report(), expected_dataset="dataset:other", expected_case_ids=IDS)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "DATASET_SCOPE_MISMATCH"
    assert_no_effect(audit)


def test_implementation_id_missing_is_invalid() -> None:
    audit = audit_evaluation_report(report(implementation_id=""), expected_dataset=DATASET, expected_case_ids=IDS)
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "IMPLEMENTATION_ID_MISSING"
    assert_no_effect(audit)


def test_research_only_flag_disabled_is_invalid() -> None:
    audit = audit_evaluation_report(report(research_only=False), expected_dataset=DATASET, expected_case_ids=IDS)
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "RESEARCH_ONLY_FLAG_DISABLED"
    assert_no_effect(audit)


def test_canonical_effect_requested_is_invalid() -> None:
    audit = audit_evaluation_report(report(canonical_effect="WRITE"), expected_dataset=DATASET, expected_case_ids=IDS)
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "CANONICAL_EFFECT_REQUESTED"
    assert_no_effect(audit)


def test_case_coverage_mismatch_holds() -> None:
    audit = audit_evaluation_report(report(cases=(case("case:1"),)), expected_dataset=DATASET, expected_case_ids=IDS)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "CASE_COVERAGE_MISMATCH"
    assert_no_effect(audit)


def test_duplicate_case_id_is_invalid() -> None:
    audit = audit_evaluation_report(report(cases=(case("case:1"), case("case:1"))), expected_dataset=DATASET, expected_case_ids=IDS)
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "DUPLICATE_CASE_ID"
    assert_no_effect(audit)


def test_case_id_missing_is_invalid() -> None:
    audit = audit_evaluation_report(report(cases=(case(""),)), expected_dataset=DATASET)
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "CASE_ID_MISSING"
    assert_no_effect(audit)


def test_case_evidence_missing_holds() -> None:
    audit = audit_evaluation_report(report(cases=(case("case:1", evidence=()),)), expected_dataset=DATASET)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "CASE_EVIDENCE_MISSING"
    assert_no_effect(audit)


def test_evaluator_id_missing_is_invalid() -> None:
    audit = audit_evaluation_report(report(cases=(case("case:1", evidence=(EvidenceResult("", passed=True),)),)), expected_dataset=DATASET)
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "EVALUATOR_ID_MISSING"
    assert_no_effect(audit)


def test_case_provenance_missing_holds() -> None:
    audit = audit_evaluation_report(report(cases=(case("case:1", metadata={"note": "no provenance"}),)), expected_dataset=DATASET)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "CASE_PROVENANCE_INCOMPLETE"
    assert_no_effect(audit)


def test_negative_evaluation_is_retained_as_review_metadata() -> None:
    audit = audit_evaluation_report(report(cases=(case("case:1", passed=False), case("case:2", passed=False))), expected_dataset=DATASET, expected_case_ids=IDS)
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.pass_rate == 0.0
    assert_no_effect(audit)


def test_nonfinite_elapsed_time_is_invalid() -> None:
    audit = audit_evaluation_report(report(cases=(case("case:1", elapsed_ms=float("nan")),)), expected_dataset=DATASET)
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "ELAPSED_TIME_INVALID"
    assert_no_effect(audit)


def test_negative_elapsed_time_is_invalid() -> None:
    audit = audit_evaluation_report(report(cases=(case("case:1", elapsed_ms=-1.0),)), expected_dataset=DATASET)
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "ELAPSED_TIME_INVALID"
    assert_no_effect(audit)


def test_forbidden_claim_promotion_is_invalid() -> None:
    audit = audit_evaluation_report(report(), expected_dataset=DATASET, forbidden_claim="subjectivity_established")
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "FORBIDDEN_CLAIM_PROMOTION"
    assert_no_effect(audit)


def test_ordinary_claim_remains_review_only() -> None:
    audit = audit_evaluation_report(report(), expected_dataset=DATASET, forbidden_claim="accuracy_observed")
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert_no_effect(audit)


def test_comparison_with_distinct_implementations_is_review_only() -> None:
    audit = audit_report_comparison(report(), report(implementation_id="impl:2"), expected_dataset=DATASET)
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "COMPARISON_ADMITTED_FOR_REVIEW_ONLY"
    assert_no_effect(audit)


def test_comparison_implementation_collision_is_invalid() -> None:
    audit = audit_report_comparison(report(), report(), expected_dataset=DATASET)
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "COMPARISON_IMPLEMENTATION_COLLISION"
    assert_no_effect(audit)


def test_comparison_dataset_mismatch_holds() -> None:
    audit = audit_report_comparison(report(), report(implementation_id="impl:2", dataset_name="dataset:other"), expected_dataset=DATASET)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "COMPARISON_DATASET_MISMATCH"
    assert_no_effect(audit)


def test_comparison_case_order_mismatch_holds() -> None:
    other = report(implementation_id="impl:2", cases=(case("case:2"), case("case:1")))
    audit = audit_report_comparison(report(), other, expected_dataset=DATASET)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "COMPARISON_CASE_ORDER_MISMATCH"
    assert_no_effect(audit)
