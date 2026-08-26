# Post-Merge State Reconciliation — 2026-08-26

This record reconciles the repository-facing state after PR #56 was merged into `main`. It does not modify research mechanisms, historical closure records, the preserved Four-Domain research branch, or any scientific conclusion.

## Merge state inspected

```text
PR = 56
PR_TITLE = research: harden endogenous goal dynamics causal harness
PR_CANDIDATE_HEAD = 67a901b16188e441040c8927806f41dd90e04b66
PR_MERGE_COMMIT = 35840d4d5629872e830ee669a15b67b183091692
PR_MERGE_TREE = f1de908abb11f4317ed96a7c92019a8d6e47386e
MAIN_AT_POST_MERGE_INSPECTION = 35840d4d5629872e830ee669a15b67b183091692
```

PR #56 materialized `research-labs/endogenous-goal-dynamics_v0.1.0/` into `main` as a bounded, experimental research candidate. This event occurred after the 2026-08-20 termination and does not retroactively alter that historical event.

## Post-merge exact-main validation

The `main` push triggered fresh repository workflows on the exact merge commit above.

```text
QUALITY_RUN_ID = 32942613152
QUALITY_RUN_NUMBER = 536
QUALITY_CONCLUSION = SUCCESS
CODEQL_RUN_ID = 32942613014
CODEQL_RUN_NUMBER = 69
CODEQL_CONCLUSION = SUCCESS
```

The Quality run reported:

```text
SOURCE_STATE_BINDING = PASS
DECLARED_HEAD = 35840d4d5629872e830ee669a15b67b183091692
ACTUAL_HEAD = 35840d4d5629872e830ee669a15b67b183091692
SOURCE_TREE_SHA = f1de908abb11f4317ed96a7c92019a8d6e47386e
PUBLIC_TREE_SCAN = PASS
CURRENT_HEAD_RELEASE_VERIFICATION = PASS
TRACKED_FILES = 734
COMPONENT_TESTS = 714 PASSED
ELIGIBLE_TARGETS = 23
TESTED_TARGETS = 23
FAILED_TARGETS = 0
ENDOGENOUS_GOAL_DYNAMICS_TESTS = 88 PASSED
COVERAGE_TARGETS = 23
COVERAGE_FAILED_TARGETS = 0
IQC = PASS
```

This establishes post-merge engineering consistency on that exact commit. It does not establish whole-system scientific validation, independent IV&V, subjectivity, consciousness, or identity continuity.

## Reconciliation findings

Two repository-facing drifts were found after the merge:

1. public status documents still described only the earlier bounded-maintenance sequence and did not yet record PR #56 as a later bounded research-materialization event;
2. committed `qa/CURRENT_*` files retained an older QA snapshot, while the live CI run generated fresh exact-head QA views only inside the workflow workspace.

The second item is not repaired by manually rewriting generated JSON. Several QA generators embed the exact Git `HEAD`; committing such an output creates a different commit SHA and would immediately make an embedded self-claim stale. The repository therefore distinguishes committed QA snapshots from live exact-head CI evidence.

See [`../qa/README.md`](../qa/README.md).

## Post-termination event classification

The repository now distinguishes later event types rather than collapsing them into one category:

```text
POST_TERMINATION_BOUNDED_MAINTENANCE = PRESENT_IN_MAIN
POST_TERMINATION_BOUNDED_RESEARCH_MATERIALIZATION = PRESENT_IN_MAIN
PROJECT_RESTART = NO
RESEARCH_RESTART = NO
ACTIVE_RESEARCH_PROGRAM = NO
AUTOMATIC_RESTART = NO
```

PRs #49–#53 are bounded engineering/evidence-maintenance increments. PR #54 is a docs-only repository-state realignment. PR #56 is a separately authorized bounded research-materialization event.

```text
BOUNDED_MAINTENANCE != PROJECT_RESTART
BOUNDED_RESEARCH_MATERIALIZATION != RESEARCH_PROGRAM_RESTART
ENGINEERING_MAINTENANCE != RESEARCH_MATERIALIZATION
HISTORICAL_TERMINATION != LATER_BOUNDED_EVENT
```

## Preserved scientific boundaries

```text
ENDOGENOUS_GOAL_DYNAMICS = EXPERIMENTAL_MECHANISM_CANDIDATE
REAL_MODEL_LIVE_EXECUTION = NO
CROSS_PROVIDER_REPLICATION = NOT_EXECUTED
SUBJECTIVITY_EVIDENCE_ADMISSION = NOT_AUTOMATIC
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
ACTION_AUTHORITY = NONE
```

This reconciliation is documentary and provenance-oriented. It does not change the implementation or promote the candidate beyond the state already established by PR #56.
