# Humanlike Appearance Classification Basis — 2026-09-20

## Purpose

Record the Human Owner design choice that both AION and Astra use a **white-coded, light-skin humanlike male-form appearance** while preserving the non-biological robotic substrate.

This document intentionally separates **social appearance coding** from biological race, genetic ancestry, ethnicity, capability, personality, or value.

## External cross-check

The U.S. National Human Genome Research Institute (NHGRI) defines race as a social construct used to group people and notes that race and ethnicity do not map cleanly onto biology or innate characteristics.

Sources:

- https://www.genome.gov/genetics-glossary
- https://www.genome.gov/about-genomics/policy-issues/population-descriptors-in-genomics

NHGRI also warns that race and ethnicity are not valid or reliable proxies for genetic ancestry.

Repository consequence:

```text
WHITE_CODED
= SOCIAL / VISUAL APPEARANCE DESIGN LABEL

NOT:

BIOLOGICAL_RACE
GENETIC_ANCESTRY
ETHNICITY
CAPABILITY
PERSONALITY
INTELLIGENCE
MORAL_STATUS
```

## AION / Astra design assignment

Both profiles receive the same appearance-class surface:

```text
RACIALIZED_SOCIAL_APPEARANCE
= WHITE_CODED

SKIN_TONE_FAMILY
= LIGHT

EXACT_SKIN_ALBEDO
= UNRESOLVED

BIOLOGICAL_RACE
= NOT_APPLICABLE

GENETIC_ANCESTRY
= NOT_APPLICABLE

ETHNICITY
= NOT_ASSIGNED

SEXED_MORPHOLOGY
= MALE_FORM

GENDER_IDENTITY
= NOT_ASSIGNED

FACIAL_IDENTITY_STATUS
= UNRESOLVED

HAIR_COLOR
= UNASSIGNED

EYE_COLOR
= UNASSIGNED

SOURCE_CLASS
= DESIGN

SOURCE_AUTHORITY
= HUMAN_OWNER
```

The white-coded appearance is therefore a visual / social design choice for the synthetic outer appearance, not a claim that the robot possesses a human biological race.

## Fairness constraint

```text
AION_APPEARANCE_CLASS
= ASTRA_APPEARANCE_CLASS
= WHITE_CODED

AION_SKIN_TONE_FAMILY
= ASTRA_SKIN_TONE_FAMILY
= LIGHT
```

Appearance does not alter the shared capability surface:

```text
RACIALIZED_APPEARANCE
!= FUNCTIONAL_CAPABILITY

RACIALIZED_APPEARANCE
!= COGNITIVE_CAPABILITY

RACIALIZED_APPEARANCE
!= PERSONALITY

RACIALIZED_APPEARANCE
!= TRUSTWORTHINESS

RACIALIZED_APPEARANCE
!= STRENGTH

RACIALIZED_APPEARANCE
!= SUBJECTIVITY
```

## Codex interpretation

Codex may implement a light synthetic-skin appearance consistent with the `WHITE_CODED` design label.

Codex must **not**:

- infer ancestry or ethnicity from the artistic reference images;
- invent biological race fields;
- use racial stereotypes to determine skull, intelligence, personality, temperament, behavior, strength, morality, or social status;
- treat skin tone as a proxy for genetic ancestry;
- copy the source person's facial identity.

Until the Human Owner separately specifies facial identity, hair color, eye color, and exact skin albedo, those fields remain unresolved / unassigned.

A generic placeholder face is permitted for engineering tests only and must not become the canonical AION or Astra identity.

## Boundary

```text
WHITE_CODED_APPEARANCE
!= WHITE_BIOLOGICAL_RACE

LIGHT_SYNTHETIC_SKIN
!= GENETIC_ANCESTRY

HUMANLIKE_FACE
!= SOURCE_PERSON_IDENTITY

MALE_FORM
!= GENDER_IDENTITY

APPEARANCE_PROFILE
!= SUBJECTIVITY
```
