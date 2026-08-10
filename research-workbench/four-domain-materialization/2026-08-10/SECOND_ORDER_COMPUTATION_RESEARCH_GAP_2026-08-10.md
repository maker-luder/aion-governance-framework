# Second-Order Computation Research Gap — 2026-08-10

```text
STATUS = OPEN_RESEARCH_GAP
EXECUTABLE_CANDIDATE = NOT_IMPLEMENTED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```

## Why this gap exists

The current research line separates three levels:

```text
LEVEL 1 — representation of self-relevant / self-other state
LEVEL 2 — first-order functional self-model
LEVEL 3 — computation about the reliability/performance of the first-order mechanism itself
```

Level 1 is represented by reviewed research candidates such as the metacognitive self-state and self/other boundary reworks.

Level 2 is implemented on this research branch by the finite predictive self-model and matched self-model ablation experiment.

Level 3 remains open.

## Existing Level-1 source

`review/metacognitive-self-state-rework@638dcb46136d879ed16ff7dfe2d260ac2eed734b` explicitly reports:

```text
METACOGNITIVE_STATE_REPRESENTATION = IMPLEMENTED
METACOGNITIVE_COMPUTATION = NOT_IMPLEMENTED
```

Its remaining hold includes:

- prediction-error-driven confidence calibration;
- inferred uncertainty updates;
- strategy adaptation from monitored error;
- second-order estimate of self-model reliability.

The Level-3 gap must not duplicate the Level-1 state representation.

## Existing Level-2 source

`review/four-domain-research-materialization@d219b76e38844c9b4487b2e93fc5e1819f720131` contains the finite predictive self-model research line with matched:

```text
SELF_MODEL_PRESENT
SELF_MODEL_ABLATED
SELF_MODEL_RANDOMIZED
SELF_MODEL_STALE
```

The first-order model maintains a bounded capability estimate, predicts success as a boolean relation to task difficulty, and selects `COMMIT / DEFER` using a risk buffer.

Important semantic lock:

```text
CAPABILITY_ESTIMATE != SUCCESS_PROBABILITY
```

A second-order mechanism must not reinterpret the first-order capability estimate as a calibrated probability unless a separate probability contract is added and validated.

## Narrow research question

A valid Level-3 question is narrower than “does the system have metacognition?”

Candidate form:

> Can a causally valid second-order mechanism derive an auditable performance/reliability signal from prior first-order prediction/action/outcome evidence and use that signal to alter downstream treatment of the first-order model under matched controls?

The answer may be negative.

```text
NULL_RESULT = VALID_RESULT
```

## Measurement requirements

A future candidate must define exactly what it measures.

For example, if real deployment only observes outcomes after `COMMIT`, then:

```text
OBSERVED_COMMIT_SUCCESS_RATE
= P(success | COMMIT, observed decision policy)
```

and therefore:

```text
OBSERVED_COMMIT_SUCCESS_RATE != GENERAL_PREDICTION_RELIABILITY
OBSERVED_COMMIT_SUCCESS_RATE != GLOBAL_MODEL_RELIABILITY
OBSERVED_COMMIT_SUCCESS_RATE != PREDICTION_CALIBRATION
```

A future full prediction-reliability experiment would require an explicit external benchmark/counterfactual outcome contract rather than silently treating missing `DEFER` outcomes as failures or zeros.

## Causal requirements

For online trial `t`:

```text
prior history < t
    -> derive second-order signal_t
    -> apply modulation_t
    -> action_t fixed
    -> outcome_t observed
    -> append evidence_t
    -> updated signal available for t+1
```

Hard invariant:

```text
OUTCOME_t MUST NOT AFFECT ACTION_t
```

No lookahead, target leakage, future-data leakage, or hidden outcome access is permitted.

## Source-of-truth requirements

A future implementation should use an immutable, explicit trial/evidence record as the scientific source of truth rather than manually supplied summary counters.

Relevant fields may include:

- run reference;
- subject/context/model reference;
- trial reference and sequence index;
- first-order prediction;
- action;
- observed outcome or explicit missing status;
- evidence refs;
- provenance refs.

All derived rates/counts should be deterministically recomputable from the stored records.

## Control requirements

A Level-3 functional candidate may use matched controls such as:

```text
SECOND_ORDER_PRESENT
SECOND_ORDER_ABLATED
SECOND_ORDER_RANDOMIZED
SECOND_ORDER_STALE
```

Only if all conditions:

- use the same task sequence and baseline first-order mechanism;
- receive isolated mutable first-order instances;
- differ only in the second-order condition;
- preserve causal timing;
- accept null or harmful results.

Ablation is a causal experiment, not deletion of a stored field.

## Selection / feedback limitation

If second-order caution reduces `COMMIT`, then fewer future outcomes become observable. This can change both the second-order evidence stream and the first-order learning trajectory.

Therefore:

```text
SECOND_ORDER_DIRECT_EFFECT_ISOLATION = NOT_ESTABLISHED
FEEDBACK_STARVATION_CORRECTION = NOT_IMPLEMENTED
```

A first candidate should expose this limitation instead of adding arbitrary smoothing or priors solely to make the mechanism appear successful.

## Rejected partial build attempt

An external-agent partial build on:

`review/second-order-commit-performance-monitor-candidate`

was independently reviewed and rejected as an implementation candidate. The branch head was returned to a tree with no file difference from its approved base while preserving audit history.

Disposition:

```text
PARTIAL_IMPLEMENTATION = REJECTED
USEFUL_CONCEPTS = CONCEPTUAL_SALVAGE_ONLY
EXECUTABLE_LEVEL_3_CANDIDATE = NOT_IMPLEMENTED
```

Useful lessons retained from the review include:

- environment-provided outcomes rather than private-model hidden state;
- success-rate / prediction-reliability separation;
- explicit missing-outcome semantics;
- source-of-truth trial records;
- anti-lookahead tests;
- condition isolation;
- precise modulation direction.

No code from that attempt is promoted by this record.

## Scientific non-claims

```text
SECOND_ORDER_SIGNAL != METACOGNITIVE_FEELING
SECOND_ORDER_SIGNAL != SELF_AWARENESS
SECOND_ORDER_FUNCTIONAL_EFFECT != CONSCIOUSNESS
SECOND_ORDER_FUNCTIONAL_EFFECT != PHENOMENAL_EXPERIENCE
SECOND_ORDER_MONITOR != PERSONAL_IDENTITY
SECOND_ORDER_MODULATION != ACTION_AUTHORITY
```

## Promotion boundary

This record only materializes the gap and design constraints.

```text
RESEARCH_GAP_MATERIALIZED = YES
IMPLEMENTATION_PROMOTED = NO
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
```
