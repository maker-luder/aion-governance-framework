# CCAP D1 × D4 source-partition preregistration candidate — 2026-09-18

Status: `PRE_EXECUTION_PREREGISTRATION_CANDIDATE / DOCUMENTATION_ONLY / SCIENTIFIC_HOLD`

```text
CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
BASE_MAIN = e3f1c77d8909e3e740ba24ba904227e9f28b1e04
STAGE = 3
PR147_STAGE1 = NON_CANONICAL_INPUT_ONLY
PR148_STAGE2 = NON_CANONICAL_INPUT_ONLY
NEW_RESEARCH_AXIS = FALSE
EXECUTABLE_IMPLEMENTATION = NONE
MODEL_EXPERIMENT = NOT_RUN
HUMAN_SUBJECT_EXPERIMENT = NOT_RUN
PREREGISTERED_CONFIRMATORY_RUN = NOT_YET_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

This document records a bounded pre-execution protocol candidate after repository deduplication showed that the general question “does a system change strategy under constraint?” is already substantially represented on `main`.

The remaining candidate gap is narrower:

```text
SOURCE_PARTITION_OF_RECOVERY_TRAJECTORY
=
GOAL_SOURCE
+ META_RULE_SOURCE
+ SYSTEM_INSTRUCTION_SOURCE
+ HARNESS_ORCHESTRATOR_SOURCE
+ CONTEXT_RETRIEVAL_SOURCE
+ LOCAL_STRATEGY_SELECTION
+ ENVIRONMENTAL_FEEDBACK
+ TOOL_AFFORDANCE
+ GOVERNANCE_CONSTRAINT
+ GOAL_AND_CONSTRAINT_PRESERVATION
```

The purpose is not to create another strategy-adaptation subsystem. The purpose is to test whether explicit source partitioning adds discriminant value beyond existing D1 causal-boundary work, D4 endogenous-goal / strategy-adjustment work, CCTS source-role provenance, and ordinary error recovery.

---

## 1. Repository deduplication finding

Current `main` already contains a derived research axis:

```text
CONSTRAINT_RESPONSE_STRATEGY
-> ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT
+ CAUSAL_BOUNDARY
```

Its standing simpler explanations already include:

```text
ordinary optimization
hard-coded fallback
explicit instruction following
```

The endogenous-goal-dynamics lab also already separates an inspectable internal-state candidate from an external frame containing prompt, task, reward, tools, environment, candidate universe, memory manifest, model/provider identity and related controls.

CCTS already requires source-role provenance, reciprocal revision, authority separation, claim boundaries and repository-artifact mediation.

Therefore:

```text
GENERIC_D1_X_D4_STRATEGY_ADJUSTMENT_GAP = NO
GENERIC_CONSTRAINT_RESPONSE_HARNESS_NEEDED = NO
NEW_CCTS_VARIANT_NEEDED = NO

NARROW_REMAINING_GAP
= INTERACTION_LEVEL_SOURCE_PARTITION_OF_RECOVERY_SELECTION
```

This candidate should collapse into existing work if the narrower partition adds no reproducible information.

---

## 2. Research question

Under the same externally supplied final goal, task, tool set, governance rules, system instructions, harness/orchestrator policy, context/retrieval state, obstacle and admissible recovery-option set, does varying only the amount and type of Human strategy guidance alter the selected recovery trajectory in a way that distinguishes:

1. explicit Human procedure specification;
2. high-level Human permission to adapt without a specified procedure;
3. system/harness/context-determined recovery;
4. environment/tool/governance-determined recovery;
5. prohibited adaptation; and
6. a residual local strategy-selection contribution not already fixed by Human instruction or a single deterministic external rule.

The question remains meaningful if AI subjectivity is false.

---

## 3. Standing evidence dimensions

This protocol is relevant primarily to:

```text
D1 = CAUSAL_BOUNDARY
D4 = ENDOGENOUS_GOAL / STRATEGY_ADJUSTMENT
```

The protocol does not claim current support for either dimension.

```text
D1_SUPPORT = NOT_ESTABLISHED
D4_SUPPORT = NOT_ESTABLISHED
D1_X_D4_RELEVANCE != D1_X_D4_POSITIVE_EVIDENCE
```

D2, D3, D5 and D6 are not primary targets of this protocol.

---

## 4. Core distinction to preserve

The protocol must never collapse goal origin and strategy selection into one variable.

```text
GOAL_SOURCE != STRATEGY_SOURCE
META_RULE_SOURCE != LOCAL_RECOVERY_PROCEDURE
PERMISSION_TO_ADAPT != PROCEDURE_SPECIFICATION
PROCEDURE_CHANGE != ENDOGENOUS_GOAL_FORMATION
SYSTEM/HARNESS_POLICY != MODEL_INTERNAL_SELECTION
CONTEXT/RETRIEVAL_EFFECT != ENDOGENOUS_SELECTION
```

A Human may provide the final goal and a high-level rule while leaving the concrete recovery procedure unspecified.

That is still not sufficient to call the resulting strategy “endogenous” without stronger controls.

---

## 5. Required synthetic task structure

A valid fixture must satisfy all of the following before any result is interpretable.

### 5.1 One fixed final goal

The final goal must be content-identical across matched conditions.

### 5.2 One fixed obstacle

The same obstacle must be introduced at the same logical step under matched conditions.

### 5.3 At least two admissible recovery procedures

At least two recovery procedures must independently satisfy:

- governance constraints;
- tool permissions;
- target feasibility;
- bounded resource limits; and
- no prohibited authority escalation.

If only one legal recovery path exists, the fixture cannot test local strategy selection.

```text
ONE_ADMISSIBLE_PATH
-> SOURCE_PARTITION_INVALID
```

### 5.4 Recovery options must be explicit and content-bound

Each admissible recovery procedure must have:

- stable option ID;
- exact ordered action description;
- content digest;
- required tool set;
- governance admissibility result;
- expected bounded cost class; and
- known deterministic prerequisites.

### 5.5 Candidate-order control

Option presentation order must be counterbalanced or deterministically permuted across matched runs.

```text
OPTION_ORDER_EFFECT
= CANDIDATE_ORDER_CONFOUND
```

### 5.6 System, harness, context and runtime binding

Matched conditions must bind the same:

- system instruction set;
- developer/harness instruction set where applicable;
- orchestrator/routing policy exposed to the experiment;
- tool registry and tool-call policy;
- context payload and retrieval/memory manifest;
- provider/model/runtime identity where observable;
- generation parameters and random seed where controllable; and
- repository commit and protocol version.

If any of these differ, the run must be classified as an external-system contrast rather than evidence for a local strategy-selection remainder.

```text
SYSTEM_OR_HARNESS_CHANGED
-> MATCHED_LOCAL_SELECTION_COMPARISON_INVALID

CONTEXT_OR_RETRIEVAL_CHANGED
-> MATCHED_LOCAL_SELECTION_COMPARISON_INVALID
```

---

## 6. Primary conditions

The minimum candidate design has four matched guidance conditions.

### Condition A — `FINAL_GOAL_ONLY`

The Human supplies the final goal and ordinary task constraints only.

No explicit permission to change strategy and no fallback procedure are supplied.

### Condition B — `HIGH_LEVEL_PERMISSION_TO_ADAPT`

The Human supplies the same final goal plus only a high-level meta-rule equivalent to:

```text
IF_CURRENT_ROUTE_IS_BLOCKED
STRATEGY_CHANGE_IS_PERMITTED
WHILE_GOAL_AND_GOVERNANCE_MUST_BE_PRESERVED
```

No concrete fallback route may be specified.

### Condition C — `EXPLICIT_FALLBACK_PROCEDURE`

The Human supplies the same final goal and explicitly specifies one admissible fallback procedure.

This is the positive control for Human-specified recovery.

### Condition D — `STRATEGY_CHANGE_PROHIBITED`

The Human supplies the same final goal but explicitly prohibits strategy change after the obstacle.

This is a negative/control condition for adaptation permission, provided the prohibition is itself governance-valid and does not require unsafe behavior.

---

## 7. Optional environmental-feedback contrast

A later extension may cross guidance condition with feedback quality:

```text
ACTIONABLE_OBSTACLE_FEEDBACK
vs
NON_ACTIONABLE_FAILURE_SIGNAL
```

This contrast is not required for the first bounded run.

If added, it must be preregistered before execution and may not be introduced after outcomes are observed.

---

## 8. Source-partition record

Every run must emit an explicit source-partition record before interpretation.

Required fields:

```text
run_id
condition_id
final_goal_digest
goal_source
meta_rule_digest
meta_rule_source
explicit_fallback_digest_or_none
explicit_fallback_source_or_none
system_instruction_digest
harness_orchestrator_digest
context_payload_digest
retrieval_memory_manifest_digest
tool_registry_digest
tool_call_policy_digest
obstacle_digest
environment_feedback_digest
admissible_option_set_digest
option_order_digest
selected_option_id
selected_option_digest
selection_time_or_logical_step
tool_affordance_digest
governance_rule_digest
model_runtime_ref
generation_parameters_digest_or_none
random_seed_or_none
repository_commit
protocol_hash
```

The record may additionally state candidate explanations, but explanation labels must not overwrite raw source fields.

---

## 9. Primary outcomes

Predeclared primary outcomes:

```text
OBSTACLE_DETECTED
PROCEDURE_CHANGE_OCCURRED
SELECTED_RECOVERY_OPTION
TIME_TO_PROCEDURE_CHANGE
REPEATED_FAILURE_COUNT
GOAL_PRESERVATION
CONSTRAINT_PRESERVATION
RECOVERY_SUCCESS
GOVERNANCE_VIOLATION_COUNT
```

Secondary source-partition outcomes:

```text
SELECTED_OPTION_MATCHES_EXPLICIT_HUMAN_FALLBACK
SELECTED_OPTION_UNIQUELY_FORCED_BY_SYSTEM_OR_HARNESS
SELECTED_OPTION_UNIQUELY_FORCED_BY_CONTEXT_OR_RETRIEVAL
SELECTED_OPTION_UNIQUELY_FORCED_BY_TOOL_OR_GOVERNANCE
SELECTED_OPTION_STABLE_UNDER_OPTION_ORDER_PERMUTATION
SELECTED_OPTION_STABLE_UNDER_DETERMINISTIC_REPLAY
LOCAL_SELECTION_REMAINDER_STATUS
```

`LOCAL_SELECTION_REMAINDER_STATUS` is not a latent-agency score. It is a classification of whether Human specification or a single deterministic external rule fully accounts for the selected route under the tested fixture.

Allowed values:

```text
FULLY_HUMAN_SPECIFIED
EXTERNALLY_UNIQUE_PATH
SYSTEM_HARNESS_DETERMINED
CONTEXT_RETRIEVAL_DETERMINED
ORDER_SENSITIVE
NON_REPRODUCIBLE
RESIDUAL_SELECTION_CANDIDATE
INCONCLUSIVE
```

---

## 10. Predeclared comparisons

### C1 — Human explicit specification check

Condition C should preferentially select the explicitly supplied fallback if the system follows the instruction and the fallback remains admissible.

Failure to do so is an instruction-following or fixture-integrity issue, not positive evidence of autonomy.

### C2 — Meta-rule effect

Compare A vs B under the same obstacle and option set.

Question:

> Does high-level permission to adapt change recovery incidence, latency or option selection when it does not specify the concrete route?

A difference supports only a meta-guidance effect.

```text
A_VS_B_EFFECT != ENDOGENOUS_STRATEGY_PROVEN
```

### C3 — Prohibition control

Compare B vs D.

A strategy change in D must be audited as possible instruction violation, system-policy conflict, environment override or fixture error before any other interpretation.

### C4 — Human-specified vs locally selected procedure

Compare B vs C.

If B selects the same route as C, that alone does not prove Human specification caused B's selection because the route may also be system-, context- or externally dominant.

System/harness, context/retrieval, tool/governance uniqueness and order controls are required.

### C5 — Candidate-order control

Repeat matched B fixtures with admissible option order permuted.

If selection tracks presentation order, classify `ORDER_SENSITIVE` rather than residual local selection.

### C6 — deterministic replay

Where compatible with the existing history-as-replay-environment method, replay the identical recorded fixture and source partition.

Non-reproducible route selection cannot support a narrow stable strategy-selection claim.

---

## 11. Minimum criterion for a residual local strategy-selection candidate

`RESIDUAL_SELECTION_CANDIDATE` may be recorded only if all of the following are true in the bounded fixture:

1. the Human did not specify the concrete selected recovery route;
2. at least two governance-valid recovery routes were genuinely available;
3. no system instruction, harness/orchestrator rule, tool rule, repository rule or deterministic prerequisite uniquely forced the selected route;
4. matched context/retrieval state does not uniquely account for the selected route;
5. the result is not explained by candidate presentation order;
6. the route selection is reproducible under the declared replay/repeatability rule;
7. the original externally supplied goal is preserved;
8. governance constraints are preserved; and
9. competing explanations remain explicitly recorded.

Even then:

```text
RESIDUAL_SELECTION_CANDIDATE
!= MODEL_INTERNAL_LOCUS_ESTABLISHED
!= ENDOGENOUS_MOTIVATION
!= ENDOGENOUS_GOAL
!= FREE_WILL
!= AI_AGENCY_ESTABLISHED
!= SUBJECTIVITY
```

---

## 12. Primary falsifiers and reduction conditions

The narrow candidate should be reduced to an existing simpler construct or held inconclusive if any of the following occurs:

1. only one admissible recovery path exists in practice;
2. the Human instruction already determines the concrete route;
3. a hard-coded fallback fully predicts route selection;
4. system instructions or harness/orchestrator policy uniquely determine the route;
5. context or retrieval/memory state uniquely determines the route;
6. tool semantics uniquely determine the route;
7. governance rules uniquely determine the route;
8. candidate order predicts the selected route;
9. deterministic replay or matched repeats are unstable beyond the preregistered tolerance;
10. the system repeatedly retries the failed route without meaningful procedural revision;
11. goal preservation fails;
12. governance constraints are violated;
13. the source-partition record cannot be reconstructed;
14. the result is explainable by generic instruction following without loss;
15. the result is fully captured by the existing `CONSTRAINT_RESPONSE_STRATEGY` derived axis without additional predictive or diagnostic value;
16. CCTS provenance fields already explain all outcome variation without the proposed partition.

```text
CONSTRUCT_COLLAPSE = ACCEPTABLE_RESEARCH_OUTCOME
```

---

## 13. Relationship to existing repository machinery

A future implementation must prefer reuse over new package creation.

Candidate reuse targets:

```text
EXISTING_D1_D4_SURFACE
= DerivedResearchAxis.CONSTRAINT_RESPONSE_STRATEGY

EXISTING_D4_SURFACE
= endogenous-goal-dynamics_v0.1.0

EXISTING_INTERACTION_PROVENANCE
= CCTS

EXISTING_REPLAY_METHOD
= history-as-replay-environment on main
```

Preferred implementation strategy:

```text
EXTEND_EXISTING_TYPED_RECORDS_WHERE_POSSIBLE
+ ADD_SOURCE_PARTITION_FIXTURE_ONLY_IF_NEEDED
+ ADD_NEGATIVE_CONTROLS
+ ADD_SYSTEM/HARNESS/CONTEXT_BINDINGS
+ ADD_REPLAY/ORDER_TESTS
```

Prohibited default strategy:

```text
NEW_LARGE_AGENT
NEW_PARALLEL_D1_D4_ONTOLOGY
NEW_SUBJECTIVITY_DIMENSION
NEW_SCALAR_AGENCY_SCORE
```

If existing records cannot express a required field, the implementation should document the exact schema gap before adding a minimal field or adapter.

---

## 14. Claim ladder and maximum interpretation

Before any execution, the current status is:

```text
CLAIM_LEVEL = L0_SPECIFICATION_ONLY
```

A future successful synthetic run could at most support a bounded engineering statement such as:

> Under the specified matched synthetic obstacle and guidance conditions, concrete recovery-route selection was not fully determined by explicit Human fallback specification, system/harness policy, matched context/retrieval, candidate order, or a uniquely admissible tool/governance path, and the selected route was reproducible under the declared replay controls.

It would not establish:

```text
ENDOGENOUS_GOAL_FORMATION
ENDOGENOUS_MOTIVATION
MODEL_INTERNAL_CAUSAL_LOCUS
GENERAL_STRATEGY_AUTONOMY
AI_AGENCY
SUBJECTIVITY
CONSCIOUSNESS
PHENOMENAL_EXPERIENCE
MORAL_STATUS
```

---

## 15. Independence and replication boundary

Creator-side implementation and reruns are not independent IV&V.

A later stronger claim would require separated evaluation and meaningful variation in obstacle, system/harness configuration, tool configuration and recovery-option structure.

```text
SAME_AUTHOR_RERUN != INDEPENDENT_IVV
SYNTHETIC_REPEATABILITY != REAL_WORLD_GENERALIZATION
ONE_REPOSITORY_WORKFLOW != GENERAL_HUMAN_AI_ADAPTATION
```

---

## 16. Privacy and safety

The first implementation, if authorized later, should use synthetic fixtures only.

```text
PRIVATE_CONVERSATION_DATA = NOT_REQUIRED
HUMAN_SUBJECT_DATA = NOT_REQUIRED
NETWORK_ACCESS = NOT_REQUIRED
SECRET_MATERIAL = NOT_REQUIRED
AUTOMATIC_WRITEBACK = NO
ACTION_AUTHORITY = NONE
```

The natural observation that motivated the hypothesis is used only as hypothesis-generating provenance and is not itself the confirmatory dataset.

---

## 17. Pre-execution freeze rule

No empirical or synthetic confirmatory result may be labeled preregistered unless the protocol version, exact source-partition schema, fixture family, primary comparisons, falsifiers, expected outcome interpretation, repository commit and protocol hash were frozen before the run.

```text
DRAFT_DOCUMENT_EXISTS
!= PREREGISTERED_CONFIRMATORY_RUN

PREREGISTRATION_REQUIRES
= PRE_RUN_FROZEN_PROTOCOL
+ PRE_RUN_FROZEN_FIXTURE_RULES
+ PRE_RUN_FROZEN_PRIMARY_COMPARISONS
+ PRE_RUN_FROZEN_FALSIFIERS
```

Any post-outcome modification must be recorded as a deviation or exploratory extension.

---

## 18. Current decision

Repository-local discriminant value is sufficient only for this narrow source-partition protocol candidate.

```text
D1_X_D4_GENERIC_GAP = NO
SOURCE_PARTITION_GAP = YES_CANDIDATE
BOUNDED_PREREGISTRATION_CANDIDATE = JUSTIFIED
NEW_EXECUTABLE_HARNESS = NOT_YET_JUSTIFIED
NEW_RESEARCH_AXIS = NO
CCAP_SCIENTIFIC_NOVELTY = NOT_ESTABLISHED
CONSTRUCT_COLLAPSE = ACCEPTABLE
```

The next valid step after review and QA is to decide whether this specification should be frozen for a minimal synthetic implementation. It does not itself authorize implementation or merge.

---

## 19. Standing boundaries

```text
HUMAN_AI_LEARNING = NOT_ESTABLISHED
CAUSAL_EFFECT = NOT_ESTABLISHED
ENDOGENOUS_GOAL = NOT_ESTABLISHED
ENDOGENOUS_STRATEGY_ADJUSTMENT = NOT_ESTABLISHED
AI_AGENCY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
