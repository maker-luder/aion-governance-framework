# AION Runtime implementation candidate v0.1.0

This component begins the post-RC implementation of a standard AION Runtime by composing two already-public project lines:

- bounded, Owner-governed task execution from `components/executable_runtime_v0.1.0`;
- topic-cued recall governance plus a persistent SQLite store from `components/memory_recall_governance_v0.1.0`.

## Current implemented surface

- `AIONRuntime.status()` exposes machine-readable capability state.
- `AIONRuntime.run_task(...)` delegates to the existing bounded execution engine.
- `AIONRuntime.remember(...)` persists a cross-session record only when writeback is explicitly approved.
- `AIONRuntime.recall(...)` applies identity, access-scope, provenance, conflict and relevance gates before returning memory.
- `aion-runtime` provides operator CLI commands for status, memory write, recall, and a self-host HTTP entry.

## Deliberate boundaries

- This branch implements a **runtime candidate**. It is not automatically promoted to canonical status.
- Persistent memory is not canonical truth. `canonical_effect` remains `NONE`.
- Relationship, familiarity or trust cannot grant access or write authority.
- Public ablation execution remains disabled.
- Sexual-function and intimate-interaction runtime remains `NOT_AUTHORIZED`.
- 3D embodiment assets are outside this component.
- Subjectivity, consciousness and identity continuity remain `NOT_ESTABLISHED`.
- Independent IV&V has not yet occurred.

## Minimal local use

After installing the local component dependencies in a governed Python 3.11+ environment:

```bash
aion-runtime --memory-db runtime_sessions/aion_memory.sqlite3 status
```

An approved memory write must include `--approve-writeback`; omitting it is a hard failure. Recall also requires the matching identity and access scopes.

## Self-host deployment entry

The initial HTTP surface is deliberately read-only:

```bash
aion-runtime --memory-db runtime_sessions/aion_memory.sqlite3 serve --host 127.0.0.1 --port 8080
```

Available endpoints:

- `GET /healthz`
- `GET /v1/status`

All `POST` requests return `405 state_changing_http_disabled` in v0.1.0. Binding to a non-loopback interface requires the explicit `--allow-non-loopback` flag, but doing so **does not** enable state-changing execution.

This allows self-host deployment and health/status inspection without turning public network access into execution authority. Authentication, rate limiting, abuse controls, TLS termination, and any future state-changing network API remain separate review items.
