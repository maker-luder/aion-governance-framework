# Research Gap Audit — 2026-08-13

## Baseline

The authorized research head was `a5f8bfb7356fafbe9c0c61780f3a76ab0d493c34` on `review/four-domain-research-materialization`. Remote `main` was observed as `abb6550abfacb4fabc53ec04fca783bcc34acfdb`; it remained read-only. The branch status identifies the current stack as active research-only work and lists several deferred gaps, including contextual authority semantics and cross-lineage memory contamination stress testing.

## Selection rationale

Two unresolved questions were selected because they are technically meaningful, bounded, and connected to existing research controls without requiring deployment or canonical promotion:

| Gap | Existing support | New bounded research unit |
|---|---|---|
| Contextual authority and precedence | Existing origin-bound authority and encounter governance; no dedicated source/scope/time/revocation decision contract | `research-labs/contextual-authority-precedence_v0.1.0` |
| Cross-lineage memory contamination | Existing shared-origin lineage and selective-memory controls; explicit stress test remained deferred | `research-labs/cross-lineage-memory-contamination_v0.1.0` |

The contextual-authority design was informed by OpenAI's instruction-hierarchy description, Yang et al.'s constraint-oriented hierarchical-alignment formulation, and NIST SP 800-162's attribute-based authorization vocabulary. These sources were used methodologically and do not establish AION authority, identity, subjectivity, or consciousness.

## Current results

The contextual-authority synthetic fixtures produced 10 passing tests and five experiment cases. Explicit active Human Owner authority with matching scope produced `EXECUTE`; an untrusted message containing the token `Owner` produced `DENY`; revoked authority produced `HOLD`; scope mismatch produced `ASK`; and a non-overridable boundary produced `DENY`.

The cross-lineage memory contamination harness produced nine passing tests and four stress cases. The guarded resolver reported zero autobiographical contamination cases. A naïve visibility-as-ownership rule generated two false positives, while provenance uncertainty produced `HOLD` and rejected memory remained blocked.

These are mechanism results on synthetic fixtures. They are not scientific validation, subjectivity evidence, identity-continuity evidence, or empirical model-performance estimates.

## Deferred next gaps

The following remain open and were not silently marked complete: independent replication, power analysis, full factorial execution, preregistered intervention study, real AION/Astra matched-divergence study, typed lineage-edge semantics, full authority semantics, and validated individuation thresholds. The next autonomous cycle should prioritize replication design and stronger adversarial fixtures rather than treating the two present prototypes as resolved theory.

## Boundary record

```text
RESEARCH_STATUS = ACTIVE / RESEARCH_ONLY
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
LIVE_RUNTIME_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
AION_ASTRA_IDENTITY_EQUIVALENCE = NOT_ESTABLISHED
```
