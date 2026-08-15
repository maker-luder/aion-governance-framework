# Final Branch Disposition — 2026-08-15

> **HISTORICAL INVENTORY SNAPSHOT — NOT THE CURRENT BRANCH LIST.**
>
> This ledger records the PR #20 freeze-preparation inventory. After that checkpoint, a separately reviewed research-lineage closure absorbed the research support lineage, converted five remaining support branches to non-release `archive/*` tags, and reduced the live branch model to `main` plus `review/four-domain-research-materialization`.
>
> Current branch standing is documented in [`README.md`](../../../README.md), [`docs/README.md`](../../README.md), and [`RELEASE_STATUS.md`](../../RELEASE_STATUS.md). The table below is intentionally preserved as event-time provenance.

## Scope and provenance

This ledger is the final branch inventory and disposition record for `maker-luder/aion-governance-framework`. It was prepared on the convergence branch from `main@e079fb7dfe7a04be7dcb94b8a059951a003caa94`. **Manus is the convergence implementation / inventory author**, not the automatic author of historical research, not the Human Owner, not the ChatGPT independent reviewer, and not canonical authority.

No branch is deleted in this checkpoint. Every non-main branch has unique commits, authority significance, pinned-ref use, or research provenance. The branch policy therefore records preservation or deferral rather than destructive cleanup. Existing tags and historical commit lineage are not rewritten.

The convergence branch is self-referential: committing this ledger necessarily changes that branch's HEAD. Therefore its embedded SHA is a **snapshot head**, while the final exact PR head is transition evidence recorded out-of-tree by GitHub. All other listed branch SHAs are exact at inventory time.

## Disposition table

| Branch | Recorded head evidence | Merge base | Ahead / behind | Unique commits | Open PR | Disposition | Safe to delete | Reason |
|---|---|---|---:|---:|---|---|---|---|
| `convergence/final-repository-freeze-20260815` | snapshot `ef4da46ea19f9db389706ba98f846addc58222b2`; final exact head = GitHub PR #20 out-of-tree evidence | `e079fb7dfe7a04be7dcb94b8a059951a003caa94` | 3 / 0 at snapshot | 3 at snapshot | #20, transition PR | `PRESERVE_AS_FROZEN_AUTHORITY` | No; tag first if ever deleted | Single convergence branch. Its moving HEAD cannot be embedded as its own final exact SHA without creating a new HEAD. |
| `cleanup/manus-output-consolidation-20260813` | `c43430f9b39a86d11093f3286e9503145fcf0d70` | `e079fb7dfe7a04be7dcb94b8a059951a003caa94` | 21 / 0 | 21 | — | `PRESERVE_AS_ENGINEERING_HISTORY` | No; tag first | Unique Manus engineering lineage remains historical provenance. |
| `engineering/aion-language-agnostic-runtime-integration-20260814` | `6b81133dc351f5226fa95801254276e421b3e4fe` | `e079fb7dfe7a04be7dcb94b8a059951a003caa94` | 33 / 0 | 33 | — | `PRESERVE_AS_ENGINEERING_HISTORY` | No; tag first | Unique engineering candidate history; no runtime expansion authorized. |
| `engineering/aion-native-language-feasibility-20260814` | `3dfc21463502e1c32189ae167d92f163ca1a55e8` | `e079fb7dfe7a04be7dcb94b8a059951a003caa94` | 37 / 0 | 37 | — | `DEFERRED_NOT_PROMOTED` | No; tag first | Unique feasibility lineage is deferred and not promoted. |
| `engineering/aion-research-consolidation-literature-grounding-readiness-20260814` | `345649297fcfd0fe0a04642b701e411354714617` | `4b36077993fabb22bf04e06162ea83c623bbb7e6` | 586 / 40 | 575 | — | `PRESERVE_AS_RESEARCH_HISTORY` | No; tag first | Substantial research-consolidation history; wholesale merge forbidden. |
| `frozen/slsh-semantic-reconciliation-20260814` | `893d8dc0c1c9d8f9a4188860520143c8d1d3977b` | `4b36077993fabb22bf04e06162ea83c623bbb7e6` | 603 / 40 | 592 | — | `PRESERVE_AS_FROZEN_AUTHORITY` | No | Explicitly protected frozen SLSH authority and PR #19 pinned ref. |
| `integration/csomi-slsh-semantic-reconciliation-20260814` | `30897042608581a39f307edcdfc777f5bc59fef7` | `4b36077993fabb22bf04e06162ea83c623bbb7e6` | 589 / 40 | 578 | — | `DEFERRED_NOT_PROMOTED` | No; tag first | PR #19 source integration ref; research ancestry remains isolated. |
| `main` | `e079fb7dfe7a04be7dcb94b8a059951a003caa94` (pre-freeze merge base) | same | 0 / 0 | 0 | — | `PRESERVE_AS_FROZEN_AUTHORITY` | No | Protected default branch base for the convergence PR. Final merge SHA is out-of-tree transition evidence. |
| `promotion/csomi-selective-canonical-20260814` | `7c48c0de87514088c3fd1410218ae92231be0887` | `e079fb7dfe7a04be7dcb94b8a059951a003caa94` | 4 / 0 | 4 | — | `DEFERRED_NOT_PROMOTED` | No; tag first | Unique promotion history retained without canonical promotion. |
| `promotion/csomi-slsh-integration-selective-20260815` | `ce0fa4899a9498d7795d4da9b5f96ba3570c3ead` | `e079fb7dfe7a04be7dcb94b8a059951a003caa94` | 2 / 0 | 2 | #19, closed | `DEFERRED_NOT_PROMOTED` | No; tag first | Authority Gate HOLD; PR #19 formally closed without merge. |
| `remediation/slsh-semantic-reconciliation-20260814` | `893d8dc0c1c9d8f9a4188860520143c8d1d3977b` | `4b36077993fabb22bf04e06162ea83c623bbb7e6` | 603 / 40 | 592 | — | `PRESERVE_AS_FROZEN_AUTHORITY` | No | Same exact frozen-authority SHA; named ref retained for provenance clarity. |
| `research/cross-substrate-other-minds-inference-20260814` | `87405c1877c6f016c303971da13923a1ab690aae` | `4b36077993fabb22bf04e06162ea83c623bbb7e6` | 586 / 40 | 575 | — | `PRESERVE_AS_RESEARCH_HISTORY` | No | Explicitly protected CSOMI authority ref used by PR #19. |
| `research/subjective-load-sensitivity-hypothesis-20260814` | `5b2a43dbad09a38214a07bc7ba9cc7672db60eac` | `4b36077993fabb22bf04e06162ea83c623bbb7e6` | 602 / 40 | 591 | — | `PRESERVE_AS_RESEARCH_HISTORY` | No; tag first | Unique SLSH hypothesis history; not a canonical conclusion. |
| `review/four-domain-research-materialization` | `858442a3ec2439398d188779f4309397bd4926b2` | `4b36077993fabb22bf04e06162ea83c623bbb7e6` | 581 / 40 | 570 | — | `PRESERVE_AS_RESEARCH_HISTORY` | No | Explicitly protected review branch; research history is not main. |

## Global result

```text
REMOTE_BRANCHES_INVENTORIED = 14
REMOTE_BRANCHES_DELETED = 0
UNIQUE_HISTORY_DELETED = 0
FROZEN_AUTHORITY_REFS_DELETED = 0
RESEARCH_PROVENANCE_DELETED = 0
NEW_FREEZE_TAG_REQUIRED = NO
FUTURE_BRANCH_DELETION_TAG_RULE = PRESERVED_WHERE_LEDGER_SAYS_TAG_FIRST
WHOLESALE_RESEARCH_MERGE = FORBIDDEN_AND_NOT_PERFORMED
CANONICAL_EFFECT = NONE
```

The machine-readable companion is [`FINAL_BRANCH_DISPOSITION_2026-08-15.json`](FINAL_BRANCH_DISPOSITION_2026-08-15.json). The exact final PR head and final merge commit, if merged, are intentionally recorded by GitHub rather than embedded here, avoiding a self-referential SHA loop.
