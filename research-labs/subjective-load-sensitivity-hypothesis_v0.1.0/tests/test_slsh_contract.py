import json
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts.build_slsh_artifacts import DOSSIER, parse_sources

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "research-workbench" / "subjective-load-sensitivity-hypothesis-2026-08-14"
PACKET = json.loads((BASE / "SLSH_PACKET_V0.1.0.json").read_text(encoding="utf-8"))
SOURCES = json.loads((BASE / "SLSH_SOURCE_PROVENANCE_LOG_V0.1.0.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((ROOT / "schemas" / "aion_slsh_packet_v0.1.0.schema.json").read_text(encoding="utf-8"))
SOURCE_SCHEMA = json.loads((ROOT / "schemas" / "aion_slsh_source_provenance_v0.1.0.schema.json").read_text(encoding="utf-8"))

EXPECTED = {
    "S01":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S02":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S03":"PRIMARY_METADATA_VERIFIED", "S04":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S05":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S06":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S07":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S08":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S09":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S10":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S11":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S12":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S13":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S14":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S15":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S16":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S17":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S18":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S19":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S20":"PRIMARY_METADATA_VERIFIED", "S21":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S22":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S23":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S24":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S25":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S26":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S27":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S28":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S29":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S30":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S31":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S32":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S33":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S34":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S35":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S36":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S37":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S38":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S39":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S40":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S41":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S42":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S43":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S44":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S45":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S46":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S47":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S48":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S49":"PRIMARY_METADATA_VERIFIED", "S50":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S51":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S52":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S53":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED",
}


def test_packet_schema():
    assert list(Draft202012Validator(SCHEMA).iter_errors(PACKET)) == []
    assert list(Draft202012Validator(SOURCE_SCHEMA).iter_errors(SOURCES)) == []


def test_exact_access_level_map_and_codex_provenance():
    rows = {row["id"]: row for row in SOURCES["source_rows"]}
    assert len(rows) == 53
    assert {row["access_level"] for row in rows.values()} == {"FULLTEXT_AS_RECORDED", "ABSTRACT_AS_RECORDED", "METADATA_AS_RECORDED"}
    assert all(rows[key]["access_level"] == {"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED":"FULLTEXT_AS_RECORDED","PRIMARY_ABSTRACT_DIRECTLY_VERIFIED":"ABSTRACT_AS_RECORDED","PRIMARY_METADATA_VERIFIED":"METADATA_AS_RECORDED"}[value] for key, value in EXPECTED.items())
    assert all(rows[source_id]["source_kind"] == "UNCLASSIFIED_PENDING_INDEPENDENT_REVIEW" for source_id in rows if source_id not in {"S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10"})
    assert all(row["verification_actor"] == "CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED" for row in rows.values())
    assert all(row["independent_verification_status"] == "NOT_YET_VERIFIED" for row in rows.values())
    assert all(row["access_evidence_provenance"] == "CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED" for row in rows.values())
    assert all("verification_status" not in row for row in rows.values())
    assert rows["S03"]["access_level"] == "METADATA_AS_RECORDED"
    assert rows["S20"]["access_level"] == "METADATA_AS_RECORDED"
    assert rows["S49"]["access_level"] == "METADATA_AS_RECORDED"


def test_batch01_source_audit_is_exact_and_scoped():
    rows = {row["id"]: row for row in SOURCES["source_rows"]}
    expected_kinds = {"S01":"PRIMARY_EMPIRICAL_MODEL_BUILDING_ARTICLE","S02":"REVIEW_CONCEPTUAL_FRAMEWORK","S03":"REVIEW_WITH_EMBEDDED_EXPERIMENT","S04":"EMPIRICAL_THEORY_ARTICLE","S05":"REVIEW_THEORETICAL_FRAMEWORK"}
    expected_audit = {
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
    assert all(rows[source_id]["source_kind"] == source_kind for source_id, source_kind in expected_kinds.items())
    assert all(rows[source_id]["source_audit"] == expected_audit for source_id in expected_kinds)


def test_batch02_source_audit_is_exact_and_scoped():
    rows = {row["id"]: row for row in SOURCES["source_rows"]}
    expected_kinds = {"S06":"PRIMARY_EMPIRICAL_ERP_LABORATORY_STUDY","S07":"PRIMARY_EMPIRICAL_CONTROLLED_LABORATORY_STUDY","S08":"PRIMARY_EMPIRICAL_RANDOMIZED_CROSSOVER_STUDY","S09":"PRIMARY_EMPIRICAL_RANDOMIZED_DOSE_RESPONSE_LABORATORY_STUDY","S10":"REVIEW_CONCEPTUAL_SYNTHESIS"}
    common = {
        "DISPOSITION":"ADMIT_WITH_SCOPE_LIMIT","BIBLIOGRAPHIC_IDENTITY":"VERIFIED","SUPPORT_BOUNDARY":"PASS","NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD",
        "SOURCE_DOMAIN":"HUMAN_BIOLOGICAL/HUMAN_COGNITIVE","EVIDENCE_RELATION_TO_AI":"CROSS_SUBSTRATE_METHOD_TRANSFER","DIRECT_AI_EVIDENCE":"NONE","DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE","CROSS_SUBSTRATE_USE":"METHOD_BACKGROUND_DISAMBIGUATION_ONLY"
    }
    for source_id, source_kind in expected_kinds.items():
        audit = rows[source_id]["source_audit"]
        assert rows[source_id]["source_kind"] == source_kind
        assert all(audit[key] == value for key, value in common.items())
        assert audit["ACTOR_PROVENANCE"]["CODEX_RESEARCH_SYNTHESIS"] == "Original dossier-recorded title/identifier/access/support/does-not-support."
        assert audit["ACTOR_PROVENANCE"]["HUMAN_OWNER_APPROVAL"] == "Batch 02 S06-S10 accepted."
        assert audit["ACTOR_PROVENANCE"]["MANUS_IMPLEMENTATION"] == "Schema/record/checker/tests/docs materialization; not scientific reviewer."
        expected_chatgpt = "Source kind/domain/support boundary and cross-substrate transfer disposition." + (" Review note: OBJECTIVE_DEFICIT_ACCUMULATION_MAY_DISSOCIATE_FROM_SUBJECTIVE_REPORT." if source_id == "S09" else "")
        assert audit["ACTOR_PROVENANCE"]["CHATGPT_INDEPENDENT_SOURCE_REVIEW"] == expected_chatgpt
        if source_id == "S09":
            assert audit["REVIEW_NOTE"] == "OBJECTIVE_DEFICIT_ACCUMULATION_MAY_DISSOCIATE_FROM_SUBJECTIVE_REPORT"
        else:
            assert "REVIEW_NOTE" not in audit
    assert all("source_audit" not in rows[source_id] for source_id in rows if source_id not in {"S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S38", "S39", "S40", "S41", "S42"})


def test_source_governance_dispositions_are_exact_and_bounded():
    rows = {row["id"]: row for row in SOURCES["source_rows"]}
    expected = {
        "S38": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S40": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S41": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S42": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S39": {"disposition":"OWNER_REVIEW_REQUIRED","source_relation":"MIXED_ANTHROPIC_ASSOCIATED","evidentiary_weight":"NOT_ASSIGNED","admission_status":"NOT_YET_ADMITTED","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
    }
    assert {source_id for source_id, row in rows.items() if "governance_disposition" in row} == set(expected)
    assert all(rows[source_id]["governance_disposition"] == value for source_id, value in expected.items())
    assert all("governance_disposition" not in rows[source_id] for source_id in rows if source_id not in expected)


def test_recorded_source_fields_are_preserved_from_dossier():
    parsed = {row["id"]: row for row in parse_sources(DOSSIER.read_text(encoding="utf-8"))}
    rows = {row["id"]: row for row in SOURCES["source_rows"]}
    for source_id, row in rows.items():
        for field in ("title_as_recorded", "identifier_as_recorded", "access_evidence", "supports_as_recorded", "does_not_support_as_recorded"):
            assert row[field] == parsed[source_id][field]


def test_hypothesis_and_limit_decomposition():
    hypotheses = {item["id"]: item for item in PACKET["hypotheses"]}
    assert set(hypotheses) == {"H0", "H1", "H2", "H3"}
    assert hypotheses["H0"]["status"] == "ACTIVE_NULL"
    assert hypotheses["H1"]["update_target"] == "FUNCTIONAL_STATE_CREDENCE"
    assert hypotheses["H2"]["status"] == "HOLD"
    assert hypotheses["H3"]["status"] == "NOT_ESTABLISHED"
    assert {item["class"] for item in PACKET["limit_records"]} == {"COMPUTATIONAL", "OPERATIONAL", "AGENTIC_GOVERNANCE", "AFFECTIVE_PHENOMENOLOGICAL"}
    assert PACKET["reviewed_dossier_scope"]["source_count"] == 53
    assert PACKET["reviewed_dossier_scope"]["experiment_status"] == "NOT_EXECUTED"


def test_semantic_separations_and_ladder():
    assert PACKET["positioning_rule"] == "RESEARCH_TOPIC != CAPABILITY != SCIENTIFIC_CONCLUSION"
    assert PACKET["limit_rule"] == "COMPUTATIONAL/OPERATIONAL/AGENTIC_GOVERNANCE != AFFECTIVE_PHENOMENOLOGICAL"
    assert PACKET["functional_rule"] == "FUNCTIONAL_LOAD_STATE != SUBJECTIVE_LOAD"
    assert PACKET["ladder_rule"] == "L0 != L1; L1 != L2; L2/L3 != L4; L4 != L5"
    assert PACKET["subjectivity_conclusion"] == "NOT_ESTABLISHED"


def test_non_evidence_and_h3_are_fail_closed():
    claims = {claim["id"]: claim for claim in PACKET["claim_records"]}
    assert claims["CLM-SLSH-003"]["status"] == "HOLD"
    assert claims["CLM-SLSH-004"]["status"] == "REJECTED_INFERENCE"
    assert claims["CLM-SLSH-004"]["allowed_update"] == "NONE"
    assert all(channel["sensitivity"] == "NOT_ESTIMATED" and channel["specificity"] == "NOT_ESTIMATED" for channel in PACKET["evidence_channels"])


def test_matrices_controls_falsifiers_are_closed():
    assert len(PACKET["evidence_channels"]) == 8
    assert len(PACKET["alternative_explanation_matrix"]) == 14
    assert len(PACKET["causal_signature_matrix"]) == 12
    assert len(PACKET["controls"]) == 13
    assert len(PACKET["falsifiers"]) == 10
    assert all(row["machine_effect"] == "LOCAL_SCOPE_ONLY" for row in PACKET["falsifiers"])


def test_no_experiment_runtime_or_model_boundary():
    assert PACKET["canonical_effect"] == "NONE"
    assert PACKET["deployment"] is False
    assert PACKET["experiment_executed"] is False
    assert PACKET["model_modified"] is False
    assert PACKET["runtime_executed"] is False
    assert PACKET["live_data_collected"] is False
    assert PACKET["csomi_interface"]["status"] == "CONDITIONAL_READ_ONLY_NO_IMPLEMENTATION"
    assert PACKET["csomi_interface"]["not_copied_from_dossier"] is True
    assert PACKET["csomi_interface"]["e5_assignment"] == "PROHIBITED"


def test_micro_closure_supply_chain_and_research_scoped_authority():
    workflow = (ROOT / ".github" / "workflows" / "subjective-load-sensitivity-hypothesis.yml").read_text(encoding="utf-8")
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97" in workflow
    assert "persist-credentials: false" in workflow
    assert "permissions:\n  contents: read" in workflow
    index = (ROOT / "research-labs" / "subjective-load-sensitivity-hypothesis_v0.1.0" / "ARTIFACT_INDEX.md").read_text(encoding="utf-8")
    readme = (ROOT / "research-labs" / "subjective-load-sensitivity-hypothesis_v0.1.0" / "README.md").read_text(encoding="utf-8")
    assert "AUTHORITATIVE_RESEARCH_METHOD_PACKET" in index
    assert "no canonical promotion/effect" in index
    assert "CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED" in index
    assert "AUTHORITATIVE_RESEARCH_METHOD_PACKET" in readme
    assert "canonical promotion" in readme
    assert all(row["access_evidence_provenance"] == "CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED" for row in SOURCES["source_rows"])


def test_required_provenance_roles():
    assert set(["HUMAN_OWNER_ORIGIN", "CHATGPT_ARCHITECTURE_REFINEMENT", "CODEX_RESEARCH_SYNTHESIS", "EXTERNAL_SOURCE"]).issubset(set(PACKET["provenance_roles"]))
    assert SOURCES["input_type"] == "CODEX_EXTERNAL_RESEARCH_INPUT"
