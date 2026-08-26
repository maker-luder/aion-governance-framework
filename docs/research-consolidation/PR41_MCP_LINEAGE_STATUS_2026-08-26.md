# PR #41 MCP lineage status — 2026-08-26

Status: `CURRENT_LINEAGE_STATUS / DOCUMENTARY_ONLY`

This record reconciles the current standing of the bounded MCP Phase 1 Observation Evidence Bridge without reopening, merging, or rewriting PR #41.

## Source lineage

```text
PR41 = feat: add Phase 1 observation evidence MCP bridge
PR41_HEAD = 7986381dd48bbf702f2fc015078c8d072523adb2
PR41_TEACHER_EXACT_HEAD_REVIEW = PASS
PR41_MAIN_TRANSITION_AUTHORITY_GATE = HISTORICAL_EXPECTED_FAIL_CLOSED
PR41_MAIN_MERGE = NO
PR41_CLOSE_WITHOUT_MERGE = YES
PR41 = SUPERSEDED_BY_PR42

PR42 = convergence: materialize research evidence and repair reader surfaces
PR42_FINAL_HEAD = 055b97c5781a57ddbad4ee0b58b549522fc87db8
PR42_TEACHER_EXACT_HEAD_REVIEW = PASS
PR42_HUMAN_OWNER_MERGE_APPROVAL = EXPLICITLY_GIVEN
PR42_DUAL_REVIEW_GATE = SATISFIED
PR42_RESEARCH_BRANCH_ADMISSION = MERGED

PR47 = chore: add research-branch correctness lint gate
PR47_RUFF_CORRECTNESS_GATE = PASS
PR47_ACTIVE_RUFF_BASELINE = 0_FINDINGS
```

## Current component standing

The selectively admitted component lives at:

`components/mcp_observation_evidence_v0.1.0/`

It remains a six-tool, local-stdio, closed-world, pure-read observation/provenance bridge. It does not import or call AION/Astra Runtime `recall()`, ingest private conversation corpora, write memory, grant identity authority, perform canonical writes, deploy a public MCP service, or establish subjectivity evidence.

```text
RESEARCH_BRANCH_ADMISSION = YES
MAIN_MERGE = NO
CANONICAL_EFFECT = NONE
PUBLIC_DEPLOYMENT = NO
RUNTIME_MEMORY_ACCESS = NO
MEMORY_WRITE = NO
IDENTITY_AUTHORITY = NO
SUBJECTIVITY_EVIDENCE_WEIGHT = 0
INDEPENDENT_IVV = NOT_ACHIEVED
```

## Historical validation-gap disposition

PR #41 recorded `ruff` and `mypy` as unavailable in its isolated audit environment. These must not be carried forward as one undifferentiated current gap.

- Ruff: later research-branch hardening in PR #47 installed a pinned Ruff correctness gate and reduced the active correctness baseline to zero findings. The PR #41 Ruff gap is therefore historical for the active research tree.
- mypy: no component-specific mypy/type-check acceptance claim is established by this record. It remains `NOT_ESTABLISHED`, not `FAIL`.

```text
PR41_RUFF_GAP = HISTORICAL / RESOLVED_BY_PR47
MYPY_COMPONENT_ACCEPTANCE = NOT_ESTABLISHED
```

## Provenance references

- PR #41: https://github.com/maker-luder/aion-governance-framework/pull/41
- PR #42: https://github.com/maker-luder/aion-governance-framework/pull/42
- PR #47: https://github.com/maker-luder/aion-governance-framework/pull/47
- PR #41 exact-head Teacher review: preserved in the PR #41 timeline.
- PR #41 closure receipt: preserved in the PR #41 timeline.
- PR #42 final dual-approval receipt: preserved in the PR #42 timeline.

Historical comments, red checks, and closure receipts remain unchanged.

```text
HISTORICAL_PROVENANCE = PRESERVED
RETROACTIVE_GREENWASH = FORBIDDEN
PR41_REOPEN = NO
PR41_MERGE = NO
```
