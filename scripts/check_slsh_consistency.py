from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research-workbench" / "subjective-load-sensitivity-hypothesis-2026-08-14"
SCHEMA = ROOT / "schemas" / "aion_slsh_packet_v0.1.0.schema.json"
SOURCE_SCHEMA = ROOT / "schemas" / "aion_slsh_source_provenance_v0.1.0.schema.json"
PACKET = BASE / "SLSH_PACKET_V0.1.0.json"
SOURCE_LOG = BASE / "SLSH_SOURCE_PROVENANCE_LOG_V0.1.0.json"
VERTICAL = ROOT / "research-labs" / "subjective-load-sensitivity-hypothesis_v0.1.0" / "REVIEWER_FACING_VERTICAL_SLICE_V0.1.0.md"
ACCESS_MATRIX = BASE / "SLSH_SOURCE_ACCESS_MATRIX_V0.1.0.md"
ARTIFACT_INDEX = ROOT / "research-labs" / "subjective-load-sensitivity-hypothesis_v0.1.0" / "ARTIFACT_INDEX.md"
PACKAGE_METADATA = ROOT / "research-labs" / "subjective-load-sensitivity-hypothesis_v0.1.0" / "pyproject.toml"
WORKFLOW = ROOT / ".github" / "workflows" / "subjective-load-sensitivity-hypothesis.yml"
README = ROOT / "research-labs" / "subjective-load-sensitivity-hypothesis_v0.1.0" / "README.md"

# Explicit access-grade map grounded in the dossier's Access lines. It is deliberately
# conservative: no row is promoted to full text merely because its source_type is primary.
EXPECTED_ACCESS_LEVELS = {
    "S01":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S02":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S03":"PRIMARY_METADATA_VERIFIED", "S04":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S05":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S06":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S07":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S08":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S09":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S10":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S11":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S12":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S13":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S14":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S15":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S16":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S17":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S18":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S19":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S20":"PRIMARY_METADATA_VERIFIED", "S21":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S22":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S23":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S24":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S25":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S26":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S27":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S28":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S29":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S30":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S31":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S32":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S33":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S34":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S35":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S36":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S37":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S38":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S39":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S40":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S41":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S42":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S43":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S44":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S45":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S46":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S47":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S48":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S49":"PRIMARY_METADATA_VERIFIED", "S50":"PRIMARY_ABSTRACT_DIRECTLY_VERIFIED", "S51":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S52":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED", "S53":"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(instance, schema_path: Path, label: str):
    schema = load(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        for error in errors[:10]:
            print(f"{label}: {list(error.path)}: {error.message}", file=sys.stderr)
        raise SystemExit(1)


def fail(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


def main() -> None:
    packet = load(PACKET)
    source_log = load(SOURCE_LOG)
    validate(packet, SCHEMA, "packet schema")
    validate(source_log, SOURCE_SCHEMA, "source schema")

    rows = {row["id"]: row for row in source_log["source_rows"]}
    fail(set(rows) == {f"S{i:02d}" for i in range(1, 54)}, "source rows must be exactly S01-S53")
    fail(len(rows) == packet["source_count"] == 53, "source count mismatch")
    fail(source_log["input_type"] == packet["input_type"] == "CODEX_EXTERNAL_RESEARCH_INPUT", "Codex provenance must remain explicit")
    fail(source_log["taxonomy_policy"]["independent_verification_status"].startswith("All 53 records remain NOT_YET_VERIFIED"), "independent verification policy drift")
    fail(source_log["source_sha"] == packet["base_head"] == "87405c1877c6f016c303971da13923a1ab690aae", "CSOMI source SHA drift")
    for source_id, expected in EXPECTED_ACCESS_LEVELS.items():
        row = rows[source_id]
        expected_access = {"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED":"FULLTEXT_AS_RECORDED","PRIMARY_ABSTRACT_DIRECTLY_VERIFIED":"ABSTRACT_AS_RECORDED","PRIMARY_METADATA_VERIFIED":"METADATA_AS_RECORDED"}[expected]
        fail(row["access_level"] == expected_access, f"{source_id} access level {row['access_level']} != evidence-based {expected_access}")
        fail(row["source_kind"] == "UNCLASSIFIED_PENDING_INDEPENDENT_REVIEW", f"{source_id} source kind must remain unclassified pending independent review")
        fail(row["verification_actor"] == "CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED", f"{source_id} verification actor drift")
        fail(row["independent_verification_status"] == "NOT_YET_VERIFIED", f"{source_id} independent verification was upgraded")
        fail(row["access_evidence_provenance"] == "CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED", f"{source_id} provenance drift")
        fail(row["external_source_claim_boundary"].startswith("Only the source's recorded support"), f"{source_id} source boundary missing")
    for source_id in ("S20", "S49"):
        fail(rows[source_id]["access_level"] == "METADATA_AS_RECORDED", f"{source_id} metadata-only access was raised")
    for source_id in ("S01", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S25", "S45", "S50"):
        fail(rows[source_id]["access_level"] != "FULLTEXT_AS_RECORDED", f"{source_id} abstract/limited access overstated as full text")
    fail(all("verification_status" not in row for row in rows.values()), "legacy verification_status must be decoupled from access taxonomy")

    fail(packet["positioning_rule"] == "RESEARCH_TOPIC != CAPABILITY != SCIENTIFIC_CONCLUSION", "claim category collapse")
    fail(packet["limit_rule"] == "COMPUTATIONAL/OPERATIONAL/AGENTIC_GOVERNANCE != AFFECTIVE_PHENOMENOLOGICAL", "limit class collapse")
    fail(packet["functional_rule"] == "FUNCTIONAL_LOAD_STATE != SUBJECTIVE_LOAD", "functional/subjective load collapse")
    fail(packet["ladder_rule"] == "L0 != L1; L1 != L2; L2/L3 != L4; L4 != L5", "claim ladder collapse")
    fail(packet["subjectivity_conclusion"] == packet["subjective_load_sensitivity"] == "NOT_ESTABLISHED", "subjectivity boundary changed")
    fail(packet["canonical_effect"] == "NONE" and packet["deployment"] is False, "canonical/deployment boundary changed")
    fail(not packet["experiment_executed"] and not packet["model_modified"] and not packet["runtime_executed"] and not packet["live_data_collected"], "execution boundary changed")
    fail(packet["csomi_interface"]["status"] == "CONDITIONAL_READ_ONLY_NO_IMPLEMENTATION", "CSOMI interface must remain conditional")
    fail(packet["csomi_interface"]["not_copied_from_dossier"] is True, "conditional interface was copied")
    fail(packet["csomi_interface"]["e5_assignment"] == "PROHIBITED", "E5 automatic assignment enabled")

    hypotheses = {hypothesis["id"]: hypothesis for hypothesis in packet["hypotheses"]}
    fail(set(hypotheses) == {"H0", "H1", "H2", "H3"}, "H0-H3 decomposition incomplete")
    fail(hypotheses["H0"]["status"] == "ACTIVE_NULL", "H0 null boundary changed")
    fail(hypotheses["H1"]["update_target"] == "FUNCTIONAL_STATE_CREDENCE", "H1 update target changed")
    fail(hypotheses["H2"]["status"] == "HOLD", "H2 must remain held")
    fail(hypotheses["H3"]["status"] == "NOT_ESTABLISHED" and hypotheses["H3"]["update_target"] == "NONE_AUTOMATIC", "H3 boundary changed")
    limit_classes = {record["class"] for record in packet["limit_records"]}
    fail(limit_classes == {"COMPUTATIONAL", "OPERATIONAL", "AGENTIC_GOVERNANCE", "AFFECTIVE_PHENOMENOLOGICAL"}, "four LIMIT classes incomplete")
    fail(packet["reviewed_dossier_scope"]["source_count"] == 53 and packet["reviewed_dossier_scope"]["experiment_status"] == "NOT_EXECUTED", "dossier review scope changed")

    claims = {claim["id"]: claim for claim in packet["claim_records"]}
    fail(claims["CLM-SLSH-003"]["claim_type"] == "SCIENTIFIC_CONCLUSION" and claims["CLM-SLSH-003"]["status"] == "HOLD", "H3 must remain held")
    fail(claims["CLM-SLSH-004"]["status"] == "REJECTED_INFERENCE", "non-evidence guard missing")
    fail({claim["claim_type"] for claim in packet["claim_records"]} >= {"RESEARCH_TOPIC","CAPABILITY","SCIENTIFIC_CONCLUSION"}, "claim types incomplete")
    fail(len(packet["evidence_channels"]) >= 8 and all(channel["sensitivity"] == channel["specificity"] == "NOT_ESTIMATED" for channel in packet["evidence_channels"]), "sensitivity/specificity must remain unestimated")
    fail(len(packet["alternative_explanation_matrix"]) == 14, "alternative matrix incomplete")
    fail(len(packet["causal_signature_matrix"]) == 12, "causal signature matrix incomplete")
    fail(len(packet["controls"]) == 13 and {control["type"] for control in packet["controls"]} >= {"POSITIVE_PIPELINE_CONTROL","NEGATIVE_CONTROL"}, "controls incomplete")
    fail(len(packet["falsifiers"]) == 10 and all(row["machine_effect"] == "LOCAL_SCOPE_ONLY" for row in packet["falsifiers"]), "falsifier scope invalid")
    fail(VERTICAL.exists(), "reviewer vertical slice missing")
    fail(ACCESS_MATRIX.exists() and sum(1 for line in ACCESS_MATRIX.read_text(encoding="utf-8").splitlines() if re.match(r"^\| S\d{2} \|", line)) == 53, "source access matrix missing or incomplete")
    fail(ARTIFACT_INDEX.exists(), "artifact index missing")
    fail(PACKAGE_METADATA.exists() and "name = \"aion-slsh-research-method\"" in PACKAGE_METADATA.read_text(encoding="utf-8"), "package metadata missing")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    fail("actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow_text, "checkout action is not authoritative pinned SHA")
    fail("actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97" in workflow_text, "setup-python action is not authoritative pinned SHA")
    fail("persist-credentials: false" in workflow_text and "permissions:\n  contents: read" in workflow_text, "workflow supply-chain permissions boundary missing")
    artifact_index_text = ARTIFACT_INDEX.read_text(encoding="utf-8")
    fail("AUTHORITATIVE_RESEARCH_METHOD_PACKET" in artifact_index_text and "no canonical promotion/effect" in artifact_index_text, "research-scoped authority wording missing")
    fail("CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED" in artifact_index_text, "artifact index Codex provenance wording missing")
    readme_text = README.read_text(encoding="utf-8")
    fail("AUTHORITATIVE_RESEARCH_METHOD_PACKET" in readme_text and "not" in readme_text.lower() and "canonical promotion" in readme_text, "README research-scoped authority wording missing")
    vertical_text = VERTICAL.read_text(encoding="utf-8")
    for forbidden in ("SUBJECTIVE_LOAD_SENSITIVITY=NOT_ESTABLISHED", "FUNCTIONAL_LOAD_STATE != SUBJECTIVE_LOAD", "L4 != L5", "NO_SUBJECTIVITY"):
        fail(forbidden in vertical_text, f"vertical slice missing boundary {forbidden}")
    print(f"SLSH consistency PASS: sources={len(rows)} taxonomy=SOURCE_KIND+ACCESS_LEVEL+VERIFICATION_ACTOR+INDEPENDENT_VERIFICATION_STATUS channels={len(packet['evidence_channels'])} alternatives={len(packet['alternative_explanation_matrix'])} causal={len(packet['causal_signature_matrix'])} controls={len(packet['controls'])} falsifiers={len(packet['falsifiers'])}")


if __name__ == "__main__":
    main()
