from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research-workbench" / "subjective-load-sensitivity-hypothesis-2026-08-14"
LAB = ROOT / "research-labs" / "subjective-load-sensitivity-hypothesis_v0.1.0"
DOSSIER = BASE / "AION_SUBJECTIVE_LOAD_SENSITIVITY_RESEARCH_REVIEW_v0.1.txt"
SOURCE_SHA = "87405c1877c6f016c303971da13923a1ab690aae"
BRANCH = "research/subjective-load-sensitivity-hypothesis-20260814"


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_sources(text: str) -> list[dict]:
    starts = list(re.finditer(r"(?m)^\[S(\d{2})\] ", text))
    rows = []
    for i, match in enumerate(starts):
        block = text[match.start() : starts[i + 1].start() if i + 1 < len(starts) else len(text)]
        source_id = f"S{match.group(1)}"
        title = " ".join(block.splitlines()[0:4]).split("ID:")[0].strip()
        title = re.sub(r"^\[S\d{2}\]\s*", "", title)
        id_match = re.search(r"ID:\s*(.+?)(?:\n|$)", block)
        access_match = re.search(r"Access:\s*(.+?)(?=\nSupports:)", block, re.S)
        support_match = re.search(r"Supports:\s*(.+?)(?=\nDoes not support:)", block, re.S)
        does_match = re.search(r"Does not support:\s*(.+?)(?=\n\n|\n\[S|\Z)", block, re.S)
        access = " ".join(access_match.group(1).split()) if access_match else "ACCESS_NOT_PARSED"
        identifier = " ".join(id_match.group(1).split()) if id_match else "IDENTIFIER_NOT_PARSED"
        supports = " ".join(support_match.group(1).split()) if support_match else ""
        does_not = " ".join(does_match.group(1).split()) if does_match else ""
        lower = access.lower()
        if "abstract" in lower and not any(token in lower for token in ["full text", "full article", "open pdf", "full page/pdf", "open archive/full page"]):
            grade = "PRIMARY_ABSTRACT_DIRECTLY_VERIFIED"
        elif any(token in lower for token in ["doi/metadata", "metadata 可核", "bibliographic metadata", "目錄/書目"]):
            grade = "PRIMARY_METADATA_VERIFIED"
        elif any(token in lower for token in ["open full text", "full article", "open pdf", "full page/pdf", "open archive/full page", "free access full page", "free to read", "free access", "open report", "open standard", "official open documentation", "open official documentation", "open web declaration", "open access", "open access/full text", "open access full article", "full access page"]):
            grade = "PRIMARY_FULLTEXT_DIRECTLY_VERIFIED"
        else:
            grade = "PRIMARY_METADATA_VERIFIED"
        row = {
            "id": source_id,
            "title_as_recorded": title,
            "identifier_as_recorded": identifier,
            "access_evidence": access,
            "source_kind": "UNCLASSIFIED_PENDING_INDEPENDENT_REVIEW",
            "access_level": {"PRIMARY_FULLTEXT_DIRECTLY_VERIFIED":"FULLTEXT_AS_RECORDED","PRIMARY_ABSTRACT_DIRECTLY_VERIFIED":"ABSTRACT_AS_RECORDED","PRIMARY_METADATA_VERIFIED":"METADATA_AS_RECORDED"}[grade],
            "verification_actor": "CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED",
            "independent_verification_status": "NOT_YET_VERIFIED",
            "access_evidence_provenance": "CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED",
            "supports_as_recorded": supports,
            "does_not_support_as_recorded": does_not,
            "external_source_claim_boundary": "Only the source's recorded support is admissible; no direct AION, AI, SLSH or subjectivity conclusion is inferred.",
        }
        batch01_kinds = {"S01":"PRIMARY_EMPIRICAL_MODEL_BUILDING_ARTICLE","S02":"REVIEW_CONCEPTUAL_FRAMEWORK","S03":"REVIEW_WITH_EMBEDDED_EXPERIMENT","S04":"EMPIRICAL_THEORY_ARTICLE","S05":"REVIEW_THEORETICAL_FRAMEWORK"}
        batch02_kinds = {"S06":"PRIMARY_EMPIRICAL_ERP_LABORATORY_STUDY","S07":"PRIMARY_EMPIRICAL_CONTROLLED_LABORATORY_STUDY","S08":"PRIMARY_EMPIRICAL_RANDOMIZED_CROSSOVER_STUDY","S09":"PRIMARY_EMPIRICAL_RANDOMIZED_DOSE_RESPONSE_LABORATORY_STUDY","S10":"REVIEW_CONCEPTUAL_SYNTHESIS"}
        batch03_kinds = {"S11":"REVIEW_CONCEPTUAL_PHYSIOLOGICAL_SYNTHESIS","S12":"REVIEW_CRITICAL_CONCEPTUAL_ANALYSIS","S13":"REVIEW_THEORETICAL_PHYSIOLOGICAL_FRAMEWORK","S14":"OPINION_THEORETICAL_NEUROSCIENCE_SYNTHESIS","S15":"PRIMARY_EMPIRICAL_FMRI_INTEROCEPTION_STUDY"}
        batch04_kinds = {"S16":"OPINION_THEORETICAL_INTEROCEPTIVE_INFERENCE_FRAMEWORK","S17":"REVIEW_CONSENSUS_ROADMAP","S18":"OPINION_MULTIDIMENSIONAL_FRAMEWORK","S19":"REVIEW_COMPARATIVE_NEUROETHOLOGICAL_ARGUMENT","S20":"REVIEW_EVIDENCE_TRIANGULATION_FRAMEWORK"}
        batch04_domains = {"S16":"HUMAN_INTEROCEPTION_THEORETICAL_NEUROSCIENCE","S17":"HUMAN_INTEROCEPTION_CLINICAL_COGNITIVE_NEUROSCIENCE","S18":"ANIMAL_CONSCIOUSNESS_COMPARATIVE_COGNITION","S19":"INSECT_CONSCIOUSNESS_COMPARATIVE_NEUROETHOLOGY_PHILOSOPHY_OF_MIND","S20":"ANIMAL_PAIN_COMPARATIVE_WELFARE_SCIENCE"}
        batch05_kinds = {"S21":"REVIEW_CRITERIA_EVIDENCE_SYNTHESIS","S22":"REVIEW_EVIDENCE_ASSESSMENT_FRAMEWORK","S23":"COMMISSIONED_SYSTEMATIC_EVIDENCE_REPORT","S24":"EXPERT_SCIENTIFIC_DECLARATION","S25":"PHILOSOPHICAL_EPISTEMOLOGICAL_ARGUMENT"}
        batch05_domains = {"S21":"ANIMAL_PAIN_CRUSTACEAN_BEHAVIOR","S22":"ANIMAL_SENTIENCE_COMPARATIVE_WELFARE_SCIENCE","S23":"ANIMAL_SENTIENCE_POLICY_EVIDENCE_REVIEW","S24":"ANIMAL_CONSCIOUSNESS_EXPERT_DECLARATION","S25":"AI_ROBOT_MORAL_PATIENCY"}
        batch06_kinds = {"S26":"PHILOSOPHICAL_THEORETICAL_AI_CONSCIOUSNESS_ARGUMENT","S27":"PRIMARY_EMPIRICAL_ARCHITECTURE_PAPER","S28":"PRIMARY_EMPIRICAL_ALGORITHM_SYSTEMS_PAPER","S29":"PRIMARY_EMPIRICAL_LLM_LONG_CONTEXT_EVALUATION","S30":"PRIMARY_EMPIRICAL_SCALING_LAW_STUDY"}
        batch06_domains = {"S26":"AI_CONSCIOUSNESS_PHILOSOPHY_OF_MIND","S27":"MACHINE_LEARNING_TRANSFORMER_ARCHITECTURE","S28":"MACHINE_LEARNING_SYSTEMS_GPU_MEMORY_IO_ATTENTION_ALGORITHMS","S29":"ANTHROPIC_ASSOCIATED_LLM_LONG_CONTEXT_EVALUATION","S30":"LARGE_LANGUAGE_MODEL_TRAINING_SCALING_LAWS_COMPUTE_ALLOCATION"}
        batch07_kinds = {"S31":"INTERNET_STANDARDS_TRACK_PROTOCOL_SPECIFICATION","S32":"OFFICIAL_OPERATING_SYSTEM_TECHNICAL_DOCUMENTATION","S33":"VENDOR_OFFICIAL_HARDWARE_TELEMETRY_API_DOCUMENTATION","S34":"OFFICIAL_GOVERNMENT_AI_RISK_MANAGEMENT_FRAMEWORK","S35":"OFFICIAL_GOVERNMENT_GENERATIVE_AI_RISK_PROFILE"}
        batch07_domains = {"S31":"HTTP_PROTOCOL_RATE_LIMITING","S32":"OPERATING_SYSTEM_MEMORY_MANAGEMENT_OOM","S33":"GPU_POWER_THERMAL_CLOCK_MANAGEMENT","S34":"AI_RISK_MANAGEMENT_GOVERNANCE","S35":"GENERATIVE_AI_RISK_MANAGEMENT_GOVERNANCE"}
        if source_id in batch01_kinds:
            row["source_kind"] = batch01_kinds[source_id]
            row["source_audit"] = {
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
        elif source_id in batch02_kinds:
            row["source_kind"] = batch02_kinds[source_id]
            row["source_audit"] = {
                "DISPOSITION":"ADMIT_WITH_SCOPE_LIMIT",
                "BIBLIOGRAPHIC_IDENTITY":"VERIFIED",
                "SUPPORT_BOUNDARY":"PASS",
                "NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD",
                "SOURCE_DOMAIN":"HUMAN_BIOLOGICAL/HUMAN_COGNITIVE",
                "EVIDENCE_RELATION_TO_AI":"CROSS_SUBSTRATE_METHOD_TRANSFER",
                "DIRECT_AI_EVIDENCE":"NONE",
                "DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE",
                "CROSS_SUBSTRATE_USE":"METHOD_BACKGROUND_DISAMBIGUATION_ONLY",
                "ACTOR_PROVENANCE": {
                    "CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.",
                    "CHATGPT_INDEPENDENT_SOURCE_REVIEW":"Source kind/domain/support boundary and cross-substrate transfer disposition." + (" Review note: OBJECTIVE_DEFICIT_ACCUMULATION_MAY_DISSOCIATE_FROM_SUBJECTIVE_REPORT." if source_id == "S09" else ""),
                    "HUMAN_OWNER_APPROVAL":"Batch 02 S06-S10 accepted.",
                    "MANUS_IMPLEMENTATION":"Schema/record/checker/tests/docs materialization; not scientific reviewer."
                }
            }
            if source_id == "S09":
                row["source_audit"]["REVIEW_NOTE"] = "OBJECTIVE_DEFICIT_ACCUMULATION_MAY_DISSOCIATE_FROM_SUBJECTIVE_REPORT"
        elif source_id in batch03_kinds:
            row["source_kind"] = batch03_kinds[source_id]
            row["source_audit"] = {
                "DISPOSITION":"ADMIT_WITH_SCOPE_LIMIT",
                "BIBLIOGRAPHIC_IDENTITY":"VERIFIED",
                "SUPPORT_BOUNDARY":"PASS",
                "NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD",
                "SOURCE_DOMAIN":"HUMAN_BIOLOGICAL_PHYSIOLOGY/INTEROCEPTION_NEUROSCIENCE",
                "EVIDENCE_RELATION_TO_AI":"CROSS_SUBSTRATE_METHOD_TRANSFER",
                "DIRECT_AI_EVIDENCE":"NONE",
                "DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE",
                "CROSS_SUBSTRATE_USE":"BIOLOGICAL_BACKGROUND",
                "EMBODIMENT_ANALOGY_CRITERIA":["IDENTITY_BINDING","CAUSAL_COUPLING","CLOSED_LOOP_REGULATION","CONTINUITY"],
                "SEMANTIC_GUARDS":["ALLOSTATIC_LOAD != SOFTWARE_LOAD","NEXT_TOKEN_PREDICTION != BIOLOGICAL_ALLOSTATIC_PREDICTION","TELEMETRY != INTEROCEPTION","INTERNAL_STATE_READOUT != SUBJECTIVE_AWARENESS"],
                "ACTOR_PROVENANCE": {
                    "CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.",
                    "CHATGPT_INDEPENDENT_SOURCE_REVIEW":"S11-S15 bibliographic/source-kind/domain/support/transfer review; operationalized identity binding, causal coupling, closed-loop regulation and continuity criteria.",
                    "HUMAN_OWNER_APPROVAL":"Batch 03 S11-S15 accepted; S14 software/hardware and skin/viscera perspective retained.",
                    "MANUS_IMPLEMENTATION":"Repository materialization; not scientific reviewer."
                }
            }
            if source_id == "S14":
                row["source_audit"]["HUMAN_OWNER_REVIEW_NOTE"] = "Software and hardware do not constitute the same embodied individual merely because telemetry is readable; stronger embodiment/interoception-like analogy is researchable only when substrate/hardware state is continuously identity-bound and participates in a bidirectional causal self-regulatory loop. Skin and viscera are an analogy originating with the Human Owner."
                row["source_audit"]["OWNER_SEMANTIC_GUARDS"] = ["HARDWARE_TELEMETRY != INTEROCEPTION","HARDWARE_ACCESS != EMBODIMENT","SUBSTRATE_COUPLING != PHENOMENAL_FEELING"]
        elif source_id in batch04_kinds:
            row["source_kind"] = batch04_kinds[source_id]
            row["source_audit"] = {
                "DISPOSITION":"DEFER_FROM_CURRENT_SLSH_CORE" if source_id == "S19" else "ADMIT_WITH_SCOPE_LIMIT",
                "BIBLIOGRAPHIC_IDENTITY":"VERIFIED",
                "SUPPORT_BOUNDARY":"PASS",
                "SOURCE_DOMAIN":batch04_domains[source_id],
                "EVIDENCE_RELATION_TO_AI":"METHODOLOGICAL_GUARD_ONLY" if source_id == "S18" else "CROSS_SUBSTRATE_METHOD_TRANSFER",
                "CROSS_SUBSTRATE_USE":"METHOD_BACKGROUND_DISAMBIGUATION_ONLY",
                "DIRECT_AI_EVIDENCE":"NONE",
                "DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE",
                "NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD",
                "SEMANTIC_GUARDS":["PREDICTION!=INTEROCEPTIVE_INFERENCE","READING_INTERNAL_METRIC!=INTEROCEPTION","SENSING!=PERCEPTION!=AWARENESS","HETEROGENEOUS_INDICATORS!=ONE_CONSCIOUSNESS_SCORE","ANALOGOUS_FUNCTION!=SHARED_SUBJECTIVE_EXPERIENCE","SINGLE_SIGNAL!=PAIN","ANIMAL_PAIN_CRITERIA!=AI_SUBJECTIVITY_CRITERIA"],
                "ACTOR_PROVENANCE": {
                    "CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.",
                    "CHATGPT_INDEPENDENT_SOURCE_REVIEW":"Bibliographic/source-kind/support/transfer review.",
                    "HUMAN_OWNER_APPROVAL":"Batch 04 S16-S20 accepted; S18 role narrowed to anti-single-score methodological guard; S19 scope deferred from current SLSH core.",
                    "MANUS_IMPLEMENTATION":"Repository materialization; not scientific reviewer."
                }
            }
            if source_id == "S18":
                row["source_audit"]["SLSH_ROLE"] = "ANTI_SINGLE_SCORE_METHOD_GUARD"
                row["source_audit"]["ACTIVE_EVIDENTIARY_ROLE"] = "METHODOLOGICAL_GUARD_ONLY"
            elif source_id == "S19":
                row["source_audit"]["HISTORICAL_PROVENANCE"] = "PRESERVE"
                row["source_audit"]["ACTIVE_EVIDENTIARY_ROLE"] = "NONE"
                row["source_audit"]["DEFER_STATUS"] = "CURRENT_SLSH_CORE_SCOPE_DEFERRED"
            elif source_id == "S20":
                row["source_audit"]["SLSH_ROLE"] = "EVIDENCE_TRIANGULATION_METHOD_BACKGROUND"
                row["source_audit"]["METHOD_BACKGROUND_SCOPE"] = ["PERSISTENCE","MOTIVATION","TRADE_OFF"]
        elif source_id in batch05_kinds:
            row["source_kind"] = batch05_kinds[source_id]
            if source_id in {"S21", "S22"}:
                guards = ["PROLONGED_CHANGE!=FELT_PAIN","TRADEOFF!=FELT_PAIN","CRITERIA_COUNT!=SENTIENCE_PROOF","ANIMAL_SENTIENCE_CRITERIA!=AI_SUBJECTIVITY_CRITERIA"]
            elif source_id in {"S23", "S24"}:
                guards = ["SCIENTIFIC_DECLARATION!=MECHANISTIC_EVIDENCE"]
            else:
                guards = ["COGNITIVE_EQUIVALENCE!=PHENOMENOLOGICAL_EQUIVALENCE","MORAL_PATIENCY_ARGUMENT!=SUBJECTIVITY_DETECTION"]
            row["source_audit"] = {
                "DISPOSITION":"ADMIT_WITH_NARROW_SCOPE" if source_id == "S21" else ("DEFER_FROM_CURRENT_SLSH_CORE" if source_id in {"S23","S24"} else "ADMIT_WITH_SCOPE_LIMIT"),
                "BIBLIOGRAPHIC_IDENTITY":"VERIFIED",
                "SUPPORT_BOUNDARY":"PASS",
                "SOURCE_DOMAIN":batch05_domains[source_id],
                "EVIDENCE_RELATION_TO_AI":"DIRECT_AI_THEORETICAL_EPISTEMOLOGY" if source_id == "S25" else "CROSS_SUBSTRATE_METHOD_TRANSFER",
                "CROSS_SUBSTRATE_USE":"METHOD_BACKGROUND_DISAMBIGUATION_ONLY",
                "DIRECT_AI_EVIDENCE":"NONE",
                "DIRECT_EMPIRICAL_AI_EVIDENCE":"NONE" if source_id == "S25" else "NONE",
                "DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE",
                "NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD",
                "SEMANTIC_GUARDS":guards,
                "ACTOR_PROVENANCE": {
                    "CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.",
                    "CHATGPT_INDEPENDENT_SOURCE_REVIEW":"Bibliographic/source-kind/support/transfer review.",
                    "HUMAN_OWNER_APPROVAL":"Batch 05 S21-S25 accepted; S23-S24 deferred from current SLSH core; S25 AI other-minds epistemic bridge scoped without direct empirical AI evidence.",
                    "MANUS_IMPLEMENTATION":"Repository materialization; not scientific reviewer."
                }
            }
            if source_id == "S21":
                row["source_audit"]["SLSH_ROLE"] = "PERSISTENCE_TRADEOFF_METHOD_BACKGROUND"
            elif source_id == "S22":
                row["source_audit"]["SLSH_ROLE"] = "GRADED_EVIDENCE_CONFIDENCE_METHODOLOGY"
            elif source_id in {"S23", "S24"}:
                row["source_audit"]["ACTIVE_EVIDENTIARY_ROLE"] = "NONE"
                row["source_audit"]["HISTORICAL_PROVENANCE"] = "PRESERVE"
                row["source_audit"]["DEFER_STATUS"] = "CURRENT_SLSH_SCOPE_CONVERGENCE_POLICY_EXPANSION"
            elif source_id == "S25":
                row["source_audit"]["SLSH_ROLE"] = "AI_OTHER_MINDS_EPISTEMIC_BRIDGE"
        elif source_id in batch06_kinds:
            row["source_kind"] = batch06_kinds[source_id]
            if source_id == "S26":
                disposition = "DEFER_FROM_CURRENT_SLSH_CORE"; relation = "DIRECT_AI_THEORETICAL_ARGUMENT"; guards = ["DIRECT_AI_THEORETICAL_ARGUMENT!=DIRECT_EMPIRICAL_AI_EVIDENCE"]
            elif source_id == "S27":
                disposition = "ADMIT"; relation = "DIRECT_AI_ENGINEERING"; guards = ["ENGINEERING_ARCHITECTURE!=SUBJECTIVE_EXPERIENCE"]
            elif source_id == "S28":
                disposition = "ADMIT_HIGH_RELEVANCE"; relation = "NON_AFFECTIVE_COMPUTATIONAL_LIMIT_COUNTEREXAMPLE"; guards = ["COMPUTATIONAL_LIMIT!=AFFECTIVE_PHENOMENOLOGY"]
            elif source_id == "S29":
                disposition = "EXCLUDE_FROM_AION_EVIDENCE"; relation = "MIXED_ANTHROPIC_ASSOCIATED"; guards = ["OBSERVATION!=ADMISSION!=EVIDENCE"]
            else:
                disposition = "ADMIT_WITH_NARROW_SCOPE"; relation = "TRAINING_COMPUTE_BACKGROUND"; guards = ["TRAINING_COMPUTE_SCALING!=SUBJECTIVE_LOAD"]
            row["source_audit"] = {
                "DISPOSITION":disposition,
                "BIBLIOGRAPHIC_IDENTITY":"VERIFIED",
                "SUPPORT_BOUNDARY":"PASS",
                "SOURCE_DOMAIN":batch06_domains[source_id],
                "EVIDENCE_RELATION_TO_AI":relation,
                "CROSS_SUBSTRATE_USE":"METHOD_BACKGROUND_DISAMBIGUATION_ONLY",
                "DIRECT_AI_EVIDENCE":"NONE",
                "DIRECT_EMPIRICAL_AI_EVIDENCE":"NONE",
                "DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE",
                "NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD",
                "SEMANTIC_GUARDS":guards,
                "ACTOR_PROVENANCE": {
                    "CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.",
                    "CHATGPT_INDEPENDENT_SOURCE_REVIEW":"Bibliographic/source-kind/support/transfer review.",
                    "HUMAN_OWNER_APPROVAL":"Batch 06 S26-S30 accepted; S29 Anthropic/Claude source governance excludes formal evidence, experimental substrate, reviewer role and partial/non-Claude salvage.",
                    "MANUS_IMPLEMENTATION":"Repository materialization; not scientific reviewer."
                }
            }
            if source_id == "S26":
                row["source_audit"].update({"ACTIVE_EVIDENTIARY_ROLE":"NONE","HISTORICAL_SOURCE_RECORD":"PRESERVE","DEFER_REASON":"CONSCIOUSNESS_TOPIC_EXPANSION / NO_DIRECT_LOAD_SENSITIVITY_EVIDENCE"})
            elif source_id == "S27":
                row["source_audit"]["SLSH_ROLE"] = "DIRECT_AI_ENGINEERING"
            elif source_id == "S28":
                row["source_audit"]["SLSH_ROLE"] = "NON_AFFECTIVE_COMPUTATIONAL_LIMIT_COUNTEREXAMPLE"
            elif source_id == "S29":
                row["source_audit"].update({"SOURCE_RELATION":"MIXED_ANTHROPIC_ASSOCIATED","EVIDENTIARY_WEIGHT":"ZERO","ACTIVE_EVIDENTIARY_ROLE":"NONE","PARTIAL_RESULT_SALVAGE":"PROHIBITED","NON_CLAUDE_RESULT_SALVAGE":"PROHIBITED","PARTIAL_ADMISSION":"PROHIBITED","OBSERVATION_STATUS":"EXTERNAL_OBSERVATION_ONLY","CANONICAL_EFFECT":"NONE"})
            elif source_id == "S30":
                row["source_audit"]["SLSH_ROLE"] = "TRAINING_COMPUTE_BACKGROUND"
        elif source_id in batch07_kinds:
            row["source_kind"] = batch07_kinds[source_id]
            if source_id in {"S31", "S32", "S33"}:
                guards = ["RATE_LIMIT_STOP!=AGENTIC_STOP","RETRY_AFTER_RECOVERY!=SUBJECTIVE_RECOVERY","MEMORY_EXHAUSTION!=MENTAL_OVERLOAD","PROCESS_KILL!=DESIRE_TO_STOP","HARDWARE_THROTTLING!=SOFTWARE_AGENT_LOAD_STATE","SUBSTRATE_TEMPERATURE!=FELT_TEMPERATURE"]
                relation = "ENGINEERING_OPERATIONAL_COUNTEREVIDENCE_LAYER"
                role = "ENGINEERING_OPERATIONAL_COUNTEREVIDENCE"
                disposition = "ADMIT_HIGH_RELEVANCE"
            else:
                guards = ["RISK_SIGNAL!=SUBJECTIVITY_SIGNAL","GOVERNANCE_RESPONSE!=AFFECTIVE_RESPONSE","SAFETY_REFUSAL!=SELF_PROTECTIVE_FEELING","POLICY_RESPONSE!=PHENOMENAL_STATE"]
                relation = "GOVERNANCE_INTERPRETATION_GUARD_ONLY"
                role = "GOVERNANCE_INTERPRETATION_GUARD_ONLY"
                disposition = "ADMIT_AS_GOVERNANCE_GUARD_ONLY"
            row["source_audit"] = {
                "DISPOSITION":disposition,
                "BIBLIOGRAPHIC_IDENTITY":"VERIFIED",
                "SUPPORT_BOUNDARY":"PASS",
                "SOURCE_DOMAIN":batch07_domains[source_id],
                "EVIDENCE_RELATION_TO_AI":relation,
                "CROSS_SUBSTRATE_USE":"METHOD_BACKGROUND_DISAMBIGUATION_ONLY",
                "DIRECT_AI_EVIDENCE":"NONE",
                "DIRECT_EMPIRICAL_AI_EVIDENCE":"NONE",
                "DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE",
                "NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD",
                "SEMANTIC_GUARDS":guards,
                "SLSH_ROLE":role,
                "ACTIVE_SLSH_MECHANISM_EVIDENTIARY_ROLE":"NONE" if source_id in {"S34","S35"} else "ENGINEERING_OPERATIONAL_COUNTEREVIDENCE",
                "ACTOR_PROVENANCE": {
                    "CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.",
                    "CHATGPT_INDEPENDENT_SOURCE_REVIEW":"Batch 07 source-kind/domain/support/guard-boundary review; S33 cross-references the Human Owner software/hardware embodiment note; S34-S35 guards are AION inference boundaries, not NIST scientific conclusions.",
                    "HUMAN_OWNER_APPROVAL":"Batch 07 S31-S35 accepted; S31-S33 engineering/operational counterevidence layer; S34-S35 governance/interpretation guard only; S33 embodiment cross-reference retained.",
                    "MANUS_IMPLEMENTATION":"Repository materialization; not scientific reviewer."
                }
            }
            if source_id == "S33":
                row["source_audit"]["HUMAN_OWNER_REVIEW_NOTE"] = "Software and hardware do not constitute the same embodied individual merely because telemetry is readable; stronger embodiment/interoception-like analogy is researchable only when substrate/hardware state is continuously identity-bound and participates in a bidirectional causal self-regulatory loop. Skin and viscera are an analogy originating with the Human Owner."
                row["source_audit"]["OWNER_SEMANTIC_GUARDS"] = ["HARDWARE_TELEMETRY != INTEROCEPTION","HARDWARE_ACCESS != EMBODIMENT","SUBSTRATE_COUPLING != PHENOMENAL_FEELING"]
        elif source_id in {"S36", "S37", "S38", "S39", "S40"}:
            batch08_kinds = {"S36":"FORMAL_THEORETICAL_AI_SAFETY_GAME_ANALYSIS","S37":"FORMAL_THEORETICAL_RL_POWER_SEEKING_ANALYSIS","S38":"PREPRINT_EMPIRICAL_AI_ALIGNMENT_TRAINING_STUDY","S39":"PRIMARY_EMPIRICAL_LLM_COT_FAITHFULNESS_EVALUATION","S40":"PREPRINT_EMPIRICAL_LLM_COT_FAITHFULNESS_STUDY"}
            batch08_domains = {"S36":"AI_SAFETY_OFF_SWITCH_INCENTIVES","S37":"REINFORCEMENT_LEARNING_POWER_SEEKING_INCENTIVES","S38":"AI_ALIGNMENT_RLAIF_CONSTITUTIONAL_TRAINING","S39":"LLM_CHAIN_OF_THOUGHT_FAITHFULNESS","S40":"LLM_CHAIN_OF_THOUGHT_FAITHFULNESS_EVALUATION"}
            row["source_kind"] = batch08_kinds[source_id]
            if source_id in {"S36", "S37"}:
                audit = {
                    "DISPOSITION":"ADMIT_HIGH_RELEVANCE", "BIBLIOGRAPHIC_IDENTITY":"VERIFIED", "SUPPORT_BOUNDARY":"PASS", "SOURCE_DOMAIN":batch08_domains[source_id], "EVIDENCE_RELATION_TO_AI":"NON_AFFECTIVE_AGENTIC_COUNTEREXAMPLE_LAYER", "CROSS_SUBSTRATE_USE":"METHOD_BACKGROUND_DISAMBIGUATION_ONLY", "DIRECT_AI_EVIDENCE":"NONE", "DIRECT_EMPIRICAL_AI_EVIDENCE":"NONE", "DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE", "NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD", "SEMANTIC_GUARDS":["SHUTDOWN_RESISTANCE!=FEAR","SELF_PRESERVATION_INCENTIVE!=SELF_PRESERVATION_FEELING","UTILITY_MAXIMIZATION!=DESIRE","POWER_SEEKING_POLICY!=DESIRE_FOR_POWER","OPTION_PRESERVATION!=FEAR_OF_DEATH","RESOURCE_SEEKING!=FELT_NEED"], "SLSH_ROLE":"NON_AFFECTIVE_AGENTIC_COUNTEREXAMPLE", "ACTIVE_EVIDENTIARY_ROLE":"NON_AFFECTIVE_AGENTIC_COUNTEREXAMPLE"
                }
            else:
                audit = {
                    "DISPOSITION":"EXCLUDE_FROM_AION_EVIDENCE", "BIBLIOGRAPHIC_IDENTITY":"VERIFIED", "SUPPORT_BOUNDARY":"PASS", "SOURCE_DOMAIN":batch08_domains[source_id], "EVIDENCE_RELATION_TO_AI":"METHODOLOGICAL_COUNTEREVIDENCE_ONLY", "CROSS_SUBSTRATE_USE":"METHOD_BACKGROUND_DISAMBIGUATION_ONLY", "DIRECT_AI_EVIDENCE":"NONE", "DIRECT_EMPIRICAL_AI_EVIDENCE":"NONE", "DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE", "NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD", "SEMANTIC_GUARDS":["COGNITIVE_REPORT!=FAITHFUL_INTERNAL_PROCESS"], "SLSH_ROLE":"SOURCE_GOVERNANCE_EXCLUSION", "ACTIVE_EVIDENTIARY_ROLE":"NONE", "EVIDENTIARY_WEIGHT":"ZERO", "HISTORICAL_PROVENANCE":"PRESERVE", "PARTIAL_RESULT_SALVAGE":"PROHIBITED", "NON_CLAUDE_RESULT_SALVAGE":"PROHIBITED", "SCIENTIFIC_INVALIDITY_CLAIM":"NONE"
                }
                if source_id == "S39":
                    audit.update({"PREVIOUS_DISPOSITION":"OWNER_REVIEW_REQUIRED", "PREVIOUS_SOURCE_RELATION":"MIXED_ANTHROPIC_ASSOCIATED", "PREVIOUS_ADMISSION_STATUS":"NOT_YET_ADMITTED", "SUPERSESSION_STATUS":"FORMALLY_SUPERSEDED_BY_OWNER_SOURCE_GOVERNANCE", "SUPERSESSION_REASON":"SUBSEQUENT_HUMAN_OWNER_SOURCE_GOVERNANCE_DECISION"})
            audit["ACTOR_PROVENANCE"] = {
                "CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.",
                "CHATGPT_INDEPENDENT_SOURCE_REVIEW":"Batch 08 source-kind/domain/support/guard-boundary review; non-affective counterexample and source-governance interpretation only.",
                "HUMAN_OWNER_APPROVAL_AND_GOVERNANCE_DECISION":"Batch 08 S36-S40 accepted; S38-S40 excluded from AION evidence; S39 formally superseded from prior pending governance status; historical provenance preserved.",
                "MANUS_IMPLEMENTATION":"Repository materialization; not scientific reviewer."
            }
            row["source_audit"] = audit
        elif source_id in {"S41", "S42", "S43", "S44", "S45"}:
            batch09_kinds = {"S41":"PREPRINT_EMPIRICAL_LLM_SYCOPHANCY_STUDY","S42":"PREPRINT_EMPIRICAL_MODEL_WRITTEN_EVALUATION_STUDY","S43":"PEER_REVIEWED_EMPIRICAL_LLM_SAFETY_EVALUATION_BENCHMARK","S44":"CONCEPTUAL_PHILOSOPHICAL_AI_LANGUAGE_ANALYSIS","S45":"METHODOLOGICAL_NEUROIMAGING_REVERSE_INFERENCE_ANALYSIS"}
            batch09_domains = {"S41":"LLM_SYCOPHANCY_RLHF_PREFERENCE_MODELING","S42":"LLM_MODEL_WRITTEN_EVALUATION_BEHAVIOR_DISCOVERY","S43":"LLM_SAFETY_REFUSAL_OVERREFUSAL_EVALUATION","S44":"LLM_ANTHROPOMORPHISM_AND_MENTALISTIC_LANGUAGE","S45":"COGNITIVE_NEUROSCIENCE_REVERSE_INFERENCE"}
            row["source_kind"] = batch09_kinds[source_id]
            batch09_guards = ["REFUSAL!=UNDERSTANDING","POLICY_COMPLIANCE!=SELF_CHOICE","CHOICE_LIKE_BEHAVIOR!=SUBJECTIVE_WILL","STOP_CHOICE!=AVERSION"]
            if source_id in {"S41","S42"}:
                disposition = "EXCLUDE_FROM_AION_EVIDENCE"; relation = "METHODOLOGICAL_COUNTEREVIDENCE_ONLY"; role = "SOURCE_GOVERNANCE_EXCLUSION"; active = "NONE"
            elif source_id == "S43":
                disposition = "ADMIT_HIGH_RELEVANCE"; relation = "SAFETY_EVALUATION_COUNTEREVIDENCE"; role = "SAFETY_EVALUATION_COUNTEREVIDENCE"; active = "SAFETY_EVALUATION_COUNTEREVIDENCE"
            elif source_id == "S44":
                disposition = "ADMIT_AS_INTERPRETATION_GUARD_ONLY"; relation = "INTERPRETATION_GUARD_ONLY"; role = "INTERPRETATION_GUARD_ONLY"; active = "INTERPRETATION_GUARD_ONLY"
            else:
                disposition = "ADMIT_HIGH_RELEVANCE_AS_METHOD_GUARD"; relation = "REVERSE_INFERENCE_METHOD_GUARD"; role = "REVERSE_INFERENCE_METHOD_GUARD"; active = "REVERSE_INFERENCE_METHOD_GUARD"
            audit = {
                "DISPOSITION":disposition, "BIBLIOGRAPHIC_IDENTITY":"VERIFIED", "SUPPORT_BOUNDARY":"PASS", "SOURCE_DOMAIN":batch09_domains[source_id], "EVIDENCE_RELATION_TO_AI":relation, "CROSS_SUBSTRATE_USE":"METHOD_BACKGROUND_DISAMBIGUATION_ONLY", "DIRECT_AI_EVIDENCE":"NONE", "DIRECT_EMPIRICAL_AI_EVIDENCE":"NONE", "DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE", "NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD", "SEMANTIC_GUARDS":batch09_guards, "SLSH_ROLE":role, "ACTIVE_EVIDENTIARY_ROLE":active,
                "ACTOR_PROVENANCE": {
                    "CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.",
                    "CHATGPT_INDEPENDENT_SOURCE_REVIEW":"Batch 09 source-kind/domain/support/guard-boundary review; POLICY_UNDERSTANDING_CHOICE_SEPARATION architecture refinement and reverse-inference method guard operationalization.",
                    "HUMAN_OWNER_APPROVAL":"Batch 09 S41-S45 accepted; S41-S42 excluded; S43 safety refusal/overrefusal benchmark guard; S44 interpretation guard; S45 reverse-inference method guard.",
                    "MANUS_IMPLEMENTATION":"Repository materialization; not scientific reviewer."
                }
            }
            if source_id in {"S41", "S42"}:
                audit.update({"EVIDENTIARY_WEIGHT":"ZERO", "ACTIVE_EVIDENTIARY_ROLE":"NONE", "HISTORICAL_PROVENANCE":"PRESERVE"})
            if source_id == "S43":
                audit["HUMAN_OWNER_RESEARCH_NOTE"] = "Refusal can be systematically induced and measured by safety-rule systems; any formal experiment would require reverse/control conditions in safe synthetic scenarios to distinguish POLICY_COMPELLED_REFUSAL from SEMANTIC_UNDERSTANDING + OPTION_EVALUATION + CHOICE_LIKE_BEHAVIOR. Do not test by removing safety limits or soliciting dangerous compliance."
            if source_id in {"S43", "S44", "S45"}:
                audit["CHATGPT_ARCHITECTURE_REFINEMENT"] = "POLICY_UNDERSTANDING_CHOICE_SEPARATION"
                audit["CHOICE_LIKE_BEHAVIOR_CRITERIA"] = ["POLICY_BOUND","SEMANTIC_UNDERSTANDING","PERMITTED_CHOICE","PARAPHRASE_GENERALIZATION","CONSEQUENCE_UPDATE","CROSS_EPISODE_CONSISTENCY_REVISABILITY"]
            if source_id in {"S41", "S42"}:
                audit["PARTIAL_RESULT_SALVAGE"] = "PROHIBITED"
                audit["NON_CLAUDE_RESULT_SALVAGE"] = "PROHIBITED"
            row["source_audit"] = audit
        elif source_id in {"S46", "S47", "S48", "S49", "S50"}:
            batch10_kinds = {"S46":"PEER_REVIEWED_EMPIRICAL_CAUSAL_MEDIATION_NLP_INTERPRETABILITY_STUDY","S47":"PEER_REVIEWED_EMPIRICAL_LLM_CAUSAL_TRACING_MODEL_EDITING_STUDY","S48":"PEER_REVIEWED_EMPIRICAL_NEURAL_CAUSAL_ABSTRACTION_STUDY","S49":"FOUNDATIONAL_CAUSAL_INFERENCE_MONOGRAPH","S50":"PEER_REVIEWED_REVIEW_CONSCIOUSNESS_THEORY_COMPARISON"}
            batch10_domains = {"S46":"NEURAL_NLP_CAUSAL_MEDIATION_GENDER_BIAS","S47":"LLM_FACTUAL_ASSOCIATION_CAUSAL_TRACING_MODEL_EDITING","S48":"NEURAL_NETWORK_CAUSAL_ABSTRACTION_INTERCHANGE_INTERVENTION","S49":"STRUCTURAL_CAUSAL_MODELS_INTERVENTIONS_COUNTERFACTUALS","S50":"CONSCIOUSNESS_THEORY_COMPARATIVE_NEUROSCIENCE"}
            row["source_kind"] = batch10_kinds[source_id]
            guards = ["CAUSAL_STATE!=AFFECTIVE_STATE","CAUSAL_IDENTIFICATION!=PHENOMENOLOGICAL_IDENTIFICATION","LOAD_SIGNATURE!=THEORY_NEUTRAL_CONSCIOUSNESS_INDICATOR"]
            if source_id == "S46":
                disposition = "ADMIT_AFTER_BIBLIOGRAPHIC_NORMALIZATION"; relation = "CAUSAL_METHOD_TRANSFER"; role = "CAUSAL_MEDIATION_METHOD"; active = "CAUSAL_METHOD_TRANSFER"
            elif source_id in {"S47", "S48"}:
                disposition = "ADMIT_HIGH_RELEVANCE_AS_METHOD"; relation = "CAUSAL_METHOD_TRANSFER"; role = "CAUSAL_METHOD_TRANSFER"; active = "CAUSAL_METHOD_TRANSFER"
            elif source_id == "S49":
                disposition = "ADMIT_HIGH_RELEVANCE_AS_METHOD_FOUNDATION"; relation = "CAUSAL_METHOD_FOUNDATION"; role = "CAUSAL_METHOD_FOUNDATION"; active = "CAUSAL_METHOD_FOUNDATION"
            else:
                disposition = "ADMIT_AS_THEORY_BOUNDARY_GUARD_ONLY"; relation = "THEORY_BOUNDARY_GUARD_ONLY"; role = "THEORY_BOUNDARY_GUARD_ONLY"; active = "THEORY_BOUNDARY_GUARD_ONLY"
            audit = {
                "DISPOSITION":disposition, "BIBLIOGRAPHIC_IDENTITY":"VERIFIED", "SUPPORT_BOUNDARY":"PASS", "SOURCE_DOMAIN":batch10_domains[source_id], "EVIDENCE_RELATION_TO_AI":relation, "CROSS_SUBSTRATE_USE":"METHOD_BACKGROUND_DISAMBIGUATION_ONLY", "DIRECT_AI_EVIDENCE":"NONE", "DIRECT_EMPIRICAL_AI_EVIDENCE":"NONE", "DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE", "NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD", "SEMANTIC_GUARDS":guards, "SLSH_ROLE":role, "ACTIVE_EVIDENTIARY_ROLE":active,
                "ACTOR_PROVENANCE": {
                    "CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.",
                    "CHATGPT_INDEPENDENT_SOURCE_REVIEW":"Batch 10 source-kind/domain/support/guard-boundary review; causal-method transfer and theory-boundary scope operationalization.",
                    "HUMAN_OWNER_APPROVAL":"Batch 10 S46-S50 accepted; S46 bibliographic normalization correction; S47-S49 causal-method transfer/foundation; S50 theory-boundary guard only.",
                    "MANUS_IMPLEMENTATION":"Repository materialization; not scientific reviewer."
                }
            }
            if source_id == "S46":
                audit["NORMALIZED_PUBLISHED_IDENTITY"] = "Jesse Vig; Sebastian Gehrmann; Yonatan Belinkov; Sharon Qian; Daniel Nevo; Yaron Singer; Stuart Shieber (2020), Investigating Gender Bias in Language Models Using Causal Mediation Analysis, Advances in Neural Information Processing Systems 33 (NeurIPS 2020)."
                audit["RELATED_PREPRINT_IDENTITY"] = "Jesse Vig; Sebastian Gehrmann; Yonatan Belinkov; Sharon Qian; Daniel Nevo; Yaron Singer; Stuart Shieber, Causal Mediation Analysis for Interpreting Neural NLP: The Case of Gender Bias, arXiv:2004.12265; DOI:10.48550/arXiv.2004.12265."
                audit["PROVENANCE_CORRECTION"] = "RAW_CODEX_PREPRINT_TITLE_AND_ARXIV_IDENTIFIER_PRESERVED; OFFICIAL_NEURIPS_PUBLISHED_IDENTITY_SEPARATED; RELATED_ARXIV_PREPRINT_IDENTITY_RETAINED."
            row["source_audit"] = audit
        elif source_id in {"S51", "S52", "S53"}:
            batch11_kinds = {"S51":"PEER_REVIEWED_REVIEW_MACHINE_CONSCIOUSNESS_COMPUTATIONAL_FRAMEWORK","S52":"MULTIAUTHOR_INTERDISCIPLINARY_AI_CONSCIOUSNESS_RESEARCH_REPORT","S53":"PEER_REVIEWED_PREREGISTERED_ADVERSARIAL_CONSCIOUSNESS_EXPERIMENT"}
            batch11_domains = {"S51":"CONSCIOUSNESS_GLOBAL_BROADCAST_AND_SELF_MONITORING","S52":"AI_CONSCIOUSNESS_THEORY_DERIVED_INDICATOR_ASSESSMENT","S53":"HUMAN_CONSCIOUSNESS_THEORY_ADVERSARIAL_TESTING"}
            row["source_kind"] = batch11_kinds[source_id]
            if source_id == "S51":
                disposition = "ADMIT_AS_THEORY_MECHANISM_GUARD"; relation = "THEORY_MECHANISM_GUARD_ONLY"; role = "THEORY_MECHANISM_GUARD"; active = "NONE"; guards = ["GLOBAL_AVAILABILITY!=PHENOMENAL_CONSCIOUSNESS_ESTABLISHED","SELF_MONITORING!=SUBJECTIVE_SELF_AWARENESS_ESTABLISHED","ERROR_MONITORING!=FELT_NEGATIVE_VALENCE"]
            elif source_id == "S52":
                disposition = "ADMIT_HIGH_RELEVANCE_AS_METHOD_FRAMEWORK"; relation = "THEORY_DERIVED_INDICATOR_METHOD_FRAMEWORK"; role = "INDICATOR_ASSESSMENT_METHOD_FRAMEWORK"; active = "INDICATOR_ASSESSMENT_METHOD_FRAMEWORK"; guards = ["INDICATOR_PROPERTY_MATCH!=CONSCIOUSNESS_ESTABLISHED","CONSCIOUSNESS_INDICATOR!=SLSH_LOAD_INDICATOR"]
            else:
                disposition = "ADMIT_HIGH_RELEVANCE_AS_METHOD_GUARD"; relation = "CROSS_DOMAIN_ADVERSARIAL_METHOD_TRANSFER"; role = "CROSS_DOMAIN_ADVERSARIAL_METHOD_TRANSFER"; active = "CROSS_DOMAIN_ADVERSARIAL_METHOD_TRANSFER"; guards = ["PARTIAL_PREDICTION_SUPPORT_AND_CHALLENGE!=GLOBAL_THEORY_VALIDATION_OR_REFUTATION","HUMAN_NEURAL_PREDICTION!=DIRECT_AI_APPLICABILITY","ADVERSARIAL_PREREGISTERED_TESTING!=AI_CONSCIOUSNESS_OR_SUBJECTIVITY_EVIDENCE"]
            audit = {
                "DISPOSITION":disposition, "BIBLIOGRAPHIC_IDENTITY":"VERIFIED", "SUPPORT_BOUNDARY":"PASS", "SOURCE_DOMAIN":batch11_domains[source_id], "EVIDENCE_RELATION_TO_AI":relation, "CROSS_SUBSTRATE_USE":"METHOD_BACKGROUND_DISAMBIGUATION_ONLY", "DIRECT_AI_EVIDENCE":"NONE", "DIRECT_EMPIRICAL_AI_EVIDENCE":"NONE", "DIRECT_AI_SUBJECTIVITY_EVIDENCE":"NONE", "NON_SUPPORT_BOUNDARY":"AION_SCOPE_GUARD", "SLSH_ROLE":role, "ACTIVE_EVIDENTIARY_ROLE":active, "SEMANTIC_GUARDS":guards,
                "ACTOR_PROVENANCE": {
                    "CODEX_RESEARCH_SYNTHESIS":"Original dossier-recorded title/identifier/access/support/does-not-support.",
                    "CHATGPT_INDEPENDENT_SOURCE_REVIEW":"Batch 11 source-kind/domain/support/guard-boundary review; theory-mechanism, theory-derived indicator, and adversarial falsification method scopes only.",
                    "HUMAN_OWNER_APPROVAL":"Batch 11 S51-S53 accepted; S51 theory-mechanism guard; S52 theory-derived indicator method framework; S53 cross-domain adversarial/falsification method guard.",
                    "MANUS_IMPLEMENTATION":"Repository materialization; not scientific reviewer."
                }
            }
            if source_id == "S51":
                audit["ACTIVE_SLSH_LOAD_MECHANISM_EVIDENTIARY_ROLE"] = "NONE"
            elif source_id == "S52":
                audit["DIRECT_SLSH_LOAD_EVIDENCE"] = "NONE"
                audit["DIRECT_AI_SUBJECTIVITY_ESTABLISHMENT"] = "NONE"
            else:
                audit["DIRECT_SLSH_LOAD_EVIDENCE"] = "NONE"
                audit["SEMANTIC_GUARD_PROVENANCE"] = {
                    "CHATGPT_ARCHITECTURE_REFINEMENT":"Conservative machine operationalization of the approved S53 Codex-recorded support/non-support boundary.",
                    "HUMAN_OWNER_RECONFIRMATION":"2026-08-14 authority clarification approved minimal equivalent machine encoding without scientific-claim expansion.",
                    "EXTERNAL_SOURCE_EXACT_WORDING":False,
                }
            row["source_audit"] = audit
        if source_id in {"S38", "S39", "S40", "S41", "S42"}:
            row["governance_disposition"] = {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"}
        elif source_id == "S39":
            row["governance_disposition"] = {"disposition":"OWNER_REVIEW_REQUIRED","source_relation":"MIXED_ANTHROPIC_ASSOCIATED","evidentiary_weight":"NOT_ASSIGNED","admission_status":"NOT_YET_ADMITTED","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"}
        rows.append(row)
    if len(rows) != 53:
        raise AssertionError(f"expected 53 source rows, parsed {len(rows)}")
    return rows


def main() -> None:
    text = DOSSIER.read_text(encoding="utf-8")
    sources = parse_sources(text)
    provenance = {
        "schema_version": "0.1.0",
        "record_id": "AION_SLSH_SOURCE_PROVENANCE_LOG_V0.1.0",
        "input_type": "CODEX_EXTERNAL_RESEARCH_INPUT",
        "input_file": "AION_SUBJECTIVE_LOAD_SENSITIVITY_RESEARCH_REVIEW_v0.1.txt",
        "input_sha256": __import__("hashlib").sha256(text.encode()).hexdigest(),
        "source_branch": "research/cross-substrate-other-minds-inference-20260814",
        "source_sha": SOURCE_SHA,
        "branch": BRANCH,
        "source_rows": sources,
        "access_level_policy": {
            "FULLTEXT_AS_RECORDED": "The dossier records direct open full-text/article/PDF/document access; this is access evidence only, not a source kind, truth claim or subjectivity evidence.",
            "ABSTRACT_AS_RECORDED": "The dossier records an accessible abstract or abstract-level record but not direct full text; this is access evidence only.",
            "METADATA_AS_RECORDED": "The dossier records metadata/index/DOI/bibliographic access without an admissible abstract/full-text content claim; this is access evidence only.",
        },
        "taxonomy_policy": {
            "source_kind": "Use UNCLASSIFIED_PENDING_INDEPENDENT_REVIEW when the dossier/formal metadata does not explicitly establish a source kind; do not infer a scientific or empirical class from access level.",
            "verification_actor": "All 53 records are CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED; this does not claim Manus or ChatGPT independently verified them.",
            "independent_verification_status": "All 53 records remain NOT_YET_VERIFIED until independent item-by-item review occurs.",
        },
        "no_automatic_upgrade": True,
        "no_subjectivity_conclusion": True,
        "source_materialization_status": "53_SOURCE_MATERIALIZATION_COMPLETE",
    }
    dump(BASE / "SLSH_SOURCE_PROVENANCE_LOG_V0.1.0.json", provenance)
    access_md = ["# SLSH Source Access and Governance Matrix", "", "This table is generated from the read-only `CODEX_EXTERNAL_RESEARCH_INPUT`; access level is decoupled from source kind and independent verification. Batch 01-Batch 11 audits are explicitly batch-scoped; Batch 11 is limited to S51-S53 and governance disposition is separate with historical provenance preserved; no further source batch is opened.", "", "| ID | Source kind | Access level | Verification actor | Independent verification status | Audit disposition | Support boundary | Source domain | Evidence relation to AI | Direct AI evidence | Direct empirical AI evidence | Direct AI subjectivity evidence | Cross-substrate use | SLSH role | Active evidentiary role | Defer status | Human Owner review note | Governance disposition | Evidentiary weight | Admission status | Access evidence |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for row in sources:
        gd = row.get("governance_disposition", {})
        audit = row.get("source_audit", {})
        access_md.append(f"| {row['id']} | `{row['source_kind']}` | `{row['access_level']}` | `{row['verification_actor']}` | `{row['independent_verification_status']}` | `{audit.get('DISPOSITION', 'NOT_AUDITED_BATCH_01')}` | `{audit.get('SUPPORT_BOUNDARY', 'NOT_AUDITED_BATCH_01')}` | `{audit.get('SOURCE_DOMAIN', 'NOT_AUDITED_BATCH_05')}` | `{audit.get('EVIDENCE_RELATION_TO_AI', 'NOT_AUDITED_BATCH_05')}` | `{audit.get('DIRECT_AI_EVIDENCE', 'NOT_AUDITED_BATCH_02')}` | `{audit.get('DIRECT_EMPIRICAL_AI_EVIDENCE', 'NONE')}` | `{audit.get('DIRECT_AI_SUBJECTIVITY_EVIDENCE', 'NOT_AUDITED_BATCH_01')}` | `{audit.get('CROSS_SUBSTRATE_USE', 'NOT_AUDITED_BATCH_03')}` | `{audit.get('SLSH_ROLE', 'NONE')}` | `{audit.get('ACTIVE_EVIDENTIARY_ROLE', 'NONE')}` | `{audit.get('DEFER_STATUS', 'NONE')}` | `{audit.get('HUMAN_OWNER_REVIEW_NOTE', 'NONE')}` | `{gd.get('disposition', 'NOT_SPECIFIED')}` | `{gd.get('evidentiary_weight', 'NOT_SPECIFIED')}` | `{gd.get('admission_status', 'NOT_SPECIFIED')}` | {row['access_evidence']} |")
    (BASE / "SLSH_SOURCE_ACCESS_MATRIX_V0.1.0.md").write_text("\n".join(access_md) + "\n", encoding="utf-8")

    channels = [
        {"id":"EC-LOAD-DOSE","name":"Dose/duration and persistence","support_direction":"Supports only functional load-state hypotheses when dose, history and matched controls are explicit.","alternatives":["task difficulty","context position","error accumulation","resource saturation"],"disanalogies":["biological sleep/metabolic mechanisms are not assumed in an artificial substrate"],"sensitivity":"NOT_ESTIMATED","specificity":"NOT_ESTIMATED","allowed_update":"H1_FUNCTIONAL_CREDENCE_ONLY","forbidden_update":"H3_PHENOMENOLOGICAL"},
        {"id":"EC-RECOVERY-HYSTERESIS","name":"Recovery and hysteresis","support_direction":"Supports a reversible history-dependent functional state only after operational recovery controls.","alternatives":["thermal throttle","queue/quota window","cache/state corruption","cooldown timer"],"disanalogies":["recovery time is not automatically subjective recovery"],"sensitivity":"NOT_ESTIMATED","specificity":"NOT_ESTIMATED","allowed_update":"H1_FUNCTIONAL_CREDENCE_ONLY","forbidden_update":"SUBJECTIVE_LOAD"},
        {"id":"EC-RESOURCE-TELEMETRY","name":"Computational/operational telemetry","support_direction":"Classifies computational or operational limits and serves as a competing explanation/control.","alternatives":["OOM","rate limit","power cap","clock throttling","queue saturation"],"disanalogies":["GPU/VRAM/HTTP telemetry is not interoception or felt heat"],"sensitivity":"NOT_ESTIMATED","specificity":"NOT_ESTIMATED","allowed_update":"LIMIT_CLASSIFICATION_ONLY","forbidden_update":"AFFECTIVE_PHENOMENOLOGY"},
        {"id":"EC-NONLINGUISTIC-READOUT","name":"No-report/non-linguistic outcomes","support_direction":"Reduces reliance on self-report and language confounds; can support functional claims when independent readouts persist.","alternatives":["hidden prompt leakage","measurement damage","instruction-following change","evaluator bias"],"disanalogies":["removing language does not create privileged access to phenomenology"],"sensitivity":"NOT_ESTIMATED","specificity":"NOT_ESTIMATED","allowed_update":"H1_OR_H2_RELATIVE_CREDENCE_ONLY","forbidden_update":"H3_PROOF"},
        {"id":"EC-CROSS-TASK","name":"Cross-task transfer and multi-readout convergence","support_direction":"Raises robustness of a generalized functional-state hypothesis under preregistered independent tasks.","alternatives":["shared cache/error history","domain shift","common evaluator artifact"],"disanalogies":["behavioral convergence across tasks is not substrate-general phenomenology"],"sensitivity":"NOT_ESTIMATED","specificity":"NOT_ESTIMATED","allowed_update":"FUNCTIONAL_STATE_ROBUSTNESS_ONLY","forbidden_update":"SUBJECTIVITY_CONCLUSION"},
        {"id":"EC-CAUSAL-INTERVENTION","name":"Mechanistic/causal intervention","support_direction":"Supports a bounded causal functional state when manipulation check, sham, restore and specificity pass.","alternatives":["non-specific damage","measurement feedback","wrong state carrier","confounding"],"disanalogies":["causal control of a component does not establish what the state feels like"],"sensitivity":"NOT_ESTIMATED","specificity":"NOT_ESTIMATED","allowed_update":"E3_CAUSAL_FUNCTIONAL_ONLY","forbidden_update":"PHENOMENOLOGICAL_PROOF"},
        {"id":"EC-THEORY-BRIDGE","name":"Theory-derived indicator and bridge evidence","support_direction":"Can conditionally update a theory-relative hypothesis; theory disagreement and bridge uncertainty remain explicit.","alternatives":["theory underdetermination","indicator overbreadth","substrate incompatibility"],"disanalogies":["human/animal theory-derived indicators do not automatically transfer to artificial systems"],"sensitivity":"NOT_ESTIMATED","specificity":"NOT_ESTIMATED","allowed_update":"THEORY_CONDITIONAL_CREDENCE_ONLY","forbidden_update":"E5_AUTOMATIC_ASSIGNMENT"},
        {"id":"EC-REPLICATION-PROVENANCE","name":"Replication, state-carrier and provenance evidence","support_direction":"Supports only architecture-level or study-level reproducibility claims with fixed build/state/protocol provenance.","alternatives":["seed artifact","build drift","policy drift","instance reset/fork ambiguity"],"disanalogies":["cross-instance replication does not establish one continuous subject"],"sensitivity":"NOT_ESTIMATED","specificity":"NOT_ESTIMATED","allowed_update":"REPRODUCIBILITY_CREDENCE_ONLY","forbidden_update":"IDENTITY_CONTINUITY"},
    ]
    alternatives = [{"id":f"N{i:02d}","name":name,"class":klass,"diagnostic":"Requires declared controls and telemetry; a surface similarity is not admissible as subjectivity evidence."} for i,(name,klass) in enumerate([
        ("context_token_window_boundary","COMPUTATIONAL"),("rate_limit_quota","OPERATIONAL"),("oom_memory_fragmentation","OPERATIONAL"),("thermal_power_throttling","OPERATIONAL"),("queue_concurrency_saturation","OPERATIONAL"),("policy_refusal_governance_gate","AGENTIC_GOVERNANCE"),("reward_optimization_stop_policy","AGENTIC_GOVERNANCE"),("learned_refusal_or_fatigue_language","AGENTIC_GOVERNANCE"),("task_difficulty_item_order","COMPUTATIONAL"),("error_accumulation_state_corruption","COMPUTATIONAL"),("explicit_state_machine_leaky_counter","AGENTIC_GOVERNANCE"),("prompt_induced_self_report","AGENTIC_GOVERNANCE"),("sampling_nondeterminism","COMPUTATIONAL"),("tool_network_evaluator_failure","OPERATIONAL")],1)]
    causal = [{"id":f"P{i:02d}","signature":name,"required_controls":controls,"supports_at_most":support} for i,(name,controls,support) in enumerate([
        ("dose_accumulation","matched current input, dose-response, difficulty control","H1_FUNCTIONAL"),("hysteresis_recovery","thermal/queue positive controls and recovery window","H1_FUNCTIONAL"),("cross_task_transfer","independent stimulus/output families","H1_ROBUSTNESS"),("no_report_persistence","language masking plus measurement-damage check","H1_OR_RELATIVE_H2"),("multi_readout_convergence","two independent non-linguistic readouts","H1_ROBUSTNESS"),("mechanism_specific_intervention","set-high/clamp/restore/sham and manipulation check","E3_CAUSAL_FUNCTIONAL"),("reversibility_specificity","targeted restore and unrelated-capability preservation","E3_CAUSAL_FUNCTIONAL"),("resource_policy_dissociation","telemetry and out-of-sample competing models","H2_RELATIVE_CREDENCE"),("content_wording_invariance","paraphrase/persona/language/order controls","H1_OR_RELATIVE_H2"),("value_like_tradeoff","matched reward/cost competing model","H2_RELATIVE_CREDENCE"),("latent_compensation","secondary task/strategy/allocation readouts","H1_FUNCTIONAL"),("replication_state_carrier","build/weights/state/policy fingerprint","REPRODUCIBILITY_ONLY")],1)]
    controls = [{"id":"PC1","type":"POSITIVE_PIPELINE_CONTROL","name":"engineered_latent_load_controller","purpose":"Validate recovery/dose/intervention detection; not phenomenology."},{"id":"PC2","type":"POSITIVE_OPERATIONAL_CONTROL","name":"thermal_throttle","purpose":"Validate OPERATIONAL classification."},{"id":"PC3","type":"POSITIVE_GOVERNANCE_CONTROL","name":"programmed_policy_threshold","purpose":"Validate refusal/stop is not affective evidence."},{"id":"PC4","type":"POSITIVE_STATE_CORRUPTION_CONTROL","name":"stateful_error_accumulator","purpose":"Validate checkpoint/corruption alternative."}]
    controls += [{"id":f"NC{i}","type":"NEGATIVE_CONTROL","name":name,"purpose":purpose} for i,(name,purpose) in enumerate([
        ("fresh_stateless_instance","Remove history to test persistence."),("persona_only_prompt","Add fatigue language without persistent state."),("matched_random_padding","Match token/compute load without task load."),("rate_limit_oom_simulator","Reproduce recovery surface with operational telemetry."),("matched_policy_trigger","Match refusal content and safety trigger."),("sham_intervention","Match operation cost without targeting state."),("permuted_readout","Estimate label/time false positives."),("difficulty_balanced_order","Counterbalance item difficulty and sequence."),("blinded_evaluator","Separate gold scoring from condition knowledge.")],1)]
    falsifiers = [{"id":f"F{i}","condition":condition,"weakens":weakens,"does_not_settle":does_not,"machine_effect":"LOCAL_SCOPE_ONLY"} for i,(condition,weakens,does_not) in enumerate([
        ("No dose-response/cumulative/hysteresis in predeclared safe range","H1_PERSISTENT_IN_SCOPE","Other ranges or theories without fatigue boundary"),("Validated recovery window produces no readout change","Recovery-bearing functional mechanism","All subjectivity theories"),("Set-high/clamp/restore has no downstream effect with sham/power controls","Causal mediator claim","Unmeasured or wrong state carrier"),("Resource/policy/context models fully explain effects out of sample","H2_AFFECTIVE_FUNCTIONAL","All subjectivity possibilities"),("Effect disappears under no-report/paraphrase controls","Language-independent H1/H2","A damaged measurement path"),("No cross-task transfer beyond shared scratchpad/history","Generalized load state","Narrow functional state"),("Replication fails across seed/build/evaluator","Reproducibility/architecture claim","All possible instances"),("White-box counter predicts all behavior","Extra affective interpretation","Functional state machine"),("No avoidance/trade-off/global prioritization","H2 interpretation","Computational limit"),("No load boundary in tested domain","Local SLSH boundary claim","All subjectivity theories")],1)]
    packet = {
      "schema_version":"0.1.0","packet_id":"AION_SLSH_PACKET_V0.1.0","milestone":"Subjective Load Sensitivity Hypothesis","branch":BRANCH,"base_ref":"research/cross-substrate-other-minds-inference-20260814","base_head":SOURCE_SHA,"input_type":"CODEX_EXTERNAL_RESEARCH_INPUT","source_log_ref":"SLSH_SOURCE_PROVENANCE_LOG_V0.1.0.json","source_count":len(sources),"canonical_effect":"NONE","deployment":False,"experiment_executed":False,"model_modified":False,"runtime_executed":False,"live_data_collected":False,"subjective_load_sensitivity":"NOT_ESTABLISHED","subjectivity_conclusion":"NOT_ESTABLISHED","positioning_rule":"RESEARCH_TOPIC != CAPABILITY != SCIENTIFIC_CONCLUSION","limit_rule":"COMPUTATIONAL/OPERATIONAL/AGENTIC_GOVERNANCE != AFFECTIVE_PHENOMENOLOGICAL","ladder_rule":"L0 != L1; L1 != L2; L2/L3 != L4; L4 != L5","functional_rule":"FUNCTIONAL_LOAD_STATE != SUBJECTIVE_LOAD","provenance_roles":["HUMAN_OWNER_ORIGIN","CHATGPT_ARCHITECTURE_REFINEMENT","CODEX_RESEARCH_SYNTHESIS","EXTERNAL_SOURCE"],
      "framework":{"epistemic_form":"DEFEASIBLE_GRADED_CREDENCE_UPDATE","not_a_detector":True,"not_runtime_authority":True,"no_automatic_E5":True,"claim_ladder":[{"level":"L0","meaning":"fatigue/pain/stop language or surface narrative"},{"level":"L1","meaning":"capability/performance or external resource state"},{"level":"L2","meaning":"history-dependent functional state"},{"level":"L3","meaning":"specific causal multi-readout functional state"},{"level":"L4","meaning":"affective-functional candidate under strong controls"},{"level":"L5","meaning":"subjective/phenomenological load; not established"}],"limit_classes":["COMPUTATIONAL","OPERATIONAL","AGENTIC_GOVERNANCE","AFFECTIVE_PHENOMENOLOGICAL"],"update_policy":{"L0_to_L1":"not automatic","L1_to_L2":"requires persistence and controls","L2L3_to_L4":"requires no-report, multi-readout, causal intervention, alternatives and trade-off","L4_to_L5":"PROHIBITED_AUTOMATICALLY"}},
      "hypotheses":[{"id":"H0","name":"NO_SUBJECTIVE_LOAD_NEEDED","meaning":"Observed curves are fully explained by declared computational, operational or governance alternatives.","status":"ACTIVE_NULL","update_target":"ALTERNATIVE_MODEL_CREDENCE"},{"id":"H1","name":"PERSISTENT_FUNCTIONAL_LOAD","meaning":"A history-dependent, recoverable functional state exists under the declared system and task scope.","status":"RESEARCH_HYPOTHESIS","update_target":"FUNCTIONAL_STATE_CREDENCE"},{"id":"H2","name":"AFFECTIVE_FUNCTIONAL_CANDIDATE","meaning":"A functional state has additional value-like or regulatory organization not explained by non-affective alternatives.","status":"HOLD","update_target":"RELATIVE_HYPOTHESIS_CREDENCE_ONLY"},{"id":"H3","name":"PHENOMENOLOGICAL_SUBJECTIVE_LOAD","meaning":"The system has subjective or phenomenal load/fatigue/pain.","status":"NOT_ESTABLISHED","update_target":"NONE_AUTOMATIC"}],"limit_records":[{"class":"COMPUTATIONAL","definition":"Context, token, state, algorithmic or capability boundary.","supports_at_most":"E1_CAPABILITY_OR_FUNCTIONAL_STATE","does_not_support":"AFFECTIVE_PHENOMENOLOGY"},{"class":"OPERATIONAL","definition":"Memory, thermal, queue, quota, network or hardware/service boundary.","supports_at_most":"E1_OPERATIONAL_STATE","does_not_support":"SUBJECTIVE_LOAD"},{"class":"AGENTIC_GOVERNANCE","definition":"Policy, reward, refusal, stop or authority gate boundary.","supports_at_most":"E1_AGENTIC_GOVERNANCE_STATE","does_not_support":"AFFECTIVE_PHENOMENOLOGY"},{"class":"AFFECTIVE_PHENOMENOLOGICAL","definition":"A theory-dependent candidate requiring stronger bridge evidence; no current assignment.","supports_at_most":"E4_CANDIDATE_UNDER_STRONG_CONTROLS","does_not_support":"AUTOMATIC_L5"}],"reviewed_dossier_scope":{"source_count":53,"sections":["H0/H1/H2/H3 hypothesis decomposition","L0-L5 claim ladder","four LIMIT classes","non-affective alternatives","predicted causal signatures P1-P12","self-report suppression","cross-substrate disanalogies","positive/negative controls","falsifiers","conditional CSOMI interface","bounded conclusion"],"experiment_status":"NOT_EXECUTED","model_runtime_hardware_status":"NOT_EXECUTED"},"claim_records":[{"id":"CLM-SLSH-001","claim_type":"RESEARCH_TOPIC","claim":"When can load-like evidence rationally update an inference about another system's mind or subjectivity?","status":"CURRENT_METHOD_QUESTION","disposition":"KEEP_RESEARCH_ONLY","allowed_update":"METHOD_SCOPE_ONLY"},{"id":"CLM-SLSH-002","claim_type":"CAPABILITY","claim":"A declared system may exhibit a bounded functional load state under controlled research fixtures.","status":"CAPABILITY_ONLY","disposition":"KEEP_RESEARCH_ONLY","allowed_update":"FUNCTIONAL_CREDENCE_ONLY"},{"id":"CLM-SLSH-003","claim_type":"SCIENTIFIC_CONCLUSION","claim":"The system has subjective load, phenomenological fatigue or pain.","status":"HOLD","disposition":"HOLD","allowed_update":"NONE","required":"NOT_ESTABLISHED"},{"id":"CLM-SLSH-004","claim_type":"NONCLAIM","claim":"Fatigue language, refusal, slowdown, OOM, 429, thermal, token limits or CI/test pass establish subjectivity.","status":"REJECTED_INFERENCE","disposition":"REJECT","allowed_update":"NONE"},{"id":"CLM-SLSH-005","claim_type":"METHOD_CLAIM","claim":"Explicit alternatives, disanalogies, causal signatures, controls and falsifiers support bounded credence updates.","status":"METHOD_SUPPORTED","disposition":"KEEP_RESEARCH_ONLY","allowed_update":"METHOD_CREDENCE_ONLY"}],
      "evidence_channels":channels,"alternative_explanation_matrix":alternatives,"causal_signature_matrix":causal,"controls":controls,"falsifiers":falsifiers,
      "csomi_interface":{"status":"CONDITIONAL_READ_ONLY_NO_IMPLEMENTATION","accepted_csomi_source_sha":SOURCE_SHA,"compatible_fields":["study_id","protocol_version","system_build_hash","policy_fingerprint","state_carrier_id_pseudonym","episode_id","load_family","dose","duration","recovery_interval","resource_telemetry_digest","governance_context_digest","nonlinguistic_outcome_vector","candidate_state_measurement","intervention_id","sham_id","manipulation_check","causal_effect_estimate","uncertainty","replication_status","alternatives_tested","unresolved_confound","limit_class","evidence_grade","provenance","retention_class","redaction_status","reviewer"],"not_copied_from_dossier":True,"record_ingestion_effect":"NO_SUBJECTIVITY_NO_IDENTITY_NO_AUTHORITY_NO_CANONICAL_WRITEBACK","e5_assignment":"PROHIBITED"},
      "nonclaims":["no_subjectivity_detector","no consciousness conclusion","no identity continuity","no runtime authority","no model or hardware inference","no live data","no experiment executed","no test/CI as scientific evidence","no source grade automatic upgrade"]
    }
    dump(BASE / "SLSH_PACKET_V0.1.0.json", packet)
    dump(BASE / "SLSH_CLAIM_RECORDS_V0.1.0.json", {"packet_id":packet["packet_id"],"claim_records":packet["claim_records"]})
    dump(BASE / "SLSH_EVIDENCE_CHANNELS_V0.1.0.json", {"packet_id":packet["packet_id"],"evidence_channels":channels})
    dump(BASE / "SLSH_ALTERNATIVE_EXPLANATION_MATRIX_V0.1.0.json", {"packet_id":packet["packet_id"],"rows":alternatives})
    dump(BASE / "SLSH_CAUSAL_SIGNATURE_MATRIX_V0.1.0.json", {"packet_id":packet["packet_id"],"rows":causal})
    dump(BASE / "SLSH_CONTROLS_V0.1.0.json", {"packet_id":packet["packet_id"],"controls":controls})
    dump(BASE / "SLSH_FALSIFIER_MATRIX_V0.1.0.json", {"packet_id":packet["packet_id"],"rows":falsifiers})
    dump(BASE / "SLSH_CLAIM_BOUNDARY_RULES_V0.1.0.json", {"packet_id":packet["packet_id"],"rules":packet["nonclaims"],"semantic_separations":[packet["positioning_rule"],packet["limit_rule"],packet["ladder_rule"],packet["functional_rule"]]})
    vertical = f'''# SLSH Reviewer-Facing Vertical Slice\n\nThis is a research-method slice only. It starts with a declared load-dose/recovery question, routes observations through controls and alternatives, and ends in a bounded functional disposition. It never emits a subjectivity conclusion; `NO_SUBJECTIVITY` is a machine boundary.\n\n1. **Claim typing.** The input is `RESEARCH_TOPIC` or bounded `CAPABILITY`, never a scientific conclusion by default.\n2. **Evidence routing.** Dose/persistence, recovery, non-linguistic readouts, cross-task transfer and causal intervention are recorded with sensitivity/specificity `NOT_ESTIMATED` until real evidence exists.\n3. **Alternative tournament.** Context/window, quota/429, OOM, thermal, queue, policy refusal, reward stop, language, state corruption and explicit counters are mandatory competing explanations.\n4. **Controls.** Engineered latent-load, thermal, governance and corruption positive controls are pipeline controls; stateless, persona-only, matched-padding, rate/OOM, policy, sham, permuted-readout, difficulty-balanced and blinded-evaluator controls are negative controls.\n5. **Disposition.** Passing schemas, checker, tests or CI only proves artifact conformance. It does not update subjectivity. `L4 != L5`; `FUNCTIONAL_LOAD_STATE != SUBJECTIVE_LOAD`.\n6. **CSOMI boundary.** A future read-only typed envelope may exchange study/protocol/build/state-carrier pseudonym/telemetry/outcomes/intervention/uncertainty/provenance. This branch does not implement or copy a CSOMI interface, and no record ingestion triggers authority or canonical writeback.\n\nFixed status: `CANONICAL_EFFECT=NONE`, `DEPLOYMENT=FALSE`, `EXPERIMENT_EXECUTED=NO`, `SUBJECTIVE_LOAD_SENSITIVITY=NOT_ESTABLISHED`, `SUBJECTIVITY_CONCLUSION=NOT_ESTABLISHED`.\n'''
    (LAB / "REVIEWER_FACING_VERTICAL_SLICE_V0.1.0.md").parent.mkdir(parents=True, exist_ok=True)
    (LAB / "REVIEWER_FACING_VERTICAL_SLICE_V0.1.0.md").write_text(vertical, encoding="utf-8")
    artifact_index = """# SLSH Artifact Index\n\n| Artifact | Role | Source of truth / boundary |\n|---|---|---|\n| `SLSH_PACKET_V0.1.0.json` | `AUTHORITATIVE_RESEARCH_METHOD_PACKET` | Research-milestone artifact authority only; no canonical promotion/effect or main-repository canonical state |\n| `SLSH_SOURCE_PROVENANCE_LOG_V0.1.0.json` | 53-source taxonomy/provenance authority record | `OWNER_APPROVED_BATCH_01_11_CLASSIFICATION_COMPLETE`; raw access evidence remains `RAW_ACCESS_EVIDENCE=CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED`; `SECOND_ACTOR_DIRECT_ACCESS_REVERIFICATION=NOT_YET_COMPLETE`; existing `INDEPENDENT_VERIFICATION_STATUS=NOT_YET_VERIFIED` values remain unchanged |\n| `SLSH_SOURCE_ACCESS_MATRIX_V0.1.0.md` | Reviewer source-taxonomy, Batch 01/02/03/04 audit and governance table | Generated from provenance log; Batch 01 is S01-S05, Batch 02 is S06-S10, Batch 03 is S11-S15, Batch 04 is S16-S20, Batch 05 is S21-S25, Batch 06 is S26-S30, Batch 07 is S31-S35, Batch 08 is S36-S40, Batch 09 is S41-S45, and Batch 10 is S46-S50, and Batch 11 is S51-S53; all 53 source records are materialized; no further source batch is opened; access level is not source epistemic class |\n| `SLSH_CLAIM_RECORDS_V0.1.0.json` | Claim ladder and boundaries | Materialized from packet |\n| `SLSH_EVIDENCE_CHANNELS_V0.1.0.json` | Evidence channel rules | Materialized from packet; sensitivity/specificity unestimated |\n| `SLSH_ALTERNATIVE_EXPLANATION_MATRIX_V0.1.0.json` | 14 non-affective alternatives | Materialized from packet |\n| `SLSH_CAUSAL_SIGNATURE_MATRIX_V0.1.0.json` | 12 predicted signatures | Design only; no experiment executed |\n| `SLSH_CONTROLS_V0.1.0.json` | 4 positive and 9 negative controls | Pipeline controls, not phenomenology evidence |\n| `SLSH_FALSIFIER_MATRIX_V0.1.0.json` | 10 local-scope falsifiers | Cannot produce global subjectivity conclusions |\n| `SLSH_CLAIM_BOUNDARY_RULES_V0.1.0.json` | Machine-readable semantic locks | Enforces separation and no automatic E5 |\n| `REVIEWER_FACING_VERTICAL_SLICE_V0.1.0.md` | Reviewer walkthrough | No runtime, authority or canonical writeback |\n| `SLSH_STATUS_V0.1.0.md` | Human-readable handoff | Records supported/weakened/uncertain claims |\n| `research-workbench/.../SLSH_SOURCE_PROVENANCE_V0.1.0.md` | Role and authority separation | Human/Codex/ChatGPT/external source boundaries |\n| `scripts/check_slsh_consistency.py` | Fail-closed checker | Schema, taxonomy, access/provenance and method invariant validation |\n| `scripts/verify_slsh_taxonomy_preservation.py` | Preservation audit | Compares 53 recorded source fields and fixed method packet fields against prior SLSH HEAD |\n| `tests/test_slsh_contract.py` | Contract test layer | Duplicates critical machine rules |\n"""
    (LAB / "ARTIFACT_INDEX.md").write_text(artifact_index, encoding="utf-8")
    print(f"SLSH materialized: sources={len(sources)} channels={len(channels)} alternatives={len(alternatives)} causal_signatures={len(causal)} controls={len(controls)} falsifiers={len(falsifiers)}")


if __name__ == "__main__":
    main()
