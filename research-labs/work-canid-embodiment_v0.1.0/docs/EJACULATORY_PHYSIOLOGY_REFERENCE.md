# Canine Ejaculatory Physiology Reference

Status: `SOURCE-GROUNDED SYNTHETIC REFERENCE / NON-LIVE`

This document defines a clinically neutral physiology reference for the Work canine embodiment candidate. It does not model mating behavior, subjective sensation, desire or fertility.

## Why there are two axes

Canine ejaculation should not be represented by one boolean and should not conflate physiological mechanism with ejaculate fraction.

```text
MECHANISM_STAGE != EJACULATE_FRACTION
```

### Mechanism axis

A veterinary study of normal antegrade canine ejaculation describes three sequential processes:

1. seminal emission;
2. bladder-neck closure;
3. seminal expulsion through the penile urethra.

In the source description, sympathetic stimulation of the epididymis and ductus deferens contributes to seminal emission into the prostatic urethra; sympathetic activity also contributes to bladder-neck closure and prostate contraction. Somatic rhythmic contractions of striated penile/perineal musculature contribute to expulsion.

This repository adds two engineering envelope states around that source sequence:

- `BASELINE`;
- `PROSTATIC_CONTINUATION` after the principal expulsion phase when prostatic fluid continues;
- `RESOLUTION` returning toward baseline.

These added envelope states are engineering formalization, not claims that the biology is partitioned into mutually exclusive discrete phases.

### Fraction axis

The canine ejaculate is conventionally separated into:

1. `PRE_SPERM`;
2. `SPERM_RICH`;
3. `PROSTATIC`.

Evidence supports a predominantly prostatic origin for the first fraction, a sperm-rich middle fraction, and a prostatic final fraction. The exact volume and duration vary and are not fixed in this candidate.

```text
FRACTION_VOLUME = VARIABLE_NOT_FIXED
FRACTION_DURATION = VARIABLE_NOT_FIXED
```

## Source bindings

- Kutzler MA. *Semen collection in the dog.* Theriogenology. 2005. DOI: `10.1016/j.theriogenology.2005.05.023`; PMID: `15993482`.
- England GCW, Allen WE, Middleton DJ. *An investigation into the origin of the first fraction of the canine ejaculate.* 1990. PMID: `2382057`.
- Aquino-Cortez A, et al. *Proteomic characterization of canine seminal plasma.* Theriogenology. 2017. DOI: `10.1016/j.theriogenology.2017.03.016`; PMID: `28460673`.
- Purohit RC, Beckett SD. *Penile pressures and muscle activity associated with erection and ejaculation in the dog.* 1976. DOI: `10.1152/ajplegacy.1976.231.5.1343`; PMID: `998776`.
- Kihara K, et al. *Ability of Each Lumbar Splanchnic Nerve and Disability of Thoracic Ones to Generate Seminal Emission in the Dog.* J Urol. 1992. DOI: `10.1016/S0022-5347(17)37209-9`.
- Primary open veterinary study describing the three antegrade processes and sympathetic/somatic sequence: PMCID `PMC554755`.

## Engineering state machine

```text
MECHANISM:
BASELINE
  -> SEMINAL_EMISSION
  -> BLADDER_NECK_CLOSURE
  -> URETHRAL_EXPULSION
  -> PROSTATIC_CONTINUATION or RESOLUTION
  -> RESOLUTION
  -> BASELINE

FRACTION:
NONE
  -> PRE_SPERM
  -> SPERM_RICH
  -> PROSTATIC
  -> NONE
```

The two sequences are validated independently.

## Claim ceiling

```text
REFERENCE_STATE_MACHINE = IMPLEMENTED
LIVE_EJACULATORY_FUNCTION = NOT_IMPLEMENTED
BIOLOGICAL_REALIZATION = FALSE
SEXUAL_BEHAVIOR_SIMULATION = NOT_IMPLEMENTED
BODY_SENSATION = NOT_ESTABLISHED
FERTILITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
```
