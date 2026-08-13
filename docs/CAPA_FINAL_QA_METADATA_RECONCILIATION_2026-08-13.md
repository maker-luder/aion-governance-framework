# CAPA — Final QA Metadata Reconciliation — 2026-08-13

## Detection and classification

```text
FAILURE_MODE = STALE_AUTHORITATIVE_METADATA
TASK_BOUNDARY_FAILURE = FALSE
IMPLEMENTATION_SOURCE_DRIFT = FALSE
TESTED_SUBJECT_HEAD = 8dd022f805f4eab9593ee64dc2db93155a55079d
```

The final QA receipt and current test reconciliation reported the discovered current target surface as `50` eligible/current targets, `47` tested targets, `3` explicit non-applicable targets and `920` passed tests. A separate `qa/CURRENT_RELEASE_STATUS_LOCK.json` still contained the superseded `48 / 46 / 2` counts, while `qa/CI_APPLICABILITY.md` still described an older `review/aion-astra-whole-system-completion-v2` handoff.

This was a current-evidence consistency failure, not an implementation or scientific-result failure. The stale values were preserved in the working-tree diff before correction and were not silently treated as current truth.

## Contributing cause

The authoritative QA orchestrator refreshed the dynamic test matrix and reconciliation artifacts but did not rewrite every older status/prose artifact that had been generated for a prior review branch. The mismatch was therefore between evidence producers with different update lifecycles.

## Corrective action

The release lock now states `50 / 47 / 3`, retains `920 PASSED`, and remains bound to `TESTED_SUBJECT_HEAD = 8dd022f805f4eab9593ee64dc2db93155a55079d`. The CI applicability document was rewritten for the final formal-research tree. Historical v2 material is explicitly described as historical and no untriggered workflow is promoted to success.

The existing final QA receipt remains the exact-head authority for A. The correction commit is evidence-only and does not claim that the correction commit itself was tested as the implementation subject. Remote CI must be re-checked against the correction commit's published head before the final report.

## Revalidation boundary

The preceding full exact-head QA against A had `25/25` applicable gates pass with `0` failures. After the evidence-only correction, bounded non-mutating checks are used to verify scope lock, autonomous-growth contract, public/sensitive/stale scans, manifest verification and evidence regressions. Any generated current-state artifacts remain bound to A; no source implementation or local-only model checkpoint is added.

## Status

```text
CAPA_STATUS = CORRECTED_PENDING_REMOTE_CI_ON_CORRECTION_HEAD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
```
