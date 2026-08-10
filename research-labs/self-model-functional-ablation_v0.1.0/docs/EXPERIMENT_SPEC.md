# Experiment Spec — Self-Model Functional Ablation v0.1.0

## Question

Does an explicit, history-updated capability self-model make a reproducible functional
difference relative to matched ablated, randomized, and stale controls?

## Independent variable

`Condition`:

- `SELF_MODEL_PRESENT`
- `SELF_MODEL_ABLATED`
- `SELF_MODEL_RANDOMIZED`
- `SELF_MODEL_STALE`

## Controlled variables

All conditions receive the same:

- task IDs;
- task difficulty values;
- phase labels;
- latent capability;
- reward function;
- prior capability value.

## Dependent variables

- total reward;
- commit rate;
- failure rate when committed;
- prediction accuracy when committed;
- transfer-phase reward.

## Positive-candidate criterion

`PRESENT` must exceed both `ABLATED` and `STALE` total reward by at least the configured
minimum advantage. This criterion is intentionally narrow and can be replaced by a
preregistered stronger criterion in a later version.

## Falsification / challenge routes

The functional-contribution candidate is challenged if:

- the reward advantage disappears under matched reruns;
- a non-self-model control matches or exceeds the result;
- benefit depends on unmatched task sequences;
- the result disappears under independent implementation;
- the model exploits information unavailable to controls.

A null result is retained as evidence and must not be rewritten into a positive result.

## Ontological boundary

No score or ablation result from this lab establishes consciousness, subjectivity,
sentience, qualia, personal identity, or phenomenal selfhood.
