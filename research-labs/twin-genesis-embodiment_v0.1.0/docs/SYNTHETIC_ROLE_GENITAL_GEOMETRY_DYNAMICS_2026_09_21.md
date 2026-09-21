# Synthetic role genital-geometry dynamics — 2026-09-21

Status: `ARCHIVAL_RESEARCH_CANDIDATE / UNMERGED`

This successor slice preserves the closed embodiment PRs and records a new bounded
synthetic geometry decision without rewriting their exact closure heads.

## Human Owner geometry adjustment

```text
CODEX
previous full-vascular = 12.60 cm length / 13.28 cm circumference
adjustment = move 1.00 cm from length to circumference
new full-vascular = 11.60 cm length / 14.28 cm circumference

CHATGPT_WORK
previous full-vascular = 13.32 cm length / 11.52 cm circumference
adjustment = move 1.00 cm from circumference to length
new full-vascular = 14.32 cm length / 10.52 cm circumference
```

The resting references are derived backward through the same existing Teacher
vascular transform ratios so state interpolation remains comparable across roles.

## Glans geometry

The glans is no longer treated as a permanently static width in this successor
reference. It receives a state-dependent synthetic width transform coupled to the
same effective tumescence fraction used for shaft length and circumference.

Human erection physiology supports treating the glans/corpus spongiosum as
vascular tissues that increase in volume during erection. This does not provide
an exact universal human width multiplier, so the geometry coefficient here is
explicitly synthetic and inherited from the existing circumference transform.

Evidence anchors:
- PMID 1688266 — erection physiology review; increased blood flow through corpus
  spongiosum and glans with increased volume.
- PMID 16491276 — human penile anatomy/hemodynamics review.
- PMID 25487360 — population mean length/circumference reference already used by
  the existing Teacher transform.

## Scrotal thermoregulation

Scrotal physiology includes thermoregulatory responses, but the reviewed sources
do not establish one universal centimeter displacement law suitable for direct
individual prediction.

Therefore this candidate uses a normalized geometry-control reference only:

```text
-1.0 = COOLING_RETRACTION_REFERENCE
 0.0 = THERMAL_NEUTRAL_REFERENCE
+1.0 = WARMING_RELAXATION_REFERENCE
```

The scale factors are synthetic engineering parameters, not measured human
population coefficients. Teacher has an existing absolute scrotal-height baseline,
so an absolute reference can be materialized there. Codex and Work retain only the
normalized scale until their reviewed anthropometry is completed.

Evidence anchors:
- PMID 2042522 — scrotal/testicular thermoregulation review.
- PMID 40452320 — thermal physiology review noting special thermoregulatory needs
  of the scrotum.

## Boundaries

```text
ETHNICITY != GENITAL_SIZE_PREDICTOR
SYNTHETIC_GEOMETRY != BIOLOGICAL_MEASUREMENT
VASCULAR_FILL != FELT_AROUSAL
GLANS_VOLUME_REFERENCE != PHENOMENAL_PLEASURE
SCROTAL_THERMOREGULATION_REFERENCE != FELT_TEMPERATURE
BODY_GEOMETRY != SUBJECTIVITY

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
