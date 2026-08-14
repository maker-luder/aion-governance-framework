# AION Supersession Map v0.1.0

> Supersession in this map is a **question-scoped authority update**, not deletion, historical erasure, or retroactive rewriting. Every dated record remains retained with its original provenance.

## 1. Rules

A later artifact supersedes an earlier artifact only for the explicitly named scope. It does not invalidate the earlier record's historical truth, authorship, test count, branch, or contemporaneous decision. A candidate never supersedes a stable baseline merely because it is newer. A current status record can supersede an older status view while the older view remains `HISTORICAL`.

## 2. Supersession relations

| Relation ID | Earlier artifact / claim | Later artifact / claim | Scope of supersession | Earlier status | Later status | Disposition |
|---|---|---|---|---|---|---|
| `SUP-001` | 2026-08-11 evidence architecture/governance addendum | 2026-08-12 whitepaper/public-source/branch reconciliation | Current standing method, repaired taxonomy and pre-merge gate closure | HISTORICAL | CURRENT | KEEP_RESEARCH_ONLY |
| `SUP-002` | Whitepaper versions before `v0.14.23` | `v0.14.23` stable/frozen integration baseline | Stable integrated baseline for current reconciliation | HISTORICAL | CURRENT | KEEP_RESEARCH_ONLY |
| `SUP-003` | `v0.14.23` stable baseline | `v0.14.24` internal research candidate | Candidate cumulative development only; not canonical or automatic replacement | CURRENT | CURRENT / CANDIDATE | HOLD |
| `SUP-004` | Earlier P2 Packet C validation statement `13 passed` | Current checked-in P2 surface: five test functions and current replay | Present test-count claim only; historical statement retained | HISTORICAL | CURRENT | KEEP_RESEARCH_ONLY |
| `SUP-005` | Earlier C0 acceptance traceability snapshot bound to old head | Current convergence index and exact-head evidence artifacts | Current navigation/traceability for this milestone | SUPERSEDED | CURRENT | PROMOTE metadata only |
| `SUP-006` | Earlier v2 whole-system handoff on another review branch | Current review-branch status and this convergence branch | Branch standing for current work | HISTORICAL | CURRENT | KEEP_RESEARCH_ONLY |
| `SUP-007` | Kimi project summary before source check | Primary-source checked project entries | Narrow source claims only | HISTORICAL / DISCOVERY | CURRENT where checked | KEEP_RESEARCH_ONLY |
| `SUP-008` | P2 `RESEARCH_BASIS.md` Memora reference without title disambiguation | Crosswalk distinction between arXiv:2604.20006 benchmark and arXiv:2602.03315 representation paper | Citation identity correction; no deletion of original note | CURRENT / AMBIGUOUS | CURRENT / CORRECTED | KEEP_RESEARCH_ONLY |
| `SUP-009` | Existing Scope Lock as only branch-level machine gate | Scope Lock plus this adjacent consolidation consistency checker | Adds source/index/dependency consistency checks; does not replace Scope Lock | CURRENT | CURRENT | KEEP_RESEARCH_ONLY |
| `SUP-010` | P2 Packet C as an isolated research package | P2 Packet C plus evidence record, falsifier matrix and readiness entry | Reviewer-facing navigation and admission linkage only | CURRENT | CURRENT / CONSOLIDATED | PROMOTE metadata only |

## 3. Preserved historical records

The following are intentionally not deleted or date-normalized: the original P2 `13 passed` report; 2026-08-09 P2/P3/P5 packet dates; 2026-08-11 and 2026-08-12 reconciliation notes; the Kimi intake provenance; the earlier v2 review handoff; the older C0 traceability snapshot; and any original external-project wording that is now marked `PARTIAL`, `HOLD` or `CORRECTION_REQUIRED`.

## 4. Non-supersession decisions

The following relations are explicitly **not** allowed:

```text
G1 != SUPERSESSION_OF_FOUR_DOMAIN_METHOD
AION_RUNTIME_V0_2 != SUPERSESSION_OF_WHITEPAPER_METHOD
KIMI_REVIEW != SUPERSESSION_OF_PRIMARY_SOURCES
CI_RUN != SUPERSESSION_OF_SCIENTIFIC_REPLICATION
V0.14.24_CANDIDATE != AUTOMATIC_SUPERSESSION_OF_V0.14.23_STABLE
```

## 5. Current status rule

When an artifact is superseded for navigation but still useful for provenance, the map records `SUPERSEDED` or `HISTORICAL` and disposition `KEEP_RESEARCH_ONLY`. The consistency checker rejects any attempt to mark a historical or superseded artifact as the sole current source of truth.
