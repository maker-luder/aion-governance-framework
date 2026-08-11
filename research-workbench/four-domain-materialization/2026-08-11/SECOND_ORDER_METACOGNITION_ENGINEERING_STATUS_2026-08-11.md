# Second-Order Metacognition Engineering Status — 2026-08-11

```text
STATUS = RESEARCH_IMPLEMENTATION
SOURCE_GAP = SECOND_ORDER_COMPUTATION_RESEARCH_GAP_2026-08-10
SOURCE_CALIBRATION = SECOND_ORDER_METACOGNITION_LITERATURE_CALIBRATION_2026-08-11
EXECUTABLE_LEVEL_3_CANDIDATE = IMPLEMENTED
LEVEL_3_FUNCTIONAL_CONTRIBUTION = NOT_ESTABLISHED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```

## Closed engineering gap

The earlier records already specified the monitored first-order target, immutable evidence
requirements, anti-lookahead order, matched conditions, monitoring/control separation,
missing-outcome semantics and ontological non-claims. This pass materializes those
repository-defined constraints in:

`research-labs/second-order-metacognition_v0.1.0/`

## Implementation decisions

These are Codex research implementation decisions, not canonical doctrine:

1. reuse the existing Level‑2 `FinitePredictiveSelfModel`, `Task` and `Action` types;
2. use prior categorical prediction accuracy as the first bounded monitor signal;
3. keep the monitor deterministically recomputable from immutable trial records;
4. make `REQUEST_VERIFICATION` the only active v0.1.0 control effect;
5. preserve full-label and commit-only outcome contracts as separate regimes;
6. return `NOT_ESTABLISHED` for functional contribution and subjectivity conclusions.
7. reject silent monitor-evidence pooling across run, subject, context or model identity;
8. fail closed on mixed-condition monitor recomputation while leaving the scientific
   admissibility of a separate cross-condition analysis as `HOLD_FOR_RESEARCH_DECISION`.
9. expose missingness, raw observed sample size, evidence growth and action-conditioned
   observation counts without imputing unavailable outcomes or claiming an ESS estimator.
10. provide matched threshold-sweep plumbing without selecting or tuning a preferred
    threshold; scientific execution remains `DEFERRED_TO_EXPERIMENT`.
11. add a deterministic in-memory `VerificationProvider` contract, fallible evidence
    schema, immutable trace ledger, timing/scope guards and raw rejection diagnostics;
12. preserve the first-order trace and control disposition while keeping any experimental
    post-verification disposition in a separate intervention artifact.
13. adapt matched condition summaries into the existing generic evaluation harness while
    retaining raw denominators, verification diagnostics and claim-boundary dispositions.
14. bind verification diagnostics to explicit condition/run/provenance artifacts; missing
    condition evidence remains `NOT_PROVIDED`, and global diagnostics remain global.
15. bind every verification assessment to an immutable first-order-prediction target;
16. replace permissive evidence strings with a typed allowlist plus oracle/unknown
    rejection paths, and require a bounded provider capability declaration;
17. add deterministic verification-ledger JSON round trips that preserve accepted,
    incorrect and rejected evidence semantics.
18. materialize trace-only, applied, ablated and seeded-randomized matched intervention
    conditions; stale intervention remains deferred;
19. add raw full-label operational trade-off metrics while returning `NOT_IDENTIFIABLE`
    for outcome-dependent `COMMIT_ONLY` metrics;
20. adapt each intervention condition to its own generic-harness case without cross-
    condition diagnostics borrowing.

```text
VERIFICATION_PROVIDER = IMPLEMENTED / TARGETED_TESTED
VERIFICATION_EVIDENCE_SCHEMA = IMPLEMENTED / TARGETED_TESTED
ANTI_ORACLE_CONTRACT = IMPLEMENTED / TARGETED_TESTED
VERIFICATION_ACTION_EFFECT = RESEARCH_INTERVENTION_SUBSTRATE_IMPLEMENTED
SECOND_ORDER_EVALUATION_ADAPTER = IMPLEMENTED / TARGETED_TESTED
CLAIM_BOUNDARY_PRESERVED = TARGETED_TESTED
CONDITION_SCOPED_DIAGNOSTICS = IMPLEMENTED / TARGETED_TESTED
VERIFICATION_TARGET_BINDING = IMPLEMENTED / TARGETED_TESTED
TRACE_SERIALIZATION = IMPLEMENTED / TARGETED_TESTED
EVIDENCE_TYPE_FAIL_CLOSED = IMPLEMENTED / TARGETED_TESTED
DECLARED_PROVIDER_CAPABILITY_CONTRACT = IMPLEMENTED / TARGETED_TESTED
BUILT_IN_SYNTHETIC_PROVIDER = BOUNDED_BY_IMPLEMENTATION
POST_VERIFICATION_DISPOSITION = IMPLEMENTED / SEPARATE_ARTIFACT
TRACE_ONLY_CONDITION = IMPLEMENTED
APPLIED_CONDITION = IMPLEMENTED
ABLATION_CONDITION = IMPLEMENTED
RANDOMIZED_CONDITION = IMPLEMENTED
STALE_CONDITION = DEFERRED
RAW_CAUSAL_METRICS = IMPLEMENTED / NO_AGGREGATE_SCORE
```

## Still open

- independent fixture design and preregistration;
- whether any cross-condition monitor-evidence pooling is scientifically admissible;
- adverse-condition experiments and execution of a preregistered threshold study
  (threshold-sweep support is implemented);
- causal correction for feedback starvation / selection bias outside the full-label
  synthetic contract (diagnostics are implemented; correction remains open);
- independent evaluation-adapter implementation and QA;
- independent implementation and QA;
- any claim about phenomenal metacognition, self-awareness or consciousness.

```text
DEFERRED_TO_QA = REPO_WIDE_TESTS / MATRIX / COVERAGE / TYPE_AUDIT / SECURITY_AUDIT
```
