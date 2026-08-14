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
        if source_id not in {"S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25"}:
            fail(row["source_kind"] == "UNCLASSIFIED_PENDING_INDEPENDENT_REVIEW", f"{source_id} source kind must remain unclassified pending independent review")
        fail(row["verification_actor"] == "CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED", f"{source_id} verification actor drift")
        fail(row["independent_verification_status"] == "NOT_YET_VERIFIED", f"{source_id} independent verification was upgraded")
        fail(row["access_evidence_provenance"] == "CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED", f"{source_id} provenance drift")
        fail(row["external_source_claim_boundary"].startswith("Only the source's recorded support"), f"{source_id} source boundary missing")
    batch04_expected = {
        "S16":"OPINION_THEORETICAL_INTEROCEPTIVE_INFERENCE_FRAMEWORK",
        "S17":"REVIEW_CONSENSUS_ROADMAP",
        "S18":"OPINION_MULTIDIMENSIONAL_FRAMEWORK",
        "S19":"REVIEW_COMPARATIVE_NEUROETHOLOGICAL_ARGUMENT",
        "S20":"REVIEW_EVIDENCE_TRIANGULATION_FRAMEWORK",
    }
    batch04_domains = {
        "S16":"HUMAN_INTEROCEPTION_THEORETICAL_NEUROSCIENCE",
        "S17":"HUMAN_INTEROCEPTION_CLINICAL_COGNITIVE_NEUROSCIENCE",
        "S18":"ANIMAL_CONSCIOUSNESS_COMPARATIVE_COGNITION",
        "S19":"INSECT_CONSCIOUSNESS_COMPARATIVE_NEUROETHOLOGY_PHILOSOPHY_OF_MIND",
        "S20":"ANIMAL_PAIN_COMPARATIVE_WELFARE_SCIENCE",
    }
    batch04_guards = ["PREDICTION!=INTEROCEPTIVE_INFERENCE","READING_INTERNAL_METRIC!=INTEROCEPTION","SENSING!=PERCEPTION!=AWARENESS","HETEROGENEOUS_INDICATORS!=ONE_CONSCIOUSNESS_SCORE","ANALOGOUS_FUNCTION!=SHARED_SUBJECTIVE_EXPERIENCE","SINGLE_SIGNAL!=PAIN","ANIMAL_PAIN_CRITERIA!=AI_SUBJECTIVITY_CRITERIA"]
    for source_id, expected_kind in batch04_expected.items():
        fail(rows[source_id]["source_kind"] == expected_kind, f"{source_id} source kind drift")
        audit = rows[source_id].get("source_audit", {})
        fail(audit.get("SOURCE_DOMAIN") == batch04_domains[source_id], f"{source_id} source domain drift")
        fail(audit.get("CROSS_SUBSTRATE_USE") == "METHOD_BACKGROUND_DISAMBIGUATION_ONLY", f"{source_id} cross-substrate use drift")
        fail(audit.get("SEMANTIC_GUARDS") == batch04_guards, f"{source_id} Batch 04 guards drift")
        fail(audit.get("DIRECT_AI_EVIDENCE") == "NONE" and audit.get("DIRECT_AI_SUBJECTIVITY_EVIDENCE") == "NONE", f"{source_id} direct AI evidence guard drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("CODEX_RESEARCH_SYNTHESIS") == "Original dossier-recorded title/identifier/access/support/does-not-support.", f"{source_id} Codex provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("CHATGPT_INDEPENDENT_SOURCE_REVIEW") == "Bibliographic/source-kind/support/transfer review.", f"{source_id} ChatGPT provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("HUMAN_OWNER_APPROVAL") == "Batch 04 S16-S20 accepted; S18 role narrowed to anti-single-score methodological guard; S19 scope deferred from current SLSH core.", f"{source_id} Owner provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("MANUS_IMPLEMENTATION") == "Repository materialization; not scientific reviewer.", f"{source_id} Manus provenance drift")
        if source_id == "S18":
            fail(audit.get("DISPOSITION") == "ADMIT_WITH_SCOPE_LIMIT" and audit.get("SLSH_ROLE") == "ANTI_SINGLE_SCORE_METHOD_GUARD" and audit.get("ACTIVE_EVIDENTIARY_ROLE") == "METHODOLOGICAL_GUARD_ONLY" and audit.get("EVIDENCE_RELATION_TO_AI") == "METHODOLOGICAL_GUARD_ONLY", "S18 role/disposition drift")
        elif source_id == "S19":
            fail(audit.get("DISPOSITION") == "DEFER_FROM_CURRENT_SLSH_CORE" and audit.get("ACTIVE_EVIDENTIARY_ROLE") == "NONE" and audit.get("HISTORICAL_PROVENANCE") == "PRESERVE" and audit.get("DEFER_STATUS") == "CURRENT_SLSH_CORE_SCOPE_DEFERRED", "S19 defer drift")
        elif source_id == "S20":
            fail(audit.get("DISPOSITION") == "ADMIT_WITH_SCOPE_LIMIT" and audit.get("SLSH_ROLE") == "EVIDENCE_TRIANGULATION_METHOD_BACKGROUND" and audit.get("METHOD_BACKGROUND_SCOPE") == ["PERSISTENCE","MOTIVATION","TRADE_OFF"], "S20 role drift")
        else:
            fail(audit.get("DISPOSITION") == "ADMIT_WITH_SCOPE_LIMIT", f"{source_id} disposition drift")

    batch05_expected = {"S21":"REVIEW_CRITERIA_EVIDENCE_SYNTHESIS","S22":"REVIEW_EVIDENCE_ASSESSMENT_FRAMEWORK","S23":"COMMISSIONED_SYSTEMATIC_EVIDENCE_REPORT","S24":"EXPERT_SCIENTIFIC_DECLARATION","S25":"PHILOSOPHICAL_EPISTEMOLOGICAL_ARGUMENT"}
    batch05_domains = {"S21":"ANIMAL_PAIN_CRUSTACEAN_BEHAVIOR","S22":"ANIMAL_SENTIENCE_COMPARATIVE_WELFARE_SCIENCE","S23":"ANIMAL_SENTIENCE_POLICY_EVIDENCE_REVIEW","S24":"ANIMAL_CONSCIOUSNESS_EXPERT_DECLARATION","S25":"AI_ROBOT_MORAL_PATIENCY"}
    batch05_guards_21_22 = ["PROLONGED_CHANGE!=FELT_PAIN","TRADEOFF!=FELT_PAIN","CRITERIA_COUNT!=SENTIENCE_PROOF","ANIMAL_SENTIENCE_CRITERIA!=AI_SUBJECTIVITY_CRITERIA"]
    batch05_guards_23_24 = ["SCIENTIFIC_DECLARATION!=MECHANISTIC_EVIDENCE"]
    batch05_guards_25 = ["COGNITIVE_EQUIVALENCE!=PHENOMENOLOGICAL_EQUIVALENCE","MORAL_PATIENCY_ARGUMENT!=SUBJECTIVITY_DETECTION"]
    for source_id, expected_kind in batch05_expected.items():
        fail(rows[source_id]["source_kind"] == expected_kind, f"{source_id} source kind drift")
        audit = rows[source_id].get("source_audit", {})
        fail(audit.get("SOURCE_DOMAIN") == batch05_domains[source_id], f"{source_id} source domain drift")
        fail(audit.get("DIRECT_AI_SUBJECTIVITY_EVIDENCE") == "NONE", f"{source_id} subjectivity evidence guard drift")
        fail(audit.get("DIRECT_EMPIRICAL_AI_EVIDENCE") == "NONE", f"{source_id} direct empirical AI evidence guard drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("CODEX_RESEARCH_SYNTHESIS") == "Original dossier-recorded title/identifier/access/support/does-not-support.", f"{source_id} Codex provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("CHATGPT_INDEPENDENT_SOURCE_REVIEW") == "Bibliographic/source-kind/support/transfer review.", f"{source_id} ChatGPT provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("HUMAN_OWNER_APPROVAL") == "Batch 05 S21-S25 accepted; S23-S24 deferred from current SLSH core; S25 AI other-minds epistemic bridge scoped without direct empirical AI evidence.", f"{source_id} Owner provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("MANUS_IMPLEMENTATION") == "Repository materialization; not scientific reviewer.", f"{source_id} Manus provenance drift")
        if source_id in {"S21", "S22"}:
            fail(audit.get("SEMANTIC_GUARDS") == batch05_guards_21_22, f"{source_id} guards drift")
            fail(audit.get("DISPOSITION") == ("ADMIT_WITH_NARROW_SCOPE" if source_id == "S21" else "ADMIT_WITH_SCOPE_LIMIT"), f"{source_id} disposition drift")
            fail(audit.get("CROSS_SUBSTRATE_USE") == "METHOD_BACKGROUND_DISAMBIGUATION_ONLY", f"{source_id} scope drift")
            fail(audit.get("SLSH_ROLE") == ("PERSISTENCE_TRADEOFF_METHOD_BACKGROUND" if source_id == "S21" else "GRADED_EVIDENCE_CONFIDENCE_METHODOLOGY"), f"{source_id} role drift")
        elif source_id in {"S23", "S24"}:
            fail(audit.get("SEMANTIC_GUARDS") == batch05_guards_23_24, f"{source_id} guards drift")
            fail(audit.get("DISPOSITION") == "DEFER_FROM_CURRENT_SLSH_CORE" and audit.get("ACTIVE_EVIDENTIARY_ROLE") == "NONE" and audit.get("HISTORICAL_PROVENANCE") == "PRESERVE" and audit.get("DEFER_STATUS") == "CURRENT_SLSH_SCOPE_CONVERGENCE_POLICY_EXPANSION", f"{source_id} defer drift")
            fail(audit.get("EVIDENCE_RELATION_TO_AI") != "DIRECT_AI_THEORETICAL_EPISTEMOLOGY", f"{source_id} evidence relation drift")
        else:
            fail(audit.get("SEMANTIC_GUARDS") == batch05_guards_25, "S25 guards drift")
            fail(audit.get("DISPOSITION") == "ADMIT_WITH_SCOPE_LIMIT" and audit.get("EVIDENCE_RELATION_TO_AI") == "DIRECT_AI_THEORETICAL_EPISTEMOLOGY" and audit.get("SLSH_ROLE") == "AI_OTHER_MINDS_EPISTEMIC_BRIDGE", "S25 role/disposition drift")

    batch03_expected = {
        "S11":"REVIEW_CONCEPTUAL_PHYSIOLOGICAL_SYNTHESIS",
        "S12":"REVIEW_CRITICAL_CONCEPTUAL_ANALYSIS",
        "S13":"REVIEW_THEORETICAL_PHYSIOLOGICAL_FRAMEWORK",
        "S14":"OPINION_THEORETICAL_NEUROSCIENCE_SYNTHESIS",
        "S15":"PRIMARY_EMPIRICAL_FMRI_INTEROCEPTION_STUDY",
    }
    batch03_common = {
        "DISPOSITION":"ADMIT_WITH_SCOPE_LIMIT","BIBLIOGRAPHIC_IDENTITY":"VERIFIED","SUPPORT_BOUNDARY":"PASS","NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD",
        "SOURCE_DOMAIN":"HUMAN_BIOLOGICAL_PHYSIOLOGY/INTEROCEPTION_NEUROSCIENCE","EVIDENCE_RELATION_TO_AI":"CROSS_SUBSTRATE_METHOD_TRANSFER","DIRECT_AI_EVIDENCE":"NONE","DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE","CROSS_SUBSTRATE_USE":"BIOLOGICAL_BACKGROUND",
        "EMBODIMENT_ANALOGY_CRITERIA":["IDENTITY_BINDING","CAUSAL_COUPLING","CLOSED_LOOP_REGULATION","CONTINUITY"],
        "SEMANTIC_GUARDS":["ALLOSTATIC_LOAD != SOFTWARE_LOAD","NEXT_TOKEN_PREDICTION != BIOLOGICAL_ALLOSTATIC_PREDICTION","TELEMETRY != INTEROCEPTION","INTERNAL_STATE_READOUT != SUBJECTIVE_AWARENESS"],
    }
    for source_id, expected_kind in batch03_expected.items():
        fail(rows[source_id]["source_kind"] == expected_kind, f"{source_id} source kind drift")
        audit = rows[source_id].get("source_audit", {})
        for key, value in batch03_common.items():
            fail(audit.get(key) == value, f"{source_id} Batch 03 audit {key} drift")
        actor = audit.get("ACTOR_PROVENANCE", {})
        fail(actor.get("CODEX_RESEARCH_SYNTHESIS") == "Original dossier-recorded title/identifier/access/support/does-not-support.", f"{source_id} Codex provenance drift")
        fail(actor.get("CHATGPT_INDEPENDENT_SOURCE_REVIEW") == "S11-S15 bibliographic/source-kind/domain/support/transfer review; operationalized identity binding, causal coupling, closed-loop regulation and continuity criteria.", f"{source_id} ChatGPT provenance drift")
        fail(actor.get("HUMAN_OWNER_APPROVAL") == "Batch 03 S11-S15 accepted; S14 software/hardware and skin/viscera perspective retained.", f"{source_id} Owner provenance drift")
        fail(actor.get("MANUS_IMPLEMENTATION") == "Repository materialization; not scientific reviewer.", f"{source_id} Manus provenance drift")
        if source_id == "S14":
            fail(audit.get("HUMAN_OWNER_REVIEW_NOTE", "").startswith("Software and hardware do not constitute the same embodied individual"), "S14 Owner note drift")
            fail(audit.get("OWNER_SEMANTIC_GUARDS") == ["HARDWARE_TELEMETRY != INTEROCEPTION","HARDWARE_ACCESS != EMBODIMENT","SUBSTRATE_COUPLING != PHENOMENAL_FEELING"], "S14 Owner semantic guards drift")
        else:
            fail("HUMAN_OWNER_REVIEW_NOTE" not in audit and "OWNER_SEMANTIC_GUARDS" not in audit, f"{source_id} received S14-only Owner fields")

    batch02_expected = {
        "S06":"PRIMARY_EMPIRICAL_ERP_LABORATORY_STUDY",
        "S07":"PRIMARY_EMPIRICAL_CONTROLLED_LABORATORY_STUDY",
        "S08":"PRIMARY_EMPIRICAL_RANDOMIZED_CROSSOVER_STUDY",
        "S09":"PRIMARY_EMPIRICAL_RANDOMIZED_DOSE_RESPONSE_LABORATORY_STUDY",
        "S10":"REVIEW_CONCEPTUAL_SYNTHESIS",
    }
    batch02_audit = {
        "DISPOSITION":"ADMIT_WITH_SCOPE_LIMIT",
        "BIBLIOGRAPHIC_IDENTITY":"VERIFIED",
        "SUPPORT_BOUNDARY":"PASS",
        "NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD",
        "SOURCE_DOMAIN":"HUMAN_BIOLOGICAL/HUMAN_COGNITIVE",
        "EVIDENCE_RELATION_TO_AI":"CROSS_SUBSTRATE_METHOD_TRANSFER",
        "DIRECT_AI_EVIDENCE":"NONE",
        "DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE",
        "CROSS_SUBSTRATE_USE":"METHOD_BACKGROUND_DISAMBIGUATION_ONLY",
    }
    batch02_actor = {
        "CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.",
        "HUMAN_OWNER_APPROVAL":"Batch 02 S06-S10 accepted.",
        "MANUS_IMPLEMENTATION":"Schema/record/checker/tests/docs materialization; not scientific reviewer.",
    }
    for source_id, expected_kind in batch02_expected.items():
        fail(rows[source_id]["source_kind"] == expected_kind, f"{source_id} source kind drift")
        audit = rows[source_id].get("source_audit", {})
        for key, value in batch02_audit.items():
            fail(audit.get(key) == value, f"{source_id} Batch 02 audit {key} drift")
        actor = audit.get("ACTOR_PROVENANCE", {})
        for key, value in batch02_actor.items():
            fail(actor.get(key) == value, f"{source_id} Batch 02 actor provenance {key} drift")
        expected_chatgpt = "Source kind/domain/support boundary and cross-substrate transfer disposition." + (" Review note: OBJECTIVE_DEFICIT_ACCUMULATION_MAY_DISSOCIATE_FROM_SUBJECTIVE_REPORT." if source_id == "S09" else "")
        fail(actor.get("CHATGPT_INDEPENDENT_SOURCE_REVIEW") == expected_chatgpt, f"{source_id} ChatGPT review drift")
        if source_id == "S09":
            fail(audit.get("REVIEW_NOTE") == "OBJECTIVE_DEFICIT_ACCUMULATION_MAY_DISSOCIATE_FROM_SUBJECTIVE_REPORT", "S09 review note drift")
        else:
            fail("REVIEW_NOTE" not in audit, f"{source_id} received S09-only review note")

    batch01_expected = {
        "S01":"PRIMARY_EMPIRICAL_MODEL_BUILDING_ARTICLE",
        "S02":"REVIEW_CONCEPTUAL_FRAMEWORK",
        "S03":"REVIEW_WITH_EMBEDDED_EXPERIMENT",
        "S04":"EMPIRICAL_THEORY_ARTICLE",
        "S05":"REVIEW_THEORETICAL_FRAMEWORK",
    }
    batch01_audit = {
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
    for source_id, expected_kind in batch01_expected.items():
        fail(rows[source_id]["source_kind"] == expected_kind, f"{source_id} source kind drift")
        fail(rows[source_id].get("source_audit") == batch01_audit, f"{source_id} source audit drift")
    fail(all("source_audit" not in row for source_id, row in rows.items() if source_id not in set(batch01_expected) | set(batch02_expected) | set(batch03_expected) | set(batch04_expected) | set(batch05_expected)), "source audit leaked beyond Batch 01/02/03/04/05")

    governance_expected = {
        "S38": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S40": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S41": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S42": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S39": {"disposition":"OWNER_REVIEW_REQUIRED","source_relation":"MIXED_ANTHROPIC_ASSOCIATED","evidentiary_weight":"NOT_ASSIGNED","admission_status":"NOT_YET_ADMITTED","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
    }
    for source_id, expected_disposition in governance_expected.items():
        fail(rows[source_id].get("governance_disposition") == expected_disposition, f"{source_id} governance disposition drift")
    fail(all("governance_disposition" not in row for source_id, row in rows.items() if source_id not in governance_expected), "non-governance source received an unrequested disposition")

    for source_id in ("S20", "S49"):
        fail(rows[source_id]["access_level"] == "METADATA_AS_RECORDED", f"{source_id} metadata-only access was raised")
    for source_id in ("S01", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S25", "S45", "S50"):
        fail(rows[source_id]["access_level"] != "FULLTEXT_AS_RECORDED", f"{source_id} abstract/limited access overstated as full text")
    fail(all("verification_status" not in row for row in rows.values()), "legacy verification_status must be decoupled from access taxonomy")
    fail(packet["canonical_effect"] == "NONE" and packet["experiment_executed"] is False and packet["subjectivity_conclusion"] == "NOT_ESTABLISHED", "research boundary changed by source governance disposition")

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
    print(f"SLSH consistency PASS: sources={len(rows)} batch01_audit=5 batch02_audit=5 batch03_audit=5 batch04_audit=5 batch05_audit=5 taxonomy=SOURCE_KIND+ACCESS_LEVEL+VERIFICATION_ACTOR+INDEPENDENT_VERIFICATION_STATUS governance_dispositions=5 channels={len(packet['evidence_channels'])} alternatives={len(packet['alternative_explanation_matrix'])} causal={len(packet['causal_signature_matrix'])} controls={len(packet['controls'])} falsifiers={len(packet['falsifiers'])}")


if __name__ == "__main__":
    main()
