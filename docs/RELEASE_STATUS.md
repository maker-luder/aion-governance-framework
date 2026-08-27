# Release and Repository Status

> This file records release/termination standing and major bounded transitions. For the concise **present semantic state**, read [`CURRENT_STATE.md`](CURRENT_STATE.md). For exact-commit engineering status, use live GitHub/CI evidence.

## Historical closure state — 2026-08-20

```text
FREEZE_EFFECTIVE_DATE = 2026-08-18
REPOSITORY_STATE_EVENT = INDEFINITE_FREEZE
TERMINATION_EFFECTIVE_DATE = 2026-08-20
PROJECT_WORK_LOOP = TERMINATED
ACTIVE_ENGINEERING = NO
ACTIVE_RESEARCH_MATERIALIZATION = NO
ACTIVE_RESEARCH_PROGRAM = NO
NEW_PUBLIC_RELEASE = NO
RELEASE_PIPELINE = STOPPED
DEPLOYMENT = NO
AUTOMATIC_RESTART = NO
RESEARCH_QUESTION = NOT_DECLARED_PROVEN_OR_DISPROVEN
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
PHENOMENAL_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
```

This block preserves the closure meaning at its event time. It is not rewritten to pretend later bounded events had already occurred.

## Later explicitly authorized bounded events

After termination, individually scoped events were merged through separate protected-main decisions. Important milestones include:

- PR #49 — AION Evidence Interop Profile v0.1.0;
- PR #50 — Four-Domain Evidence Bridge v0.1.0;
- PR #51 — shared AION / Astra Agent Execution Substrate v0.1.0;
- PR #52 — AION / Astra runtime-to-substrate integration;
- PR #53 — adapter registry and durable execution-evidence loop;
- PR #54 — research-question / repository-state documentation reconciliation;
- PR #56 — Endogenous Goal Dynamics × Four-Domain bounded research materialization;
- PR #63 — governed knowledge, seven-state experiments, AION/Astra isolation accounting, and theory-plural subjectivity-relevant research convergence.

PR #63 merged the approved exact candidate head `e85651583d204162e309ffd968f31249a8bce983` as merge commit `2d37aa92c2bc454abcea41b2174e3415d98865b1`.

```text
PROJECT_WORK_LOOP = TERMINATED
POST_TERMINATION_BOUNDED_MAINTENANCE = PRESENT_IN_MAIN
POST_TERMINATION_BOUNDED_RESEARCH_MATERIALIZATION = PRESENT_IN_MAIN
PROJECT_RESTART = NO
RESEARCH_RESTART = NO
ACTIVE_RESEARCH_PROGRAM = NO
BOUNDED_MAINTENANCE != PROJECT_RESTART
BOUNDED_RESEARCH_MATERIALIZATION != RESEARCH_PROGRAM_RESTART
```

## Current scientific boundary

Later engineering and bounded research materialization improve inspectability, provenance, falsifiability and experimental control. They do not upgrade the scientific conclusion.

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
SCIENTIFIC_DISPOSITION = HOLD
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
IDENTITY_CONTINUITY = NOT_ESTABLISHED
INDEPENDENT_REPLICATION = NOT_ESTABLISHED
WHOLE_SYSTEM_VALIDATION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED

ENGINEERING_CAPABILITY != SUBJECTIVITY_EVIDENCE
RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH
CI_PASS != SCIENTIFIC_VALIDATION
```

For the fuller current semantic state, see [`CURRENT_STATE.md`](CURRENT_STATE.md).

## Exact-head QA rule

Historical PR bodies, workflow runs, and committed QA snapshots remain evidence for the exact commits they evaluated. They are not self-updating current-tip ledgers.

```text
COMMITTED_QA_SNAPSHOT != AUTOMATIC_CURRENT_TIP
HISTORICAL_CI_PASS != FUTURE_HEAD_PASS
QA_PASS != MERGE_APPROVAL
```

Use [`../qa/README.md`](../qa/README.md) for QA evidence semantics and GitHub Actions for live exact-head status.

## Historical authority rule

The event order remains:

1. 2026-08-18 — indefinite repository freeze;
2. 2026-08-20 — project-work-loop termination;
3. later — individually authorized bounded maintenance, documentation reconciliation and bounded research-materialization events.

```text
FREEZE != TERMINATION
TERMINATION != LATER_BOUNDED_EVENT
HISTORICAL_RECORD = PRESERVE_EVENT_TIME_MEANING
RETROACTIVE_REWRITE = FORBIDDEN
RETROACTIVE_GREENWASH = FORBIDDEN
HISTORICAL_RECORD != CURRENT_STATE
```

Historical event records include [`PROJECT_TERMINATION_NOTICE_2026-08-20.md`](PROJECT_TERMINATION_NOTICE_2026-08-20.md), [`REPOSITORY_FREEZE_NOTICE_2026-08-18.md`](REPOSITORY_FREEZE_NOTICE_2026-08-18.md), and [`history/`](history/).

## Whitepaper lineage

```text
v0.14.23 = STABLE / FROZEN METHOD BASELINE
v0.14.24 = INTERNAL RESEARCH CANDIDATE
FILE_PRESENCE != CANONICAL_AUTHORITY
LATER_FILENAME != AUTHORITATIVE_VERSION
```

Later bounded artifacts do not automatically supersede the stable research-method lineage.

## Where to read next

- First-time reader: [`START_HERE.md`](START_HERE.md)
- Present semantic standing: [`CURRENT_STATE.md`](CURRENT_STATE.md)
- Research method: [`SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](SUBJECTIVITY_EVIDENCE_PROTOCOL.md)
- Documentation classes: [`INDEX.md`](INDEX.md)
- Provenance: [`PROVENANCE.md`](PROVENANCE.md)
