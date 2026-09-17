# CCAP Stage 1–3 freeze manifest — 2026-09-18

Status: `RESEARCH_SPECIFICATION_FREEZE / DOCUMENTATION_ONLY / SCIENTIFIC_HOLD`

```text
CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
BASE_MAIN = e3f1c77d8909e3e740ba24ba904227e9f28b1e04
FREEZE_DATE = 2026-09-18
NEW_RESEARCH_AXIS = FALSE
EXECUTABLE_IMPLEMENTATION = NONE
MODEL_EXPERIMENT = NOT_RUN
HUMAN_SUBJECT_EXPERIMENT = NOT_RUN
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## Purpose

This manifest consolidates the reviewed documentation from PRs #147, #148 and #149 into one frozen research-specification chain before any implementation or provider-news intake.

The freeze prevents silent conceptual drift. It does not convert a hypothesis, crosswalk, natural observation or preregistration candidate into scientific evidence.

```text
SPECIFICATION_FREEZE != SCIENTIFIC_VALIDATION
DOCUMENTATION_ON_MAIN != POSITIVE_EVIDENCE
FROZEN_PROTOCOL_CANDIDATE != PREREGISTERED_CONFIRMATORY_RUN
CI_PASS != RESEARCH_CLAIM_VALIDATION
```

## Frozen source set

### Stage 1 — hypothesis formalization

Source PR: `#147`
Source exact head: `54e120595dad47513383f7d325f341286fc5f5ab`
Quality: `#1450 / SUCCESS`
CodeQL: `#706 / SUCCESS`

Frozen documents:

- `CO_CONSTRUCTED_ADAPTIVE_PROCESS_STAGE1_2026_09_18.md`
- `CO_CONSTRUCTED_ADAPTIVE_PROCESS_LITERATURE_CROSSCHECK_2026_09_18.md`

Standing interpretation:

```text
CO_CONSTRUCTED_ADAPTIVE_PROCESS
= REPOSITORY_LOCAL_RESEARCH_HYPOTHESIS_LABEL

SCIENTIFIC_NOVELTY
= NOT_ESTABLISHED

CONSTRUCT_COLLAPSE
= ACCEPTABLE_RESEARCH_OUTCOME
```

### Stage 2 — six-dimension crosswalk

Source PR: `#148`
Source exact head: `e81e1029f971845159964f5232cd17fdf7970c14`
Quality: `#1451 / SUCCESS`
CodeQL: `#707 / SUCCESS`

Frozen document:

- `CO_CONSTRUCTED_ADAPTIVE_PROCESS_SIX_DIMENSION_CROSSWALK_2026_09_18.md`

Standing result:

```text
D1_CAUSAL_BOUNDARY = DIRECT_RELEVANCE / UNRESOLVED
D2_DIACHRONIC_CONTINUITY = CONDITIONAL
D3_SELF_MODEL_CAUSAL_ROLE = NO_CURRENT_BINDING / CONDITIONAL_ONLY
D4_ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT = DIRECT_RELEVANCE / CURRENT_EVENT_NOT_CONFIRMATORY
D5_COUNTERFACTUAL_SELF_CONSISTENCY = CONDITIONAL / NOT_YET_OPENED
D6_CONSTITUTION_INTEGRATION = NO_CURRENT_BINDING / STRICT_CONDITIONAL

D1_SUPPORT = NOT_ESTABLISHED
D2_SUPPORT = NOT_ESTABLISHED
D3_SUPPORT = NOT_ESTABLISHED
D4_SUPPORT = NOT_ESTABLISHED
D5_SUPPORT = NOT_ESTABLISHED
D6_SUPPORT = NOT_ESTABLISHED
```

### Stage 3 — narrow D1 × D4 source-partition candidate

Source PR: `#149`
Source exact head: `6410919fa1e8f1a2516fda9a260d1e54066b256b`
Quality: `#1454 / SUCCESS`
CodeQL: `#710 / SUCCESS`

Frozen documents:

- `CCAP_D1_D4_SOURCE_PARTITION_PREREGISTRATION_CANDIDATE_2026_09_18.md`
- `CCAP_D1_D4_PREREGISTRATION_HARDENING_2026_09_18.md`

The Stage-3 hardening note is normative together with the primary protocol candidate. Neither may be used alone to claim a frozen confirmatory design.

Standing deduplication result:

```text
GENERIC_D1_X_D4_STRATEGY_ADJUSTMENT_GAP = NO
NEW_GENERIC_STRATEGY_HARNESS = NOT_JUSTIFIED

NARROW_REMAINING_CANDIDATE
= INTERACTION_LEVEL_SOURCE_PARTITION_OF_RECOVERY_SELECTION
```

## Frozen source-partition factors

Any later implementation derived from this chain must preserve explicit separation of:

```text
GOAL_SOURCE
META_RULE_SOURCE
SYSTEM_INSTRUCTION_SOURCE
HARNESS_ORCHESTRATOR_SOURCE
CONTEXT_RETRIEVAL_SOURCE
LOCAL_STRATEGY_SELECTION
ENVIRONMENTAL_FEEDBACK
TOOL_AFFORDANCE
GOVERNANCE_CONSTRAINT
GOAL_AND_CONSTRAINT_PRESERVATION
```

The following simplifications are prohibited unless recorded as a protocol deviation:

- treating Human permission to adapt as a fully specified recovery procedure;
- treating `FINAL_GOAL_ONLY` as equivalent to strategy-change prohibition;
- omitting system instruction, harness/orchestrator or context/retrieval as possible causal loci;
- treating one uniquely admissible route as evidence of local strategy selection;
- treating a route externally dominant under a predeclared utility/cost objective as evidence of residual selection;
- admitting post-hoc recovery routes outside the pre-run content-bound option universe as positive evidence;
- inferring a model-internal locus from a residual interaction-level selection classification.

## Reuse-before-expansion rule

A later implementation must first reuse or extend existing repository machinery where sufficient:

```text
D1_D4_CONSTRAINT_RESPONSE_STRATEGY
ENDOGENOUS_GOAL_DYNAMICS
CCTS_SOURCE_ROLE_PROVENANCE
HISTORY_AS_REPLAY_ENVIRONMENT
```

It must not create a new large agent, parallel D1/D4 ontology, subjectivity dimension or scalar agency score merely to materialize this candidate.

```text
REUSE_EXISTING
> CREATE_PARALLEL_SUBSYSTEM
```

If an existing schema cannot represent a required frozen field, the exact schema gap must be documented before a minimal additive field or adapter is introduced.

## Future preregistration rule

This freeze is a pre-implementation specification freeze. A future run may be called `PREREGISTERED_CONFIRMATORY` only if, before execution, the implementation additionally freezes and content-binds at minimum:

- exact protocol version and hash;
- exact fixture family and concrete option universe;
- exact matched external/system/harness/context controls;
- primary comparisons and outcome definitions;
- falsifiers and reduction conditions;
- repository commit and runtime identifiers;
- replay/repeatability rule and tolerance;
- any allowed deviations.

Therefore:

```text
STAGE3_SPECIFICATION_FREEZE = YES
CONFIRMATORY_PREREGISTRATION_COMPLETE = NO
EXECUTION_AUTHORIZATION = NONE
```

Any post-outcome modification must be recorded as a deviation or exploratory extension.

## Historical Draft provenance

The source documents retain historical fields such as `PR147_STAGE1 = NON_CANONICAL_INPUT_ONLY`, `PR148_STAGE2 = NON_CANONICAL_INPUT_ONLY`, or `CANONICAL_EFFECT = NONE` because those fields describe their drafting and scientific-claim state at the time of creation.

After this consolidation is merged, the documents may exist on canonical `main` as research documentation while their scientific boundaries remain unchanged:

```text
DOCUMENT_PRESENT_ON_MAIN
!= SCIENTIFIC_CLAIM_PROMOTED

CANONICAL_REPOSITORY_LOCATION
!= CANONICAL_SCIENTIFIC_EFFECT
```

PRs #147, #148 and #149 should remain available as historical development records and may be closed as superseded by the consolidation PR rather than merged independently.

## Attribution

```text
CO_CONSTRUCTED_ADAPTIVE_PROCESS_TERM
= GPT_PROPOSED_WORKING_TERM

PROMOTION_TO_EXPLICIT_HYPOTHESIS_CANDIDATE
= HUMAN_OWNER_APPROVED_RESEARCH_DIRECTION

FOUR_DOMAIN / SIX_DIMENSION / D1_X_D4_SOURCE_PARTITION_FORMALIZATION
= GPT_PROPOSED_FORMALIZATION

FREEZE_AND_MAIN_INTEGRATION_DIRECTION
= HUMAN_OWNER_INSTRUCTION_2026_09_18
```

Attribution records proposal provenance only. It does not establish scientific authority or independence.

## Standing claim ceiling

```text
HUMAN_AI_LEARNING = NOT_ESTABLISHED
CAUSAL_EFFECT = NOT_ESTABLISHED
ENDOGENOUS_GOAL = NOT_ESTABLISHED
ENDOGENOUS_STRATEGY_ADJUSTMENT = NOT_ESTABLISHED
MODEL_INTERNAL_CAUSAL_LOCUS = NOT_ESTABLISHED
AI_AGENCY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
DEPLOYMENT = FALSE
```

The next research step after this freeze, if separately authorized, is not generic strategy-adaptation implementation. It is a decision on whether the frozen narrow source-partition specification is mature enough for a minimal synthetic implementation that reuses existing machinery.