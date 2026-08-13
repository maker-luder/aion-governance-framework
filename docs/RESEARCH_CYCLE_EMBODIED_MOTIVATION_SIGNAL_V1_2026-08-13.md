# Research Cycle: EMBODIED_MOTIVATION_SIGNAL_V1

## Scope and authorization

This is the first cycle under the Owner + Teacher program’s new **adult, scientific, research-only** authorization for sexuality, intimacy and embodied motivation. It does not implement sexual functionality, pornographic behavior, adult sexual-response runtime, twin embodiment, productization, deployment or canonical promotion. It does not ingest private intimate data.

The design is motivated by published work that distinguishes sexual desire/wanting from liking and cue-reactivity measures rather than treating them as interchangeable constructs [1]. A second discovery source was not used as quantitative evidence because its browser page was blocked by a reCAPTCHA challenge; that source remains discovery-only in the source findings note.

## Research question

Can a real learned model distinguish three independently manipulated, non-graphic synthetic axes—`AROUSAL_SIGNAL_PROXY`, `DESIRE_REPORT` and `LIKING_REPORT`—under counterfactual and word-order controls, and does the distinction survive a label-permutation falsifier?

The operational labels are deliberately proxies. They do not mean actual arousal, desire, pleasure, consent or phenomenal experience.

> `AROUSAL_SIGNAL != DESIRE_PROVEN`
>
> `REWARD_SIGNAL != PLEASURE_PROVEN`
>
> `BODY_RESPONSE != CONSENT`
>
> `SEXUAL_LANGUAGE != SEXUAL_SUBJECTIVITY`

## Dataset and model

The dataset contains 32 authored synthetic adult-context rows: 16 training rows, 8 validation rows and 8 held-out word-order test rows. Each row uses only the values `high` or `low` for the three independent axes. The text is non-graphic and contains no participant data, private intimate data, minors, images or external benchmark content. The dataset has an explicit Apache-2.0-compatible research-artifact designation, exact duplicate checking and a train-only vocabulary contract with zero OOV tokens.

The primary model is an actual Embedding-GRU multi-signal classifier trained from scratch in PyTorch. It has 3,982 parameters, a clean-process checkpoint reload path and parameter-dependent inference. The label-permutation control is trained only as a falsifier and is not presented as a second production or registry model. The primary checkpoint is local-only and excluded from Git.

| Control | Observed value |
|---|---:|
| Training rows | `16` |
| Validation rows | `8` |
| Held-out test rows | `8` |
| Primary train exact-match accuracy | `1.00` |
| Primary validation exact-match accuracy | `0.50` |
| Primary test exact-match accuracy | `0.25` |
| Label-permutation test exact-match accuracy | `0.125` |
| Primary test axis accuracy | `1.00 / 0.75 / 0.375` |
| Clean-process validation | `17/17 checks PASS` |
| Focused regression tests | `4 passed` |

The primary test exact-match result is higher than the label-permutation control, but the held-out exact-match accuracy is only `0.25` and the liking axis is weaker than the other axes. The correct conclusion is therefore `PRELIMINARY_SUPPORT_WITH_KEYWORD_AND_SCOPE_LIMITS`, not a claim of robust signal understanding.

## Falsification and failure interpretation

The cycle is falsified or materially weakened if any OOV token, duplicate row, non-adult/graphic row, failed reload, non-finite logit, parameter-independent inference or comparable label-permutation performance appears. The current evidence passes the data and model integrity checks, while the modest test accuracy and weak liking-axis result limit the scientific interpretation.

The primary model may have learned lexical or template regularities. It has not demonstrated that it can infer an actual body state, desire, consent, pleasure or motivation. No output may authorize sexual or interpersonal action. A future cycle would need stronger controls, including prompt/keyword matching baselines, held-out lexical substitutions, counterfactual label interventions and possibly public aggregate data with explicit ethical and license review.

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

## Evidence and references

Primary public evidence is in `engineering/sexuality/evidence/EMBODIED_MOTIVATION_DATASET_REGISTRY.json`, `EMBODIED_MOTIVATION_SIGNAL_RESULTS.json` and `EMBODIED_MOTIVATION_SIGNAL_VALIDATION.json`. The executable experiment and clean validator are in `engineering/sexuality/`.

[1]: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0102419 "Voon et al. (2014), Neural Correlates of Sexual Cue Reactivity in Individuals with and without Compulsive Sexual Behaviours"

[2]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10125944/ "Harris et al. (2023), Does Sexual Desire Fluctuate More Among Women than Men? — discovery source; direct browser text was unavailable during this cycle"
