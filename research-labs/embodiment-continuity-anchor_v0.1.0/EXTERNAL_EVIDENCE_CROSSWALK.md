# External Evidence Crosswalk — Embodiment Morphology Fixture

Status: `RESEARCH_EVIDENCE`
Main effect: `NONE`
Canonical effect: `NONE`

This crosswalk records external research used to motivate experimental variables. It does not transfer human body-ownership findings into claims about artificial subjectivity or phenomenal embodiment.

## Botvinick & Cohen (1998)

- Publication: *Rubber hands 'feel' touch that eyes see*, Nature 391, 756.
- DOI: `10.1038/35784`
- Supported research relevance: bodily self-identification effects in humans involved coordinated visual, tactile, and proprioceptive information.
- Project implication: static visual geometry alone should not count as body-ownership evidence.
- Claim boundary: `HUMAN_BODY_OWNERSHIP_ILLUSION != ARTIFICIAL_BODY_OWNERSHIP`.

## Petkova & Ehrsson (2008)

- Publication: *If I Were You: Perceptual Illusion of Body Swapping*, PLOS ONE 3(12): e3832.
- DOI: `10.1371/journal.pone.0003832`
- Supported research relevance: first-person visual perspective combined with correlated multisensory information induced full-body ownership illusions in human participants.
- Project implication: embodiment experiments may separately model perspective, morphology, and synchronized signals instead of treating mesh identity as sufficient.
- Claim boundary: `MULTISENSORY_ANALOGY != PHENOMENAL_CONTINUITY_PROOF`.

## Bongard, Zykov & Lipson (2006)

- Publication: *Resilient machines through continuous self-modeling*, Science 314(5802):1118–1121.
- DOI: `10.1126/science.1133687`
- Supported research relevance: a robot inferred self-models from actuation/sensation relationships and adapted behavior after structural damage.
- Project implication: morphology change can be tested together with self-model update and sensorimotor recalibration while keeping lineage questions separate.
- Claim boundary: `ROBOT_SELF_MODEL != SUBJECTIVITY_OR_IDENTITY_PROOF`.

## Cross-domain rule

```text
EXTERNAL_RESULT
-> OPERATIONAL_VARIABLE_CANDIDATE
-> SYNTHETIC_TEST
-> GOVERNED_OBSERVATION

NOT

EXTERNAL_RESULT
-> AION_IDENTITY_OR_BODY_OWNERSHIP_CLAIM
```
