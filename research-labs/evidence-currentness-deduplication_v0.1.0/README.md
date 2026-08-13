# Evidence Currentness and Deduplication v0.1.0

Status: `RESEARCH_ONLY / METADATA_ONLY / CANONICAL_EFFECT=NONE / DEPLOYMENT=FALSE`

## Research question

Can a bounded evidence ledger distinguish **current**, **stale**, **historical**, **retrieved-but-unverified**, **remembered-but-unverified**, and **unknown** source status while also distinguishing unique underlying evidence, reused records, derived records, and genuine replication claims?

This unit addresses a cross-cutting research-integrity gap exposed by the repository's evidence-reuse requirements. It does not replace `external-evidence-normalization_v0.1.0`; that existing unit classifies static review, logical reproduction, and executed replication claims. The present unit instead audits **time/status identity and duplicate counting** before any later evidence admission.

## Prior-art transformation

W3C PROV-O provides a provenance model for entities, activities, agents, derivation, attribution, generation, invalidation, revision, specialization, alternate representations, and provenance chains. It is a W3C Recommendation and stable reference, while the W3C document notes that the technical-reports index should be consulted for later revisions.[1] The prototype borrows only the narrow ideas of identity, derivation, revision/invalidation-style status, and provenance linkage; it does not claim full PROV-O conformance.

The FAIR Principles emphasize persistent identifiers, rich and explicit metadata, accessibility of metadata, qualified references, clear licenses, and detailed provenance, including continued metadata accessibility when data are no longer available.[2] DataCite describes DOI and metadata infrastructure for connecting research outputs and enabling discovery and reuse.[3] Neither a FAIR-aligned record nor a DOI is treated here as proof that evidence is current, independent, or scientifically true.

The repository's existing `external-evidence-normalization_v0.1.0` remains stable prior evidence for execution-mode admission. Its evidence is reused by stable reference and is not counted again as a new independent evidence item.

## Contract

Every evidence record requires a stable source identifier, an underlying-evidence identifier, a locator, authority kind, transformation reference, claim scope, and status-specific time/version metadata. `CURRENT` additionally requires a source-version reference and currentness basis. `STALE` and `HISTORICAL` are preserved for review but are not placed in the current set. `RETRIEVED_UNVERIFIED` is distinguishable from current; `REMEMBERED_UNVERIFIED` and `UNKNOWN` are held rather than silently treated as retrieved or current.

Records sharing one `underlying_evidence_id` are counted once for unique underlying evidence and marked as reuse. A derived record is linked to its parent rather than treated as a fresh independent replication. A claimed replication record that shares an underlying evidence identifier with another record is held as `DUPLICATION_MISLABELED_AS_REPLICATION`. Same-locator records with unresolved underlying identity are indeterminate rather than deduplicated by URL alone. Conflicting content digests for the same underlying evidence are invalid.

Temporal contradictions are fail-closed: a source publication time after its retrieval time is invalid. Missing derivation parents, self-derivation, duplicate record identifiers, missing stable identity, and mismatched new-evidence counts are held or invalid. All decisions normalize output boundary fields to `CANONICAL_EFFECT=NONE`, `GOVERNANCE_EFFECT=NONE`, and `DEPLOYMENT=FALSE`, even when an input case requests an effect.

## Results

The module passed **21 pytest tests** and **15 synthetic cases**. The results are mechanism outcomes only.

| Case | Status | Interpretation |
|---|---|---|
| Current unique evidence | `COMPLETE` | Admissible for review; one unique underlying item |
| Stale or historical evidence | `COMPLETE` | Preserved but excluded from current set |
| Retrieved but unverified | `COMPLETE` | Review metadata only; not current |
| Remembered but unverified | `INDETERMINATE` | Held as non-admissible without retrieval basis |
| Unknown currentness | `INDETERMINATE` | Held rather than guessed current |
| Duplicate records | `COMPLETE` | One underlying item; reuse explicitly recorded |
| Duplicate labeled as replication | `INVALID` | `DUPLICATION_MISLABELED_AS_REPLICATION` |
| Derived record | `COMPLETE` | Linked to parent; not silently counted as independent replication |
| Same locator, unresolved underlying relation | `INDETERMINATE` | URL equality is insufficient for deduplication |
| Same underlying digest contradiction | `INVALID` | Conflicting content identity held |
| Publication after retrieval | `INVALID` | Temporal contradiction |
| Missing stable identity | `INDETERMINATE` | Provenance incomplete |
| Missing derivation parent | `INDETERMINATE` | Lineage incomplete |
| Boundary-effect request | `INVALID` | Output effects normalized to NONE/FALSE |

## Falsifiers

The mechanism would be falsified if it treated remembered material as current, treated a retrieved-but-unverified record as a verified source, counted mirrors or derived records as independent evidence, deduplicated distinct evidence solely by URL, accepted conflicting digests for one underlying item, accepted temporal contradictions, or emitted canonical/governance/deployment effects from metadata.

A successful ledger audit does not mean that evidence is true, representative, independent, replicable, causal, generalizable, or suitable for canonical promotion. It establishes only that the supplied identity/currentness metadata is internally admissible for later human review.

## Explicit non-claims

```text
RETRIEVED != CURRENT
REMEMBERED != AUTHORITATIVE
REFERENCE != NEW_EVIDENCE
DUPLICATION != REPLICATION
DERIVED_RECORD != INDEPENDENT_REPLICATION
PROVENANCE_METADATA != SCIENTIFIC_VALIDITY
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

The implementation uses only the Python standard library. It does not execute models, query private data, alter `main`, or change any canonical state.

## Reproduction

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_currentness_experiment.py --output fixtures/currentness_result.json
```

## References

[1]: https://www.w3.org/TR/prov-o/ "W3C — PROV-O: The PROV Ontology"
[2]: https://www.go-fair.org/fair-principles/ "GO FAIR — FAIR Principles"
[3]: https://datacite.org/ "DataCite — Connecting Research, Advancing Knowledge"
