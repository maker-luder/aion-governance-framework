# Individual Runtime Lifecycle — Python/SQLite Implementation Note v0.1.0

## Status

This note describes the current **reference implementation mechanism** for the language-neutral lifecycle request contract. It is not a cross-language requirement, does not authorize a storage technology, and does not establish canonical, deployment, subjectivity, or independent-validation authority.

## Reference implementation mechanism

The active Python state store uses SQLite to make the following semantic operation one transaction:

```text
BEGIN IMMEDIATE
    read persisted lifecycle history on the same connection
    validate the requested event against the derived current state
    append the event to the hash-chained lineage
COMMIT
```

A rejected request raises before an event is appended. A SQLite persistence failure is converted to a runtime-state failure and the transaction is rolled back. The existing append-only hash-chain verification remains an independent integrity check.

`BEGIN IMMEDIATE`, same-connection reads, SQLite write locks, and `COMMIT` are implementation details of this adapter. Another implementation may use a serializable database transaction, a transactional event log, or an equivalent mechanism, provided it preserves the generic atomicity guarantees:

1. persisted state read, transition validation, and event append behave as one atomic state transition;
2. conflicting concurrent transitions cannot both commit; and
3. a failed transition leaves no partial lifecycle mutation.

## Compatibility adapter

The existing `transition_lifecycle(event_type, payload)` Python method remains available as a compatibility-preserving adapter. It creates a strict request with `canonical_effect = NONE` and delegates to `transition_lifecycle_request(...)`. New cross-language callers should target the strict request contract rather than rely on Python-specific positional arguments.

## Evidence boundary

Passing concurrency, rollback, and lineage-integrity tests demonstrate behavior of this Python/SQLite candidate. They do not prove that every future implementation is atomic, do not establish distributed transaction semantics, and do not constitute independent IV&V.
