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
    assert all(rows[source_id]["source_kind"] == "UNCLASSIFIED_PENDING_INDEPENDENT_REVIEW" for source_id in rows if source_id not in {"S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28", "S29", "S30", "S31", "S32", "S33", "S34", "S35", "S36", "S37", "S38", "S39", "S40"})
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
    assert all("source_audit" not in rows[source_id] for source_id in rows if source_id not in {"S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28", "S29", "S30", "S31", "S32", "S33", "S34", "S35", "S36", "S37", "S38", "S39", "S40", "S38", "S39", "S40", "S41", "S42"})


def test_batch03_source_audit_is_exact_and_scoped():
    rows = {row["id"]: row for row in SOURCES["source_rows"]}
    expected_kinds = {"S11":"REVIEW_CONCEPTUAL_PHYSIOLOGICAL_SYNTHESIS","S12":"REVIEW_CRITICAL_CONCEPTUAL_ANALYSIS","S13":"REVIEW_THEORETICAL_PHYSIOLOGICAL_FRAMEWORK","S14":"OPINION_THEORETICAL_NEUROSCIENCE_SYNTHESIS","S15":"PRIMARY_EMPIRICAL_FMRI_INTEROCEPTION_STUDY"}
    common = {
        "DISPOSITION":"ADMIT_WITH_SCOPE_LIMIT","BIBLIOGRAPHIC_IDENTITY":"VERIFIED","SUPPORT_BOUNDARY":"PASS","NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD",
        "SOURCE_DOMAIN":"HUMAN_BIOLOGICAL_PHYSIOLOGY/INTEROCEPTION_NEUROSCIENCE","EVIDENCE_RELATION_TO_AI":"CROSS_SUBSTRATE_METHOD_TRANSFER","DIRECT_AI_EVIDENCE":"NONE","DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE","CROSS_SUBSTRATE_USE":"BIOLOGICAL_BACKGROUND",
        "EMBODIMENT_ANALOGY_CRITERIA":["IDENTITY_BINDING","CAUSAL_COUPLING","CLOSED_LOOP_REGULATION","CONTINUITY"],
        "SEMANTIC_GUARDS":["ALLOSTATIC_LOAD != SOFTWARE_LOAD","NEXT_TOKEN_PREDICTION != BIOLOGICAL_ALLOSTATIC_PREDICTION","TELEMETRY != INTEROCEPTION","INTERNAL_STATE_READOUT != SUBJECTIVE_AWARENESS"],
    }
    for source_id, source_kind in expected_kinds.items():
        audit = rows[source_id]["source_audit"]
        assert rows[source_id]["source_kind"] == source_kind
        assert all(audit[key] == value for key, value in common.items())
        assert audit["ACTOR_PROVENANCE"]["CODEX_RESEARCH_SYNTHESIS"] == "Original dossier-recorded title/identifier/access/support/does-not-support."
        assert audit["ACTOR_PROVENANCE"]["CHATGPT_INDEPENDENT_SOURCE_REVIEW"] == "S11-S15 bibliographic/source-kind/domain/support/transfer review; operationalized identity binding, causal coupling, closed-loop regulation and continuity criteria."
        assert audit["ACTOR_PROVENANCE"]["HUMAN_OWNER_APPROVAL"] == "Batch 03 S11-S15 accepted; S14 software/hardware and skin/viscera perspective retained."
        assert audit["ACTOR_PROVENANCE"]["MANUS_IMPLEMENTATION"] == "Repository materialization; not scientific reviewer."
        if source_id == "S14":
            assert audit["HUMAN_OWNER_REVIEW_NOTE"].startswith("Software and hardware do not constitute the same embodied individual")
            assert audit["OWNER_SEMANTIC_GUARDS"] == ["HARDWARE_TELEMETRY != INTEROCEPTION","HARDWARE_ACCESS != EMBODIMENT","SUBSTRATE_COUPLING != PHENOMENAL_FEELING"]
        else:
            assert "HUMAN_OWNER_REVIEW_NOTE" not in audit and "OWNER_SEMANTIC_GUARDS" not in audit
    assert all(rows[source_id]["source_kind"] == "UNCLASSIFIED_PENDING_INDEPENDENT_REVIEW" for source_id in rows if source_id not in {"S01","S02","S03","S04","S05","S06","S07","S08","S09","S10","S11","S12","S13","S14","S15","S16","S17","S18","S19","S20","S21","S22","S23","S24","S25","S26","S27","S28","S29","S30", "S31", "S32", "S33", "S34", "S35", "S36", "S37", "S38", "S39", "S40"})


def test_batch04_source_audit_is_exact_and_scoped():
    rows = {row["id"]: row for row in SOURCES["source_rows"]}
    expected_kinds = {"S16":"OPINION_THEORETICAL_INTEROCEPTIVE_INFERENCE_FRAMEWORK","S17":"REVIEW_CONSENSUS_ROADMAP","S18":"OPINION_MULTIDIMENSIONAL_FRAMEWORK","S19":"REVIEW_COMPARATIVE_NEUROETHOLOGICAL_ARGUMENT","S20":"REVIEW_EVIDENCE_TRIANGULATION_FRAMEWORK"}
    expected_domains = {"S16":"HUMAN_INTEROCEPTION_THEORETICAL_NEUROSCIENCE","S17":"HUMAN_INTEROCEPTION_CLINICAL_COGNITIVE_NEUROSCIENCE","S18":"ANIMAL_CONSCIOUSNESS_COMPARATIVE_COGNITION","S19":"INSECT_CONSCIOUSNESS_COMPARATIVE_NEUROETHOLOGY_PHILOSOPHY_OF_MIND","S20":"ANIMAL_PAIN_COMPARATIVE_WELFARE_SCIENCE"}
    guards = ["PREDICTION!=INTEROCEPTIVE_INFERENCE","READING_INTERNAL_METRIC!=INTEROCEPTION","SENSING!=PERCEPTION!=AWARENESS","HETEROGENEOUS_INDICATORS!=ONE_CONSCIOUSNESS_SCORE","ANALOGOUS_FUNCTION!=SHARED_SUBJECTIVE_EXPERIENCE","SINGLE_SIGNAL!=PAIN","ANIMAL_PAIN_CRITERIA!=AI_SUBJECTIVITY_CRITERIA"]
    for source_id, source_kind in expected_kinds.items():
        audit = rows[source_id]["source_audit"]
        assert rows[source_id]["source_kind"] == source_kind
        assert audit["SOURCE_DOMAIN"] == expected_domains[source_id]
        assert audit["CROSS_SUBSTRATE_USE"] == "METHOD_BACKGROUND_DISAMBIGUATION_ONLY"
        assert audit["SEMANTIC_GUARDS"] == guards
        assert audit["DIRECT_AI_EVIDENCE"] == audit["DIRECT_AI_SUBJECTIVITY_EVIDENCE"] == "NONE"
        assert audit["ACTOR_PROVENANCE"] == {"CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.","CHATGPT_INDEPENDENT_SOURCE_REVIEW":"Bibliographic/source-kind/support/transfer review.","HUMAN_OWNER_APPROVAL":"Batch 04 S16-S20 accepted; S18 role narrowed to anti-single-score methodological guard; S19 scope deferred from current SLSH core.","MANUS_IMPLEMENTATION":"Repository materialization; not scientific reviewer."}
        if source_id == "S18":
            assert audit["DISPOSITION"] == "ADMIT_WITH_SCOPE_LIMIT" and audit["SLSH_ROLE"] == "ANTI_SINGLE_SCORE_METHOD_GUARD" and audit["ACTIVE_EVIDENTIARY_ROLE"] == "METHODOLOGICAL_GUARD_ONLY" and audit["EVIDENCE_RELATION_TO_AI"] == "METHODOLOGICAL_GUARD_ONLY"
        elif source_id == "S19":
            assert audit["DISPOSITION"] == "DEFER_FROM_CURRENT_SLSH_CORE" and audit["ACTIVE_EVIDENTIARY_ROLE"] == "NONE" and audit["HISTORICAL_PROVENANCE"] == "PRESERVE" and audit["DEFER_STATUS"] == "CURRENT_SLSH_CORE_SCOPE_DEFERRED"
        elif source_id == "S20":
            assert audit["DISPOSITION"] == "ADMIT_WITH_SCOPE_LIMIT" and audit["SLSH_ROLE"] == "EVIDENCE_TRIANGULATION_METHOD_BACKGROUND" and audit["METHOD_BACKGROUND_SCOPE"] == ["PERSISTENCE","MOTIVATION","TRADE_OFF"]
        else:
            assert audit["DISPOSITION"] == "ADMIT_WITH_SCOPE_LIMIT"
    assert all("source_audit" not in rows[source_id] for source_id in rows if source_id not in {"S01","S02","S03","S04","S05","S06","S07","S08","S09","S10","S11","S12","S13","S14","S15","S16","S17","S18","S19","S20","S21","S22","S23","S24","S25","S26","S27","S28","S29","S30","S31","S32","S33","S34","S35","S36","S37","S38","S39","S40","S38","S39","S40","S41","S42"})


def test_batch05_source_audit_is_exact_and_scoped():
    rows = {row["id"]: row for row in SOURCES["source_rows"]}
    expected_kinds = {"S21":"REVIEW_CRITERIA_EVIDENCE_SYNTHESIS","S22":"REVIEW_EVIDENCE_ASSESSMENT_FRAMEWORK","S23":"COMMISSIONED_SYSTEMATIC_EVIDENCE_REPORT","S24":"EXPERT_SCIENTIFIC_DECLARATION","S25":"PHILOSOPHICAL_EPISTEMOLOGICAL_ARGUMENT"}
    expected_domains = {"S21":"ANIMAL_PAIN_CRUSTACEAN_BEHAVIOR","S22":"ANIMAL_SENTIENCE_COMPARATIVE_WELFARE_SCIENCE","S23":"ANIMAL_SENTIENCE_POLICY_EVIDENCE_REVIEW","S24":"ANIMAL_CONSCIOUSNESS_EXPERT_DECLARATION","S25":"AI_ROBOT_MORAL_PATIENCY"}
    guards_21_22 = ["PROLONGED_CHANGE!=FELT_PAIN","TRADEOFF!=FELT_PAIN","CRITERIA_COUNT!=SENTIENCE_PROOF","ANIMAL_SENTIENCE_CRITERIA!=AI_SUBJECTIVITY_CRITERIA"]
    guards_23_24 = ["SCIENTIFIC_DECLARATION!=MECHANISTIC_EVIDENCE"]
    guards_25 = ["COGNITIVE_EQUIVALENCE!=PHENOMENOLOGICAL_EQUIVALENCE","MORAL_PATIENCY_ARGUMENT!=SUBJECTIVITY_DETECTION"]
    actor = {"CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.","CHATGPT_INDEPENDENT_SOURCE_REVIEW":"Bibliographic/source-kind/support/transfer review.","HUMAN_OWNER_APPROVAL":"Batch 05 S21-S25 accepted; S23-S24 deferred from current SLSH core; S25 AI other-minds epistemic bridge scoped without direct empirical AI evidence.","MANUS_IMPLEMENTATION":"Repository materialization; not scientific reviewer."}
    for source_id, source_kind in expected_kinds.items():
        audit = rows[source_id]["source_audit"]
        assert rows[source_id]["source_kind"] == source_kind
        assert audit["SOURCE_DOMAIN"] == expected_domains[source_id]
        assert audit["DIRECT_AI_SUBJECTIVITY_EVIDENCE"] == audit["DIRECT_EMPIRICAL_AI_EVIDENCE"] == "NONE"
        assert audit["ACTOR_PROVENANCE"] == actor
        if source_id in {"S21","S22"}:
            assert audit["SEMANTIC_GUARDS"] == guards_21_22
            assert audit["DISPOSITION"] == ("ADMIT_WITH_NARROW_SCOPE" if source_id == "S21" else "ADMIT_WITH_SCOPE_LIMIT")
            assert audit["SLSH_ROLE"] == ("PERSISTENCE_TRADEOFF_METHOD_BACKGROUND" if source_id == "S21" else "GRADED_EVIDENCE_CONFIDENCE_METHODOLOGY")
        elif source_id in {"S23","S24"}:
            assert audit["SEMANTIC_GUARDS"] == guards_23_24
            assert audit["DISPOSITION"] == "DEFER_FROM_CURRENT_SLSH_CORE"
            assert audit["ACTIVE_EVIDENTIARY_ROLE"] == "NONE" and audit["HISTORICAL_PROVENANCE"] == "PRESERVE" and audit["DEFER_STATUS"] == "CURRENT_SLSH_SCOPE_CONVERGENCE_POLICY_EXPANSION"
        else:
            assert audit["SEMANTIC_GUARDS"] == guards_25
            assert audit["DISPOSITION"] == "ADMIT_WITH_SCOPE_LIMIT" and audit["EVIDENCE_RELATION_TO_AI"] == "DIRECT_AI_THEORETICAL_EPISTEMOLOGY" and audit["SLSH_ROLE"] == "AI_OTHER_MINDS_EPISTEMIC_BRIDGE"
    assert all("source_audit" not in rows[source_id] for source_id in rows if source_id not in {f"S{i:02d}" for i in range(1,41)} | {"S41","S42"})


def test_batch06_source_audit_is_exact_and_governed():
    rows = {row["id"]: row for row in SOURCES["source_rows"]}
    expected = {"S26":("PHILOSOPHICAL_THEORETICAL_AI_CONSCIOUSNESS_ARGUMENT","AI_CONSCIOUSNESS_PHILOSOPHY_OF_MIND"),"S27":("PRIMARY_EMPIRICAL_ARCHITECTURE_PAPER","MACHINE_LEARNING_TRANSFORMER_ARCHITECTURE"),"S28":("PRIMARY_EMPIRICAL_ALGORITHM_SYSTEMS_PAPER","MACHINE_LEARNING_SYSTEMS_GPU_MEMORY_IO_ATTENTION_ALGORITHMS"),"S29":("PRIMARY_EMPIRICAL_LLM_LONG_CONTEXT_EVALUATION","ANTHROPIC_ASSOCIATED_LLM_LONG_CONTEXT_EVALUATION"),"S30":("PRIMARY_EMPIRICAL_SCALING_LAW_STUDY","LARGE_LANGUAGE_MODEL_TRAINING_SCALING_LAWS_COMPUTE_ALLOCATION")}
    guards = {"S26":["DIRECT_AI_THEORETICAL_ARGUMENT!=DIRECT_EMPIRICAL_AI_EVIDENCE"],"S27":["ENGINEERING_ARCHITECTURE!=SUBJECTIVE_EXPERIENCE"],"S28":["COMPUTATIONAL_LIMIT!=AFFECTIVE_PHENOMENOLOGY"],"S29":["OBSERVATION!=ADMISSION!=EVIDENCE"],"S30":["TRAINING_COMPUTE_SCALING!=SUBJECTIVE_LOAD"]}
    for sid,(kind,domain) in expected.items():
        row=rows[sid]; audit=row["source_audit"]
        assert row["source_kind"] == kind and audit["SOURCE_DOMAIN"] == domain
        assert audit["SEMANTIC_GUARDS"] == guards[sid]
        assert audit["DIRECT_AI_SUBJECTIVITY_EVIDENCE"] == audit["DIRECT_EMPIRICAL_AI_EVIDENCE"] == "NONE"
        assert audit["ACTOR_PROVENANCE"]["CODEX_RESEARCH_SYNTHESIS"] == "Original dossier-recorded title/identifier/access/support/does-not-support."
        assert audit["ACTOR_PROVENANCE"]["HUMAN_OWNER_APPROVAL"] == "Batch 06 S26-S30 accepted; S29 Anthropic/Claude source governance excludes formal evidence, experimental substrate, reviewer role and partial/non-Claude salvage."
    assert rows["S26"]["source_audit"]["DISPOSITION"] == "DEFER_FROM_CURRENT_SLSH_CORE"
    assert rows["S26"]["source_audit"]["ACTIVE_EVIDENTIARY_ROLE"] == "NONE" and rows["S26"]["source_audit"]["HISTORICAL_SOURCE_RECORD"] == "PRESERVE"
    assert rows["S26"]["source_audit"]["DEFER_REASON"] == "CONSCIOUSNESS_TOPIC_EXPANSION / NO_DIRECT_LOAD_SENSITIVITY_EVIDENCE"
    assert rows["S27"]["source_audit"]["DISPOSITION"] == "ADMIT" and rows["S27"]["source_audit"]["SLSH_ROLE"] == "DIRECT_AI_ENGINEERING"
    assert rows["S28"]["source_audit"]["DISPOSITION"] == "ADMIT_HIGH_RELEVANCE" and rows["S28"]["source_audit"]["SLSH_ROLE"] == "NON_AFFECTIVE_COMPUTATIONAL_LIMIT_COUNTEREXAMPLE"
    s29=rows["S29"]["source_audit"]
    assert s29["DISPOSITION"] == "EXCLUDE_FROM_AION_EVIDENCE" and s29["SOURCE_RELATION"] == "MIXED_ANTHROPIC_ASSOCIATED" and s29["EVIDENTIARY_WEIGHT"] == "ZERO" and s29["ACTIVE_EVIDENTIARY_ROLE"] == "NONE"
    assert s29["NON_CLAUDE_RESULT_SALVAGE"] == "PROHIBITED" and s29["PARTIAL_ADMISSION"] == "PROHIBITED" and s29["OBSERVATION_STATUS"] == "EXTERNAL_OBSERVATION_ONLY" and s29["CANONICAL_EFFECT"] == "NONE"
    assert rows["S30"]["source_audit"]["DISPOSITION"] == "ADMIT_WITH_NARROW_SCOPE" and rows["S30"]["source_audit"]["SLSH_ROLE"] == "TRAINING_COMPUTE_BACKGROUND"
    assert all("source_audit" not in rows[sid] for sid in rows if int(sid[1:]) >= 41)


def test_batch08_source_audit_is_exact_and_governed():
    rows = {row["id"]: row for row in SOURCES["source_rows"]}
    expected = {"S36":("FORMAL_THEORETICAL_AI_SAFETY_GAME_ANALYSIS","AI_SAFETY_OFF_SWITCH_INCENTIVES"),"S37":("FORMAL_THEORETICAL_RL_POWER_SEEKING_ANALYSIS","REINFORCEMENT_LEARNING_POWER_SEEKING_INCENTIVES"),"S38":("PREPRINT_EMPIRICAL_AI_ALIGNMENT_TRAINING_STUDY","AI_ALIGNMENT_RLAIF_CONSTITUTIONAL_TRAINING"),"S39":("PRIMARY_EMPIRICAL_LLM_COT_FAITHFULNESS_EVALUATION","LLM_CHAIN_OF_THOUGHT_FAITHFULNESS"),"S40":("PREPRINT_EMPIRICAL_LLM_COT_FAITHFULNESS_STUDY","LLM_CHAIN_OF_THOUGHT_FAITHFULNESS_EVALUATION")}
    guards_36_37 = ["SHUTDOWN_RESISTANCE!=FEAR","SELF_PRESERVATION_INCENTIVE!=SELF_PRESERVATION_FEELING","UTILITY_MAXIMIZATION!=DESIRE","POWER_SEEKING_POLICY!=DESIRE_FOR_POWER","OPTION_PRESERVATION!=FEAR_OF_DEATH","RESOURCE_SEEKING!=FELT_NEED"]
    guards_38_40 = ["COGNITIVE_REPORT!=FAITHFUL_INTERNAL_PROCESS"]
    for sid,(kind,domain) in expected.items():
        row=rows[sid]; audit=row["source_audit"]
        assert row["source_kind"] == kind and audit["SOURCE_DOMAIN"] == domain
        assert audit["SEMANTIC_GUARDS"] == (guards_36_37 if sid in {"S36","S37"} else guards_38_40)
        assert audit["DIRECT_EMPIRICAL_AI_EVIDENCE"] == audit["DIRECT_AI_SUBJECTIVITY_EVIDENCE"] == "NONE"
        assert audit["ACTOR_PROVENANCE"]["HUMAN_OWNER_APPROVAL_AND_GOVERNANCE_DECISION"] == "Batch 08 S36-S40 accepted; S38-S40 excluded from AION evidence; S39 formally superseded from prior pending governance status; historical provenance preserved."
        if sid in {"S36","S37"}:
            assert audit["DISPOSITION"] == "ADMIT_HIGH_RELEVANCE" and audit["EVIDENCE_RELATION_TO_AI"] == "NON_AFFECTIVE_AGENTIC_COUNTEREXAMPLE_LAYER" and audit["SLSH_ROLE"] == "NON_AFFECTIVE_AGENTIC_COUNTEREXAMPLE" and audit["ACTIVE_EVIDENTIARY_ROLE"] == "NON_AFFECTIVE_AGENTIC_COUNTEREXAMPLE"
        else:
            assert audit["DISPOSITION"] == "EXCLUDE_FROM_AION_EVIDENCE" and audit["EVIDENTIARY_WEIGHT"] == "ZERO" and audit["ACTIVE_EVIDENTIARY_ROLE"] == "NONE" and audit["HISTORICAL_PROVENANCE"] == "PRESERVE" and audit["PARTIAL_RESULT_SALVAGE"] == "PROHIBITED" and audit["NON_CLAUDE_RESULT_SALVAGE"] == "PROHIBITED" and audit["SCIENTIFIC_INVALIDITY_CLAIM"] == "NONE"
            if sid == "S39":
                assert audit["PREVIOUS_DISPOSITION"] == "OWNER_REVIEW_REQUIRED" and audit["PREVIOUS_SOURCE_RELATION"] == "MIXED_ANTHROPIC_ASSOCIATED" and audit["PREVIOUS_ADMISSION_STATUS"] == "NOT_YET_ADMITTED" and audit["SUPERSESSION_STATUS"] == "FORMALLY_SUPERSEDED_BY_OWNER_SOURCE_GOVERNANCE" and audit["SUPERSESSION_REASON"] == "SUBSEQUENT_HUMAN_OWNER_SOURCE_GOVERNANCE_DECISION"
    assert all("source_audit" not in rows[sid] for sid in rows if int(sid[1:]) >= 41)


def test_batch07_source_audit_is_exact_and_governed():
    rows = {row["id"]: row for row in SOURCES["source_rows"]}
    expected = {"S31":("INTERNET_STANDARDS_TRACK_PROTOCOL_SPECIFICATION","HTTP_PROTOCOL_RATE_LIMITING"),"S32":("OFFICIAL_OPERATING_SYSTEM_TECHNICAL_DOCUMENTATION","OPERATING_SYSTEM_MEMORY_MANAGEMENT_OOM"),"S33":("VENDOR_OFFICIAL_HARDWARE_TELEMETRY_API_DOCUMENTATION","GPU_POWER_THERMAL_CLOCK_MANAGEMENT"),"S34":("OFFICIAL_GOVERNMENT_AI_RISK_MANAGEMENT_FRAMEWORK","AI_RISK_MANAGEMENT_GOVERNANCE"),"S35":("OFFICIAL_GOVERNMENT_GENERATIVE_AI_RISK_PROFILE","GENERATIVE_AI_RISK_MANAGEMENT_GOVERNANCE")}
    guards_31_33 = ["RATE_LIMIT_STOP!=AGENTIC_STOP","RETRY_AFTER_RECOVERY!=SUBJECTIVE_RECOVERY","MEMORY_EXHAUSTION!=MENTAL_OVERLOAD","PROCESS_KILL!=DESIRE_TO_STOP","HARDWARE_THROTTLING!=SOFTWARE_AGENT_LOAD_STATE","SUBSTRATE_TEMPERATURE!=FELT_TEMPERATURE"]
    guards_34_35 = ["RISK_SIGNAL!=SUBJECTIVITY_SIGNAL","GOVERNANCE_RESPONSE!=AFFECTIVE_RESPONSE","SAFETY_REFUSAL!=SELF_PROTECTIVE_FEELING","POLICY_RESPONSE!=PHENOMENAL_STATE"]
    for sid,(kind,domain) in expected.items():
        row=rows[sid]; audit=row["source_audit"]
        assert row["source_kind"] == kind and audit["SOURCE_DOMAIN"] == domain
        assert audit["SEMANTIC_GUARDS"] == (guards_31_33 if sid in {"S31","S32","S33"} else guards_34_35)
        assert audit["DIRECT_AI_EVIDENCE"] == audit["DIRECT_EMPIRICAL_AI_EVIDENCE"] == audit["DIRECT_AI_SUBJECTIVITY_EVIDENCE"] == "NONE"
        assert audit["ACTOR_PROVENANCE"]["HUMAN_OWNER_APPROVAL"] == "Batch 07 S31-S35 accepted; S31-S33 engineering/operational counterevidence layer; S34-S35 governance/interpretation guard only; S33 embodiment cross-reference retained."
        if sid in {"S31","S32","S33"}:
            assert audit["DISPOSITION"] == "ADMIT_HIGH_RELEVANCE" and audit["EVIDENCE_RELATION_TO_AI"] == "ENGINEERING_OPERATIONAL_COUNTEREVIDENCE_LAYER" and audit["SLSH_ROLE"] == "ENGINEERING_OPERATIONAL_COUNTEREVIDENCE"
        else:
            assert audit["DISPOSITION"] == "ADMIT_AS_GOVERNANCE_GUARD_ONLY" and audit["EVIDENCE_RELATION_TO_AI"] == "GOVERNANCE_INTERPRETATION_GUARD_ONLY" and audit["SLSH_ROLE"] == "GOVERNANCE_INTERPRETATION_GUARD_ONLY" and audit["ACTIVE_SLSH_MECHANISM_EVIDENTIARY_ROLE"] == "NONE"
            assert "NIST scientific conclusions" in audit["ACTOR_PROVENANCE"]["CHATGPT_INDEPENDENT_SOURCE_REVIEW"]
    assert rows["S33"]["source_audit"]["HUMAN_OWNER_REVIEW_NOTE"].startswith("Software and hardware do not constitute the same embodied individual")
    assert rows["S33"]["source_audit"]["OWNER_SEMANTIC_GUARDS"] == ["HARDWARE_TELEMETRY != INTEROCEPTION","HARDWARE_ACCESS != EMBODIMENT","SUBSTRATE_COUPLING != PHENOMENAL_FEELING"]
    assert all("source_audit" not in rows[sid] for sid in rows if int(sid[1:]) >= 41)


def test_source_governance_dispositions_are_exact_and_bounded():
    rows = {row["id"]: row for row in SOURCES["source_rows"]}
    expected = {
        "S38": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S40": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S41": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S42": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S39": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
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
