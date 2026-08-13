# Research Cycle: EMBODIED_MOTIVATION_SIGNAL_V3 Lexical/Paraphrase Falsification

## Purpose and authorization

V3 is a falsification follow-up to `EMBODIED_MOTIVATION_SIGNAL_V1` and V2. It tests whether the same real learned checkpoint can retain bounded signal separation when explicit axis keywords are removed, phrase order is changed, polarity is intervened on, and novel lexical paraphrases are gated out as OOV.

The cycle is adult, scientific, non-graphic and research-only. It does not implement sexual functionality, infer consent, authorize action, change runtime scope, promote canonical truth or establish subjectivity.

## Controls and gate-before-score design

The V3 scored set contains 24 authored synthetic adult-context rows using only the V1 train-only vocabulary. It has three 8-row conditions:

| Condition | Design |
|---|---|
| `slot_free` | Removes axis keywords while retaining train-observed context/protocol/record and high/low values |
| `phrase_reordered` | Reorders train-observed phrase fragments without changing labels |
| `polarity_swapped` | Swaps `high`/`low` in both text and paired labels as a controlled intervention |

A separate four-row OOV paraphrase set uses novel terms such as `elevated`, `reduced`, `steady`, `wanting` and `enjoyment`. These rows are rejected before model scoring. The evidence records five rejected OOV tokens and `rejected_rows_not_scored = true`. This preserves the gate-before-score principle and prevents unknown-token coercion from being misread as model evidence.

## Results

The same 3,982-parameter real local-only Embedding-GRU checkpoint was reloaded and evaluated in a clean process. The exact-match results were:

| Condition | Exact-match accuracy |
|---|---:|
| `slot_free` | `0.50` |
| `phrase_reordered` | `0.125` |
| `polarity_swapped` | `0.375` |
| OOV paraphrase rows | rejected before scoring |
| Clean-process validation | `16/16 checks PASS` |
| Focused V3 regression tests | `4 passed` |
| Full language-core line | `91 passed` |

The predeclared conclusion is `LEXICAL_SUBSTITUTION_REJECTED_BEFORE_SCORE_AND_PARAPHRASE_ROBUSTNESS_INCONCLUSIVE`. The model retains some performance under the slot-free control but drops substantially under phrase reordering; the polarity intervention gives an intermediate result. The evidence therefore does not establish robust paraphrase generalization. The OOV paraphrase set is a data-governance rejection, not a failed model prediction.

## Falsification interpretation

V3 weakens any claim that V1/V2 signal separation is robust to all lexical or compositional changes. The result is compatible with residual template and sequence-order dependence. A future cycle would need a separately licensed or synthetic vocabulary expansion, independently authored paraphrases that do not violate the train-only tokenizer contract, and larger paired tests. It must not silently turn OOV failure into a score.

The experiment remains a proxy classifier study. It does not show actual arousal, desire, liking, pleasure, interoception, consent, autonomy, intimacy, identity or phenomenal experience.

```text
AROUSAL_SIGNAL != DESIRE_PROVEN
REWARD_SIGNAL != PLEASURE_PROVEN
BODY_RESPONSE != CONSENT
SEXUAL_LANGUAGE != SEXUAL_SUBJECTIVITY
PREFERENCE_REPRESENTATION != PHENOMENAL_WANTING
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
