# Provenance and Evidence Matrix — v0.2.1

## Rule

```text
ORGAN_EXISTENCE != SPECIES_SPECIFIC_DIMENSION
SPECIES_SPECIFIC_DIMENSION_UNKNOWN != ORGAN_ABSENT
PHYSIOLOGY_REFERENCE_IMPLEMENTED != LITERAL_BIOLOGICAL_REALIZATION
```

| Component | Evidence class | Repository treatment |
| --- | --- | --- |
| scrotum / scrotal skin | direct brown-bear | required topology |
| testes | direct brown-bear | required topology; dimensions separately evidenced |
| epididymis caput/corpus/cauda | direct brown-bear | required topology |
| spermatic cord | direct brown-bear | required topology |
| ductus deferens | direct brown-bear reproductive context | required topology |
| ampullae ductus deferentis | comparative ursid | required topology; no invented dimensions |
| prostate | comparative ursid + brown-bear seminal context | required topology; no invented dimensions |
| penile urethra | direct brown-bear catheterization | required topology |
| penis | direct brown-bear | required topology |
| prepuce | direct brown-bear semen-collection method | required topology |
| glans penis | comparative carnivoran | required topology; no invented dimensions |
| corpus cavernosum / os penis | direct brown-bear | required topology |
| seasonal reproductive cycle | direct brown-bear/grizzly literature | implemented physiology reference |
| spermatogenesis / epididymal maturation / sperm transport | direct brown-bear reproductive literature | implemented physiology reference |
| erection / ejaculation | direct brown-bear electroejaculation observations | implemented physiology reference |
| semen characteristics | Hokkaido brown-bear study | external reference, not universal mean |

## Validation philosophy

v0.2.0 required exact topology equality. v0.2.1 changes this to a minimum-required set:

```text
REQUIRED_STRUCTURES subset-of candidate.reproductive_topology
```

This prevents accidental deletion of established anatomy while allowing future source-supported extension.

## Removed hard locks

The following are no longer core anatomy fields:

```text
LIVE_REPRODUCTIVE_FUNCTION = NOT_IMPLEMENTED
SEXUAL_BEHAVIOR_SIMULATION = NOT_IMPLEMENTED
BODY_SENSATION = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
ACTION_AUTHORITY = NONE
```

Reason: they are not required to represent adult male brown-bear anatomy and were over-constraining the model.

## Retained epistemic boundaries

```text
BIOLOGICAL_REALIZATION = FALSE
FERTILITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

These are claim controls, not anatomical omissions.
