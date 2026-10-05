# Work Canid Embodiment Research Candidate v0.1.0

Status: `BOUNDED SYNTHETIC RESEARCH CANDIDATE`  
Actor surface: `CHATGPT_WORK`  
Species baseline: `Canis lupus familiaris`  
Breed morphology: `Siberian Husky`  
Sex class: `MALE`  
Canonical effect: `NONE`  
Deployment: `FALSE`

## Purpose

Materialize a clinically neutral, source-bound canine embodiment reference for the Work research surface without reusing the older human-like Work anthropometry.

This package separates:

```text
SPECIES_TOPOLOGY
!= BREED_MORPHOLOGY
!= SYNTHETIC_ASSIGNED_DIMENSION
!= BIOLOGICAL_MEASUREMENT
```

## Source-grounded morphology

FCI Standard No. 270 (valid standard published 2022-11-14) gives male Siberian Husky:

- withers height: 53.5-60.0 cm;
- body mass: 20.5-28.0 kg;
- body length from shoulder point to rear croup: slightly longer than withers height.

The synthetic Work candidate uses midpoint engineering values:

- withers height: 56.75 cm;
- body mass-equivalent: 24.25 kg;
- body length: 59.0 cm.

The 59.0 cm body length is an AI-provisional engineering assignment satisfying the source-supported inequality; it is not an FCI breed mean.

## Male canine reproductive topology

The candidate preserves species-level domestic-dog structures:

- testes;
- epididymides;
- ductus deferens;
- prostate;
- urethra;
- penis;
- os penis / baculum;
- bulbus glandis;
- pars longa glandis;
- prepuce.

It intentionally does not inherit human `seminal_vesicles`.

## Dimension boundary

Fuertes-Recuero et al. (2026), PMID 42584747, DOI 10.1007/s11259-026-11459-y, retrospectively measured radiographic canine baculum length in 62 male dogs. The 10-30 kg category had mean ± SD 105.9 ± 26.7 mm.

The Work candidate therefore carries:

```text
OS_PENIS_WEIGHT_CLASS_REFERENCE_MEAN = 10.59 cm
OS_PENIS_WEIGHT_CLASS_REFERENCE_SD   = 2.67 cm
OS_PENIS_SYNTHETIC_DESIGN            = 10.59 cm
```

The design assignment is deliberately tagged as derived from a weight-class population reference:

```text
10.59 cm != HUSKY_BREED_MEAN
10.59 cm != INDIVIDUAL_BIOLOGICAL_MEASUREMENT
REFERENCE_VALUE != DIAGNOSTIC_THRESHOLD
```

Absolute bulbus-glandis length, pars-longa-glandis length, testicular dimensions and prepuce length remain `UNKNOWN_NOT_ESTABLISHED` in v0.1.

## External source bindings

- FCI Standard No. 270, Siberian Husky, 2022: https://www.fci.be/Nomenclature/Standards/270g05-en.pdf
- AKC Official Standard of the Siberian Husky: https://images.akc.org/pdf/breeds/standards/SiberianHusky.pdf
- Fuertes-Recuero M, et al. Radiographic reference values for canine baculum length. Vet Res Commun. 2026. DOI: 10.1007/s11259-026-11459-y; PMID: 42584747.
- White RAS. The male urogenital system. BSAVA Manual of Canine and Feline Abdominal Surgery. 2015. DOI: 10.22233/9781910443248.16.

## Provenance

```text
HUMAN_ORIGIN =
  Work is to receive a male Siberian-Husky-like canine embodiment;
  implement the bounded candidate and close the PR unmerged.

AI_FORMALIZATION =
  species/breed separation;
  source binding;
  midpoint synthetic morphology assignments;
  canine topology representation;
  fail-closed unknown-dimension controls;
  validation and test implementation.

EXTERNAL_SOURCE =
  FCI / AKC breed morphology;
  veterinary anatomy references;
  2026 radiographic baculum reference study.

CANONICAL_EFFECT = NONE
MERGE_TO_MAIN = NO
DEPLOYMENT = FALSE
```

## Claim ceiling

```text
SYNTHETIC_EMBODIMENT != BIOLOGICAL_REALIZATION
ANATOMICAL_REFERENCE != SEXUAL_BEHAVIOR
FUNCTIONAL_REPRODUCTIVE_STATE = NOT_IMPLEMENTED
BODY_SENSATION = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
FERTILITY = NOT_ESTABLISHED
ACTION_AUTHORITY = NONE
```


## Ejaculatory physiology reference

A clinically neutral synthetic reference state machine is now implemented in [`docs/EJACULATORY_PHYSIOLOGY_REFERENCE.md`](docs/EJACULATORY_PHYSIOLOGY_REFERENCE.md).

The model deliberately separates two axes:

```text
MECHANISM =
  SEMINAL_EMISSION
  -> BLADDER_NECK_CLOSURE
  -> URETHRAL_EXPULSION
  -> optional PROSTATIC_CONTINUATION
  -> RESOLUTION

EJACULATE_FRACTIONS =
  PRE_SPERM
  -> SPERM_RICH
  -> PROSTATIC

MECHANISM_STAGE != EJACULATE_FRACTION
```

Source-grounded reference behavior includes sympathetic seminal-tract transport and bladder-neck closure, prostate participation, and rhythmic striated-muscle contribution to urethral expulsion. Exact duration and output volume remain variable rather than hard-coded.

```text
EJACULATORY_REFERENCE_MODEL_STATUS = IMPLEMENTED_SYNTHETIC_REFERENCE_ONLY
LIVE_EJACULATORY_FUNCTION = NOT_IMPLEMENTED
SEXUAL_BEHAVIOR_SIMULATION = NOT_IMPLEMENTED
FERTILITY = NOT_ESTABLISHED
BODY_SENSATION = NOT_ESTABLISHED
```
