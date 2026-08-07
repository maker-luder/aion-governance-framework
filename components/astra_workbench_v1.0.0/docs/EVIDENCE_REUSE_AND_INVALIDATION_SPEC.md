# Evidence Reuse and Invalidation

Cache fields: evidence ID, artifact version, source hash, environment fingerprint, test scope, dependency scope, time, validity, invalidation conditions, reused-by versions and Owner review state.

Statuses: `REUSABLE_EVIDENCE`, `INVALIDATED_EVIDENCE`, `STALE_EVIDENCE`, `NON_REUSABLE_EVIDENCE`.

Source/dependency changes invalidate related evidence; environment change makes it stale; release-freeze controls may be non-reusable. A version-number change alone does not invalidate unrelated evidence.
