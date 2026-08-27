# Documentation Governance

## Purpose

This control prevents document volume, historical preservation, and component-local notes from becoming an accidental authority system.

```text
FILE_COUNT != AUTHORITY
NEWER_FILE != MORE_AUTHORITATIVE
HISTORICAL_RECORD != CURRENT_STATE
SUPPORTING_DOCUMENT != ENTRY_POINT
DOCUMENTATION_CONVERGENCE != RESEARCH_SCOPE_EXPANSION
```

## Reader authority order

For ordinary readers, use this order:

1. [`../START_HERE.md`](../START_HERE.md) — single reader entry point;
2. [`../CURRENT_STATE.md`](../CURRENT_STATE.md) — semantic current-state summary;
3. [`../RESEARCH_CONTRIBUTION_ONE_PAGER.md`](../RESEARCH_CONTRIBUTION_ONE_PAGER.md) and [`../SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](../SUBJECTIVITY_EVIDENCE_PROTOCOL.md) — research contribution and method;
4. [`../ARCHITECTURE.md`](../ARCHITECTURE.md), [`../NON_CLAIMS.md`](../NON_CLAIMS.md), [`../PROVENANCE.md`](../PROVENANCE.md) — architecture, epistemic boundaries and provenance;
5. governance/component/research/evidence documents needed for a specific question;
6. dated/history records for event-time reconstruction.

This reader order does not override a more specific governance control for a specific action. For example, a main-transition authority receipt is still governed by its dedicated validator and protocol.

## Document classes

Every public document belongs to one of these semantic classes:

| Class | Meaning | Typical location |
|---|---|---|
| `CURRENT_ENTRY` | First-stop reader navigation | root `README*`, `docs/START_HERE.md` |
| `CURRENT_STATE` | Semantic present-state summary | `docs/CURRENT_STATE.md` |
| `CURRENT_CORE` | Current research/governance method needed for interpretation | selected undated `docs/*.md` |
| `CURRENT_SUPPORT` | Supporting policy, process, legal, security or operational reference | root policy files, `docs/governance/`, selected `docs/*.md` |
| `COMPONENT_LOCAL` | Documentation whose authority is bounded to a component/lab | `components/**`, `research-labs/**`, `experiments/**` |
| `RESEARCH_REFERENCE` | Research material supporting interpretation without becoming current-state authority | `docs/research/` and explicitly marked research references |
| `ENGINEERING_EVIDENCE` | Engineering/QA evidence and evidence semantics | `docs/evidence/`, `qa/`, generated workflow evidence |
| `HISTORICAL` | Dated or event-specific records preserved for provenance | `docs/history/`, dated notices/reconciliations/snapshots |
| `SUPERSEDED` | Retained only when provenance requires it; must point to the replacing authority | explicit case-by-case designation |

## Path classification rules

These rules classify the repository without requiring an ever-growing hand-maintained list of every file:

- root `README.md` and `README.zh-TW.md` → `CURRENT_ENTRY`;
- `docs/START_HERE.md` → `CURRENT_ENTRY`;
- `docs/CURRENT_STATE.md` → `CURRENT_STATE`;
- `docs/INDEX.md` and `docs/README.md` → navigation support, not independent authority;
- `docs/history/**` → `HISTORICAL`;
- dated event/snapshot/reconciliation documents under `docs/` → `HISTORICAL` unless a file explicitly states a narrower role;
- `docs/governance/**` → `CURRENT_SUPPORT` or action-specific active control;
- `docs/evidence/**` and `qa/**` → `ENGINEERING_EVIDENCE`;
- `docs/research/**` → `RESEARCH_REFERENCE`;
- `components/**/README*`, `components/**/docs/**` → `COMPONENT_LOCAL`;
- `research-labs/**/README*`, `research-labs/**/docs/**` → `COMPONENT_LOCAL` / bounded research material;
- `experiments/**` documentation → `COMPONENT_LOCAL` / experimental evidence surface;
- legal/security/community root documents keep their specialized policy role and do not become research-state authority.

If a document does not fit these rules, classify it explicitly in [`../INDEX.md`](../INDEX.md) before treating it as current authority.

## Current-state rule

`CURRENT_STATE.md` is semantic, not a self-updating commit ledger. Exact commit identity, CI status, workflow logs and generated evidence belong to GitHub/CI or generated evidence artifacts.

```text
STATIC_CURRENT_STATE != LIVE_EXACT_HEAD_STATUS
CI_ARTIFACT != SCIENTIFIC_CONCLUSION
COMMITTED_QA_SNAPSHOT != AUTOMATIC_CURRENT_TIP
```

## Historical preservation rule

Do not rewrite dated records merely because current facts changed.

```text
HISTORICAL_RECORD = PRESERVE_EVENT_TIME_MEANING
RETROACTIVE_REWRITE = FORBIDDEN
RETROACTIVE_GREENWASH = FORBIDDEN
```

When a dated record conflicts with current standing, the reader must be routed to `CURRENT_STATE.md`; the historical record remains intact.

## Duplicate-reduction rule

Before adding a new top-level document, ask:

1. Can the content fit into an existing current entry/core document?
2. Is the content component-local and therefore better placed with that component?
3. Is it event-specific and therefore historical?
4. Is it generated evidence rather than prose documentation?
5. Would adding it create another competing entry point?

A new document should be created only when the information has a distinct responsibility that cannot be expressed clearly in an existing source of truth.

```text
NEW_DOCUMENT != NEW_AUTHORITY
NEW_DOCUMENT_REQUIRES_DISTINCT_RESPONSIBILITY = TRUE
```

## Convergence rule

Documentation convergence means reducing ambiguity, not deleting provenance.

```text
CONVERGENCE =
ONE_ENTRY_POINT
+ ONE_CURRENT_STATE
+ CLEAR_AUTHORITY_ORDER
+ DOCUMENT_CLASSIFICATION
+ HISTORY_SEPARATION
+ DUPLICATE_REDUCTION

CONVERGENCE != DELETE_HISTORY
CONVERGENCE != RESEARCH_SCOPE_EXPANSION
```
