# AION Branch Convergence Ledger — 2026-08-18

> This is the **single** branch-convergence ledger for the current PHASE 0–5 cycle. It records content-level materialization and quarantine decisions without deleting refs, merging histories, force-pushing authoritative branches, or granting canonical effect.

## Authority and end-state target

```text
AUTHORITATIVE_MAIN = main@752fce6fb26ec2e8ea44f77d989afaf549ab7dfe
AUTHORITATIVE_RESEARCH = review/four-domain-research-materialization@744b97bc61c753dae84250526ffc17643db7779f
TEMPORARY_WORK = convergence/two-branch-finalization-20260818
TEMPORARY_BASE = review/four-domain-research-materialization@744b97bc61c753dae84250526ffc17643db7779f
FINAL_BRANCH_TARGET = main + review/four-domain-research-materialization
EXPANSION_MODE = OFF
MAIN_WRITE = NO
RESEARCH_MERGE = OWNER_AUTH_REQUIRED
BRANCH_DELETE = NO
CANONICAL_EFFECT = NONE
```

`PR #41` is a source branch only in this ledger. Its exact source head is `7986381dd48bbf702f2fc015078c8d072523adb2`. Its obsolete main-target Authority Gate failure is preserved as historical/expected fail-closed evidence and is not repaired or greenwashed.

## Transitional branch ledger

| Source branch | Exact source head | Authority comparison | Unique content / current disposition | Destination or containment | Red-X classification | Provenance | Retirement status |
|---|---|---|---|---|---|---|---|
| `convergence/whitepaper-main-alignment-20260818` | `3bcc007dc9905a2a69ea1425919922819d1ff83e` | Main lineage; no new ahead content in fresh compare | No new materialization required | Existing main lineage | None observed; preserve historical checks if referenced | `MAIN_LINEAGE_REACHABLE` | `SAFE_TO_RETIRE_AFTER_OWNER_EXACT_TARGET_CONFIRMATION` |
| `remediation/documentation-structure-convergence-20260816` | `f5368f6dc81a536a6535a1bddbeecd8fc3218c2f` | Main-support history; no new ahead content required | No new materialization required | Existing main lineage | Historical evidence only | `MAIN_LINEAGE_REACHABLE` | `SAFE_TO_RETIRE_AFTER_OWNER_EXACT_TARGET_CONFIRMATION` |
| `remediation/pr23-control-closure-20260815` | `2b46ee5a2f0017de7709c14541b5071b38f00606` | Main-support history; no new ahead content required | No new materialization required; PR23 historical failure remains preserved | Existing main lineage + historical PR evidence | `HISTORICAL_FAILURE / PRESERVE` | `MAIN_LINEAGE_REACHABLE` | `SAFE_TO_RETIRE_AFTER_OWNER_EXACT_TARGET_CONFIRMATION` |
| `remediation/pr23-control-closure-final-seal-20260815` | `125fdba956f21decf37a6178a4adef31bd78967d` | Main-support history; no new ahead content required | No new materialization required | Existing main lineage + historical PR evidence | `HISTORICAL_FAILURE / PRESERVE` | `MAIN_LINEAGE_REACHABLE` | `SAFE_TO_RETIRE_AFTER_OWNER_EXACT_TARGET_CONFIRMATION` |
| `security/codeql-setup-20260817` | `97824bd840b929c88ed9851f8b286683fb5fa224` | Main lineage; no new ahead content required | No new materialization required | Existing main lineage | None current; historical CodeQL evidence preserved | `MAIN_LINEAGE_REACHABLE` | `SAFE_TO_RETIRE_AFTER_OWNER_EXACT_TARGET_CONFIRMATION` |
| `upstream/openai-assistants-sunset-20260817` | `a2cb63fe465ef162743786cbe27452dc5b28306c` | Main lineage; no new ahead content required | No new materialization required | Existing main lineage | Historical upstream evidence only | `MAIN_LINEAGE_REACHABLE` | `SAFE_TO_RETIRE_AFTER_OWNER_EXACT_TARGET_CONFIRMATION` |
| `research/openai-public-resource-supplement-20260817` | `bbbd911c0892d09a33f96b3825625add86247829` | Research lineage; no new ahead content required | No new materialization required | Existing research lineage | Public-resource evidence remains bounded and noncanonical | `RESEARCH_LINEAGE_REACHABLE` | `SAFE_TO_RETIRE_AFTER_OWNER_EXACT_TARGET_CONFIRMATION` |
| `remediation/research-convergence-ci-target-20260817` | `092a389c70b417dc318e5a6f9f55470fa0872f2b` | Research-related branch; ahead 1 / behind 5 in fresh compare | One semantic workflow target correction only | `.github/workflows/research-convergence-consistency.yml` on temporary branch; old history not merged | `CURRENT_TRUE_DEFECT` | `EXPLICIT_SOURCE_BRANCH / ONE_WORKFLOW_CHANGE` | `SAFE_TO_RETIRE_AFTER_EXACT_DIFF_REVIEW_AND_OWNER_CONFIRMATION` |
| `design/twin-autobiographical-memory-mcp-20260817` | `852339be16207ca08450ca6a8d3597772de3cd3b` | Main comparison showed five unique research files | Five design-candidate files selectively materialized under `research/` | Same research paths on temporary branch; no runtime activation | No red check; design remains `PHASE_2 = HOLD` | `HUMAN_OWNER_ORIGIN + CHATGPT_TEACHER_DESIGN; RUNTIME_OUTPUTS_NOT_GENERATED` | `SAFE_TO_RETIRE_AFTER_CONTENT_REVIEW_AND_OWNER_CONFIRMATION` |
| `test/governance-negative-20260815` | `26de721573a0f4210a1aab8e92dc86dc82be1b9c` | Main comparison showed one unique historical file | Historical wrapper preserves the three-line payload verbatim | `docs/history/governance-tests/2026-08-15/NEGATIVE_TEST_2026-08-15.archive.md` | Historical governance evidence; not current policy | `HISTORICAL_EVIDENCE` | `SAFE_TO_RETIRE_AFTER_OWNER_EXACT_TARGET_CONFIRMATION` |
| `test/governance-positive-20260815` | `bedcf6a6a56fa6f5c79e3806384f6519817b492a` | Main comparison showed one unique historical file | Historical wrapper preserves the three-line payload verbatim | `docs/history/governance-tests/2026-08-15/POSITIVE_TEST_2026-08-15.archive.md` | Historical governance evidence; not current policy | `HISTORICAL_EVIDENCE` | `SAFE_TO_RETIRE_AFTER_OWNER_EXACT_TARGET_CONFIRMATION` |
| `codex/mcp-phase1-evidence-bridge-20260818` | `7986381dd48bbf702f2fc015078c8d072523adb2` | PR #41 exact source diff; do not merge branch history | Eight Phase 1 component files plus one quality-workflow dependency line selectively materialized | `components/mcp_observation_evidence_v0.1.0/` and `.github/workflows/quality.yml` on temporary branch | Quality/CodeQL successful; Main Transition Authority Gate #96 = `HISTORICAL / OBSOLETE EXPECTED_FAIL_CLOSED`; no repair | `PR41_EXACT_SOURCE_HEAD / CONTENT_LEVEL_ONLY` | `NOT_YET_SAFE_TO_RETIRE_WHILE_PR41_OPEN_AND_REVIEW_PENDING` |
| `publication/aion-astra-publication-v0.1-20260817` | `540d190e8b60e92e3b6af94ad8f96d06091c73b3` | Main comparison showed publication/site candidate files | Inert exact branch-only diff snapshot preserved; no executable publication/site files absorbed | `docs/research-consolidation/quarantine/2026-08-18/publication-aion-astra-v0.1-20260817.patch` plus manifest; `vercel.json` remains outside active paths | No current red check; publication/deployment remains prohibited | `PUBLICATION_CANDIDATE / HOLD_ARTIFACT` | `RETIREMENT_CANDIDATE_AFTER_DURABLE_PRESERVATION / OWNER_CONFIRMATION` |
| `feat/mcp-readonly-interface-20260817` | `d5125c91da3cfa170f0651c0d2d44939fef2f070` | Main comparison showed MCP interface/QA unique content | Inert exact branch-only diff snapshot preserved; not absorbed as approved implementation; provenance uncertain | `docs/research-consolidation/quarantine/2026-08-18/feat-mcp-readonly-interface-20260817.patch` plus manifest; no runtime/public MCP activation | `PROVENANCE_UNCERTAIN / QUARANTINED_RESEARCH_ARTIFACT` | `UNCERTAIN_PROVENANCE` | `RETIREMENT_CANDIDATE_AFTER_DURABLE_PRESERVATION / OWNER_CONFIRMATION` |

## Selective materialization manifest

The temporary branch contains only content-level changes from the following sources:

1. PR #41 exact source head `7986381...`: the Phase 1 MCP component (eight files) and one existing Quality workflow install line. Fixed boundaries remain `RUNTIME_MEMORY_ACCESS=NO`, `MEMORY_WRITE=NO`, `IDENTITY_AUTHORITY=NO`, `CANONICAL_WRITE=NO`, `PUBLIC_DEPLOYMENT=NO`, and `SUBJECTIVITY_EVIDENCE_WEIGHT=0`.
2. Twin design source head `852339b...`: five documents only; all remain `DESIGN_CANDIDATE`, `PHASE_2=HOLD`, `MCP_TRANSPORT=HOLD`, `RUNTIME_EXECUTION=NOT_EXECUTED`, and `CANONICAL_EFFECT=NONE`.
3. Governance historical source heads `26de721...` and `bedcf6a...`: one three-line historical evidence file each; neither is promoted to current policy.
4. Research CI source head `092a389...`: only the two-line semantic target correction is re-materialized; source branch history is not merged.

No publication site, `vercel.json`, or uncertain MCP interface was materialized in an active executable path. Their exact branch-only deltas are preserved only as inert quarantine patch snapshots; no private conversation record, newsletter, model/provider/connector, or public deployment surface was added.

## Red-X policy

`HISTORICAL_FAILURE` remains preserved and is not rerun for green. `EXPECTED_FAIL_CLOSED` remains documented and is not technically repaired. Only the research workflow target mismatch is a `CURRENT_TRUE_DEFECT`; it is corrected in the temporary branch and must be revalidated by bounded checks.

## Phase boundary

This ledger records PHASE 0–5 only. No branch deletion, PR merge, main write, research merge, public deployment, publication enablement, or canonical promotion is performed in this cycle.

## Current research surface repairs in this convergence

The following existing research surfaces were repaired in place on the temporary branch:

| Path | Repair | Classification |
|---|---|---|
| `.github/workflows/research-convergence-consistency.yml` | Both branch targets remain scoped to `review/four-domain-research-materialization`; detached-head handling is validated in the checker | `CURRENT_TRUE_DEFECT / 2-LINE SEMANTIC FIX` |
| `scripts/check_research_consolidation_consistency.py` | PR CI validates GITHUB_BASE_REF, push CI validates GITHUB_REF_NAME, and local runs use explicit local branch rules; temporary branch is not a permanent CI requirement | `CURRENT_TRUE_DEFECT / DETACHED_HEAD_FIX` |
| `tests/research_consolidation/test_research_consolidation_contract.py` | Workflow target remains current research branch and a pull_request base-context regression test protects R1 | `CURRENT_TRUE_DEFECT / REGRESSION_GUARD` |
| `docs/research-consolidation/SOURCE_OF_TRUTH_MAP_V0.1.0.md` | Local v0.14.23 stable/frozen artifact is primary; 2026-08-12 file is derived supervised reconciliation bridge; primary path not confirmed | `READER_AUTHORITY_REPAIR` |
| `docs/research-consolidation/SOURCE_OF_TRUTH_MAP_V0.1.0.json` | Machine-readable hierarchy marks v0.14.23 primary, reconciliation derived, and primary path NOT_CONFIRMED_IN_CURRENT_RESEARCH_REF | `READER_AUTHORITY_REPAIR` |
| `docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md` | Stable-whitepaper method inheritance selectively synchronized from main without inventing verbatim stage labels | `READER_AUTHORITY_REPAIR` |
| `RESEARCH_BRANCH_STATUS.md` | Phase-0 count relabeled as PHASE0 snapshot; fresh PR42 inventory recorded separately as 17-ref observation | `CURRENT_VS_TARGET_CORRECTION` |

### Bounded test transition

The first bounded run found two current contract failures because the checker/test still encoded the obsolete engineering branch target. This was classified as `CURRENT_TRUE_DEFECT`, recorded before repair, and fixed minimally. The R1 detached-head defect is now included in this correction cycle; the final rerun will be bound to the new exact head:

```text
RESEARCH_CONSOLIDATION_CHECK = PASS
RESEARCH_EVIDENCE_TESTS = 12 passed
MCP_PHASE1_TESTS = 10 passed
MCP_PHASE1_COMPILE = PASS
RESEARCH_SOURCE_COMPILE = PASS
GIT_DIFF_CHECK = PASS
```

No historical failure was rerun for green. PR41 Main Transition Authority Gate evidence was not touched.
