# AION Cross-Branch Research Index v0.1.0

> This index is a branch-local, read-only crosswalk. It does not merge, promote, retag or modify any repository setting. Its purpose is to make the relationship between the protected `main` public baseline, the protected research source branch and the independent convergence branch explicit.

## 1. Branch authority table

| Branch | Exact HEAD | Role | Status | Canonical state | Supersession relation | Promotion disposition |
|---|---|---|---|---|---|---|
| `main` | `e079fb7dfe7a04be7dcb94b8a059951a003caa94` | Protected public/default baseline | CURRENT | `PROTECTED_PUBLIC_BASELINE` | Not superseded by this branch; convergence metadata does not replace main | ALREADY_CANONICAL_BASELINE |
| `review/four-domain-research-materialization` | `858442a3ec2439398d188779f4309397bd4926b2` | Protected Four-Domain research source | CURRENT | `RESEARCH_BRANCH_ONLY` | Remains source of truth for original research material; convergence indexes but does not supersede source content | KEEP_RESEARCH_ONLY |
| `engineering/aion-research-consolidation-literature-grounding-readiness-20260814` | `bcc66c788a7d0882d139ae547447deb1f90adae4` (index baseline before this artifact set) | Independent consolidation and readiness candidate | CURRENT | `CANDIDATE_CONVERGENCE_ONLY` | Derived from review branch; adds metadata/index/crosswalk and does not supersede main or research source | PROMOTE (metadata only, Owner review required) |
| `engineering/aion-native-language-feasibility-20260814` | `3dfc21463502e1c32189ae167d92f163ca1a55e8` | Separate Native Language feasibility candidate | CURRENT | `ENGINEERING_RESEARCH_ONLY` | Not part of current research consolidation source; remains separate read-only engineering branch | KEEP_RESEARCH_ONLY |
| `engineering/aion-language-agnostic-runtime-integration-20260814` | `6b81133dc351f5226fa95801254276e421b3e4fe` | Separate cross-language runtime integration source | CURRENT | `ENGINEERING_RESEARCH_ONLY` | Not modified or superseded; remains a separate source branch | KEEP_RESEARCH_ONLY |
| `cleanup/manus-output-consolidation-20260813` | `c43430f9b39a86d11093f3286e9503145fcf0d70` | Historical cleanup branch | HISTORICAL | `HISTORICAL_BRANCH_ONLY` | Retained as dated lineage; not a current source | KEEP_RESEARCH_ONLY |

`CANONICAL_EFFECT=NONE` applies to the entire current convergence branch. `PROMOTE` in this table is only a recommendation for future metadata review; it is not an operation.

## 2. Artifact crosswalk

| Artifact family | `main` | `review/four-domain-research-materialization` | Current convergence branch | Canonical state | Status | Supersession | Promotion disposition |
|---|---|---|---|---|---|---|---|
| Root `README.md` | Present; public baseline navigation | Present; research branch navigation | Present; inherited and branch-local context | Main remains public baseline | CURRENT, branch-scoped | Convergence does not supersede README on main | ALREADY_CANONICAL_BASELINE |
| `RESEARCH_BRANCH_STATUS.md` | Absent | Present; research standing authority | Present; inherited standing authority | Research-only | CURRENT | Not present on main; no main replacement | KEEP_RESEARCH_ONLY |
| Four-Domain repository crosswalk | Absent | Present; original research source | Present; indexed source | Research-only | CURRENT | Consolidation maps it but does not replace it | KEEP_RESEARCH_ONLY |
| Kimi external-project intake | Absent | Present; discovery provenance | Present; indexed and primary-source crosswalked | Research-only | CURRENT | Primary-source crosswalk narrows claims; intake retained | KEEP_RESEARCH_ONLY |
| Whitepaper/web reconciliation 2026-08-12 | Absent | Present; standing method and lineage source | Present; indexed source | Research-only | CURRENT | 2026-08-12 supersedes 2026-08-11 for current standing only | KEEP_RESEARCH_ONLY |
| P2 Packet C and P2 source/tests/fixture | Absent | Present; research implementation | Present; current-count reconciled and vertical-slice linked | Research-only | CURRENT | Historical 13-test statement retained; current five-test surface is authoritative | KEEP_RESEARCH_ONLY |
| G1 README/governance/traceability | Present | Present | Present | Research-only substrate; no authority | CURRENT | No Four-Domain scientific-authority supersession | KEEP_RESEARCH_ONLY |
| AION Runtime v0.2 README/source/tests | Absent | Present | Present | Research-only substrate | CURRENT | No P2 integration or method supersession | KEEP_RESEARCH_ONLY |
| Consolidation index/maps/crosswalk/matrix | Absent | Absent | Present | Candidate convergence metadata | CURRENT | New metadata layer; does not supersede original source artifacts | PROMOTE (metadata only) |
| Native Language feasibility docs/grammar/IR | Absent | Absent | Absent | Separate engineering research-only branch | CURRENT on separate branch | Not part of this branch’s source; do not duplicate here | KEEP_RESEARCH_ONLY |
| Cross-language runtime contract artifacts | Baseline varies by file | Present on separate source branch lineage | Not modified by this branch | Separate engineering research-only | CURRENT on separate branch | Not superseded or copied into this index as source | KEEP_RESEARCH_ONLY |
| Repository Topics | Empty on public repo at inspection time | N/A | Candidate taxonomy only | Repository settings unchanged | CURRENT metadata observation | No settings supersession | HOLD (Owner review) |

## 3. Main↔research resolution rules

`main` is the public/default protected baseline. It is not a container for every research artifact. The protected research branch is the source of truth for Four-Domain research materialization and its dated evidence. The convergence branch is a derived candidate that indexes both; it must never be interpreted as a merge, promotion, or replacement of either source.

When a path exists in both `main` and research, the index records the branch-specific role rather than choosing one silently. For example, `README.md` is current navigation in both contexts, while `RESEARCH_BRANCH_STATUS.md` exists only on the research lineage and is authoritative for research standing. When a path exists only on the research lineage, it remains research-only and is not implied to be public/canonical merely because it is indexed here.

## 4. Drift controls

The companion JSON records protected branch heads exactly and records the convergence branch's parent HEAD as an explicit baseline binding before this index artifact set; the final commit HEAD is reported by the final handoff and CI evidence. The public-discoverability consistency test must fail if the protected branch heads drift from this index, if a first-batch metadata artifact is absent, if a Native Language or cross-language artifact is copied into this branch without an explicit status row, or if the candidate Topics contain forbidden novelty language. A future branch-head update requires an intentional index revision; it is not silently inferred.

## 5. Boundary

```text
INDEX_ONLY = TRUE
REPOSITORY_SETTINGS_MODIFIED = FALSE
TOPICS_APPLIED = FALSE
MAIN_MODIFIED = FALSE
RESEARCH_SOURCE_MODIFIED = FALSE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
