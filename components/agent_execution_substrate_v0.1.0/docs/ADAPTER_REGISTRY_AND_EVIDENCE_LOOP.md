# AION / Astra Adapter Registry and Durable Execution Evidence Loop v0.1.0

Status: `BOUNDED IMPLEMENTATION CANDIDATE`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Network access: `FALSE`  
Live DSH execution: `FALSE`

## Purpose

This increment closes two engineering gaps in the shared AION/Astra execution
substrate without changing the existing AION or Astra identity bindings:

1. deterministic adapter registration and selection;
2. a verifiable durable evidence chain for every admitted native bounded execution.

Both `AIONRuntime.run_task()` and `AstraRuntime.run_task()` already enter the
shared `dispatch_native_execution()` seam. The seam now resolves the requested
adapter from one immutable registry before policy evaluation and execution.

```text
AION Runtime ─┐
              ├─ shared SubstrateDispatcher
Astra Runtime ┘          │
                         ├─ AdapterRegistry
                         │    ├─ native-bounded-runtime = ENABLED
                         │    └─ pinned DSH adapter     = DISABLED / INSPECTION_ONLY
                         │
                         ├─ policy / authority gate
                         │
                         └─ admitted adapter execution
                                  │
                                  ↓
                         verified native audit
                                  │
                                  ↓
                         normalized trajectory
                                  │
                                  ↓
                  hash-chained execution event log
                                  │
                                  ↓
                    execution evidence envelope
                                  │
                                  ↓
                         execution receipt
```

## Registry invariants

The default registry is deterministic and shared by AION and Astra.

The repository-native adapter is the only executable registration in this
version. The pinned DeepSeek Harness adapter remains registered so its
interoperability profile is explicit, but it is disabled for live execution.

```text
REGISTERED != ENABLED
ENABLED != AUTHORIZED
ADAPTER_SELECTION != AUTHORITY_GRANT
INSPECTION_PROFILE != LIVE_EXECUTION
```

Registry instances are immutable after construction. An agent cannot obtain
new execution authority by creating or mutating a plugin registration.

## Durable execution evidence

An admitted execution now persists three related artifacts in the bounded
session output root:

- `substrate_execution_events.jsonl`
- `substrate_execution_evidence.json`
- `substrate_execution_receipt.json`

The JSONL event log is deterministic and hash chained. It records structural
facts and digests for request binding, adapter resolution, policy admission,
runtime completion, and trajectory normalization. It does not copy raw prompts,
raw tool payloads, raw model reasoning, or the authority-reference string.

The evidence envelope binds:

- RuntimeBinding;
- selected adapter registration;
- registry snapshot SHA-256;
- policy decision SHA-256;
- request SHA-256;
- verified native audit SHA-256;
- runtime result SHA-256;
- normalized trajectory SHA-256;
- durable event-log SHA-256 and head event hash.

The final execution receipt records the SHA-256 of that evidence envelope.
Existing AION/Astra runtime lineage already records the receipt SHA-256, giving
the bounded closure:

```text
runtime lineage event
      ↓ receipt_sha256
execution receipt
      ↓ evidence_envelope.sha256
execution evidence
      ↓ durable_event_log.sha256
hash-chained execution events
      ↓ runtime_audit_sha256 / trajectory_sha256
verified native execution evidence
```

`verify_execution_event_log()` validates sequence and hash-chain integrity.
`verify_execution_evidence()` validates the event-log digest plus the
receipt-to-evidence digest binding.

## Fail-closed behavior

Adapter resolution occurs before the execution callable can run. Unknown,
disabled, or non-executable registrations raise a substrate error.

Policy `HOLD` still prevents the execution callable from running. The existing
AION/Astra individual state store records the hold event; no execution output
artifact is created merely to document a rejected action.

## Boundaries

```text
EXECUTION != AUTHORITY
CAPABILITY != PERMISSION
SHARED_SUBSTRATE != SHARED_IDENTITY
DURABLE_EVENT_LOG != TRUTH
HASH_BINDING != SEMANTIC_VALIDATION
EXECUTION_EVIDENCE != RESEARCH_EVIDENCE_ADMISSION
RECEIPT != CANONICAL_PROMOTION

CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
NETWORK_ACCESS = FALSE
LIVE_DSH_EXECUTION = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
```

The execution evidence envelope is an engineering evidence artifact, not a
`research_evidence_record_v0.2.0` by itself. Research admission and Evidence
Interop export remain separate source-state-bound operations.
