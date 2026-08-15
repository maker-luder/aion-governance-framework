# Historical Documentation Archive

This directory preserves dated, event-specific, incident, reconciliation, branch, release, C0, and other historical records. These files are retained because provenance and auditability matter. Their presence does not make them current, and their relocation does not make them invalid.

## Reading rules

`HISTORICAL_RECORD != CURRENT_STATUS`

`MOVE != REWRITE`

`ARCHIVE != INVALID`

`ARCHIVE != DELETE`

`OLD_FAILURE != CURRENT_FAILURE`

A historical file may accurately describe an older branch list, workflow state, candidate status, owner direction, acceptance state, incident, or process deviation. Current repository status must be read from [`../README.md`](../README.md), [`../RELEASE_STATUS.md`](../RELEASE_STATUS.md), and [`../governance/README.md`](../governance/README.md), not inferred from a dated archive filename.

## Archive sections

- [`c0/`](c0/README.md) contains dated C0 acceptance, calibration, review, and HOLD records.
- [`incidents/`](incidents/README.md) contains PR-specific, authority, closure, and reconciliation records.
- [`branch-and-release/`](branch-and-release/README.md) contains freeze and branch-disposition snapshots.
- [`reconciliation/`](reconciliation/README.md) contains dated implementation, runtime, policy-cycle, and stabilization records.
- [`other/`](other/README.md) contains other dated checkpoints and superseded directions that remain provenance-bearing.

The archive is not a deletion queue. Any future deletion proposal must separately identify `DELETION_CANDIDATE = REVIEW_REQUIRED` and receive Human Owner plus independent review; this convergence performs no deletion.
