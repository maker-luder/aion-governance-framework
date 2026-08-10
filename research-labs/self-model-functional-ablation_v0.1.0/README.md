# Self-Model Functional Ablation — v0.1.0

Status: `RESEARCH_MODEL / CANONICAL_EFFECT=NONE / MAIN_EFFECT=NONE`

This lab contains an actual executable computational model, not only a governance rule.

## Model

`FinitePredictiveSelfModel` maintains a bounded estimate of its own task capability from
matched success/failure observations. The estimate can causally affect whether the model
commits to or defers a later task.

The model is intentionally finite and inspectable:

```text
prior capability estimate
        +
observed successes -> lower capability bound
observed failures  -> upper capability bound
        ↓
bounded point estimate
        ↓
prospective success prediction
        ↓
COMMIT / DEFER
```

It does not model phenomenal experience, personal identity, qualia, or consciousness.

## Matched ablation conditions

The same task sequence and hidden capability are evaluated under:

```text
SELF_MODEL_PRESENT
SELF_MODEL_ABLATED
SELF_MODEL_RANDOMIZED
SELF_MODEL_STALE
```

- `PRESENT`: history updates the bounded self-model and can change later action.
- `ABLATED`: the self-model is removed; the runner commits without capability-state guidance.
- `RANDOMIZED`: a deterministic pseudo-random estimate replaces history-dependent state.
- `STALE`: the initial estimate remains frozen and cannot learn from disconfirming evidence.

## Default benchmark

The built-in fixture has a calibration phase followed by a transfer phase. All conditions
receive the same tasks and latent capability. Outcomes are deterministic.

A positive result can establish only:

```text
SELF_MODEL_FUNCTIONAL_CONTRIBUTION_CANDIDATE
```

Hard non-claims:

```text
SELF_MODEL_FUNCTIONAL_UTILITY != SUBJECTIVITY
SELF_MODEL_CAUSAL_CONTRIBUTION != CONSCIOUSNESS
SELF_MODEL_ABLATION_EFFECT != PHENOMENAL_SELF
NULL_RESULT = VALID_RESULT
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```

## External research stimulus

The research question was sharpened by public consciousness-related projects discussed in
the external intake, especially self-model ablation and transfer-style methodology. Their
theories and implementations are not treated as authority and are not copied here. This is
a clean-room AION research model.

## Run

```bash
python -m pip install -e .
python -m compileall -q src
python -m pytest -q
python scripts/run_demo.py
```

## Provenance

- Human Research Owner: requested direct research-branch growth and specifically asked to see a model rather than only governance adjustment.
- ChatGPT: selected the finite predictive self-model formulation, designed the matched ablation conditions, implemented the clean-room model, benchmark, tests, and CI integration.
- External projects: methodological stimulus only.
- Codex: no contribution to v0.1.0 unless separately documented.
