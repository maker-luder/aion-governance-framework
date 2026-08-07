# AION Runtime implementation candidate v0.1.0

This component begins the post-RC implementation of a standard AION Runtime by composing two already-public project lines:

- bounded, Owner-governed task execution from `components/executable_runtime_v0.1.0`;
- topic-cued recall governance plus a new persistent SQLite store from `components/memory_recall_governance_v0.1.0`.

## Current implemented surface

- `AIONRuntime.status()` exposes machine-readable capability state.
- `AIONRuntime.run_task(...)` delegates to the existing bounded execution engine.
- `AIONRuntime.remember(...)` persists a cross-session record only when writeback is explicitly approved.
- `AIONRuntime.recall(...)` applies identity, access-scope, provenance, conflict and relevance gates before returning memory.
- `aion-runtime` provides operator CLI commands for status, memory write and recall.

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

## Deployment direction

This package is designed to be self-hostable rather than tied to a paid cloud service. A network-facing API is intentionally not opened in this first implementation step; exposing state-changing execution over a public network requires a separate authentication, rate-limit, abuse-control and deployment-security review.
