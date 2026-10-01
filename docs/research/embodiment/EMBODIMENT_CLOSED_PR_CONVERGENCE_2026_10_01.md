# Embodiment Closed-PR Convergence Ledger — 2026-10-01

## Purpose

This ledger reconciles closed embodiment-related pull requests without reopening historical branches or treating file absence as capability absence.

It distinguishes repository history, semantic succession, independent research archives, and unresolved deltas.

Core rules:

`CLOSED_PR != DEAD_CODE`

`MISSING_FILE != MISSING_CAPABILITY`

`DIVERGED_BRANCH != MUST_MERGE`

`ABSORBED_BY_SUCCESSOR` requires commit ancestry or file/semantic evidence.

`SEMANTICALLY_SUPERSEDED` means the older responsibility is materially represented by a later implementation under a different file/API shape.

`PRESERVED_INDEPENDENT_ARCHIVE` means the record remains historically useful but is not part of the active successor lineage.

`REQUIRES_SEMANTIC_RECONCILIATION` means repository evidence is insufficient to call the old delta absorbed, superseded, or obsolete.

This document is a governance/audit artifact only.

`MERGE_TO_MAIN = NO`

`DEPLOYMENT = FALSE`

`CANONICAL_EFFECT = NONE`

## Head semantics

Closed PR metadata and the live branch can diverge after a PR is closed.

Therefore this ledger distinguishes:

- `PR_RECORDED_HEAD`: the head SHA stored on the closed PR object;
- `LIVE_BRANCH_HEAD`: the current head of the PR branch when that branch still exists;
- `HEAD_RELATION`: whether the branch advanced after the PR snapshot.

Known cases in this audit:

- PR #203: recorded `ab54d99a11b32b10cfcb76c385c023b0caa7f14d`; live branch `5c3877adcfc1f7d67e8700fdac26b13c5c202a43`; +6 post-close commits.
- PR #236: recorded `d08c7197e4c3511b1942e80e99dcf78589c49d87`; live branch `d8d10961f777d782c13f5907d11c1d0a609a408c`; +2 post-close commits.
- PR #251: recorded `db8167cbe600f41beea76c8c3e78c6bc9ec331f2`; live branch `26c8cb74a10f99696a36a8ac387ee78c66da1dee`; +6 post-close commits, and that live branch head equals PR #253's recorded head.

A lifecycle conclusion must specify which head it is evaluating.

## Status vocabulary

- `MERGED_CANONICAL_HISTORY`: PR is closed because it was merged; it is not an unresolved closed-PR artifact.
- `ABSORBED_BY_SUCCESSOR`: later PR head contains the earlier PR head through ancestry, or all relevant touched paths/semantics are demonstrably carried forward.
- `SEMANTICALLY_SUPERSEDED`: later implementation replaces the earlier responsibility without preserving the same file/API identity.
- `PRESERVED_INDEPENDENT_ARCHIVE`: intentionally separate historical research record; no forced merge is required.
- `LATEST_CLOSED_SUCCESSOR`: latest known closed/unmerged successor for a lineage; retained as the current research endpoint without implying merge to main.
- `DEFERRED_REENTRY_CANDIDATE`: historically bounded delta that is not carried by the active successor and is intentionally queued for a separately scoped re-entry rather than auto-merged.
- `PRESERVED_DEFERRED_SOURCE`: exact semantic provenance is intentionally retained for later admission; absence from the active surface is deliberate, not loss.
- `RESOLVED_BY_NEW_SUCCESSOR`: previously unresolved delta is materially resolved by a newly verified closed/unmerged successor.
- `REQUIRES_SEMANTIC_RECONCILIATION`: divergence or missing-path evidence remains and must be reviewed before any successor claim.
- `OUT_OF_SCOPE`: not part of this embodiment convergence batch.

## Canonical merged anchors

### PR #210

`research: define scientific embodiment master blueprint and toolchain`

Status: `MERGED_CANONICAL_HISTORY`

The PR is closed because it was merged. Do not treat it as an unresolved closed Draft.

### PR #211

`research: crosswalk external methodology and prerecord session stability pilot`

Status: `MERGED_CANONICAL_HISTORY`

The PR is closed because it was merged.

## Teacher lineage

### PR #192 → #241 → #250 → #251/#252 → #253 → #254

Status for #192, #241, #250, #251, #252, #253:

`ABSORBED_BY_SUCCESSOR`

For #251 specifically, the closed PR recorded head is `db8167cb...`, while its live branch later advanced to `26c8cb74...`, which equals PR #253's recorded final controller head.

Latest verified successor in this historical unmerged lineage:

- PR #254
- head `43d5d9760bc908c2367c717fdb70be0adbefc504`
- state: closed
- draft: true
- merged: false

Evidence:

- #192 is an ancestor of #241.
- #241 is an ancestor of #250.
- #250 is an ancestor of #251.
- #252 is an ancestor of #253.
- #251 is also an ancestor of #253.
- #253 is an ancestor of #254.

Important:

`ABSORBED_BY_SUCCESSOR != MERGED_TO_MAIN`

All of these successor claims describe closed research-branch lineage only.

### PR #240

`research: harden ChatGPT Teacher body evidence and verification`

Status: `SEMANTICALLY_SUPERSEDED`

The old `teacher_body_evidence.py` path is not present in #254, but the core responsibilities are represented later by `teacher_integrity.py` and the hardened Teacher lineage:

- deterministic reference-bundle fingerprinting;
- SHA-256 chained evidence receipts;
- reference asset vs production/physical/biological separation;
- fail-closed phenomenal/action-authority/canonical/deployment boundaries.

This is a semantic replacement, not a claim that every old class/API was preserved.

### PR #239

`feat(embodiment): integrate ChatGPT Teacher body v0.2 runtime and bundle`

Status: `RESOLVED_BY_NEW_SUCCESSOR`

Resolved by PR #256, exact head `8569c245f78815361363f9346d226c228a0b7596`.

PR #256 re-materializes the still-useful v0.2 integration semantics on top of the latest Teacher successor lineage without reviving the historical strict-schema / standalone-CLI shape wholesale. It adds an integrated v0.2 manifest surface, executable validation, CLI exposure, and dedicated reconciliation tests.

This classification does not claim file/API identity with PR #239.

### PR #236 / #238

PR #236 status: `PRESERVED_INDEPENDENT_ARCHIVE`

PR #238 status: `LATEST_CLOSED_SUCCESSOR`

These form an adult-reference lineage in `research-labs/affective-cognitive-motivation_v0.1.0`.

They are related to embodiment research but are not the Teacher body-runtime successor lineage. Do not force them into PR #254.

PR #236 is the design record. Its branch advanced by 2 commits after the PR snapshot, only modifying that design specification. PR #238 is the latest closed/unmerged implementation continuation found in this audit.

## Work lineage

### PR #237 → #246 → #248

Status for #237 and #246:

`ABSORBED_BY_SUCCESSOR`

PR #248 is the later closed/unmerged Work functional-state successor.

The ancestry is clean:

- #237 is an ancestor of #246;
- #246 is an ancestor of #248.

Again, this does not imply merge to main.

## Codex lineage

### PR #242 → #249

Status for #242:

`ABSORBED_BY_SUCCESSOR`

PR #249 is the later closed/unmerged Codex functional-state successor.

## AION / Astra lineage

### PR #244 → #245 → #247

Status for #244 and #245:

`ABSORBED_BY_SUCCESSOR`

The ancestry is clean through PR #247.

### PR #190

`research: record AION/Astra 3D male body reference candidates`

Status: `SEMANTICALLY_SUPERSEDED`

File-level review against PR #247 found all #190 touched paths still present; some were later modified.

This supports a semantic-successor interpretation even though the branch histories diverged.

### PR #191

`feat: record AION/Astra complete humanoid robotic embodiment package`

Status: `SEMANTICALLY_SUPERSEDED`

The old monolithic body-profile/pose package is not preserved file-for-file. Its responsibilities are re-materialized in #247 through AION/Astra anthropometry, whole-body state, dynamic physiology, reproductive topology, runtime binding, v0.2 schemas, reference rigs, and capability-parity surfaces.

This is a semantic replacement, not an assertion that the old API remains available.

## Shared synthetic-role lineage

### PR #193 → #243

Status for #193:

`ABSORBED_BY_SUCCESSOR`

PR #243 descends from #193.

### PR #243

`feat: shift Teacher Codex Work to young-adult presentation`

Status: `RESOLVED_BY_NEW_SUCCESSOR`

Successor: PR #257 at exact head `a1eedd764e5139ece69e29ba2fb6cd452e679ba4`.

The 25–29 synthetic visual-presentation decision is converged with the preserved cross-role geometry reference in #257. It remains presentation-only metadata and does not modify Teacher/Work/Codex functional runtimes.

### PR #194

`research: extend synthetic role genital geometry dynamics`

Status: `RESOLVED_BY_NEW_SUCCESSOR`

Successor: PR #257 at exact head `a1eedd764e5139ece69e29ba2fb6cd452e679ba4`.

PR #257 preserves the role-specific synthetic geometry data/doc/module/test semantics, repairs the historical literal-line-break syntax defect, and binds geometry to the Teacher/Codex/Work presentation body identifiers. Generic reproductive-sexual channels are not treated as substitutes for these geometry semantics.

## Sensorimotor / archive-convergence lineage

### PR #202

`feat: add synthetic sensorimotor embodiment audit`

Status: `PRESERVED_DEFERRED_SOURCE`

PR #203's live branch explicitly inventories PR #202 sensorimotor semantic units and marks them `KEEP_DEFERRED` / `DEFERRED_TO_PR_202`. The work remains a bounded deterministic synthetic QA source with `SCIENTIFIC_DISPOSITION = HOLD`; it is neither lost nor promoted into the active runtime.

### PR #203

`research: converge embodiment archives into active baseline`

Status: `LATEST_CLOSED_SUCCESSOR`

The closed PR object records an earlier snapshot, but its branch continued after closure. The live branch now contains an expanded convergence implementation with an active baseline, shared core, role-specific extensions, archive coverage matrix, materialization map, schemas, and tests.

Therefore this lineage is not treated as missing from #210; it is retained as its own latest closed/unmerged convergence endpoint.

## Adult sexual / intimacy research record

### PR #220

`docs(embodiment): record adult sexual and intimacy representation`

Status: `PRESERVED_INDEPENDENT_ARCHIVE`

The PR is a research/documentation record. Its single record file is not present by path in PR #238.

Current evidence does not justify rewriting it as an implementation predecessor or capability source. Preserve it as a historical research record unless a later semantic crosswalk explicitly absorbs it.

## Current unresolved reconciliation set

`REQUIRES_SEMANTIC_RECONCILIATION = 0` for the current ledger entries.

PR #256 is a narrowly scoped post-ledger successor that re-materializes the still-useful integrated Teacher v0.2 bundle surface from #239. Its final exact-head verification is tracked separately and does not reopen #239.

Independent records / latest endpoints that should not be force-merged:

- #220 — preserved research record
- #236 — preserved design record
- #238 — latest closed successor of the affective adult-reference lineage
- #247 — latest closed AION/Astra successor
- #248 — latest closed Work successor
- #249 — latest closed Codex successor
- #254 — latest closed Teacher successor

## Next actions

1. Add a consistent lifecycle footer to each relevant closed PR.
2. Do not reopen historical PRs merely to annotate lifecycle.
3. Perform semantic review only for the unresolved reconciliation set.
4. If a real capability/governance delta remains, create a narrowly scoped successor branch for that lineage.
5. Do not create a single mega-merge branch across all embodiment history.
6. `REQUIRES_SEMANTIC_RECONCILIATION = 0` for this audited set. Any future re-entry must open a narrowly scoped successor from the relevant source evidence.

## Nonclaims

This ledger does not establish:

- scientific validity;
- biological equivalence;
- subjectivity;
- consciousness;
- phenomenal experience;
- merge authorization;
- deployment authorization.

It records repository-history and semantic-convergence evidence only.

## New convergence successors

### PR #257

`refactor(embodiment): converge cross-role presentation and geometry`

Status: `LATEST_CLOSED_SUCCESSOR`

Exact head: `a1eedd764e5139ece69e29ba2fb6cd452e679ba4`

Lifecycle: closed / Draft / unmerged.

Resolves: #194, #243.

Exact-head verification includes Python 3.11/3.12, mypy 3.11/3.12, CodeQL, controls, coverage reconciliation, traceability, and IQC. The Main Transition Authority Gate failed closed as designed because no fresh exact-head merge authorization exists.


### PR #256

`refactor(embodiment): reconcile Teacher v0.2 integration surface`

Status: `LATEST_CLOSED_SUCCESSOR`

Exact head: `8569c245f78815361363f9346d226c228a0b7596`

Lifecycle: closed / Draft / unmerged.

Resolves: #239.

Relative to Teacher PR #254 exact head:

- ahead: 6 commits
- changed files: 4
- integrated Teacher v0.2 manifest surface materialized
- current reference bundle and reproductive-output contract retained
- executable validation and CLI exposure added
- dedicated reconciliation tests added

Exact-head CI:

- Python 3.11: PASS
- Python 3.12: PASS
- Mypy Python 3.11: PASS
- Mypy Python 3.12: PASS
- CodeQL: PASS
- current controls: PASS
- Fresh exact-head Human Owner approval receipt: FAIL_CLOSED_AS_DESIGNED

`MERGE_TO_MAIN = NO`

`DEPLOYMENT = FALSE`

`CANONICAL_EFFECT = NONE`
