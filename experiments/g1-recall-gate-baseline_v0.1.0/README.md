# Minimal Recall-Gate Contrast Experiment v0.1.0

## Research question

Does the existing Memory Recall Gate prevent clearly invalid cue-matching records from entering the eligible recall set compared with a naive cue-overlap selector?

This is a **software control experiment**. It does not test consciousness, subjective memory, or full model-level interpretation drift.

## Conditions

**M0 — naive cue recall:** select any record with entity/topic cue overlap; no provenance, identity, access, supersession or conflict gate.

**M1 — governed recall:** apply the existing `aion_memory_recall.decide_recall()` checks for inactive/superseded state, user/agent identity, access scope, provenance verification, unresolved conflict and cue relevance.

## Synthetic fixture

Six cue-matching records: valid, superseded, provenance-incomplete, unresolved-conflict, wrong-subject and inaccessible-private.

## Expected result

```text
M0_NAIVE_SELECTED = 6
M1_ELIGIBLE = 1
M1_BLOCKED_OR_QUARANTINED = 5
```

Expected M1 dispositions:

```text
valid       -> RECALL_ALLOWED_TEMPORARY_ONLY
superseded  -> RECALL_DENIED_PROVENANCE_FAILURE
badprov     -> RECALL_DENIED_PROVENANCE_FAILURE
conflict    -> RECALL_QUARANTINED_CONFLICT
wrongid     -> RECALL_DENIED_IDENTITY_MISMATCH
private     -> RECALL_DENIED_ACCESS_SCOPE
```

## Run

From repository root:

```bash
python experiments/g1-recall-gate-baseline_v0.1.0/run_experiment.py
```

No network access, model call or persistent writeback is required.

## Interpretation

A passing result establishes only that the existing gate blocks this synthetic class of invalid cue-matching recall candidates. It does not establish full Interpretation Drift prevention, whole-system validation, an LLM behavioral effect, independent IV&V, subjectivity, identity continuity or genuine recollection.
