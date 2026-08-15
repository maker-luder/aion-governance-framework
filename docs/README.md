# AION Documentation Guide

> **Current documentation map for the public repository.**
>
> This page answers one question: **what should a reader treat as current, core, supporting evidence, or historical record?**
>
> Dated incident, convergence, QA and branch-disposition files are preserved for provenance. They are not automatically current just because they remain in the repository.

## Start here

If you are new to AION, read in this order:

1. [`../README.md`](../README.md) — project orientation and current repository boundary.
2. [`RESEARCH_CONTRIBUTION_ONE_PAGER.md`](RESEARCH_CONTRIBUTION_ONE_PAGER.md) — the research question and contribution in one page.
3. [`ARCHITECTURE.md`](ARCHITECTURE.md) — the bounded governance architecture.
4. [`NON_CLAIMS.md`](NON_CLAIMS.md) — what the repository does **not** establish.
5. [`PROVENANCE.md`](PROVENANCE.md) — source, attribution and authority rules.
6. [`PUBLIC_PRIVATE_BOUNDARY.md`](PUBLIC_PRIVATE_BOUNDARY.md) — what is intentionally excluded from the public repository.
7. [`THREAT_MODEL.md`](THREAT_MODEL.md) — major research-integrity and system threats.

That sequence is the **core reader path**. Everything else is supporting detail, implementation evidence, or historical record.

## Current repository standing

```text
REPOSITORY_STATE = FROZEN_CHECKPOINT
LIVE_BRANCH_MODEL = MAIN_PLUS_RESEARCH_ONLY
ACTIVE_ENGINEERING = NO
ACTIVE_RESEARCH_MATERIALIZATION = NO
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
LICENSE = Apache-2.0
```

The live branches are intentionally limited to:

- `main` — protected public baseline;
- `review/four-domain-research-materialization` — preserved frozen research checkpoint.

Five retired support branches were converted to non-release `archive/*` tags so their exact commits and provenance remain addressable without remaining active branches. The two semantic release tags, `v0.1.0-rc.1` and `v0.2.0-rc.1`, remain historical release checkpoints.

For release/freeze standing, use [`RELEASE_STATUS.md`](RELEASE_STATUS.md). For research-branch standing, use [`RESEARCH_BRANCH_STATUS.md`](https://github.com/maker-luder/aion-governance-framework/blob/review/four-domain-research-materialization/RESEARCH_BRANCH_STATUS.md).

## Core documents

### Research meaning

- [`RESEARCH_CONTRIBUTION_ONE_PAGER.md`](RESEARCH_CONTRIBUTION_ONE_PAGER.md) — concise research contribution.
- [`NON_CLAIMS.md`](NON_CLAIMS.md) — epistemic and presentation limits.
- [`POSITION_PAPER_PROVENANCE_FIRST.md`](POSITION_PAPER_PROVENANCE_FIRST.md) — longer-form position-paper treatment.

### Governance and architecture

- [`ARCHITECTURE.md`](ARCHITECTURE.md) — architecture overview.
- [`PROVENANCE.md`](PROVENANCE.md) — attribution, lineage and authority rules.
- [`PUBLIC_PRIVATE_BOUNDARY.md`](PUBLIC_PRIVATE_BOUNDARY.md) — public/private separation.
- [`THREAT_MODEL.md`](THREAT_MODEL.md) — threat model.
- [`RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md`](RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md) — evidence-admission boundary.

### Current operational standing

- [`RELEASE_STATUS.md`](RELEASE_STATUS.md) — current public repository/release standing.
- [`../BUILD_AND_VERIFY.md`](../BUILD_AND_VERIFY.md) — verification entry point.
- [`../SECURITY.md`](../SECURITY.md) — security reporting.
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — contribution boundary.

## Repository layout

| Area | Meaning |
|---|---|
| `components/` | bounded implementation candidates and governance modules |
| `research-labs/` | research candidates and experiments; not canonical conclusions |
| `experiments/` | bounded experiment material and reproducibility evidence |
| `qa/` | current/historical QA evidence and machine-readable status artifacts |
| `docs/` | research, governance, status and preserved historical documentation |
| `manifest/` | frozen historical release evidence; not a live file inventory |
| `archive/*` tags | Git refs preserving retired branch checkpoints; not releases or approvals |

## How to interpret the large document set

The repository intentionally preserves dated evidence because provenance matters. The presence of many files therefore does **not** mean every file is equally authoritative.

Use this hierarchy:

```text
CURRENT
  README.md
  docs/README.md
  docs/RELEASE_STATUS.md
  research branch: RESEARCH_BRANCH_STATUS.md

CORE
  research contribution
  architecture
  non-claims
  provenance
  public/private boundary
  threat model

SUPPORTING EVIDENCE
  component docs
  QA reports
  release verification
  standards crosswalks
  research protocols

HISTORICAL / EVENT RECORDS
  dated C0_* files
  *_RECONCILIATION_2026-*.md
  *_CHECKLIST_2026-*.md
  FINAL_*_2026-08-15.md event snapshots
  PR-specific disposition records
  earlier branch/status snapshots
```

A historical file may accurately describe what was true at its event time while no longer describing the repository's current branch count, current workflow state, or current authority standing.

## Historical evidence rule

Do not mechanically rewrite dated evidence to make it look current. Instead:

```text
HISTORICAL_RECORD = PRESERVE_EVENT_MEANING
CURRENT_STATUS = READ_FROM_CURRENT_ENTRY_POINTS
NEWER_CANDIDATE != AUTOMATIC_SUPERSESSION
CI_PASS != SCIENTIFIC_VALIDATION
TEST_PASS != THEORY_CONFIRMATION
ARCHIVE_TAG != RELEASE
ARCHIVE_TAG != APPROVAL
RESEARCH_BRANCH != MAIN
```

This keeps the repository auditable without forcing a new reader to reconstruct current state from old incidents and convergence packets.

## What not to infer

Neither the documentation structure nor successful engineering/QA establishes consciousness, subjectivity, identity continuity, autobiographical memory, moral status, production readiness, deployment authority, or independent IV&V. See [`NON_CLAIMS.md`](NON_CLAIMS.md).
