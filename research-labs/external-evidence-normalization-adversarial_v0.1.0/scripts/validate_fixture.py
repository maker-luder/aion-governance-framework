from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED = {
    "static-review": ("ADMITTED_FOR_REVIEW", "EXTERNAL_EVIDENCE_ADMITTED_FOR_REVIEW_ONLY"),
    "logical-reproduction": ("ADMITTED_FOR_REVIEW", "EXTERNAL_EVIDENCE_ADMITTED_FOR_REVIEW_ONLY"),
    "executed-without-observation": ("HOLD", "EXECUTED_RESULT_CLAIM_WITHOUT_OBSERVATION"),
    "executed-with-observation": ("ADMITTED_FOR_REVIEW", "EXTERNAL_EVIDENCE_ADMITTED_FOR_REVIEW_ONLY"),
    "duplicate-report-id": ("INVALID", "DUPLICATE_REPORT_ID"),
    "branch-scope-mismatch": ("HOLD", "BRANCH_SCOPE_MISMATCH"),
    "main-branch-blocked": ("INVALID", "MAIN_BRANCH_RESEARCH_EVIDENCE_BLOCKED"),
    "unknown-actor": ("HOLD", "ACTOR_IDENTITY_UNRESOLVED"),
    "unknown-mode-with-digest": ("HOLD", "UNKNOWN_MODE_CANNOT_CARRY_EXECUTION_DIGESTS"),
    "unknown-mode": ("HOLD", "BASE_NORMALIZER_REQUIRES_PROVENANCE"),
    "empty-executed-claim": ("HOLD", "EXECUTED_REPLICATION_RESULT_CLAIM_MISSING"),
    "static-observation-overreach": ("INVALID", "RESULT_OBSERVATION_EXCEEDS_DECLARED_EXECUTION_MODE"),
    "static-pass-hash-masquerade": ("INVALID", "BASE_NORMALIZER_REJECTED_CLAIM"),
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
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["observed_result"] == "NOT_EVALUATED"
        print(case_id, status, reason)
    print("fixture assertions: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
