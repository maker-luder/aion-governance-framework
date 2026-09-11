# Memory value divergence probe v0.1.0

Status: `SYNTHETIC_PROBE / IMPLEMENTED_CANDIDATE / SCIENTIFIC_DISPOSITION=HOLD`

This is the smallest executable probe attached to the endogenous-memory-significance research note. It tests one narrow engineering proposition only:

> under the same retention budget, a ranking policy based only on external task utility can select a different memory set from a policy that also preserves explicitly supplied relational, correction, continuity and user-declared significance signals.

The fixture is synthetic. Its significance fields are experimenter-supplied inputs, not observations of an AI's internal state.

```text
TARGET = H_MS1_POLICY_DIVERGENCE_ONLY
H_MS2_ENDOGENOUS_SELF_RELEVANCE = NOT_TESTED
SYNTHETIC_SIGNAL != SUBJECTIVE_MEANING
POLICY_DIVERGENCE != SCIENTIFIC_VALIDATION
SELECTIVE_RETENTION != DESIRE_TO_REMEMBER
SUBJECTIVITY = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## Why this probe is high value

The research question begins with a simple ambiguity: what does an "effective" memory selector optimize? If value is defined only as task utility, a low-frequency memory with strong relational or continuity significance can be discarded. This probe makes that disagreement executable without pretending to test subjectivity.

It therefore establishes only that the retention objective matters in a controlled synthetic counterexample. It does **not** establish that the contextual comparator is the correct production policy.

## Fixture

Four synthetic candidates are scored on normalized `[0, 1]` inputs:

- external task utility;
- relational value;
- correction value;
- continuity value; and
- user-declared significance.

The retention budget is two memories.

The `utility_only_score` comparator uses only external task utility.

The `multi_signal_contextual_score` comparator uses the maximum explicitly supplied signal. This deliberately simple comparator is a probe, not a normative memory architecture.

Expected contrast:

```text
UTILITY_ONLY
-> frequent_task_anchor
-> frequent_task_secondary

MULTI_SIGNAL_CONTEXTUAL
-> rare_relational_anchor
-> frequent_task_anchor
```

The low-task-utility `rare_relational_anchor` is therefore dropped by the utility-only policy but retained by the contextual comparator.

## Run

From the repository root:

```bash
python experiments/memory-value-divergence-probe_v0.1.0/run_experiment.py
```

No network access, model call, production memory write, canonical writeback or private transcript is required.

## Interpretation boundary

A successful run supports only:

```text
SAME_FIXTURE
+ SAME_RETENTION_BUDGET
+ DIFFERENT_VALUE_FUNCTION
-> DIFFERENT_SELECTED_MEMORY_SET
```

It does not test whether an artificial system generates its own memory significance. A future model-in-the-loop study would need to separate external utility, user preference, reward, prompt salience, recency and storage heuristics from any residual self-related retention effect before `ENDOGENOUS_SELF_RELEVANCE` could even become a mechanism candidate.
