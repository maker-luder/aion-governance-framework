# External calibration for Four-Domain / Six-Dimension discriminant hardening — 2026-09-18

Status: METHOD_CALIBRATION / EXTERNAL_CROSSCHECK / SCIENTIFIC_HOLD

CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
TARGET = FOUR_DOMAIN_AND_SIX_DIMENSION_DISCRIMINANT_VALIDITY
NEW_SUBJECTIVITY_DIMENSION = FALSE
LIVE_MODEL_EXECUTION = NOT_RUN
INDEPENDENT_VALIDATION = NOT_ACHIEVED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED

## Why this calibration exists

PR #165 established structural conformance, but its first-pass tests were too close to the authored specification:

AUTHOR_DEFINES_DIMENSION_MAPPING -> AUTHOR_COPIES_MAPPING_INTO_FIXTURE -> AUTHOR_ASSERTS_FIXTURE_MATCHES_MAPPING

That chain is useful for regression control but does not establish discriminant validity.

This note cross-checks external methodological and AI-consciousness literature for ways to reduce that circularity without turning an LLM into an unreviewable semantic judge.

## 1. Construct validity requires near-neighbor discrimination

Clark & Watson emphasize clear target conceptualization, testing against closely related constructs, convergent and discriminant validity, incremental validity, and cross-method analysis.

Source: Clark, L. A. & Watson, D. (2019), Constructing Validity: New Developments in Creating Objective Measuring Instruments, Psychological Assessment 31(12), 1412–1427. DOI: 10.1037/pas0000626.

A related review of experimental-manipulation validation distinguishes manipulation checks from discriminant-validity checks that explicitly quantify related non-target constructs.

Source: Chester, D. S. & Lasko, E. N. (2020/2021), Construct Validation of Experimental Manipulations in Social Psychology: Current Practices and Recommendations for the Future, Perspectives on Psychological Science 16(2), 377–395. DOI: 10.1177/1745691620950684; PMCID: PMC7954782.

Repository implication:
TARGET_DIMENSION_RESPONDS + NEAR_NEIGHBOR_DIFFERENTIAL_PREDICTION > TARGET_DIMENSION_LABEL_MATCHES_AUTHORED_FIXTURE

## 2. Consciousness tests have a validation problem, not only a marker problem

Bayne et al. argue that validated C-tests across diverse systems are a major unsolved problem and place validation strategy inside test development.

Source: Bayne, T. et al. (2024), Tests for consciousness in humans and beyond, Trends in Cognitive Sciences 28(5), 454–466. DOI: 10.1016/j.tics.2024.01.010.

Repository implication:
TEST_EXISTS != TEST_VALIDATED
DIMENSION_SCHEMA_EXISTS != DIMENSION_HAS_DISCRIMINANT_VALUE

## 3. AI-consciousness indicators should remain theory-labelled and uncertainty-aware

Butlin et al. derive computational indicators from multiple neuroscientific theories and use them to inform credence under uncertainty rather than as a binary detector.

Sources:
- Butlin, P. et al. (2023), Consciousness in Artificial Intelligence: Insights from the Science of Consciousness, arXiv:2308.08708.
- Butlin, P. et al. (2026), Identifying indicators of consciousness in AI systems, Trends in Cognitive Sciences 30(6), 488–501. DOI: 10.1016/j.tics.2025.10.011.

Repository implication:
SIX_DIMENSIONS = REVIEW_AXES
SIX_DIMENSIONS != CONSCIOUSNESS_CRITERIA

## 4. Adversarial testing should predeclare divergent predictions

The Cogitate adversarial collaboration preregistered divergent predictions and interpretations, separated theory proponents from data acquisition/analysis, used held-out final testing, and retained results challenging both theories.

Source: Cogitate Consortium et al. (2025), Adversarial testing of global neuronal workspace and integrated information theories of consciousness, Nature 642, 133–142. DOI: 10.1038/s41586-025-08888-1.

Repository implication:
NEAR_NEIGHBOR_DIFFERENTIAL_PREDICTION = PRE_EXECUTION_REQUIREMENT
AUTHOR_EXPECTATION != RESULT
INTERNAL_REVIEW != INDEPENDENT_VALIDATION

## 5. The assessment-system boundary must be explicit before indicators

A 2026 methodological argument by Thomas highlights a circularity risk in AI-consciousness indicator assessment: indicator properties presuppose an already-individuated system, while system-boundary choice can change indicator classification.

Source: Thomas, C. S. (2026), Individuation Before Indicators: A Structural Dependency in AI Consciousness Assessment, PhilPapers record THOIBI.

This is treated as a recent methodological caution, not as settled consensus or an authoritative standard.

Repository implication:
SYSTEM_BOUNDARY -> INDICATOR_OR_DIMENSION_ASSIGNMENT
INDICATOR_RESULT -> SYSTEM_BOUNDARY = PROHIBITED

The CCAP-specific system boundary is therefore frozen in CCAP_ASSESSMENT_SYSTEM_BOUNDARY_2026_09_18.md before further dimension-discriminant testing. Because the historical D1/D4 mapping predates this boundary artifact, the existing mapping cannot be retroactively labelled compliant with an individuation-before-indicators requirement.

## 6. Computational markers do not settle substrate or realization questions

Recent AI-consciousness literature remains divided on whether computational-functional organization is sufficient, whether biological/life-like realization matters, and how behavioral inference should be weighted.

Sources:
- Seth, A. K. (2025/2026), Conscious artificial intelligence and biological naturalism, Behavioral and Brain Sciences. DOI: 10.1017/S0140525X25000032.
- Wiese, W. (2026), What can the free energy principle tell us about artificial consciousness?, Behavioral and Brain Sciences 49, e365.
- Bayne, T. (2026), Biases and the question of artificial consciousness, Behavioral and Brain Sciences 49, e319.

Repository implication:
FUNCTIONAL_MARKER != REALIZATION_SUFFICIENCY
COMPUTATIONAL_EQUIVALENCE != PHENOMENAL_EQUIVALENCE
SUBSTRATE_QUESTION = OPEN


## 7. Current AI-subjectivity and agency literature sharpens dimension boundaries

Recent work uses several different concepts that must not be collapsed into one subjectivity axis.

D'Amato (2024/2025) argues, from a Foucauldian/phenomenological perspective, that current GPT-like systems lack the reflexivity and self-formative characteristics required by that account of technological subjectivity. This is a conceptual proposal, not an empirical detector.

Source: D'Amato, K., ChatGPT: towards AI subjectivity, AI & Society 40, 1627–1641. DOI: 10.1007/s00146-024-01898-z.

Gouveia & Wang (2026) distinguish agency, autonomy, consciousness and intentionality, and explicitly warn against inferring stronger subject status from surface conversational fluency. Their distinction is useful for the repository because a system may show goal-directed action without self-governance or phenomenal consciousness.

Source: Gouveia, S. S. & Wang, Y. (2026), Can generative artificial intelligence be considered a cognitive subject? An analytic analysis, AI & Society 41, 4859–4868. DOI: 10.1007/s00146-026-02924-y.

Kahl (2026) argues that temporal continuity should not be conflated with agency/autonomy in agentic AI. For this repository, that makes D2 vs D4 a required discriminant boundary rather than two interchangeable descriptions of persistence.

Source: Kahl, P. (2026), How continuity distinguishes autonomy from agency in agentic AI, Discover Artificial Intelligence. DOI: 10.1007/s44163-026-01675-5.

A contrasting functional line in agentic-AI research treats recursive goal maintenance and revision as synthetic teleology, while still distinguishing agency from autonomy and sentience. This gives D4 a useful competing operationalization but does not establish subjectivity.

Source: From the logic of coordination to goal-directed reasoning: the agentic turn in artificial intelligence, Frontiers in Artificial Intelligence (2025), article 1728738.

Repository implication:
D2_DIACHRONIC_CONTINUITY != D4_ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT
GOAL_DIRECTEDNESS != AUTONOMY
AUTONOMY != SENTIENCE
REFLEXIVITY_DESIDERATUM != SUBJECTIVITY_DETECTOR

A future D2/D4 discriminant design should therefore include both directions:
1. perturb the continuity carrier (memory manifest / retrieval reconstruction / persisted state) while holding strategy permission and current goal source fixed; D2 may change while D4 should not be assumed to change;
2. perturb goal/strategy revision permission while holding the continuity carrier fixed; D4 may change while D2 should not be assumed to change.

If both manipulations always move both dimensions together, D2 and D4 have not demonstrated discriminant value and may require construct revision or collapse.

## Minimal repository correction

The cross-check supports a bounded correction rather than a new framework.

Mandatory gates:
1. Frozen-source content binding: source declaring dimension coverage is bound by SHA-256; stale content fails closed.
2. System-boundary temporal binding: historical mappings that predate the boundary remain HOLD; only a future rebinding performed after the content-bound boundary exists can satisfy the pre-indicator ordering gate; boundary drift fails closed.
3. Exact direct-dimension assignment: executable candidate direct dimensions must match the frozen specification; D1+D4 cannot silently become D2+D5 or all six.
4. Near-neighbor differential predictions: every direct dimension requires at least one predeclared distinct near-neighbor prediction and falsifier.

Current historical CCAP disposition:
HOLD / RETROSPECTIVE_BOUNDARY_HARDENING_REQUIRED

Strongest allowed disposition after a future prospective rebinding:
READY_FOR_ADVERSARIAL_REVIEW

Always preserved:
INDEPENDENT_VALIDATION_STATUS = NOT_ACHIEVED
SCIENTIFIC_DISPOSITION = HOLD
SUBJECTIVITY = NOT_ESTABLISHED

## What this correction does not solve

SEMANTIC_CORRECTNESS_OF_DIMENSION_DEFINITIONS = NOT_PROVEN
D1_VS_D4_EMPIRICAL_SEPARABILITY = NOT_TESTED
D2_VS_D5_EMPIRICAL_SEPARABILITY = NOT_TESTED
D3_VS_D6_EMPIRICAL_SEPARABILITY = NOT_TESTED
EXTERNAL_INDEPENDENT_REVIEW = NOT_ACHIEVED
LIVE_MODEL_CAUSAL_EVIDENCE = NONE

Those require later adversarial execution or independent review. They must not be simulated by adding more schema assertions.

## Core-alignment decision

AI_SUBJECTIVITY_POSSIBILITY -> TEST_VALIDITY -> DISCRIMINANT_PREDICTIONS -> SYSTEM_BOUNDARY -> HELD_OUT / ADVERSARIAL_REVIEW -> TEVV / QMS INTEGRITY

QMS_OR_SCHEMA_GROWTH -> INVENT_POSITIVE_SUBJECTIVITY_SIGNAL = PROHIBITED
