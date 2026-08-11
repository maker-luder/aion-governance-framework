# Experiment Spec — Second-Order Metacognition v0.1.0

## Narrow question

Can an auditable signal derived only from prior first-order prediction/outcome evidence
alter a bounded downstream verification disposition under matched controls?

The answer may be null or harmful. v0.1.0 establishes an executable experiment contract,
not a positive scientific conclusion.

## Reused first-order target

```text
TARGET = research-labs/self-model-functional-ablation_v0.1.0
MODEL = FinitePredictiveSelfModel
CAPABILITY_ESTIMATE != SUCCESS_PROBABILITY
```

The first-order model, task stream, latent benchmark capability and model update rule are
held constant across second-order conditions.

## Independent variable

`SecondOrderCondition`:

```text
MONITOR_PLUS_CONTROL
MONITOR_ONLY
MONITOR_ABLATED
MONITOR_RANDOMIZED
MONITOR_STALE
```

## Evidence contract

Each `TrialEvidence` record includes:

- run / subject / context / model references;
- trial ID and sequence index;
- first-order estimate, prediction and action;
- second-order signal and its exact prior evidence boundary;
- control disposition;
- observed or explicitly missing external outcome;
- evidence and provenance references.

Records are append-only within `TrialLedger`. Every monitor value can be recomputed from
the records named by `source_trial_ids`.

Standalone recomputation rejects evidence mixed across run, subject, context, model or
condition before it filters observed outcomes. A separate scientific cross-condition
analysis remains a research-design HOLD; the ordinary monitor path fails closed.

## Outcome contracts

- `EXTERNAL_BENCHMARK_FULL_LABELS`: the synthetic benchmark supplies a delayed label for
  every task, including a task the first-order model would defer. This permits direct
  evaluation of categorical prediction correctness.
- `COMMIT_ONLY`: deferred trials remain `MISSING`; they are excluded from observed rates
  and are never converted to failures.

These two contracts must not be pooled without an explicit analysis rule.

## Measures

- first-order categorical prediction accuracy;
- monitor coverage;
- monitor classification accuracy at the preregistered verification threshold;
- verification-request count;
- missing-outcome count;
- observed and missing fractions with raw trial/observed/missing counts;
- observed sample size, defined as the raw observed-outcome count;
- monitor evidence growth, operationalized as the maximum number of prior observed
  records used by an evidence-derived signal;
- observed-outcome counts and denominators split by first-order `COMMIT` / `DEFER`;
- anti-lookahead validity.

The monitor value is a historical categorical-accuracy rate. It is not named or interpreted
as calibration error, success probability or global reliability.

These diagnostics expose feedback starvation and action-conditioned missingness. They do
not impute outcomes or correct selection, survivorship or self-confirming-calibration bias.
No statistical effective-sample-size estimator is implemented.

## Causal checks

1. `decide(...)` has no current-outcome input.
2. Each signal's evidence boundary is strictly earlier than the current sequence.
3. `MONITOR_PLUS_CONTROL` and `MONITOR_ONLY` receive matching signal histories.
4. Only the control-enabled condition may convert a low signal into
   `REQUEST_VERIFICATION`.
5. First-order predictions/actions remain matched across conditions.

## Acceptance boundary

Passing the implementation tests establishes only that the experiment contract is
executable and internally checks its declared invariants.

```text
EXECUTABLE_LEVEL_3_CANDIDATE = IMPLEMENTED
CONTROL_PATH_EXERCISED = MEASURABLE
LEVEL_3_FUNCTIONAL_CONTRIBUTION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
```

Independent reruns, alternative fixtures, threshold sensitivity, adverse cases and formal
analysis remain later QA/research work.

## Threshold sensitivity substrate

`run_threshold_sweep(...)` repeats the complete matched experiment over an explicit,
unique, bounded threshold grid. It reuses one immutable task tuple for every point and
does not alter the first-order model, task stream or outcome timing. Results remain
separate by threshold; no aggregate score, preferred threshold or benefit claim is
computed. Executing the full preregistered study remains `DEFERRED_TO_EXPERIMENT`.
