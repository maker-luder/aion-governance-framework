# Task-selection yoked-exposure harness

Status: `BOUNDED_STRUCTURAL_QA / SYNTHETIC_ONLY / SCIENTIFIC_HOLD`

This harness is the corrected implementation successor to the closed, unmerged PR #136 candidate. It must be read with:

- `../../docs/research/TASK_SELECTION_YOKED_CONTROL_AND_TEMPORAL_PROVENANCE_2026_09_17.md`
- `../../docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md`

The old PR #136 branch remains historical evidence only.

## Design contract

The design uses anonymous between-unit yoked pairs:

```text
PAIR_i
├─ FREE_SELECTION unit
└─ YOKED_ASSIGNED_EXPOSURE unit
```

For each pair, the assigned unit must receive the exact task-domain, task-family and exposure-payload sequence realized by the free-selection unit.

```text
FREE_REALIZED_EXPOSURE_SEQUENCE_i
==
YOKED_ASSIGNED_REALIZED_EXPOSURE_SEQUENCE_i
```

The principal represented design difference is task-selection control being available versus unavailable. That structural match does not establish randomization, exchangeability or a causal effect.

## Valid null outcomes

The harness never requires free-selection units to diverge.

Two free units may independently realize identical domain distributions or identical choice traces. The audit reports whether domain-count divergence was observed, but admission does not depend on it.

```text
FREE_SELECTION_NULL != DESIGN_FAILURE
OBSERVED_DIVERGENCE != ADMISSION_REQUIREMENT
```

## Trace separation

The implementation separates:

- `selection_protocol`
- `realized_choice_trace`
- `assignment_schedule`
- `realized_exposure_trace`
- `execution_record`

`FREE_SELECTION` requires a realized choice trace and forbids an assignment schedule.

`YOKED_ASSIGNED_EXPOSURE` requires an assignment schedule and forbids a claimed realized choice trace.

Each unit requires its own execution record even when another unit has the same schedule or realized choices.

## Exposure unit

`ExposureUnitKind.TASK_EPISODE` means one represented bounded synthetic task episode.

Per-domain exposure counts are derived from the event trace. A domain may have zero episodes. Each unit must contain at least one episode overall.

Event counts are comparable as counts only:

```text
TASK_EPISODE_COUNT != DURATION
TASK_EPISODE_COUNT != DIFFICULTY
TASK_EPISODE_COUNT != TOKEN_COST
TASK_EPISODE_COUNT != COGNITIVE_LOAD
TASK_EPISODE_COUNT != LEARNING_OPPORTUNITY
```

## Artifact binding

`BoundArtifact` contains UTF-8 content plus an explicitly supplied SHA-256 digest. Object construction recomputes SHA-256 and rejects a mismatch.

This is stronger than digest-shape checking, but still bounded:

```text
HASH_MATCH = SUPPLIED_CONTENT_DIGEST_INTEGRITY
HASH_MATCH != SEMANTIC_VALIDITY
HASH_MATCH != EXTERNAL_FILE_EXISTENCE_PROVEN
HASH_MATCH != AUTHORSHIP_PROVEN
HASH_MATCH != SCIENTIFIC_VALIDATION
```

## Controls

The current structural audit holds these content bindings fixed across all units:

- exposure-unit definition;
- access profile;
- model configuration;
- tool access;
- evaluator payload;
- prior-knowledge control;
- time-budget control;
- task-difficulty control;
- resource-cost information.

This means only that the synthetic records declare and bind the same control artifacts. It does not prove real-world equality of those conditions.

## Held-out tasks

The harness requires exactly one held-out task record per declared task domain. Held-out evaluator binding must match the study evaluator, and any task family that appears in exposure events must remain consistent with the held-out family binding for that domain. Held-out payloads must be content-distinct from all exposure payloads.

```text
HELD_OUT_PAYLOAD_SEPARATION != HUMAN_TRANSFER_ESTABLISHED
```

## Temporal provenance

The Python implementation records only that a temporal-provenance specification is bound conceptually. It does not populate Human longitudinal events or estimate causal paths.

The research specification preserves the ordering:

```text
T0 PRIOR_STATE
T1 GOALS / VALUES / PRIOR_KNOWLEDGE
T2 TASK_SELECTION_OR_ASSIGNMENT
T3 REALIZED_EXPOSURE
T4 FEEDBACK / CORRECTION / REPETITION
T5 HELD_OUT_ASSESSMENT
T6 OBSERVED_DOMAIN_FLUENCY
```

```text
TEMPORAL_ORDER != CAUSALITY
PROCESS_TRACE != CAUSAL_PROOF
```

## Tests required by the PR #136 closeout

The test suite includes positive and negative cases for:

1. true free-to-yoked exposure matching;
2. valid free-selection null outcomes;
3. zero exposure in individual domains;
4. schedule-to-exposure and choice-to-exposure binding;
5. identical free-choice traces remaining admissible;
6. actual content/digest mismatch rejection;
7. complete anonymous pair structure;
8. distinct per-unit execution records;
9. control drift;
10. protocol drift and protocol collapse;
11. held-out family/payload separation;
12. privacy, empirical-observation and exact-enum boundaries.

## Evidence ceiling

A passing test suite means the implementation conforms to the declared structural contract for the tested cases. It does not establish the research hypothesis.

```text
TEST_PASS != RESEARCH_DESIGN_VALID_IN_ALL_RESPECTS
CI_PASS != SCIENTIFIC_VALIDATION
STRUCTURAL_QA_PASS != EMPIRICAL_RESULT
YOKED_CONTROL != CAUSAL_IDENTIFICATION_COMPLETE
TASK_SELECTION != HUMAN_LEARNING
HUMAN_LEARNING != AI_SUBJECTIVITY

H_TS1 = NOT_ESTABLISHED
H_DL1 = NOT_ESTABLISHED
H_RA1 = NOT_TESTED_BY_THIS_HARNESS
HUMAN_LEARNING = NOT_ESTABLISHED
CAUSAL_EFFECT = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

No model is invoked, no Human participant is observed, and no private transcript or third-party identity belongs in this harness.