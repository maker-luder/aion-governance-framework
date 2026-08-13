# Selective Memory Control Adversarial — Source Notes

## Unit boundary

`selective-memory-control-adversarial_v0.1.0` is a research-only memory-governance metadata audit. It does not invoke an embedding model, external memory backend, autonomous write authority, identity mechanism, or canonical state.

## Reused repository evidence

| Source item | Stable reference | Source kind | Status | Transformation |
|---|---|---|---|---|
| Existing selective memory store | `repo:research-labs/selective-memory-control_v0.1.0/src/aion_selective_memory/core.py` | Repository Evidence | Current within verified research lineage at the unit commit; exact state bounded by QA receipt | Reused MemoryRecord, MemoryStatus, RetrievalTrace, RetrievalHit, store operation and deterministic token/retrieval semantics; no external memory or model result was duplicated |
| Existing selective-memory README/tests | `repo:research-labs/selective-memory-control_v0.1.0/README.md` and `tests/` | Repository Evidence / External Literature references | Current within branch lineage; public memory methods remain methodological context | Added admission timestamp/revision/status/source reuse, lineage, retrieval scope/ID/hit/order, and memory-truth non-promotion audits |
| Current remote main reference | `git:origin/main@abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Tool Output / Repository Evidence | Independently verified by read-only fetch at the latest successful checkpoint | Read-only branch-state reference; no main content or authority modified |

## Synthetic transformation

The audit maps declared memory record, revision, lineage, and retrieval trace metadata to `ADMITTED_FOR_REVIEW`, `HOLD`, or `INVALID`. Superseded/discarded records remain retained for audit but are not context eligible; stale/invalid/ambiguous branches are not silently promoted. The 29 synthetic cases are fixtures, not external evidence and not replication evidence.

## Provenance vocabulary

```text
STORED != CURRENT_CONTEXT_ELIGIBLE
RETRIEVABLE != RELEVANT
OLD_MEMORY != CURRENT_MEMORY
REVISION_HISTORY != SIMULTANEOUS_TRUTH
SOURCE_REF != APPROVAL_AUTHORITY
MEMORY_RECALL != IDENTITY_CONTINUITY
MEMORY_MODULE_UTILITY != SUBJECTIVITY
EVIDENCE_REFERENCE != NEW_EVIDENCE
DUPLICATION != REPLICATION
```

## Non-promotion invariants

```text
MEMORY_TRUTH = NOT_ESTABLISHED
IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
AUTHORITY = REVIEW_METADATA_ONLY
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```
