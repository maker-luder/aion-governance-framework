# Research State Reconciliation — 2026-08-13

## Scope

This is a **bounded repository-state reconciliation checkpoint**, not a broad research consolidation or cleanup pass. All existing local research history is preserved. No main write, reset, rebase, force-push, canonical effect, deployment, or research-history deletion was performed.

## State distinctions

| State label | SHA / status | Meaning |
|---|---|---|
| `TESTED_HEAD` | `7ccbcc4e948376ed2779a41a5bf062714f53dd96` | Exact clean source head used by the final 65-record Zero-Day focused QA. |
| `REPORTING_HEAD` | `40088cbc9eef5363d6eaf2feb7dc761e0f76f271` | Later local report/provenance head; not presented as the exact execution state. |
| `KNOWN_REMOTE_CHECKPOINT` | `78dfc33fe31d05b90d39e7a5313af037c06971cf` | Human Owner-provided and previously push-reported remote research checkpoint. |
| `CACHED_REMOTE_REF_AT_START` | `78dfc33fe31d05b90d39e7a5313af037c06971cf` | Local cached research ref at reconciliation start; now superseded by independently verified remote head `76de1eda…`. |
| `LOCAL_MAIN_REF` | `4b36077993fabb22bf04e06162ea83c623bbb7e6` | Stale local checkout reference; not current main and not modified. |
| `CURRENT_MAIN_REFERENCE` | `abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Current authoritative main reference supplied by Human Owner and independently verified at `origin/main`. |
| `VERIFIED_REMOTE_RESEARCH_HEAD` | `76de1eda82865a37d3a0185336870739ed577153` | Last independently fetched/push-verified remote research head. |
| `FINAL_LOCAL_RECONCILIATION_HEAD` | `2e8d3c5b63909b100d7692fab20f6e74b9920d64` | Local final reconciliation-record head; follow-up push failed before remote write due DNS. |
| `RECONCILIATION_CORE_COMMIT` | `5237aa0d4e05ea5ceb7d7fe39ce15462b683910e` | Core commit containing this receipt and stale-reference corrections. |

## Read-only verification

The local research worktree was clean at the start of reconciliation. `git merge-base --is-ancestor 78dfc33… HEAD` passed for the reported local head `40088cbc…`, so local research history was a safe descendant of the known remote checkpoint. The local `main` ref remained untouched. The supplied current main reference `abb6550…` was initially unavailable in the local object database/ancestry check; this was a state-availability fact, not permission to modify main.

A first read-only remote query encountered DNS failure. After the bounded normal fast-forward push, a read-only fetch succeeded: `origin/review/four-domain-research-materialization = 76de1eda82865a37d3a0185336870739ed577153` and `origin/main = abb6550abfacb4fabc53ec04fca783bcc34acfdb`, matching the Human Owner's current main reference. A later local reconciliation-record commit `2e8d3c5…` was a safe descendant of verified remote `76de1eda…`, but its normal push failed before remote write with `Could not resolve host: github.com`; no tight-loop retry was made. No divergence was observed. Local `main` remained at its stale checkout ref `4b360779…` and was not modified.

## Corrected stale references

The following current-state/reporting surfaces were corrected to distinguish the Owner-authoritative current main reference from historical `4b360779…` records:

- `QA_RECEIPT.md` now uses `CURRENT_MAIN_REFERENCE = abb6550…` and separates `TESTED_HEAD` from `REPORTING_HEAD`.
- `ZERO_DAY_GOVERNANCE_FOCUSED_REPORT.md` now separates `TESTED_HEAD`, `REPORTING_HEAD`, and `CURRENT_MAIN_REFERENCE`.
- Historical v2/branch-consolidation/Manus handoff documents retain old `4b360779…` values only under explicit `HISTORICAL_*` labels or historical notes.

## Source attribution

| Claim/data | Who/where | When/status | Method | Transformation |
|---|---|---|---|---|
| Current main is `abb6550…` | Human Owner instruction plus `origin/main` repository ref | Current and independently verified after successful read-only fetch | Direct task instruction plus `git fetch`/`git rev-parse` | Used only as read-only reference; no main mutation. |
| Local HEAD/reporting state | Repository evidence in `/home/ubuntu/AION-research-worktree` | Observed at reconciliation start | `git rev-parse`, `git status`, ancestry check | Recorded as local/cached repository state, not remote proof. |
| Remote research checkpoint and final head | Human Owner instruction plus repository remote refs | `78dfc33…` was the pre-push checkpoint; `76de1eda…` is now independently verified current remote | Cached ref, safe-descendant check, normal push response, and successful fetch | Recorded as a state transition, not duplicated research evidence. |
| DNS failure | Tool output from read-only `git ls-remote` and later push attempt | Observed operational status | Network command output | Recorded as connectivity evidence only, not research evidence. |

## Invariants

```text
LOCAL_WORKTREE = CLEAN_AFTER_RECONCILIATION_COMMIT
REMOTE_RESEARCH_HEAD = VERIFIED_AT_76de1eda82865a37d3a0185336870739ed577153
LOCAL_FINAL_HEAD = 2e8d3c5b63909b100d7692fab20f6e74b9920d64
LOCAL_FINAL_HEAD_SAFE_DESCENDANT_OF_REMOTE = TRUE
REMOTE_MAIN_HEAD = VERIFIED_AT_abb6550abfacb4fabc53ec04fca783bcc34acfdb
MAIN = READ_ONLY
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
DIVERGENCE_CONCLUSION = NOT_OBSERVED_AFTER_SAFE_FAST_FORWARD_AND_FETCH
```

## Resume disposition

After this bounded reconciliation is finalized, with remote research verified at `76de1eda…` and the later local record preserved after a DNS-blocked push attempt, the previously authorized broad autonomous research cycle may resume. The later local record should be pushed at the next reasonable connectivity checkpoint, not by tight-loop retry. Evidence reuse must use stable provenance references; duplication is not replication; retrieved/remembered/reference information must not be represented as current or new evidence without status and transformation metadata. Negative, null, contradictory, and inconclusive evidence remains preserved.
