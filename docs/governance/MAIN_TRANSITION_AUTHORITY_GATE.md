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
- the timezone-aware approval timestamp is within five minutes of the edit event;
- prior authorization, candidate scope, autonomous research permission, QA, and AI review are explicitly not used as merge authority;
- contradictions and unknown fields are absent;
- `CANONICAL_EFFECT = NONE` and `DEPLOYMENT = FALSE` remain explicit.

Missing, stale, mismatched, inherited, contradictory, malformed, duplicate, ambiguous, or unknown evidence returns `HOLD` with exit status 10.

## Receipt placement

Only after the candidate head is final and the Human Owner gives fresh approval, edit the target PR body once and add exactly one block:

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

## Repository-settings recommendation

The active `Main Protection` ruleset currently requires a PR plus `Python 3.11` and `Python 3.12`, with no bypass actors. It does not require this authority check and its approving-review count is zero.

After this workflow exists on `main`, a separate Human Owner repository-settings decision would be needed to add the status context `Fresh exact-head Human Owner approval receipt` beside applicable Quality checks. This candidate does not modify branch protection or rulesets.

```text
REPOSITORY_SETTINGS_CHANGE = HUMAN_OWNER_DECISION_REQUIRED
```
