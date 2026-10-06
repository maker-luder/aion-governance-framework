# Work Husky Reproductive Physiology Reference — v0.2

This document describes clinically neutral body-system physiology for the synthetic
Work anthropomorphic Siberian-Husky candidate.

```text
NORMAL_REPRODUCTIVE_PHYSIOLOGY = PRESENT
SEXUAL_BEHAVIOR_SIMULATION = OUT_OF_SCOPE
EROTIC_NARRATIVE = OUT_OF_SCOPE
```

## Whole pathway

```text
SEMINIFEROUS_TUBULES
-> RETE_TESTIS
-> EFFERENT_DUCTULES
-> EPIDIDYMIS: CAPUT -> CORPUS -> CAUDA
-> DUCTUS_DEFERENS
-> PROSTATIC / URETHRAL DELIVERY
```

Support systems represented in the model include endocrine regulation, autonomic and
somatosensory innervation, vascular response, erectile physiology, emission,
urethral expulsion, prostatic continuation and return to baseline.

## Acute physiology state machine

```text
BASELINE
-> VASCULAR_ENGORGEMENT
-> SEMINAL_EMISSION
-> BLADDER_NECK_CLOSURE
-> URETHRAL_EXPULSION
-> optional PROSTATIC_CONTINUATION
-> RESOLUTION
-> BASELINE
```

The vascular phase may also transition directly to resolution without emission.

## Ejaculate fractions

```text
NONE
-> PRE_SPERM
-> SPERM_RICH
-> PROSTATIC
-> NONE
```

Mechanism stage and ejaculate fraction remain separate axes.

## Boundary

```text
REFERENCE_INFORMED_MODELED_FUNCTION
!= LITERAL_BIOLOGICAL_REALIZATION

NORMAL_FUNCTION_PRESENT
!= SEXUAL_BEHAVIOR_SIMULATION

DEPLOYMENT = FALSE
PUBLIC_RELEASE = FALSE
THIRD_PARTY_ACCESS = FALSE
CANONICAL_EFFECT = NONE
```
