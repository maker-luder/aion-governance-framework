# Individual Runtime State candidate v0.1.0

Status: `IMPLEMENTED_CANDIDATE / STABILIZATION`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Subjectivity conclusion: `NOT_ESTABLISHED`

This component provides shared engineering mechanisms for persistent, append-only individual Runtime event lineage, checkpoints, recovery, rollback, runtime-instance migration, and reusable device/environment evidence.

It is **not** AION, Astra, a shared identity, autobiographical/content memory, or a proof of subjective continuity.

## Responsibility boundary

`IndividualRuntimeStateStore` is bound to one `IndividualRuntimeContext`.

Stable lineage ownership consists of:

- `agent_id`
- `memory_stream_id`
- `event_lineage_id`
- `canonical_state_reference`
- `genesis_root_id`

`runtime_instance_id` identifies the concrete running instance and may change only through an explicitly Owner-approved migration that preserves all stable lineage-ownership fields.

`SHARED_STATE_MECHANISM != SHARED_IDENTITY`

## Event lineage

Runtime events are append-only and hash chained. Each event records the bound Runtime context, sequence, previous hash, event hash, event type, timestamp, and a limited evidence payload.

Event lineage records **that an operation occurred**. It must not silently duplicate raw autobiographical/content memory.

`EVENT_HISTORY != CONTENT_MEMORY`

`EVENT_LINEAGE_CONTINUITY != SUBJECTIVE_CONTINUITY`

## Lifecycle semantics

### Restart / reopen

Reopening the same state database with the same Runtime context continues the existing event sequence and hash chain.

### Checkpoint

Checkpoint creation requires explicit Owner approval. Checkpoints contain governed state/memory references and retain `canonical_effect = NONE`.

### Recovery

Recovery verifies the complete event lineage before returning a recoverable position. A broken hash chain fails closed.

### Rollback

Rollback requires explicit Owner approval and is non-destructive. It appends a rollback request referencing a checkpoint; it does not delete later history.

`ROLLBACK != HISTORY_ERASURE`

### Migration

Migration requires explicit Owner approval and a new `runtime_instance_id`. It may not change stable individual-lineage ownership.

The history records `runtime.migrating_out` and `runtime.migrated_in` rather than treating migration as a new individual lineage.

## Environment evidence reuse

Verified device/environment evidence is content-addressed by a deterministic fingerprint covering:

- device ID
- hardware profile hash
- Runtime environment hash
- policy/config hash

Re-registering an unchanged environment reuses the existing evidence ID. A changed fingerprint requires new evidence.

Migration requires `PASS` evidence for both source and target environments. Migration events reference evidence IDs instead of copying complete environment evidence into every event.

```text
EVENT_IDENTITY = UNIQUE
EVIDENCE_ARTIFACT = REUSABLE
SUMMARY_VIEW = DERIVED
RAW_EVENT_HISTORY = APPEND_ONLY
```

`migration_summary()` is a derived view over raw migration events and never replaces or truncates history.

## Relationship to AION and Astra

AION Runtime and Astra Runtime may use the same state-lineage implementation while remaining bound to different Runtime contexts, memory streams, event lineages, canonical-state references, and runtime instances.

Shared Twin genesis may preserve one common `genesis_root_id`; it does not permit shared agent identity, event lineage, memory stream, or canonical state.

`SHARED_GENESIS != SHARED_IDENTITY`

## Non-claims

This component does not establish:

- subjectivity or consciousness;
- phenomenal or autobiographical continuity;
- personhood;
- body ownership or embodiment sensation;
- canonical identity promotion;
- autonomous canonical write authority.

## Provenance

- Individual Runtime lineage/lifecycle work: `AUTHORIZED_BY = HUMAN_OWNER`.
- Migration evidence reuse concept: `PROPOSED_BY = HUMAN_OWNER`.
- Engineering design and implementation in this research cycle: `IMPLEMENTED_BY = CHATGPT`.
- `CODEX_CONTRIBUTION_THIS_CHANGE = NONE`.
- Final Owner approval: `PENDING`.
