# Main Transition Governance Falsification Review — 2026-09-19

Status: `FALSIFICATION_REVIEW / GOVERNANCE_HARDENING_CANDIDATE / MERGE_NOT_AUTHORIZED`  
Document-Class: `RESEARCH_REFERENCE / QUALITY_REVIEW`  
Target control: `Main Transition Authority Gate`  
Deployment: `FALSE`

## 1. Question

This review asks the inverse question:

> Under what conditions could the current main-transition governance appear stronger than it really is?

The purpose is not to prove the gate is secure. The purpose is to identify where
the present evidence ceiling is lower than the wording or operator intuition could
suggest.

## 2. Live repository state inspected

At review time:

```text
MAIN = a711e3110ce353e9407390dff0819177b162283c
MAIN_PROTECTION_RULESET_ID = 20545803
RULESET_UPDATED_AT = 2026-08-15T22:52:13.759+08:00
RULESET_ENFORCEMENT = active
STRICT_REQUIRED_STATUS_CHECKS = true
BYPASS_ACTORS = []
REQUIRED_APPROVING_REVIEW_COUNT = 0
```

Required checks were bound to integration ID `15368`:

```text
Fresh exact-head Human Owner approval receipt
Python 3.11
Python 3.12
```

This is a positive control because GitHub supports pinning a required status check
to a specific GitHub App source. It mitigates same-name status spoofing from an
unexpected integration; it does **not** make candidate-modified GitHub Actions workflow
logic independent of the candidate. GitHub's required-check troubleshooting guidance
also states that required status checks do not take workflow, matrix, or event-trigger
type into account. The current rule therefore does not cryptographically bind the
required context to one immutable workflow definition.

## 3. Counterexample findings

### F1 — account attribution can be mistaken for direct human action

GitHub documents that a GitHub App can make API requests on behalf of a user and
that such actions are attributed to that user. GitHub webhook documentation also
warns against assuming that the `sender` property always identifies the person who
caused an event.

Therefore:

```text
EVENT_SENDER_MATCH
!= DIRECT_HUMAN_UI_ACTION

EVENT_SENDER_MATCH
!= INDEPENDENT_HUMAN_INTENT_PROOF
```

The current v0.1 receipt mixes authority origin and repository transport inside
`approval_source`. This is a provenance weakness.

Disposition:

```text
CURRENT_GATE_CAN_VERIFY = STRUCTURAL_ACCOUNT_EVENT + ASSERTION
CURRENT_GATE_CANNOT_VERIFY = PHYSICAL_INTERACTION_ORIGIN
```

Future hardening should separate:

```text
AUTHORITY_ORIGIN
REPOSITORY_TRANSPORT
TRANSPORT_MEDIATION
```

### F2 — a candidate can influence the control used to evaluate itself

GitHub documents that `pull_request` workflows use the PR merge branch, and default
`actions/checkout` checks out that merge branch.

The current authority workflow executes a validator from the checked-out repository
state. Therefore a PR that edits the authority workflow or validator can influence
its own authority-check implementation.

```text
SELF_MODIFIED_CONTROL_PASS
!= INDEPENDENT_CONTROL_VALIDATION

CHECK_NAME_PLUS_APP_SOURCE
!= WORKFLOW_DEFINITION_BINDING
```

This is the strongest technical assurance gap found in this review.

Immediate governance compensation:

```text
CONTROL_PLANE_CHANGE
= any change to authority workflow / validator / generator / receipt schema / tests

CONTROL_PLANE_CHANGE
-> mandatory exact diff against trusted main
-> candidate gate PASS is necessary but not sufficient
-> semantic weakening = HOLD
```

Longer-term engineering options require a separate design review. Candidate options
include a trusted-base or externally anchored evaluator, but no implementation choice
is promoted by this document.

### F3 — exact head does not bind the complete approved diff

The current receipt binds `target_head` but not the exact `main` base SHA.

The live ruleset's strict-required-status policy is a meaningful compensating
control because GitHub requires the branch to be tested with the latest base before
merge. It does not make base identity part of the Human Owner's receipt.

```text
TARGET_HEAD_BINDING
!= TARGET_HEAD_PLUS_BASE_BINDING
```

Future schema hardening candidate:

```text
target_head_sha
target_base_sha
```

Operationally:

```text
BASE_MOVED_AFTER_REVIEW -> RECHECK / HOLD
```

### F4 — merge method is not bound to approval

The live ruleset allows:

```text
merge
squash
rebase
```

The v0.1 receipt approves `MERGE_PR_INTO_MAIN` but does not bind which merge method
will be used.

```text
APPROVED_PR
!= APPROVED_HISTORY_TRANSFORMATION
```

Until schema hardening:

```text
DEFAULT_MERGE_METHOD = merge
NONDEFAULT_MERGE_METHOD -> FRESH_HUMAN_OWNER_APPROVAL_REQUIRED
```

A future receipt may bind `merge_method`, or the live ruleset may be narrowed by a
separate Human Owner repository-settings decision.

### F5 — ruleset state is external and mutable

GitHub rulesets are repository-side configuration, not Git-tracked source.

```text
COMMITTED_GOVERNANCE_DOC
!= LIVE_RULESET_STATE
```

The current ruleset is strong in several respects:

- active enforcement;
- strict required-status policy;
- no bypass actors;
- required status checks pinned to a specific integration.

But these facts can change without a source commit.

Operational hardening:

```text
PRE_MERGE_LIVE_RULESET_RECHECK = REQUIRED
RULESET_ID_AND_UPDATED_AT = RECORD_IN_REVIEW
RULESET_DRIFT = HOLD_UNTIL_REASSESSED
```

### F6 — freshness is receipt-event freshness, not proof of fresh human intent

The validator compares the declared approval timestamp to the PR edit event.

That is useful against stale receipt replay, but:

```text
TIMESTAMP_FRESH
!= HUMAN_INTENT_FRESHNESS_INDEPENDENTLY_VERIFIED
```

The existing epistemic boundary already says human intent is not independently
verified. Future schema wording should avoid implying more.

### F7 — independent separation of duties is limited

NIST SP 800-53 AC-5 describes separation of duties as a control for reducing abuse
of authorized privileges.

This repository is currently a single-Human-Owner project and the live ruleset
requires zero approving reviews.

```text
SINGLE_OWNER_MODEL
!= INDEPENDENT_HUMAN_SEPARATION_OF_DUTIES
```

Independent AI review, CI, and exact-head checks are useful compensating controls,
but they are not a second Human approver and do not establish NIST conformance.

## 4. Positive controls that survived the falsification attempt

The review did **not** find evidence that every part of the gate is weak.

The following controls remain substantively useful:

```text
EXACT_PR_BINDING = PRESENT
EXACT_HEAD_BINDING = PRESENT
FRESH_EVENT_BOUND = PRESENT
FAIL_CLOSED_TO_HOLD = PRESENT
PRIOR_AUTHORIZATION_INHERITANCE = REJECTED
QA_AS_AUTHORITY = REJECTED
AI_REVIEW_AS_HUMAN_APPROVAL = REJECTED
NO_BYPASS_ACTORS = OBSERVED
STRICT_REQUIRED_STATUS_POLICY = OBSERVED
REQUIRED_CHECK_APP_SOURCE_PINNING = OBSERVED
```

GitHub documents that app-pinning a required status check prevents a same-named
status from a different source from satisfying the requirement.

## 5. Revised governance principles

```text
PRINCIPLE_1
AUTHORITY_ORIGIN != AUTHORITY_TRANSPORT

PRINCIPLE_2
ACCOUNT_ATTRIBUTION != INTERACTION_ORIGIN

PRINCIPLE_3
CONTROL_SELF_MODIFICATION != INDEPENDENT_CONTROL_VALIDATION

PRINCIPLE_4
EXACT_HEAD != COMPLETE_TRANSITION_IDENTITY

PRINCIPLE_5
LIVE_EXTERNAL_CONFIGURATION != VERSIONED_REPOSITORY_STATE

PRINCIPLE_6
FRESH_STRUCTURAL_RECEIPT != INDEPENDENT_PROOF_OF_FRESH_HUMAN_INTENT

PRINCIPLE_7
SINGLE_OWNER_COMPENSATING_CONTROLS != SEPARATION_OF_DUTIES

PRINCIPLE_8
PASSING_REQUIRED_CHECK != UNBOUNDED_SECURITY_ASSURANCE
```

## 6. Recommended implementation sequence

Do not implement all findings in one uncontrolled change.

```text
A. merge documented event-order / falsification principles only after fresh review
B. separately design receipt schema v0.2:
   - authority origin vs repository transport
   - target base SHA
   - merge method
   - ruleset observation reference
C. separately design candidate-independent authority evaluation
D. only then consider repository-settings changes
```

The control-plane change in C requires particular care because a faulty migration
could lock legitimate merges or weaken the gate.

## 7. External calibration sources

GitHub:

- https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-with-a-github-app-on-behalf-of-a-user
- https://docs.github.com/en/webhooks/webhook-events-and-payloads
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks

NIST:

- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

Use is methodological only.

```text
EXTERNAL_GUIDANCE != PROJECT_CERTIFICATION
NIST_CONTROL_ANALOGY != NIST_CONFORMANCE
GITHUB_PLATFORM_FEATURE != HUMAN_INTENT_PROOF
```

## 8. Disposition

```text
REPOSITORY_CORRUPTION = NO
UNAUTHORIZED_PR187_MERGE = NOT_ESTABLISHED

EVENT_ORDER_GAP = CONFIRMED
ACCOUNT_ATTRIBUTION_PROVENANCE_GAP = CONFIRMED
CONTROL_SELF_MODIFICATION_ASSURANCE_GAP = CONFIRMED
BASE_BINDING_GAP = CONFIRMED
MERGE_METHOD_BINDING_GAP = CONFIRMED
RULESET_DRIFT_RISK = CONFIRMED
SEPARATION_OF_DUTIES_LIMIT = CONFIRMED

CURRENT_GATE_VALUE = REAL_BUT_BOUNDED
CURRENT_GATE_ASSURANCE_CEILING = STRUCTURAL / PROCEDURAL
MERGE_AUTHORITY_FOR_THIS_REVIEW = NONE
```
