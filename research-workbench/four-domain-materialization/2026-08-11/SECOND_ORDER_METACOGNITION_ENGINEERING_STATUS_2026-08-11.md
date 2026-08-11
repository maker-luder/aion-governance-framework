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
8. leave cross-condition pooling as `HOLD_FOR_RESEARCH_DECISION` rather than creating a
   new analysis doctrine.
9. expose missingness, effective sample size, evidence growth and action-conditioned
   observation counts without imputing unavailable outcomes.

## Still open

- independent fixture design and preregistration;
- whether any cross-condition monitor-evidence pooling is scientifically admissible;
- threshold sensitivity and adverse-condition experiments;
- causal correction for feedback starvation / selection bias outside the full-label
  synthetic contract (diagnostics are implemented; correction remains open);
- integration with the generic research evaluation harness;
- independent implementation and QA;
- any claim about phenomenal metacognition, self-awareness or consciousness.

```text
DEFERRED_TO_QA = REPO_WIDE_TESTS / MATRIX / COVERAGE / TYPE_AUDIT / SECURITY_AUDIT
```
