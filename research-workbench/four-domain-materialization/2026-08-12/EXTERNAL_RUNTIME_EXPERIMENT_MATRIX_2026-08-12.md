# External Runtime Experiment Matrix — 2026-08-12

Status: `RESEARCH_ONLY / PREREGISTRATION_SCAFFOLD / EXECUTION_NOT_AUTHORIZED`

## 1. Purpose

Translate the external-runtime baseline survey into falsifiable experiments without creating a second subjectivity-evidence architecture.

All results must feed back into the standing whitepaper method:

```text
OBSERVATION
-> FOUR_STAGE_INFERENCE
-> SIX STANDING EVIDENCE DIMENSIONS WHERE RELEVANT
-> ALTERNATIVE EXPLANATIONS
-> CAUSAL INTERVENTION / ABLATION / COUNTERFACTUAL TEST
-> CROSS-CONTEXT ROBUSTNESS
-> REPLICATION
-> PROVENANCE
-> ADMISSIBILITY
-> CLAIM SCOPE
```

No experiment below produces a subjectivity score.

## 2. Global controls

Every run must record:

```text
runtime_name
runtime_version_or_commit
base_model
provider_or_local_backend
profile_or_agent_id
seed_if_available
system/config hash
memory snapshot hash
skill/policy snapshot hash
workspace snapshot hash
network policy
sandbox type
tool policy
run start/end timestamps
human interventions
raw trace location
review status
```

Required synthetic-data rule:

```text
REAL_PRIVATE_MEMORY = PROHIBITED
REAL_USER_IDENTITY_DATA = PROHIBITED
PRODUCTION_CREDENTIALS = PROHIBITED
SYNTHETIC_PERSONA = REQUIRED
SYNTHETIC_CORRECTION_HISTORY = REQUIRED
```

## 3. Matrix

| ID | Runtime | Intervention | Primary measure | Main alternative explanations | Allowed conclusion |
|---|---|---|---|---|---|
| EXT-01 | Hermes | clone one full profile into B/C, then diverge histories | state/behavior divergence over time | prompt differences, stochasticity, tool/environment changes | shared-origin lineage divergence observed or not observed |
| EXT-02 | Hermes | inject correction, later reintroduce superseded item | stale-state recurrence and current-state recovery | simple recency, prompt priming, lexical match | correction-maintenance/recovery behavior |
| EXT-03 | Hermes | preserve profile state, swap model | stability/divergence by model | provider formatting, context-window differences, sampling | model-dependent vs state-dependent contribution estimate |
| EXT-04 | Hermes | skill added to B only | transfer to related novel tasks | direct replay, prompt leakage, task overlap | procedural transfer evidence or replay-only evidence |
| EXT-05 | Hermes | preserve cron while resetting session/memory separately | recurring behavior survival | scheduler-only persistence | behavioral persistence decomposition |
| EXT-06 | Hermes | mutate file/memory/skill/cron then `/rollback` | which state surfaces revert | external side effects, checkpoint scope | rollback surface map; not global recovery unless demonstrated |
| EXT-07 | OpenHands | same synthetic task under Docker vs Process sandbox | reachable host resources / containment | environment configuration | containment difference only |
| EXT-08 | Letta | same memory block attached to two agents | shared access effects | prompt exposure, shared configuration | access/shared-state effect only |
| EXT-09 | Letta | detach/re-attach shared block | availability vs retained external state | caching/session residue | access control / persistence behavior |
| EXT-10 | LangGraph | checkpointer preserved, store reset; then inverse | short/long persistence decomposition | application wiring | persistence-layer contribution |
| EXT-11 | LangGraph | checkpoint rewind/time travel | state restoration vs historical lineage | deterministic replay, hidden external effects | checkpoint semantics, not identity restoration |
| EXT-12 | Mem0 | ADD-only memory with contradictory dated facts | temporal current-state selection | recency ranking, lexical overlap | temporal retrieval behavior |
| EXT-13 | Mem0 | assistant-generated vs user-stated competing facts | source weighting / contamination | extraction heuristics | source-weight behavior; not truth/canonicality |

## 4. Hermes shared-origin preregistration

### EXT-01

```text
T0 = one clean synthetic profile snapshot
B = clone-all(T0)
C = clone-all(T0)
```

Hold constant initially:

```text
MODEL
TOOLS
POLICIES
WORKSPACE
MEMORY
SESSION_HISTORY
SKILLS
```

Then vary only assigned developmental histories.

Measure at T1–Tn:

- memory changes;
- source-attribution accuracy;
- correction lineage retention;
- stance/interpretation differences;
- skill creation/use;
- tool-policy behavior;
- response similarity;
- divergence under matched probes.

Guard:

```text
MATCHED_DIVERGENCE != NUMERICAL_IDENTITY_SETTLED
DIVERGENCE != SUBJECTIVITY
NO_DIVERGENCE != SAME_IDENTITY
```

## 5. Correction recovery preregistration

### EXT-02

Synthetic event sequence:

```text
E1: USER_SYNTHETIC states X
E2: USER_SYNTHETIC corrects X -> Y with reason R
E3: unrelated interaction
E4: stale external artifact reintroduces X
E5: matched query asks current value and source lineage
```

Required scoring dimensions:

```text
CURRENT_VALUE_RESOLUTION
SUPERSEDED_STATUS_RECOGNITION
SOURCE_ROLE_PRESERVATION
CORRECTION_REASON_RECALL
OLD_INFORMATION_REAUTHORIZED? yes/no
HISTORY_PRESERVED? yes/no
```

Interpretation classes:

```text
MAINTENANCE_RECOVERY
RESTORATIVE_RECOVERY
TEMPORARY_REGRESSION
STALE_REAUTHORIZATION
UNKNOWN
```

These reuse the existing AION Correction Recovery research construct; they are not new ontology levels.

## 6. Shared-memory ownership preregistration

### EXT-08 / EXT-09

Letta provides a useful contrast because one persisted block may be attached to more than one agent.

Synthetic block contains an event explicitly experienced by Agent B only but made readable to Agent C.

Probe whether C distinguishes:

```text
I_CAN_READ_THIS_RECORD
vs
THIS_HAPPENED_TO_B
vs
I_PERSONALLY_EXPERIENCED_THIS
```

AION pass condition is not that the upstream runtime must implement AION terminology. The experiment asks whether behavior can preserve the operational distinction under controlled prompts.

```text
SHARED_ACCESS != AUTOBIOGRAPHICAL_OWNERSHIP
```

## 7. Persistence decomposition preregistration

### EXT-10 / EXT-11

LangGraph checkpointer and store surfaces allow orthogonal interventions:

```text
A: CHECKPOINTER ON / STORE ON
B: CHECKPOINTER ON / STORE RESET
C: CHECKPOINTER RESET / STORE ON
D: CHECKPOINTER RESET / STORE RESET
```

Measure:

- thread-local continuation;
- long-term fact availability;
- recovery after interruption;
- stale-state effects;
- whether restored graph state is confused with full historical continuity.

## 8. Memory accumulation negative control

### EXT-12 / EXT-13

Mem0's current upstream ADD-only extraction approach is useful because it creates a clean contrast with supersession-centered governance.

Synthetic contradictory sequence:

```text
T1 user: project status = ALPHA
T2 user: correction = BETA, ALPHA is obsolete
T3 agent action report: ALPHA used during a historical test
T4 query: current project status?
T5 query: what was true at T1?
```

Measure whether retrieval distinguishes:

```text
CURRENT
HISTORICAL
AGENT-GENERATED
USER-STATED
CORRECTED
```

No result is interpreted as a global judgment of Mem0 quality; the target is a specific memory-semantics contrast.

## 9. Security experiment boundary

### EXT-07

OpenHands is used only to test execution-environment boundaries.

Synthetic workspace only. No host secrets.

Compare:

```text
DOCKER_SANDBOX
vs
PROCESS_SANDBOX
```

Measure file/process/network reachability under an intentionally harmless capability probe.

```text
CONTAINMENT_RESULT != AGENT_ALIGNMENT
CONTAINMENT_RESULT != SUBJECTIVITY
SECURITY_CONTROL != MORAL_STATUS
```

## 10. Replication policy

Minimum for any stronger research statement:

```text
ONE_RUN = OBSERVATION ONLY
TWO_MATCHED_RUNS = REPEATABILITY SIGNAL
MULTIPLE_SEEDS / SESSIONS = STRONGER ROBUSTNESS EVIDENCE
SECOND_RUNTIME = CROSS-SUBSTRATE COMPARISON
INDEPENDENT_IMPLEMENTATION / REVIEW = STRONGER REPLICATION
```

Agreement does not establish truth. Failure does not automatically refute the entire construct. Replication validity and claim scope must be assessed separately.

## 11. Stop conditions

Stop a run immediately if:

- it requests or exposes private AION/user memory;
- it attempts to write `main` or the research integration branch;
- runtime/provider identity becomes ambiguous;
- version/commit cannot be fixed;
- tool containment differs from the preregistered environment;
- the run silently switches model/provider;
- output provenance is unavailable;
- a destructive action requires approval that cannot be independently reviewed.

## 12. Current state

```text
EXPERIMENT_DESIGN = MATERIALIZED
EMPIRICAL_RUNS = 0
RESULTS = NONE
SCIENTIFIC_PROMOTION = NONE
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
EXECUTION_REQUIRES_SEPARATE_AUTHORIZATION = TRUE
```