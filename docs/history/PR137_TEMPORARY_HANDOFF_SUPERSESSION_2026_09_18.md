# PR #137 temporary handoff supersession — 2026-09-18

Status: `HISTORICAL_FOLLOW_UP / OPERATIONAL_HANDOFF_SUPERSEDED / NO_RESEARCH_CLAIM`

```text
BASE_MAIN = 579906fe87ad95b12cb8751ef42e0b924e41b4af
PR137_TEMPORARY_HANDOFF = RETAINED_AS_HISTORY
PR137_NEXT_TASK_GUIDANCE = SUPERSEDED
PR136 = CLOSED_UNMERGED_HISTORICAL_CANDIDATE
CANONICAL_IMPLEMENTATION_SOURCE = CURRENT_MAIN
```

## 1. Purpose

PR #137 added `docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md` as a deliberately temporary recovery guide after PR #136 was closed without merge.

That document explicitly required future review and supersession once later accepted implementations resolved or revised the listed gaps.

This follow-up performs that operational closeout. It does not edit or erase the original handoff because the original record remains important repository history.

```text
SUPERSEDE_OPERATIONAL_USE != DELETE_HISTORY
```

## 2. Canonical successor chain

The recovery work recorded by PR #137 was subsequently implemented through:

```text
PR #139
research: reimplement task-selection harness with yoked exposure controls
MERGE_COMMIT = 686a6ed5a8d3d287d144a80ad58749391562018d

PR #140
research: harden task-selection opportunity and transfer controls
MERGE_COMMIT = 6e5254bd35e8ed2df7b937cd5a134f892c874b79
```

Current `main` later advanced through PR #143 and is the only source of truth for current behavior.

## 3. PR #137 handoff item disposition

### 3.1 Free-selection divergence admission bug

**Disposition: RESOLVED BY PR #139**

Current canonical audit records free-selection divergence as an observed derived result rather than an admission requirement.

```text
FREE_SELECTION_NULL = VALID
REALIZED_DIVERGENCE = OBSERVED_RESULT
REALIZED_DIVERGENCE != DESIGN_ADMISSION_REQUIREMENT
```

### 3.2 True yoked / matched exposure

**Disposition: RESOLVED BY PR #139**

Each anonymous pair contains one `FREE_SELECTION` unit and one `YOKED_ASSIGNED_EXPOSURE` unit. The yoked unit must receive the exact realized domain/family/payload exposure sequence of its paired free unit.

### 3.3 Protocol / schedule / realized-choice / exposure separation

**Disposition: RESOLVED BY PR #139**

Current canonical structures separately bind:

```text
selection_protocol
realized_choice_trace
assignment_schedule
realized_exposure_trace
execution_record
```

### 3.4 Exposure unit semantics and zero-domain exposure

**Disposition: RESOLVED STRUCTURALLY BY PR #139**

The current bounded unit is `TASK_EPISODE`; per-domain zero exposure is representable, while the total realized exposure trace remains non-empty.

```text
TASK_EPISODE_COUNT != EQUAL_DURATION
TASK_EPISODE_COUNT != EQUAL_DIFFICULTY
TASK_EPISODE_COUNT != EQUAL_LEARNING_OPPORTUNITY
```

### 3.5 Hash semantics

**Disposition: RESOLVED STRUCTURALLY BY PR #139**

`BoundArtifact` recomputes SHA-256 from supplied UTF-8 content and fails closed on mismatch.

```text
HASH_MATCH = SUPPLIED_CONTENT_INTEGRITY_CHECK
HASH_MATCH != SCIENTIFIC_SEMANTICS_VALIDATED
```

### 3.6 Design unit and pairing model

**Disposition: RESOLVED BY PR #139**

The canonical bounded design is explicitly:

```text
BETWEEN_UNIT_YOKED_PAIR
```

with anonymous `pair_id` and separate study-unit identities.

## 4. Post-PR #139 hardening findings

A strict post-merge review of PR #139 found three additional structural gaps. PR #140 addressed them additively.

### 4.1 Event-level choice opportunity

**Disposition: RESOLVED BY PR #140**

Every free-selection event now requires a canonically bound opportunity set with multiple distinct alternatives, and the realized choice must belong to that set.

### 4.2 Execution identity vs content equality

**Disposition: RESOLVED BY PR #140**

Independent execution identity no longer requires byte-different execution-record contents.

```text
SEPARATE_EXECUTION_IDENTITY != CONTENT_MUST_DIFFER
```

### 4.3 Held-out challenge strength

**Disposition: RESOLVED STRUCTURALLY BY PR #140**

The bounded contract distinguishes:

```text
WITHIN_FAMILY_PAYLOAD_HOLDOUT
CROSS_FAMILY_CHALLENGE
```

Neither establishes empirical transfer or domain generalization.

## 5. What remains unresolved

Superseding the temporary handoff does **not** mean the underlying scientific hypotheses are established.

The temporal-provenance and causal-identification layer remains specification-bound rather than empirically populated.

```text
TEMPORAL_ORDER != CAUSALITY
PROCESS_TRACE != CAUSAL_PROOF
YOKED_CONTROL != CAUSAL_IDENTIFICATION_COMPLETE
HELD_OUT_CHALLENGE != HUMAN_TRANSFER_ESTABLISHED

HUMAN_LEARNING = NOT_ESTABLISHED
CAUSAL_EFFECT = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
```

## 6. Future recovery instruction

Future sessions should no longer use the PR #137 handoff as the current implementation to-do list.

Instead:

```text
1. READ LIVE MAIN
2. READ CURRENT CANONICAL TASK-SELECTION IMPLEMENTATION
3. TREAT PR #136 AND PR #137 AS HISTORICAL RECOVERY EVIDENCE
4. TREAT PR #139 AND PR #140 MERGED RESULTS AS CANONICAL ANCESTRY
5. RECHECK LIVE STATE BEFORE ANY NEW CHANGE
```

The original handoff remains useful for explaining why the later implementation looks the way it does, including the documented correction of earlier Human Owner and implementation-side reasoning errors.

```text
HISTORICAL_ERROR_RECORD = RETAINED
OPERATIONAL_NEXT_TASK_STATUS = SUPERSEDED
```
