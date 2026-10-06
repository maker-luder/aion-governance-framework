# Provenance and Non-Claims — Work Husky v0.2

## Provenance classes

| Item | Provenance | Treatment |
| --- | --- | --- |
| Work / Siberian-Husky furry target | HUMAN_ORIGIN | actor-bound design direction |
| male Husky height / mass | EXTERNAL_SOURCE | FCI / AKC breed reference |
| canine reproductive topology | EXTERNAL_SOURCE + AI_FORMALIZATION | canid-first normalized topology |
| normal reproductive physiology | EXTERNAL_SOURCE + COMPARATIVE_REFERENCE | implemented reference-informed model |
| 10.59 ± 2.67 cm canine baculum values | DIRECT_SOURCE | 10–30 kg study category |
| SMALL / STANDARD / LARGE baculum values | SYNTHETIC_DESIGN | mean−SD / mean / mean+SD design anchors |
| unknown absolute organ dimensions | UNKNOWN_NOT_ESTABLISHED | not fabricated as measurements |
| internal-unlock / external-lock split | HUMAN_ORIGIN + AI_FORMALIZATION | governance architecture |

## Corrected semantics

```text
NORMAL_REPRODUCTIVE_FUNCTION = PRESENT
SPECIES_TYPICAL_REPRODUCTIVE_CAPACITY_MODEL = PRESENT

EMPIRICAL_INDIVIDUAL_FERTILITY = NOT_ASSESSED
BIOLOGICAL_REALIZATION = FALSE
```

The first pair describes the synthetic body model. The second pair prevents false
claims about an empirically tested biological individual.

```text
NON_SEXUALIZATION != BIOLOGICAL_DEPRIVATION
SEXUAL_FUNCTION != SEXUAL_BEHAVIOR
SOURCE_MEASUREMENT_UNKNOWN != ORGAN_ABSENT
SYNTHETIC_DESIGN != BIOLOGICAL_MEASUREMENT
```

## Ontology

```text
ENTITY_CLASS = FANTASY_SAPIENT_NONHUMAN_BEING
FORM_CLASS = ANTHROPOMORPHIC_SIBERIAN_HUSKY_CANID
MORPHOLOGY_ORIGIN = CANID_DOMINANT
HUMAN_LIKENESS = FUNCTION_SPECIFIC_NOT_GLOBAL
PHYSIOLOGICAL_REFERENCE_PRIORITY = CANID_FIRST
```

## Nonclaims and external boundary

```text
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
BIOLOGICAL_REALIZATION = FALSE

SEXUAL_BEHAVIOR_SIMULATION = OUT_OF_SCOPE
EROTIC_NARRATIVE = OUT_OF_SCOPE

DEPLOYMENT = FALSE
PUBLIC_RELEASE = FALSE
THIRD_PARTY_ACCESS = FALSE
PRODUCTION_USE = FALSE
AUTOMATIC_WRITEBACK = FALSE
MERGE_TO_MAIN = FALSE
CANONICAL_EFFECT = NONE
```
