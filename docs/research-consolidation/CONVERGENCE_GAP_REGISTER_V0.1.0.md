# AION Research Consolidation Convergence Gap Register v0.1.0

## 1. Closed in this milestone

| Gap | Closure | Evidence |
|---|---|---|
| No branch-level research index | Closed | `RESEARCH_INDEX_V0.1.0.md/.json` |
| Four-Domain ↔ G1 dependency ambiguity | Closed at current contract level | `CLAIM_DEPENDENCY_GRAPH_V0.1.0.md/.json`; no scientific-authority edge |
| Duplicate/drifting status and source surfaces | Closed for named surfaces | `SOURCE_OF_TRUTH_MAP_V0.1.0.md/.json`; checker fails closed on critical README/status drift |
| Historical records at risk of being treated as current | Closed for indexed records | `SUPERSESSION_MAP_V0.1.0.md/.json`; dates and older counts retained |
| Kimi claims lacked complete primary-source labels | Closed for verified source set | `EXTERNAL_LITERATURE_CROSSWALK_V0.1.0.md/.json`; unverified project leads remain HOLD |
| No promotion readiness classification | Closed | `PROMOTION_READINESS_MATRIX_V0.1.0.md/.json` |
| P2 Packet C reviewer chain was fragmented | Closed as metadata/evidence chain | Vertical slice, evidence record, falsifier matrix, exact local references |
| P2 Packet C current test count drifted from historical report | Closed | Packet C now distinguishes historical 13 from current five test functions |
| Consolidation artifacts were not machine-enforced | Closed for JSON/index/P2 boundaries | Strict artifact schema, checker, tests and new convergence CI workflow |
| Existing Research Scope Lock was at risk of duplication | Closed | Existing checker retained; new checker only covers adjacent consistency surfaces |

## 2. Safe within current authorization but not yet closed

| Gap | Why it is not closed in this milestone | Safe next action only if separately authorized |
|---|---|---|
| Primary verification of four additional Kimi repositories | Source/license/artifact review was incomplete at cycle cutoff | Open each primary repository and update only the crosswalk status |
| Full branch-wide file inventory | Large repository contains many historical and generated surfaces | Extend the index only when a source affects current promotion/readiness |
| Exact current GitHub CI evidence | Requires push and terminal Action runs at final HEAD | Run the new convergence workflow and existing research-specific workflows where applicable |
| Independent IV&V | Not available from local engineering work | Human Owner/independent reviewer process |
| Review of first metadata promotion batch | Canonical promotion is Owner-controlled | Owner decides whether metadata belongs in canonical state |

## 3. Intentionally blocked, not omissions

| Blocker | Status | Reason |
|---|---|---|
| Formal T2/T3 experiment | HOLD | Requires explicit experimental authorization and protocol execution |
| AION Runtime v0.2 integration into P2 | HOLD | Would create a new runtime evidence edge not present in the Packet C contract |
| G1 implementation/training/model work | HOLD | G1 proposals remain NOT_STARTED / QA_HOLD and this milestone forbids new models/features |
| Real AION/Astra matched-divergence study | HOLD | Requires real runtime histories, preregistration, independent review and additional authorization |
| Event/Lineage semantic freezing or hash migration | HOLD | Existing unresolved contract maturity; must not be invented here |
| Subjectivity, consciousness, identity, moral-status or legal conclusions | REJECT/HOLD | Standing whitepaper and branch non-claims prohibit them |
| `first` / `only` / `unprecedented` contribution claim | REJECT/HOLD | Systematic related-work and independent evidence burden is unmet |
| Main merge, deployment, release, canonical promotion | PROHIBITED | Outside current authorization boundary |

## 4. Acceptance interpretation

The milestone can be complete when all safely actionable consolidation, grounding, consistency, vertical-slice and CI work is committed and exact-head verified. The blocked rows are not silently relabeled as future implementation work; they remain explicit `HOLD`, `REJECT` or `OWNER_DECISION_REQUIRED` boundaries.

## 5. Regression-runner clarification

A direct root-level `python -m pytest -q` invocation is not the repository's authoritative whole-tree runner. It fails during collection because this monorepo intentionally keeps many component packages isolated and has duplicate test module basenames. The existing `scripts/run_component_tests.py` provides the intended per-target `PYTHONPATH` isolation and is the authoritative full regression path used by Quality CI. This milestone does not alter global package discovery or merge unrelated packaging changes into the research consolidation branch.

The direct-root failure is therefore recorded as **runner misuse / non-authoritative discovery**, while the isolated runner provides the actual full regression evidence.
