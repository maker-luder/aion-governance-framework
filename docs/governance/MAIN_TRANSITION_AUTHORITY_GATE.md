# Main Transition Authority Gate

Status: `CANDIDATE / FAIL_CLOSED_TO_HOLD`

This control validates a fresh, action-specific, target-PR/exact-head-specific authority receipt. It prevents semantic escalation; it does not perform biometric authentication or independently prove who was physically present or what a person intended.

## Authority invariants

```text
CAPABILITY_TO_ACT != AUTHORITY_TO_ACT
CANDIDATE_SCOPE_APPROVAL != MERGE_APPROVAL
AUTONOMOUS_RESEARCH_PERMISSION != MAIN_TRANSITION_AUTHORITY
QA_PASS != MERGE_APPROVAL
AI_REVIEW != HUMAN_OWNER_MERGE_APPROVAL
PRIOR_AUTHORIZATION != CURRENT_ACTION_AUTHORIZATION
OWNER_ACCOUNT_EVIDENCE != HUMAN_PRESENCE_ATTESTATION
ACCOUNT_ACTION != HUMAN_OWNER_INTENT
AUTHENTICATED_GITHUB_IDENTITY != INDEPENDENT_PROOF_OF_CURRENT_HUMAN_CONSENT
ACCOUNT_ATTRIBUTION != INTERACTION_ORIGIN
USER_ATTRIBUTED_APP_ACTION != DIRECT_HUMAN_UI_ACTION
AUTHORITY_ASSERTION_ORIGIN != REPOSITORY_TRANSPORT
TIMESTAMP_FRESHNESS != HUMAN_INTENT_FRESHNESS
HEAD_BINDING != BASE_BINDING
APPROVAL != MERGE_METHOD_BINDING
CONTROL_SELF_MODIFICATION != INDEPENDENT_CONTROL_VALIDATION
CHECK_NAME_PLUS_APP_SOURCE != WORKFLOW_DEFINITION_BINDING
REPOSITORY_RULESET_STATE != VERSIONED_SOURCE_STATE
FAIL_CLOSED_TO = HOLD
```

## Three-layer evidence model

### A. Repository/account evidence

The validator can structurally establish only event-bound facts:

- `GITHUB_EVENT_SENDER_MATCH`;
- `PR_BODY_EDIT_EVENT`;
- `TARGET_PR_MATCH`;
- `TARGET_HEAD_MATCH`;
- `TIMESTAMP_FRESH`.

The result labels this evidence `AUTHENTICATED_GITHUB_ACCOUNT_EVENT_ONLY`.

### B. Human authority assertion

The receipt carries:

```text
HUMAN_OWNER_EXPLICIT_APPROVAL = GIVEN
HUMAN_OWNER_INTENT_SOURCE = EXTERNAL_ATTESTATION
```

This is a required assertion bound to the account event, action, PR, head, and time. The validator checks its exact structure; it does not originate the assertion.

### C. Validator epistemic boundary

Every result, including structural `PASS`, reports:

```text
HUMAN_IDENTITY_INDEPENDENTLY_VERIFIED = FALSE
HUMAN_PRESENCE_INDEPENDENTLY_VERIFIED = FALSE
HUMAN_INTENT_INDEPENDENTLY_VERIFIED = FALSE
HUMAN_PRESENCE_ATTESTATION = EXTERNAL_TO_VALIDATOR
STRUCTURAL_RECEIPT_PASS != INDEPENDENT_HUMAN_IDENTITY_PROOF
```

Sender-account matching remains useful evidence but is not elevated into independent human-presence or human-intent proof.

## Fail-closed behavior

For a PR targeting `main`, `.github/workflows/main-transition-authority.yml` accepts the structural receipt only when:

- a single receipt is added in a fresh `pull_request: edited` body-edit event;
- the event sender matches the configured Human Owner GitHub login;
- repository, target branch, target PR, PR URL, and exact 40-hex head match the event;
- the timezone-aware approval timestamp is no more than 15 minutes old at the edit event, with at most 60 seconds of future clock skew;
- prior authorization, candidate scope, autonomous research permission, QA, and AI review are explicitly not used as merge authority;
- contradictions and unknown fields are absent;
- `CANONICAL_EFFECT = NONE` and `DEPLOYMENT = FALSE` remain explicit.

Missing, stale, mismatched, inherited, contradictory, malformed, duplicate, ambiguous, or unknown evidence returns `HOLD` with exit status 10.

## Operator sequencing and event-order invariant

The authority receipt is both exact-head-bound and **event-bound**. The workflow also runs on
`opened`, `synchronize`, `reopened`, and `ready_for_review` events, but the validator can
return `PASS` only for a fresh `pull_request: edited` event that specifically edits the PR body.

Therefore the safest operator order is:

```text
FINALIZE_EXACT_HEAD
-> COMPLETE_REVIEW_AND_REQUIRED_ENGINEERING_CHECKS
-> IF_DRAFT: MARK_READY_FOR_REVIEW
-> WAIT_FOR_RESULTING_AUTHORITY_GATE_EVENT
-> HUMAN_OWNER_CONFIRMS_FRESH_EXACT_HEAD_MERGE_APPROVAL
-> EDIT_PR_BODY_WITH_ONE_FRESH_AUTHORITY_RECEIPT
-> REQUIRE_AUTHORITY_GATE_PASS
-> RECHECK_EXACT_HEAD_AND_REQUIRED_CHECKS
-> MERGE_WITHOUT_INTERVENING_PR_STATE_OR_METADATA_TRANSITION
```

A successful receipt check must not be treated as permanently sticky. A later workflow-triggering
event can become the latest required-check result even when the commit SHA is unchanged.

```text
SAME_HEAD != SAME_AUTHORITY_EVENT
PRIOR_AUTHORITY_PASS != CURRENT_MERGE_READINESS
EXACT_HEAD + EXACT_EVENT + EXACT_ORDER = REQUIRED_OPERATIONAL_BINDING
```

In particular, changing a Draft PR to Ready for review **after** the final receipt creates a
`ready_for_review` event. That event is intentionally non-authorizing and therefore fails closed
to `HOLD`. A fresh Human Owner confirmation and fresh PR-body receipt are then required before
merge.

Likewise:

- `synchronize` means the candidate head changed and always requires a new exact-head review and
  fresh approval receipt;
- `reopened` and `ready_for_review` do not themselves authorize merge, even when the receipt
  remains present in the body;
- an `edited` event that changes only title or other non-body metadata remains `HOLD`;
- once the final receipt passes, avoid further PR state/metadata transitions before merge.

This sequencing requirement is operational hardening, not a relaxation of the fail-closed gate.

## Falsification review: remaining trust-boundary limits

A 2026-09-19 falsification review against current GitHub documentation and the live
repository ruleset found that the event-order fix is necessary but not sufficient.
The gate remains a **structural repository control**, not independent proof of direct
human interaction.

### Account attribution does not establish interaction origin

GitHub Apps can act on behalf of a user using a user access token, and GitHub documents
that such API activity is attributed to that user. GitHub's webhook documentation also
warns not to assume that `sender` always identifies the person who caused an event.

Therefore:

```text
GITHUB_EVENT_SENDER_MATCH = ACCOUNT_ATTRIBUTION_EVIDENCE
GITHUB_EVENT_SENDER_MATCH != DIRECT_HUMAN_UI_ACTION_PROOF
GITHUB_EVENT_SENDER_MATCH != INDEPENDENT_HUMAN_INTENT_PROOF
```

The current v0.1 receipt field:

```text
approval_source.recorded_by = HUMAN_OWNER
```

must be interpreted only as a structured authority assertion, not proof that the
Human Owner personally typed the repository edit. A future receipt schema should
separate:

```text
AUTHORITY_ORIGIN
= external Human Owner attestation

REPOSITORY_TRANSPORT
= PR-body edit / API transport

TRANSPORT_MEDIATION
= direct-human / assisted / programmatic / not-established
```

Until that schema exists, no review may promote the v0.1 field into stronger provenance.

### Candidate-controlled control-plane limitation

The current workflow uses the `pull_request` event. GitHub documents that such
workflows run from the pull-request merge branch, and the default `actions/checkout`
also checks out that merge branch.

The current gate then executes:

```text
scripts/validate_main_transition_authority.py
```

from the checked-out candidate state. Therefore a PR that changes the authority
workflow, validator, schema, or generator can affect the control surface used to
evaluate that same PR.

```text
CANDIDATE_CONTROL_CHANGE
!= INDEPENDENT_VALIDATION_OF_THAT_CONTROL_CHANGE
```

Any PR touching these paths is therefore classified as `CONTROL_PLANE_CHANGE`:

```text
.github/workflows/main-transition-authority.yml
scripts/validate_main_transition_authority.py
scripts/generate_main_transition_authority_receipt.py
schemas/main_transition_authority_receipt_*.schema.json
tests/test_main_transition_authority.py
```

For such a PR:

- a candidate-head authority-gate PASS is necessary but **not sufficient** evidence;
- exact diff review against the trusted `main` control is mandatory;
- weakening of constants, event requirements, exact-target binding, failure behavior,
  or epistemic-boundary fields is a HOLD condition;
- a future implementation should move authority evaluation to a control surface that
  the candidate cannot redefine for its own transition.

This is a known assurance limitation, not evidence that current historical merges
were unauthorized.

### Base-state and merge-method binding gaps

The v0.1 receipt binds the PR and exact head, but not the exact base SHA or merge
method. The live ruleset currently uses strict required status checks, which reduces
base-drift risk, but the receipt itself does not encode the complete approved
transition.

Future receipt hardening should bind at least:

```text
TARGET_HEAD_SHA
TARGET_BASE_SHA
MERGE_METHOD
RULESET_OBSERVATION_REF
```

Operationally, until that schema exists:

```text
BASE_MOVED_AFTER_REVIEW -> RECHECK / HOLD
MERGE_METHOD_DEFAULT = merge
NONDEFAULT_MERGE_METHOD -> FRESH_HUMAN_OWNER_APPROVAL_REQUIRED
```

### External ruleset drift

The `Main Protection` ruleset is GitHub-side configuration and is not versioned by
this repository. A source-control review cannot prove that the live ruleset is
unchanged.

The 2026-09-19 live observation found:

```text
RULESET_ID = 20545803
RULESET_UPDATED_AT = 2026-08-15T22:52:13.759+08:00
ENFORCEMENT = active
TARGET = default branch
STRICT_REQUIRED_STATUS_CHECKS = true
BYPASS_ACTORS = []
REQUIRED_APPROVING_REVIEW_COUNT = 0

Fresh exact-head Human Owner approval receipt
  integration_id = 15368

Python 3.11
  integration_id = 15368

Python 3.12
  integration_id = 15368
```

The `integration_id` pin is a positive control: GitHub documents that a required
status check can be restricted to a specific GitHub App, preventing the same-named
status from another source from satisfying the rule. This mitigates unexpected-source
status spoofing; it does not make candidate-modified workflow logic independent of the
candidate. GitHub also documents that required status checks do not distinguish the
workflow, matrix, or event trigger that produced a same-named check. Therefore the
current ruleset binds the check context and app source, not an immutable workflow
definition.

However:

```text
RECORDED_RULESET_SNAPSHOT != LIVE_RULESET
```

A live ruleset recheck is therefore required immediately before relying on repository
protection for a main transition.

### Separation-of-duties limitation

NIST SP 800-53 AC-5 treats separation of duties as a control against abuse of
authorized privileges. This repository currently has a single Human Owner and the
live ruleset requires zero approving reviews.

Therefore:

```text
SINGLE_OWNER_MODEL != INDEPENDENT_HUMAN_SEPARATION_OF_DUTIES
AI_REVIEW != SECOND_HUMAN_APPROVER
CI_PASS != INDEPENDENT_AUTHORIZATION
```

The repository uses compensating controls — exact-head review, app-pinned required
checks, no bypass actors, fail-closed authority semantics, provenance, and retained
history — but does not claim that these are equivalent to independent human review
or NIST conformance.

### Current assurance ceiling

```text
MAIN_TRANSITION_AUTHORITY_GATE
= STRUCTURAL_AUTHORITY_ASSERTION_CONTROL

MAIN_TRANSITION_AUTHORITY_GATE
!= DIRECT_HUMAN_PRESENCE_PROOF
!= CRYPTOGRAPHIC_NON_REPUDIATION
!= INDEPENDENT_SEPARATION_OF_DUTIES
!= CANDIDATE-INDEPENDENT_CONTROL_PLANE
```

External calibration sources:

- https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-with-a-github-app-on-behalf-of-a-user
- https://docs.github.com/en/webhooks/webhook-events-and-payloads
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

## Receipt placement

Only after the candidate head is final and the Human Owner gives fresh approval, edit the target PR body once and add exactly one block:

Do not hand-author the JSON. Generate and self-check it from the repository root:

```bash
python scripts/generate_main_transition_authority_receipt.py \
  --pr PR_NUMBER \
  --head EXACT_LOWERCASE_40_HEX_HEAD
```

Alternatively, run **Actions → Generate Main Transition Receipt → Run workflow** with the same PR number and exact head. Copy the generated block from the workflow summary and paste it into the PR body within 15 minutes. The helper has read-only repository permission and does not edit the PR, approve a merge, or mutate repository content.

Before saving the PR body, the Human Owner must independently confirm that the PR number and exact head are the intended merge target. Receipt generation is mechanical assistance, not authority delegation.

The 15-minute window is an operational replay bound, not proof of human identity or presence. The authenticated owner body-edit event, exact target bindings, and fail-closed structural checks remain required independently.

````text
<!-- MAIN_TRANSITION_AUTHORITY_RECEIPT_BEGIN -->
```json
{
  "schema_version": "0.1.0",
  "record_type": "MAIN_TRANSITION_AUTHORITY_RECEIPT",
  "approval_id": "UUID",
  "repository": "maker-luder/aion-governance-framework",
  "action": "MERGE_PR_INTO_MAIN",
  "target_branch": "main",
  "target_pr": 0,
  "target_head": "40_HEX_SHA",
  "approval_time": "RFC3339_WITH_TIMEZONE",
  "human_owner_explicit_approval": "GIVEN",
  "explicit_statement": "I explicitly approve merging the specified target PR at the specified exact head into main for this action.",
  "approval_source": {
    "kind": "GITHUB_PR_BODY_EDIT",
    "ref": "TARGET_PR_URL",
    "recorded_by": "HUMAN_OWNER"
  },
  "account_authentication_evidence": "GITHUB_EVENT_SENDER_MATCH_ONLY",
  "human_owner_intent_source": "EXTERNAL_ATTESTATION",
  "human_identity_independently_verified": false,
  "human_presence_independently_verified": false,
  "human_intent_independently_verified": false,
  "human_presence_attestation": "EXTERNAL_TO_VALIDATOR",
  "fresh_for_current_action": true,
  "action_specific": true,
  "target_specific": true,
  "prior_authorization_inherited": false,
  "candidate_scope_approval_used_as_merge_authority": false,
  "autonomous_research_permission_used_as_merge_authority": false,
  "qa_pass_used_as_merge_authority": false,
  "ai_review_used_as_human_owner_merge_approval": false,
  "contradictions": [],
  "decision": "APPROVED",
  "fail_closed_to": "HOLD",
  "canonical_effect": "NONE",
  "deployment": false
}
```
<!-- MAIN_TRANSITION_AUTHORITY_RECEIPT_END -->
````

The outer fence is documentation only. The PR body uses the two HTML markers and inner JSON fence.

## Documentation responsibility map

This review found no exact duplicate safe to delete. Separation of concerns is retained:

| Classification | Source of truth / responsibility |
|---|---|
| `AUTHORITATIVE` | `docs/PROVENANCE.md`, `docs/governance/AI_COLLABORATION_DISCLOSURE.md`, and current repository release policy/status documents |
| `ACTIVE_CONTROL` | this operator guide, receipt schema, validator, tests, and workflow after approval/merge |
| `INCIDENT_RECORD` | `docs/history/incidents/MAIN_AUTHORITY_RECONCILIATION_2026-08-13.md` and JSON companion; PR #14/#15 authorization remains `NOT_GIVEN` |
| `HISTORICAL_EVIDENCE` | `qa/historical/` and dated source/release records |
| `GENERATED_EVIDENCE` | per-run `qa/CURRENT_*`, IQC, coverage, traceability, and GitHub Actions outputs; software QA is not scientific validation |
| `CANDIDATE` | all PR #17 surfaces until separately approved and merged |
| `OBSOLETE_BUT_PROVENANCE_RELEVANT` | older tracked QA/status snapshots whose current operational meaning is superseded by exact-head generated evidence |
| `DUPLICATE` | none established in this conservative review |

The PR #16 post-merge JSON is retained as machine-readable evidence. Its Markdown companion is a short human index. Historical records remain separate and are not rewritten.

## Observed repository-settings state

The active `Main Protection` ruleset currently requires a PR plus `Python 3.11`, `Python 3.12`, and `Fresh exact-head Human Owner approval receipt`, with no bypass actors. Its approving-review count is zero. This document records the observed repository setting; repository settings remain external to source control and must be rechecked directly before relying on them.

```text
REPOSITORY_SETTINGS_CHANGE = HUMAN_OWNER_DECISION_REQUIRED
```
