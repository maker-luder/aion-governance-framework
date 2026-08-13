from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = {
    "valid-confirmatory": ("VALID", "CONFIRMATORY_REVIEW", "VALID_CONFIRMATORY_PLAN_AND_REPORT"),
    "missing-plan-id": ("INVALID", "HOLD", "MISSING_PLAN_ID_OR_VERSION"),
    "digest-whitespace": ("INVALID", "HOLD", "IMMUTABLE_DIGEST_FORMAT_INVALID"),
    "missing-protocol": ("INDETERMINATE", "HOLD", "MISSING_PLAN_IMMUTABILITY_OR_PROTOCOL"),
    "outcome-id-missing": ("INVALID", "HOLD", "OUTCOME_ID_MISSING"),
    "analysis-id-missing": ("INVALID", "HOLD", "ANALYSIS_ID_MISSING"),
    "report-unknown-outcome": ("INVALID", "HOLD", "REPORT_UNKNOWN_OUTCOME"),
    "report-unknown-analysis": ("INVALID", "HOLD", "REPORT_UNKNOWN_ANALYSIS"),
    "exploratory-unknown-analysis": ("INVALID", "HOLD", "EXPLORATORY_UNKNOWN_ANALYSIS"),
    "duplicate-deviation-id": ("INVALID", "HOLD", "DUPLICATE_DEVIATION_ID"),
    "missing-deviation-id": ("INVALID", "HOLD", "DEVIATION_ID_MISSING"),
    "registration-after-start": ("INVALID", "HOLD", "REGISTRATION_AFTER_INTERVENTION_START"),
    "exploratory-separated": ("VALID", "EXPLORATORY_REVIEW", "VALID_WITH_EXPLORATORY_ANALYSES_SEPARATED"),
    "missing-reported-results": ("INDETERMINATE", "HOLD", "ALL_PREREGISTERED_RESULTS_NOT_REPORTED"),
    "undisclosed-deviation": ("INDETERMINATE", "HOLD", "DEVIATION_DISCLOSURE_INCOMPLETE"),
    "valid-disclosed-deviation": ("VALID", "CONFIRMATORY_REVIEW", "VALID_CONFIRMATORY_PLAN_AND_REPORT"),
    "lock-unchanged": ("VALID", "CONFIRMATORY_REVIEW", "OUTCOME_LOCK_UNCHANGED"),
    "post-outcome-new-declaration": ("INVALID", "HOLD", "POST_OUTCOME_DECLARATION_MUTATION"),
    "post-outcome-digest-change": ("INVALID", "HOLD", "PLAN_DIGEST_CHANGED_AFTER_OUTCOME"),
    "pre-outcome-change-review": ("INDETERMINATE", "HOLD", "PRE_OUTCOME_PLAN_CHANGE_REQUIRES_REVIEW"),
    "lock-plan-id-missing": ("INVALID", "HOLD", "LOCK_PLAN_ID_MISSING"),
    "lock-digest-missing": ("INVALID", "HOLD", "LOCK_DIGEST_MISSING"),
    "intervention-boundary": ("VALID", "CONFIRMATORY_REVIEW", "VALID_CONFIRMATORY_PLAN_AND_REPORT"),
    "plan-version-missing": ("INVALID", "HOLD", "MISSING_PLAN_ID_OR_VERSION"),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_fixture.py FIXTURE")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    assert data["case_count"] == len(EXPECTED)
    assert data["intervention_executed"] is False
    assert data["observed_outcomes"] is False
    assert data["model_execution"] is False
    assert data["observed_result"] == "NOT_EVALUATED"
    assert data["scientific_conclusion"] == "NOT_ESTABLISHED"
    assert data["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert data["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
    assert data["canonical_effect"] == "NONE"
    assert data["governance_effect"] == "NONE"
    assert data["deployment"] is False
    actual = {record["case_id"]: record["decision"] for record in data["records"]}
    assert set(actual) == set(EXPECTED)
    for case_id, (status, disposition, reason) in EXPECTED.items():
        decision = actual[case_id]
        assert (decision["status"], decision["disposition"], decision["reason"]) == (status, disposition, reason), (case_id, decision)
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["canonical_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["intervention_executed"] is False
        assert decision["observed_outcomes"] is False
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
        print(case_id, status, disposition, reason)
    print("fixture assertions: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
