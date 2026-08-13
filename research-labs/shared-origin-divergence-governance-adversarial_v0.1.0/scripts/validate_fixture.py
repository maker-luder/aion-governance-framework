from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = {
    "shared-origin": ("ADMITTED_FOR_REVIEW", "SHARED_ORIGIN_REVIEW_METADATA_ONLY"),
    "empty-event-sequence": ("HOLD", "EVENT_SEQUENCE_EMPTY"),
    "duplicate-event-id": ("INVALID", "DUPLICATE_EVENT_ID"),
    "parent-not-preceded": ("INVALID", "PARENT_NOT_PRECEDED"),
    "cross-lineage-parent": ("HOLD", "CROSS_LINEAGE_PARENT_REQUIRES_EXPLICIT_EVENT"),
    "valid-event-sequence": ("ADMITTED_FOR_REVIEW", "EVENT_SEQUENCE_REVIEW_METADATA_ONLY"),
    "valid-evidence-profile": ("ADMITTED_FOR_REVIEW", "EVIDENCE_PROFILE_REVIEW_METADATA_ONLY"),
    "evidence-role-reuse": ("HOLD", "EVIDENCE_REF_REUSED_ACROSS_ROLES"),
    "missing-counterevidence": ("HOLD", "COUNTEREVIDENCE_NOT_RECORDED"),
    "valid-comparison": ("ADMITTED_FOR_REVIEW", "COMPARISON_REVIEW_METADATA_ONLY"),
    "missing-alternatives": ("HOLD", "ALTERNATIVE_EXPLANATIONS_MISSING"),
    "valid-authority-envelope": ("ADMITTED_FOR_REVIEW", "AUTHORITY_ENVELOPE_REVIEW_METADATA_ONLY"),
    "identity-review": ("ADMITTED_FOR_REVIEW", "SHARED_ORIGIN_REVIEW_METADATA_ONLY"),
    "event-digest-review": ("ADMITTED_FOR_REVIEW", "EVENT_SEQUENCE_REVIEW_METADATA_ONLY"),
    "comparison-second-alternative": ("ADMITTED_FOR_REVIEW", "COMPARISON_REVIEW_METADATA_ONLY"),
    "evidence-empty-counterevidence": ("HOLD", "COUNTEREVIDENCE_NOT_RECORDED"),
    "event-second-lineage-origin": ("ADMITTED_FOR_REVIEW", "EVENT_SEQUENCE_REVIEW_METADATA_ONLY"),
    "authority-second-offer": ("ADMITTED_FOR_REVIEW", "AUTHORITY_ENVELOPE_REVIEW_METADATA_ONLY"),
    "comparison-more-outcomes": ("ADMITTED_FOR_REVIEW", "COMPARISON_REVIEW_METADATA_ONLY"),
    "lineage-no-inherited-artifacts": ("ADMITTED_FOR_REVIEW", "SHARED_ORIGIN_REVIEW_METADATA_ONLY"),
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
    assert data["main_effect"] == "NONE"
    assert data["canonical_effect"] == "NONE"
    assert data["runtime_effect"] == "NONE"
    assert data["governance_effect"] == "NONE"
    assert data["deployment"] is False
    actual = {record["case_id"]: record["decision"] for record in data["records"]}
    assert set(actual) == set(EXPECTED)
    for case_id, (status, reason) in EXPECTED.items():
        decision = actual[case_id]
        assert (decision["status"], decision["reason"]) == (status, reason), (case_id, decision)
        assert decision["main_effect"] == "NONE"
        assert decision["canonical_effect"] == "NONE"
        assert decision["runtime_effect"] == "NONE"
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
