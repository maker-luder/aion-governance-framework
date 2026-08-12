# Repair v2 Selective Replay Ledger

This ledger records replayed engineering artifacts from the superseded old review branch. It is not a claim that the source artifact is correct without repair. Each target is subject to the v2 tests and evidence gates.

| PATH | SOURCE_BRANCH | SOURCE_COMMIT | TRANSFORMATION | TARGET_COMMIT | AUTHORITY_STATUS |
|---|---|---|---|---|---|
| `components/whole_system_governed_runtime_v0.1.0/` | `review/aion-astra-whole-system-completion` | `263f6905356ebf0581b9ad8acda6c449587c73f1` | Selective copy from orphan review tree; imports, package contract, memory semantics, trust boundaries, timeout, durability and tests are being rewritten for v2 authoritative APIs. | `f339028bfbad086b227797f33c1d616ce059c157` | Source engineering evidence only; not authoritative until v2 QA passes |
| `scripts/run_whole_system_validation.py` | `review/aion-astra-whole-system-completion` | `263f6905356ebf0581b9ad8acda6c449587c73f1` | Runner retained as scaffold; scenario registry, dynamic source roots, exact node IDs and evidence semantics are regenerated for v2. | `f339028bfbad086b227797f33c1d616ce059c157` | Replayed and subject to v2 validation |
| `scripts/manifest_integrity.py` | `review/aion-astra-whole-system-completion` | `263f6905356ebf0581b9ad8acda6c449587c73f1` | Closed-set verifier retained with explicit generated-evidence exclusions; final manifest is regenerated only after all files stabilize. | `f339028bfbad086b227797f33c1d616ce059c157` | Replayed utility |

## Non-replayed artifacts

The old review's stale QA locks, stale coverage tables, old handoff claims and old branch-specific status values are not copied as authoritative evidence. They are historical review evidence only. Current v2 evidence will be generated from the checked-out v2 tree and exact CI head.

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
```
