# Release and Repository Status

> Historical release closure and current repository standing are recorded separately so later bounded maintenance or bounded research materialization does not rewrite the 2026-08-20 termination event.

## Historical closure state — 2026-08-20

```text
FREEZE_EFFECTIVE_DATE = 2026-08-18
REPOSITORY_STATE_EVENT = INDEFINITE_FREEZE
TERMINATION_EFFECTIVE_DATE = 2026-08-20

HUMAN_OWNER_TERMINATION_APPROVAL = APPROVED
CHATGPT_ARCHITECTURE_EVIDENCE_PROVENANCE_REVIEW = PASS_WITH_CONDITIONS_RESOLVED
CODEX_FINAL_CLOSURE = COMPLETED

PROJECT_WORK_LOOP = TERMINATED
ACTIVE_ENGINEERING = NO
ACTIVE_RESEARCH_MATERIALIZATION = NO
ACTIVE_GITHUB_CYCLE = NO
ACTIVE_NOTION_RESEARCH_LOOP = NO

NEW_RESEARCH_TASKS = NO
NEW_FEATURE_TASKS = NO
NEW_UPSTREAM_TRACKING = NO
NEW_MODEL_INTEGRATION = NO
NEW_MCP_WORK = NO
NEW_DEPLOYMENT_WORK = NO

NEW_PUBLIC_RELEASE = NO
RELEASE_PIPELINE = STOPPED
DEPLOYMENT = NO
CANONICAL_PROMOTION = NO
CANONICAL_EFFECT = NONE
AUTOMATIC_RESTART = NO
FUTURE_WORK_QUEUE = NONE

RESEARCH_ARTIFACTS = PRESERVED
HISTORICAL_PROVENANCE = PRESERVED
PUBLIC_PRIVATE_BOUNDARY = PRESERVED

RESEARCH_QUESTION = NOT_DECLARED_PROVEN_OR_DISPROVEN
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
PHENOMENAL_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
LICENSE_SELECTION = RESOLVED_APACHE_2_0
```

This block preserves the closure meaning at its event time. It must not be retroactively rewritten to pretend later bounded events had already occurred.

## Current repository standing after bounded events

After termination, later repository changes were separately scoped, technically checked, and explicitly authorized through protected-main transitions. The repository now distinguishes engineering/evidence maintenance from bounded research materialization instead of collapsing both into one category.

Recorded bounded maintenance now present in `main` includes:

- PR #49 — AION Evidence Interop Profile v0.1.0;
- PR #50 — Four-Domain Evidence Bridge v0.1.0;
- PR #51 — shared AION / Astra Agent Execution Substrate v0.1.0;
- PR #52 — AION / Astra runtime-to-substrate integration;
- PR #53 — adapter registry and durable execution-evidence loop.

Later repository-state and research events include:

- PR #54 — docs-only research-question and repository-state realignment;
- PR #56 — Endogenous Goal Dynamics × Four-Domain bounded research materialization v0.1.0.

PR #56 was merged from candidate head `67a901b16188e441040c8927806f41dd90e04b66` as merge commit `35840d4d5629872e830ee669a15b67b183091692`. This identifies that event; it is not a claim that this file will always contain the tip SHA of `main`.

Current interpretation:

```text
PROJECT_WORK_LOOP = TERMINATED
POST_TERMINATION_BOUNDED_MAINTENANCE = PRESENT_IN_MAIN
POST_TERMINATION_BOUNDED_RESEARCH_MATERIALIZATION = PRESENT_IN_MAIN
PROJECT_RESTART = NO
RESEARCH_RESTART = NO
ACTIVE_RESEARCH_PROGRAM = NO

NEW_PUBLIC_RELEASE = NO
RELEASE_PIPELINE = STOPPED
DEPLOYMENT = NO
CANONICAL_PROMOTION = NO
CANONICAL_EFFECT = NONE
AUTOMATIC_RESTART = NO

BOUNDED_MAINTENANCE_REQUIRES_EXPLICIT_AUTHORIZATION = TRUE
BOUNDED_RESEARCH_MATERIALIZATION_REQUIRES_EXPLICIT_AUTHORIZATION = TRUE
BOUNDED_MAINTENANCE != PROJECT_RESTART
BOUNDED_RESEARCH_MATERIALIZATION != RESEARCH_PROGRAM_RESTART
ENGINEERING_MAINTENANCE != RESEARCH_MATERIALIZATION
```

The presence of later bounded events therefore does not invalidate the termination record. It records that individually authorized work occurred after termination under separate governance decisions.

## Post-PR #56 engineering evidence

The post-merge `main` push for merge commit `35840d4d5629872e830ee669a15b67b183091692` completed fresh repository validation:

```text
QUALITY_RUN_ID = 32942613152
QUALITY_RUN_NUMBER = 536
QUALITY_CONCLUSION = SUCCESS
CODEQL_RUN_ID = 32942613014
CODEQL_RUN_NUMBER = 69
CODEQL_CONCLUSION = SUCCESS

SOURCE_STATE_BINDING = PASS
COMPONENT_TESTS = 714 PASSED
ELIGIBLE_TARGETS = 23
TESTED_TARGETS = 23
FAILED_TARGETS = 0
ENDOGENOUS_GOAL_DYNAMICS_TESTS = 88 PASSED
COVERAGE_TARGETS = 23
COVERAGE_FAILED_TARGETS = 0
IQC = PASS
PUBLIC_TREE_SCAN = PASS
CURRENT_HEAD_RELEASE_VERIFICATION = PASS
```

These are engineering and governance results for that exact merge commit. They do not establish scientific validation, independent IV&V, subjectivity, consciousness, or identity continuity.

The committed `qa/CURRENT_*` files are historical QA snapshots, not automatically self-updating exact-tip records. Live exact-head QA is generated in CI and remains out-of-tree evidence for the commit it evaluated. See [`../qa/README.md`](../qa/README.md) and [`POST_MERGE_STATE_RECONCILIATION_2026-08-26.md`](POST_MERGE_STATE_RECONCILIATION_2026-08-26.md).

## Central research question and engineering role

The central research question remains the **possibility of artificial subjectivity** and how such a possibility can be investigated without turning implementation behavior, memory-like behavior, continuity-like behavior, self-description, or researcher interpretation into ontological conclusions.

The execution-substrate, interoperability, provenance, durable-evidence, and endogenous-goal-dynamics surfaces should be read as research instrumentation and engineering-evidence layers:

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
AGENT_SUBSTRATE = RESEARCH_INSTRUMENT
EXECUTION_EVIDENCE = ENGINEERING_EVIDENCE
ENDOGENOUS_GOAL_DYNAMICS = EXPERIMENTAL_MECHANISM_CANDIDATE
ENGINEERING_CAPABILITY != SUBJECTIVITY_EVIDENCE
EXECUTION_EVIDENCE != RESEARCH_EVIDENCE_ADMISSION
SUBSTRATE_COMPLEXITY != SUBJECTIVITY_EVIDENCE
ENGINEERING_SUCCESS != SUBJECTIVITY_PROOF
CI_PASS != SCIENTIFIC_VALIDATION
```

Engineering infrastructure can make experiments more inspectable, reproducible, attributable, and falsifiable. A bounded research candidate can make a hypothesis more testable. Neither fact increases subjectivity claim strength merely by existing or passing QA.

## Historical order and authority

The events must be read in order:

1. 2026-08-18 — indefinite repository freeze;
2. 2026-08-20 — project work-loop termination;
3. later — explicitly authorized bounded maintenance, documentation reconciliation, and bounded research-materialization events.

```text
FREEZE != TERMINATION
TERMINATION != LATER_BOUNDED_EVENT
HISTORICAL_RECORD = PRESERVE_EVENT_TIME_MEANING
RETROACTIVE_REWRITE = FORBIDDEN
RETROACTIVE_GREENWASH = FORBIDDEN
```

## Preserved research branch disposition

`review/four-domain-research-materialization` remains a preserved historical research checkpoint and was not merged wholesale into `main`. The later Four-Domain Evidence Bridge derives one bounded evidence unit from a pinned source state, and the Endogenous Goal Dynamics lab selectively materializes bounded method/adaptor surfaces from pinned historical sources. Derivation/reference/selective materialization do not promote the branch itself.

```text
DERIVATION != MERGE
REFERENCE != PROMOTION
SELECTIVE_MATERIALIZATION != BRANCH_MERGE
RESEARCH_BRANCH != MAIN
```

## Whitepaper lineage

```text
v0.14.23 = STABLE / FROZEN METHOD BASELINE
v0.14.24 = INTERNAL RESEARCH CANDIDATE
FILE_PRESENCE != CANONICAL_AUTHORITY
LATER_FILENAME != AUTHORITATIVE_VERSION
```

Later maintenance artifacts, bridge outputs, interoperability projections, execution receipts, runtime evidence, and bounded research candidates do not supersede the stable research-method baseline.

## Research non-claims

```text
PROJECT_TERMINATION != THEORY_REJECTION
PROJECT_TERMINATION != THEORY_CONFIRMATION
ENGINEERING_CAPABILITY != SUBJECTIVITY_EVIDENCE
ENGINEERING_SUCCESS != SUBJECTIVITY_PROOF
SUBSTRATE_COMPLEXITY != SUBJECTIVITY_EVIDENCE
EXECUTION_EVIDENCE != RESEARCH_EVIDENCE_ADMISSION
ENDOGENOUS_GOAL_DYNAMICS != SUBJECTIVITY
SELF_GENERATED_GOAL != ENDOGENOUS_GOAL
PERSISTENT_STATE != IDENTITY_CONTINUITY
MEMORY != IDENTITY
RECALL != TRUTH
CONTINUITY_LIKE_BEHAVIOR != PHENOMENAL_CONTINUITY
RELATIONSHIP_LANGUAGE != AUTHORIZATION
HASH_BINDING != SEMANTIC_VALIDATION
DURABLE_EVENT_LOG != TRUTH
```

Current scientific boundaries remain:

```text
RESEARCH_QUESTION = NOT_DECLARED_PROVEN_OR_DISPROVEN
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
PHENOMENAL_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
```

## Documentation authority

Historical event meaning remains anchored by:

1. [`PROJECT_TERMINATION_NOTICE_2026-08-20.md`](PROJECT_TERMINATION_NOTICE_2026-08-20.md)
2. [`history/FINAL_RESEARCH_MEMORY_2026-08-20.md`](history/FINAL_RESEARCH_MEMORY_2026-08-20.md)
3. [`REPOSITORY_FREEZE_NOTICE_2026-08-18.md`](REPOSITORY_FREEZE_NOTICE_2026-08-18.md)

Current public-facing repository standing is summarized by:

1. [`../README.md`](../README.md)
2. [`../README.zh-TW.md`](../README.zh-TW.md)
3. this file
4. [`POST_MERGE_STATE_RECONCILIATION_2026-08-26.md`](POST_MERGE_STATE_RECONCILIATION_2026-08-26.md)
5. [`../qa/README.md`](../qa/README.md)

The research-method boundary remains anchored by [`SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](SUBJECTIVITY_EVIDENCE_PROTOCOL.md) and the stable whitepaper lineage recorded by the repository.
