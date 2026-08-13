# Main Transition Authority Gate

Status: `CANDIDATE / FAIL_CLOSED_TO_HOLD`

This control operationalizes the authority boundary recorded by the 2026-08-13 main reconciliation. It does not grant approval and does not infer approval from candidate scope, autonomous research permission, QA, AI review, prior authorization, or silence.

## Enforced boundary

For a pull request targeting `main`, `.github/workflows/main-transition-authority.yml` accepts a receipt only when all of the following are simultaneously true:

- the receipt was added through a fresh `pull_request: edited` event;
- the edit sender matches the configured Human Owner GitHub login;
- `repository`, `target_pr`, `target_branch`, and exact 40-hex `target_head` match the event;
- the approval timestamp is timezone-aware and within five minutes of the body-edit event time;
- the action and explicit statement authorize only this exact merge action;
- prior authorization, candidate-scope approval, autonomous research permission, QA PASS, and AI review are explicitly not used as merge authority;
- contradictions are absent;
- `CANONICAL_EFFECT = NONE` and `DEPLOYMENT = FALSE` remain explicit.

Any missing, stale, mismatched, inherited, or contradictory evidence returns `HOLD` with exit status 10.

## Receipt placement

After the candidate head is final and Human Owner approval is given, edit the target PR body once and add exactly one block:

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

The outer fence above is documentation only. The PR body uses the two HTML markers and the inner JSON fence.

## Evidence and identity boundary

The validator checks event/receipt consistency and the configured GitHub sender account. It does not independently establish the biological identity or mental state of the account operator. Human Owner approval remains a Human Owner act; the tool only rejects structurally absent or inconsistent evidence. Repository branch protection must require this check and applicable Quality checks for platform-level enforcement.

```text
CANDIDATE_SCOPE_APPROVAL != MERGE_APPROVAL
AUTONOMOUS_RESEARCH_PERMISSION != MAIN_TRANSITION_AUTHORITY
QA_PASS != MERGE_APPROVAL
AI_REVIEW != HUMAN_OWNER_MERGE_APPROVAL
PRIOR_AUTHORIZATION != CURRENT_ACTION_AUTHORIZATION
FAIL_CLOSED_TO = HOLD
```
