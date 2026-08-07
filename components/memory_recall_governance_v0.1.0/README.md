# Topic-Cued Cross-Session Recall Governance v0.1.0

The human Owner proposed that new conversations remain lightweight and that relevant past events be selectively recalled only when current people, events, topics or decisions provide a cue. ChatGPT assisted in naming and formalizing the concept as TCCR and a Memory Recall Gate.

The original public RC component used synthetic records only. The post-RC implementation branch now adds `SQLiteMemoryStore`, a local persistent cross-session store that retains the existing identity, access-scope, provenance, conflict and relevance gates.

Persistent storage does **not** make a record canonical truth. Writes require explicit `writeback_approved=True`; every stored record keeps `canonical_effect="NONE"`; unverified, conflicted, tombstoned, superseded, identity-mismatched or scope-inaccessible records are not recalled.

No private production memory database is included in the repository.
