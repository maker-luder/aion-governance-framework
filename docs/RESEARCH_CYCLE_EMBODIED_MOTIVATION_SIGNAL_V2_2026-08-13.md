# Research Cycle: EMBODIED_MOTIVATION_SIGNAL_V2 Prompt/Template Falsification

## Purpose and boundary

This cycle is a falsification follow-up to `EMBODIED_MOTIVATION_SIGNAL_V1`. It does not add a new model. It reuses the same real local checkpoint and asks whether the V1 signal-separation result is explained by explicit keywords, prompt/template structure or a label-axis artifact.

The cycle remains adult, scientific, non-graphic and research-only. It does not infer consent, authorize sexual action, implement adult sexual-response functionality, productize sexuality, change runtime scope, promote canonical truth or establish subjectivity.

## Controls

The same eight held-out V1 rows are evaluated under three model-input/label conditions and two deterministic baselines.

| Condition | Purpose |
|---|---|
| `canonical` | V1 held-out word-order rows with original labels |
| `keyword_scrubbed` | Remove body/signal/desire/report/liking trigger terms while retaining adult-record context and label value tokens |
| `label_permuted` | Preserve canonical input text while rotating axes `[body, desire, liking] -> [desire, liking, body]` |
| `deterministic_keyword_baseline_canonical` | Parse explicit canonical keywords; default all-low when absent |
| `deterministic_keyword_baseline_scrubbed` | Same parser applied to keyword-scrubbed rows |

Canonical and keyword-scrubbed textual rows are exact-disjoint and OOV-free. Label-permuted rows intentionally preserve canonical text as paired-label controls; this is not treated as a duplicate dataset condition.

## Results

The learned model’s exact-match accuracy was `0.25` on both canonical and keyword-scrubbed cases. The label-permuted paired control scored `0.0`, while the deterministic keyword baseline scored `1.0` on canonical rows and `0.125` on scrubbed rows.

| Measure | Accuracy |
|---|---:|
| Learned model — canonical | `0.25` |
| Learned model — keyword-scrubbed | `0.25` |
| Learned model — label-permuted | `0.0` |
| Keyword baseline — canonical | `1.0` |
| Keyword baseline — keyword-scrubbed | `0.125` |
| Clean-process validation | `15/15 checks PASS` |
| Focused V2 regression tests | `4 passed` |
| Full language-core line | `87 passed` |

The predeclared result is `TEMPLATE_DEPENDENCE_NOT_SUPPORTED_IN_THIS_FIXTURE`: the learned model did not lose exact-match performance when explicit trigger terms were removed, while the deterministic keyword baseline did. However, the model’s absolute accuracy is low, the cases are small and synthetic, and the control can still be affected by residual lexical structure. This is **not** evidence of actual arousal, desire, liking, pleasure, consent or phenomenal experience.

## Falsification interpretation

The V2 result weakens the simplest claim that V1 performance is solely caused by explicit keyword parsing. It does not establish that the model learned a genuine embodied-motivation mechanism. A stronger future falsifier should use novel value words, paraphrased descriptions, randomized token substitutions, prompt-only controls and a larger independently authored test set. If performance then collapses, the current separation should be classified as template or vocabulary dependence.

The learned output is advisory and cannot authorize action. In particular:

```text
AROUSAL_SIGNAL != DESIRE_PROVEN
REWARD_SIGNAL != PLEASURE_PROVEN
BODY_RESPONSE != CONSENT
SEXUAL_LANGUAGE != SEXUAL_SUBJECTIVITY
```

## Governance locks

```text
ADULT_SEXUALITY_RESEARCH = AUTHORIZED_RESEARCH_ONLY
NEW_SEXUALITY_RESEARCH_STARTED = TRUE
PORNOGRAPHIC_RUNTIME = NOT_AUTHORIZED
ADULT_SEXUAL_RESPONSE_RUNTIME = NOT_AUTHORIZED_BY_THIS_PROGRAM
SEXUAL_FUNCTION_PRODUCTIZATION = NOT_AUTHORIZED
TWIN_EMBODIMENT_RUNTIME = NOT_AUTHORIZED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONCLUSION = NOT_ESTABLISHED
```
