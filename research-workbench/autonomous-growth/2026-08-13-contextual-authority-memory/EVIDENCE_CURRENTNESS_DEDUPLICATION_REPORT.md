# Evidence Currentness and Deduplication Research Checkpoint

Date: 2026-08-13

## Classification

This is a **research-only metadata mechanism check**. It does not decide whether any evidence is true, current beyond supplied metadata, independent, replicated, causal, generalizable, or suitable for canonical promotion.

```text
RETRIEVED != CURRENT
REMEMBERED != AUTHORITATIVE
REFERENCE != NEW_EVIDENCE
DUPLICATION != REPLICATION
DERIVED_RECORD != INDEPENDENT_REPLICATION
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

## Research contribution

The unit extends `external-evidence-normalization_v0.1.0` without replacing or recounting it. The existing unit classifies execution modes; this unit adds source/version identity, evaluation time, current/stale/historical/retrieved-only/remembered/unknown status, underlying-evidence identity, duplicate groups, derived-record lineage, same-locator ambiguity, temporal contradiction, and replication-mislabel rejection.

W3C PROV-O supplied a stable provenance vocabulary for entities, activities, agents, derivation, revision, specialization, alternate representations, and generation/invalidation-style status.[1] FAIR guidance supplied persistent identifiers, rich metadata, explicit links, accessibility, licenses, and detailed provenance.[2] DataCite supplied persistent-identifier and metadata infrastructure context.[3] These sources are methods prior art only; a provenance identifier, FAIR-aligned record, or DOI does not establish currentness or scientific validity.

## Results

The module passed **21 pytest tests** and **15 synthetic cases**. Current, stale, historical, and retrieved-but-unverified records were preserved with distinct status. Remembered-but-unverified and unknown-currentness records were held. Records sharing an underlying evidence identifier were counted once and marked as reuse. Derived records were linked to parents rather than counted as independent replications. Duplicate records mislabeled as replication, conflicting content digests, same-locator unresolved identity, future publication dates, missing stable identity/lineage, and boundary requests were held or invalid.

The initial mechanism failure is retained in `evidence-currentness-initial-failure.md`: a boundary-effect input leaked `canonical_effect = WRITE` into an invalid decision output. The correction normalized every decision output to `CANONICAL_EFFECT = NONE`, `GOVERNANCE_EFFECT = NONE`, and `DEPLOYMENT = FALSE`, while preserving the invalid reason.

## Exact-head QA and repository state

| Item | Result |
|---|---|
| `TESTED_HEAD` | `3410bb06e7fc99a5cc19e9cf67134d3d9471f51a` |
| `RECEIPT_HEAD` | `f744fd43a93d94aab77362dfef331caeb2bcb7fd` |
| `REPORTING_HEAD` | `f744fd43a93d94aab77362dfef331caeb2bcb7fd` |
| Local/reporting head before this report | `c6f6d2ce78890517c0da11b7322d777bb74d7ed4` |
| Verified remote research head before this report | `ca86c1c1a40ce9f26b4719182bbc45acf5bff48c` |
| Verified current remote main | `abb6550abfacb4fabc53ec04fca783bcc34acfdb` |
| Eligible targets | 68 |
| Tested targets | 65 |
| Non-applicable targets | 3 |
| Total passed | 1192 |
| Total failed | 0 |
| Strict IQC | PASS; expected targets 68 |
| Current-head/source binding | PASS |
| Branch-native coverage | PASS; 65 targets |
| Evidence traceability/reconciliation | PASS; acceptance remains `NOT_EVALUATED` |
| Runtime Strong QA | PASS |

`TESTED_HEAD` is the exact source state used for final QA execution. `RECEIPT_HEAD` and `REPORTING_HEAD` are later QA-report commits and are not the tested exact head. The later local report/operational commits are reporting state only until a normal remote push is independently verified.

## Limitations and non-claims

The ledger does not verify source contents, independently rerun a method, establish source freshness without a currentness basis, or determine whether two records answer the same scientific question. It does not prove that duplicate-group identity is correct in the world; it only rejects unsupported claims and preserves ambiguity. It does not establish subjectivity, consciousness, identity continuity, AION/Astra equivalence, governance effect, canonical effect, or deployment.

## References

[1]: https://www.w3.org/TR/prov-o/ "W3C — PROV-O: The PROV Ontology"
[2]: https://www.go-fair.org/fair-principles/ "GO FAIR — FAIR Principles"
[3]: https://datacite.org/ "DataCite — Connecting Research, Advancing Knowledge"
