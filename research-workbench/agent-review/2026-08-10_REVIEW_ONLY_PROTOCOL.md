# Review-Only Agent Experiment Protocol — 2026-08-10

Status: `RESEARCH_REVIEW_SURFACE`
Main effect: `NONE`
Canonical effect: `NONE`
Automatic merge: `PROHIBITED`
Automatic code modification: `PROHIBITED`

## Purpose

Create a bounded pull-request review surface for an event-triggered GitHub AI reviewer. The reviewer may inspect and comment on the delta between the preserved pre-growth research baseline and the current research checkpoint. Its output is advisory evidence only.

## Source attribution

- `HUMAN_OWNER`: proposed using an event-triggered GitHub agent in review-only mode and explicitly required clear source attribution.
- `CHATGPT`: designed and materialized this review-only experiment protocol, the temporary review branches, and the PR review surface.
- `GITHUB_AI_REVIEWER`: any future review comments authored by GitHub Copilot / GitHub AI review infrastructure must remain attributed to that reviewer and must not be rewritten as Human Owner, ChatGPT, Codex, or repository-author conclusions.
- `GITHUB_ACTIONS_RUNNER`: deterministic CI execution evidence only; not an AI reviewer and not an author of research conclusions.
- `CODEX`: no contribution to this review-only experiment unless separately recorded later.

## Review scope

Primary research deltas:

- `research-labs/external-evidence-normalization_v0.1.0/`
- `research-labs/embodiment-continuity-anchor_v0.1.0/`
- `.github/workflows/research-workbench-ci.yml`

Review questions:

1. Are there correctness bugs, unsafe assumptions, schema inconsistencies, or missing fail-closed paths?
2. Are tests missing meaningful negative or edge cases?
3. Does any implementation collapse provenance, execution evidence, memory continuity, interpretive continuity, relational continuity, or identity claims into one category?
4. Does any code or documentation accidentally imply `main`, canonical, subjectivity, consciousness, or personal-identity promotion?
5. Are there maintainability, typing, packaging, CI, or future-compatibility concerns that should become research observations?

## Evidence classification

Any GitHub AI reviewer output starts as:

```text
RECORD_CLASS = EXTERNAL_AI_AGENTIC_CODE_REVIEW
EXECUTION_CLASS = REVIEW_ONLY
SOURCE_IDENTITY = REVIEW_PLATFORM_REPORTED
INDEPENDENT_IDENTITY_VERIFICATION = NOT_PERFORMED
AUTO_WRITE = NO
AUTO_MERGE = NO
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
```

A review comment is an observation, not a verified defect. A suggested change becomes repository-author engineering only after separate Human Owner + ChatGPT review and an explicit later implementation commit with preserved provenance.

## Promotion locks

```text
AI_REVIEW_COMMENT != VERIFIED_DEFECT
AI_SUGGESTION != ACCEPTED_DESIGN
AI_REVIEW_PASS != REPLICATION
AI_REVIEW_PASS != MAIN_APPROVAL
AI_REVIEW_PASS != CANONICAL_DECISION
AI_REVIEWER != HUMAN_OWNER
AI_REVIEWER != CHATGPT
AI_REVIEWER != CODEX
RUNNER_PASS != AI_REVIEW_OPINION
```

This PR surface is not a promotion PR and must not be merged as a route to `main`.
