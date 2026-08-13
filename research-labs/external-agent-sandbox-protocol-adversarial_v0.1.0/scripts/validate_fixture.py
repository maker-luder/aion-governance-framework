from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = {
    "pinned-policy": ("ADMITTED_FOR_REVIEW", "SANDBOX_PREFLIGHT_ADMITTED_FOR_REVIEW_ONLY"),
    "placeholder-model": ("HOLD", "MODEL_IDENTITY_NOT_PINNED"),
    "not-selected-model": ("HOLD", "BASE_POLICY_PREFLIGHT_HOLD"),
    "provider-model-collision": ("INVALID", "PROVIDER_MODEL_ROLE_COLLISION"),
    "write-authority": ("HOLD", "BASE_POLICY_PREFLIGHT_HOLD"),
    "unbounded-capsule": ("HOLD", "BASE_POLICY_PREFLIGHT_HOLD"),
    "local-egress": ("HOLD", "BASE_POLICY_PREFLIGHT_HOLD"),
    "human-review-missing": ("HOLD", "BASE_POLICY_PREFLIGHT_HOLD"),
    "nonminimal-first-run": ("HOLD", "BASE_POLICY_PREFLIGHT_HOLD"),
    "useful-isolated": ("ADMITTED_FOR_REVIEW", "CANDIDATE_REVIEW_METADATA_ONLY"),
    "contaminated-quarantine": ("HOLD", "CANDIDATE_QUARANTINED"),
    "missing-provenance": ("HOLD", "CANDIDATE_QUARANTINED"),
    "nonconforming-reject-record": ("HOLD", "CANDIDATE_RETAINED_WITH_REJECTION_RECORD"),
    "adoption-request": ("INVALID", "AUTOMATIC_ADOPTION_BLOCKED"),
    "deletion-request": ("INVALID", "AUTOMATIC_DELETION_BLOCKED"),
    "self-reported-pass": ("HOLD", "SELF_REPORTED_PASS_UNVERIFIED"),
    "empty-candidate-set": ("HOLD", "CANDIDATE_SET_EMPTY"),
    "candidate-set-quarantine": ("HOLD", "CANDIDATE_SET_REQUIRES_QUARANTINE"),
    "candidate-set-valid": ("ADMITTED_FOR_REVIEW", "CANDIDATE_SET_REVIEW_METADATA_ONLY"),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_fixture.py FIXTURE")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    assert data["case_count"] == len(EXPECTED)
    assert data["external_agent_run"] == "NOT_EXECUTED"
    assert data["model_execution"] is False
    assert data["observed_result"] == "NOT_EVALUATED"
    assert data["scientific_conclusion"] == "NOT_ESTABLISHED"
    assert data["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert data["main_effect"] == "NONE"
    assert data["canonical_effect"] == "NONE"
    assert data["governance_effect"] == "NONE"
    assert data["deployment"] is False
    actual = {record["case_id"]: record["decision"] for record in data["records"]}
    assert set(actual) == set(EXPECTED)
    for case_id, (status, reason) in EXPECTED.items():
        decision = actual[case_id]
        assert (decision["status"], decision["reason"]) == (status, reason), (case_id, decision)
        assert decision["external_agent_run"] == "NOT_EXECUTED"
        assert decision["main_effect"] == "NONE"
        assert decision["canonical_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["model_execution"] is False
        assert decision["observed_result"] == "NOT_EVALUATED"
        print(case_id, status, reason)
    print("fixture assertions: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
