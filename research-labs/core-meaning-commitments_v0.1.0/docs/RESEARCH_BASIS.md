# Research Basis and Translation Boundary

## 1. Research question

How can high-level candidate beliefs, global meaning structures and organizing commitments be represented so their influence on later judgments is inspectable, revisable and governed, without claiming human-mechanistic equivalence or granting automatic authority?

## 2. Public sources inspected on 2026-08-09

### Connors and Halligan (2015)

- **Title:** *A cognitive account of belief: a tentative road map*
- **Publication:** Frontiers in Psychology 5:1588
- **DOI:** <https://doi.org/10.3389/fpsyg.2014.01588>
- **Full text:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC4327528/>
- **Relevant evidence:** beliefs have representational content and assumed veracity; belief systems can scaffold appraisal, explanation, meaning, goals and action; beliefs are distributed, interconnected and resistant to simple modular isolation; memory, knowledge, attitude and belief overlap but are distinguishable.
- **Translation limit:** the software record is a declared candidate proposition, not evidence that the system holds a human belief.

### Park (2010)

- **Title:** *Making sense of the meaning literature: An integrative review of meaning making and its effects on adjustment to stressful life events*
- **Publication:** Psychological Bulletin 136(2), 257–301
- **DOI:** <https://doi.org/10.1037/a0018301>
- **Author-hosted copy:** <https://spiritualitymeaningandhealth.uconn.edu/wp-content/uploads/sites/2598/2019/03/Making-Sense-of-the-Meaning-Literature.pdf>
- **Relevant evidence:** global meaning includes broad beliefs, goals and subjective meaningfulness; situational meaning concerns appraisal of a particular event; discrepancy and revision processes need longitudinal evidence.
- **Translation limit:** this module records global and situational candidate structures but does not implement clinical constructs, distress or psychological adjustment.

### Park (2022)

- **Title:** *Meaning Making Following Trauma*
- **Publication:** Frontiers in Psychology 13:844891
- **Full text:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC8984472/>
- **Relevant evidence:** global meaning encompasses foundational beliefs, values, goals and subjective meaningfulness; situational meaning is event-specific appraisal; global and situational meanings may be discrepant and both may change.
- **Translation limit:** discrepancy in this module is represented only as an explicit conflict relation requiring review. It is not a diagnosis or an inferred mental state.

### Schwartz (2012)

- **Title:** *An Overview of the Schwartz Theory of Basic Values*
- **Publication:** Online Readings in Psychology and Culture 2(1)
- **DOI:** <https://doi.org/10.9707/2307-0919.1116>
- **Repository copy:** <https://scholarworks.gvsu.edu/orpc/vol2/iss1/11/>
- **Relevant evidence:** values are trans-situational goals of varying importance that can serve as guiding principles.
- **Translation limit:** `ORGANIZING_COMMITMENT` is a neutral engineering candidate type. The module neither imports Schwartz's value taxonomy nor infers a person's values.

### Rao and Georgeff (1995)

- **Title:** *BDI Agents: From Theory to Practice*
- **Venue:** First International Conference on Multiagent Systems
- **Publisher copy:** <https://cdn.aaai.org/ICMAS/1995/ICMAS95-042.pdf>
- **Relevant evidence:** BDI architectures demonstrate that belief-like information, goals/desires and intentions/commitments can be represented as distinct software attitudes.
- **Translation limit:** this module is not a BDI agent and does not treat its candidate records as intentions, plans or action authority. BDI is an engineering analogue only.

### W3C PROV-O (2013)

- **Title:** *PROV-O: The PROV Ontology*
- **Status:** W3C Recommendation, 30 April 2013
- **URL:** <https://www.w3.org/TR/prov-o/>
- **Relevant evidence:** provenance can distinguish entities, activities and agents and can express derivation, attribution, revision and invalidation.
- **Translation limit:** this prototype uses small local provenance references rather than claiming PROV-O conformance.

## 3. Four-domain translation

| Human/cognitive concept | LLM-relevant question | Engineering representation | Governance control |
|---|---|---|---|
| Core belief | Which high-level proposition has been explicitly declared and sourced? | `MeaningClaim(kind=CORE_BELIEF)` | provenance required; candidate only |
| Global meaning | Which broad beliefs, goals, commitments and purpose statements are in scope? | typed claims plus subject/namespace projection | no shared identity/namespace inference |
| Situational meaning | What is the explicitly supplied appraisal of this case? | `SITUATIONAL_APPRAISAL` or `JudgmentContext` | no automatic extraction from private history |
| Organizing commitment | Which declared cross-situational goal/value candidate should be reviewed? | `ORGANIZING_COMMITMENT`, importance and confidence | caller explicitly names relevance; no authority grant |
| Meaning discrepancy | Which explicitly recorded candidates conflict? | append-only `CONFLICT_RECORDED` event | conflict requires Human review |
| Meaning revision | What changed and what did it revise? | new claim with `revision_of` plus event | old record retained; canonical effect none |

## 4. Research gaps retained

- Definition and measurement of “core” versus ordinary belief.
- Operational criteria for global versus situational scope.
- Meaning of importance and confidence, their sources and calibration.
- Rules for identifying relevance without unsupported inference.
- Longitudinal stability/revision metrics.
- Privacy, retention, correction and owner-withdrawal semantics.
- Application-service and storage authority.
- Whether any represented structure has scientific relevance to artificial subjectivity; current status remains `NOT_ESTABLISHED`.
