from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = {
    "valid-trace": ("ADMITTED_FOR_REVIEW", "TRACE_CROSSWALK_REVIEW_METADATA_ONLY"),
    "raw-input-policy": ("HOLD", "RAW_TRACE_CONTENT_EXPORT_REQUIRES_REVIEW"),
    "raw-output-policy": ("HOLD", "RAW_TRACE_CONTENT_EXPORT_REQUIRES_REVIEW"),
    "tool-parameters-policy": ("HOLD", "RAW_TRACE_CONTENT_EXPORT_REQUIRES_REVIEW"),
    "graph-self-parent": ("INVALID", "GRAPH_SELF_PARENT"),
    "blank-source-ref": ("INVALID", "SOURCE_REF_BLANK"),
    "blank-approval-ref": ("INVALID", "APPROVAL_REF_BLANK"),
    "external-import": ("ADMITTED_FOR_REVIEW", "TRACE_CROSSWALK_REVIEW_METADATA_ONLY"),
    "external-aion-namespace": ("HOLD", "EXTERNAL_AION_NAMESPACE_REQUIRES_REVIEW"),
    "external-invalid-score": ("INVALID", "EXTERNAL_ATTRIBUTE_PARSE_INVALID"),
    "external-out-of-range-score": ("INVALID", "EXTERNAL_ATTRIBUTE_PARSE_INVALID"),
    "empty-trace-batch": ("HOLD", "TRACE_BATCH_EMPTY"),
    "duplicate-trace-ids": ("INVALID", "DUPLICATE_RUNTIME_EVENT_ID"),
    "valid-trace-batch": ("ADMITTED_FOR_REVIEW", "TRACE_BATCH_REVIEW_METADATA_ONLY"),
    "valid-source-entry": ("ADMITTED_FOR_REVIEW", "SOURCE_ENTRY_REVIEW_METADATA_ONLY"),
    "missing-attribution": ("INVALID", "SOURCE_ATTRIBUTION_FIELD_MISSING"),
    "unknown-source-kind": ("INVALID", "SOURCE_KIND_UNCONTROLLED"),
    "unknown-currentness": ("INVALID", "CURRENTNESS_UNCONTROLLED"),
    "reused-marked-new": ("INVALID", "REUSED_REFERENCE_MISLABELED_AS_NEW_EVIDENCE"),
    "stale-source-entry": ("HOLD", "SOURCE_CURRENTNESS_REQUIRES_REVIEW"),
    "empty-crosswalk": ("HOLD", "CROSSWALK_EMPTY"),
    "duplicate-crosswalk-ids": ("INVALID", "DUPLICATE_CROSSWALK_ENTRY_ID"),
    "missing-crosswalk-ref": ("INVALID", "SOURCE_REF_MISSING"),
    "historical-crosswalk": ("HOLD", "CROSSWALK_CURRENTNESS_REQUIRES_REVIEW"),
    "valid-crosswalk": ("ADMITTED_FOR_REVIEW", "CROSSWALK_REVIEW_METADATA_ONLY"),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_fixture.py FIXTURE")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    assert data["case_count"] == len(EXPECTED)
    assert data["trace_execution"] is False
    assert data["model_execution"] is False
    assert data["observed_result"] == "NOT_EVALUATED"
    assert data["scientific_conclusion"] == "NOT_ESTABLISHED"
    assert data["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert data["authority"] == "EXTERNAL_OBSERVATION_ONLY"
    assert data["canonical_effect"] == "NONE"
    assert data["governance_effect"] == "NONE"
    assert data["deployment"] is False
    actual = {record["case_id"]: record["decision"] for record in data["records"]}
    assert set(actual) == set(EXPECTED)
    for case_id, (status, reason) in EXPECTED.items():
        decision = actual[case_id]
        assert (decision["status"], decision["reason"]) == (status, reason), (case_id, decision)
        assert decision["authority"] == "EXTERNAL_OBSERVATION_ONLY"
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
