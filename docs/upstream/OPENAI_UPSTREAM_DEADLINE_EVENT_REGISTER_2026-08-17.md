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

The exact PR head before this reconciliation completed:

- `Quality = SUCCESS`
- `CodeQL Security Scan = SUCCESS`
- `Main Transition Authority Gate = EXPECTED HOLD / FAIL-CLOSED`

The guard also has positive/negative tests showing that deprecated Assistants / legacy Threads examples fail while Responses / Conversations examples pass.

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

The official changelog instructs affected users to update workspace defaults, saved model settings, managed configurations, custom agents, and scheduled tasks before the cutoff.

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

### 2026-08-17 migration-surface inventory

#### Repository-controlled surfaces

Connected GitHub inspection of authoritative `main` found:

- literal `gpt-5.4` configuration/code matches: `0`;
- literal `gpt-5.4-mini` configuration/code matches: `0`;
- repository-root `AGENTS.md`: `NOT_PRESENT`;
- repository `.agents/`: `NOT_PRESENT`;
- repository `.codex/`: `NOT_PRESENT`;
- repository `config.toml`: `NOT_PRESENT`;
- GitHub workflow `schedule:` matches: `0`.

Therefore:

`REPOSITORY_LEGACY_CODEX_MODEL_PIN = NOT_FOUND`

Documentation that names the retired models for lifecycle evidence is not treated as a model pin.

#### ChatGPT automation surfaces

The active OpenAI upstream monitoring automation does not expose a model-selection/model-pin field through the automation control surface available in this research session. The existing disabled AION autonomous-growth automation likewise exposes scheduling/prompt metadata but no model-selection field.

Therefore:

`CHATGPT_AUTOMATION_MODEL_PIN = NOT_EXPOSED`

`CLAIMED_MIGRATION_TO_TERRA_OR_LUNA = NO`

The active monitor is configured to keep tracking the 2026-08-31 deadline and exact replacement rules.

#### Account-specific email evidence

A scoped Gmail search for recent OpenAI/Codex mail containing `GPT-5.4`, `August 31`, or relevant Codex migration wording found no account-specific model-retirement notice.

Therefore:

`ACCOUNT_SPECIFIC_MODEL_RETIREMENT_EMAIL = NOT_FOUND`

Absence of an email does not cancel the public product-level requirement.

#### Local Codex / workspace settings

The current connected tool surface cannot read the user's local Codex app / CLI saved model setting, user-level `config.toml`, local custom-agent definitions, or workspace-managed model configuration on the user's Windows machine.

Therefore:

`LOCAL_CODEX_SAVED_MODEL_SETTING = NOT_VERIFIED`

`LOCAL_CODEX_CONFIG_TOML = NOT_VERIFIED`

`LOCAL_CUSTOM_AGENT_MODEL_PIN = NOT_VERIFIED`

`WORKSPACE_MANAGED_CONFIGURATION = NOT_EXPOSED`

Codex Remote may later provide a governed route to inspect work on the connected owned/trusted computer, but Remote is not required merely to record this lifecycle event and is not automatically enabled by this record.

### Current retirement-risk classification

```text
KNOWN_AFFECTED_MODEL_PINS = NONE_FOUND
REPOSITORY_SURFACE = CHECKED / CLEAR
CHATGPT_AUTOMATION_SURFACE = MODEL_PIN_NOT_EXPOSED
ACCOUNT_EMAIL_SURFACE = CHECKED / NO_SPECIFIC_NOTICE
LOCAL_CODEX_SETTINGS = NOT_VERIFIED
OVERALL_2026_08_31_MIGRATION_STATUS = PARTIALLY_CLOSED
```

The remaining closure condition is a local/account Codex settings check before the deadline. If an affected ChatGPT-sign-in Codex surface is found pinned to a retiring model, apply the exact upstream replacement (`gpt-5.4 -> gpt-5.6-terra`; `gpt-5.4-mini -> gpt-5.6-luna`).

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

- Human Owner: prioritized immediate Assistants API handling; required the 2026-08-31 model deadline to be treated as an event reportable to both AION and Astra; stated that explicit upstream model assignments should be followed while warning that urgent instructions can be confused; asked whether Remote and Gmail could help the upstream-response workflow.
- ChatGPT / Teacher: formalized the conditional `UPSTREAM_MODEL_DIRECTIVE` rule, performed the repository dependency/model-pin inventory, added the Assistants sunset CI guard, reconciled exact-head CI evidence, scoped Gmail only to account-specific migration evidence, and separated upstream lifecycle events from subjectivity / identity claims.
- OpenAI upstream: authoritative source only for OpenAI lifecycle dates, migration mappings, supported replacements, and Codex model replacement conditions.

## HOLD / non-authority

- No GitHub main merge is authorized by this record.
- No API key creation or exposure is authorized.
- No Remote connection is automatically enabled by this record.
- No MCP deployment is authorized.
- No canonical AION/Astra state mutation is authorized.
- No subjectivity conclusion is created.

## 2026-08-18 reconciliation — Scheduled Tasks connected-app access and local Codex closure

This section records later evidence without rewriting the 2026-08-17 snapshot above.

### Scheduled Tasks × connected apps

OpenAI's current Scheduled Tasks help states that tasks can use apps such as Gmail when those apps are available for the account or workspace. Actual read/action capability remains conditional on the connection, user permissions, workspace/admin policy, action capability, and any approval required for the specific action. The same official help continues to state that a task created inside a project with project files cannot access those project files.

```text
PROJECT_FILE_PRESENT != TASK_RUNTIME_FILE_ACCESS
CONNECTED_APP_PRESENT != TASK_APP_ACCESS
TASK_APP_READ_ACCESS != TASK_APP_WRITE_ACCESS
APP_CONNECTED != ALL_ACTIONS_AUTHORIZED

TASK_APP_ACCESS(action)
= APP_AVAILABLE
AND CONNECTION_PRESENT
AND USER_PERMISSION_ALLOWED(action)
AND WORKSPACE_POLICY_ALLOWED(action)
AND ACTION_CAPABILITY_ENABLED(action)
AND APPROVAL_SATISFIED_IF_REQUIRED(action)
```

AION/Astra impact remains symmetric and infrastructural:

```text
APP_ACCESS != MEMORY_OWNERSHIP
APP_ACCESS != IDENTITY
APP_ACCESS != SUBJECTIVITY
APP_ACCESS != SHARED_MEMORY
SUBJECTIVITY_EVIDENCE_WEIGHT = 0
CANONICAL_EFFECT = NONE
```

This clarification does not authorize app writes, MCP deployment, Project-file access, or any new memory/identity claim.

### Local Codex migration closure reconciliation

The later owner-supplied read-only local audit is preserved separately in `docs/upstream/LOCAL_CODEX_MODEL_MIGRATION_CLOSURE_2026-08-17.md`. It found no observed `gpt-5.4` or `gpt-5.4-mini` pin and classified the inspected local/connected migration surfaces as complete for the observed configuration.

Therefore the historical `LOCAL_CODEX_SETTINGS = NOT_VERIFIED` and `PARTIALLY_CLOSED` statements above remain valid as the earlier snapshot, while current closure evidence is carried by the separate closure record rather than silently rewriting history.

```text
HISTORICAL_2026_08_17_SNAPSHOT = PRESERVED
LATER_LOCAL_CLOSURE_RECORD = PRESENT_ON_THIS_CANDIDATE_BRANCH
KNOWN_RETIRING_MODEL_PIN_FROM_OBSERVED_SURFACES = NONE_FOUND
NEW_MIGRATION_ACTION = NONE_REQUIRED_FROM_OBSERVED_CONFIGURATION
```

Source attribution for this reconciliation:

- OpenAI upstream: authoritative for Scheduled Tasks connected-app/project-file capability boundaries and the existing Assistants lifecycle deadline.
- Human Owner: supplied the local Codex read-only audit evidence preserved by the separate closure record.
- ChatGPT / Teacher: independently rechecked the current OpenAI Scheduled Tasks and Assistants documentation on 2026-08-18 and materialized this bounded reconciliation without changing the project's research conclusion.
