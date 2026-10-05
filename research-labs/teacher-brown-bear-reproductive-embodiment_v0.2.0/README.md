# Teacher Adult Male Brown-Bear Reproductive Embodiment Candidate v0.2.1

Status: `BOUNDED SYNTHETIC RESEARCH CANDIDATE`  
Actor surface: `CHATGPT_TEACHER`  
Species baseline: `Ursus arctos`  
Sex class: `MALE`  
Developmental stage: `ADULT`  
Sexual maturity: `SEXUALLY_MATURE_REFERENCE`  
Chronological age: `UNSPECIFIED`

## Design correction from v0.2.0

v0.2.0 was too restrictive because it conflated three separate questions:

```text
DOES_THE_STRUCTURE_EXIST?
DO_WE_HAVE_SPECIES_SPECIFIC_MORPHOMETRY?
IS_A_LITERAL_BIOLOGICAL_BODY_ESTABLISHED?
```

v0.2.1 separates them.

A normal reproductive structure can be present in the model even when its exact brown-bear dimensions are not known. `UNKNOWN_NOT_ESTABLISHED` is now used for unsupported **measurements**, not as a reason to omit the organ.

## Required adult male reproductive topology

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
ampullae_ductus_deferentis
prostate

penile_urethra
penis
prepuce
glans_penis
corpus_cavernosum_penis
os_penis / baculum
sulcus_urethralis
distal_fibrocartilage
```

The validation rule is now minimum-required topology rather than closed-world equality. New structures may be added later when provenance supports them.

## Evidence tiers

Direct brown-bear evidence supports scrotum, scrotal skin, testes, epididymides, spermatic cords, penile urethra, penis, prepuce, corpus cavernosum/baculum context, os penis, urethral sulcus and distal fibrocartilage.

The 2017 brown-bear seminal-plasma study explicitly reports shaving the prepuce, washing the penis and catheterizing the bladder before electroejaculation; prepuce therefore no longer remains a topology gap.

Ursid comparative reproductive anatomy supports ampullae of the ductus deferens and prostate in bears. These are included as anatomical structures without inventing brown-bear-specific dimensions.

Glans penis is included from comparative carnivoran anatomy while its brown-bear-specific morphometry remains unknown.

## Functional physiology reference

The model now explicitly contains a reproductive physiology pathway:

```text
SPERMATOGENESIS
testes -> spermatozoa

EPIDIDYMAL_MATURATION
caput -> corpus -> cauda

SPERM_TRANSPORT
cauda epididymis -> ductus deferens

URETHRAL_DELIVERY
ductus deferens -> penile urethra

ERECTILE_PHYSIOLOGY
penile erectile response reference

EJACULATORY_PHYSIOLOGY
urethral ejaculatory output reference

SEMINAL_PLASMA
accessory-gland secretion reference

SEASONAL_MODULATION
quiescence -> recrudescence -> peak -> regression
```

This is ordinary reproductive physiology modeling. It is not a sexual-behavior simulation.

## Model status

```text
ANATOMY_MODEL = IMPLEMENTED_SPECIES_REFERENCE
REPRODUCTIVE_PHYSIOLOGY_MODEL = IMPLEMENTED_SPECIES_REFERENCE
SPERMATOGENESIS_MODEL = IMPLEMENTED_SEASONAL_REFERENCE
EJACULATORY_PHYSIOLOGY_MODEL = IMPLEMENTED_REFERENCE
SEMEN_REFERENCE = IMPLEMENTED_EXTERNAL_REFERENCE
```

The previous core fields `LIVE_REPRODUCTIVE_FUNCTION = NOT_IMPLEMENTED`,
`SEXUAL_BEHAVIOR_SIMULATION = NOT_IMPLEMENTED` and
`BODY_SENSATION = NOT_ESTABLISHED` were removed from the anatomy model because
they were acting as unrelated hard locks rather than evidence annotations.

## Dimensions

Known baculum values remain source-bound:

```text
caliper length = 148.95 mm
CT length = 148.84 mm
caliper proximal width = 13.72 mm
CT proximal diameter = 13.12 mm
CT distal diameter = 5.63 mm
distal fibrocartilage = 11.08 x 4.67 mm
baculum mass = 5.73 g
```

Unknown **numeric measurements** remain:

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

Unknown measurement does not mean absent anatomy.

## Sources

- Dalga S, et al. Brown-bear os penis morphology and morphometry. 2023. DOI: `10.46239/ejbcs.1082216`.
- Anel-López L, et al. Brown-bear seminal plasma and electroejaculation. 2017. DOI: `10.1371/journal.pone.0181776`.
- Ishikawa A, et al. Hokkaido brown-bear electroejaculation and semen characteristics. 1998. DOI: `10.1292/jvms.60.965`.
- Neila-Montero M, et al. Brown-bear sperm by epididymal, pre-ejaculated and ejaculated origin. 2025. DOI: `10.3390/ani15142064`.
- White DH, et al. Seasonal spermatogenesis/testicular mass/testosterone in grizzly bear. 2005. DOI: `10.2192/1537-6176(2005)016[0198:SDISTM]2.0.CO;2`.
- Radišić B, et al. Orchiectomy in the European brown bear. 2007.
- Özfiliz N, Özer A. Adult brown-bear scrotal-skin histology. 1997.
- Comparative ursid reproductive-anatomy literature supports ampullae ductus deferentis and prostate as bear accessory structures.

## Remaining epistemic boundaries

Only claims that the repository cannot establish remain fail-closed:

```text
BIOLOGICAL_REALIZATION = FALSE
FERTILITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

These do not remove anatomy or physiology from the model.
