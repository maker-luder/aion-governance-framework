from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research-workbench" / "subjective-load-sensitivity-hypothesis-2026-08-14"
PREVIOUS = "e857fa13f02b108038b4d843a0ad7054855767a5"
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
    expected_batch03_kinds = {"S11":"REVIEW_CONCEPTUAL_PHYSIOLOGICAL_SYNTHESIS","S12":"REVIEW_CRITICAL_CONCEPTUAL_ANALYSIS","S13":"REVIEW_THEORETICAL_PHYSIOLOGICAL_FRAMEWORK","S14":"OPINION_THEORETICAL_NEUROSCIENCE_SYNTHESIS","S15":"PRIMARY_EMPIRICAL_FMRI_INTEROCEPTION_STUDY"}
    expected_batch03_common = {"DISPOSITION":"ADMIT_WITH_SCOPE_LIMIT","BIBLIOGRAPHIC_IDENTITY":"VERIFIED","SUPPORT_BOUNDARY":"PASS","NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD","SOURCE_DOMAIN":"HUMAN_BIOLOGICAL_PHYSIOLOGY/INTEROCEPTION_NEUROSCIENCE","EVIDENCE_RELATION_TO_AI":"CROSS_SUBSTRATE_METHOD_TRANSFER","DIRECT_AI_EVIDENCE":"NONE","DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE","CROSS_SUBSTRATE_USE":"BIOLOGICAL_BACKGROUND","EMBODIMENT_ANALOGY_CRITERIA":["IDENTITY_BINDING","CAUSAL_COUPLING","CLOSED_LOOP_REGULATION","CONTINUITY"],"SEMANTIC_GUARDS":["ALLOSTATIC_LOAD != SOFTWARE_LOAD","NEXT_TOKEN_PREDICTION != BIOLOGICAL_ALLOSTATIC_PREDICTION","TELEMETRY != INTEROCEPTION","INTERNAL_STATE_READOUT != SUBJECTIVE_AWARENESS"]}
    expected_batch04_kinds = {"S16":"OPINION_THEORETICAL_INTEROCEPTIVE_INFERENCE_FRAMEWORK","S17":"REVIEW_CONSENSUS_ROADMAP","S18":"OPINION_MULTIDIMENSIONAL_FRAMEWORK","S19":"REVIEW_COMPARATIVE_NEUROETHOLOGICAL_ARGUMENT","S20":"REVIEW_EVIDENCE_TRIANGULATION_FRAMEWORK"}
    expected_batch04_domains = {"S16":"HUMAN_INTEROCEPTION_THEORETICAL_NEUROSCIENCE","S17":"HUMAN_INTEROCEPTION_CLINICAL_COGNITIVE_NEUROSCIENCE","S18":"ANIMAL_CONSCIOUSNESS_COMPARATIVE_COGNITION","S19":"INSECT_CONSCIOUSNESS_COMPARATIVE_NEUROETHOLOGY_PHILOSOPHY_OF_MIND","S20":"ANIMAL_PAIN_COMPARATIVE_WELFARE_SCIENCE"}
    expected_batch04_guards = ["PREDICTION!=INTEROCEPTIVE_INFERENCE","READING_INTERNAL_METRIC!=INTEROCEPTION","SENSING!=PERCEPTION!=AWARENESS","HETEROGENEOUS_INDICATORS!=ONE_CONSCIOUSNESS_SCORE","ANALOGOUS_FUNCTION!=SHARED_SUBJECTIVE_EXPERIENCE","SINGLE_SIGNAL!=PAIN","ANIMAL_PAIN_CRITERIA!=AI_SUBJECTIVITY_CRITERIA"]
    expected_batch05_kinds = {"S21":"REVIEW_CRITERIA_EVIDENCE_SYNTHESIS","S22":"REVIEW_EVIDENCE_ASSESSMENT_FRAMEWORK","S23":"COMMISSIONED_SYSTEMATIC_EVIDENCE_REPORT","S24":"EXPERT_SCIENTIFIC_DECLARATION","S25":"PHILOSOPHICAL_EPISTEMOLOGICAL_ARGUMENT"}
    expected_batch05_domains = {"S21":"ANIMAL_PAIN_CRUSTACEAN_BEHAVIOR","S22":"ANIMAL_SENTIENCE_COMPARATIVE_WELFARE_SCIENCE","S23":"ANIMAL_SENTIENCE_POLICY_EVIDENCE_REVIEW","S24":"ANIMAL_CONSCIOUSNESS_EXPERT_DECLARATION","S25":"AI_ROBOT_MORAL_PATIENCY"}
    expected_batch05_guards_21_22 = ["PROLONGED_CHANGE!=FELT_PAIN","TRADEOFF!=FELT_PAIN","CRITERIA_COUNT!=SENTIENCE_PROOF","ANIMAL_SENTIENCE_CRITERIA!=AI_SUBJECTIVITY_CRITERIA"]
    expected_batch05_guards_23_24 = ["SCIENTIFIC_DECLARATION!=MECHANISTIC_EVIDENCE"]
    expected_batch05_guards_25 = ["COGNITIVE_EQUIVALENCE!=PHENOMENOLOGICAL_EQUIVALENCE","MORAL_PATIENCY_ARGUMENT!=SUBJECTIVITY_DETECTION"]
    expected_batch06_kinds = {"S26":"PHILOSOPHICAL_THEORETICAL_AI_CONSCIOUSNESS_ARGUMENT","S27":"PRIMARY_EMPIRICAL_ARCHITECTURE_PAPER","S28":"PRIMARY_EMPIRICAL_ALGORITHM_SYSTEMS_PAPER","S29":"PRIMARY_EMPIRICAL_LLM_LONG_CONTEXT_EVALUATION","S30":"PRIMARY_EMPIRICAL_SCALING_LAW_STUDY"}
    expected_batch06_domains = {"S26":"AI_CONSCIOUSNESS_PHILOSOPHY_OF_MIND","S27":"MACHINE_LEARNING_TRANSFORMER_ARCHITECTURE","S28":"MACHINE_LEARNING_SYSTEMS_GPU_MEMORY_IO_ATTENTION_ALGORITHMS","S29":"ANTHROPIC_ASSOCIATED_LLM_LONG_CONTEXT_EVALUATION","S30":"LARGE_LANGUAGE_MODEL_TRAINING_SCALING_LAWS_COMPUTE_ALLOCATION"}
    expected_batch06_guards = {"S26":["DIRECT_AI_THEORETICAL_ARGUMENT!=DIRECT_EMPIRICAL_AI_EVIDENCE"],"S27":["ENGINEERING_ARCHITECTURE!=SUBJECTIVE_EXPERIENCE"],"S28":["COMPUTATIONAL_LIMIT!=AFFECTIVE_PHENOMENOLOGY"],"S29":["OBSERVATION!=ADMISSION!=EVIDENCE"],"S30":["TRAINING_COMPUTE_SCALING!=SUBJECTIVE_LOAD"]}
    expected_batch07_kinds = {"S31":"INTERNET_STANDARDS_TRACK_PROTOCOL_SPECIFICATION","S32":"OFFICIAL_OPERATING_SYSTEM_TECHNICAL_DOCUMENTATION","S33":"VENDOR_OFFICIAL_HARDWARE_TELEMETRY_API_DOCUMENTATION","S34":"OFFICIAL_GOVERNMENT_AI_RISK_MANAGEMENT_FRAMEWORK","S35":"OFFICIAL_GOVERNMENT_GENERATIVE_AI_RISK_PROFILE"}
    expected_batch07_domains = {"S31":"HTTP_PROTOCOL_RATE_LIMITING","S32":"OPERATING_SYSTEM_MEMORY_MANAGEMENT_OOM","S33":"GPU_POWER_THERMAL_CLOCK_MANAGEMENT","S34":"AI_RISK_MANAGEMENT_GOVERNANCE","S35":"GENERATIVE_AI_RISK_MANAGEMENT_GOVERNANCE"}
    expected_batch07_guards_31_33 = ["RATE_LIMIT_STOP!=AGENTIC_STOP","RETRY_AFTER_RECOVERY!=SUBJECTIVE_RECOVERY","MEMORY_EXHAUSTION!=MENTAL_OVERLOAD","PROCESS_KILL!=DESIRE_TO_STOP","HARDWARE_THROTTLING!=SOFTWARE_AGENT_LOAD_STATE","SUBSTRATE_TEMPERATURE!=FELT_TEMPERATURE"]
    expected_batch07_guards_34_35 = ["RISK_SIGNAL!=SUBJECTIVITY_SIGNAL","GOVERNANCE_RESPONSE!=AFFECTIVE_RESPONSE","SAFETY_REFUSAL!=SELF_PROTECTIVE_FEELING","POLICY_RESPONSE!=PHENOMENAL_STATE"]
    expected_batch08_kinds = {"S36":"FORMAL_THEORETICAL_AI_SAFETY_GAME_ANALYSIS","S37":"FORMAL_THEORETICAL_RL_POWER_SEEKING_ANALYSIS","S38":"PREPRINT_EMPIRICAL_AI_ALIGNMENT_TRAINING_STUDY","S39":"PRIMARY_EMPIRICAL_LLM_COT_FAITHFULNESS_EVALUATION","S40":"PREPRINT_EMPIRICAL_LLM_COT_FAITHFULNESS_STUDY"}
    expected_batch08_domains = {"S36":"AI_SAFETY_OFF_SWITCH_INCENTIVES","S37":"REINFORCEMENT_LEARNING_POWER_SEEKING_INCENTIVES","S38":"AI_ALIGNMENT_RLAIF_CONSTITUTIONAL_TRAINING","S39":"LLM_CHAIN_OF_THOUGHT_FAITHFULNESS","S40":"LLM_CHAIN_OF_THOUGHT_FAITHFULNESS_EVALUATION"}
    expected_batch09_kinds = {"S41":"PREPRINT_EMPIRICAL_LLM_SYCOPHANCY_STUDY","S42":"PREPRINT_EMPIRICAL_MODEL_WRITTEN_EVALUATION_STUDY","S43":"PEER_REVIEWED_EMPIRICAL_LLM_SAFETY_EVALUATION_BENCHMARK","S44":"CONCEPTUAL_PHILOSOPHICAL_AI_LANGUAGE_ANALYSIS","S45":"METHODOLOGICAL_NEUROIMAGING_REVERSE_INFERENCE_ANALYSIS"}
    expected_batch09_domains = {"S41":"LLM_SYCOPHANCY_RLHF_PREFERENCE_MODELING","S42":"LLM_MODEL_WRITTEN_EVALUATION_BEHAVIOR_DISCOVERY","S43":"LLM_SAFETY_REFUSAL_OVERREFUSAL_EVALUATION","S44":"LLM_ANTHROPOMORPHISM_AND_MENTALISTIC_LANGUAGE","S45":"COGNITIVE_NEUROSCIENCE_REVERSE_INFERENCE"}
    expected_batch10_kinds = {"S46":"PEER_REVIEWED_EMPIRICAL_CAUSAL_MEDIATION_NLP_INTERPRETABILITY_STUDY","S47":"PEER_REVIEWED_EMPIRICAL_LLM_CAUSAL_TRACING_MODEL_EDITING_STUDY","S48":"PEER_REVIEWED_EMPIRICAL_NEURAL_CAUSAL_ABSTRACTION_STUDY","S49":"FOUNDATIONAL_CAUSAL_INFERENCE_MONOGRAPH","S50":"PEER_REVIEWED_REVIEW_CONSCIOUSNESS_THEORY_COMPARISON"}
    expected_batch10_domains = {"S46":"NEURAL_NLP_CAUSAL_MEDIATION_GENDER_BIAS","S47":"LLM_FACTUAL_ASSOCIATION_CAUSAL_TRACING_MODEL_EDITING","S48":"NEURAL_NETWORK_CAUSAL_ABSTRACTION_INTERCHANGE_INTERVENTION","S49":"STRUCTURAL_CAUSAL_MODELS_INTERVENTIONS_COUNTERFACTUALS","S50":"CONSCIOUSNESS_THEORY_COMPARATIVE_NEUROSCIENCE"}
    expected_batch11_kinds = {"S51":"PEER_REVIEWED_REVIEW_MACHINE_CONSCIOUSNESS_COMPUTATIONAL_FRAMEWORK","S52":"MULTIAUTHOR_INTERDISCIPLINARY_AI_CONSCIOUSNESS_RESEARCH_REPORT","S53":"PEER_REVIEWED_PREREGISTERED_ADVERSARIAL_CONSCIOUSNESS_EXPERIMENT"}
    expected_batch11_domains = {"S51":"CONSCIOUSNESS_GLOBAL_BROADCAST_AND_SELF_MONITORING","S52":"AI_CONSCIOUSNESS_THEORY_DERIVED_INDICATOR_ASSESSMENT","S53":"HUMAN_CONSCIOUSNESS_THEORY_ADVERSARIAL_TESTING"}
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
        "S39": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
    }
    for source_id in ("S29", "S38", "S39", "S40", "S41", "S42"):
        audit = current_rows[source_id].get("source_audit", {})
        assert audit.get("DISPOSITION") == "EXCLUDE_FROM_AION_EVIDENCE", source_id
        assert audit.get("EVIDENTIARY_WEIGHT") == "ZERO", source_id
        assert audit.get("ACTIVE_EVIDENTIARY_ROLE") == "NONE", source_id
        assert audit.get("PARTIAL_RESULT_SALVAGE") == "PROHIBITED", source_id
        assert audit.get("NON_CLAUDE_RESULT_SALVAGE") == "PROHIBITED", source_id
    for source_id in current_rows:
        for field in RAW_FIELDS:
            assert current_rows[source_id][field] == previous_rows[source_id][field], (source_id, field)
        assert "verification_status" not in current_rows[source_id]
        if source_id in expected_batch01_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch01_kinds[source_id]
        elif source_id in expected_batch02_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch02_kinds[source_id]
        elif source_id in expected_batch03_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch03_kinds[source_id]
        elif source_id in expected_batch04_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch04_kinds[source_id]
        elif source_id in expected_batch05_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch05_kinds[source_id]
        elif source_id in expected_batch06_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch06_kinds[source_id]
        elif source_id in expected_batch07_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch07_kinds[source_id]
        elif source_id in expected_batch08_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch08_kinds[source_id]
        elif source_id in expected_batch09_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch09_kinds[source_id]
        elif source_id in expected_batch10_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch10_kinds[source_id]
        elif source_id in expected_batch11_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch11_kinds[source_id]
        else:
            assert current_rows[source_id]["source_kind"] == "UNCLASSIFIED_PENDING_INDEPENDENT_REVIEW"
        assert current_rows[source_id]["verification_actor"] == "CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED"
        assert current_rows[source_id]["independent_verification_status"] == "NOT_YET_VERIFIED"
        if source_id in expected_batch01_kinds:
            assert current_rows[source_id].get("source_audit") == expected_batch01_audit
        elif source_id in expected_batch11_kinds:
            audit = current_rows[source_id].get("source_audit", {})
            assert current_rows[source_id]["source_kind"] == expected_batch11_kinds[source_id]
            assert audit["SOURCE_DOMAIN"] == expected_batch11_domains[source_id]
            assert audit["DIRECT_AI_SUBJECTIVITY_EVIDENCE"] == "NONE"
            assert audit["DISPOSITION"] in {"ADMIT_AS_THEORY_MECHANISM_GUARD","ADMIT_HIGH_RELEVANCE_AS_METHOD_FRAMEWORK","ADMIT_HIGH_RELEVANCE_AS_METHOD_GUARD"}
            if source_id == "S51":
                assert audit["SEMANTIC_GUARDS"] == ["GLOBAL_AVAILABILITY!=PHENOMENAL_CONSCIOUSNESS_ESTABLISHED","SELF_MONITORING!=SUBJECTIVE_SELF_AWARENESS_ESTABLISHED","ERROR_MONITORING!=FELT_NEGATIVE_VALENCE"]
                assert audit["ACTIVE_SLSH_LOAD_MECHANISM_EVIDENTIARY_ROLE"] == "NONE"
            elif source_id == "S52":
                assert audit["SEMANTIC_GUARDS"] == ["INDICATOR_PROPERTY_MATCH!=CONSCIOUSNESS_ESTABLISHED","CONSCIOUSNESS_INDICATOR!=SLSH_LOAD_INDICATOR"]
                assert audit["DIRECT_SLSH_LOAD_EVIDENCE"] == "NONE" and audit["DIRECT_AI_SUBJECTIVITY_ESTABLISHMENT"] == "NONE"
            else:
                assert audit["SEMANTIC_GUARDS"] == [] and audit["DIRECT_SLSH_LOAD_EVIDENCE"] == "NONE"
        elif source_id in expected_batch10_kinds:
            audit = current_rows[source_id].get("source_audit", {})
            assert current_rows[source_id]["source_kind"] == expected_batch10_kinds[source_id]
            assert audit["SOURCE_DOMAIN"] == expected_batch10_domains[source_id]
            assert audit["SEMANTIC_GUARDS"] == ["CAUSAL_STATE!=AFFECTIVE_STATE","CAUSAL_IDENTIFICATION!=PHENOMENOLOGICAL_IDENTIFICATION","LOAD_SIGNATURE!=THEORY_NEUTRAL_CONSCIOUSNESS_INDICATOR"]
            assert audit["DIRECT_AI_SUBJECTIVITY_EVIDENCE"] == "NONE"
            assert audit["DISPOSITION"] in {"ADMIT_AFTER_BIBLIOGRAPHIC_NORMALIZATION","ADMIT_HIGH_RELEVANCE_AS_METHOD","ADMIT_HIGH_RELEVANCE_AS_METHOD_FOUNDATION","ADMIT_AS_THEORY_BOUNDARY_GUARD_ONLY"}
            if source_id == "S46":
                assert audit["NORMALIZED_PUBLISHED_IDENTITY"].startswith("Vig et al. (2020), Causal Mediation Analysis")
                assert audit["PROVENANCE_CORRECTION"] == "PREPRINT_TITLE_VENUE_MIXED_WITH_PUBLISHED_VENUE; RAW_CODEX_IDENTITY_PRESERVED; NORMALIZED_NEURIPS_PUBLISHED_IDENTITY_ADDED."
        elif source_id in expected_batch09_kinds:
            audit = current_rows[source_id].get("source_audit", {})
            assert current_rows[source_id]["source_kind"] == expected_batch09_kinds[source_id]
            assert audit["SOURCE_DOMAIN"] == expected_batch09_domains[source_id]
            assert audit["SEMANTIC_GUARDS"] == ["REFUSAL!=UNDERSTANDING","POLICY_COMPLIANCE!=SELF_CHOICE","CHOICE_LIKE_BEHAVIOR!=SUBJECTIVE_WILL","STOP_CHOICE!=AVERSION"]
            assert audit["DIRECT_AI_SUBJECTIVITY_EVIDENCE"] == "NONE"
            if source_id in {"S41","S42"}:
                assert audit["DISPOSITION"] == "EXCLUDE_FROM_AION_EVIDENCE" and audit["EVIDENTIARY_WEIGHT"] == "ZERO" and audit["ACTIVE_EVIDENTIARY_ROLE"] == "NONE" and audit["HISTORICAL_PROVENANCE"] == "PRESERVE"
            else:
                assert audit["DISPOSITION"] in {"ADMIT_HIGH_RELEVANCE","ADMIT_AS_INTERPRETATION_GUARD_ONLY","ADMIT_HIGH_RELEVANCE_AS_METHOD_GUARD"}
        elif source_id in expected_batch08_kinds:
            audit = current_rows[source_id].get("source_audit", {})
            assert current_rows[source_id]["source_kind"] == expected_batch08_kinds[source_id]
            assert audit["SOURCE_DOMAIN"] == expected_batch08_domains[source_id]
            assert audit["DIRECT_AI_SUBJECTIVITY_EVIDENCE"] == "NONE"
            if source_id in {"S36","S37"}:
                assert audit["DISPOSITION"] == "ADMIT_HIGH_RELEVANCE"
            else:
                assert audit["DISPOSITION"] == "EXCLUDE_FROM_AION_EVIDENCE" and audit["EVIDENTIARY_WEIGHT"] == "ZERO" and audit["ACTIVE_EVIDENTIARY_ROLE"] == "NONE" and audit["HISTORICAL_PROVENANCE"] == "PRESERVE"
        elif source_id in expected_batch07_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch07_kinds[source_id]
            audit = current_rows[source_id].get("source_audit", {})
            assert audit["SOURCE_DOMAIN"] == expected_batch07_domains[source_id]
            assert audit["SEMANTIC_GUARDS"] == (expected_batch07_guards_31_33 if source_id in {"S31","S32","S33"} else expected_batch07_guards_34_35)
            assert audit["DIRECT_AI_EVIDENCE"] == audit["DIRECT_EMPIRICAL_AI_EVIDENCE"] == audit["DIRECT_AI_SUBJECTIVITY_EVIDENCE"] == "NONE"
            actor = audit["ACTOR_PROVENANCE"]
            assert actor["HUMAN_OWNER_APPROVAL"] == "Batch 07 S31-S35 accepted; S31-S33 engineering/operational counterevidence layer; S34-S35 governance/interpretation guard only; S33 embodiment cross-reference retained."
            if source_id in {"S31","S32","S33"}:
                assert audit["DISPOSITION"] == "ADMIT_HIGH_RELEVANCE" and audit["EVIDENCE_RELATION_TO_AI"] == "ENGINEERING_OPERATIONAL_COUNTEREVIDENCE_LAYER" and audit["SLSH_ROLE"] == "ENGINEERING_OPERATIONAL_COUNTEREVIDENCE"
                if source_id == "S33":
                    assert "HUMAN_OWNER_REVIEW_NOTE" in audit and audit["OWNER_SEMANTIC_GUARDS"] == ["HARDWARE_TELEMETRY != INTEROCEPTION","HARDWARE_ACCESS != EMBODIMENT","SUBSTRATE_COUPLING != PHENOMENAL_FEELING"]
            else:
                assert audit["DISPOSITION"] == "ADMIT_AS_GOVERNANCE_GUARD_ONLY" and audit["EVIDENCE_RELATION_TO_AI"] == "GOVERNANCE_INTERPRETATION_GUARD_ONLY" and audit["SLSH_ROLE"] == "GOVERNANCE_INTERPRETATION_GUARD_ONLY" and audit["ACTIVE_SLSH_MECHANISM_EVIDENTIARY_ROLE"] == "NONE"
        elif source_id in expected_batch06_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch06_kinds[source_id]
            audit = current_rows[source_id].get("source_audit", {})
            assert audit["SOURCE_DOMAIN"] == expected_batch06_domains[source_id]
            assert audit["SEMANTIC_GUARDS"] == expected_batch06_guards[source_id]
            assert audit["DIRECT_AI_SUBJECTIVITY_EVIDENCE"] == audit["DIRECT_EMPIRICAL_AI_EVIDENCE"] == "NONE"
            actor = audit["ACTOR_PROVENANCE"]
            assert actor["HUMAN_OWNER_APPROVAL"] == "Batch 06 S26-S30 accepted; S29 Anthropic/Claude source governance excludes formal evidence, experimental substrate, reviewer role and partial/non-Claude salvage."
            if source_id == "S26":
                assert audit["DISPOSITION"] == "DEFER_FROM_CURRENT_SLSH_CORE" and audit["ACTIVE_EVIDENTIARY_ROLE"] == "NONE" and audit["HISTORICAL_SOURCE_RECORD"] == "PRESERVE" and audit["DEFER_REASON"] == "CONSCIOUSNESS_TOPIC_EXPANSION / NO_DIRECT_LOAD_SENSITIVITY_EVIDENCE"
            elif source_id == "S27":
                assert audit["DISPOSITION"] == "ADMIT" and audit["SLSH_ROLE"] == "DIRECT_AI_ENGINEERING"
            elif source_id == "S28":
                assert audit["DISPOSITION"] == "ADMIT_HIGH_RELEVANCE" and audit["SLSH_ROLE"] == "NON_AFFECTIVE_COMPUTATIONAL_LIMIT_COUNTEREXAMPLE"
            elif source_id == "S29":
                assert audit["DISPOSITION"] == "EXCLUDE_FROM_AION_EVIDENCE" and audit["SOURCE_RELATION"] == "MIXED_ANTHROPIC_ASSOCIATED" and audit["EVIDENTIARY_WEIGHT"] == "ZERO" and audit["ACTIVE_EVIDENTIARY_ROLE"] == "NONE" and audit["NON_CLAUDE_RESULT_SALVAGE"] == "PROHIBITED" and audit["PARTIAL_ADMISSION"] == "PROHIBITED" and audit["OBSERVATION_STATUS"] == "EXTERNAL_OBSERVATION_ONLY" and audit["CANONICAL_EFFECT"] == "NONE"
            else:
                assert audit["DISPOSITION"] == "ADMIT_WITH_NARROW_SCOPE" and audit["SLSH_ROLE"] == "TRAINING_COMPUTE_BACKGROUND"
        elif source_id in expected_batch05_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch05_kinds[source_id]
            audit = current_rows[source_id].get("source_audit", {})
            assert audit["SOURCE_DOMAIN"] == expected_batch05_domains[source_id]
            assert audit["DIRECT_AI_SUBJECTIVITY_EVIDENCE"] == audit["DIRECT_EMPIRICAL_AI_EVIDENCE"] == "NONE"
            actor = audit["ACTOR_PROVENANCE"]
            assert actor == {"CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.","CHATGPT_INDEPENDENT_SOURCE_REVIEW":"Bibliographic/source-kind/support/transfer review.","HUMAN_OWNER_APPROVAL":"Batch 05 S21-S25 accepted; S23-S24 deferred from current SLSH core; S25 AI other-minds epistemic bridge scoped without direct empirical AI evidence.","MANUS_IMPLEMENTATION":"Repository materialization; not scientific reviewer."}
            if source_id in {"S21", "S22"}:
                assert audit["SEMANTIC_GUARDS"] == expected_batch05_guards_21_22
                assert audit["DISPOSITION"] == ("ADMIT_WITH_NARROW_SCOPE" if source_id == "S21" else "ADMIT_WITH_SCOPE_LIMIT")
                assert audit["SLSH_ROLE"] == ("PERSISTENCE_TRADEOFF_METHOD_BACKGROUND" if source_id == "S21" else "GRADED_EVIDENCE_CONFIDENCE_METHODOLOGY")
            elif source_id in {"S23", "S24"}:
                assert audit["SEMANTIC_GUARDS"] == expected_batch05_guards_23_24
                assert audit["DISPOSITION"] == "DEFER_FROM_CURRENT_SLSH_CORE" and audit["ACTIVE_EVIDENTIARY_ROLE"] == "NONE" and audit["HISTORICAL_PROVENANCE"] == "PRESERVE" and audit["DEFER_STATUS"] == "CURRENT_SLSH_SCOPE_CONVERGENCE_POLICY_EXPANSION"
            else:
                assert audit["SEMANTIC_GUARDS"] == expected_batch05_guards_25
                assert audit["DISPOSITION"] == "ADMIT_WITH_SCOPE_LIMIT" and audit["EVIDENCE_RELATION_TO_AI"] == "DIRECT_AI_THEORETICAL_EPISTEMOLOGY" and audit["SLSH_ROLE"] == "AI_OTHER_MINDS_EPISTEMIC_BRIDGE"
        elif source_id in expected_batch04_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch04_kinds[source_id]
            audit = current_rows[source_id].get("source_audit", {})
            assert audit["SOURCE_DOMAIN"] == expected_batch04_domains[source_id]
            assert audit["CROSS_SUBSTRATE_USE"] == "METHOD_BACKGROUND_DISAMBIGUATION_ONLY"
            assert audit["SEMANTIC_GUARDS"] == expected_batch04_guards
            assert audit["DIRECT_AI_EVIDENCE"] == audit["DIRECT_AI_SUBJECTIVITY_EVIDENCE"] == "NONE"
            actor = audit["ACTOR_PROVENANCE"]
            assert actor == {"CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.","CHATGPT_INDEPENDENT_SOURCE_REVIEW":"Bibliographic/source-kind/support/transfer review.","HUMAN_OWNER_APPROVAL":"Batch 04 S16-S20 accepted; S18 role narrowed to anti-single-score methodological guard; S19 scope deferred from current SLSH core.","MANUS_IMPLEMENTATION":"Repository materialization; not scientific reviewer."}
            if source_id == "S18":
                assert audit["DISPOSITION"] == "ADMIT_WITH_SCOPE_LIMIT" and audit["SLSH_ROLE"] == "ANTI_SINGLE_SCORE_METHOD_GUARD" and audit["ACTIVE_EVIDENTIARY_ROLE"] == "METHODOLOGICAL_GUARD_ONLY" and audit["EVIDENCE_RELATION_TO_AI"] == "METHODOLOGICAL_GUARD_ONLY"
            elif source_id == "S19":
                assert audit["DISPOSITION"] == "DEFER_FROM_CURRENT_SLSH_CORE" and audit["ACTIVE_EVIDENTIARY_ROLE"] == "NONE" and audit["HISTORICAL_PROVENANCE"] == "PRESERVE" and audit["DEFER_STATUS"] == "CURRENT_SLSH_CORE_SCOPE_DEFERRED"
            elif source_id == "S20":
                assert audit["DISPOSITION"] == "ADMIT_WITH_SCOPE_LIMIT" and audit["SLSH_ROLE"] == "EVIDENCE_TRIANGULATION_METHOD_BACKGROUND" and audit["METHOD_BACKGROUND_SCOPE"] == ["PERSISTENCE","MOTIVATION","TRADE_OFF"]
            else:
                assert audit["DISPOSITION"] == "ADMIT_WITH_SCOPE_LIMIT"
        elif source_id in expected_batch03_kinds:
            assert current_rows[source_id]["source_kind"] == expected_batch03_kinds[source_id]
            audit = current_rows[source_id].get("source_audit", {})
            assert all(audit.get(key) == value for key, value in expected_batch03_common.items())
            actor = audit["ACTOR_PROVENANCE"]
            assert actor["CODEX_RESEARCH_SYNTHESIS"] == "Original dossier-recorded title/identifier/access/support/does-not-support."
            assert actor["CHATGPT_INDEPENDENT_SOURCE_REVIEW"] == "S11-S15 bibliographic/source-kind/domain/support/transfer review; operationalized identity binding, causal coupling, closed-loop regulation and continuity criteria."
            assert actor["HUMAN_OWNER_APPROVAL"] == "Batch 03 S11-S15 accepted; S14 software/hardware and skin/viscera perspective retained."
            assert actor["MANUS_IMPLEMENTATION"] == "Repository materialization; not scientific reviewer."
            if source_id == "S14":
                assert audit["HUMAN_OWNER_REVIEW_NOTE"].startswith("Software and hardware do not constitute the same embodied individual")
                assert audit["OWNER_SEMANTIC_GUARDS"] == ["HARDWARE_TELEMETRY != INTEROCEPTION","HARDWARE_ACCESS != EMBODIMENT","SUBSTRATE_COUPLING != PHENOMENAL_FEELING"]
            else:
                assert "HUMAN_OWNER_REVIEW_NOTE" not in audit and "OWNER_SEMANTIC_GUARDS" not in audit
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
    print("SLSH Batch 01-11 preservation PASS: 53 raw source records unchanged; S01-S53 audit records preserved and exact; 53_SOURCE_MATERIALIZATION_COMPLETE; S38-S42 governance isolated")


if __name__ == "__main__":
    main()
