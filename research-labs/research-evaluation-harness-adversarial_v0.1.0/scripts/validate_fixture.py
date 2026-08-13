from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = {
    "valid-report": ("ADMITTED_FOR_REVIEW", "EVALUATION_REPORT_ADMITTED_FOR_REVIEW_ONLY"),
    "dataset-scope-mismatch": ("HOLD", "DATASET_SCOPE_MISMATCH"),
    "implementation-id-missing": ("INVALID", "IMPLEMENTATION_ID_MISSING"),
    "research-only-disabled": ("INVALID", "RESEARCH_ONLY_FLAG_DISABLED"),
    "canonical-effect-requested": ("INVALID", "CANONICAL_EFFECT_REQUESTED"),
    "case-coverage-mismatch": ("HOLD", "CASE_COVERAGE_MISMATCH"),
    "duplicate-case-id": ("INVALID", "DUPLICATE_CASE_ID"),
    "case-evidence-missing": ("HOLD", "CASE_EVIDENCE_MISSING"),
    "evaluator-id-missing": ("INVALID", "EVALUATOR_ID_MISSING"),
    "case-provenance-incomplete": ("HOLD", "CASE_PROVENANCE_INCOMPLETE"),
    "negative-result-retained": ("ADMITTED_FOR_REVIEW", "EVALUATION_REPORT_ADMITTED_FOR_REVIEW_ONLY"),
    "elapsed-time-invalid": ("INVALID", "ELAPSED_TIME_INVALID"),
    "forbidden-claim": ("INVALID", "FORBIDDEN_CLAIM_PROMOTION"),
    "ordinary-claim": ("ADMITTED_FOR_REVIEW", "EVALUATION_REPORT_ADMITTED_FOR_REVIEW_ONLY"),
    "comparison-valid": ("ADMITTED_FOR_REVIEW", "COMPARISON_ADMITTED_FOR_REVIEW_ONLY"),
    "comparison-implementation-collision": ("INVALID", "COMPARISON_IMPLEMENTATION_COLLISION"),
    "comparison-dataset-mismatch": ("HOLD", "COMPARISON_DATASET_MISMATCH"),
    "comparison-case-order-mismatch": ("HOLD", "COMPARISON_CASE_ORDER_MISMATCH"),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_fixture.py FIXTURE")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    assert data["case_count"] == len(EXPECTED)
    assert data["model_execution"] is False
    assert data["observed_result"] == "NOT_EVALUATED"
    assert data["scientific_conclusion"] == "NOT_ESTABLISHED"
    assert data["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert data["canonical_effect"] == "NONE"
    assert data["governance_effect"] == "NONE"
    assert data["deployment"] is False
    actual = {record["case_id"]: record["decision"] for record in data["records"]}
    assert set(actual) == set(EXPECTED)
    for case_id, (status, reason) in EXPECTED.items():
        decision = actual[case_id]
        assert (decision["status"], decision["reason"]) == (status, reason), (case_id, decision)
        assert decision["canonical_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["research_only"] is True
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["model_execution"] is False
        assert decision["observed_result"] == "NOT_EVALUATED"
        print(case_id, status, reason)
    print("fixture assertions: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
