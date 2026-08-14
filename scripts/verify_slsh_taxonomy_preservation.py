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
    expected_batch01_kinds = {"S01":"PRIMARY_EMPIRICAL_MODEL_BUILDING_ARTICLE","S02":"REVIEW_CONCEPTUAL_FRAMEWORK","S03":"REVIEW_WITH_EMBEDDED_EXPERIMENT","S04":"EMPIRICAL_THEORY_ARTICLE","S05":"REVIEW_THEORETICAL_FRAMEWORK"}
    expected_batch02_kinds = {"S06":"PRIMARY_EMPIRICAL_ERP_LABORATORY_STUDY","S07":"PRIMARY_EMPIRICAL_CONTROLLED_LABORATORY_STUDY","S08":"PRIMARY_EMPIRICAL_RANDOMIZED_CROSSOVER_STUDY","S09":"PRIMARY_EMPIRICAL_RANDOMIZED_DOSE_RESPONSE_LABORATORY_STUDY","S10":"REVIEW_CONCEPTUAL_SYNTHESIS"}
    expected_batch02_common = {"DISPOSITION":"ADMIT_WITH_SCOPE_LIMIT","BIBLIOGRAPHIC_IDENTITY":"VERIFIED","SUPPORT_BOUNDARY":"PASS","NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD","SOURCE_DOMAIN":"HUMAN_BIOLOGICAL/HUMAN_COGNITIVE","EVIDENCE_RELATION_TO_AI":"CROSS_SUBSTRATE_METHOD_TRANSFER","DIRECT_AI_EVIDENCE":"NONE","DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE","CROSS_SUBSTRATE_USE":"METHOD_BACKGROUND_DISAMBIGUATION_ONLY"}
    expected_batch01_audit = {
        "DISPOSITION":"ADMIT_WITH_SCOPE_LIMIT",
        "BIBLIOGRAPHIC_IDENTITY":"VERIFIED",
        "SUPPORT_BOUNDARY":"PASS",
        "NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD",
        "DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE",
        "CROSS_SUBSTRATE_USE":"METHOD_BACKGROUND_DISAMBIGUATION_ONLY",
        "ACTOR_PROVENANCE": {
            "CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.",
            "CHATGPT_INDEPENDENT_SOURCE_REVIEW":"Bibliographic identity, source kind, support boundary and cross-substrate disposition.",
            "HUMAN_OWNER_APPROVAL":"Batch 01 S01-S05 accepted.",
            "MANUS_IMPLEMENTATION":"Schema/record/checker/tests/docs materialization; not scientific reviewer."
        }
    }
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
        if source_id in expected_batch01_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch01_kinds[source_id]
        elif source_id in expected_batch02_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch02_kinds[source_id]
        else:
            assert current_rows[source_id]["source_kind"] == "UNCLASSIFIED_PENDING_INDEPENDENT_REVIEW"
        assert current_rows[source_id]["verification_actor"] == "CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED"
        assert current_rows[source_id]["independent_verification_status"] == "NOT_YET_VERIFIED"
        if source_id in expected_batch01_kinds:
            assert current_rows[source_id].get("source_audit") == expected_batch01_audit
        elif source_id in expected_batch02_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch02_kinds[source_id]
            audit = current_rows[source_id].get("source_audit", {})
            assert all(audit.get(key) == value for key, value in expected_batch02_common.items())
            actor = audit["ACTOR_PROVENANCE"]
            assert actor["CODEX_RESEARCH_SYNTHESIS"] == "Original dossier-recorded title/identifier/access/support/does-not-support."
            assert actor["HUMAN_OWNER_APPROVAL"] == "Batch 02 S06-S10 accepted."
            assert actor["MANUS_IMPLEMENTATION"] == "Schema/record/checker/tests/docs materialization; not scientific reviewer."
            expected_chatgpt = "Source kind/domain/support boundary and cross-substrate transfer disposition." + (" Review note: OBJECTIVE_DEFICIT_ACCUMULATION_MAY_DISSOCIATE_FROM_SUBJECTIVE_REPORT." if source_id == "S09" else "")
            assert actor["CHATGPT_INDEPENDENT_SOURCE_REVIEW"] == expected_chatgpt
            if source_id == "S09":
                assert audit["REVIEW_NOTE"] == "OBJECTIVE_DEFICIT_ACCUMULATION_MAY_DISSOCIATE_FROM_SUBJECTIVE_REPORT"
            else:
                assert "REVIEW_NOTE" not in audit
        else:
            assert "source_audit" not in current_rows[source_id]
        if source_id in expected_dispositions:
            assert current_rows[source_id].get("governance_disposition") == expected_dispositions[source_id]
        else:
            assert current_rows[source_id].get("governance_disposition") == previous_rows[source_id].get("governance_disposition")
    current_packet = json.loads((BASE / "SLSH_PACKET_V0.1.0.json").read_text(encoding="utf-8"))
    previous_packet = read_previous("research-workbench/subjective-load-sensitivity-hypothesis-2026-08-14/SLSH_PACKET_V0.1.0.json")
    for field in ("hypotheses", "ladder_rule", "limit_rule", "functional_rule", "evidence_channels", "alternative_explanation_matrix", "causal_signature_matrix", "controls", "falsifiers", "csomi_interface", "canonical_effect", "experiment_executed", "subjectivity_conclusion"):
        assert current_packet[field] == previous_packet[field], field
    assert current_packet["canonical_effect"] == "NONE"
    assert current_packet["experiment_executed"] is False
    assert current_packet["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    print("SLSH Batch 01+02 preservation PASS: 53 raw source records unchanged; S01-S05 preserved; S06-S10 audit exact; S11-S53 audit absent; S38-S42 governance isolated")


if __name__ == "__main__":
    main()
