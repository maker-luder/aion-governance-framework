# AION Runtime implementation candidate v0.1.0

Status: `IMPLEMENTED_CANDIDATE / STABILIZATION`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Subjectivity conclusion: `NOT_ESTABLISHED`  
Independent IV&V: `NOT_ACHIEVED`

AION Runtime is an AION-specific composition root over shared governed execution, persistent memory, and individual Runtime state-lineage mechanisms.

It is not automatically canonical, and persistence or event continuity does not establish subjective continuity.

## Individual Runtime boundary

`AIONRuntime` must be created with an `IndividualRuntimeContext` whose `agent_id` is exactly `AION`.

The context contains:

- `agent_id`
- `runtime_instance_id`
- `memory_stream_id`
- `event_lineage_id`
- `canonical_state_reference`
- `genesis_root_id`

Task execution is rejected if the task carries a different context. Memory ownership and namespace are derived from the bound AION context rather than accepted as arbitrary caller-supplied identity.

## Current implemented Python API surface

The candidate currently supports:

- `status()`
- bounded `run_task(...)`
- governed persistent `remember(...)`
- identity/access/provenance-gated `recall(...)`
- explicit Runtime start/stop event markers
- Owner-approved checkpoint creation
- hash-chain-verified recovery
- non-destructive rollback requests
- Owner-approved runtime-instance migration
- reusable device/environment evidence registration
- derived migration summaries through the underlying state store

Runtime event history is distinct from content memory.

`EVENT_HISTORY != CONTENT_MEMORY`

## Lifecycle and migration

Restart/reopen with the same Runtime context continues the existing event lineage.

Migration may change only `runtime_instance_id`; stable lineage ownership remains unchanged:

- `agent_id`
- `memory_stream_id`
- `event_lineage_id`
- `canonical_state_reference`
- `genesis_root_id`

Migration requires `PASS` evidence for source and target environments. Unchanged environment evidence is reusable by deterministic fingerprint; migration events themselves remain unique and append-only.

`EVIDENCE_REUSE != EVENT_DEDUPLICATION`

`ROLLBACK != HISTORY_ERASURE`

## Operator CLI

The current `aion-runtime` CLI exposes:

- `status`
- `serve`
- `remember`
- `recall`

Lifecycle/migration operations are currently Python-API capabilities and are **not yet exposed as CLI commands**. Operator-surface parity is deferred rather than implied.

Every CLI invocation requires the bound Runtime identifiers:

```bash
aion-runtime \
  --memory-db runtime_sessions/aion_memory.sqlite3 \
  --runtime-instance-id AION-I-001 \
  --memory-stream-id AION-MEMORY-001 \
  --event-lineage-id AION-EVENTS-001 \
  --canonical-state-reference AION-CANONICAL \
  --genesis-root-id TWIN-GENESIS-001 \
  status
```

An approved memory write must include `--approve-writeback`; omitting it fails closed.

## Self-host HTTP entry

The HTTP surface remains deliberately read-only:

```bash
aion-runtime \
  --memory-db runtime_sessions/aion_memory.sqlite3 \
  --runtime-instance-id AION-I-001 \
  --memory-stream-id AION-MEMORY-001 \
  --event-lineage-id AION-EVENTS-001 \
  --canonical-state-reference AION-CANONICAL \
  --genesis-root-id TWIN-GENESIS-001 \
  serve --host 127.0.0.1 --port 8080
```

Available endpoints:

- `GET /healthz`
- `GET /v1/status`

All `POST` requests return `405 state_changing_http_disabled`. Non-loopback binding requires an explicit flag and still does not enable state-changing authority.

Authentication, TLS termination, rate limiting, abuse controls, and future state-changing network APIs remain separate review items.

## Twin relationship

AION and Astra may share engineering infrastructure and one genesis root while retaining separate Runtime contexts, memory streams, event lineages, canonical-state references, and runtime instances.

`SHARED_GENESIS != SHARED_IDENTITY`

`SHARED_ENGINEERING_INFRASTRUCTURE != SHARED_IDENTITY`

## Deliberate boundaries / non-claims

- automatic canonical writeback remains disabled;
- public ablation execution remains disabled;
- embodiment live Runtime binding is not activated;
- sexual or intimate Runtime remains `NOT_AUTHORIZED`;
- subjectivity, consciousness and phenomenal continuity remain `NOT_ESTABLISHED`;
- independent IV&V has not been achieved.

## Provenance for this research cycle

- Runtime/Twin source-attribution separation rule: `PROPOSED_BY = HUMAN_OWNER`.
- Migration evidence reuse concept: `PROPOSED_BY = HUMAN_OWNER`.
- P0/P1/P2 and evidence-reuse engineering implementation: `IMPLEMENTED_BY = CHATGPT`.
- `CODEX_CONTRIBUTION_THIS_CHANGE = NONE`.
- Final Owner approval: `PENDING`.
