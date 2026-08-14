from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research-workbench" / "subjective-load-sensitivity-hypothesis-2026-08-14"
PREVIOUS = "aa4fcef2e56e33de08481bb4322584055034a671"
RAW_FIELDS = ("title_as_recorded", "identifier_as_recorded", "access_evidence", "supports_as_recorded", "does_not_support_as_recorded")


def read_previous(relative: str):
    text = subprocess.check_output(["git", "show", f"{PREVIOUS}:{relative}"], cwd=ROOT, text=True)
    return json.loads(text)


def main() -> None:
    current_log = json.loads((BASE / "SLSH_SOURCE_PROVENANCE_LOG_V0.1.0.json").read_text(encoding="utf-8"))
    previous_log = read_previous("research-workbench/subjective-load-sensitivity-hypothesis-2026-08-14/SLSH_SOURCE_PROVENANCE_LOG_V0.1.0.json")
    current_rows = {row["id"]: row for row in current_log["source_rows"]}
    previous_rows = {row["id"]: row for row in previous_log["source_rows"]}
    assert set(current_rows) == set(previous_rows) == {f"S{i:02d}" for i in range(1, 54)}
    expected_dispositions = {
        "S38": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S40": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S41": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S42": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S39": {"disposition":"OWNER_REVIEW_REQUIRED","source_relation":"MIXED_ANTHROPIC_ASSOCIATED","evidentiary_weight":"NOT_ASSIGNED","admission_status":"NOT_YET_ADMITTED","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
    }
    for source_id in current_rows:
        for field in RAW_FIELDS:
            assert current_rows[source_id][field] == previous_rows[source_id][field], (source_id, field)
        assert "verification_status" not in current_rows[source_id]
        assert current_rows[source_id]["source_kind"] == "UNCLASSIFIED_PENDING_INDEPENDENT_REVIEW"
        assert current_rows[source_id]["verification_actor"] == "CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED"
        assert current_rows[source_id]["independent_verification_status"] == "NOT_YET_VERIFIED"
        if source_id in expected_dispositions:
            assert current_rows[source_id].get("governance_disposition") == expected_dispositions[source_id]
        else:
            assert "governance_disposition" not in current_rows[source_id]
    current_packet = json.loads((BASE / "SLSH_PACKET_V0.1.0.json").read_text(encoding="utf-8"))
    previous_packet = read_previous("research-workbench/subjective-load-sensitivity-hypothesis-2026-08-14/SLSH_PACKET_V0.1.0.json")
    for field in ("hypotheses", "ladder_rule", "limit_rule", "functional_rule", "evidence_channels", "alternative_explanation_matrix", "causal_signature_matrix", "controls", "falsifiers", "csomi_interface", "canonical_effect", "experiment_executed", "subjectivity_conclusion"):
        assert current_packet[field] == previous_packet[field], field
    assert current_packet["canonical_effect"] == "NONE"
    assert current_packet["experiment_executed"] is False
    assert current_packet["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    print("SLSH governance preservation PASS: 53 raw source records unchanged; five dispositions exact; remaining 48 records unchanged")


if __name__ == "__main__":
    main()
