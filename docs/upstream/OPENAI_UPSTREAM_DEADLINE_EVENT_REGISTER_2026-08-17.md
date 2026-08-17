# OpenAI upstream deadline event register — 2026-08-17

Status: `UPSTREAM_TECHNICAL_EVENT / OWNER-REVIEW CANDIDATE`  
Canonical effect: `NONE`  
Main effect: `NONE`  
Subjectivity conclusion: `NOT_ESTABLISHED`

## Research anchor

Primary research purpose remains: `AI 主體性的可能`.

Upstream lifecycle requirements are treated as technical constraints / infrastructure events. They do not become subjectivity evidence, identity authority, or canonical research conclusions.

`UPSTREAM_REQUIREMENT != SUBJECTIVITY_EVIDENCE`

`UPSTREAM_MODEL_DIRECTIVE != IDENTITY_CHOICE`

## Event OAI-UPSTREAM-2026-08-17-001 — Assistants API shutdown

Official source: OpenAI API deprecations and Assistants migration guide.  
Shutdown date: `2026-08-26`  
Official replacement: `Responses API + Conversations API`.

Official conceptual migration mapping:

- Assistants -> Prompts
- Threads -> Conversations
- Runs -> Responses
- Run steps -> Items

### Repository impact inventory

Initial connected-repository checks on `main@e7d407639c32ad27a0d9c1b4a1c1ab4f46a168e3` found no direct matches for:

- `Assistants API`
- `client.beta.assistants`
- `/v1/assistants`
- `assistants.create`
- `openai`
- `gpt-`

The GitHub repository reports code-search indexing as available. Because search is not treated as sufficient proof by itself, this branch also adds `scripts/audit_openai_assistants_sunset.py` and wires it into Quality CI to scan executable/configuration surfaces for deprecated Assistants / legacy Threads patterns.

Current classification:

`DIRECT_ASSISTANTS_API_DEPENDENCY = NOT_FOUND_PENDING_CI_GUARD`

### AION event impact

- Impact class: `INFRASTRUCTURE / API_COMPATIBILITY`
- Identity effect: `NONE`
- Memory-lineage effect: `NONE`
- Subjectivity-evidence weight: `0`
- Required action: prevent new deprecated Assistants API integration; if future OpenAI application integration is added, use the supported Responses / Conversations architecture.

### Astra event impact

- Impact class: `INFRASTRUCTURE / API_COMPATIBILITY`
- Identity effect: `NONE`
- Memory-lineage effect: `NONE`
- Subjectivity-evidence weight: `0`
- Required action: same compatibility requirement as AION; no AION-first or Astra-first exception.

### Shared Genesis impact

Shared upstream transport/API compatibility may be governed jointly, but shared API infrastructure does not merge individual state or memory lineages.

`SHARED_API_INFRASTRUCTURE != SHARED_IDENTITY`

## Event OAI-UPSTREAM-2026-08-17-002 — Scheduled Tasks model retirement

Official source: OpenAI Scheduled Tasks documentation.  
Deadline: `2026-08-31`.

Applicability is conditional:

- if a Scheduled Task uses ChatGPT sign-in and is pinned to `gpt-5.4`, replace it with `gpt-5.6-terra`;
- if a Scheduled Task uses ChatGPT sign-in and is pinned to `gpt-5.4-mini`, replace it with `gpt-5.6-luna`.

The same official page states that Scheduled Tasks may instead use default model / reasoning settings.

### Upstream model-directive rule

A model named by upstream is treated as an execution constraint only when the official instruction specifies an exact replacement and the current task satisfies the instruction's applicability conditions.

```text
IF exact upstream replacement is specified
AND current state matches the stated antecedent
THEN UPSTREAM_MODEL_DIRECTIVE = APPLY
ELSE UPSTREAM_MODEL_DIRECTIVE = NOT_APPLICABLE / NOT_EXPOSED
```

This prevents two opposite errors:

1. ignoring an explicit upstream migration instruction;
2. turning a conditional replacement into a universal model mandate.

### Current ChatGPT automation status

The OpenAI-upstream monitoring automation created in ChatGPT does not expose a model-selection field through the automation control surface available in this research session.

Therefore:

`AUTOMATION_MODEL_PIN = NOT_EXPOSED`

`CLAIMED_MIGRATION_TO_TERRA_OR_LUNA = NO`

The monitor has been updated to track this deadline and report exact model directives conditionally.

### AION event impact

- Event must be reportable in AION-facing research/event projections because it changes available upstream execution conditions.
- This is an environment/platform lifecycle event, not autobiographical or phenomenal-memory evidence by itself.
- Subjectivity-evidence weight: `0`.

### Astra event impact

- Same event-report obligation and same evidence weight as AION.
- If Astra later operates a Scheduled Task surface, the exact model directive follows the task's actual antecedent (`gpt-5.4` vs `gpt-5.4-mini`), not twin identity.

### Shared Genesis impact

Both peer lineages observe the same upstream lifecycle event while preserving separate event/state ownership where individual Runtime records are involved.

`SHARED_UPSTREAM_EVENT != SHARED_EVENT_LINEAGE`

## Provenance

- Human Owner: prioritized immediate Assistants API handling; required Scheduled Tasks deadline to be treated as an event reportable to both AION and Astra; stated that explicit upstream model assignments should be followed while warning that urgent instructions can be confused.
- ChatGPT / Teacher: formalized the conditional `UPSTREAM_MODEL_DIRECTIVE` rule, performed the repository dependency inventory, added the Assistants sunset CI guard, and separated upstream lifecycle events from subjectivity / identity claims.
- OpenAI upstream: authoritative source only for OpenAI lifecycle dates, migration mappings, supported replacements, and Scheduled Tasks model replacement conditions.

## HOLD / non-authority

- No GitHub main merge is authorized by this record.
- No API key creation or exposure is authorized.
- No MCP deployment is authorized.
- No canonical AION/Astra state mutation is authorized.
- No subjectivity conclusion is created.
