# Task-selection exposure harness

Status: `BOUNDED_STRUCTURAL_HARNESS / SYNTHETIC_ONLY / SCIENTIFIC_HOLD`

This extension operationalizes one narrow part of the 2026-09-17 task-selection / domain-specific Human–AI learning hypothesis. It does not run a Human study and does not call an AI model.

## Research question represented

```text
SAME_OR_SIMILAR_PRODUCT_ACCESS
!= SAME_EFFECTIVE_EXPOSURE
```

The structural design asks whether a later empirical study can hold access, model configuration, tool availability, evaluator, prior-knowledge control, time budget, task difficulty and resource-cost information fixed while representing different longitudinal task-exposure distributions.

The implementation supports two synthetic regimes:

```text
FREE_SELECTION
MATCHED_ASSIGNED_EXPOSURE
```

and two anonymous synthetic tracks:

```text
TRACK_A
TRACK_B
```

The tracks are not people and do not encode third-party identity. In the deterministic fixture, the free-selection tracks deliberately have different domain exposure distributions while the matched-assigned tracks have the same distribution and the same exposure payloads.

The regime labels are not accepted by themselves. Each regime must bind to one exact `selection_protocol_sha256`, and the two regimes must have content-distinct protocol bindings. Each arm also binds an exact `selection_trace_sha256`. The matched-assigned tracks require one identical assignment trace; the free-selection tracks require distinct synthetic selection traces.

```text
REGIME_LABEL != SELECTION_PROTOCOL_BINDING
EXPOSURE_VECTOR != SELECTION_TRACE
SYNTHETIC_SELECTION_TRACE != HUMAN_CHOICE_OBSERVED
```

## Domains

```text
IMAGE_VISUAL
CREATIVE_TEXT
RESEARCH_PROVENANCE
GIT_ENGINEERING
```

These are study-design labels. They are not measurements of intelligence, education, worth, personality, or general AI literacy.

## Fail-closed controls

`audit_task_selection_exposure_design()` requires:

- exactly one arm for every `SelectionRegime x SyntheticTrack` cell;
- exact enum instances rather than raw strings;
- exactly one exposure record per task domain in every arm;
- one exact protocol binding within each regime and content-distinct protocol bindings across regimes;
- one exact assigned-selection trace across the two matched-assigned tracks;
- content-distinct synthetic selection traces across the two free-selection tracks;
- identical access, model, tool, evaluator, prior-knowledge, time-budget, task-difficulty and resource-cost-information bindings across arms;
- identical task-family binding for each domain across all arms;
- equal total exposure units across arms;
- identical exposure distributions and exact exposure payloads across the two matched-assigned tracks;
- different effective exposure distributions across the two free-selection tracks;
- one held-out synthetic transfer task per domain;
- held-out task-family binding matched to the exposure family;
- held-out payloads distinct from all exposure payloads;
- zero model invocation, zero Human observation, no Human identity and no private material.

## Why H-RA1 is not implemented as a manipulation

The research note records a Human Owner self-report that perceived resource cost can affect which AI tasks feel worth repeating. That is a candidate moderator, not an established mechanism.

This v0.1.0 harness therefore holds `resource_cost_information_sha256` constant across arms instead of pretending that a valid resource-cost manipulation has already been designed.

```text
RESOURCE_COST_INFORMATION_CONTROLLED = YES
H_RA1_EMPIRICAL_TEST = NO
```

A later H-RA1 study would require a separately reviewed manipulation, outcome definition, ethical decision, and empirical protocol.

## Evidence boundary

The code can establish only that a synthetic study design satisfies its declared structural controls.

```text
STRUCTURAL_QA_PASS != H_TS1_CONFIRMED
STRUCTURAL_QA_PASS != H_DL1_CONFIRMED
SAME_ACCESS_BINDING != REAL_WORLD_EQUAL_ACCESS
SELECTION_PROTOCOL_BOUND != HUMAN_FREE_CHOICE_OBSERVED
SYNTHETIC_SELECTION_TRACE != HUMAN_SELECTION_HISTORY
SYNTHETIC_EXPOSURE_DIVERGENCE != HUMAN_SELF_SELECTION_OBSERVED
HELD_OUT_TASK_BINDING != HUMAN_TRANSFER
DOMAIN_FLUENCY != GENERAL_AI_LITERACY
AI_ASSISTED_OUTPUT != HUMAN_LEARNING
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

## Privacy boundary

The harness does not contain the private conversation that generated the hypothesis, does not name the third-party comparison participant, and rejects synthetic records that declare Human identity or private material.

```text
RAW_PRIVATE_TRANSCRIPT = NOT_PUBLISHED
THIRD_PARTY_IDENTITY = NOT_RECORDED
MODEL_INVOCATION = FALSE
HUMAN_PARTICIPANT_OBSERVATION = FALSE
```
