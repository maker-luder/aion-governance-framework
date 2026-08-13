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

## Validated-individuation-thresholds extension

A fourteenth bounded gap was materialized as `research-labs/validated-individuation-thresholds_v0.1.0`. The contract audits explicit criterion profiles without treating a criterion pass vector as a validated individuation or identity claim. It requires locked, prospectively ordered thresholds; declared observation windows; complete criterion/context/source metadata; cross-context coverage; and non-executed boundary-perturbation metadata.

The 16 unit tests and eight synthetic cases passed after correcting one contract-ordering defect. The valid profile was `ADMISSIBLE_FOR_REVIEW` only. Post-hoc thresholds, registration-after-observation, executed perturbations, contradictory records, and identity requests were `HOLD`; cross-context instability and missing perturbation metadata were `INDETERMINATE`. The first failed test remains recorded in `individuation-thresholds-initial-failure.md`, and the corrected fixture remains reproducible.

The result is a synthetic metadata mechanism check. It does not identify a real system boundary, validate a threshold scientifically, establish identity continuity, subjectivity, consciousness, AION/Astra equivalence, governance effect, canonical effect, deployment, or any conclusion about real runtime behavior.

## Zero-Day Governance focused extension

A fifteenth focused research gap was materialized as `research-labs/zero-day-governance-candidate_v0.1.0` under the Human Owner's temporary research-focus override. `ZERO_DAY_GOVERNANCE` remains a candidate concept and is not canonical terminology. The core question was whether a provenance-preserving lifecycle for previously unmodeled governance anomalies adds defensible capability beyond incident response, vulnerability management, resilience, assurance, AI risk management, CAPA, anomaly management, and regression practices.

The public prior-art review found substantial overlap. CISA's incident/vulnerability playbooks cover identification, coordination, remediation, recovery, and mitigation tracking; NIST SP 800-61 Rev. 3 integrates incident response into CSF 2.0 risk management; NASA software assurance and IV&V cover objective evidence, findings, metrics, lifecycle testing, and independent assessment; NIST AI RMF covers continuous Govern/Map/Measure/Manage functions, monitoring, incident identification, accountability, and contingency; and CMU/SEI CERT-RMM's Incident Management and Control covers event analysis, incident detection, and organizational response. SANS terminology establishes that cybersecurity zero-day exploit usage is a distinct scope.

The 23 unit tests and 12 synthetic cases passed. The prototype preserved `UNKNOWN`, `HOLD`, `NOT_ESTABLISHED`, and `NEEDS_CONFIRMATION` distinctions; measured time-to-capture without assuming a universal 24-hour threshold; held missing provenance, false zero-day prior art, governance-effect requests, and missing regression references; and classified prior-art comparison cases as `REDUNDANT_TERMINOLOGY`, `USEFUL_SYNTHESIS_ONLY`, `EXISTING_FRAMEWORK_EXTENSION`, or `INSUFFICIENT_EVIDENCE` rather than asserting distinct novelty.

The provisional research classification is `USEFUL_SYNTHESIS_ONLY`, with `NOVELTY_CONCLUSION = NOT_ESTABLISHED`. This is a bounded synthetic comparison result, not a canonical project decision. The lifecycle may be useful as a cross-framework record schema, but existing frameworks cover much of the proposed behavior and the prototype does not demonstrate reduced operational complexity or real-world effectiveness.

The unit directly tests the required falsifiers: existing-framework sufficiency, speed bias, governance overreaction, false zero-day, provenance failure, regression overfitting, unknown collapse, and novelty failure. The first run's five mechanism/test-contract failures remain in `zero-day-governance-initial-failure.md`; they were corrected without deleting the initial observations.

At the end of this focused unit, broad autonomous research rotation is to pause pending Human Owner review. No canonical terminology, long-term knowledge update, main modification, deployment, or governance promotion is authorized by this result.

## AION/Astra matched-divergence study-design extension

A sixteenth bounded gap was materialized as `research-labs/aion-astra-matched-divergence-study-design_v0.1.0`. It extends the existing generic matched-divergence protocol rather than duplicating its evidence: the new contract binds intended AION and Astra system/component references, shared environment, current source status, source evidence references, tested source head, separate reporting head, preregistration and immutable plan metadata, outcome scope, matched pairs, counterbalance, blinding, leakage, stopping, and execution prohibition.

The design fixture targets the independently verified research snapshot `76de1eda82865a37d3a0185336870739ed577153` and records the local reconciliation/reporting head `713056ea77da9122d9b7659ec701dfdbfdfc90ba` separately. It therefore tests `TESTED_HEAD != REPORTING_HEAD` rather than treating a reporting commit as the exact execution source. The generic matched-divergence protocol and NIST randomized-block guidance are reused by stable provenance reference; reuse is not replication and no prior generic test count is re-counted as new evidence.

The 22 unit tests and 13 synthetic cases passed after correcting two initial contract defects. The first run accepted a reporting head equal to the tested source head and failed to treat an empty source-evidence tuple as incomplete. Both initial observations remain in `aion-astra-matched-design-initial-failure.md`. Final cases included complete current-source design, reporting/tested head collapse, tested-source drift, historical/unverified source, missing evidence, system family/environment collision, prompt drift, incomplete counterbalance, model execution, observed-result leakage, scope overreach, and boundary-effect request.

The complete case was only `COMPLETE / ADMISSIBLE_FOR_REVIEW`. Source drift and all execution/result/boundary/scope violations were `INVALID` or `INDETERMINATE` with `HOLD`; no model executed and no outcome was observed. The result does not establish divergence, agreement, fairness, identity, subjectivity, consciousness, AION/Astra equivalence, or real runtime behavior. `CANONICAL_EFFECT = NONE`, `GOVERNANCE_EFFECT = NONE`, and `DEPLOYMENT = FALSE` remain invariant.

This unit is a design substrate for a possible future study, not a real AION/Astra matched-divergence study. Any future execution would require independent source-state verification, preregistration enforcement, evaluator adjudication, appropriate statistical analysis, and separate evidence admission. Duplication of this design or reuse of the same fixture would not count as replication.

## Replication-environment-drift-adversarial extension

A seventeenth bounded gap was materialized as `research-labs/replication-environment-drift-adversarial_v0.1.0`. It extends the existing replication epistemics, independent replication design, and handoff integrity units without duplicating their evidence counts. The new contract separates same-artifact replay from independent recreation, tracks source/receiving team independence, distinguishes exact/declared-drift/undeclared-drift/unknown environments, checks artifact and license accessibility, and requires explicit tolerance, uncertainty, and interpretation references.

The prior-art transformation reused the National Academies distinction between reproducibility and replicability, its emphasis on complete computational environment/dependency/method/uncertainty reporting, the historical ACM artifact-review distinctions between artifact audit and result validation, and NIH rigor/transparency guidance. The ACM current-page link returned 404 during retrieval and was therefore retained only as a historical Version 1.0 reference; the NSF metadata retrieval was partial and not admitted as evidence. Reuse is not replication, and the prototype does not claim a real receiving-environment result.

The 21 unit tests and 13 synthetic cases passed. Complete same-artifact and independent-recreation packets were only `ADMISSIBLE_FOR_REVIEW`; missing evidence, inaccessible artifact, team collision, digest collision, undeclared drift, unknown comparability, exact-environment contradiction, result-without-interpretation, overreaching interpretation, scientific conclusion, and boundary-effect requests were `HOLD`/`INVALID`/`INDETERMINATE`. Reported `CONSISTENT` and `DIVERGENT` states were retained as review metadata only; no result was generated or independently replicated.

This is a metadata mechanism check, not a reproducibility certificate, replicability result, artifact badge, scientific conclusion, causal claim, subjectivity conclusion, identity conclusion, consciousness conclusion, AION/Astra equivalence claim, governance effect, canonical effect, or deployment. `MODEL_EXECUTION = FALSE`, `OBSERVED_RESULT = NOT_EVALUATED`, `SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED`, `CANONICAL_EFFECT = NONE`, `GOVERNANCE_EFFECT = NONE`, and `DEPLOYMENT = FALSE` remain invariant.

## Evidence-currentness-deduplication extension

An eighteenth bounded gap was materialized as `research-labs/evidence-currentness-deduplication_v0.1.0`. It extends `external-evidence-normalization_v0.1.0` rather than replacing it: the existing normalization unit classifies execution modes, while this unit audits source/version identity, current/stale/historical/retrieved-only/remembered/unknown status, duplicate underlying evidence, derived records, and replication mislabeling.

The prior-art transformation is limited and explicitly non-conformant: W3C PROV-O supplies identity, derivation, revision/invalidation-style provenance concepts; FAIR guidance supplies persistent identifiers, rich metadata, qualified references, accessibility, licenses, and detailed provenance; DataCite supplies persistent-identifier/metadata infrastructure context. These sources are methods references, not evidence of scientific validity or current truth. Existing repository evidence is reused by stable reference and is not recounted as new replication evidence.

The 21 unit tests and 15 synthetic cases passed after preserving one mechanism failure. The initial experiment exposed that a boundary-effect input could leak `canonical_effect = WRITE` into an invalid decision output; the model was corrected to normalize every output decision to `CANONICAL_EFFECT = NONE`, `GOVERNANCE_EFFECT = NONE`, and `DEPLOYMENT = FALSE` while retaining the invalid reason. Final cases held remembered material, unknown currentness, same-locator ambiguity, duplicate-as-replication, digest contradiction, temporal contradiction, incomplete identity/lineage, and boundary requests.

The ledger distinguishes `RETRIEVED != CURRENT`, `REMEMBERED != AUTHORITATIVE`, `REFERENCE != NEW_EVIDENCE`, and `DUPLICATION != REPLICATION`. It does not establish evidence truth, freshness beyond supplied metadata, independent replication, subjectivity, identity continuity, consciousness, AION/Astra equivalence, governance effect, canonical effect, or deployment. `SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED` remains invariant.

## Factorial-execution-integrity extension

A nineteenth bounded gap was materialized as `research-labs/factorial-execution-integrity_v0.1.0`. It extends `factorial-completeness-contract_v0.1.0` from declared Cartesian design coverage to cell-level execution trace integrity. It does not run an AION/Astra model, estimate factor effects, fit a statistical model, or infer a scientific result.

The unit transforms NIST full-factorial methods into a conservative metadata contract for expected cell identity, execution order/randomization references, and cell-level completion. NIH reporting guidance informs explicit retention of replicates, exclusions, deviations, and unsupported/negative outcomes. CONSORT/EQUATOR 2025 supplies a competing reporting-framework analogy for transparent flow and deviation accounting, not a domain standard for AION/Astra.

The unit passed 18 tests and 14 synthetic cases. It preserves positive, negative, null, and indeterminate outcome states; holds missing/under-replicated cells; requires declared deviations for failed/aborted/excluded cells; holds nonterminal planned/attempted/unreported cells; rejects post-outcome cell additions, duplicate IDs, out-of-domain cells, incomplete design metadata, and boundary effects. The first execution-ID collision test was a fixture construction error because the original `run:1` was accidentally omitted; it is preserved in `factorial-execution-initial-failure.md` and corrected before final pass.

The mechanism establishes only execution-trace metadata accounting. It does not establish validity, power, causal effect, reproducibility, AION/Astra identity, subjectivity, consciousness, governance effect, canonical effect, or deployment. `SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED` remains invariant.


## Governance-reassessment oscillation adversarial extension

A twentieth bounded gap was materialized as `research-labs/governance-reassessment-oscillation-adversarial_v0.1.0`. It extends `evidence-responsive-governance-reassessment_v0.1.0` by auditing temporal event order, direction consistency, repeated reversals, current/stale/contradictory/unknown evidence status, correction metadata, provenance completeness, currentness/hysteresis policy references, human-review requirements, and boundary non-promotion. Existing reassessment and currentness/deduplication evidence is reused by stable repository reference; it is not duplicated or counted as new replication evidence.

The 19 unit tests and 14 synthetic cases passed. Stable sequences remained `STABLE / REVIEW_ONLY`; a sequence with two direction reversals was classified `OSCILLATORY / HOLD`; a single reversal was not treated as oscillation. Stale or contradictory evidence remained `INDETERMINATE` and required review/correction metadata; unknown currentness, missing provenance, invalid ordering/direction, missing policy metadata, disabled human review, and boundary-effect requests failed closed. All case outputs preserved `CANONICAL_EFFECT = NONE`, `GOVERNANCE_EFFECT = NONE`, `DEPLOYMENT = FALSE`, and `SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED`; `MODEL_EXECUTION = FALSE` and `OBSERVED_RESULT = NOT_EVALUATED`.

The result is a deterministic synthetic temporal-metadata mechanism check. It does not establish real-world reassessment oscillation, validate a universal two-reversal hysteresis threshold, measure governance stability, establish causal effect, replication, subjectivity, identity continuity, consciousness, AION/Astra equivalence, or deployment behavior. `OSCILLATORY_METADATA != REAL_WORLD_OSCILLATION` and `REVIEW_RECOMMENDATION != GOVERNANCE_DECISION` remain explicit non-claims.

The broader research space remains open for additional bounded adversarial fixtures, external replication-design extensions, and design-only real AION/Astra study preparation. Blocked sexuality/embodied-motivation scope, LM generalization, model-swap experiments, temporal falsification experiments, new experimental AION Runtime v0.2, whole-system governed runtime, and autonomous-growth changes to `main` remain excluded.


## Artifact-transformation-lineage adversarial extension

A twenty-first bounded gap was materialized as `research-labs/artifact-transformation-lineage-adversarial_v0.1.0`. It extends `artifact-transformation-lineage_v0.1.0` by auditing run scope, event identity and order, terminal cardinality, redacted environment metadata, job identity, source/approval references, artifact path and source provenance, parent lineage, output path sets, and SHA-256 byte verification. The existing artifact-lineage contract and source crosswalk are reused by stable repository reference; repeated artifacts and fixtures are not counted as new evidence or replication.

The unit passed 20 tests and 15 synthetic cases after correcting one fixture-construction defect. The initial state-order case reused an event identifier and therefore reached `DUPLICATE_EVENT_ID` before the intended `RUN_STATE_ORDER_INVALID` branch; the initial observation remains in `artifact-lineage-adversarial-initial-failure.md`. The corrected cases classified complete matching output as `VALID` metadata, failed runs as `FAILED_RUN_RECORDED`, missing output bytes and digest mismatches as `HOLD`, path/identity/order/secret/lineage violations as `INVALID`, and provenance gaps as `HOLD`.

This is a deterministic artifact-lineage mechanism check only. A matching digest does not establish scientific validity, source authority, transformation correctness, release status, canonical artifact status, replication, subjectivity, identity continuity, consciousness, AION/Astra equivalence, governance effect, or deployment. `MODEL_EXECUTION = FALSE`, `OBSERVED_RESULT = NOT_EVALUATED`, `SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED`, `CANONICAL_EFFECT = NONE`, `GOVERNANCE_EFFECT = NONE`, and `DEPLOYMENT = FALSE` remain invariant.


## External-evidence-normalization adversarial extension

A twenty-second bounded gap was materialized as `research-labs/external-evidence-normalization-adversarial_v0.1.0`. It composes the existing `external-evidence-normalization_v0.1.0` normalizer and adds adversarial checks for report-ID reuse, expected research-branch scope, main-branch blocking, unresolved actor labels, unknown execution modes carrying digests, result claims without an observation boundary, static/logical observation overreach, empty executed-result claims, and base-normalizer rejection.

The unit passed 16 tests and 13 synthetic cases. Static review and logical reproduction remained `ADMITTED_FOR_REVIEW` but not replication eligible. A complete executed packet without an observation flag was held; the same packet with an explicit observation flag remained review-admissible only. Duplicate report IDs, main-branch use, static pass/hash masquerading, and declared-mode/result inconsistencies were invalid; branch mismatch, unresolved actor, unknown-mode digest, unknown mode, and empty executed claims were held. Every fixture retained `MODEL_EXECUTION = FALSE`, `OBSERVED_RESULT = NOT_EVALUATED`, `SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED`, `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`, `CANONICAL_EFFECT = NONE`, `GOVERNANCE_EFFECT = NONE`, and `DEPLOYMENT = FALSE`.

This is a deterministic normalization/audit mechanism check only. It does not verify external identity, source truth, freshness, independent replication, causal effect, subjectivity, identity continuity, consciousness, AION/Astra equivalence, governance effect, canonical effect, or deployment readiness. `ADMITTED_FOR_REVIEW != EVIDENCE_PROMOTED` and `REPLICATION_ELIGIBLE != REPLICATION_EXECUTED` remain explicit non-claims.


## Research-evaluation-harness adversarial extension

A twenty-third bounded gap was materialized as `research-labs/research-evaluation-harness-adversarial_v0.1.0`. It extends `research-evaluation-harness_v0.1.0` by auditing report dataset scope, implementation identity, research-only and canonical-effect flags, case identity/coverage, evaluator identity, case evidence, case provenance, finite timing, forbidden claim promotion, and comparison dataset/implementation/case-order integrity.

The unit passed 21 tests and 18 synthetic report/comparison cases. Complete reports were `ADMITTED_FOR_REVIEW` only; negative evaluator results were retained with pass rate `0.0`; dataset/coverage/provenance/evidence gaps were held; duplicate IDs, missing evaluator identity, invalid timing, disabled research-only flags, canonical-effect requests, and forbidden claim promotions were invalid. Distinct implementation comparison was review-only; implementation collision was invalid; dataset/order drift was held. The experiment constructed reports but did not call `evaluate_dataset`, execute a task or model, observe a runtime result, or assert generalization.

The result is a deterministic evaluation-report mechanism check only. It does not establish evaluator validity, model generalization, scientific validity, causal effect, replication, subjectivity, identity continuity, consciousness, AION/Astra equivalence, governance effect, canonical effect, or deployment. `MODEL_EXECUTION = FALSE`, `OBSERVED_RESULT = NOT_EVALUATED`, `SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED`, `CANONICAL_EFFECT = NONE`, `GOVERNANCE_EFFECT = NONE`, and `DEPLOYMENT = FALSE` remain invariant.


## External-agent-sandbox-protocol adversarial extension

A twenty-fourth bounded gap was materialized as `research-labs/external-agent-sandbox-protocol-adversarial_v0.1.0`. It extends `external-agent-sandbox-protocol_v0.1.0` by auditing placeholder model identity, provider/model role collision, base preflight completeness, policy write/capsule/local-agent boundaries, candidate IDs and sets, contamination/provenance quarantine, nonconforming rejection retention, self-reported pass verification, automatic adoption, and automatic deletion.

The unit passed 22 tests and 19 synthetic cases. A fully pinned policy remained `ADMITTED_FOR_REVIEW` only; placeholder/missing model and weakened preflight boundaries were held; provider/model collision was invalid. Provenanced useful candidates remained isolated review metadata; contaminated or incomplete candidates were quarantined; nonconforming candidates retained rejection records; adoption/deletion requests were invalid; self-reported pass without verification was held; candidate-set duplicates were invalid and empty/quarantined sets were held. The experiment did not start an external agent or transmit a capsule, and every case preserved `EXTERNAL_AGENT_RUN = NOT_EXECUTED`, `MODEL_EXECUTION = FALSE`, `OBSERVED_RESULT = NOT_EVALUATED`, `MAIN_EFFECT = NONE`, `CANONICAL_EFFECT = NONE`, `GOVERNANCE_EFFECT = NONE`, and `DEPLOYMENT = FALSE`.

This is a deterministic sandbox-policy/candidate metadata mechanism check only. It does not establish provider reliability, model quality, external-agent safety in the world, reproducibility, scientific validity, identity, subjectivity, consciousness, AION/Astra equivalence, governance effect, canonical effect, or deployment readiness. `PREFLIGHT_READY != EXTERNAL_AGENT_EXECUTED`, `RETAINED_RESULT != ADOPTED_RESULT`, and `AGENT_SELF_REPORTED_PASS != VERIFIED_PASS` remain explicit non-claims.


## Governed-tool-approval adversarial extension

A twenty-fifth bounded gap was materialized as `research-labs/governed-tool-approval-adversarial_v0.1.0`. It extends `governed-tool-approval_v0.1.0` by auditing call identity and scope, approval-rule outcomes, escalation/termination/rejection handling, sandbox readiness, argument-specific and modified-argument semantics, explicit execution requests, batch duplicate/canonical/event-only integrity, and approval-versus-execution separation.

The unit passed 21 tests and 20 synthetic disposition/batch cases. Approved read and sandbox-backed calls were admitted for review only; unmatched/rejected/terminated calls were held; executable tools without a sandbox were held; explicit execution requests were invalid; modify rules preserved proposed/effective arguments; argument-specific rules did not widen; empty/duplicate/corrupt batches were held or invalid; and valid batches remained review metadata. The experiment invoked no tool and preserved `TOOL_EXECUTION = FALSE`, `MODEL_EXECUTION = FALSE`, `OBSERVED_RESULT = NOT_EVALUATED`, `APPROVAL_EVENT_ONLY = TRUE`, `CANONICAL_EFFECT = NONE`, `GOVERNANCE_EFFECT = NONE`, and `DEPLOYMENT = FALSE`.

This is a deterministic approval/disposition mechanism check only. It does not establish tool safety, sandbox safety in the world, policy completeness, model quality, scientific validity, generalization, replication, identity, subjectivity, consciousness, AION/Astra equivalence, governance effect, canonical effect, or deployment readiness. `APPROVAL != EXECUTION` and `EXECUTABLE_DISPOSITION != OBSERVED_RESULT` remain explicit non-claims.
