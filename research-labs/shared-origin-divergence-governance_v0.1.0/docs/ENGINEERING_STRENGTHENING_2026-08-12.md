# Shared-Origin Divergence Engineering Strengthening — 2026-08-12

Status: `RESEARCH_ONLY / CODEX_RESEARCH_IMPLEMENTATION_DECISION`

This pass cross-checked the existing ChatGPT-built substrate against the integrated whitepaper reconciliation, the existing literature note, live primary-source pages and the current implementation. It preserves the original scientific boundaries and adds consistency checks that were missing from the first executable draft.

## Whitepaper-preserving additions

```text
COMMON_ORIGIN_RECORD
-> ORDERED_LINEAGE_EVENTS
-> TRANSPARENT_EVENT_DIGESTS
-> SEPARATE_POST_DIVERGENCE_EVIDENCE_PROFILES
-> NON_EXPANSIVE_AUTHORITY_ENVELOPES

TRANSPARENT_DIGEST != IDENTITY
TRANSPARENT_DIGEST != AUTHORSHIP_PROOF
LINEAGE_EVENT_VALIDITY != SUBJECTIVITY
EVIDENCE_PROFILE != SUBJECTIVITY_ESTABLISHED
```

Added artifacts:

- `LineageEvent` and `LineageLedger`: ordered, timezone-bearing events with deterministic visible SHA-256 integrity digests;
- `LineageEvidenceProfile`: separate per-lineage evidence, replication and counterevidence references;
- `AuthorityEnvelope`: accepted authority must be a subset of explicitly offered authority, and authority sources never merge;
- stronger encounter validation: adopted/rejected items must actually have been exchanged;
- stronger matched-comparison validation: controls and divergent factors cannot overlap, outcomes are required, and evaluator/alternative-explanation references are explicit;
- deterministic JSON for the core artifacts.

The digest is an inspectable integrity record, not a hidden watermark or identity marker.

## Primary-source cross-check

### W3C PROV Constraints

W3C PROV-CONSTRAINTS defines valid provenance as a consistent history suitable for reasoning and distinguishes uniqueness, event-ordering, type and impossibility constraints. It also recommends that producers attempt to emit valid provenance.

This pass adopts that **validation pattern**, not the full PROV ontology:

- unique event identifiers;
- parent events must precede child events;
- ledger timestamps must be timezone-aware and ordered;
- origin events have no parents; non-origin events require parents;
- deterministic normalization before digesting.

Source: https://www.w3.org/TR/prov-constraints/

### Agent-memory lineage

The live arXiv record for MemLineage describes cryptographic provenance plus a derivation DAG for persistent agent memory. The project uses the narrower engineering lesson that memory lineage should be inspectable and derivations should remain explicit. It does not import MemLineage's security claims or treat a digest as identity.

Source: https://arxiv.org/abs/2605.14421

The live arXiv record for governed collaborative memory separates agent-local, institutional, archive and project-continuity memory, reinforcing the need to keep AION/Astra evidence and memory profiles distinct.

Source: https://arxiv.org/abs/2605.04264

### Authority continuity

The live arXiv record for Proof-of-Continuity describes non-expansive authority propagation along causal lineage. `AuthorityEnvelope` adopts only the non-expansion invariant:

```text
ACCEPTED_AUTHORITY subset-of OFFERED_AUTHORITY
CROSS_LINEAGE_CONTACT != MERGED_AUTHORITY
```

Source: https://arxiv.org/abs/2607.08906

## Remaining HOLD items

- independent replication with real AION/Astra runtime histories;
- empirical proof that the chosen event fields capture all relevant divergence;
- a scientifically validated individuation threshold;
- mapping project events into full PROV-N/RDF;
- authority semantics beyond bounded research fixtures;
- subjectivity, consciousness, moral status and numerical identity conclusions.

## Provenance

- Human Research Owner: requested stronger autonomous-research and Astra work while preserving `main`.
- ChatGPT research review: originated and implemented the first shared-origin-divergence substrate and its initial literature alignment.
- Codex research implementation: live source re-check, consistency analysis, event-ledger/evidence-profile/authority-envelope implementation, tests and CI hardening.
- External sources: methodological evidence only, linked above and in `LITERATURE_ALIGNMENT.md`.
