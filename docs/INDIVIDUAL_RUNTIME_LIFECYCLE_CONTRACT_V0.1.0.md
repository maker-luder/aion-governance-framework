# Individual Runtime Lifecycle Contract v0.1.0

## Status and scope

This is a candidate language-neutral contract for the lifecycle semantics already implemented by the individual runtime state layer. It preserves the existing state vocabulary and does not introduce `STARTING`, `STOPPING`, `RECOVERING`, or `FAILED` as new persisted states. It has `CANONICAL_EFFECT = NONE`, does not authorize deployment, and does not establish subjectivity, consciousness, phenomenal continuity, or personhood.

The machine-readable definition is [`schemas/individual_runtime_lifecycle_transition_v0.1.0.schema.json`](../schemas/individual_runtime_lifecycle_transition_v0.1.0.schema.json). The contract is intentionally narrower than a future lifecycle redesign.

## Current transition contract

| From state | Event | To state | Result |
|---|---|---|---|
| `INITIALIZED` | `runtime.started` | `RUNNING` | Allowed |
| `STOPPED` | `runtime.started` | `RUNNING` | Allowed |
| `RUNNING` | `runtime.started` | — | Rejected as duplicate start |
| `RUNNING` | `runtime.stopped` | `STOPPED` | Allowed |
| `INITIALIZED` | `runtime.stopped` | — | Rejected |
| `STOPPED` | `runtime.stopped` | — | Rejected |

The contract does not authorize callers to append arbitrary lifecycle event types. Other non-lifecycle event types may remain part of the broader event history, but they do not expand this lifecycle state machine.

## Atomicity rule

For every accepted lifecycle transition, the implementation must perform the following operations on one database connection and one write transaction:

```text
BEGIN IMMEDIATE
    read lifecycle state from the same connection
    validate the requested transition
    append the lifecycle event using the same connection
COMMIT
```

A rejected transition must not append an event. A persistence failure must roll back the transaction. The event remains subject to the existing hash-chain verification and malformed-history detection controls.

## Representation and compatibility

The interoperable transition representation contains exactly `from_state`, `event_type`, `to_state`, `atomic`, and `canonical_effect`. `atomic` must be `true`; `canonical_effect` must be `NONE`. Object member order is non-semantic, while deterministic event hashing is governed by the implementation’s explicit canonical serialization routine.

Version `0.1.0` records the current implementation semantics. A future state expansion or incompatible transition rule requires a new version and a separately reviewed conformance set. It must not be smuggled in by accepting unknown fields or silently mapping new events to existing states.

## Non-authority boundary

Lifecycle state and event continuity are engineering evidence about persisted runtime behavior only. They are not evidence of subjective continuity, consciousness, phenomenal experience, canonical truth, deployment approval, or independent validation.
