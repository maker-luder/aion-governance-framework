# Change-Level Provenance Rules v0.1

## Status

- `STATUS = ENGINEERING_GOVERNANCE_CANDIDATE`
- `CANONICAL_EFFECT = NONE`
- `RUNTIME_EFFECT = NONE`
- `OWNER_REVIEW = PENDING`

## Origin of this rule

`PROPOSED_BY = HUMAN_OWNER`

The Human Owner proposed separating proposal origin, implementation origin, review, and approval so project history, AION/Astra state, and collaborator contributions remain distinguishable.

`IMPLEMENTED_BY = CHATGPT_TEACHER`

The repository-local ChatGPT Teacher role translated that proposal into this candidate governance format.

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
- `CHATGPT_TEACHER`
- `CHATGPT_WORK`
- `CODEX`
- `AION_RUNTIME`
- `ASTRA_RUNTIME`
- `AUTOMATED_TEST`
- `GITHUB_ACTIONS`
- `SOURCE_UNVERIFIED`

Do not substitute a generic `AI` or generic `CHATGPT` actor when a specific collaborator is known. For new records, `CHATGPT_TEACHER`, `CHATGPT_WORK`, and `CODEX` are distinct actor labels and must not be collapsed merely because they are AI-assisted collaborators.

```text
CONTRIBUTION_ORIGIN != ACTOR_ID
AI_FORMALIZATION + CHATGPT_TEACHER
!= AI_FORMALIZATION + CHATGPT_WORK
!= AI_FORMALIZATION + CODEX
```

Legacy records that only say `CHATGPT` may remain historical when finer attribution cannot be reconstructed; they must not be silently upgraded. Use `SOURCE_UNVERIFIED` when the specific collaborator cannot be recovered.

## Actor surface and pre-delegation binding

The repository distinguishes an operational actor label from the product or
interaction surface through which the contribution was made.

OpenAI's current Help Center distinguishes **Chat**, **Work**, and **Codex** as
separate experiences. It describes Work as an agent for longer multi-step work
and finished deliverables, while Codex is dedicated to software-development and
technical work. The same upstream documentation also states that Work and Codex
can share model families and usage structure while Codex remains a separate view
with separate history. Source checked 2026-09-30:

<https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex>

Repository interpretation:

```text
UPSTREAM_PRODUCT_SURFACE != VERIFIED_MODEL_IDENTITY

CHATGPT_TEACHER
= REPOSITORY_LOCAL_ROLE_LABEL
+ CHATGPT_CHAT_SURFACE

CHATGPT_WORK
= CHATGPT_WORK_SURFACE

CODEX
= CODEX_SURFACE

SHARED_MODEL_FAMILY != SAME_ACTOR
SHARED_USAGE_POOL != SAME_ACTOR
SAME_ACCOUNT != SAME_ACTOR
TASK_DOMAIN != ACTOR
REPOSITORY_TASK != CODEX_BY_DEFAULT
LONG_MULTISTEP_TASK != CHATGPT_WORK_BY_DEFAULT
```

Task semantics must never be used to infer the actor after the fact. A repository
review performed in Work remains `CHATGPT_WORK` even if it modifies code. A
document review performed in Codex remains `CODEX` even if the task is mostly
prose.

For material delegated AI work, bind the expected actor and surface **before**
the delegated step whenever the surface is known:

```text
EXPECTED_ACTOR
EXPECTED_SURFACE
CONTRIBUTION_FUNCTION
SOURCE_EVIDENCE
```

The returned attribution must match that pre-bound record exactly. A collaborator
self-label, output style, task domain, Git committer, or shared OpenAI product
family must not override the pre-delegation binding.

```text
RETURNED_ACTOR != EXPECTED_ACTOR
=> CONFLICT_REQUIRES_REVIEW
=> PROVENANCE_HOLD

RETURNED_SURFACE != EXPECTED_SURFACE
=> CONFLICT_REQUIRES_REVIEW
=> PROVENANCE_HOLD
```

If the pre-delegation surface itself cannot be reconstructed, use
`SOURCE_UNVERIFIED` rather than guessing. A conflict is repaired only from
evidence; it is not silently normalized to whichever actor label best matches the
task.

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
  implemented_by: CHATGPT_TEACHER
  interaction_surface: CHATGPT_CHAT
  confidence: CONFIRMED
  source_evidence: teacher_chat_handoff
  artifact_scope:
    - docs/example.md

review:
  expected_actor: CHATGPT_WORK
  expected_surface: CHATGPT_WORK
  contribution_function: REVIEW
  reviewed_by: SOURCE_UNVERIFIED
  status: PENDING
  source_evidence: work_review_handoff

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
