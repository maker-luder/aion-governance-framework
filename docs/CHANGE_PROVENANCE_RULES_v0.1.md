# Change-Level Provenance Rules v0.1

## Status

- `STATUS = ENGINEERING_GOVERNANCE_CANDIDATE`
- `CANONICAL_EFFECT = NONE`
- `RUNTIME_EFFECT = NONE`
- `OWNER_REVIEW = PENDING`

## Origin of this rule

`PROPOSED_BY = HUMAN_OWNER`

The Human Owner proposed separating proposal origin, implementation origin, review, and approval so project history, AION/Astra state, and collaborator contributions remain distinguishable.

`IMPLEMENTED_BY = CHATGPT`

ChatGPT translated that proposal into this candidate governance format.

`CODEX_CONTRIBUTION = NONE`

Codex did not contribute to this change.

## Required fields for material changes

Every material research, engineering, governance, memory, runtime or canonical-state change should be capable of answering the following independently:

- `PROPOSED_BY` — who originated the proposal, requirement, question or change request;
- `IMPLEMENTED_BY` — who created the actual code, schema, test, document transformation or other implementation;
- `REVIEWED_BY` — who examined the implementation or research product;
- `APPROVED_BY` — who authorized the change to advance to the stated governance level;
- `STATE_OWNER` — which project/agent/state domain the resulting record belongs to, if applicable;
- `SOURCE_EVIDENCE` — what evidence supports the attribution;
- `RUNTIME_EFFECT` — whether an operating runtime was changed;
- `CANONICAL_EFFECT` — whether authoritative canonical state was changed.

## Separation rules

The following are not equivalent:

`SOURCE != AUTHORSHIP != IMPLEMENTATION != REVIEW != APPROVAL != STATE_OWNERSHIP`

A Git commit author/committer identifies the Git operation identity; it does not by itself prove conceptual authorship, implementation authorship or approval authority.

An AI collaborator's implementation does not imply that collaborator originated the research question.

The Human Owner's proposal does not imply the Owner personally authored every implementation line produced from it.

Review does not imply approval unless the project record explicitly grants that authority.

## Actor vocabulary

Use explicit actor values where known:

- `HUMAN_OWNER`
- `CHATGPT`
- `CODEX`
- `AION_RUNTIME`
- `ASTRA_RUNTIME`
- `AUTOMATED_TEST`
- `GITHUB_ACTIONS`
- `SOURCE_UNVERIFIED`

Do not substitute a generic `AI` actor when a specific collaborator is known.

## Attribution confidence

Where evidence is incomplete, use one of:

- `CONFIRMED`
- `SUPPORTED`
- `SOURCE_UNVERIFIED`
- `CONFLICT_REQUIRES_REVIEW`

Never resolve missing attribution by guessing.

## Recommended record shape

```yaml
change_id: EXAMPLE-001
status: CANDIDATE

proposal:
  proposed_by: HUMAN_OWNER
  confidence: CONFIRMED
  source_evidence: owner_current_instruction

implementation:
  implemented_by: CHATGPT
  confidence: CONFIRMED
  artifact_scope:
    - docs/example.md

review:
  reviewed_by: HUMAN_OWNER
  status: PENDING

approval:
  approved_by: HUMAN_OWNER
  status: PENDING

state:
  state_owner: PROJECT_GOVERNANCE
  runtime_effect: NONE
  canonical_effect: NONE

other_contributors:
  codex: NONE
```

## AION / Astra state rule

When a material record affects AION or Astra, provenance must not stop at human/AI collaborator authorship. It must also identify the state domain.

Examples:

- an AION memory record should not silently become Astra memory;
- an Astra event should not silently enter AION life history;
- shared project knowledge should not be mislabeled as either twin's autobiographical memory;
- a shared engineering component should not be treated as shared identity;
- a candidate Runtime artifact should not silently become canonical state.

When ownership is genuinely shared at the engineering/project level, use an explicit shared project/infrastructure scope rather than assigning the record to both individual agents.

## Historical records

Do not retroactively assign fine-grained authorship where evidence is insufficient.

Existing broad statements such as `ChatGPT and Codex assisted` may remain valid for project-level history, but they must not be used to override a confirmed change-level attribution record.

For unresolved historical attribution:

`SOURCE_UNVERIFIED`

is preferred over a guessed actor.

## Promotion rule

This governance candidate must not be treated as canonical solely because it exists in a branch or because tests pass.

Promotion requires explicit Human Owner review and approval.
