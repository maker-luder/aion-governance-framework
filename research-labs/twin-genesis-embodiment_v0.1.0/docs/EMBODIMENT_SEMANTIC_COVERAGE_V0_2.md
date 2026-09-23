# Phase A v0.2 embodiment semantic coverage contract

## Status boundary

- `ENGINEERING_PASS != SCIENTIFIC_VALIDATION`
- `SUBJECTIVITY = NOT_ESTABLISHED`
- `SCIENTIFIC_DISPOSITION = HOLD`
- `CANONICAL_EFFECT = NONE`
- `DEPLOYMENT = FALSE`
- Phase B is not entered by this contract.

## Exact archive bindings

| PR | Exact source head |
|---:|---|
| #190 | `066ed1afccebee869eb658c09691b7f096694332` |
| #191 | `48bcf45a55a0b67dfc0e7b9cd838c5f9068b08d2` |
| #192 | `861e6a556a21afffd04b187714c0608fe73ea4fc` |
| #202 | `7f84ae8c95f1b7caaaa0c3850a0b6cfd049b7108` |

Each source and supporting artifact is bound to both its exact archive head and
its Git blob SHA. Each Python top-level definition is a separate semantic unit;
file-level and multi-module catch-all buckets are absent.

## Resolved 14 / 15 / 16 ambiguity

The prior heading that said 14 conflicted with the listed module inventory. The
v0.2 inventory derives the counts from exact source artifacts:

1. #192 has **19** reviewed implementation modules.
2. Of those, **17** have a `teacher_` prefix; the two role-neutral modules are
   `governance_epistemics.py` and `physiology.py`.
3. The v0.1 ledger explicitly named **4** #192 modules.
4. Therefore #192 had **15** implementation modules without an explicit v0.1
   row: `19 - 4 = 15`.
5. #202 adds **1** external sensorimotor implementation module.
6. The combined formerly unexplicit source-module count is **16**: `15 + 1`.

## Independent dimensions

`classification` records semantic ownership type:

- `SHARED_CORE`
- `ROLE_SPECIFIC_EXTENSION`
- `EXTERNAL_DEFERRED`
- `ARCHIVE_RECORD`

`disposition` records Phase A action:

- `ADOPTED`
- `DEFERRED`
- `SUPERSEDED`
- `ARCHIVE_ONLY`

A unit may therefore be classified `SHARED_CORE` while remaining `DEFERRED`.
The final matrix forbids `MISSING_UNACCOUNTED` rather than hiding it in another
classification.

## #202 boundary

#202 is bound to its exact source, protocol, schema, and test blobs. Every #202
semantic unit is `EXTERNAL_DEFERRED / DEFERRED`, has no active target, and is
not imported or modified by Phase A v0.2.

## Canonicalization and verification

Canonical order is fixed before hashing:

1. `source_pr`
2. `source_path`
3. `semantic_unit_id`

Within each semantic unit, embodiment axes follow the declared axis order and
supporting artifact identifiers are lexically sorted. The canonical content
hash is order-independent for the two collections but changes when semantic
content changes.

Run the exact binding verifier from the repository root:

```bash
python research-labs/twin-genesis-embodiment_v0.1.0/scripts/verify_coverage_matrix_v0_2.py
```

The completion gates are:

- `MISSING_UNACCOUNTED_COUNT = 0`
- `DUPLICATE_SEMANTIC_OWNERSHIP = 0`
- `UNCOVERED_SOURCE_MODULE_COUNT = 0`
- all exact source/support blobs exist
- all adopted active targets exist
- all superseded replacement paths exist
