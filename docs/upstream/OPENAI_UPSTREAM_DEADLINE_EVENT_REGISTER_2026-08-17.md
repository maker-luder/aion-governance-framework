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

The GitHub repository reports code-search indexing as available. Because search is not treated as sufficient proof by itself, this branch adds `scripts/audit_openai_assistants_sunset.py` and wires it into Quality CI to scan executable/configuration surfaces for deprecated Assistants / legacy Threads patterns.

The exact PR head before this reconciliation (`17134197033682913fc92c9b8be6d7f6d85c5d13`) completed:

- `Quality = SUCCESS`
- `CodeQL Security Scan = SUCCESS`
- `Main Transition Authority Gate = EXPECTED HOLD / FAIL-CLOSED`

Current classification:

`DIRECT_ASSISTANTS_API_DEPENDENCY = NOT_FOUND`

`ASSISTANTS_API_REGRESSION_GUARD = IMPLEMENTED_CANDIDATE`

This means no migration workload was found in the current repository state, while future executable/configuration reintroduction of deprecated Assistants / legacy Threads integration is intended to fail CI.

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

## Event OAI-UPSTREAM-2026-08-17-002 — Codex model retirement / Scheduled Tasks applicability

Official source: OpenAI ChatGPT & Codex changelog.  
Deadline: `2026-08-31`.

OpenAI states that on 2026-08-31, `gpt-5.4` and `gpt-5.4-mini` will no longer be available in Codex for users signed in with ChatGPT. The models remain available through the OpenAI API and Codex sessions authenticated with an API key.

Official recommended replacements for the affected ChatGPT-sign-in Codex condition:

- `gpt-5.4` -> `gpt-5.6-terra`
- `gpt-5.4-mini` -> `gpt-5.6-luna`

Scheduled Tasks are included in the project impact inventory because unattended/scheduled Codex work may inherit or pin an affected model configuration. Applicability must be checked against the actual task/session configuration rather than inferred from twin identity.

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

The monitor is configured to track this deadline and report exact model directives conditionally.

### AION event impact

- Event must be reportable in AION-facing research/event projections because it changes available upstream execution conditions.
- This is an environment/platform lifecycle event, not autobiographical or phenomenal-memory evidence by itself.
- Subjectivity-evidence weight: `0`.

### Astra event impact

- Same event-report obligation and same evidence weight as AION.
- If Astra later operates an affected Codex / Scheduled Task surface, the exact replacement follows the actual previous model (`gpt-5.4` vs `gpt-5.4-mini`), not twin identity.

### Shared Genesis impact

Both peer lineages may observe the same upstream lifecycle event while preserving separate event/state ownership where individual Runtime records are involved.

`SHARED_UPSTREAM_EVENT != SHARED_EVENT_LINEAGE`

## Provenance

- Human Owner: prioritized immediate Assistants API handling; required the 2026-08-31 model deadline to be treated as an event reportable to both AION and Astra; stated that explicit upstream model assignments should be followed while warning that urgent instructions can be confused.
- ChatGPT / Teacher: formalized the conditional `UPSTREAM_MODEL_DIRECTIVE` rule, performed the repository dependency inventory, added the Assistants sunset CI guard, reconciled exact-head CI evidence, and separated upstream lifecycle events from subjectivity / identity claims.
- OpenAI upstream: authoritative source only for OpenAI lifecycle dates, migration mappings, supported replacements, and Codex model replacement conditions.

## HOLD / non-authority

- No GitHub main merge is authorized by this record.
- No API key creation or exposure is authorized.
- No MCP deployment is authorized.
- No canonical AION/Astra state mutation is authorized.
- No subjectivity conclusion is created.
