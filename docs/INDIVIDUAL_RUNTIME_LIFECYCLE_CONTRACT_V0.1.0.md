# Individual Runtime Lifecycle Contract v0.1.0

## Status and scope

This is a candidate **language-neutral** contract for the lifecycle semantics implemented by the individual runtime state layer. It preserves the existing state vocabulary and does not introduce `STARTING`, `STOPPING`, `RECOVERING`, or `FAILED` as new persisted states. It has `CANONICAL_EFFECT = NONE`, does not authorize deployment, and does not establish subjectivity, consciousness, phenomenal continuity, or personhood.

The machine-readable request definition is [`schemas/individual_runtime_lifecycle_transition_request_v0.1.0.schema.json`](../schemas/individual_runtime_lifecycle_transition_request_v0.1.0.schema.json). The previous transition-observation artifact is retained only as historical evidence of the initial foundation slice; it is not the caller request contract.

## Request versus derived facts

A caller may request only an admitted lifecycle event and must explicitly carry `canonical_effect = NONE`. The caller may not supply or claim the persisted `from_state`, the resulting `to_state`, atomicity, runtime identity authority, or Owner approval.

| Layer | Fields or responsibility | Authority |
|---|---|---|
| Request | `event_type`, `canonical_effect` | Caller input, strictly parsed and fail-closed |
| Derived state | `from_state`, `to_state` | Persisted event history and state machine |
| Implementation invariant | atomic state read + validation + append; no partial mutation | Runtime/state-layer behavior and tests |

## Current state-machine semantics

| Derived current state | Requested event | Derived resulting state | Result |
|---|---|---|---|
| `INITIALIZED` | `runtime.started` | `RUNNING` | Allowed |
| `STOPPED` | `runtime.started` | `RUNNING` | Allowed |
| `RUNNING` | `runtime.started` | — | Rejected as duplicate start |
| `RUNNING` | `runtime.stopped` | `STOPPED` | Allowed |
| `INITIALIZED` | `runtime.stopped` | — | Rejected |
| `STOPPED` | `runtime.stopped` | — | Rejected |

The contract does not authorize callers to append arbitrary lifecycle event types. Other non-lifecycle events may remain part of the broader event history, but they do not expand this lifecycle state machine.

## Generic atomicity guarantee

For every accepted request, persisted lifecycle state read, transition validation, and event append must behave as **one atomic state transition**. Two conflicting concurrent transitions must not both commit. A failed transition must leave no partial lifecycle mutation, and the existing event-lineage verification must remain valid.

The contract intentionally does not prescribe SQLite, PostgreSQL, a transactional event log, a lock mode, a connection strategy, or a programming language. The current Python/SQLite mechanism is documented separately in [`docs/INDIVIDUAL_RUNTIME_LIFECYCLE_PYTHON_SQLITE_IMPLEMENTATION_NOTE_V0.1.0.md`](INDIVIDUAL_RUNTIME_LIFECYCLE_PYTHON_SQLITE_IMPLEMENTATION_NOTE_V0.1.0.md).

## Representation and compatibility

The request representation contains exactly `event_type` and `canonical_effect`. `event_type` is one of `runtime.started` or `runtime.stopped`; `canonical_effect` must be `NONE`; unknown fields and type coercion are rejected. `from_state` and `to_state` belong in the returned derived outcome or conformance expectation, not in the request.

The existing Python method `transition_lifecycle(event_type, payload)` remains as a compatibility adapter. New language implementations should target the strict request shape and derive state from their own persisted lineage. Version `0.1.0` does not authorize silent state expansion or semantic reinterpretation.

## Non-authority boundary

Lifecycle state and event continuity are engineering evidence about persisted runtime behavior only. They are not evidence of subjective continuity, consciousness, phenomenal experience, canonical truth, deployment approval, or independent validation.
