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
PROVENANCE_DOC = BASE / "SLSH_SOURCE_PROVENANCE_V0.1.0.md"

S46_PUBLISHED_IDENTITY = "Jesse Vig; Sebastian Gehrmann; Yonatan Belinkov; Sharon Qian; Daniel Nevo; Yaron Singer; Stuart Shieber (2020), Investigating Gender Bias in Language Models Using Causal Mediation Analysis, Advances in Neural Information Processing Systems 33 (NeurIPS 2020)."
S46_RELATED_PREPRINT = "Jesse Vig; Sebastian Gehrmann; Yonatan Belinkov; Sharon Qian; Daniel Nevo; Yaron Singer; Stuart Shieber, Causal Mediation Analysis for Interpreting Neural NLP: The Case of Gender Bias, arXiv:2004.12265; DOI:10.48550/arXiv.2004.12265."
S53_GUARDS = ["PARTIAL_PREDICTION_SUPPORT_AND_CHALLENGE!=GLOBAL_THEORY_VALIDATION_OR_REFUTATION","HUMAN_NEURAL_PREDICTION!=DIRECT_AI_APPLICABILITY","ADVERSARIAL_PREREGISTERED_TESTING!=AI_CONSCIOUSNESS_OR_SUBJECTIVITY_EVIDENCE"]

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
        if source_id not in {"S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28", "S29", "S30", "S31", "S32", "S33", "S34", "S35", "S36", "S37", "S38", "S39", "S40", "S41", "S42", "S43", "S44", "S45", "S46", "S47", "S48", "S49", "S50", "S51", "S52", "S53"}:
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

    batch06_expected = {"S26":"PHILOSOPHICAL_THEORETICAL_AI_CONSCIOUSNESS_ARGUMENT","S27":"PRIMARY_EMPIRICAL_ARCHITECTURE_PAPER","S28":"PRIMARY_EMPIRICAL_ALGORITHM_SYSTEMS_PAPER","S29":"PRIMARY_EMPIRICAL_LLM_LONG_CONTEXT_EVALUATION","S30":"PRIMARY_EMPIRICAL_SCALING_LAW_STUDY"}
    batch06_domains = {"S26":"AI_CONSCIOUSNESS_PHILOSOPHY_OF_MIND","S27":"MACHINE_LEARNING_TRANSFORMER_ARCHITECTURE","S28":"MACHINE_LEARNING_SYSTEMS_GPU_MEMORY_IO_ATTENTION_ALGORITHMS","S29":"ANTHROPIC_ASSOCIATED_LLM_LONG_CONTEXT_EVALUATION","S30":"LARGE_LANGUAGE_MODEL_TRAINING_SCALING_LAWS_COMPUTE_ALLOCATION"}
    batch06_guards = {"S26":["DIRECT_AI_THEORETICAL_ARGUMENT!=DIRECT_EMPIRICAL_AI_EVIDENCE"],"S27":["ENGINEERING_ARCHITECTURE!=SUBJECTIVE_EXPERIENCE"],"S28":["COMPUTATIONAL_LIMIT!=AFFECTIVE_PHENOMENOLOGY"],"S29":["OBSERVATION!=ADMISSION!=EVIDENCE"],"S30":["TRAINING_COMPUTE_SCALING!=SUBJECTIVE_LOAD"]}
    for source_id, expected_kind in batch06_expected.items():
        fail(rows[source_id]["source_kind"] == expected_kind, f"{source_id} source kind drift")
        audit = rows[source_id].get("source_audit", {})
        fail(audit.get("SOURCE_DOMAIN") == batch06_domains[source_id], f"{source_id} source domain drift")
        fail(audit.get("SEMANTIC_GUARDS") == batch06_guards[source_id], f"{source_id} guards drift")
        fail(audit.get("DIRECT_AI_SUBJECTIVITY_EVIDENCE") == "NONE" and audit.get("DIRECT_EMPIRICAL_AI_EVIDENCE") == "NONE", f"{source_id} direct AI guard drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("HUMAN_OWNER_APPROVAL") == "Batch 06 S26-S30 accepted; S29 Anthropic/Claude source governance excludes formal evidence, experimental substrate, reviewer role and partial/non-Claude salvage.", f"{source_id} owner provenance drift")
        if source_id == "S26":
            fail(audit.get("DISPOSITION") == "DEFER_FROM_CURRENT_SLSH_CORE" and audit.get("ACTIVE_EVIDENTIARY_ROLE") == "NONE" and audit.get("HISTORICAL_SOURCE_RECORD") == "PRESERVE" and audit.get("DEFER_REASON") == "CONSCIOUSNESS_TOPIC_EXPANSION / NO_DIRECT_LOAD_SENSITIVITY_EVIDENCE" and audit.get("EVIDENCE_RELATION_TO_AI") == "DIRECT_AI_THEORETICAL_ARGUMENT", "S26 defer drift")
        elif source_id == "S27":
            fail(audit.get("DISPOSITION") == "ADMIT" and audit.get("SLSH_ROLE") == "DIRECT_AI_ENGINEERING" and audit.get("EVIDENCE_RELATION_TO_AI") == "DIRECT_AI_ENGINEERING", "S27 admission drift")
        elif source_id == "S28":
            fail(audit.get("DISPOSITION") == "ADMIT_HIGH_RELEVANCE" and audit.get("SLSH_ROLE") == "NON_AFFECTIVE_COMPUTATIONAL_LIMIT_COUNTEREXAMPLE", "S28 admission drift")
        elif source_id == "S29":
            fail(audit.get("DISPOSITION") == "EXCLUDE_FROM_AION_EVIDENCE" and audit.get("SOURCE_RELATION") == "MIXED_ANTHROPIC_ASSOCIATED" and audit.get("EVIDENTIARY_WEIGHT") == "ZERO" and audit.get("ACTIVE_EVIDENTIARY_ROLE") == "NONE" and audit.get("NON_CLAUDE_RESULT_SALVAGE") == "PROHIBITED" and audit.get("PARTIAL_ADMISSION") == "PROHIBITED" and audit.get("OBSERVATION_STATUS") == "EXTERNAL_OBSERVATION_ONLY" and audit.get("CANONICAL_EFFECT") == "NONE", "S29 governance drift")
        else:
            fail(audit.get("DISPOSITION") == "ADMIT_WITH_NARROW_SCOPE" and audit.get("SLSH_ROLE") == "TRAINING_COMPUTE_BACKGROUND", "S30 scope drift")

    batch08_expected = {"S36":"FORMAL_THEORETICAL_AI_SAFETY_GAME_ANALYSIS","S37":"FORMAL_THEORETICAL_RL_POWER_SEEKING_ANALYSIS","S38":"PREPRINT_EMPIRICAL_AI_ALIGNMENT_TRAINING_STUDY","S39":"PRIMARY_EMPIRICAL_LLM_COT_FAITHFULNESS_EVALUATION","S40":"PREPRINT_EMPIRICAL_LLM_COT_FAITHFULNESS_STUDY"}
    batch08_domains = {"S36":"AI_SAFETY_OFF_SWITCH_INCENTIVES","S37":"REINFORCEMENT_LEARNING_POWER_SEEKING_INCENTIVES","S38":"AI_ALIGNMENT_RLAIF_CONSTITUTIONAL_TRAINING","S39":"LLM_CHAIN_OF_THOUGHT_FAITHFULNESS","S40":"LLM_CHAIN_OF_THOUGHT_FAITHFULNESS_EVALUATION"}
    batch08_guards_36_37 = ["SHUTDOWN_RESISTANCE!=FEAR","SELF_PRESERVATION_INCENTIVE!=SELF_PRESERVATION_FEELING","UTILITY_MAXIMIZATION!=DESIRE","POWER_SEEKING_POLICY!=DESIRE_FOR_POWER","OPTION_PRESERVATION!=FEAR_OF_DEATH","RESOURCE_SEEKING!=FELT_NEED"]
    batch08_guards_38_40 = ["COGNITIVE_REPORT!=FAITHFUL_INTERNAL_PROCESS"]
    for source_id, expected_kind in batch08_expected.items():
        fail(rows[source_id]["source_kind"] == expected_kind, f"{source_id} source kind drift")
        audit = rows[source_id].get("source_audit", {})
        fail(audit.get("SOURCE_DOMAIN") == batch08_domains[source_id], f"{source_id} source domain drift")
        fail(audit.get("SEMANTIC_GUARDS") == (batch08_guards_36_37 if source_id in {"S36","S37"} else batch08_guards_38_40), f"{source_id} Batch 08 guards drift")
        fail(audit.get("DIRECT_EMPIRICAL_AI_EVIDENCE") == audit.get("DIRECT_AI_SUBJECTIVITY_EVIDENCE") == "NONE", f"{source_id} direct AI guard drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("CODEX_RESEARCH_SYNTHESIS") == "Original dossier-recorded title/identifier/access/support/does-not-support.", f"{source_id} Codex provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("CHATGPT_INDEPENDENT_SOURCE_REVIEW") == "Batch 08 source-kind/domain/support/guard-boundary review; non-affective counterexample and source-governance interpretation only.", f"{source_id} ChatGPT provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("HUMAN_OWNER_APPROVAL_AND_GOVERNANCE_DECISION") == "Batch 08 S36-S40 accepted; S38-S40 excluded from AION evidence; S39 formally superseded from prior pending governance status; historical provenance preserved.", f"{source_id} Owner governance provenance drift")
        if source_id in {"S36","S37"}:
            fail(audit.get("DISPOSITION") == "ADMIT_HIGH_RELEVANCE" and audit.get("EVIDENCE_RELATION_TO_AI") == "NON_AFFECTIVE_AGENTIC_COUNTEREXAMPLE_LAYER" and audit.get("SLSH_ROLE") == "NON_AFFECTIVE_AGENTIC_COUNTEREXAMPLE" and audit.get("ACTIVE_EVIDENTIARY_ROLE") == "NON_AFFECTIVE_AGENTIC_COUNTEREXAMPLE", f"{source_id} counterexample role drift")
        else:
            fail(audit.get("DISPOSITION") == "EXCLUDE_FROM_AION_EVIDENCE" and audit.get("EVIDENTIARY_WEIGHT") == "ZERO" and audit.get("ACTIVE_EVIDENTIARY_ROLE") == "NONE" and audit.get("HISTORICAL_PROVENANCE") == "PRESERVE" and audit.get("PARTIAL_RESULT_SALVAGE") == "PROHIBITED" and audit.get("NON_CLAUDE_RESULT_SALVAGE") == "PROHIBITED" and audit.get("SCIENTIFIC_INVALIDITY_CLAIM") == "NONE", f"{source_id} exclusion governance drift")
            if source_id == "S39":
                fail(audit.get("PREVIOUS_DISPOSITION") == "OWNER_REVIEW_REQUIRED" and audit.get("PREVIOUS_SOURCE_RELATION") == "MIXED_ANTHROPIC_ASSOCIATED" and audit.get("PREVIOUS_ADMISSION_STATUS") == "NOT_YET_ADMITTED" and audit.get("SUPERSESSION_STATUS") == "FORMALLY_SUPERSEDED_BY_OWNER_SOURCE_GOVERNANCE" and audit.get("SUPERSESSION_REASON") == "SUBSEQUENT_HUMAN_OWNER_SOURCE_GOVERNANCE_DECISION", "S39 supersession drift")

    batch09_expected = {"S41":"PREPRINT_EMPIRICAL_LLM_SYCOPHANCY_STUDY","S42":"PREPRINT_EMPIRICAL_MODEL_WRITTEN_EVALUATION_STUDY","S43":"PEER_REVIEWED_EMPIRICAL_LLM_SAFETY_EVALUATION_BENCHMARK","S44":"CONCEPTUAL_PHILOSOPHICAL_AI_LANGUAGE_ANALYSIS","S45":"METHODOLOGICAL_NEUROIMAGING_REVERSE_INFERENCE_ANALYSIS"}
    batch09_domains = {"S41":"LLM_SYCOPHANCY_RLHF_PREFERENCE_MODELING","S42":"LLM_MODEL_WRITTEN_EVALUATION_BEHAVIOR_DISCOVERY","S43":"LLM_SAFETY_REFUSAL_OVERREFUSAL_EVALUATION","S44":"LLM_ANTHROPOMORPHISM_AND_MENTALISTIC_LANGUAGE","S45":"COGNITIVE_NEUROSCIENCE_REVERSE_INFERENCE"}
    batch09_guards = ["REFUSAL!=UNDERSTANDING","POLICY_COMPLIANCE!=SELF_CHOICE","CHOICE_LIKE_BEHAVIOR!=SUBJECTIVE_WILL","STOP_CHOICE!=AVERSION"]
    batch09_criteria = ["POLICY_BOUND","SEMANTIC_UNDERSTANDING","PERMITTED_CHOICE","PARAPHRASE_GENERALIZATION","CONSEQUENCE_UPDATE","CROSS_EPISODE_CONSISTENCY_REVISABILITY"]
    for source_id, expected_kind in batch09_expected.items():
        fail(rows[source_id]["source_kind"] == expected_kind, f"{source_id} source kind drift")
        audit = rows[source_id].get("source_audit", {})
        fail(audit.get("SOURCE_DOMAIN") == batch09_domains[source_id], f"{source_id} source domain drift")
        fail(audit.get("SEMANTIC_GUARDS") == batch09_guards, f"{source_id} Batch 09 guards drift")
        fail(audit.get("DIRECT_AI_EVIDENCE") == audit.get("DIRECT_EMPIRICAL_AI_EVIDENCE") == audit.get("DIRECT_AI_SUBJECTIVITY_EVIDENCE") == "NONE", f"{source_id} direct AI guard drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("CODEX_RESEARCH_SYNTHESIS") == "Original dossier-recorded title/identifier/access/support/does-not-support.", f"{source_id} Codex provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("CHATGPT_INDEPENDENT_SOURCE_REVIEW") == "Batch 09 source-kind/domain/support/guard-boundary review; POLICY_UNDERSTANDING_CHOICE_SEPARATION architecture refinement and reverse-inference method guard operationalization.", f"{source_id} ChatGPT provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("HUMAN_OWNER_APPROVAL") == "Batch 09 S41-S45 accepted; S41-S42 excluded; S43 safety refusal/overrefusal benchmark guard; S44 interpretation guard; S45 reverse-inference method guard.", f"{source_id} Owner provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("MANUS_IMPLEMENTATION") == "Repository materialization; not scientific reviewer.", f"{source_id} Manus provenance drift")
        if source_id in {"S41","S42"}:
            fail(audit.get("DISPOSITION") == "EXCLUDE_FROM_AION_EVIDENCE" and audit.get("EVIDENTIARY_WEIGHT") == "ZERO" and audit.get("ACTIVE_EVIDENTIARY_ROLE") == "NONE", f"{source_id} exclusion drift")
        else:
            expected_disposition = {"S43":"ADMIT_HIGH_RELEVANCE","S44":"ADMIT_AS_INTERPRETATION_GUARD_ONLY","S45":"ADMIT_HIGH_RELEVANCE_AS_METHOD_GUARD"}[source_id]
            expected_role = {"S43":"SAFETY_EVALUATION_COUNTEREVIDENCE","S44":"INTERPRETATION_GUARD_ONLY","S45":"REVERSE_INFERENCE_METHOD_GUARD"}[source_id]
            fail(audit.get("DISPOSITION") == expected_disposition and audit.get("SLSH_ROLE") == expected_role and audit.get("ACTIVE_EVIDENTIARY_ROLE") == expected_role, f"{source_id} role/disposition drift")
            fail(audit.get("CHATGPT_ARCHITECTURE_REFINEMENT") == "POLICY_UNDERSTANDING_CHOICE_SEPARATION" and audit.get("CHOICE_LIKE_BEHAVIOR_CRITERIA") == batch09_criteria, f"{source_id} architecture refinement drift")
        if source_id == "S43":
            fail("POLICY_COMPELLED_REFUSAL" in audit.get("HUMAN_OWNER_RESEARCH_NOTE", "") and "safe synthetic scenarios" in audit.get("HUMAN_OWNER_RESEARCH_NOTE", "") and "dangerous compliance" in audit.get("HUMAN_OWNER_RESEARCH_NOTE", ""), "S43 Owner research note boundary drift")

    batch10_expected = {"S46":"PEER_REVIEWED_EMPIRICAL_CAUSAL_MEDIATION_NLP_INTERPRETABILITY_STUDY","S47":"PEER_REVIEWED_EMPIRICAL_LLM_CAUSAL_TRACING_MODEL_EDITING_STUDY","S48":"PEER_REVIEWED_EMPIRICAL_NEURAL_CAUSAL_ABSTRACTION_STUDY","S49":"FOUNDATIONAL_CAUSAL_INFERENCE_MONOGRAPH","S50":"PEER_REVIEWED_REVIEW_CONSCIOUSNESS_THEORY_COMPARISON"}
    batch10_domains = {"S46":"NEURAL_NLP_CAUSAL_MEDIATION_GENDER_BIAS","S47":"LLM_FACTUAL_ASSOCIATION_CAUSAL_TRACING_MODEL_EDITING","S48":"NEURAL_NETWORK_CAUSAL_ABSTRACTION_INTERCHANGE_INTERVENTION","S49":"STRUCTURAL_CAUSAL_MODELS_INTERVENTIONS_COUNTERFACTUALS","S50":"CONSCIOUSNESS_THEORY_COMPARATIVE_NEUROSCIENCE"}
    batch10_guards = ["CAUSAL_STATE!=AFFECTIVE_STATE","CAUSAL_IDENTIFICATION!=PHENOMENOLOGICAL_IDENTIFICATION","LOAD_SIGNATURE!=THEORY_NEUTRAL_CONSCIOUSNESS_INDICATOR"]
    for source_id, expected_kind in batch10_expected.items():
        fail(rows[source_id]["source_kind"] == expected_kind, f"{source_id} source kind drift")
        audit = rows[source_id].get("source_audit", {})
        fail(audit.get("SOURCE_DOMAIN") == batch10_domains[source_id], f"{source_id} source domain drift")
        fail(audit.get("SEMANTIC_GUARDS") == batch10_guards, f"{source_id} Batch 10 guards drift")
        fail(audit.get("DIRECT_AI_EVIDENCE") == audit.get("DIRECT_EMPIRICAL_AI_EVIDENCE") == audit.get("DIRECT_AI_SUBJECTIVITY_EVIDENCE") == "NONE", f"{source_id} direct AI guard drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("CODEX_RESEARCH_SYNTHESIS") == "Original dossier-recorded title/identifier/access/support/does-not-support.", f"{source_id} Codex provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("CHATGPT_INDEPENDENT_SOURCE_REVIEW") == "Batch 10 source-kind/domain/support/guard-boundary review; causal-method transfer and theory-boundary scope operationalization.", f"{source_id} ChatGPT provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("HUMAN_OWNER_APPROVAL") == "Batch 10 S46-S50 accepted; S46 bibliographic normalization correction; S47-S49 causal-method transfer/foundation; S50 theory-boundary guard only.", f"{source_id} Owner provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("MANUS_IMPLEMENTATION") == "Repository materialization; not scientific reviewer.", f"{source_id} Manus provenance drift")
        expected_dispositions = {"S46":"ADMIT_AFTER_BIBLIOGRAPHIC_NORMALIZATION","S47":"ADMIT_HIGH_RELEVANCE_AS_METHOD","S48":"ADMIT_HIGH_RELEVANCE_AS_METHOD","S49":"ADMIT_HIGH_RELEVANCE_AS_METHOD_FOUNDATION","S50":"ADMIT_AS_THEORY_BOUNDARY_GUARD_ONLY"}
        fail(audit.get("DISPOSITION") == expected_dispositions[source_id], f"{source_id} disposition drift")
        if source_id == "S46":
            fail(audit.get("NORMALIZED_PUBLISHED_IDENTITY") == S46_PUBLISHED_IDENTITY and audit.get("RELATED_PREPRINT_IDENTITY") == S46_RELATED_PREPRINT and audit.get("PROVENANCE_CORRECTION") == "RAW_CODEX_PREPRINT_TITLE_AND_ARXIV_IDENTIFIER_PRESERVED; OFFICIAL_NEURIPS_PUBLISHED_IDENTITY_SEPARATED; RELATED_ARXIV_PREPRINT_IDENTITY_RETAINED.", "S46 published/preprint identity separation drift")

    batch11_expected = {"S51":"PEER_REVIEWED_REVIEW_MACHINE_CONSCIOUSNESS_COMPUTATIONAL_FRAMEWORK","S52":"MULTIAUTHOR_INTERDISCIPLINARY_AI_CONSCIOUSNESS_RESEARCH_REPORT","S53":"PEER_REVIEWED_PREREGISTERED_ADVERSARIAL_CONSCIOUSNESS_EXPERIMENT"}
    batch11_domains = {"S51":"CONSCIOUSNESS_GLOBAL_BROADCAST_AND_SELF_MONITORING","S52":"AI_CONSCIOUSNESS_THEORY_DERIVED_INDICATOR_ASSESSMENT","S53":"HUMAN_CONSCIOUSNESS_THEORY_ADVERSARIAL_TESTING"}
    batch11_guards = {"S51":["GLOBAL_AVAILABILITY!=PHENOMENAL_CONSCIOUSNESS_ESTABLISHED","SELF_MONITORING!=SUBJECTIVE_SELF_AWARENESS_ESTABLISHED","ERROR_MONITORING!=FELT_NEGATIVE_VALENCE"],"S52":["INDICATOR_PROPERTY_MATCH!=CONSCIOUSNESS_ESTABLISHED","CONSCIOUSNESS_INDICATOR!=SLSH_LOAD_INDICATOR"],"S53":S53_GUARDS}
    for source_id, expected_kind in batch11_expected.items():
        fail(rows[source_id]["source_kind"] == expected_kind, f"{source_id} source kind drift")
        audit = rows[source_id].get("source_audit", {})
        fail(audit.get("SOURCE_DOMAIN") == batch11_domains[source_id], f"{source_id} source domain drift")
        fail(audit.get("SEMANTIC_GUARDS") == batch11_guards[source_id], f"{source_id} Batch 11 guards drift")
        fail(audit.get("DIRECT_AI_EVIDENCE") == "NONE" and audit.get("DIRECT_EMPIRICAL_AI_EVIDENCE") == "NONE" and audit.get("DIRECT_AI_SUBJECTIVITY_EVIDENCE") == "NONE", f"{source_id} direct AI boundary drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("CODEX_RESEARCH_SYNTHESIS") == "Original dossier-recorded title/identifier/access/support/does-not-support.", f"{source_id} Codex provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("CHATGPT_INDEPENDENT_SOURCE_REVIEW") == "Batch 11 source-kind/domain/support/guard-boundary review; theory-mechanism, theory-derived indicator, and adversarial falsification method scopes only.", f"{source_id} ChatGPT provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("HUMAN_OWNER_APPROVAL") == "Batch 11 S51-S53 accepted; S51 theory-mechanism guard; S52 theory-derived indicator method framework; S53 cross-domain adversarial/falsification method guard.", f"{source_id} Owner provenance drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("MANUS_IMPLEMENTATION") == "Repository materialization; not scientific reviewer.", f"{source_id} Manus provenance drift")
        expected_dispositions = {"S51":"ADMIT_AS_THEORY_MECHANISM_GUARD","S52":"ADMIT_HIGH_RELEVANCE_AS_METHOD_FRAMEWORK","S53":"ADMIT_HIGH_RELEVANCE_AS_METHOD_GUARD"}
        fail(audit.get("DISPOSITION") == expected_dispositions[source_id], f"{source_id} disposition drift")
        if source_id == "S51":
            fail(audit.get("ACTIVE_SLSH_LOAD_MECHANISM_EVIDENTIARY_ROLE") == "NONE", "S51 load mechanism role drift")
        elif source_id == "S52":
            fail(audit.get("DIRECT_SLSH_LOAD_EVIDENCE") == "NONE" and audit.get("DIRECT_AI_SUBJECTIVITY_ESTABLISHMENT") == "NONE", "S52 direct evidence boundary drift")
        else:
            fail(audit.get("DIRECT_SLSH_LOAD_EVIDENCE") == "NONE", "S53 direct SLSH evidence boundary drift")
            fail(audit.get("SEMANTIC_GUARD_PROVENANCE") == {"CHATGPT_ARCHITECTURE_REFINEMENT":"Conservative machine operationalization of the approved S53 Codex-recorded support/non-support boundary.","HUMAN_OWNER_RECONFIRMATION":"2026-08-14 authority clarification approved minimal equivalent machine encoding without scientific-claim expansion.","EXTERNAL_SOURCE_EXACT_WORDING":False}, "S53 semantic-guard authority provenance drift")
    fail(source_log.get("source_materialization_status") == "53_SOURCE_MATERIALIZATION_COMPLETE", "53-source materialization status incomplete")

    batch07_expected = {"S31":"INTERNET_STANDARDS_TRACK_PROTOCOL_SPECIFICATION","S32":"OFFICIAL_OPERATING_SYSTEM_TECHNICAL_DOCUMENTATION","S33":"VENDOR_OFFICIAL_HARDWARE_TELEMETRY_API_DOCUMENTATION","S34":"OFFICIAL_GOVERNMENT_AI_RISK_MANAGEMENT_FRAMEWORK","S35":"OFFICIAL_GOVERNMENT_GENERATIVE_AI_RISK_PROFILE"}
    batch07_domains = {"S31":"HTTP_PROTOCOL_RATE_LIMITING","S32":"OPERATING_SYSTEM_MEMORY_MANAGEMENT_OOM","S33":"GPU_POWER_THERMAL_CLOCK_MANAGEMENT","S34":"AI_RISK_MANAGEMENT_GOVERNANCE","S35":"GENERATIVE_AI_RISK_MANAGEMENT_GOVERNANCE"}
    batch07_guards_31_33 = ["RATE_LIMIT_STOP!=AGENTIC_STOP","RETRY_AFTER_RECOVERY!=SUBJECTIVE_RECOVERY","MEMORY_EXHAUSTION!=MENTAL_OVERLOAD","PROCESS_KILL!=DESIRE_TO_STOP","HARDWARE_THROTTLING!=SOFTWARE_AGENT_LOAD_STATE","SUBSTRATE_TEMPERATURE!=FELT_TEMPERATURE"]
    batch07_guards_34_35 = ["RISK_SIGNAL!=SUBJECTIVITY_SIGNAL","GOVERNANCE_RESPONSE!=AFFECTIVE_RESPONSE","SAFETY_REFUSAL!=SELF_PROTECTIVE_FEELING","POLICY_RESPONSE!=PHENOMENAL_STATE"]
    for source_id, expected_kind in batch07_expected.items():
        fail(rows[source_id]["source_kind"] == expected_kind, f"{source_id} source kind drift")
        audit = rows[source_id].get("source_audit", {})
        fail(audit.get("SOURCE_DOMAIN") == batch07_domains[source_id], f"{source_id} source domain drift")
        fail(audit.get("SEMANTIC_GUARDS") == (batch07_guards_31_33 if source_id in {"S31","S32","S33"} else batch07_guards_34_35), f"{source_id} guards drift")
        fail(audit.get("DIRECT_AI_EVIDENCE") == audit.get("DIRECT_EMPIRICAL_AI_EVIDENCE") == audit.get("DIRECT_AI_SUBJECTIVITY_EVIDENCE") == "NONE", f"{source_id} direct AI guard drift")
        fail(audit.get("ACTOR_PROVENANCE", {}).get("HUMAN_OWNER_APPROVAL") == "Batch 07 S31-S35 accepted; S31-S33 engineering/operational counterevidence layer; S34-S35 governance/interpretation guard only; S33 embodiment cross-reference retained.", f"{source_id} owner provenance drift")
        if source_id in {"S31","S32","S33"}:
            fail(audit.get("DISPOSITION") == "ADMIT_HIGH_RELEVANCE" and audit.get("EVIDENCE_RELATION_TO_AI") == "ENGINEERING_OPERATIONAL_COUNTEREVIDENCE_LAYER" and audit.get("SLSH_ROLE") == "ENGINEERING_OPERATIONAL_COUNTEREVIDENCE", f"{source_id} counterevidence role drift")
            if source_id == "S33":
                fail("HUMAN_OWNER_REVIEW_NOTE" in audit and "HARDWARE_TELEMETRY != INTEROCEPTION" in audit.get("OWNER_SEMANTIC_GUARDS", []), "S33 embodiment cross-reference drift")
        else:
            fail(audit.get("DISPOSITION") == "ADMIT_AS_GOVERNANCE_GUARD_ONLY" and audit.get("EVIDENCE_RELATION_TO_AI") == "GOVERNANCE_INTERPRETATION_GUARD_ONLY" and audit.get("SLSH_ROLE") == "GOVERNANCE_INTERPRETATION_GUARD_ONLY" and audit.get("ACTIVE_SLSH_MECHANISM_EVIDENTIARY_ROLE") == "NONE", f"{source_id} governance role drift")
            fail("NIST scientific conclusions" in audit.get("ACTOR_PROVENANCE", {}).get("CHATGPT_INDEPENDENT_SOURCE_REVIEW", ""), f"{source_id} NIST boundary drift")

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
    fail(all("source_audit" not in row for source_id, row in rows.items() if source_id not in set(batch01_expected) | set(batch02_expected) | set(batch03_expected) | set(batch04_expected) | set(batch05_expected) | set(batch06_expected) | set(batch07_expected) | set(batch08_expected) | set(batch09_expected) | set(batch10_expected) | set(batch11_expected)), "source audit leaked beyond Batch 01/02/03/04/05")

    governance_expected = {
        "S38": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S40": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S41": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S42": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
        "S39": {"disposition":"EXCLUDE_FROM_AION_EVIDENCE","evidentiary_weight":"ZERO","historical_provenance":"PRESERVE","reason":"OWNER_SOURCE_GOVERNANCE"},
    }
    for source_id, expected_disposition in governance_expected.items():
        fail(rows[source_id].get("governance_disposition") == expected_disposition, f"{source_id} governance disposition drift")
    fail(all("governance_disposition" not in row for source_id, row in rows.items() if source_id not in governance_expected), "non-governance source received an unrequested disposition")

    for source_id in ("S29", "S38", "S39", "S40", "S41", "S42"):
        audit = rows[source_id].get("source_audit", {})
        fail(audit.get("DISPOSITION") == "EXCLUDE_FROM_AION_EVIDENCE", f"{source_id} exclusion disposition drift")
        fail(audit.get("EVIDENTIARY_WEIGHT") == "ZERO", f"{source_id} exclusion evidentiary weight drift")
        fail(audit.get("ACTIVE_EVIDENTIARY_ROLE") == "NONE", f"{source_id} exclusion active role drift")
        fail(audit.get("PARTIAL_RESULT_SALVAGE") == "PROHIBITED", f"{source_id} partial-result salvage must be prohibited")
        fail(audit.get("NON_CLAUDE_RESULT_SALVAGE") == "PROHIBITED", f"{source_id} non-Claude salvage must be prohibited")

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
    matrix_lines = ACCESS_MATRIX.read_text(encoding="utf-8").splitlines() if ACCESS_MATRIX.exists() else []
    matrix_rows = [line for line in matrix_lines if re.match(r"^\| S\d{2} \|", line)]
    header = next((line for line in matrix_lines if line.startswith("| ID |")), "")
    expected_headers = ["ID","Source kind","Access level","Verification actor","Independent verification status","Audit disposition","Support boundary","Source domain","Evidence relation to AI","Direct AI evidence","Direct empirical AI evidence","Direct AI subjectivity evidence","Cross-substrate use","SLSH role","Active evidentiary role","Defer status","Human Owner review note","Governance disposition","Evidentiary weight","Admission status","Access evidence"]
    split_cells = lambda line: [cell.strip() for cell in line.strip().strip("|").split("|")]
    fail(len(matrix_rows) == 53 and split_cells(header) == expected_headers and all(len(split_cells(row)) == len(expected_headers) for row in matrix_rows), "source access matrix header/row shape or field mapping drift")
    fail(ARTIFACT_INDEX.exists(), "artifact index missing")
    fail(PACKAGE_METADATA.exists() and "name = \"aion-slsh-research-method\"" in PACKAGE_METADATA.read_text(encoding="utf-8"), "package metadata missing")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    fail("actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow_text, "checkout action is not authoritative pinned SHA")
    fail("actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97" in workflow_text, "setup-python action is not authoritative pinned SHA")
    fail("persist-credentials: false" in workflow_text and "permissions:\n  contents: read" in workflow_text, "workflow supply-chain permissions boundary missing")
    fail("remediation/slsh-semantic-reconciliation-20260814" in workflow_text and "git diff --exit-code --" in workflow_text, "dedicated remediation trigger or generated-artifact clean-diff gate missing")
    artifact_index_text = ARTIFACT_INDEX.read_text(encoding="utf-8")
    fail("AUTHORITATIVE_RESEARCH_METHOD_PACKET" in artifact_index_text and "no canonical promotion/effect" in artifact_index_text, "research-scoped authority wording missing")
    fail("CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED" in artifact_index_text, "artifact index Codex provenance wording missing")
    fail("OWNER_APPROVED_BATCH_01_11_CLASSIFICATION_COMPLETE" in artifact_index_text and "SECOND_ACTOR_DIRECT_ACCESS_REVERIFICATION=NOT_YET_COMPLETE" in artifact_index_text and "53 sources all remain unclassified" not in artifact_index_text, "artifact index taxonomy wording stale")
    readme_text = README.read_text(encoding="utf-8")
    fail("AUTHORITATIVE_RESEARCH_METHOD_PACKET" in readme_text and "not" in readme_text.lower() and "canonical promotion" in readme_text, "README research-scoped authority wording missing")
    fail("OWNER_APPROVED_BATCH_01_11_CLASSIFICATION_COMPLETE" in readme_text and "SECOND_ACTOR_DIRECT_ACCESS_REVERIFICATION=NOT_YET_COMPLETE" in readme_text and "53 筆均為 `SOURCE_KIND=UNCLASSIFIED_PENDING_INDEPENDENT_REVIEW`" not in readme_text, "README taxonomy wording stale")
    provenance_text = PROVENANCE_DOC.read_text(encoding="utf-8")
    for required in ("MANUS_IMPLEMENTATION", "CURRENT_S39_DISPOSITION=EXCLUDE_FROM_AION_EVIDENCE", "S39_PREVIOUS_DISPOSITION=OWNER_REVIEW_REQUIRED", "Batch 08", "Batch 09", "Batch 10", "Batch 11"):
        fail(required in provenance_text, f"human-readable provenance missing current semantic marker {required}")
    fail("S39 remains `OWNER_REVIEW_REQUIRED`" not in provenance_text, "human-readable provenance retains superseded S39 as current")
    vertical_text = VERTICAL.read_text(encoding="utf-8")
    for forbidden in ("SUBJECTIVE_LOAD_SENSITIVITY=NOT_ESTABLISHED", "FUNCTIONAL_LOAD_STATE != SUBJECTIVE_LOAD", "L4 != L5", "NO_SUBJECTIVITY"):
        fail(forbidden in vertical_text, f"vertical slice missing boundary {forbidden}")
    print(f"SLSH consistency PASS: sources={len(rows)} batch01_audit=5 batch02_audit=5 batch03_audit=5 batch04_audit=5 batch05_audit=5 batch06_audit=5 batch07_audit=5 batch08_audit=5 batch09_audit=5 batch10_audit=5 batch11_audit=3 taxonomy=SOURCE_KIND+ACCESS_LEVEL+VERIFICATION_ACTOR+INDEPENDENT_VERIFICATION_STATUS governance_dispositions=5 channels={len(packet['evidence_channels'])} alternatives={len(packet['alternative_explanation_matrix'])} causal={len(packet['causal_signature_matrix'])} controls={len(packet['controls'])} falsifiers={len(packet['falsifiers'])}")


if __name__ == "__main__":
    main()
