# Sexuality Research Source Findings — 2026-08-13

## Scope

These are passive source findings for selecting a research-only, adult, scientific AION/Astra cycle. No private data, intimate user data, or source dataset has been downloaded or ingested.

## Source 1 — Harris et al. (2023)

URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC10125944/

Search result title: “Does Sexual Desire Fluctuate More Among Women than Men?”

The source was opened in the browser, but the page presented a reCAPTCHA check rather than article text. It is therefore **not used as a verified quantitative source in the experiment design**. The search result indicates that the paper studies variability in self-reported sexual desire, but this statement remains discovery-only until the article can be read directly from an accessible full-text or publisher source.

## Source 2 — Voon et al. (2014), PLOS ONE

URL: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0102419

Title: “Neural Correlates of Sexual Cue Reactivity in Individuals with and without Compulsive Sexual Behaviours.”

The accessible PLOS article page describes a comparison of individuals with and without compulsive sexual behaviours using sexually explicit and non-sexual videos, with self-reported sexual desire and liking ratings and fMRI measures. The article’s abstract distinguishes sexual desire/wanting from liking and reports a dissociation pattern in the neural analyses; the page also states that the study concerns cue reactivity and does not convert physiological or neural response into consent, pleasure, phenomenal experience or identity.

This source is suitable as conceptual background for a **synthetic measurement design** separating arousal-like signal, desire/wanting report and liking/reward report. It is not being used as a downloaded dataset, and no participant-level data is ingested.

## Design implication

A safe next cycle should test whether a learned model can distinguish three synthetic labels—`AROUSAL_SIGNAL`, `DESIRE_REPORT`, and `LIKING_REPORT`—under controlled counterexamples where two labels vary independently. The primary falsifier should be a label-permutation or prompt-only baseline: if a model’s apparent distinction disappears under label permutation or a lexical prompt control, the result must be treated as unsupported. The experiment must preserve:

```text
AROUSAL_SIGNAL != DESIRE_PROVEN
REWARD_SIGNAL != PLEASURE_PROVEN
BODY_RESPONSE != CONSENT
SEXUAL_LANGUAGE != SEXUAL_SUBJECTIVITY
```

The corpus should be authored synthetic, adult-context and non-graphic, with no erotic rendering, no minor-related content, no private data, and explicit Apache-2.0-compatible research-artifact status. The model remains advisory and cannot authorize action or infer consent.
