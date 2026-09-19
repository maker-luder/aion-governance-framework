# Deferred / historical PR implementation re-entry plan — 2026-09-19

Status: `REFRESHED_CURRENT_MAIN_REVIEW / CURRENT_MAIN_REAUTHORING_ONLY / SCIENTIFIC_HOLD`

## 1. Purpose

This document converts historical Closed / Draft PR material into one bounded execution queue.

It is intentionally **not** a historical-branch revival plan.

```text
REPOSITORY = maker-luder/aion-governance-framework
BASE_MAIN = 27f42f0636583a7f2da5a3d5b8a2352aecd1cfc8
BASE_TREE = 2d38ccebc8522c07b90fc4d7439441ef1b7003b3
REFRESHED_FROM_PR_HEAD = ab9e349a56528ea79c650785027c480c3fe424cb
REFRESH_DATE = 2026-09-20
REFRESH_DISPOSITION = MINIMAL_DOC_REFRESH

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

## 3. Current disposition queue

Q1 and Q2 are no longer active implementation work. They moved to the completed / absorbed section after the live current-main recheck below.

### Q3 — PR #61: latent regulatory-variable discovery extension

Current `main` already contains two relevant but non-identical surfaces:

1. `research-labs/endogenous-goal-dynamics_v0.1.0/` freezes the candidate universe for matched selection trials, separates generation from selection, binds provider/model/generator/selector/seed, and preregisters random, prompt, memory, intervention, ablation, stale-state and cross-provider falsifiers;
2. `research-labs/endogenous-norm-formation_v0.1.0/docs/LATENT_REGULATORY_STATE_DISCOVERY.md` documents a future latent-state protocol with held-out prediction, intervention, ablation, replay, transfer, provenance and rejection criteria, but remains explicitly `NOT IMPLEMENTED`.

Therefore Q3 is not a new research axis and is not an executable implementation item in this refresh:

```text
CURRENT_MAIN_DEDUP = COMPLETE
DEDUP_RESULT = OVERLAPPING_CONTROL_MACHINERY / DISTINCT_UNIMPLEMENTED_DISCOVERY_QUESTION
ACTION = DESIGN_ONLY_HOLD
Q3_EXECUTABLE_IMPLEMENTATION = NOT_AUTHORIZED
PRIORITY = MEDIUM_HIGH
SCIENTIFIC_DISPOSITION = HOLD
```

The surviving discriminant is narrower than the earlier prototype wording:

```text
OBSERVED_REGULARITY
!= LATENT_REGULATORY_VARIABLE

IF
STOCHASTIC_VARIATION
+ SELECTION
+ EVALUATOR_PRESSURE
+ ENVIRONMENT_FEEDBACK
CAN EXPLAIN THE EFFECT

THEN
LATENT_REGULATORY_VARIABLE = NOT_ESTABLISHED
```

Before a latent regulatory-variable candidate may be considered, a future protocol must control or bind:

- stochastic candidate generation and the candidate universe;
- the selection rule;
- random-seed effects;
- evaluator / reward pressure;
- environmental feedback;
- prompt, context, memory, tools and harness / orchestration confounds;
- provider, model and runtime identity.

Only after those controls may the following justify further study:

- a reproducible residual effect;
- predictable intervention sensitivity;
- held-out predictive value under conditions not used to design the candidate.

```text
RESIDUAL_EFFECT != LATENT_REGULATORY_VARIABLE_PROVEN
RESIDUAL_EFFECT != ENDOGENOUS_VARIABLE_PROVEN
RESIDUAL_EFFECT != SUBJECTIVITY
PREDICTIVE_GAIN != SUBJECTIVITY_EVIDENCE
```

This compact compound falsifier adds discriminant value because the existing current-main surfaces distribute these controls across the Endogenous Goal Dynamics harness, the latent-state future protocol, and the upstream 12-axis intake; none states the complete stochastic-search-plus-selection rejection rule in one Q3 admission boundary.

### OpenAI source cross-check for Q3 scope

The already-ingested OpenAI case, *How a researcher uses Codex and ChatGPT to search for new antimicrobial molecules* (2026-09-10), describes bacteria, fungi, parasites and viruses as the biomedical problem domain. Those organisms are not an AI mutation or latent-regulation mechanism.

```text
FUNGI_AS_AI_MECHANISM = REJECT
BIOMEDICAL_PROBLEM_DOMAIN != AI_MUTATION_MECHANISM
AI_HYPOTHESIS_GENERATION != EMPIRICAL_CONFIRMATION
PROMISING_CANDIDATE != VALIDATED_EFFECT
DUPLICATE_REINGESTION = NO
NEW_BIOLOGY_RESEARCH_AXIS = NO
```

The source remains useful only for the repository's existing hypothesis-generation / empirical-confirmation boundary.

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

## 4. Completed / absorbed / reimplemented — do not revive old PR

### Q1 — completed on current main by PR #183

PR #183 merged the claim-admission bridge at merge commit `3d381de4eab5ee294ec508cd6e16996d90720b53`.

```text
Q1_STATUS = COMPLETED / IMPLEMENTED_ON_CURRENT_MAIN
SOURCE_GAP = #93-DERIVED
CURRENT_IMPLEMENTATION = LONGITUDINAL_CLAIM_ADMISSION_BRIDGE
ACTIVE_IMPLEMENTATION_QUEUE = NO
CLAIM_CEILING = STRUCTURAL_ADMISSIBILITY_ONLY
```

### Q2 — completed on current main by PR #184

PR #184 merged the bounded synthetic memory-locus dependency harness at merge commit `240c1c36c1d06cd12de93d1bc3637203c2351e47`. The implementation explicitly deduplicates against the continuity-dissociation harness and preserves the functional-dependency claim ceiling.

```text
Q2_STATUS = COMPLETED / IMPLEMENTED_ON_CURRENT_MAIN
SOURCE_SPECIFICATION = #122
CURRENT_IMPLEMENTATION = MEMORY_LOCUS_DEPENDENCY_HARNESS
ACTIVE_IMPLEMENTATION_QUEUE = NO
FUNCTIONAL_DEPENDENCY = NOT_ESTABLISHED
IDENTITY_CONTINUITY = NOT_ESTABLISHED
```

The following earlier items also remain absorbed or reimplemented:

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

For any eventual `main` transition, PR #188 makes the following event order binding:

```text
FINALIZE_EXACT_HEAD
-> COMPLETE_REVIEW_AND_REQUIRED_ENGINEERING_CHECKS
-> IF_DRAFT: MARK_READY_FOR_REVIEW
-> WAIT_FOR_RESULTING_AUTHORITY_GATE_EVENT
-> HUMAN_OWNER_CONFIRMS_FRESH_EXACT_HEAD_MERGE_APPROVAL
-> EDIT_PR_BODY_WITH_ONE_FRESH_AUTHORITY_RECEIPT
-> REQUIRE_AUTHORITY_GATE_PASS
-> RECHECK_EXACT_HEAD_AND_REQUIRED_CHECKS
-> MERGE_WITHOUT_INTERVENING_PR_STATE_OR_METADATA_TRANSITION
```

The authority receipt is event-bound as well as exact-head-bound. A later `synchronize`, `reopened`, `ready_for_review`, title edit, or other relevant state / metadata event does not inherit an earlier PASS. Any such change requires a fresh exact-head review and, where applicable, a fresh Human Owner confirmation and PR-body receipt.

```text
CI_PASS != MERGE_AUTHORITY
AI_REVIEW != HUMAN_OWNER_MERGE_APPROVAL
PRIOR_AUTHORITY_PASS != CURRENT_MERGE_READINESS
NO_INTERVENING_PR_STATE_OR_METADATA_CHANGE = REQUIRED_AFTER_FINAL_PASS
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
VARIATION != SELECTION
CANDIDATE_GENERATION != CANDIDATE_SELECTION
SELF_GENERATED_CANDIDATE != ENDOGENOUS_SELECTION
STOCHASTIC_SEARCH_PLUS_SELECTION != ENDOGENOUS_AGENCY
OBSERVED_REGULARITY != LATENT_INTERNAL_MECHANISM
RESIDUAL_EFFECT != SUBJECTIVITY
PREDICTIVE_GAIN != SUBJECTIVITY_EVIDENCE
ADAPTATION != SUBJECTIVITY
CONTINUITY != IDENTITY
TEST_PASS != SCIENTIFIC_VALIDATION
CI_PASS != SCIENTIFIC_VALIDATION
QUALITY_GATE_PASS != SCIENTIFIC_VALIDATION

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
```
