# AION/Astra Whole-System Governed Runtime — v2 Architecture

## Scope

The v2 candidate is a local, in-process integration target built on the formal research branch lineage. It composes the authoritative v2 memory store with a selectively replayed whole-system control flow. It is not a deployed runtime, a canonical state writer, a network MCP service, a trained foundation model, or evidence that subjectivity or identity has been established.

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
```

## Control flow

```text
Request
  -> Input validation
  -> Identity and namespace binding
  -> Trusted provenance lookup
  -> RecallRequest
  -> Upstream recall gate
  -> Namespace/access/provenance/state filtering
  -> Bounded authorized MemoryContext payload
  -> Trusted approval lookup for each tool
  -> Killable tool process with global deadline
  -> Killable Language Core process with global deadline
  -> Response build
  -> Trusted writeback authorization
  -> Durable write-ahead intent
  -> Separate memory store write
  -> Append-only audit event
  -> State checkpoint
  -> Intent commit or PENDING_RECONCILIATION
  -> Output
```

## Semantic memory

The upstream memory store returns full `StoredMemory` records. The whole-system layer maps eligible records into a bounded `MemoryContext` with the memory identifier, safe content representation, namespace, derived candidate authority, confidence, revision, timestamp, provenance source, verification status and active/supersession status. The adapter receives this structured payload, not only IDs.

Records from a different namespace, missing requester scope, unverified provenance, tombstoned records, superseded records and conflict-flagged records are excluded. Negative tests use a sentinel secret and inspect adapter input to show that namespace isolation is semantic rather than ID-only.

## Authorization and provenance

Request booleans are claims only. A tool call requires an independently registered `TrustedApprovalRecord` whose requester, approver, authority, exact tool, namespace, scopes, issuance/expiry and revocation state all match. The requester cannot become the approver by setting request fields.

A source requires an independently registered `TrustedProvenanceRecord` whose source ID, kind, locator, digest, branch and validity match. If evidence cannot be resolved, the status remains unverified and generation/writeback is denied.

## Bounded execution and cancellation

Generation and tool execution run in child processes. The parent observes the global deadline and cancellation token while the child is in flight. On timeout or cancellation, the child is terminated, a structured result and audit event are produced, and no later writeback mutation is permitted by the runtime path. This is a hard boundary for the local process model; it is not a claim that arbitrary remote provider infrastructure can be cancelled after a network request has escaped the process.

## Durability and recovery

Memory and whole-system state remain separate SQLite stores. Cross-store atomicity is not claimed. A write-ahead intent is persisted before memory write. The intent is committed only after audit and checkpoint persistence succeeds. If persistence fails, the result is not `COMPLETED`; it is `PENDING_RECONCILIATION` when a writeback intent exists. Restart recovery compares the stored memory content digest against the pending intent and marks it deterministically reconciled or aborted.

## Evidence and lineage

The old orphan review branch is preserved as historical evidence. Only the whole-system engineering surface and its runner were selectively replayed. Current research modules remain from formal research authority. The replay ledger records source branch, source SHA, transformation, target SHA and authority status.
