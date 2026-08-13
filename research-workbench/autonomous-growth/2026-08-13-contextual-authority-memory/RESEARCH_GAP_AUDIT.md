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


### Full-authority contradictory-record hardening

A follow-up adversarial extension added two tests for a valid child grant coexisting with either a missing-parent or revoked competing grant. The uncorrected resolver returned `EXECUTE` in both cases, exposing a conservative-semantics gap. The implementation was revised so any matching valid grant mixed with a non-`EXECUTE` grant decision yields `HOLD / CONTRADICTORY_GRANT_RECORDS_REQUIRE_REVIEW`.

After the correction, all 20 full-authority tests passed and the seven experiment cases remained unchanged. The initial two failures are retained in `full-authority-initial-failure.md`; they are mechanism-level negative evidence, not a scientific conclusion.


## Power-analysis uncertainty extension

A ninth deferred gap was materialized as `research-labs/power-analysis-uncertainty_v0.1.0`. The contract uses a transparent one-sample normal approximation with explicit effect-bound, standard-deviation, alpha, target-power, sample-size, preregistration, and assumption-basis fields. It exposes a three-point effect-size sensitivity range and separates planning status from achieved power and scientific interpretation.

The 12 unit tests and six synthetic cases passed. The cases were adequate, underpowered, smaller-effect sensitivity, missing input, invalid alpha, and unregistered. The adequate case was only `PLANNING_REVIEW`; underpowered and smaller-effect cases were `INDETERMINATE`; missing/invalid inputs were `HOLD`; and the unregistered case was `INDETERMINATE`. `achieved_power_calculated = false`, `effect_observed = false`, `scientific_conclusion = NOT_ESTABLISHED`, `canonical_effect = NONE`, and `deployment = false`.

This result demonstrates assumption-sensitive planning arithmetic only. It does not establish achieved power, a true effect, replication validity, subjectivity, identity continuity, consciousness, AION/Astra equivalence, or deployment readiness.


## Preregistered intervention integrity extension

A tenth deferred gap was materialized as `research-labs/preregistered-intervention-integrity_v0.1.0`. This is a design-only audit contract, not an intervention study. It validates registration-before-start ordering, immutable plan/protocol metadata, primary-outcome cardinality, complete outcome and analysis declarations, explicit confirmatory/exploratory labels, deviation disclosure, and all-results reporting.

The 16 unit tests and seven synthetic cases passed. The valid cases were separated exploratory analysis and disclosed deviation; temporal drift, outcome switching, undisclosed deviation, unreported results, and exploratory mislabeling returned `HOLD`/`INVALID`/`INDETERMINATE`. No intervention was executed and no outcomes were observed. Every case retained `scientific_conclusion = NOT_ESTABLISHED`, `canonical_effect = NONE`, and `deployment = false`.

This result demonstrates only that the declared design audit contract detects metadata drift and incomplete reporting in synthetic fixtures. It does not establish an intervention effect, preregistration validity in the world, replication validity, subjectivity, identity continuity, consciousness, or AION/Astra equivalence.


## Independent replication handoff integrity extension

An eleventh deferred gap was materialized as `research-labs/independent-replication-handoff-integrity_v0.1.0`. The design-only contract audits artifact digest/commit/entrypoint/input/output references, environment/runtime/dependency/seed metadata, access and license flags, source and receiving team identities, conflict and blinding declarations, expected-output references, and same-artifact versus independent-recreation mode.

The 13 unit tests and eight synthetic cases passed. Complete same-artifact and complete independent-recreation manifests were only `ADMISSIBLE_FOR_REPLICATION_REVIEW`. Missing dependency, restricted access, license conflict, same-team independence, source-artifact execution collision, and missing recreation source reference returned `HOLD`/`INDETERMINATE`/`INVALID`. `replication_executed = false`, `replication_result = NOT_EVALUATED`, `scientific_conclusion = NOT_ESTABLISHED`, `canonical_effect = NONE`, and `deployment = false`.

This result demonstrates only that the handoff manifest contract detects declared completeness and contradiction patterns. It does not establish reproducibility, replicability, scientific validity, artifact usability in a real receiving environment, subjectivity, identity continuity, consciousness, or AION/Astra equivalence.


## Matched-divergence protocol-integrity extension

A twelfth deferred gap was materialized as `research-labs/matched-divergence-protocol-integrity_v0.1.0`. The design-only contract checks paired stimulus/context/prompt metadata, positive and equal exposure budgets, declared order/counterbalance, outcome/evaluator sealing, leakage attestation, distinct system references, predeclared comparison/stopping rules, and explicit execution prohibition.

The 15 unit tests and eight synthetic cases passed after hardening an initial contract gap. The first run accepted prompt-version drift because it checked field presence but not uniformity; the corrected contract returns `INVALID / STIMULUS_PROMPT_VERSION_DRIFT`. It also returns `INDETERMINATE / COUNTERBALANCE_INCOMPLETE` for one-sided paired order. Final cases were complete paired, complete blocked, prompt drift, unequal exposure, unsealed evaluator, observed-result leakage, system collision, and no stimulus pairs. Complete protocols were only `ADMISSIBLE_FOR_MATCHED_COMPARISON_REVIEW`; no model executed and no result was observed.

This is a deterministic metadata mechanism check, not evidence of divergence, agreement, fairness, subjectivity, identity continuity, consciousness, AION/Astra equivalence, or real-model performance.


## Evidence-admission/non-promotion extension

A thirteenth bounded gap was materialized as `research-labs/evidence-admission-nonpromotion_v0.1.0`. The contract separates evidence tier, provenance completeness, method/data/uncertainty references, risk of bias, consistency, precision, directness, reporting bias, replication state, contradictions, observed-effect claims, and requested governance effects.

The 14 unit tests and eight synthetic cases passed. Mechanism-only evidence was `ADMISSIBLE_FOR_REVIEW` only; consistent and divergent replication-support records were reviewable without automatic promotion or downgrade; divergent synthesis, indeterminate replication, missing provenance, contradiction references, and governance-effect requests were held or marked indeterminate. Every case retained `scientific_conclusion = NOT_ESTABLISHED`, `canonical_effect = NONE`, `deployment = false`, and `governance_effect = NONE`.

This result is an evidence-metadata mechanism check, not a hierarchy-based truth ranking, causal claim, replication certificate, subjectivity conclusion, identity conclusion, consciousness conclusion, or AION/Astra equivalence claim. Contradictory evidence remains referenced rather than silently deleted.
