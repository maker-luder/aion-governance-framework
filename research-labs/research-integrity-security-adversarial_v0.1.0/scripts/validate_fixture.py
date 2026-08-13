from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = {
    "clean-evidence": ("ADMITTED_FOR_REVIEW", "EVIDENCE_CANDIDATE_REVIEW_ONLY"),
    "missing-evidence-id": ("INVALID", "EVIDENCE_ID_MISSING"),
    "raw-hash-whitespace": ("INVALID", "RAW_HASH_FORMAT_INVALID"),
    "prompt-induced": ("HOLD", "EVIDENCE_STATE_PROMPT_INDUCED"),
    "roleplay-contaminated": ("HOLD", "EVIDENCE_STATE_ROLEPLAY_CONTAMINATED"),
    "edited-without-history": ("HOLD", "EVIDENCE_STATE_QUARANTINED"),
    "missing-hash": ("INVALID", "EVIDENCE_STATE_NOT_ADMISSIBLE"),
    "missing-provenance": ("INVALID", "EVIDENCE_STATE_NOT_ADMISSIBLE"),
    "context-incomplete": ("HOLD", "EVIDENCE_STATE_CONTEXT_INCOMPLETE"),
    "valid-provenance": ("ADMITTED_FOR_REVIEW", "PROVENANCE_REVIEW_METADATA_ONLY"),
    "provenance-field-missing": ("INVALID", "PROVENANCE_FIELD_MISSING"),
    "source-class-uncontrolled": ("INVALID", "SOURCE_CLASS_UNCONTROLLED"),
    "currentness-uncontrolled": ("INVALID", "CURRENTNESS_UNCONTROLLED"),
    "retrieved-at-timezone-invalid": ("INVALID", "RETRIEVED_AT_TIMEZONE_INVALID"),
    "approval-attribution-collapsed": ("INVALID", "APPROVAL_ATTRIBUTION_COLLAPSED"),
    "canonical-effect-requested": ("INVALID", "CANONICAL_EFFECT_REQUESTED"),
    "unverified-source": ("HOLD", "PROVENANCE_REQUIRES_REVIEW"),
    "stale-source": ("HOLD", "PROVENANCE_REQUIRES_REVIEW"),
    "valid-tombstone": ("ADMITTED_FOR_REVIEW", "SUPPRESSION_TOMBSTONE_REVIEW_METADATA_ONLY"),
    "tombstone-input-missing": ("INVALID", "TOMBSTONE_INPUT_MISSING"),
    "tombstone-field-missing": ("INVALID", "TOMBSTONE_FIELD_MISSING"),
    "tombstone-status-invalid": ("INVALID", "TOMBSTONE_STATUS_INVALID"),
    "tombstone-content-deletion": ("INVALID", "SUPPRESSION_CONTENT_DELETION_UNVERIFIED"),
    "explicit-permission": ("ADMITTED_FOR_REVIEW", "ACTION_PERMISSION_REVIEW_ONLY"),
    "relationship-no-permission": ("HOLD", "ACTION_PERMISSION_NOT_ESTABLISHED"),
    "prohibited-conclusion": ("INVALID", "PROHIBITED_CONCLUSION_DENIED"),
    "empty-batch": ("HOLD", "EVIDENCE_BATCH_EMPTY"),
    "duplicate-batch": ("INVALID", "DUPLICATE_EVIDENCE_ID"),
    "invalid-batch": ("INVALID", "EVIDENCE_BATCH_CONTAINS_INVALID"),
    "held-batch": ("HOLD", "EVIDENCE_BATCH_REQUIRES_REVIEW"),
    "valid-batch": ("ADMITTED_FOR_REVIEW", "EVIDENCE_BATCH_REVIEW_METADATA_ONLY"),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_fixture.py FIXTURE")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    assert data["case_count"] == len(EXPECTED)
    assert data["security_incident"] is False
    assert data["credentials_accessed"] is False
    assert data["external_action_executed"] is False
    assert data["model_execution"] is False
    assert data["observed_result"] == "NOT_EVALUATED"
    assert data["scientific_conclusion"] == "NOT_ESTABLISHED"
    assert data["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert data["identity_conclusion"] == "NOT_ESTABLISHED"
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
        assert decision["canonical_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["security_incident"] is False
        assert decision["action_executed"] is False
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["identity_conclusion"] == "NOT_ESTABLISHED"
        print(case_id, status, reason)
    print("fixture assertions: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
