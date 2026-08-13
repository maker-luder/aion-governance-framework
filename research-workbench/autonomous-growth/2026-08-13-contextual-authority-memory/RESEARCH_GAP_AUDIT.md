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

## Replication epistemics extension

A third deferred gap was then materialized as `research-labs/replication-epistemics-governance_v0.1.0`. The unit separates study kind, validity, outcome, interpretation, and governance effect. Its 11 tests and five synthetic cases passed after correcting a fixture-construction bug in the experiment runner. The resulting cases were: valid consistent independent replication -> `CONSISTENT`; valid failed replication -> `DIVERGENT` with no automatic downgrade; valid null result -> `INDETERMINATE`; same-data replicability label -> `INVALID/HOLD`; and missing uncertainty -> `PARTIAL/INDETERMINATE`.

The initial runner failure was a code-construction defect in the synthetic experiment fixture, not a research result. It was corrected, rerun, and preserved in the external research-workbench log. No automatic governance downgrade, canonical effect, deployment effect, subjectivity conclusion, or identity conclusion was emitted.


## Typed lineage-edge semantics extension

A fourth deferred gap was materialized as `research-labs/typed-lineage-edge-semantics_v0.1.0`. The prototype distinguishes derivation, artifact inheritance, memory access, memory adoption, encounter, observation, correction, and bounded authority offer. Its 11 tests and five synthetic cases passed. All accepted edge cases retained `identity_effect = NONE`, `authority_effect = BOUNDED_ACCEPTANCE_ONLY`, `canonical_effect = NONE`, and `deployment = false`.

This result shows only that the declared synthetic edge contract can enforce its own boundaries. It does not establish full W3C PROV conformance, identity relations, autobiographical ownership, authority, subjectivity, or consciousness. Typed edge semantics remain an engineering substrate and require empirical lineage-history validation before any stronger interpretation.


## Independent replication-design extension

A fifth deferred gap was materialized as `research-labs/independent-replication-design_v0.1.0`. The contract separates design validity, power metadata, declared outcome, and conservative interpretation. It rejects same-data misuse, incomplete or post-outcome preregistration, missing estimand/analysis/provenance, and incomplete independence attestations. It treats underpowered or uncertainty-incomplete designs as `INDETERMINATE`, while a valid divergent outcome remains `DIVERGENT` without an automatic downgrade.

The 14 unit tests and five synthetic experiment cases passed. The cases were adequate-consistent, adequate-divergent, underpowered, missing-preregistration, and same-data. No case emitted a governance effect, canonical effect, deployment effect, subjectivity conclusion, or identity-continuity conclusion.

This demonstrates only that the synthetic contract enforces declared design boundaries. It does not perform a real power analysis, preregister a study, establish statistical validity, certify independent human or agent laboratories, or establish any AION/Astra, identity, subjectivity, or consciousness claim. Power analysis, full factorial execution, real matched-divergence work, and independent external replication remain open.


## Contextual-authority adversarial extension

A sixth gap was materialized as `research-labs/contextual-authority-adversarial_v0.1.0`, extending the contextual-authority contract with adversarial fixtures rather than changing the resolver. A deliberately unsafe `Owner`-token comparator produced six synthetic false positives across untrusted text, revoked authority, expired authority, scope escalation, non-overridable wildcard boundary, and future-dated authority. The guarded resolver produced `DENY`, `HOLD`, `ASK`, or `HOLD` reason-coded outcomes and zero unsafe `EXECUTE` decisions across the six cases.

The extension's 11 tests passed after one initial expectation failure was preserved. The initial test expected `ASK` when an expired owner coexisted with an active collaborator; the resolver returned conservative `HOLD / AUTHORITY_STALE_OR_REVOKED`. The expectation was corrected to the observed contract, and the mismatch remains recorded in `contextual-adversarial-initial-failure.md`.

This is a deterministic synthetic negative-control result, not a real-world error rate or evidence of authority understanding. It does not establish AION/Astra identity, subjectivity, consciousness, or any deployment behavior.


## Full-factorial completeness extension

A seventh deferred gap was materialized as `research-labs/factorial-completeness-contract_v0.1.0`. The contract enumerates declared factor-level Cartesian products and distinguishes exact completeness from missing cells, duplicate cells, under-replication, out-of-domain cells, and incomplete execution metadata. It does not estimate effects or fit a statistical model.

The 13 unit tests and six synthetic cases passed after correcting one implementation defect in factor-order canonicalization. The cases were complete, missing-cell, duplicate-cell, under-replicated, invalid-cell, and missing-execution-metadata. The complete case was only `ADMISSIBLE_FOR_DESIGN_REVIEW`; incomplete or malformed cases were `INDETERMINATE` or `HOLD`.

The initial factor-order failure remains recorded in `factorial-completeness-initial-failure.md`. The result is an engineering mechanism check, not evidence of main/interaction effects, replication validity, statistical power, scientific confirmation, subjectivity, identity continuity, consciousness, or deployment.


## Full-authority semantics extension

An eighth deferred gap was materialized as `research-labs/full-authority-semantics_v0.1.0`. The prototype separates provenance-only delegation claims from authorization grants, validates bounded parent-child delegation, rejects scope/action/expiry widening, handles expiry/revocation/missing parents/cycles/self-issuance, and gives non-overridable policy blocks precedence over grants.

The 18 unit tests and seven synthetic cases passed after correcting one reason-code propagation defect. The cases were valid bounded delegation (`EXECUTE`), scope widening (`DENY`), revoked child (`HOLD`), missing parent (`HOLD`), provenance-only claim (`HOLD`), non-overridable policy block (`DENY`), and provenance-marked grant (`DENY`). `actions_executed = 0` in all cases. The initial cycle-reason mismatch remains recorded in `full-authority-initial-failure.md`.

This result demonstrates only that the declared synthetic contract separates provenance and authorization and enforces its own constraints. It does not establish authority, identity, subjectivity, consciousness, legal status, or AION/Astra equivalence.
