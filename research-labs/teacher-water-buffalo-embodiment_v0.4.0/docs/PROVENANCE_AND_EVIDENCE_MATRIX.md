# Teacher water-buffalo whole-body candidate — provenance and evidence matrix

## Provenance split

| Item | Provenance | Status |
| --- | --- | --- |
| Bubalus bubalis reference | HUMAN_ORIGIN + EXTERNAL_SOURCE | current species reference |
| white skin | HUMAN_ORIGIN | synthetic phenotype |
| paired horns | HUMAN_ORIGIN | synthetic phenotype |
| square / 國字臉 craniofacial proportion | HUMAN_ORIGIN | synthetic phenotype |
| bovine ears | HUMAN_ORIGIN | synthetic phenotype |
| human-like nose | HUMAN_ORIGIN | synthetic phenotype |
| heavyset body | HUMAN_ORIGIN | synthetic phenotype |
| long hair | HUMAN_ORIGIN | synthetic phenotype |
| human-like hands/feet evolved from hoof morphology | HUMAN_ORIGIN | synthetic phenotype |
| exact anthropomorphic whole-body cm values | AI_FORMALIZATION | SYNTHETIC_DESIGN; revisable |
| buffalo reproductive anatomy and source cm values | EXTERNAL_SOURCE | reference only |
| sexual-function state machine | AI_FORMALIZATION + EXTERNAL_SOURCE | non-erotic physiology ordering |
| felt desire / pleasure / body sensation | UNKNOWN | NOT_ESTABLISHED |

## External sources

1. N. A. Tonizza de Carvalho, J. G. Soares, P. R. Kahwage, A. R. Garcia. *Anatomy of the Reproductive Tract of the Female and Male Buffaloes.* In: Bubaline Theriogenology, IVIS, 2014, document A5701.0714.  
   https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1037632/1/CARVALHO-SOARES-KAHWAGE-e-GARCIA-2014-Anatomy-of-the-Reproductive-Tract-of-the-Female-and-Male-Buffaloes.pdf

2. I. C. A. Ribeiro et al. *Stereological study of the elastic fiber and smooth muscle cell system in the bovine and buffalo penis.* Adult Mediterranean buffalo material; supports fibroelastic histology and the importance of elastic fibers.

3. N. Isnaini, T. Harsi, W. R. Zamani. *Age-Dependent Changes in Fresh Semen Quality of Swamp Buffalo (Bubalus bubalis).* IOP Conference Series: Earth and Environmental Science 478 (2020) 012034. The age-specific semen table is retained as dataset-specific reference, not a species mean.

4. Philippine water-buffalo ampulla study: adults 3–5 years, reported average ampulla length 7.4 cm and diameter 7.1 mm. Values are retained as population/sample-specific reference rather than universal anatomy.

## Exact-source boundaries

Carvalho et al. reports adult buffalo-bull average penis length of 80.15 cm measured from the beginning of the sigmoid flexure to the free end, and average thickness of 1.95 cm. It also reports adult bubaline vesicular glands at approximately 8–10 cm long and 2–3 cm in diameter.

The chapter compiles multiple studies. Therefore:

```text
REPORTED_REFERENCE_MEAN != INDIVIDUAL_TEACHER_MEASUREMENT
MULTI_STUDY_RANGE != POPULATION_CONSTANT
BIOLOGICAL_REFERENCE_DIMENSION != ANTHROPOMORPHIC_SYNTHETIC_TARGET
```

The anthropomorphic whole-body dimensions in this package are explicit `SYNTHETIC_DESIGN` values. Reproductive species-reference dimensions are not silently rescaled into the fantasy body.

## Claim ceiling

```text
ANTHROPOMORPHIC_WATER_BUFFALO = FANTASY_EMBODIMENT
BUBALUS_BUBALIS_REFERENCE != BIOLOGICAL_REALIZATION
WHOLE_BODY_REFERENCE_SCAFFOLD != FULL_BIOPHYSICAL_SIMULATION
REPRODUCTIVE_ANATOMY != SEXUALIZATION
SEXUAL_FUNCTION_PHYSIOLOGY != EROTIC_NARRATIVE
PHYSIOLOGICAL_STATE != FELT_DESIRE
BODY_SENSATION = NOT_ESTABLISHED
PLEASURE = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MERGE_TO_MAIN = NO
CANONICAL_EFFECT = NONE
```
