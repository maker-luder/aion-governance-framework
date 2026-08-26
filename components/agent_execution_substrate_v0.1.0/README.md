# AION / Astra Agent Execution Substrate v0.1.0

Status: `IMPLEMENTED / MERGED BOUNDED INTEGRATION`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Live DSH execution: `FALSE`  
Network access: `FALSE`  
Subjectivity conclusion: `NOT_ESTABLISHED`  
Identity continuity conclusion: `NOT_ESTABLISHED`  
Independent IV&V: `NOT_ACHIEVED`

This component provides one shared **agent execution substrate contract** for the existing AION and Astra individual Runtime compositions.

It does **not** replace the AION/Astra Runtime identities and it is not itself the scientific object of conclusion. Its role is **research instrumentation**: make bounded execution observable, governable, attributable, replay-inspectable, and convertible into evidence without treating runtime sophistication as evidence of subjectivity.

```text
AGENT_SUBSTRATE = RESEARCH_INSTRUMENTATION
SUBSTRATE_COMPLEXITY != SUBJECTIVITY_EVIDENCE
EXECUTION_EVIDENCE != RESEARCH_EVIDENCE_ADMISSION
ENGINEERING_SUCCESS != SUBJECTIVITY_PROOF
```

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
              ├─ RuntimeBinding ─ shared SubstrateDispatcher
Astra Runtime ┘                         │
                                       ├─ immutable AdapterRegistry
                                       │    ├─ native bounded runtime = ENABLED
                                       │    └─ pinned DSH profile     = DISABLED / INSPECTION_ONLY
                                       │
                                       ├─ mandatory policy / authority gate
                                       │
                                       └─ admitted native execution
                                                │
                                                ↓
                                       verified runtime audit
                                                │
                                                ↓
                                       normalized trajectory
                                                │
                                                ↓
                                   hash-chained durable event log
                                                │
                                                ↓
                                      execution evidence envelope
                                                │
                                                ↓
                                         execution receipt
                                                │
                                                ↓
                                    separate research-evidence seam
                                                │
                                                ↓
                                      AION Evidence Interop
```

The contract covers model routing, tools, skills, session logging/forking, sandbox, storage, subagents, teams, plugins, agent-loop replacement, UI rendering, and trajectory export.

## Native Runtime integration

`AIONRuntime.run_task()` and `AstraRuntime.run_task()` route native bounded execution through the shared substrate seam before the existing `BoundedExecutionEngine` is invoked.

For the v0.1.0 native profile:

- one `RuntimeBinding` is created from the existing individual Runtime context;
- the requested adapter is resolved from an immutable registry before execution;
- the repository-native bounded adapter is the only live-executable default registration;
- the pinned DSH adapter remains registered but disabled / inspection-only;
- the whole bounded task is classified as `SANDBOX_WRITE`;
- the substrate policy must return `ALLOW` before the execution callable can run;
- `TaskSpec.owner_approved` and the existing non-blank `TaskSpec.approved_by` label feed the bounded authority gate;
- any non-offline network policy is held before execution;
- canonical effects and deployment remain inadmissible;
- the verified native runtime audit is normalized after execution;
- durable execution artifacts are persisted under the bounded session output root;
- artifacts store structural facts and cryptographic bindings, not raw prompts, raw tool payloads, raw model reasoning, or the authority-reference string.

The `approved_by` value is an engineering approval-reference label in this integration profile. It is not independent proof of Human Owner identity, presence, or intent.

```text
RUNTIME_TASK_APPROVAL_LABEL != INDEPENDENT_IDENTITY_VERIFICATION
SUBSTRATE_ALLOW != CANONICAL_AUTHORITY
NORMALIZED_TRAJECTORY != TRUTH
REGISTERED != ENABLED
ENABLED != AUTHORIZED
ADAPTER_SELECTION != AUTHORITY_GRANT
INSPECTION_PROFILE != LIVE_EXECUTION
```

## Durable execution evidence

An admitted native execution persists three linked artifacts:

- `substrate_execution_events.jsonl`
- `substrate_execution_evidence.json`
- `substrate_execution_receipt.json`

The event log is deterministic and SHA-256 hash chained. It records bounded structural events for dispatch request, adapter resolution, policy admission, runtime completion, and trajectory normalization.

The evidence envelope binds the RuntimeBinding, adapter registration, registry snapshot, policy decision, request, verified runtime audit, runtime result, normalized trajectory, and durable event-log digest. The final receipt binds the evidence-envelope digest, while the AION/Astra runtime lineage records the receipt digest.

```text
runtime lineage
      ↓ receipt_sha256
execution receipt
      ↓ evidence_sha256
execution evidence
      ↓ event_log_sha256
hash-chained durable events
      ↓ audit / trajectory digests
verified native execution facts
```

`verify_execution_event_log()` validates event sequence and hash-chain integrity. `verify_execution_evidence()` validates the event-log digest and receipt-to-evidence binding. Tampering therefore fails structural verification.

```text
HASH_BINDING != SEMANTIC_VALIDATION
DURABLE_EVENT_LOG != TRUTH
EXECUTION_EVIDENCE != RESEARCH_EVIDENCE_ADMISSION
```

The execution evidence envelope remains an engineering evidence artifact, not a `research_evidence_record_v0.2.0` by itself. Research admission and Evidence Interop export remain separate source-state-bound operations.

## Implemented controls

- AION/Astra-only runtime binding using the existing individual Runtime identifiers.
- No cross-binding of AION and Astra session state.
- Shared immutable adapter registry and deterministic selection.
- Unknown, disabled, or non-executable adapters fail closed before the execution callable runs.
- Fail-closed governance for mutating/executing capabilities.
- `canonical_effect != NONE`, deployment, or network access fail closed.
- Self-requested/plugin-generated composition never grants authority.
- DSH live/transient events are not admitted as durable evidence.
- Durable DSH events are content-minimized: raw payloads are not copied into normalized evidence; structural keys and SHA-256 bindings are retained.
- Provider-exposed reasoning fields are labeled `PROVIDER_EXPOSED_ONLY`; hidden chain-of-thought is never inferred.
- Fork lineage records keep `IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED`.
- Team snapshots keep `COLLECTIVE_IDENTITY_CONCLUSION = NOT_ESTABLISHED`.
- Deterministic trajectory evidence can materialize a `research_evidence_record_v0.2.0` and flow through the existing Evidence Interop exporters only through the separate research-evidence seam.

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
SUBSTRATE_COMPLEXITY != SUBJECTIVITY_EVIDENCE
EXECUTION_EVIDENCE != RESEARCH_EVIDENCE_ADMISSION
```

## Scientific role

The central AION research question remains the **possibility of artificial subjectivity**. This component helps make future observations, interventions, mechanism claims, alternatives, and provenance more inspectable. It does not increase the strength of a subjectivity claim merely because it enables richer agent behavior or better execution evidence.

A complex agent may have memory, sessions, tools, forks, teams, plugins, subagents, planning, or self-model representations. Those capabilities can create better experimental variables; they do not by themselves establish phenomenal experience or subjectivity.

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

See `docs/AION_ASTRA_SUBSTRATE_ARCHITECTURE.md`, `docs/DSH_ADAPTER_PROFILE.md`, and `docs/ADAPTER_REGISTRY_AND_EVIDENCE_LOOP.md`.
