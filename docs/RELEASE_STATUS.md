# Release Status

> **Current public repository standing.** Historical source-package and release-tag states are preserved below, but this file's current-status block is authoritative for the present repository freeze.

## Current repository freeze checkpoint

The public repository is in a frozen checkpoint after repository and research-lineage convergence on 2026-08-15.

```text
CURRENT_REPOSITORY_STATE = FROZEN_CHECKPOINT
LIVE_BRANCH_MODEL = MAIN_PLUS_RESEARCH_ONLY
LIVE_BRANCH_COUNT = 2
ACTIVE_ENGINEERING = NO
ACTIVE_RESEARCH_MATERIALIZATION = NO
NEW_FEATURE_DEVELOPMENT = NO
DEPLOYMENT = FALSE
CANONICAL_PROMOTION = NOT_AUTHORIZED
CANONICAL_EFFECT = NONE
LICENSE_SELECTION = RESOLVED_APACHE_2_0
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
RELATIONAL_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
```

The two live branches are:

- `main` — protected public baseline;
- `review/four-domain-research-materialization` — frozen preserved research checkpoint.

Five retired support branches were converted to non-release `archive/*` tags after exact-head verification. These archive tags preserve engineering/research/deferred-promotion checkpoints without keeping those refs as active branches. An archive tag is not a release, approval, canonical promotion or deployment authority.

The exact current branch heads, workflow runs and merge/approval events are GitHub transition evidence and are intentionally not embedded here as self-referential permanent status fields.

## Governance process-deviation record

PR #23 (`docs: converge public documentation around a clear reader path`) was merged into `main` while the Main Transition Authority Gate for that PR still held `HOLD` because the Human Owner approval receipt timestamp was not fresh for the PR-body edit event. The merge therefore did **not** satisfy the repository's intended gate-before-merge procedure.

The content itself had passed the PR Quality workflow, and the resulting merged `main` later passed post-merge Quality run #393. Those later PASS results establish current implementation/documentation quality only; they do **not** retroactively convert the historical Authority Gate failure into a PASS.

```text
PR23_CONTENT_REVIEW = ACCEPTED
PR23_PR_QUALITY = PASS
PR23_AUTHORITY_GATE_AT_MERGE = HOLD
PR23_PROCESS_DEVIATION = MERGED_WITHOUT_GATE_PASS
POST_MERGE_MAIN_QUALITY = PASS
RETROACTIVE_GATE_GREENWASH = FORBIDDEN
REVERT_REQUIRED_BY_THIS_RECORD = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

PR #19 is a contrasting fail-closed case: its promotion candidate was closed without merge after its authority gate remained unresolved. PR #21 and PR #22 concern research-only lineage convergence and are documented in the research branch's `RESEARCH_BRANCH_STATUS.md` with their own QA process-deviation record.

This section is an audit record, not a new authorization. It preserves the difference between current repository health and historical process compliance.

## Historical release tags

The existing semantic release tags remain:

- `v0.1.0-rc.1`
- `v0.2.0-rc.1`

They are immutable historical release checkpoints. The 2026-08-15 convergence did not create a new semantic release and did not require a new freeze release tag.

## Historical source candidate

The 2026-08-03 public source package was previously marked `PUBLIC_RELEASE_CANDIDATE_NOT_RELEASED`, `QA_HOLD`, `OWNER_SELECTION_REQUIRED` for license, and `CANONICAL_EFFECT=NONE`.

That paragraph describes the historical source package only. It does **not** describe current repository standing. The current public repository license is Apache-2.0.

## Documentation authority

For reader orientation and document hierarchy, use [`README.md`](../README.md) and [`docs/README.md`](README.md).

Dated convergence, branch-disposition, incident, acceptance and QA files preserve what was recorded at their event time. They are historical evidence unless a current entry point explicitly says otherwise.

In particular, [`FINAL_REPOSITORY_FREEZE_2026-08-15.md`](history/branch-and-release/FINAL_REPOSITORY_FREEZE_2026-08-15.md) and [`FINAL_BRANCH_DISPOSITION_2026-08-15.md`](history/branch-and-release/FINAL_BRANCH_DISPOSITION_2026-08-15.md) preserve the earlier PR #20 freeze-preparation snapshot; their original branch inventory predates the later support-branch archive conversion and two-branch closure.

## Boundary

A successful QA run, branch cleanup, archive-tag creation, documentation convergence or implementation completion does not establish subjectivity, identity continuity, scientific validity, independent IV&V, canonical runtime authority or deployment authority.

```text
CI_PASS != SCIENTIFIC_VALIDATION
ARCHIVE_TAG != RELEASE
ARCHIVE_TAG != APPROVAL
RESEARCH_BRANCH != MAIN
RESEARCH_CONVERGENCE != CANONICAL_PROMOTION
```
