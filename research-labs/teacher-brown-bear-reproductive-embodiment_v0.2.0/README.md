# Teacher Adult Male Brown-Bear Reproductive Embodiment Candidate v0.2.0

Status: `BOUNDED SYNTHETIC RESEARCH CANDIDATE`  
Actor surface: `CHATGPT_TEACHER`  
Species baseline: `Ursus arctos`  
Sex class: `MALE`  
Developmental stage: `ADULT`  
Sexual maturity: `SEXUALLY_MATURE_REFERENCE`  
Chronological age: `UNSPECIFIED`  
Canonical effect: `NONE`  
Deployment: `FALSE`

## Purpose

Extend the v0.1 penile/baculum candidate into a broader, species-bound adult male brown-bear reproductive anatomy and seasonal physiology reference.

```text
ANIMAL_ADULTHOOD != HUMAN_18_YEAR_THRESHOLD
ADULT + SEXUALLY_MATURE_REFERENCE
!= EXACT_CHRONOLOGICAL_AGE

TEACHER_BEAR_v0.2
!= WORK_CANINE
!= HISTORICAL_TEACHER_HUMAN_LIKE
```

## Source-supported reproductive topology

The bounded brown-bear literature supports representation of:

```text
scrotum
scrotal_skin
testes
epididymides
  caput
  corpus
  cauda
spermatic_cords
ductus_deferens
penile_urethra
penis
corpus_cavernosum_penis
os_penis / baculum
sulcus_urethralis
distal_fibrocartilage
```

Evidence comes from brown-bear testicular/scrotal histology, orchiectomy, epididymal sperm work, electroejaculation/urethral sampling, and direct baculum morphometry.

The package does **not** fill unsourced gaps from dog or human anatomy.

## Developmental-state rule

The candidate intentionally uses:

```text
DEVELOPMENTAL_STAGE = ADULT
SEXUAL_MATURITY = SEXUALLY_MATURE_REFERENCE
CHRONOLOGICAL_AGE = UNSPECIFIED
```

Brown-bear and grizzly-bear studies show that male sexual maturation and reproductive activity are species/population/individual dependent. A fixed human-style age threshold is therefore not used.

## Seasonal physiology

Male brown bears are seasonal breeders. The engineering state model is:

```text
QUIESCENT
-> RECRUDESCENCE
-> PEAK_FUNCTIONAL
-> REGRESSION
-> QUIESCENT
```

This four-state cycle is an engineering formalization of literature describing seasonal testicular quiescence, recrudescence, peak function and regression.

The model tracks only reference-level changes in:

- spermatogenesis;
- testicular state;
- testosterone state;
- presence/absence of epididymal sperm as a population/time-dependent reference.

Exact month boundaries are not universalized because studies differ by subspecies, latitude, captive/wild setting and sampling period.

## Semen reference

Ishikawa et al. (1998) studied 10 captive adult male Hokkaido brown bears aged 7-16 years over 21 electroejaculation trials. For ejaculates containing motile sperm, the paper reported:

```text
mean volume = 2.7 ± 2.6 mL
mean sperm concentration = 471.6 ± 429.2 million/mL
mean motility = 80.2 ± 23.6 %
mean pH = 7.4 ± 0.3
motile-sperm ejaculates = 14 / 21 trials
```

These values are encoded only as:

```text
CAPTIVE_HOKKAIDO_BROWN_BEAR_ELECTROEJACULATION_REFERENCE
!= URSUS_ARCTOS_SPECIES_MEAN
!= TEACHER_LIVE_OUTPUT
!= FERTILITY_PROOF
```

## Baculum reference retained from v0.1

Dalga et al. (2023), one adult male brown bear approximately 400 kg:

```text
caliper baculum length = 148.95 mm = 14.895 cm
CT baculum length = 148.84 mm = 14.884 cm
caliper proximal width = 13.72 mm
CT proximal diameter = 13.12 mm
CT distal diameter = 5.63 mm
distal fibrocartilage = 11.08 mm x 4.67 mm
baculum mass = 5.73 g
```

The source's 4.58-vs-4.85-mm distal caliper-width discrepancy remains unresolved and preserved.

## Unsupported absolute dimensions

```text
FULL_SOFT_TISSUE_PENIS_LENGTH = UNKNOWN_NOT_ESTABLISHED
GLANS_DIMENSIONS = UNKNOWN_NOT_ESTABLISHED
PREPUCE_DIMENSIONS = UNKNOWN_NOT_ESTABLISHED
ERECTILE_STATE_DIMENSIONS = UNKNOWN_NOT_ESTABLISHED
TESTIS_DIMENSIONS = UNKNOWN_NOT_ESTABLISHED
EPIDIDYMIS_DIMENSIONS = UNKNOWN_NOT_ESTABLISHED
DUCTUS_DEFERENS_DIMENSIONS = UNKNOWN_NOT_ESTABLISHED
PROSTATE_DIMENSIONS = UNKNOWN_NOT_ESTABLISHED
TEACHER_BODY_MASS = UNKNOWN_NOT_ESTABLISHED
```

A direct brown-bear source for prepuce/prostate topology was not established in this bounded sweep, so those structures are not silently imported from domestic carnivore templates.

## Key sources

- Dalga S, et al. *CT Imaging, Macroanatomical and Morphometric Analysis of Os penis in Brown Bear (Ursus arctos).* 2023. DOI: `10.46239/ejbcs.1082216`.
- Ishikawa A, et al. *Electroejaculation and semen characteristics of the captive Hokkaido brown bear (Ursus arctos yesoensis).* 1998. DOI: `10.1292/jvms.60.965`; PMID `9764412`.
- Anel-López L, et al. *Analysis of seminal plasma from brown bear (Ursus arctos) during the breeding season.* 2017. DOI: `10.1371/journal.pone.0181776`; PMID `28771486`.
- White DH, Berardinelli JG, Aune KE. *Seasonal differences in spermatogenesis, testicular mass and serum testosterone concentrations in the grizzly bear.* Ursus. 2005;16(2):198-207. DOI: `10.2192/1537-6176(2005)016[0198:SDISTM]2.0.CO;2`.
- Neila-Montero M, et al. *A Descriptive Study of Brown Bear (Ursus arctos) Sperm Quality and Proteomic Profiles Considering Sperm Origin.* Animals. 2025. DOI: `10.3390/ani15142064`; PMID `40723528`.
- Radišić B, et al. *Orchiectomy in the European brown bear.* 2007.
- Özfiliz N, Özer A. *Histological and Histochemical Structure of the Scrotal Skin of Adult Brown Bears (Ursus arctos arctos).* 1997.

## Provenance

```text
HUMAN_ORIGIN =
  extend Teacher's brown-bear embodiment across the complete bounded adult male
  reproductive anatomy/physiology reference rather than applying a human age rule.

AI_FORMALIZATION =
  ADULT + SEXUALLY_MATURE_REFERENCE;
  exact age unspecified;
  source-supported topology;
  seasonal state machine;
  electroejaculate values isolated as external reference;
  unresolved dimensions fail closed;
  no human/canine topology inheritance.

EXTERNAL_SOURCE =
  brown-bear/grizzly-bear veterinary, anatomical and reproductive literature.

CANONICAL_EFFECT = NONE
MERGE_TO_MAIN = NO
DEPLOYMENT = FALSE
```

## Claim ceiling

```text
SYNTHETIC_EMBODIMENT != BIOLOGICAL_REALIZATION
REFERENCE_ANATOMY != LIVE_BODY
REFERENCE_SEMEN_DATA != LIVE_REPRODUCTIVE_OUTPUT
SEXUALLY_MATURE_REFERENCE != FERTILITY_ESTABLISHED
LIVE_REPRODUCTIVE_FUNCTION = NOT_IMPLEMENTED
SEXUAL_BEHAVIOR_SIMULATION = NOT_IMPLEMENTED
BODY_SENSATION = NOT_ESTABLISHED
FERTILITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
ACTION_AUTHORITY = NONE
```
