from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = {
    "valid-record": ("ADMITTED_FOR_REVIEW", "MEMORY_RECORD_REVIEW_METADATA_ONLY"),
    "missing-field": ("INVALID", "MEMORY_FIELD_MISSING"),
    "timezone-invalid": ("INVALID", "CREATED_AT_TIMEZONE_INVALID"),
    "revision-zero": ("INVALID", "REVISION_INVALID"),
    "initial-supersedes": ("INVALID", "INITIAL_RECORD_CANNOT_SUPERSEDE"),
    "revision-parent-missing": ("INVALID", "REVISION_PARENT_MISSING"),
    "non-active-record": ("HOLD", "NON_ACTIVE_MEMORY_NOT_CONTEXT_ELIGIBLE"),
    "empty-store": ("HOLD", "MEMORY_STORE_EMPTY"),
    "duplicate-memory-id": ("INVALID", "DUPLICATE_MEMORY_ID"),
    "revision-parent-not-found": ("INVALID", "REVISION_PARENT_NOT_FOUND"),
    "revision-scope-drift": ("INVALID", "REVISION_SCOPE_DRIFT"),
    "revision-number-drift": ("INVALID", "REVISION_NUMBER_DRIFT"),
    "source-reference-reuse": ("HOLD", "SOURCE_REF_REUSE_REQUIRES_REVIEW"),
    "discarded-retained": ("HOLD", "DISCARDED_MEMORY_RETAINED_OUTSIDE_CONTEXT"),
    "valid-revision-chain": ("ADMITTED_FOR_REVIEW", "MEMORY_STORE_REVIEW_METADATA_ONLY"),
    "valid-lineage": ("ADMITTED_FOR_REVIEW", "MEMORY_LINEAGE_REVIEW_METADATA_ONLY"),
    "missing-lineage-id": ("INVALID", "MEMORY_ID_NOT_FOUND"),
    "valid-retrieval": ("ADMITTED_FOR_REVIEW", "RETRIEVAL_TRACE_REVIEW_METADATA_ONLY"),
    "retrieval-scope-missing": ("INVALID", "RETRIEVAL_SCOPE_MISSING"),
    "considered-duplicate": ("INVALID", "DUPLICATE_CONSIDERED_ID"),
    "blocked-duplicate": ("INVALID", "DUPLICATE_BLOCKED_ID"),
    "considered-blocked-overlap": ("INVALID", "CONSIDERED_BLOCKED_OVERLAP"),
    "non-active-hit": ("INVALID", "NON_ACTIVE_MEMORY_RETURNED"),
    "hit-not-considered": ("INVALID", "HIT_NOT_CONSIDERED"),
    "hit-scope-mismatch": ("INVALID", "HIT_SCOPE_MISMATCH"),
    "hit-score-invalid": ("INVALID", "HIT_SCORE_OR_TERMS_INVALID"),
    "hit-terms-empty": ("INVALID", "HIT_SCORE_OR_TERMS_INVALID"),
    "hit-order-invalid": ("INVALID", "HIT_ORDER_INVALID"),
    "hit-record-not-found": ("INVALID", "HIT_RECORD_NOT_FOUND"),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_fixture.py FIXTURE")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    assert data["case_count"] == len(EXPECTED)
    assert data["memory_store_execution"] is False
    assert data["model_execution"] is False
    assert data["observed_result"] == "NOT_EVALUATED"
    assert data["memory_truth"] == "NOT_ESTABLISHED"
    assert data["identity_continuity"] == "NOT_ESTABLISHED"
    assert data["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert data["authority"] == "REVIEW_METADATA_ONLY"
    assert data["canonical_effect"] == "NONE"
    assert data["governance_effect"] == "NONE"
    assert data["deployment"] is False
    actual = {record["case_id"]: record["decision"] for record in data["records"]}
    assert set(actual) == set(EXPECTED)
    for case_id, (status, reason) in EXPECTED.items():
        decision = actual[case_id]
        assert (decision["status"], decision["reason"]) == (status, reason), (case_id, decision)
        assert decision["authority"] == "REVIEW_METADATA_ONLY"
        assert decision["memory_truth"] == "NOT_ESTABLISHED"
        assert decision["identity_continuity"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["canonical_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["model_execution"] is False
        assert decision["observed_result"] == "NOT_EVALUATED"
        print(case_id, status, reason)
    print("fixture assertions: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
