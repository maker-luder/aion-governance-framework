# AION/Astra Whole-System Review v2 — Source Reconciliation

## Evidence status

This document records source-state evidence captured before selective replay and repair. It is a review artifact only. It does not promote canonical state, deploy runtime code, or approve a merge.

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
```

## Remote heads re-fetched before work

| Source | Exact SHA | Role |
|---|---|---|
| `main` | `4b36077993fabb22bf04e06162ea83c623bbb7e6` | authoritative main baseline |
| `review/four-domain-research-materialization` | `6f39fff07f1b1a79867c270f953c554e18addbc1` | formal research source and v2 starting point |
| `review/aion-astra-whole-system-completion` | `263f6905356ebf0581b9ad8acda6c449587c73f1` | historical orphan review artifact; preserved, not merge candidate |

The remote heads above were re-fetched from GitHub before v2 reconstruction. No remote branch was modified during this evidence capture.

## Lineage findings

The historical old review branch has no merge base with either authoritative branch in the local Git object database after fetch:

```text
merge-base(main, old review) = NONE
merge-base(formal research, old review) = NONE
```

GitHub compare API requests for the old review branch returned HTTP `404` in this sandbox session rather than the Teacher-observed `No common ancestor` response. This is an evidence-format discrepancy: local Git independently confirms no merge base; the GitHub API response could not be re-observed as a compare status here. The old branch remains retained for provenance and is not force-pushed, deleted, reset, rebased, or merged.

The v2 branch was created from formal research and received a normal non-fast-forward merge of current main:

```text
v2 starting head = 6f39fff07f1b1a79867c270f953c554e18addbc1
main merge parent = 4b36077993fabb22bf04e06162ea83c623bbb7e6
merge commit = bdf4efb474df266f9b7c64d943101f42170c7268
merge-base(v2, main) = 4b36077993fabb22bf04e06162ea83c623bbb7e6
merge-base(v2, formal research) = 6f39fff07f1b1a79867c270f953c554e18addbc1
```

The merge had one README conflict. It was resolved conservatively by retaining the research validation boundary and the main provenance/watermark boundary. No conflict markers remain.

## Dynamic eligible-target inventory

The inventory uses direct child directories under `components/`, `examples/`, and `research-labs/`; it does not hard-code an expected count.

| Source tree | Components | Examples | Research labs | Eligible target count |
|---|---:|---:|---:|---:|
| v2 immediately after lineage merge | 14 | 1 | 32 | 47 |
| old review candidate | 15 | 1 | 9 | 25 |
| v2 plus selectively replayed old whole-system target | 15 | 1 | 32 | 48 |

The Teacher review described a previous local registry of 48 and the old pushed review branch of 25. Current repository evidence explains the count: the formal research branch currently exposes 47 eligible targets, and the old review contributes one additional `components/whole_system_governed_runtime_v0.1.0` target, yielding 48 after selective replay. The three AION-prefixed public candidate directories also contain a nested formal-research candidate, but it is not used as authority because the current remote formal research branch is newer and authoritative under the stated order.

## Source authority and selective replay

```text
1 current Owner instruction
2 current approved governance/canonical records
3 current main
4 current formal research branch
5 authorized local completion candidate
6 old orphan review branch
7 Manus inference
```

The whole-system runtime, validation runner, and related review evidence are therefore replayed selectively from the old review artifact with explicit source attribution. Research modules already present on current formal research are preserved from that branch rather than copied from local artifacts.

## Old review disposition

```text
SUPERSEDED_REVIEW_ARTIFACT
NOT_MERGE_CANDIDATE
RETAINED_FOR_PROVENANCE
```
