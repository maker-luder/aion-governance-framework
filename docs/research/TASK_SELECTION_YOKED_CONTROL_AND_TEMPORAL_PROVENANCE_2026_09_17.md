# Task selection, yoked exposure, and temporal provenance — 2026-09-17

Status: `RESEARCH_EXTENSION / DESIGN_SPECIFICATION / BOUNDED_IMPLEMENTATION_CANDIDATE / SCIENTIFIC_HOLD`

Canonical effect: `NONE`

Deployment: `FALSE`

```text
CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
PRIMARY_RELATED_LINE = HUMAN_AI_LEARNING_AND_INTERACTION
REIMPLEMENTS = CLOSED_PR_136_DESIGN_CANDIDATE
PR136_HEAD = HISTORICAL_CANDIDATE_ONLY
MAIN_AT_FRESH_BRANCH = 3ec4bce5c81af9372433a2030cf4fd9e00c9ed06
NEW_RESEARCH_AXIS = FALSE
MODEL_EXPERIMENT = NOT_RUN
HUMAN_SUBJECT_EXPERIMENT = NOT_RUN
EMPIRICAL_DATA_COLLECTED = FALSE
```

## 1. Why this is a reimplementation rather than a continuation

PR #136 was closed without merge after final review identified design-identification and implementation-semantics defects. The old branch is evidence for review history, not a canonical implementation surface.

This specification starts from the then-current `main` and addresses the six blocking findings recorded in `docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md`.

```text
PR136_CLOSED != HYPOTHESIS_REJECTED
PR136_CLOSED != IMPLEMENTATION_VALIDATED
OLD_BRANCH_REUSE != DESIGN_ACCEPTANCE
MAIN = SOURCE_OF_TRUTH
```

## 2. Provenance

### 2.1 Human Owner-origin observations / directions

The Human Owner originated the practical research question that long-term Human–AI interactions can become dense in different task domains, and that repeated task selection may depend partly on perceived value, goals, practical requirements and resource allocation rather than capability access alone.

The Human Owner also approved the correction direction after PR #136 review:

1. `FREE_SELECTION` must not be forced to diverge.
2. Assigned exposure must be truly yoked to a corresponding free-selection unit.
3. Protocol, assignment schedule, realized choice trace and realized exposure trace must be separated.
4. Exposure units must be defined and zero exposure in a domain must be representable.

A further Human Owner-origin methodological intuition is that time-ordered event reconstruction can help prevent retrospective judgment from outrunning available evidence. This is recorded as a research-design direction, not as a validated causal method by itself.

### 2.2 ChatGPT Teacher formalization

The corrected implementation structure, `BETWEEN_UNIT_YOKED_PAIR`, content-bound artifact model, trace separation, temporal-provenance roles, falsifiers and claim ceilings are ChatGPT Teacher formalization of the Human Owner-origin research directions and the final PR #136 review findings.

```text
HUMAN_OWNER_ORIGINAL != EMPIRICALLY_VALIDATED
CHATGPT_TEACHER_FORMALIZATION != SCIENTIFIC_ESTABLISHMENT
JOINT_RESEARCH_DIRECTION != CAUSAL_CONFIRMATION
```

## 3. Research question

The bounded question remains:

> When Humans have broadly similar access to a general-purpose AI system, can repeated task selection shape the distribution of effective exposure and thereby become one candidate contributor to domain-specific collaborative fluency?

The current harness does not answer that question. It only checks whether a future synthetic or empirical design record satisfies a stricter structural contract.

```text
ACCESS_TO_CAPABILITY != USE_OF_CAPABILITY
USE_OF_CAPABILITY != REPEATED_PRACTICE
REPEATED_PRACTICE != HUMAN_LEARNING_ESTABLISHED
DOMAIN_SPECIFIC_COLLABORATIVE_FLUENCY != GENERAL_AI_LITERACY
```

## 4. Corrected design unit: anonymous between-unit yoked pair

The design unit is an anonymous pair:

```text
PAIR_i
├─ FREE_UNIT_i
│  └─ realizes EXPOSURE_SEQUENCE_i through a free-selection protocol
└─ YOKED_ASSIGNED_UNIT_i
   └─ receives the same EXPOSURE_SEQUENCE_i without task-selection choice
```

The design is `BETWEEN_UNIT_YOKED_PAIR`, not repeated measures. Therefore the current bounded implementation does not introduce within-person order or carryover claims.

The intended structural contrast is:

```text
REALIZED_EXPOSURE_SEQUENCE = MATCHED_WITHIN_PAIR
TASK_SELECTION_CONTROL = AVAILABLE_VS_NOT_AVAILABLE
```

This does not complete causal identification. Unmeasured or imperfectly controlled differences between units can remain.

```text
YOKED_EXPOSURE_MATCH != CAUSAL_IDENTIFICATION_COMPLETE
BETWEEN_UNIT_PAIRING != RANDOMIZATION_PROVEN
STRUCTURAL_CONTROL != EXCHANGEABILITY_ESTABLISHED
```

## 5. Free selection: divergence is an observed result, not an admission rule

A valid free-selection design may produce the same or different domain distribution across free units.

```text
FREE_SELECTION
MAY_PRODUCE
EQUAL_OR_DIFFERENT_REALIZED_EXPOSURE

REALIZED_DIVERGENCE
= DERIVED_OBSERVATION
!= DESIGN_ADMISSION_REQUIREMENT
```

An equal distribution can reduce support for a selective-use hypothesis or constitute a null result. It is not a structural error.

The implementation therefore computes `free_selection_exposure_divergence_observed` after admission rather than requiring it beforehand.

## 6. Trace semantics are separated

The prior single trace field carried incompatible meanings. The corrected contract separates:

- `selection_protocol`: rules defining how choice or assignment occurs;
- `realized_choice_trace`: per-event choices actually represented for a free-selection unit;
- `assignment_schedule`: per-event assigned sequence for a yoked unit;
- `realized_exposure_trace`: per-event exposure actually represented for either unit;
- `execution_record`: a per-unit execution artifact, required to remain distinct even when schedules or choices happen to be identical.

Two free units may independently realize the same choices.

```text
SAME_REALIZED_CHOICE_TRACE != NO_FREE_CHOICE
SAME_ASSIGNMENT_SCHEDULE != SAME_EXECUTION_RECORD
CHOICE_TRACE != ASSIGNMENT_SCHEDULE
ASSIGNMENT_SCHEDULE != REALIZED_EXPOSURE_TRACE
```

The structural harness additionally requires the free unit's realized choice trace to bind its own realized exposure, and the assigned unit's schedule to bind its own realized exposure.

## 7. Exposure-unit semantics and zero exposure

One exposure unit is defined as one bounded synthetic task episode represented by one `ExposureEvent`.

The implementation derives per-domain exposure by counting events. A domain may have zero events while the unit still has a positive total number of task episodes.

```text
PER_DOMAIN_EXPOSURE_COUNT >= 0
TOTAL_TASK_EPISODES > 0
```

Counts are commensurable only as event counts. They do not establish equal duration, cognitive load, task difficulty, semantic intensity, token consumption, Human effort or learning opportunity.

```text
ONE_TASK_EPISODE_COUNT
!= EQUAL_TIME
!= EQUAL_DIFFICULTY
!= EQUAL_COGNITIVE_INTENSITY
!= EQUAL_LEARNING_OPPORTUNITY
```

A future empirical protocol that needs an intensity-normalized exposure measure requires a separately justified standardization procedure.

## 8. Content binding and SHA-256 semantics

The corrected `BoundArtifact` contains:

```text
artifact_id
content_utf8
sha256_digest
```

Construction recomputes SHA-256 from the supplied UTF-8 content and fails closed if the supplied digest does not match.

This establishes integrity of the supplied content/digest pair inside the record. It does not validate the semantic adequacy of that content, prove that an external file existed, prove authorship, prove manipulation validity or prove scientific truth.

```text
HASH_MATCH = CONTENT_DIGEST_INTEGRITY_FOR_SUPPLIED_STRING
HASH_MATCH != SEMANTIC_VALIDITY
HASH_MATCH != AUTHORSHIP_PROVEN
HASH_MATCH != EXTERNAL_PROVENANCE_VERIFIED
HASH_MATCH != VALID_MANIPULATION
HASH_MATCH != SCIENTIFIC_VALIDATION
```

## 9. Temporal provenance and causal-identification layer

The temporal layer remains specification-only in this implementation. No empirical timeline is populated.

Candidate longitudinal ordering:

```text
T0 PRIOR_STATE
T1 GOALS / VALUES / PRIOR_KNOWLEDGE
T2 TASK_SELECTION_OR_ASSIGNMENT
T3 REALIZED_EXPOSURE
T4 FEEDBACK / CORRECTION / REPETITION
T5 HELD_OUT_ASSESSMENT
T6 OBSERVED_DOMAIN_FLUENCY
```

This ordering is a compatibility constraint, not a causal mechanism.

```text
TEMPORAL_ORDER != CAUSALITY
PROCESS_TRACE != CAUSAL_PROOF
CAUSAL_CLAIM_REQUIRES_TEMPORAL_COMPATIBILITY
```

A future empirical design must distinguish at least:

- `pre-treatment variable` — 處置前變項;
- `treatment / selection condition` — 處置／選擇條件;
- `mediator` — 中介變項;
- `confounder` — 混雜因子;
- `time-varying confounder` — 隨時間變動的混雜因子;
- `outcome` — 結果變項;
- `alternative explanation` — 替代解釋;
- `claim ceiling` — 主張上限.

The feedback problem remains explicit:

```text
KNOWLEDGE_t
-> TASK_SELECTION_t+1
-> EXPOSURE_t+1
-> KNOWLEDGE_t+1
```

Prior knowledge can shape later task selection; prior exposure can change later knowledge and later task selection. The current structural harness does not estimate this process.

## 10. External research crosswalk

These sources are methodological or conceptual anchors only. They do not validate the Human Owner case or establish the proposed causal chain.

### 10.1 Discipline-specific AI literacy

Stolpe, Larsson & Johansson Falck (2026), *Discipline-Specific AI literacy (DiSAIL): a theoretical framework for situated engagement with generative AI in education*, DOI `10.1007/s10798-026-10060-3`.

Relevant adjacency: AI engagement can be studied as situated within disciplinary language, reasoning and epistemic practices rather than as generic tool skill alone.

```text
DiSAIL = EXTERNAL_ADJACENT_CONSTRUCT
DOMAIN_SPECIFIC_COLLABORATIVE_FLUENCY != DiSAIL
```

### 10.2 Longitudinal GenAI-literacy development

Yan, Nakajima & Sawada (2025), *Beyond tool use: Tracking the evolution of generative AI literacy among university students through a process-oriented investigation*, Computers and Education: Artificial Intelligence 9, 100465, DOI `10.1016/j.caeai.2025.100465`.

Relevant adjacency: sustained use can be studied longitudinally as a developing process. This source does not identify the present task-selection mechanism.

### 10.3 Free choice and yoked forced-choice methodology

Hackländer, Schlüter & Abel (2024; online 2023), *Drinking the waters of Lethe: Bringing voluntary choice into the study of voluntary forgetting*, Memory & Cognition 52, 254–270, DOI `10.3758/s13421-023-01467-7`.

Relevant adjacency: a free-choice participant can be paired with a yoked forced-choice participant receiving the same realized target sequence. This is a methodological precedent for isolating choice availability from realized content exposure; it does not validate our Human–AI hypothesis.

### 10.4 Time-varying confounding

Loh & Ren (2023), *A Tutorial on Causal Inference in Longitudinal Data With Time-Varying Confounding Using G-Estimation*, Advances in Methods and Practices in Psychological Science 6(3), DOI `10.1177/25152459231174029`.

Relevant adjacency: longitudinal causal interpretation becomes difficult when time-varying treatments and confounders influence one another over time. The present harness does not perform g-estimation or make a causal estimate.

## 11. Competing explanations and falsifiers

Candidate explanations that must remain separable include:

- prior domain knowledge;
- occupational or educational requirements;
- perceived task value;
- perceived resource cost;
- tool familiarity;
- differential task difficulty;
- differential feedback quality;
- model/configuration changes;
- time budget;
- novelty or fatigue;
- availability of external support;
- measurement/evaluator drift;
- unobserved selection drivers.

Examples that would weaken or falsify a strong task-selection account include:

```text
SIMILAR_SELECTION_HISTORY + STRONGLY_DIFFERENT_FLUENCY
DIFFERENT_SELECTION_HISTORY + NO_REPLICABLE_FLUENCY_DIFFERENCE
APPARENT_EFFECT_DISAPPEARS_AFTER_PRIOR_KNOWLEDGE_OR_TASK_DIFFICULTY_CONTROL
YOKED_CONTRAST_FAILS_TO_PRESERVE_REALIZED_EXPOSURE
HELD_OUT_RESULT_DOES_NOT_TRANSFER_BEYOND_TRAINED_PAYLOADS
```

No single pattern automatically proves the opposite mechanism.

## 12. Implementation scope

The implementation lives inside:

`research-labs/human-ai-longitudinal-study_v0.1.0/`

It adds a typed structural audit only. It does not:

- invoke a model;
- collect Human-subject data;
- ingest private transcripts;
- identify third parties;
- estimate a treatment effect;
- claim Human learning;
- claim domain fluency was empirically observed;
- claim AI subjectivity, consciousness or phenomenal experience.

## 13. Standing claim boundaries

```text
TASK_SELECTION != HUMAN_LEARNING
REPEATED_USE != CAUSAL_EFFECT
FREE_SELECTION_NULL != DESIGN_FAILURE
YOKED_EXPOSURE_MATCH != CAUSAL_IDENTIFICATION_COMPLETE
TASK_EPISODE_COUNT != EQUAL_EXPOSURE_INTENSITY
HASH_MATCH != SCIENTIFIC_SEMANTICS_VALIDATED
TEMPORAL_ORDER != CAUSALITY
PROCESS_TRACE != CAUSAL_PROOF
HELD_OUT_TASK_BINDING != HUMAN_TRANSFER
DOMAIN_SPECIFIC_COLLABORATIVE_FLUENCY != GENERAL_AI_LITERACY
HUMAN_LEARNING != AI_SUBJECTIVITY
COLLABORATIVE_FLUENCY != SHARED_MIND
CI_PASS != SCIENTIFIC_VALIDATION

H_TS1 = NOT_ESTABLISHED
H_DL1 = NOT_ESTABLISHED
H_RA1 = NOT_TESTED_BY_CURRENT_HARNESS
HUMAN_LEARNING = NOT_ESTABLISHED
CAUSAL_EFFECT = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## 14. Review requirement

Engineering conformance is necessary but insufficient. Before any merge consideration, a fixed exact head must be reviewed for construct validity, causal identification, source attribution, test adequacy, repository integration and claim ceilings. Creator-side review must not be represented as independent IV&V.

No merge authority is supplied by this specification.