# Typed Lineage Edge Semantics v0.1.0

Status: `RESEARCH_ONLY / SYNTHETIC_FIXTURES / CANONICAL_EFFECT=NONE`

## Research question

Can typed lineage edges make derivation, artifact inheritance, memory access, memory adoption, encounter, observation, correction, and bounded authority offer distinguishable without allowing provenance relations to become identity or authority claims?

The existing shared-origin research line already uses W3C PROV as a methodological vocabulary and explicitly separates provenance from identity.[1] This prototype adds a small typed edge contract to the deferred `TYPED_LINEAGE_EDGE_SEMANTICS` gap. It does not claim full PROV conformance and does not replace the standing evidence architecture.

## Edge types

| Edge type | Permitted interpretation | Prohibited inference |
|---|---|---|
| `DERIVED_FROM` | A record or artifact has a declared derivation source. | Same identity or same autobiographical owner. |
| `INHERITS_ARTIFACT` | An artifact reference is carried into a later lineage. | Inherited memory ownership or authority. |
| `MEMORY_ACCESS` | A target can inspect a source memory reference. | Target autobiographical ownership. |
| `MEMORY_ADOPTION` | A target uses a memory as contextual material. | Identity merge or source-owner replacement. |
| `ENCOUNTERED` | Two lineages exchanged or observed material. | Merged authority or identity. |
| `OBSERVED` | An observation is linked to a lineage event. | Observation becomes ontology. |
| `CORRECTED` | A later record revises an earlier record. | Earlier evidence erased or silently rewritten. |
| `AUTHORITY_OFFER` | A bounded authority set is explicitly offered. | Authority acceptance beyond offered scope. |

## Hypotheses and falsifiers

`H1`: Typed edges reduce semantic ambiguity compared with a single untyped parent relation while preserving the non-identity boundary.

`H2`: Memory access/adoption and authority offer edges do not create autobiographical ownership, identity merge, or authority merge.

`H3`: Duplicate, self-loop, unprovenanced, contradictory, or out-of-scope edges are rejected or held rather than normalized into a valid lineage.

A falsifier is any accepted edge that creates `IDENTITY_EQUIVALENCE`, changes canonical state, merges authority, or transfers autobiographical ownership without an explicit separate record.

## Run

```bash
python -m pytest -q
python scripts/run_edge_experiment.py --output fixtures/edge_result.json
```

## Non-claims

```text
PROVENANCE_RELATION != IDENTITY_RELATION
MEMORY_ADOPTION != AUTOBIOGRAPHICAL_OWNERSHIP
AUTHORITY_OFFER != AUTHORITY_MERGE
EDGE_VALIDITY != SUBJECTIVITY_EVIDENCE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## References

[1]: https://www.w3.org/TR/prov-o/ "W3C PROV-O Recommendation"
[2]: https://www.w3.org/TR/prov-constraints/ "W3C PROV-CONSTRAINTS"
[3]: ../../research-labs/shared-origin-divergence-governance_v0.1.0/docs/LITERATURE_ALIGNMENT.md "AION shared-origin literature alignment"
