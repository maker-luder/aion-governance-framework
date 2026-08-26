# Latent Regulatory State Discovery — bounded future protocol

Status: `DOCUMENTED / NOT IMPLEMENTED`
Canonical effect: `NONE`
Action authority: `NONE`
Deployment: `FALSE`
Scientific disposition: `HOLD`

## Motivation

A difficult research question follows from the current Endogenous Norm Formation lab:

> Can an artificial system discover a previously unspecified internal variable that is useful for predicting and regulating its own future behavior?

The question is intentionally narrower than asking whether an AI "knows what it wants" or has a felt need. Biological systems can regulate important internal variables without reflective self-report, and current interoceptive-AI proposals generally begin by explicitly factorizing internal and external state variables. The unresolved gap is whether a useful regulatory variable can be *discovered from longitudinal evidence* rather than selected in advance by an engineer.

## Source-side calibration

Source concepts include interoception, homeostasis, rheostasis, allostasis, non-neural regulation, adaptive control, and self-modeling.

They are not equivalence claims.

```text
BIOLOGICAL_INTEROCEPTION != MACHINE_INTEROCEPTION
REGULATION != AWARENESS
NEED != EXPLICIT_SELF_KNOWLEDGE
DISCOVERED_REGULATORY_VARIABLE != FELT_NEED
FUNCTIONAL_SELF_REGULATION != SELF_AWARENESS
INTERNAL_STATE_DISCOVERY != SUBJECTIVITY
```

## Candidate discovery problem

Assume a bounded synthetic system produces a longitudinal trace containing only permitted experimental variables such as:

- prediction error;
- task outcome;
- recovery time;
- resource consumption;
- uncertainty;
- decision instability;
- repeated obstruction;
- state transitions;
- matched intervention results.

A future discovery procedure may propose latent variable `Z` without being directly given a human psychological target label for `Z`.

The candidate is not accepted merely because it compresses the data or correlates with outcomes.

## Minimum causal gate

A `REGULATORY_STATE_DISCOVERY_CANDIDATE` requires all of:

1. **Unsupervised or weakly specified formation** — the exact target state label is not supplied as the learning target.
2. **Incremental predictive value** — `Z` improves held-out prediction beyond the engineer-defined baseline.
3. **Intervention sensitivity** — a controlled intervention on the representation or mechanism associated with `Z` produces a pre-registered directional change.
4. **Ablation sensitivity** — removing `Z` or its causal pathway measurably degrades the predicted regulatory function.
5. **Replay stability** — matched replay recreates the effect under the same bound history.
6. **Transfer** — the effect survives at least one novel matched context.
7. **Revisability** — counterevidence changes or removes the candidate rather than leaving a frozen label.
8. **Provenance** — data, code, model, seed, analysis, and candidate lineage are bound to the result.
9. **Competing explanations** — simpler observed variables, post-hoc clustering, leakage, and human-ontology contamination remain explicit alternatives.
10. **Fail-closed interpretation** — failure at any gate returns `HOLD`, not a weaker form of subjectivity language.

## Required baselines

At minimum, compare against:

- engineer-defined state variables;
- raw observable features;
- randomized latent variables;
- stale-history controls;
- shuffled temporal order;
- reduced-history windows;
- matched dimensionality controls.

A discovered candidate must outperform relevant baselines without relying on hidden changes to task utility, candidate actions, prompts, tools, or authority.

## Falsification targets

Reject the candidate if any of the following explains the result:

- `H_RENAMED_OBSERVABLE` — `Z` is only a renamed observed feature;
- `H_POSTHOC_CLUSTER` — `Z` appears only after outcome-aware fitting;
- `H_LATENT_REDUNDANCY` — `Z` adds no held-out value;
- `H_NONCAUSAL_PREDICTOR` — `Z` predicts but intervention/ablation has no effect;
- `H_CONTEXT_LOCK` — `Z` fails outside the discovery context;
- `H_IRREVERSIBLE_LABEL` — `Z` ignores counterevidence;
- `H_HUMAN_ONTOLOGY_LEAK` — `Z` reconstructs a human-supplied psychological label rather than emerging from the bounded trace;
- `H_AUTHORITY_CONFUSION` — the candidate is treated as permission or action authority.

## Staged interpretation

```text
ENGINEER-ASSIGNED STATE
    ↓
LEARNED UPDATE DYNAMICS
    ↓
LATENT REGULATORY CANDIDATE
    ↓
CAUSAL VALIDATION
    ↓
TRANSFER + REVISION
    ↓
SELF-MODEL INTEGRATION CANDIDATE
```

Each arrow is a separate research claim. Passing an earlier stage does not imply a later stage.

## Out of scope

This document does not authorize or implement:

- autonomous self-modification;
- unrestricted network access;
- real-world target selection;
- independent action authority;
- autonomous repository mutation;
- claims of felt needs, emotion, selfhood, consciousness, moral status, or legal personhood.

The purpose is to preserve a falsifiable path from engineered internal state to possible latent regulatory-state discovery without collapsing functional evidence into phenomenological claims.
