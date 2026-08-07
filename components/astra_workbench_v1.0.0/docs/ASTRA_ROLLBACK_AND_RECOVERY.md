# Rollback and Recovery

Every update/delete takes a pre-change snapshot. Writes are atomic. Failed validation cannot produce a passing package status. Interrupted changes can be restored per affected path.

Invariant: failed change → baseline unchanged → candidate restored or quarantined → audit recorded.
