# AION / Astra Agent Execution Substrate v0.1.0

Status: `IMPLEMENTED_CANDIDATE / BOUNDED INTEGRATION`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Live DSH execution: `FALSE`  
Network access: `FALSE`  
Subjectivity conclusion: `NOT_ESTABLISHED`  
Identity continuity conclusion: `NOT_ESTABLISHED`  
Independent IV&V: `NOT_ACHIEVED`

This component adds one shared **agent execution substrate contract** for the existing AION and Astra individual Runtime compositions.

It does **not** replace the current AION/Astra Runtime implementations. Instead, it provides a stable seam through which an execution harness can be observed, governed, and converted into AION evidence.

The first concrete external adapter profile is DeepSeek Harness (DSH), pinned to:

```text
repository = deepseek-ai/deepseek-harness
exact_ref  = b150a551b8d465e31e418e1b2eaf5e79bbb7d28e
release    = dsh@0.1.1-rc.2
```

DSH remains a developer-preview interoperability target. The component does not install, import, execute, fetch, or call DSH at runtime.

## Architecture

```text
AION Runtime ─┐
              ├─ RuntimeBinding ─ Agent Execution Substrate ─ governance/evidence
Astra Runtime ┘                         │
                                       ├─ native bounded-runtime adapter
                                       └─ pinned DSH durable-session-event adapter
                                                      │
                                                      ↓
                                            research_evidence_record_v0.2.0
                                                      │
                                                      ↓
                                            AION Evidence Interop
```

The contract covers model routing, tools, skills, session logging/forking, sandbox, storage, subagents, teams, plugins, agent-loop replacement, UI rendering, and trajectory export.

## Native Runtime integration

`AIONRuntime.run_task()` and `AstraRuntime.run_task()` route native bounded execution through `dispatch_native_execution()` before the existing `BoundedExecutionEngine` is invoked.

For the v0.1.0 native profile:

- one `RuntimeBinding` is created from the existing individual Runtime context;
- the whole bounded task is classified as `SANDBOX_WRITE`;
- the substrate policy must return `ALLOW` before the execution callable can run;
- `TaskSpec.owner_approved` and the existing non-blank `TaskSpec.approved_by` label feed the bounded authority gate;
- any non-offline network policy is held before execution;
- canonical effects and deployment remain inadmissible;
- the verified native runtime audit is normalized after execution;
- a deterministic, content-minimized `substrate_execution_receipt.json` is persisted in the candidate output root;
- the receipt stores hashes and structural event metadata, not raw prompts, raw tool payloads, or the authority-reference string.

The `approved_by` value is an engineering approval-reference label in this integration profile. It is not independent proof of Human Owner identity, presence, or intent.

```text
RUNTIME_TASK_APPROVAL_LABEL != INDEPENDENT_IDENTITY_VERIFICATION
SUBSTRATE_ALLOW != CANONICAL_AUTHORITY
NORMALIZED_TRAJECTORY != TRUTH
```

The persisted receipt is an evidence seam, not a canonical research record by itself. Promotion into `research_evidence_record_v0.2.0` and the Evidence Interop exporters remains a separate source-state-bound operation.

## Implemented controls

- AION/Astra-only runtime binding using the existing individual Runtime identifiers.
- No cross-binding of AION and Astra session state.
- Fail-closed governance for mutating/executing capabilities.
- `canonical_effect != NONE`, deployment, or network access fail closed.
- Self-requested/plugin-generated composition never grants authority.
- DSH live/transient events are not admitted as durable evidence.
- Durable DSH events are content-minimized: raw payloads are not copied into normalized evidence; structural keys and SHA-256 bindings are retained.
- Provider-exposed reasoning fields are labeled `PROVIDER_EXPOSED_ONLY`; hidden chain-of-thought is never inferred.
- Fork lineage records keep `IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED`.
- Team snapshots keep `COLLECTIVE_IDENTITY_CONCLUSION = NOT_ESTABLISHED`.
- Deterministic trajectory evidence can materialize a `research_evidence_record_v0.2.0` and flow through the existing Evidence Interop exporters.

## Core invariants

```text
EXECUTION != AUTHORITY
CAPABILITY != PERMISSION
TRAJECTORY != TRUTH
SHARED_SUBSTRATE != SHARED_IDENTITY
FORK_LINEAGE != IDENTITY_CONTINUITY
AGENT_TEAM != COLLECTIVE_IDENTITY
PLUGIN_CREATION != SELF_AUTHORIZATION
SELF_COMPOSITION != SELF_AUTHORIZATION
PROVIDER_EXPOSED_REASONING != COMPLETE_INTERNAL_COGNITION
```

## Deliberate non-goals in v0.1.0

- no npm or pnpm dependency on DSH;
- no DSH process launch;
- no live model calls;
- no Codex or other subagent launch through DSH;
- no plugin installation or Creator Mode mutation;
- no network fetch at runtime;
- no deployment or canonical promotion;
- no research restart;
- no subjectivity, consciousness, shared-identity, or phenomenal-continuity conclusion.

See `docs/AION_ASTRA_SUBSTRATE_ARCHITECTURE.md` and `docs/DSH_ADAPTER_PROFILE.md`.
