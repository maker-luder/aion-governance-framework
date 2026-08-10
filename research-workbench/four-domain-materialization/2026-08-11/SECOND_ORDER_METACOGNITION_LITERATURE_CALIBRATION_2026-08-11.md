# Second-Order Metacognition Literature Calibration — 2026-08-11

```text
STATUS = RESEARCH_CALIBRATION
BASE_GAP = SECOND_ORDER_COMPUTATION_RESEARCH_GAP_2026-08-10
EXECUTABLE_CANDIDATE = NOT_IMPLEMENTED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```

## Purpose

The 2026-08-10 Level-3 gap asked whether a second-order mechanism can derive an auditable reliability/performance signal from prior first-order evidence and use that signal to alter downstream treatment of the first-order model.

Primary research located on 2026-08-11 sharpens that question without closing it.

See `PRIMARY_LITERATURE_INTAKE_2026-08-11.md` for source provenance.

## Literature-aligned decomposition

The 2026 metacognition review by Liu et al. describes a loop with two distinct processes:

```text
MONITORING
    -> estimate uncertainty / performance / progress

CONTROL
    -> change planning / strategy / effort based on monitoring
```

This maps cleanly onto the existing AION three-level distinction only if Level 3 requires **both** an independently evaluated monitor and a causally linked control effect.

Therefore:

```text
SECOND_ORDER_STATE_ONLY != LEVEL_3_FUNCTION
MONITORING_WITHOUT_CONTROL = PARTIAL_LEVEL_3_CANDIDATE
CONTROL_WITHOUT_VALID_MONITOR = UNGROUNDED_CONTROL
MONITORING_PLUS_CONTROL_WITHOUT_CAUSAL_TEST = NOT_ESTABLISHED
```

## Decouple first-order and second-order quality

The AAAI DMC work explicitly motivates separating metacognitive measurement from ordinary task performance. The AION Level-3 experiment should therefore never infer metacognitive quality from a stronger first-order model alone.

```text
TASK_ACCURACY_t = TYPE_1_SIGNAL
MONITOR_QUALITY_t = TYPE_2_SIGNAL
TYPE_1_IMPROVEMENT != TYPE_2_IMPROVEMENT
```

Candidate monitor evaluation should use external outcome/correctness evidence rather than self-description alone.

Possible measures include:

```text
failure_prediction_accuracy
confidence_correctness_separation
calibration_error
sensitivity_to_correct_vs_incorrect_trials
```

The project does not commit to any single metric before fixture design and semantic review.

## Verification is a separate capability

Chen et al. (2026) report that stronger generation does not automatically imply stronger self-verification and formulate generation and verification as distinct objectives.

AION research consequence:

```text
FIRST_ORDER_GENERATION != SECOND_ORDER_VERIFICATION
```

A Level-3 candidate should therefore include trials where first-order performance is held as constant as practicable while the second-order monitor/control condition changes.

## Internal-activation evidence is bounded

Li et al. (NeurIPS 2025) report experimentally measurable monitoring/control over selected internal activation directions, while also finding that the accessible metacognitive space is much smaller than the full neural space.

AION interpretation:

```text
MONITORABLE_INTERNAL_SUBSET != GLOBAL_SELF_ACCESS
INTERNAL_ACTIVATION_CONTROL != SELF_AWARENESS
```

Because the same work raises safety concerns about oversight evasion, this calibration does **not** authorize a neural-activation-control implementation. Internal-activation experiments remain optional external evidence, not a required AION route.

## Minimal Level-3 acceptance criteria

A future executable Level-3 candidate should satisfy all of the following before the project calls it a second-order functional contribution candidate.

### L3-01 — Explicit first-order target

The monitored first-order mechanism must be named and bounded.

### L3-02 — Independent monitoring signal

The second-order signal must be computed from evidence available before the downstream control decision and must be evaluated against later external outcome/correctness evidence.

### L3-03 — No task-performance substitution

Raw first-order success or model scale cannot be used as proof of second-order quality.

### L3-04 — Causal control path

The monitor signal must alter a defined downstream variable such as defer threshold, verification request, evidence request or strategy selection.

### L3-05 — Anti-lookahead timing

```text
HISTORY_<t
    -> MONITOR_t
    -> CONTROL_t
    -> ACTION_t
    -> OUTCOME_t
```

`OUTCOME_t` must not affect `MONITOR_t`, `CONTROL_t` or `ACTION_t`.

### L3-06 — Matched controls

At minimum, consider:

```text
MONITOR_PLUS_CONTROL
MONITOR_ONLY
MONITOR_ABLATED
MONITOR_RANDOMIZED
MONITOR_STALE
```

The first-order task stream must be matched across conditions as closely as the experimental design permits.

### L3-07 — Separate monitoring and control effects

If `MONITOR_ONLY` improves reported confidence but not behavior, that is still informative and must not be relabeled as a control effect.

### L3-08 — Null and harmful results accepted

```text
NO_EFFECT = VALID_RESULT
NEGATIVE_EFFECT = VALID_RESULT
```

### L3-09 — No verbal self-report shortcut

Natural-language self-description alone is not sufficient evidence for the monitor.

### L3-10 — No subjectivity promotion

```text
LEVEL_3_FUNCTIONAL_EFFECT != SELF_AWARENESS
LEVEL_3_FUNCTIONAL_EFFECT != CONSCIOUSNESS
LEVEL_3_FUNCTIONAL_EFFECT != PHENOMENAL_METACOGNITION
```

## Candidate experiment skeleton

A future synthetic fixture may use externally scoreable tasks with delayed outcome labels.

```text
trial input
    -> first-order prediction
    -> second-order monitor estimate
    -> control decision
    -> first-order action
    -> external correctness/outcome label
    -> immutable trial record
```

The trial record should make it possible to recompute every second-order metric without relying on mutable summary counters.

Possible control actions remain bounded:

```text
ACCEPT
REQUEST_VERIFICATION
REQUEST_MORE_EVIDENCE
DEFER
```

No unrestricted tool-use authority is implied.

## Measurement caution

Confidence magnitude is not enough. A system that says `0.9` frequently may simply be overconfident.

The research question is whether the monitor distinguishes conditions in a way that tracks external correctness and then supports a causally measurable control effect.

```text
CONFIDENCE_LEVEL != METACOGNITIVE_SENSITIVITY
CALIBRATION != CAUSAL_CONTROL
MONITORING != CONTROL
```

## Relationship to the existing 2026-08-10 gap

This document does not rewrite the historical gap. It adds literature-grounded acceptance constraints to the next candidate cycle.

```text
2026-08-10 = GAP_DEFINITION_AND_IQC_LESSONS
2026-08-11 = PRIMARY_LITERATURE_CALIBRATION
NEXT = OPTIONAL_EXECUTABLE_CANDIDATE_AFTER_REVIEW
```

## Non-claims

```text
METACOGNITIVE_METRIC != SUBJECTIVE_EXPERIENCE
SELF_VERIFICATION != INTROSPECTIVE_ACCESS
INTERNAL_ACTIVATION_MONITORING != FULL_SELF_MODEL
SECOND_ORDER_CONTROL != AUTONOMOUS_AUTHORITY
LITERATURE_CONSISTENCY != REPLICATION
```
