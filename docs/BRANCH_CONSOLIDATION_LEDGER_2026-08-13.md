# Branch Consolidation Ledger — 2026-08-13

> **HISTORICAL RECORD:** This ledger captures an earlier consolidation state. Its `4b360779…` main values are historical and must not be read as current main. The current authoritative main reference is `abb6550abfacb4fabc53ec04fca783bcc34acfdb`.

This ledger is the provenance index for the final two-branch consolidation. It is generated from the read-only remote branch inventory captured before consolidation. No main write was permitted. The final research commit containing this ledger is reported in the final handoff because a commit cannot self-reference its own hash without changing that hash.

## State locks

| Field | Value |
|---|---|
| `HISTORICAL_MAIN_HEAD_BEFORE` | `4b36077993fabb22bf04e06162ea83c623bbb7e6` |
| `RESEARCH_HEAD_BEFORE` | `6f39fff07f1b1a79867c270f953c554e18addbc1` |
| `HISTORICAL_MAIN_HEAD_AFTER` | `4b36077993fabb22bf04e06162ea83c623bbb7e6` |
| `CURRENT_MAIN_REFERENCE` | `abb6550abfacb4fabc53ec04fca783bcc34acfdb` |
| `RESEARCH_HEAD_AFTER` | See final handoff receipt (`RESEARCH_HEAD_AFTER`); the final commit SHA is intentionally recorded outside this self-referential ledger |
| `RESEARCH_HEAD_AT_PRIOR_LEDGER_COMMIT` | `700545e15bc9a4cd7811dd9cccf1c88b93bd77a8` |
| Permanent branch budget | 2 |
| Canonical effect | NONE |
| Deployment | FALSE |
| Independent IV&V | NOT_ACHIEVED |

## Remote branch dispositions

| Branch | Old head | Unique commits / paths (before consolidation) | Disposition | Integrated content / target | Deletion justification |
|---|---|---:|---|---|---|
| `agent/research-contribution-one-pager` | `116ba5d342e90b6566eb925a5afa985ef5556e30` | 0 commits / 0 paths | `ALREADY_INCLUDED` | No remaining unique path against the local consolidation after existing lineage merges.; `Current formal research consolidation` | All useful content is already represented; deleted after final QA, independent checkout and final remote-state gates. |
| `agent/runtime-twin-provenance-alignment` | `5477313470898909fe7c4ffffc02dba6bc27c7fc` | 0 commits / 0 paths | `ALREADY_INCLUDED` | No remaining unique path against the local consolidation after existing lineage merges.; `Current formal research consolidation` | All useful content is already represented; deleted after final QA, independent checkout and final remote-state gates. |
| `autogrow/2026-08-12-evidence-profile-adapter` | `181a1d203e4fed8999baa75a94e50ae348c00858` | 0 commits / 0 paths | `ALREADY_INCLUDED` | No remaining unique path against the local consolidation after existing lineage merges.; `Current formal research consolidation` | All useful content is already represented; deleted after final QA, independent checkout and final remote-state gates. |
| `docs/homepage-watermark-boundary` | `3b52806cabad240ec33de60e71a9605ee1c813c3` | 2 commits / 2 paths | `ALREADY_INCLUDED` | No remaining unique path against the local consolidation after existing lineage merges.; `Current formal research consolidation` | All useful content is already represented; deleted after final QA, independent checkout and final remote-state gates. |
| `experiment/hermes-p0-mechanism-eval-20260812` | `dcde2eabca3f64c7f41f7ebbc1aa35817b305e63` | 8 commits / 3 paths | `INTEGRATE` | Hermes P0 read-only/network-disabled mechanism harness; `local merge commit; final QA target head` | Merged after safety scan; preserve research-only boundary. |
| `feat/upstream-supplier-trust-v0.1.1` | `0436185a941e7dec7b340970f0b5ccaf9d9d4077` | 0 commits / 0 paths | `ALREADY_INCLUDED` | No remaining unique path against the local consolidation after existing lineage merges.; `Current formal research consolidation` | All useful content is already represented; deleted after final QA, independent checkout and final remote-state gates. |
| `policy/imperceptible-watermark-rejection` | `665d1d8415ed0e2aa0b51e93f973a0e61fa0529f` | 1 commits / 1 paths | `ALREADY_INCLUDED` | No remaining unique path against the local consolidation after existing lineage merges.; `Current formal research consolidation` | All useful content is already represented; deleted after final QA, independent checkout and final remote-state gates. |
| `review/affective-motivational-salvage` | `9079e10448b8535ac8ecdd481d83edf75c2ae8c8` | 17 commits / 61 paths | `ALREADY_INCLUDED` | No remaining unique path against the local consolidation after existing lineage merges.; `Current formal research consolidation` | All useful content is already represented; deleted after final QA, independent checkout and final remote-state gates. |
| `review/agent-check/base-20260810` | `a3ab63671c92d5b29c81b1ef23a5fe65cc246074` | 0 commits / 0 paths | `ALREADY_INCLUDED` | No remaining unique path against the local consolidation after existing lineage merges.; `Current formal research consolidation` | All useful content is already represented; deleted after final QA, independent checkout and final remote-state gates. |
| `review/agent-check/eca-evidence-20260810` | `2d393d4437094049e9767f8fea72ad7feea3fb08` | 1 commits / 1 paths | `INTEGRATE` | review-only agent experiment protocol; `local merge commit; final QA target head` | Merged as governance evidence; AUTO_WRITE=NO and AUTO_MERGE=NO. |
| `review/aion-astra-whole-system-completion` | `263f6905356ebf0581b9ad8acda6c449587c73f1` | 390 commits / 0 paths | `SUPERSEDED` | old whole-system v1 line; `review/aion-astra-whole-system-completion-v2` | V2 is the valid adopted whole-system line; do not preserve a second permanent whole-system branch. |
| `review/aion-astra-whole-system-completion-v2` | `f7f76d31e98985464972304fa1184a755a1104cf` | 6 commits / 90 paths | `INTEGRATE` | whole-system governed runtime v0.1.0, QA/manifest/coverage automation; `f7f76d31e98985464972304fa1184a755a1104cf fast-forward lineage` | V2 was formal-research descendant with merge-base formal head and 9 commits ahead. |
| `review/continuity-evidence-lineage-rework` | `a5da5353c414db2043c13908d1795a66b042836a` | 59 commits / 54 paths | `INTEGRATE` | continuity evidence lineage and integration candidates; `local merge commit; final QA target head` | Selective lineage-preserving merge; duplicate candidate surfaces retained only in current reconciled form. |
| `review/embodied-action-regulation-salvage` | `8ff170374e59cf1e02caacf2e99392b6eeacc8c3` | 32 commits / 59 paths | `ALREADY_INCLUDED` | No remaining unique path against the local consolidation after existing lineage merges.; `Current formal research consolidation` | All useful content is already represented; deleted after final QA, independent checkout and final remote-state gates. |
| `review/embodiment-handoff-protocol-rework` | `3e2377a425a107bf7c8d5e9d5b62fac708b34c32` | 46 commits / 57 paths | `ALREADY_INCLUDED` | No remaining unique path against the local consolidation after existing lineage merges.; `Current formal research consolidation` | All useful content is already represented; deleted after final QA, independent checkout and final remote-state gates. |
| `review/encounter-longitudinal-evidence-reconstruction` | `e98aad2f3b11a0deeeda2425c7621c7e2a646ca7` | 85 commits / 48 paths | `INTEGRATE` | encounter evidence protocol and longitudinal change evidence; superseded earlier duplicate package names; `local merge commit; final QA target head` | Git rename/delete resolution selected evidence-grounded current surfaces. |
| `review/manus-adult-male-embodiment-correction-20260812` | `2c3833ed4ebf2b4ff180945e32bc2e59f9b89d23` | 0 commits / 0 paths | `ALREADY_INCLUDED` | No remaining unique path against the local consolidation after existing lineage merges.; `Current formal research consolidation` | All useful content is already represented; deleted after final QA, independent checkout and final remote-state gates. |
| `review/manus-iqc-main-reconciliation-20260812` | `7f06ba94ff8aedddd4474970bdeb74118e86393c` | 27 commits / 40 paths | `INTEGRATE` | source-state binding, evidence admission, manifest and Runtime Strong QA improvements; `local merge commit; final QA target head` | Conflicts reconciled with research branch contract; strict schema and fail-closed tests retained. |
| `review/manus-iqc-research-reconciliation-20260812` | `1679b759279cb6560407b874a97692e875adf647` | 25 commits / 41 paths | `INTEGRATE` | IQC inspection, current QA reconciliation, evidence traceability and research-workbench controls; `local merge commit; final QA target head` | Fast-forward descendant relationship preserved before v2/other local merges. |
| `review/metacognitive-self-state-rework` | `638dcb46136d879ed16ff7dfe2d260ac2eed734b` | 10 commits / 65 paths | `INTEGRATE` | metacognitive self-state rework and regression evidence; `local merge commit; final QA target head` | Merged after continuity base; package rework tests pass. |
| `review/p0-crosswalk-verifier-reconciliation` | `60cd97cf2e0855a29e6f1083a1599cb236f90117` | 0 commits / 0 paths | `ALREADY_INCLUDED` | No remaining unique path against the local consolidation after existing lineage merges.; `Current formal research consolidation` | All useful content is already represented; deleted after final QA, independent checkout and final remote-state gates. |
| `review/public-closure-2026-08-09` | `9eed7bf9a2004539e4168dbe76134c78a40fa950` | 0 commits / 0 paths | `ALREADY_INCLUDED` | No remaining unique path against the local consolidation after existing lineage merges.; `Current formal research consolidation` | All useful content is already represented; deleted after final QA, independent checkout and final remote-state gates. |
| `review/second-order-commit-performance-monitor-candidate` | `8059e455fb9bc1297f7734b0eceb4704be4ffef6` | 9 commits / 0 paths | `SUPERSEDED` | partial candidate cleanup/removal history; `current formal research evidence` | No unique public path remains against consolidation; later cleanup supersedes the temporary candidate. |
| `review/self-other-boundary-rework` | `59e85e7aa5b65a041390cb13241ad69af5086f12` | 14 commits / 66 paths | `INTEGRATE` | self/other boundary rework and immutable snapshot tests; `local merge commit; final QA target head` | Merged after continuity base; serialization and boundary tests pass. |
| `session/agent_99a9dfc9-f4f4-432c-a918-f97527f129bc` | `2f3e9b05e5035ed718ec553c235de8b5acf738a7` | 4 commits / 64 paths | `ALREADY_INCLUDED` | No remaining unique path against the local consolidation after existing lineage merges.; `Current formal research consolidation` | All useful content is already represented; deleted after final QA, independent checkout and final remote-state gates. |
| `tmp-do-not-use` | `cbf9e2e4b0f4bc2be318896684825dc0dcb1000b` | 0 commits / 0 paths | `HISTORICAL_ONLY` | temporary branch with no unique current path; `none` | Deleted after final QA, independent checkout and final remote-state gates; no content to integrate. |

## Local Manus work disposition

| Local artifact class | Disposition | Rationale |
|---|---|---|
| Public-safe model source, training/evaluation scripts, registries, evidence summaries | `INTEGRATE_TO_RESEARCH` | Added under `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/`; hashes and non-claims retained. |
| Eight local checkpoint binaries | `RESOURCE_ONLY_LOCAL` / `OWNER_REVIEW_REQUIRED` | Not copied into Git; public registries retain hash/provenance and explicitly state repository absence. |
| Seven synthetic dataset binaries | `RESOURCE_ONLY_LOCAL` / `OWNER_REVIEW_REQUIRED` | No private material is assessed, but publication/storage policy remains an Owner decision; metadata is retained without fabricating current presence. |
| Four bounded local candidates | `INTEGRATE_TO_RESEARCH` | Copied as research-labs integration candidates and covered by dynamic nested test runner; all 148 tests pass. |
| Raw remote API JSON, local absolute paths, credentials, cache and generated artifacts | `UNSAFE_TO_PUBLISH` | Excluded from the research tree and final deliverable. |

## Permanent branch governance rule

```text
REMOTE_PERMANENT_BRANCH_BUDGET = 2
ALLOWED_PERMANENT_REMOTE_BRANCHES = [
  main,
  review/four-domain-research-materialization,
]
THIRD_PERMANENT_BRANCH_REQUIRES = EXPLICIT_HUMAN_OWNER_APPROVAL
```

Local temporary worktrees/branches may be used for isolation, but they must not become permanent remote branches. Normal unpromoted AION/Astra growth belongs on the governed research line.

## Integration and deletion gate

All selected useful branches were integrated into the local formal-research consolidation before remote deletion. Branches classified `ALREADY_INCLUDED`, `SUPERSEDED` or `HISTORICAL_ONLY` had no remaining useful unique path in the final tree. After final QA, terminal GitHub Actions success, independent checkout, main-head invariance and final remote-state re-fetch, all 26 temporary branches were deleted. Final remote state is exactly `main` plus `review/four-domain-research-materialization`.

## Final remote cleanup receipt

```text
RESEARCH_HEAD_AFTER = SEE_FINAL_HANDOFF_RECEIPT
BRANCH_COUNT_BEFORE = 28
BRANCH_COUNT_AFTER = 2
DELETED_BRANCH_COUNT = 26
FINAL_BRANCHES = [main, review/four-domain-research-materialization]
MAIN_HEAD_CHANGED = FALSE
QUALITY_STATUS = PASS
RESEARCH_WORKBENCH_STATUS = PASS
RESEARCH_SCOPE_LOCK_STATUS = PASS
INDEPENDENT_CHECKOUT = PASS / 35 TESTS PASSED
```

The machine-readable deletion receipt is retained in the local consolidation evidence under `remote-state/REMOTE_DELETION_RESULTS.json`; the final remote-state receipt is `remote-state/REMOTE_STATE_FINAL.json`.

## Non-claims

This ledger does not claim canonical promotion, deployment, subjectivity, consciousness, identity continuity, production readiness or independent IV&V. Research integration preserves evidence status and does not turn candidate or experimental material into scientific proof.
