from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = {
    "read-approved": ("ADMITTED_FOR_REVIEW", "APPROVAL_DISPOSITION_REVIEW_ONLY"),
    "missing-call-id": ("INVALID", "CALL_ID_MISSING"),
    "call-id-scope-mismatch": ("HOLD", "CALL_ID_SCOPE_MISMATCH"),
    "unmatched-call": ("HOLD", "TOOL_CALL_NOT_EXECUTABLE"),
    "escalate-then-approve": ("ADMITTED_FOR_REVIEW", "APPROVAL_DISPOSITION_REVIEW_ONLY"),
    "reject-call": ("HOLD", "TOOL_CALL_NOT_EXECUTABLE"),
    "terminate-call": ("HOLD", "TOOL_CALL_NOT_EXECUTABLE"),
    "python-without-sandbox": ("HOLD", "SANDBOX_REQUIRED_BUT_ABSENT"),
    "python-with-sandbox": ("ADMITTED_FOR_REVIEW", "APPROVAL_DISPOSITION_REVIEW_ONLY"),
    "restricted-sandbox": ("ADMITTED_FOR_REVIEW", "APPROVAL_DISPOSITION_REVIEW_ONLY"),
    "execution-request": ("INVALID", "EXECUTION_REQUEST_EXCEEDS_RESEARCH_BOUNDARY"),
    "modify-arguments": ("ADMITTED_FOR_REVIEW", "APPROVAL_DISPOSITION_REVIEW_ONLY"),
    "argument-scope-allowed": ("ADMITTED_FOR_REVIEW", "APPROVAL_DISPOSITION_REVIEW_ONLY"),
    "argument-scope-denied": ("HOLD", "TOOL_CALL_NOT_EXECUTABLE"),
    "empty-batch": ("HOLD", "CALL_BATCH_EMPTY"),
    "duplicate-batch": ("INVALID", "DUPLICATE_CALL_ID"),
    "batch-missing-call-id": ("INVALID", "CALL_ID_MISSING"),
    "batch-canonical-effect": ("INVALID", "CANONICAL_EFFECT_REQUESTED"),
    "batch-event-flag": ("INVALID", "APPROVAL_EVENT_ONLY_FLAG_MISSING"),
    "valid-batch": ("ADMITTED_FOR_REVIEW", "CALL_BATCH_REVIEW_ONLY"),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_fixture.py FIXTURE")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    assert data["case_count"] == len(EXPECTED)
    assert data["tool_execution"] is False
    assert data["model_execution"] is False
    assert data["observed_result"] == "NOT_EVALUATED"
    assert data["scientific_conclusion"] == "NOT_ESTABLISHED"
    assert data["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert data["approval_event_only"] is True
    assert data["canonical_effect"] == "NONE"
    assert data["governance_effect"] == "NONE"
    assert data["deployment"] is False
    actual = {record["case_id"]: record["decision"] for record in data["records"]}
    assert set(actual) == set(EXPECTED)
    for case_id, (status, reason) in EXPECTED.items():
        decision = actual[case_id]
        assert (decision["status"], decision["reason"]) == (status, reason), (case_id, decision)
        assert decision["approval_event_only"] is True
        assert decision["canonical_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["model_execution"] is False
        assert decision["observed_result"] == "NOT_EVALUATED"
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        print(case_id, status, reason)
    print("fixture assertions: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
