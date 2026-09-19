# PR #187 main-transition event-order learning — 2026-09-19

Status: `CLOSED_EVENT / OPERATIONAL_LEARNING_CAPTURED / NO_REPOSITORY_CORRUPTION`  
Document-Class: `HISTORICAL`  
Scope: repository-observable main-transition workflow behavior around PR #187  
Canonical effect: `NONE`  
Deployment: `FALSE`

## 1. Event boundary

This record preserves the repository-visible event sequence only. It does not treat
conversation-side tool-availability misclassification as a repository defect.

```text
ASSISTANT_TOOL_AVAILABILITY_MISCLASSIFICATION
= OUTSIDE_REPOSITORY_INCIDENT_SCOPE

REPOSITORY_CORRUPTION
= NO

SOURCE_CONTENT_DAMAGE
= NO

MAIN_HISTORY_REWRITE
= NO
```

## 2. Exact target

```text
TARGET_PR = 187
TARGET_HEAD = 85887450e836974e6ed24e136886a0767eee91b8
MERGE_COMMIT = a711e3110ce353e9407390dff0819177b162283c
MERGED_AT = 2026-09-19T15:23:48Z
```

## 3. Observed authority-gate sequence

The same candidate head produced different authority-gate outcomes because the
GitHub event type changed.

```text
Main Transition Authority Gate #1377
= SUCCESS
= fresh PR-body authority-receipt edit

then

DRAFT -> READY_FOR_REVIEW

triggered

Main Transition Authority Gate #1378
= FAILURE / HOLD
```

The #1378 validator diagnostics were:

```text
fresh approval must arrive in a pull_request edited event
fresh approval event must specifically edit the pull request body
```

The same run still reported:

```text
TARGET_PR_MATCH = TRUE
TARGET_HEAD_MATCH = TRUE
TIMESTAMP_FRESH = TRUE
HUMAN_OWNER_EXPLICIT_APPROVAL = GIVEN
```

Therefore the HOLD was not evidence that the exact head was corrupted or that the
receipt payload had become false. It was an event-binding failure: the
`ready_for_review` event is deliberately non-authorizing.

A subsequent fresh PR-body receipt edit produced:

```text
Main Transition Authority Gate #1379
= SUCCESS
```

PR #187 was then merged at the unchanged exact head.

## 4. Root-cause classification

```text
REPOSITORY_DEFECT = NOT_ESTABLISHED
VALIDATOR_DEFECT = NOT_ESTABLISHED
WORKFLOW_DEFECT = NOT_ESTABLISHED

PRIMARY_CAUSE
= OPERATOR_SEQUENCE_ALLOWED_FINAL_RECEIPT_BEFORE_NONFINAL_PR_STATE_TRANSITION

CONTROL_BEHAVIOR
= EXPECTED_FAIL_CLOSED
```

The workflow intentionally runs on `ready_for_review`, while the validator
intentionally accepts authority only from a fresh PR-body `edited` event.
Those two facts are compatible, but they make operation order material.

## 5. Quality disposition

No NCR is opened for the gate itself because it behaved according to its declared
fail-closed semantics.

```text
NCR_FOR_GATE_BEHAVIOR = NO
CAPA_CORRECTIVE_ACTION_FOR_DEFECT = NO
PREVENTIVE_PROCEDURAL_HARDENING = YES
REGRESSION_TEST_ADDED = YES
```

The preventive action is to make the safe operator order explicit and pin the
observed `ready_for_review -> HOLD` behavior in a regression test.

## 6. Learned invariant

```text
SAME_HEAD != SAME_AUTHORITY_EVENT
PRIOR_AUTHORITY_PASS != CURRENT_MERGE_READINESS

EXACT_HEAD
+ EXACT_EVENT
+ EXACT_ORDER
= REQUIRED_OPERATIONAL_BINDING
```

Safe sequencing:

```text
FINALIZE_EXACT_HEAD
-> COMPLETE_REVIEW_AND_REQUIRED_CHECKS
-> MARK_READY_IF_NEEDED
-> HUMAN_OWNER_FRESH_APPROVAL
-> FINAL_PR_BODY_RECEIPT_EDIT
-> AUTHORITY_GATE_PASS
-> NO_INTERVENING_PR_STATE_OR_METADATA_TRANSITION
-> MERGE
```

This historical record does not itself change merge authority or authorize any
future transition.
