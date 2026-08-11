# Autonomous Growth Ledger

Status: `ACTIVE / RESEARCH_ONLY`

```text
BASE_BRANCH = review/four-domain-research-materialization
AUTONOMOUS_RESEARCH_GROWTH = ENABLED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
```

This ledger is the index for unattended research cycles authorized on 2026-08-12.

Each cycle should record, directly or by linked checkpoint/PR:

- cycle date/time;
- starting research-branch SHA;
- research question;
- epistemic role (`HYPOTHESIS`, `MEASUREMENT`, `FALSIFIER`, `EXPERIMENTAL_SUBSTRATE`, or `ENABLING_ONLY`);
- sources and provenance;
- files changed;
- focused validation performed;
- negative/null/contradictory results;
- candidate branch / PR / merge status;
- whether scope lock and CI passed;
- unresolved HOLD items.

No cycle entry is a scientific promotion record.

Machine-checkable cycle requirements are defined by:

- `AUTONOMOUS_GROWTH_CONTRACT.json`
- `AUTONOMOUS_CYCLE_RECORD_SCHEMA.json`
- `scripts/check_autonomous_growth_contract.py`

Cycle JSON records belong under `research-workbench/autonomous-growth/cycles/`. The validator checks branch/effect locks, required fields, explicit positive/negative/null/contradictory/inconclusive classification, repository-relative paths, full starting SHAs, pinned read-only Actions dependencies and validation evidence.

## Initialization — 2026-08-12

```text
AUTHORIZATION = HUMAN_RESEARCH_OWNER
FORMALIZATION = CHATGPT_RESEARCH_REVIEW
CODEX_INVOCATION = NONE
AUTONOMOUS_CYCLE_LIMIT = ONE_COHERENT_INCREMENT_PER_RUN_PREFERRED
LATER_BATCH_REVIEW = REQUIRED_FOR_PROMOTION
```
