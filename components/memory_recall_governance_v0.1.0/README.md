# Topic-Cued Cross-Session Recall Governance v0.1.0

The human Owner proposed that new conversations remain lightweight and that relevant past events be selectively recalled only when current people, events, topics or decisions provide a cue. ChatGPT assisted in naming and formalizing the concept as TCCR and a Memory Recall Gate.

The original public RC component used synthetic records only. The post-RC implementation branch now adds `SQLiteMemoryStore`, a local persistent cross-session store that retains the existing identity, access-scope, provenance, conflict and relevance gates.

Persistent storage does **not** make a record canonical truth. Writes require explicit `writeback_approved=True`; every stored record keeps `canonical_effect="NONE"`; unverified, conflicted, tombstoned, superseded, identity-mismatched or scope-inaccessible records are not recalled.

No private production memory database is included in the repository.

## Opt-in cross-cycle claim revision

`ClaimRevisionService` adds bounded claim versions, premise dependencies, typed
evidence and explicit review history in the same `SQLiteMemoryStore` database.
Challenges atomically quarantine affected downstream memory; retain/revise creates
an immutable successor and never silently releases dependent claims. All mutations
require explicit local writeback approval. Enrolled memory must use this revision
protocol instead of the legacy direct flag setters. Unenrolled memory is unchanged.

See [the dated design, API boundaries, contrast and source notes](../../docs/research/CLAIM_REVISION_2026_09_03.md).
`RECORDED` is recall eligibility, not truth. Semantic contradiction detection,
automatic review and artificial subjectivity remain unestablished/not implemented
as specified in that document. No private database migration runs automatically.

See the [bounded hardening addendum](../../docs/research/CLAIM_REVISION_HARDENING_2026_09_03.md)
for version-bound DAG semantics, atomicity, declared source lineage, new-event
canonicalization, resource caps, disposable migration tests and downgrade limits.
