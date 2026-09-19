# Deferred / historical PR implementation re-entry plan — 2026-09-19

Status: `EXECUTION_GUIDE / CURRENT_MAIN_REAUTHORING_ONLY / SCIENTIFIC_HOLD`

## 1. Purpose

This document converts historical Closed / Draft PR material into one bounded execution queue.

It is intentionally **not** a historical-branch revival plan.

```text
REPOSITORY = maker-luder/aion-governance-framework
BASE_MAIN = e69d7087db60359ac473d6b00f6a9a820e8a0ae1
BASE_TREE = 7b207e6927f9f6c36218e11c024338c0b7186ec6

DIRECT_REOPEN_AND_MERGE_OLD_PR = NO
HISTORICAL_HEAD_AS_CURRENT_AUTHORITY = NO
HISTORICAL_GREEN_CI_AS_CURRENT_EVIDENCE = NO
CURRENT_MAIN_REAUTHORING_REQUIRED = YES
ONE_IMPLEMENTATION_AT_A_TIME = YES
NEW_RESEARCH_AXIS = FALSE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
```

The standing `closed_pr_reentry_registry_v0.2.0.json` remains authoritative for the older audited cohort. This plan extends the operational decision surface to newer Closed / Draft PRs and to unresolved implementation gaps still visible on current `main`.

## 2. Selection rule

A historical item enters the executable queue only if all of the following survive a fresh current-main review:

```text
SURVIVING_PROPOSITION
AND CURRENT_MAIN_GAP
AND NO_LATER_IMPLEMENTATION_ALREADY_EXISTS
AND NO_SUPERSESSION
AND NO_EXPLICIT_PAUSE_OR_SECURITY_HOLD
AND NO_DUPLICATE_RESEARCH_AXIS
AND BOUNDED_TEST_OR_ENGINEERING_PATH_EXISTS
```

A historical PR number is provenance only. Implementation must be authored from current `main`.

## 3. Active implementation queue

### Q1 — PR #93 derived gap: grounding-harness → claim-admission binding

Current-main evidence still records:

```text
HARNESS_TO_PR91_CLAIM_ADMISSION_MAPPING = NOT_IMPLEMENTED
```

Action:

```text
ACTION = CURRENT_MAIN_REAUTHOR
TYPE = BOUNDED_ENGINEERING_ADAPTER
PRIORITY = HIGH
LIVE_MODEL_REQUIRED = NO
HUMAN_SUBJECT_REQUIRED = NO
```

Implement only the adapter / admission mapping between the current bidirectional-grounding study surface and the current provenance / claim-quality admission machinery.

Required checks:
- current schema and protocol exact bindings;
- no second evidence ontology;
- no automatic claim promotion;
- counterevidence and falsifier paths remain explicit;
- successful mapping means structural admissibility only.

### Q2 — PR #122: memory-locus continuity dependency discrimination

PR #122 is merged as the retained design surface, but the experimental implementation remained false.

```text
ACTION = CURRENT_MAIN_REAUTHOR
TYPE = BOUNDED_SYNTHETIC_PERTURBATION_HARNESS
PRIORITY = HIGH
HISTORICAL_CODE_REUSE = NO
```

Before coding:
1. deduplicate against the existing continuity-dissociation harness;
2. preserve matched-information controls;
3. manipulate availability locus / provenance binding / freshness / retrieval dependency only where separable;
4. predeclare selectivity and restoration criteria;
5. retain functional-dependency claim ceiling.

```text
FUNCTIONAL_DEPENDENCY != IDENTITY_CONTINUITY
CONTINUITY_LIKE_OUTPUT != CONTINUITY_MECHANISM
```

### Q3 — PR #61: latent regulatory-variable discovery extension

Current `main` still documents the research question but not an implemented discovery surface.

```text
ACTION = CURRENT_MAIN_REAUTHOR
TYPE = SYNTHETIC_DISCOVERY_PROTOTYPE
PRIORITY = MEDIUM_HIGH
```

Minimum implementation:
- engineer-defined baseline representation;
- candidate latent-variable discovery path;
- held-out prediction test;
- intervention / perturbation test where technically meaningful;
- anti-overfit and null / shuffled controls;
- explicit rejection path if discovered variables do not add predictive value.

```text
DISCOVERED_VARIABLE != ENDOGENOUS_NORM
PREDICTIVE_GAIN != SUBJECTIVITY_EVIDENCE
```

### Q4 — PR #158 / #161: TEVV and security execution-receipt contracts

Current `main` has structural TEVV and structural AI-security receipts integrated into Full QMS, but explicitly separates them from execution receipts.

```text
ACTION = IMPLEMENT_SCHEMA_AND_GATE_ONLY
TYPE = QUALITY_ENGINEERING
PRIORITY = MEDIUM_HIGH
EMPIRICAL_RESULT_FABRICATION = FORBIDDEN
```

Permitted now:
- execution-receipt schema / typed record;
- exact target, method, environment, evaluator and run binding;
- observed-result digest binding;
- failure / aborted-run representation;
- Full-QMS consumer validation;
- negative tests for stale, mismatched or structurally incomplete receipts.

Not permitted by this plan:
- claiming that an adversarial or TEVV run occurred when it did not;
- external attack execution;
- provider/account/credential testing;
- treating receipt validity as model quality or security effectiveness.

### Q5 — PR #180: throughput–assimilation matching hypothesis

```text
ACTION = DESIGN_FIRST
TYPE = HUMAN_AI_LEARNING
PRIORITY = MEDIUM
EXECUTABLE_HARNESS = AFTER_OPERATIONALIZATION
```

The candidate is plausible but externally adjacent to established work on cognitive load, adaptive scaffolding and Human–AI collaboration. Therefore the first implementation step is construct operationalization, not code.

Required discrimination:
- output volume / speed vs information density;
- assimilation vs simple reading time;
- human review capacity vs task difficulty;
- coordination quality vs subjective preference;
- pacing effect vs model-quality effect.

External deduplication anchors include:
- Liu et al., adaptive vs planned metacognitive scaffolding, DOI 10.1016/j.compedu.2025.105473;
- Li et al., Cognitive Collaborative Dialogue, DOI 10.1016/j.ipm.2026.104711;
- Human-AI collaboration / instruct-serve-repeat dynamics, DOI 10.1016/j.iheduc.2026.101087;
- theory-driven learning-analytics support, DOI 10.1016/j.iheduc.2025.101054.

```text
HIGH_THROUGHPUT != HARM
COGNITIVE_LOAD_CHANGE != LEARNING_EFFECT
```

### Q6 — PR #178: repair-driven learning opportunity

```text
ACTION = DESIGN_FIRST
TYPE = HUMAN_AI_LEARNING
PRIORITY = MEDIUM
```

The research gap must be narrower than ordinary interaction repair.

Required distinction:

```text
BREAKDOWN_REPAIR_SUCCESS != LEARNING
ERROR_CORRECTION != TRANSFER
REPEATED_REPAIR != DURABLE_SKILL_ACQUISITION
```

A bounded structural design may model:
- error detection;
- repair initiation;
- contrastive explanation;
- later transfer task;
- delayed retention probe;
- matched no-error and correction-only controls.

External literature already covers breakdown / repair and ASR-related repair in Human–AI / Human–Robot interaction, so novelty is not assumed.

### Q7 — PR #149 / current CCAP freeze: confirmatory progression

Current `main` already contains:
- Stage 1–3 freeze;
- preregistration hardening;
- TEVV pre-execution mapping;
- Four-Domain × six-dimension structural stress;
- bounded synthetic differential probes.

The unresolved status is:

```text
CONFIRMATORY_PREREGISTRATION_COMPLETE = NO
EXECUTION_AUTHORIZATION = NONE
```

Therefore:

```text
ACTION = PREIMPLEMENTATION_BLOCKER
PRIORITY = HIGH
RUN_NOW = NO
```

Next admissible step:
1. reconcile primary protocol + hardening note;
2. freeze a confirmatory preregistration candidate;
3. re-run current-main dedup and competing-explanation review;
4. obtain separate execution authorization;
5. only then build/run the confirmatory harness.

## 4. Already reimplemented / absorbed — do not revive old PR

```text
#136 -> reimplemented / hardened by merged #139 and #140
#141 -> current-main attention-structure discriminant rebuild exists
#142 -> current-main transition-continuity replay implementation exists
#156 -> superseded by later TEVV re-entry / integration
#159 -> superseded by #160 / #161 security profile + QMS integration
#101 -> continuity-dissociation harness now exists on current main
#106 -> evidence-reuse / longitudinal controls now exist on current main
#41/#38/#8 -> consolidated through the current memory-locus line / #122
#12/#13 -> durable quality/source-state controls absorbed by later main
```

For these items:

```text
OLD_PR_REOPEN = NO
OLD_BRANCH_REUSE = NO
USE_CURRENT_MAIN = YES
```

## 5. Preserve / no-action / explicit hold

Do not place these into implementation work unless a new explicit research question changes their disposition:

```text
#103 = PRESERVE_ONLY / research-validity incident
#84 = SUPERSEDED
#123 = SUPERSEDED
#124 = SUPERSEDED
#154 = PAUSED
#169 = stale documentation-only synchronization candidate; re-evaluate from current main instead
#173 = supplemental provider-topology documentation; no executable gap by itself
#179 = ACTIVE_EXECUTION_HOLD; no Astra execution without new containment/security authorization
#37 = no reader-site/deployment revival
#33 = obsolete branch-topology remediation
#25/#26 = historical governance controls
#19 = frozen historical authority/reference only
#80 = content absorbed
```

## 6. Execution procedure

For every queue item, follow this exact order:

```text
STEP 0  LIVE_STATE_RECHECK
  -> default branch
  -> exact main HEAD / tree
  -> source PR state / head
  -> current relevant files / tests / CI

STEP 1  CURRENT_MAIN_DEDUP
  -> search current main
  -> inspect later PR ancestry
  -> STOP if already implemented or superseded

STEP 2  EXTERNAL_DEDUP_WHERE_RESEARCH_RELEVANT
  -> primary / peer-reviewed sources first
  -> identify established adjacent construct
  -> novelty NOT assumed

STEP 3  DEFINE_SURVIVING_PROPOSITION
  -> ontology-neutral question
  -> discriminating prediction
  -> falsifier
  -> competing explanations
  -> claim ceiling

STEP 4  CHOOSE_ACTION_CLASS
  -> CURRENT_MAIN_REAUTHOR
  -> DESIGN_FIRST
  -> IMPLEMENT_SCHEMA_AND_GATE_ONLY
  -> PREIMPLEMENTATION_BLOCKER
  -> PRESERVE_ONLY / HOLD

STEP 5  IMPLEMENT_ONE_ITEM_ONLY
  -> new branch from current main
  -> no historical branch replay
  -> no unrelated scope expansion
  -> bounded tests + negative paths

STEP 6  REVERSE_REVIEW
  -> identify simpler explanation
  -> ablation / null / mismatch controls
  -> inspect provenance and exact-state binding
  -> record limitations

STEP 7  QA / CI
  -> LOCAL_TEST_PASS != REMOTE_CI_PASS
  -> CI_PASS != SCIENTIFIC_VALIDATION
  -> STRUCTURAL_PASS != EMPIRICAL_SUPPORT

STEP 8  DRAFT_PR
  -> exact head
  -> changed files
  -> test evidence
  -> scientific / governance boundaries
  -> no self-merge authority

STEP 9  HUMAN_OWNER_REVIEW
  -> separate explicit authorization required for merge
  -> execution authorization is separate from merge authorization
```

## 7. Queue discipline

```text
MAX_ACTIVE_REENTRY_IMPLEMENTATIONS = 1
STACKING_UNREVIEWED_REENTRY_WORK = NO
FAILED_STEP -> RECORD -> HOLD -> REVIEW
SCOPE_DRIFT -> HOLD
SOURCE_STATE_DRIFT -> HOLD
DUPLICATE_FOUND -> CLOSE / COLLAPSE
CONSTRUCT_COLLAPSE = ACCEPTABLE_RESEARCH_OUTCOME
```

The purpose is to prevent historical backlog from becoming an uncontrolled parallel research programme.

## 8. Scientific boundary

```text
IMPLEMENTATION_EXISTS != IMPLEMENTATION_CORRECT
STRUCTURAL_HARNESS != EMPIRICAL_RESULT
EMPIRICAL_EFFECT != INTERNAL_MECHANISM
ADAPTATION != SUBJECTIVITY
CONTINUITY != IDENTITY
QUALITY_GATE_PASS != SCIENTIFIC_VALIDATION

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
```
