# QA Evidence Semantics

> For present semantic repository standing, read [`../docs/CURRENT_STATE.md`](../docs/CURRENT_STATE.md). This file defines QA evidence semantics and preserves historical exact-head examples; it is not a current-state authority.

The `qa/` directory contains committed quality-assurance evidence snapshots and supporting review records. Some filenames retain the historical `CURRENT_*` convention, but a committed file cannot serve as a self-referential exact-HEAD record after the commit that contains it is created.

## Committed snapshot versus live exact-head evidence

The committed `qa/CURRENT_*` files are repository evidence snapshots. Their embedded `target_head`, test counts, timestamps, or coverage counts describe the source state at which those files were generated. They must not be interpreted as automatically tracking the tip of `main`.

```text
COMMITTED_QA_SNAPSHOT != LIVE_EXACT_HEAD_EVIDENCE
FILENAME_CURRENT != AUTOMATIC_HEAD_FRESHNESS
CI_GENERATED_QA_VIEW = OUT_OF_TREE_EXACT_HEAD_EVIDENCE
```

This distinction is necessary because several QA generators write the exact Git `HEAD` into their output. If that output were then committed as a claim about the commit containing itself, the new commit would have a different SHA and the embedded head would immediately be stale. Manual replacement of generated fields is therefore not an acceptable freshness mechanism.

## Historical exact-main example — PR #56

PR #56 was merged as:

```text
PR56_CANDIDATE_HEAD = 67a901b16188e441040c8927806f41dd90e04b66
PR56_MERGE_COMMIT = 35840d4d5629872e830ee669a15b67b183091692
PR56_MERGE_TREE = f1de908abb11f4317ed96a7c92019a8d6e47386e
```

The post-merge `main` push was independently re-executed by repository workflows on that exact merge commit:

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
IQC = PASS
PUBLIC_TREE_SCAN = PASS
CURRENT_HEAD_RELEASE_VERIFICATION = PASS
```

Those workflow results are the exact-head evidence for `main@35840d4d5629872e830ee669a15b67b183091692`. The committed QA files remain historical snapshots unless and until a separately governed snapshot is intentionally materialized; they are not silently rewritten to pretend they were generated at a later head.

## Scientific and governance boundaries

```text
QA_PASS != SCIENTIFIC_VALIDATION
CI_PASS != THEORY_CONFIRMATION
TEST_PASS != SUBJECTIVITY_EVIDENCE
WHOLE_SYSTEM_VALIDATION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

See also [`../docs/POST_MERGE_STATE_RECONCILIATION_2026-08-26.md`](../docs/POST_MERGE_STATE_RECONCILIATION_2026-08-26.md) for the historical repository-level post-merge reconciliation record.
