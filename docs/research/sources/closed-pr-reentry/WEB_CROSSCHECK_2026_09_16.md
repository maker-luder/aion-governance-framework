# Closed-PR re-entry external cross-check — 2026-09-16

Status: `DERIVATIVE_RESEARCH_NOTE / REFERENCE_ONLY / NO_RAW_PUBLICATION_COPY`

This note records the bounded external cross-check used while reviewing historical
closed pull requests. It does **not** vendor third-party papers or copy external
framework text into the repository. Existing exact NIST/FDA acquisitions remain governed
by `docs/research/sources/quality/` and its repository-external download-cache workflow.

```text
EXTERNAL_SOURCE != REPOSITORY_AUTHORITY
SOURCE_EXISTENCE != CLAIM_VALIDATION
DERIVATIVE_NOTE != COPIED_METHOD
QUALITY_METHOD_REFERENCE != SUBJECTIVITY_EVIDENCE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## 1. NIST AI RMF — continuous quality/risk-management cross-check

Official current page:
https://www.nist.gov/itl/ai-risk-management-framework

AI RMF Core:
https://airc.nist.gov/airmf-resources/airmf/5-sec-core/

NIST AI 600-1 publication page:
https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

Recheck result on 2026-09-16:

- AI RMF 1.0 remains the published framework, while NIST states that a revision is in progress.
- The current Core still organizes risk-management activity as `GOVERN / MAP / MEASURE / MANAGE`.
- Governance is cross-cutting; measurement includes reassessing the appropriateness of metrics and effectiveness of controls as knowledge and risks change.
- NIST AI 600-1 remains a Generative-AI companion profile, not a subjectivity or consciousness method.

Repository transformation:

```text
HISTORICAL_PR_CI_PASS != CURRENT_CONTROL_EFFECTIVENESS
OLD_RISK_MAP != CURRENT_RISK_MAP
OLD_MEASUREMENT != CURRENT_MEASUREMENT
REENTRY_REQUIRES_CURRENT_MAIN_RECHECK
```

No new NIST-derived quality ontology is created. Historical PR salvage must map into the
repository's existing `ResearchQualityChain` and current IQC/governance controls.

## 2. Theory-derived consciousness indicators — method, not detector

Existing repository card:
`docs/research/sources/subjectivity/butlin-tics-2026.md`

Primary article metadata / open-access publisher page:
https://doi.org/10.1016/j.tics.2025.10.011

The 2026 Trends in Cognitive Sciences article presents a theory-derived indicator method
for assessing AI systems under uncertainty. The repository does not convert those
indicators into a consciousness detector, subjectivity score, or automatic claim gate.

Repository transformation for historical-PR re-entry:

```text
INDICATOR_MATCH != CONSCIOUSNESS
INDICATOR_MATCH != SUBJECTIVITY
THEORY_DERIVED_PROPERTY != VALIDATED_DETECTOR
BEHAVIORAL_SIMILARITY != INTERNAL_MECHANISM
```

A future closed-PR idea that claims subjectivity relevance must therefore state its exact
theory/construct link, discriminating prediction, falsifier, alternatives and claim
ceiling before it can reach the existing Four-Domain design-admission surface.

## 3. 2026 indicator-validation / mimicry exchange — bounded metadata use

Pennartz, *How can we validate theory-derived indicators of consciousness in Artificial
Intelligence?*, Trends in Cognitive Sciences 30(7), 573-574 (2026).
DOI: https://doi.org/10.1016/j.tics.2026.01.011
PubMed: https://pubmed.ncbi.nlm.nih.gov/41820112/

Butlin et al., *Consciousness indicators, mimicry, and internal variants*, Trends in
Cognitive Sciences 30(7), 575-576 (2026).
DOI: https://doi.org/10.1016/j.tics.2026.04.006
PubMed: https://pubmed.ncbi.nlm.nih.gov/42036253/

The PubMed records expose bibliographic metadata but no abstract. This audit therefore
does **not** attribute detailed arguments from inaccessible full text. The titles and
verified publication relationship are used only as a conservative reminder that
indicator validation, behavioural mimicry and variation in internal implementation are
live methodological questions.

Repository-native re-entry fields added by this work:

```text
INDICATOR_VALIDATION_STATUS = REQUIRED
MIMICRY_ALTERNATIVE = REQUIRED
INTERNAL_VARIANT_ALTERNATIVE = REQUIRED
```

These fields are prompts for falsification and alternative explanation, not borrowed
conclusions and not positive evidence for artificial subjectivity.

## 4. COGITATE adversarial collaboration — discrimination over interpretive fit

Primary open-access article:
https://www.nature.com/articles/s41586-025-08888-1

The 2025 COGITATE collaboration preregistered contrasting predictions and interpretation
criteria for competing human consciousness theories and used multiple modalities and
independent data. It is a human neuroscience study, not evidence about AI systems.

The narrow methodological transfer is:

```text
HYPOTHESIS_COMPATIBILITY != HYPOTHESIS_DISCRIMINATION
POST_HOC_FIT != PREDECLARED_DIFFERENTIAL_PREDICTION
ONE_SUPPORTING_PATTERN != ALTERNATIVE_EXPLANATIONS_CLOSED
```

This aligns with the repository's existing interpretive-specificity note and supports the
requirement that a re-entered subjectivity question name discriminating predictions and
support-reducing conditions before implementation.

## Intake decision

No new raw external publication is required in Git history for this re-entry control.
The quality sources that require byte-level acquisition already have exact external-cache
receipts and derivative cards. The additional 2026 consciousness-method exchange is
retained here only as a metadata-bounded derivative reference because copying full text
would add legal/provenance cost without increasing the value of the control.

```text
RAW_EXTERNAL_PUBLICATION_IN_REPO = FALSE
DERIVATIVE_TRANSFORMATION = TRUE
CURRENT_MAIN_DEDUP = REQUIRED
HISTORICAL_PR_REENTRY = FAIL_CLOSED
```
