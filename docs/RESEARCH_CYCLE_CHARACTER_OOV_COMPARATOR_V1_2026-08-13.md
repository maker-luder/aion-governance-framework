# Research Cycle: CHARACTER_OOV_COMPARATOR_V1

## Scope and reason for selection

This cycle was already started before receipt of the complete continuation packets. It is therefore completed as an integration and publication obligation, not a newly selected post-STOP research program. It directly follows V3's evidenced limitation: word-tokenized OOV paraphrases were correctly rejected before scoring, leaving unresolved whether the failure was primarily a tokenizer boundary or a broader lexical/compositional generalization problem.

The comparator is an **OPTIONAL_RESEARCH_MODEL**, not a required runtime model. It is an actual PyTorch character-tokenized Embedding-GRU classifier trained from scratch with a local-only checkpoint. It does not change the AION runtime, product scope or canonical state.

## Dataset governance

The dataset is authored synthetic adult-context, non-graphic research data. It contains 16 prior train rows and 8 newly authored held-out OOV-word combinations. There is no PII, no private intimate data, no minor-related content, no intimate image and no external paid resource. The dataset registry records source, Apache-2.0-compatible synthetic-artifact boundary, allowed use, vocabulary digests, split method, exact-text duplicate check, contamination risk and transformation lineage.

The word-tokenizer control finds 7 OOV word tokens in the held-out rows and scores 0 rows. The character vocabulary contains no OOV characters and scores all 8 held-out rows. This is a gate-before-score comparison: word-tokenizer rejection is not treated as a model error, and character-tokenizer scoring is not treated as evidence of general language competence.

## Model and results

The character comparator was trained from scratch with seed `7319` using an Embedding-GRU architecture and a six-logit multi-signal head. Its primary checkpoint is local-only and has a SHA-256 recorded in the public evidence. The model achieved training exact-match accuracy `1.0` and held-out novel-word exact-match accuracy `0.125`. An in-memory label-permutation control achieved held-out exact-match accuracy `0.25`.

| Measurement | Result |
|---|---:|
| Train rows | `16` |
| Held-out OOV-word rows | `8` |
| Word-tokenizer OOV tokens | `7` |
| Word-tokenizer rows scored | `0` |
| Character-tokenizer OOV characters | `0` |
| Character-tokenizer held-out rows scored | `8` |
| Character model train exact match | `1.0` |
| Character model OOV exact match | `0.125` |
| Label-permutation OOV exact match | `0.25` |
| Clean-process validation | `18/18 checks PASS` |
| Focused regression tests | `4 passed` |

The declared result is `CHARACTER_OOV_RECOVERY_INCONCLUSIVE`. The character model can technically process the novel word forms, but its held-out performance is below the label-permutation control in this small fixture. This does not support a positive learned OOV-recovery claim. The result is compatible with insufficient training diversity, sequence/template dependence or a weak synthetic task. It does not establish that word-tokenizer OOV was the only limitation.

## Falsification and boundaries

The negative control is important: a model that merely produces outputs on character sequences is not automatically recovering the target proxy. The held-out result did not exceed the label-permutation control, so the positive interpretation is not supported in this fixture. Larger, independently authored, appropriately licensed or synthetic vocabulary-shift datasets would be required for stronger inference.

The experiment does not show actual arousal, desire, liking, pleasure, interoception, consent, autonomy, intimacy, identity or phenomenal experience. The following distinctions remain active:

```text
AROUSAL_SIGNAL != DESIRE_PROVEN
BODY_RESPONSE != CONSENT
SEXUAL_LANGUAGE != SEXUAL_SUBJECTIVITY
PREFERENCE_REPRESENTATION != PHENOMENAL_WANTING
```

## Continuation and governance state

The cycle is governed by the completed PART 1 + PART 2A + PART 2B + PART 2C task authority. It preserves exact-head QA provenance, current-state reconciliation, remote CI verification, the two-branch invariant and final STOP after the report. No new research program is selected after this cycle.

```text
ADULT_SEXUALITY_RESEARCH = AUTHORIZED_RESEARCH_ONLY
PORNOGRAPHIC_RUNTIME = NOT_AUTHORIZED
ADULT_SEXUAL_RESPONSE_RUNTIME = NOT_AUTHORIZED_BY_THIS_PROGRAM
SEXUAL_FUNCTION_PRODUCTIZATION = NOT_AUTHORIZED
TWIN_EMBODIMENT_RUNTIME = NOT_AUTHORIZED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONCLUSION = NOT_ESTABLISHED
```
