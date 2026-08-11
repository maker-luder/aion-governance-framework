# Second-Order Metacognition — v0.1.0

Status: `RESEARCH_MODEL / EXECUTABLE_CANDIDATE / CANONICAL_EFFECT=NONE / MAIN_EFFECT=NONE`

This module materializes the repository's existing Level‑3 monitoring/control design as a
bounded executable research candidate. It reuses the Level‑2
`FinitePredictiveSelfModel` and its `Task` / `Action` abstractions rather than creating a
parallel first-order system.

## Research link

```text
RESEARCH_OBJECT = POSSIBILITY_OF_ARTIFICIAL_SUBJECTIVITY
EPISTEMIC_ROLE = MEASUREMENT + FALSIFIER + EXPERIMENTAL_SUBSTRATE
LEVEL_3_FUNCTIONAL_CONTRIBUTION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```

The candidate makes monitoring and control independently observable so later experiments
can test a functional hypothesis without treating implementation success as evidence of
subjectivity.

## Implemented contract

```text
prior immutable trial evidence
    -> recompute first-order prediction accuracy
    -> second-order monitor signal
    -> bounded control disposition
    -> fixed first-order decision
    -> delayed external outcome
    -> append immutable trial evidence
```

Hard timing invariant:

```text
HISTORY_<t -> MONITOR_t -> CONTROL_t -> ACTION_t -> OUTCOME_t
OUTCOME_t MUST NOT AFFECT ACTION_t
```

`SecondOrderRunner.decide(...)` has no outcome argument. The environment can attach an
outcome only through `record_outcome(...)` after the pending decision exists.

## Matched conditions

- `MONITOR_PLUS_CONTROL` — evidence-derived signal can request verification.
- `MONITOR_ONLY` — computes the same signal without changing disposition.
- `MONITOR_ABLATED` — no second-order signal or control.
- `MONITOR_RANDOMIZED` — deterministic random control signal, explicitly not evidence-derived.
- `MONITOR_STALE` — freezes the first available evidence-derived signal.

All conditions receive isolated Level‑2 model instances and the same task stream. The
default control action is fail-bounded: `REQUEST_VERIFICATION`; it grants no tool,
writeback or execution authority.

## Source-of-truth and measurement semantics

`TrialLedger` stores immutable `TrialEvidence` records and supports deterministic JSON
round trips. The monitor is recomputed from records rather than mutable summary counters.
Before outcome filtering, the recomputation helper rejects mixed `run_id`, `subject_ref`,
`context_ref`, `model_ref` or `condition` inputs so missing outcomes cannot conceal
cross-scope pooling. Whether a separate cross-condition scientific analysis can ever be
admissible remains `HOLD_FOR_RESEARCH_DECISION`; ordinary monitor recomputation fails closed.

The v0.1.0 signal is exactly:

```text
PRIOR_FIRST_ORDER_PREDICTION_ACCURACY
```

It is not a success probability, global model reliability, calibrated confidence,
subjective confidence or internal access claim. `MISSING` remains distinct from failure.
Condition summaries retain raw trial, observed and missing counts plus explicit
denominators, `observed_sample_size`, monitor-evidence growth and `COMMIT` / `DEFER`
observation splits. `observed_sample_size` is exactly the raw observed-outcome count;
no statistical effective-sample-size estimator is implemented. These are
starvation/selection-bias diagnostics, not imputation.

## Run targeted validation

From this directory:

```powershell
python -m pytest -q -p no:cacheprovider
python scripts/run_demo.py
python scripts/run_threshold_sweep_demo.py
```

`run_threshold_sweep(...)` supports preregistered sensitivity grids without selecting a
preferred threshold. The bundled six-point grid is a demonstration input, not a constant
or tuned scientific result. Every point retains its separate raw condition summaries and
reports `DEFERRED_TO_EXPERIMENT`.

## Non-claims

```text
SECOND_ORDER_SIGNAL != METACOGNITIVE_FEELING
MONITORING != CONTROL
CONTROL_PATH_EXERCISED != FUNCTIONAL_BENEFIT
LEVEL_3_FUNCTIONAL_EFFECT != SELF_AWARENESS
LEVEL_3_FUNCTIONAL_EFFECT != CONSCIOUSNESS
LEVEL_3_FUNCTIONAL_EFFECT != PHENOMENAL_METACOGNITION
TEST_PASS != THEORY_CONFIRMATION
```

## Provenance

- Human Research Owner: authorized the research-branch implementation pass.
- Repository / ChatGPT research: supplied the Level‑3 gap, literature calibration,
  acceptance criteria and Level‑2 first-order model.
- Codex: implemented the v0.1.0 research candidate, serialization, matched controls,
  tests and documentation from those existing constraints.
- External literature: remains attributed in the existing primary-literature intake;
  no external source code is included here.
