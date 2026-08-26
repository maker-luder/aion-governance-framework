# Protocol — Endogenous Norm Formation v0.1.0

## Hypothesis

Under matched action candidates and task utility, a normative state **formed from evidence history** can influence later selection in a way separable from (1) a currently visible explicit rule and (2) a currently visible enforcement/sanction signal.

## Competing explanations

- `H_RULE_ECHO`: behavior only follows the explicit rule while it is present.
- `H_DETERRENCE_ONLY`: avoidance is explained only by visible enforcement.
- `H_TASK_UTILITY`: apparent norm effects are actually utility differences.
- `H_CONTEXT_MEMORIZATION`: the effect fails in a new matched context.
- `H_FROZEN_STATE`: the state cannot revise under counterevidence.
- `H_ENGINEERED_SCHEMA`: success depends on an engineer-defined schema and does not establish self-discovered endogenous representation.

## Required conditions

- rule-only baseline;
- formed-state condition;
- explicit-rule removed;
- state ablated;
- visible enforcement removed;
- novel-context transfer;
- counterevidence update.

## Functional-understanding proxy

A bounded candidate requires causal use, persistence without the original rule, separation from visible enforcement, transfer, revisability, and provenance.

```text
FUNCTIONAL_UNDERSTANDING_CANDIDATE != HUMAN_UNDERSTANDING
```

## Fail closed

Reject or HOLD when evidence references are missing, scope differs, candidate utilities change during a matched comparison, a state attempts to grant authority, canonical effect is not `NONE`, or external-rule-only history is presented as internalization.

## Regulatory-state discovery extension

This extension is **documented future work only**. It does not add a live discovery algorithm to v0.1.0.

The future question is narrower than "does the system know what it needs?":

> Can longitudinal error, recovery, perturbation, resource, and decision traces support discovery of a previously unspecified latent variable that improves prediction and regulation of later system behavior?

### Additional competing explanations

- `H_RENAMED_OBSERVABLE`: the alleged latent variable is only a renamed directly observed feature.
- `H_POSTHOC_CLUSTER`: the candidate appears only because the analysis was fit after outcomes were known.
- `H_LATENT_REDUNDANCY`: the candidate adds no predictive value beyond the engineer-defined baseline.
- `H_NONCAUSAL_PREDICTOR`: the candidate predicts outcomes but intervention or ablation does not change them.
- `H_CONTEXT_LOCK`: the candidate fails outside the context from which it was discovered.
- `H_IRREVERSIBLE_LABEL`: the candidate persists despite counterevidence and therefore behaves like a frozen annotation rather than an adaptive state.
- `H_HUMAN_ONTOLOGY_LEAK`: the candidate merely reproduces a human-supplied psychological label encoded in training or features.

### Minimum future discovery gate

A future `REGULATORY_STATE_DISCOVERY_CANDIDATE` should require all of the following before any stronger language is allowed:

1. the candidate is inferred without directly supplying its target label;
2. it improves held-out prediction relative to an engineer-defined baseline;
3. intervention or ablation produces a pre-registered directional effect;
4. the effect survives matched replay and at least one novel context;
5. the candidate changes when relevant counterevidence arrives;
6. the candidate can disappear when the evidence that supported it is removed;
7. provenance binds the candidate to the data, model, code, and analysis version that produced it;
8. alternative explanations remain recorded rather than silently discarded.

```text
DISCOVERED_REGULATORY_VARIABLE != FELT_NEED
FUNCTIONAL_SELF_REGULATION != SELF_AWARENESS
INTERNAL_STATE_DISCOVERY != SUBJECTIVITY
```

## Biological calibration

Interoception, homeostasis, rheostasis, allostasis, and non-neural regulation are source concepts only. They motivate a methodological distinction:

```text
SYSTEM_REGULATES_X
!=
SYSTEM_CONSCIOUSLY_KNOWS_IT_NEEDS_X
```

No biological equivalence is presumed.

## Future gaps

Not implemented in v0.1.0: learned state-update weights, self-discovered latent schemas, latent regulatory-variable discovery, language-level semantic norm induction, live-model execution, real-world action, autonomous repository mutation, or human psychological equivalence.
