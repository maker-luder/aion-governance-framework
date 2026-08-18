# AION Source-of-Truth Map v0.1.0

> This map distinguishes **current authority for a particular question** from historical context and derived navigation. It does not declare a single file authoritative for every kind of fact.

## 1. Authority rules

The source of truth is selected by **question type**. Executable source and tests are authoritative for implemented behavior. Schemas and validators are authoritative for record shape and admission rules. Current status documents are authoritative for branch standing. Whitepaper reconciliation is authoritative for the standing scientific method and supersession interpretation. Primary external sources are authoritative only for what their authors report. Kimi intake and derived crosswalks are discovery/translation layers, never primary evidence.

A later artifact may supersede a current-state view without deleting the earlier record. Dates remain part of provenance. No document is allowed to promote a test pass, runtime maturity, literature alignment, or repository label into a subjectivity, identity, consciousness, moral-status, canonical or deployment conclusion.

## 2. Map

| Question | Current source of truth | Secondary/derived surface | Historical or superseded surface | Status | Disposition |
|---|---|---|---|---|---|
| What is the research branch standing? | `RESEARCH_BRANCH_STATUS.md` | Root `README.md` navigation and summary | Earlier branch handoffs | CURRENT | KEEP_RESEARCH_ONLY |
| What is the public reviewer orientation? | `README.md` plus status file parity checks | This consolidation index | Historical homepages | CURRENT | KEEP_RESEARCH_ONLY |
| What is the primary scientific evidence method? | Preserved integrated-whitepaper lineage: `research-workbench/four-domain-materialization/2026-08-12/WHITEPAPER_WEB_BRANCH_RECONCILIATION_2026-08-12.md` plus `RESEARCH_BRANCH_STATUS.md` standing interpretation | `docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md` as the current question-scoped operational projection | 2026-08-11 reconciliation remains historical context; `v0.14.23` is stable/frozen and `v0.14.24` is an internal candidate | CURRENT | KEEP_RESEARCH_ONLY |
| Which whitepaper is stable? | Local lineage reconciliation: `v0.14.23` stable/frozen baseline | `v0.14.24` candidate notes | `v0.14.24` is not automatic supersession | CURRENT | KEEP_RESEARCH_ONLY |
| What is Four-Domain construct mapping? | `FOUR_DOMAIN_REPOSITORY_CROSSWALK.md` | P1–P5 packet documents | Earlier gap maps | CURRENT | KEEP_RESEARCH_ONLY |
| What does P2 actually implement? | P2 Python source under `research-labs/four-domain-p2-materialization_v0.1.0/src/` | P2 README and Packet C | Original Packet C count is historical | CURRENT | KEEP_RESEARCH_ONLY |
| What behavior does P2 promise? | `tests/test_p2_compact.py` and `fixtures/p2_synthetic_fixture_a.json` | P2 Packet C and README | Old reported test count | CURRENT | KEEP_RESEARCH_ONLY |
| What is P2's research boundary? | P2 Packet C and README stop boundary | Vertical-slice document | None | CURRENT | KEEP_RESEARCH_ONLY |
| What is the P2 current evidence count? | Current checked-in test function count and current CI run | Packet C reconciliation section | Original `13 passed` statement | CURRENT + HISTORICAL | KEEP_RESEARCH_ONLY |
| What is P2 evidence admission shape? | `schemas/research_evidence_record_v0.2.0.schema.json` and `scripts/validate_research_evidence.py` | P2 evidence record in dated workbench | Older C0 traceability generator | CURRENT | PROMOTE metadata only |
| What is Runtime v0.2? | Runtime source/tests and `components/aion_runtime_v0.2.0/README.md` | Research Workbench CI result | Runtime v0.1 remains distinct | CURRENT | KEEP_RESEARCH_ONLY |
| What is G1? | G1 README, governance, traceability CSV, source/tests | G1 proposal registry and this map | Any external “language core” description | CURRENT | KEEP_RESEARCH_ONLY |
| What is already enforced by Scope Lock? | `scripts/check_research_scope_lock.py` and its workflow | This package's adjacent consistency checker | None | CURRENT | KEEP_RESEARCH_ONLY |
| What does P5 prove? | P5 source/tests/full-run fixture | `FULL_RUN_VERIFICATION.md` | Any interpretation of synthetic convergence as scientific truth | CURRENT | KEEP_RESEARCH_ONLY |
| What do external papers report? | Each cited primary/official page listed in the literature crosswalk | P2 research basis and crosswalk | Kimi summary | CURRENT | KEEP_RESEARCH_ONLY |
| What did Kimi contribute? | `EXTERNAL_CONSCIOUSNESS_PROJECTS_INTAKE.md` as discovery provenance | Primary-source verification note | Unverified summary text | CURRENT | KEEP_RESEARCH_ONLY |
| What did Meta review require? | Owner-supplied review directives recorded in the convergence baseline and this package | Completion audit and readiness matrix | Informal review fragments | CURRENT | KEEP_RESEARCH_ONLY |
| What is a GitHub CI result? | Exact GitHub Actions run at exact HEAD | Local test logs | Older run snapshots | CURRENT when exact-head bound | PROMOTE evidence only |
| What is the older C0 traceability artifact? | Its own dated JSON and index | None | `qa/CURRENT_EVIDENCE_TRACEABILITY.json` | SUPERSEDED/HISTORICAL | KEEP_RESEARCH_ONLY |
| What is the earlier v2 review handoff? | Its own explicit historical header | None | `docs/REVIEW_HANDOFF_REPORT.md` | HISTORICAL | KEEP_RESEARCH_ONLY |

## 3. Resolved duplicate and drift cases

### 3.1 README versus status file

`RESEARCH_BRANCH_STATUS.md` is authoritative for standing fields and deferred/HOLD declarations. `README.md` is the reviewer-facing navigation and summary surface. They are not competing scientific sources. The new checker requires their critical branch-effect and conclusion fields to agree; if they diverge, the check fails rather than selecting one silently.

### 3.2 Whitepaper reconciliation versus older governance addenda

The 2026-08-12 supervised reconciliation is the current source for the standing architecture, stable-vs-candidate lineage and repair dispositions. The 2026-08-11 addenda are preserved as dated historical evidence and may explain how the current position developed. They are not deleted and are not allowed to override later current standing.

### 3.3 P2 packet prose versus implementation/test reality

P2 source code defines behavior. The current five test functions and fixture define replayable expected behavior. Packet C defines research interpretation and stop boundaries. The formerly reported thirteen-test count is retained as a historical statement and is no longer presented as current evidence.

### 3.4 Kimi intake versus primary sources

The Kimi review remains an external discovery lead. Each verified entry in the literature crosswalk points to a primary paper, official venue page, or upstream repository page. Missing primary verification remains `HOLD`; no claim is upgraded from a Kimi summary alone.

### 3.5 Runtime/G1 versus Four-Domain scientific authority

Runtime v0.2 and G1 are implementation substrates, not the scientific method and not authority sources. They can be evaluated by Four-Domain methods but do not establish Four-Domain conclusions. There is no current integration edge to canonicalize.

## 4. Source-of-truth invariants

```text
EXECUTABLE_SOURCE + TESTS = IMPLEMENTED_BEHAVIOR
SCHEMA + VALIDATOR = ADMISSION_SHAPE
RESEARCH_BRANCH_STATUS = CURRENT_BRANCH_STANDING
WHITEPAPER_RECONCILIATION = CURRENT_STANDING_METHOD
PRIMARY_SOURCE = EXTERNAL_AUTHOR_REPORT
KIMI_INTAKE = DISCOVERY_ONLY
HISTORICAL_RECORD = PRESERVED_NOT_CURRENT
README_DRIFT = FAIL_CLOSED
CI_SUCCESS != SCIENTIFIC_VALIDATION
```
