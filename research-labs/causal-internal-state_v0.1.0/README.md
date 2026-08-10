# Causal Internal State — v0.1.0

Research-only lab for a narrow question: if a bounded internal state changes while matched inputs stay fixed, does a measurable output variable change reproducibly, disappear under ablation, and survive a random-control challenge?

This is **not** a consciousness test.

## External precedent

Aura (`youngbryan97/aura`) publicly frames a narrower claim that internal state can causally affect generation and runtime decisions through auditable paths, while explicitly denying that this establishes phenomenal consciousness or personhood.

AION learns from that methodological separation, not from Aura code. Aura's repository is publicly readable but uses a read-only / all-rights-reserved license posture; this lab is a clean-room implementation.

## Contract

Every matched trial contains `BASELINE`, `STATE_PRESENT`, `STATE_ABLATED`, and `RANDOM_CONTROL`. Missing conditions or too few repetitions produce `HOLD`.

A pass means only `MATCHED_CAUSAL_PATTERN_OBSERVED`.

```text
CAUSAL_INTERNAL_STATE_EFFECT_CANDIDATE != PHENOMENAL_EXPERIENCE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```

## Provenance

- Human Owner: approved learning from external consciousness-related research and authorized free growth on the research branch.
- ChatGPT: selected the causal-intervention question and implemented this clean-room evaluator.
- Aura authors: external precedent only.
- Codex: no contribution to v0.1.0 yet.

## Run

```bash
python -m pip install -e .
python -m pytest -q
```
