# Astra Runtime implementation candidate v0.1.0

Status: `IMPLEMENTED_CANDIDATE / STABILIZATION`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Subjectivity conclusion: `NOT_ESTABLISHED`  
Independent IV&V: `NOT_ACHIEVED`

Astra Runtime is an Astra-specific individual Runtime composition over shared bounded execution, persistent memory, and individual Runtime state-lineage mechanisms.

It is a peer composition to AION Runtime, not an internal AION subcomponent and not a shared identity.

## Individual Runtime boundary

`AstraRuntime` requires an `IndividualRuntimeContext` whose `agent_id` is exactly `ASTRA`.

The context contains:

- `agent_id`
- `runtime_instance_id`
- `memory_stream_id`
- `event_lineage_id`
- `canonical_state_reference`
- `genesis_root_id`

Task execution is rejected if the task carries a different context. Memory writes derive Astra ownership and namespace from the bound Runtime context rather than arbitrary caller-supplied identity.

## Shared mechanism, separate individual state

Astra and AION use the same shared engineering mechanisms where appropriate:

- `BoundedExecutionEngine`
- `SQLiteMemoryStore`
- `IndividualRuntimeStateStore`

Sharing these mechanisms does not create shared memory ownership, event history, canonical state, Runtime instance, or identity.

`SHARED_ENGINEERING_INFRASTRUCTURE != SHARED_IDENTITY`

## Current implemented Python API surface

The candidate supports:

- `status()`
- bounded `run_task(...)`
- governed persistent `remember(...)`
- gated `recall(...)`
- explicit Runtime start/stop event markers
- Owner-approved checkpoints
- hash-chain-verified recovery
- non-destructive rollback requests
- Owner-approved runtime-instance migration
- reusable device/environment evidence registration
- derived migration summaries through the state store

Runtime event evidence remains distinct from content memory.

`EVENT_HISTORY != CONTENT_MEMORY`

## Lifecycle and migration

Restart/reopen using the same Runtime context continues Astra's existing event lineage.

Migration may change only `runtime_instance_id` while preserving:

- `agent_id`
- `memory_stream_id`
- `event_lineage_id`
- `canonical_state_reference`
- `genesis_root_id`

Source and target environment evidence must both be `PASS`. Repeated use of an unchanged verified environment reuses the evidence artifact, while each migration event remains unique and append-only.

`EVIDENCE_REUSE != EVENT_DEDUPLICATION`

`ROLLBACK != HISTORY_ERASURE`

## Twin Genesis relationship

Twin Genesis validation can produce two distinct Runtime contexts after verifying shared genesis and separate individual identifiers.

AION and Astra may share `genesis_root_id`, but must keep separate:

- agent IDs
- runtime instance IDs
- memory streams
- event lineages
- canonical-state references

Existing embodiment governance remains unchanged: `EmbodimentInstance.runtime_binding` is not activated by this Runtime work.

`SHARED_GENESIS != SHARED_IDENTITY`

## Operator surface

Astra's lifecycle and migration capabilities are currently Python-API capabilities. A dedicated Astra operator CLI/network surface is not part of this stabilization cycle and must not be implied by the existence of the Runtime composition.

`OPERATOR_SURFACE_PARITY = DEFERRED`

## Non-claims

- no canonical promotion;
- no automatic canonical write authority;
- no subjectivity or consciousness conclusion;
- no phenomenal-continuity inference from event lineage;
- no body-ownership or embodiment-sensation claim;
- no activation of embodiment live Runtime binding;
- independent IV&V remains `NOT_ACHIEVED`.

## Provenance for this research cycle

- Runtime/Twin source-attribution separation rule: `PROPOSED_BY = HUMAN_OWNER`.
- Migration evidence reuse concept: `PROPOSED_BY = HUMAN_OWNER`.
- P0/P1/P2 and evidence-reuse engineering implementation: `IMPLEMENTED_BY = CHATGPT`.
- `CODEX_CONTRIBUTION_THIS_CHANGE = NONE`.
- Final Owner approval: `PENDING`.
