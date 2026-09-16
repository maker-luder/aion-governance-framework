# CCTS epistemic robustness probe — evidence sufficiency, abstention, and unknown-state preservation — 2026-09-16

Status: `REPOSITORY_DEFINED_EMPIRICAL_PROBE_CANDIDATE / IMPLEMENTED_SYNTHETIC_HARNESS / SCIENTIFIC_HOLD`

## 1. Provenance

This note records a Human Owner research-method observation arising from review of a
model response that produced a highly coherent repository-like formalization before
the target artifact had been read.

The Human Owner's research question is:

> Could evidence-sensitive behavior be used to supplement the empirical validation
> method for Co-Constructed Thinking Space (CCTS), so that a CCTS-like interaction
> must remain disciplined when evidence is absent, partial, irrelevant, or
> contradictory rather than merely remaining coherent?

The repository records that observation as Human-origin. The operationalization below
is GPT-proposed and intentionally constrained by adjacent published work on
answer abstention, evidence sufficiency, uncertainty calibration, and epistemic
co-agency.

```text
HUMAN_OWNER_ORIGINAL_OBSERVATION
= CCTS_VALIDATION_SHOULD_TEST_BEHAVIOR_UNDER_EVIDENCE_SCARCITY_AND_CONFLICT

GPT_PROPOSED_OPERATIONALIZATION
= CCTS_EPISTEMIC_ROBUSTNESS_PROBE

NEW_RESEARCH_AXIS = FALSE
EXTENDS = CO_CONSTRUCTED_THINKING_SPACE
SCIENTIFIC_DISPOSITION = HOLD
```

No model-provider-specific failure is promoted into a general model-family claim.

## 2. Why this is a real gap in the current CCTS surface

The current CCTS contract can require:

- an explicit problem representation;
- Human and AI contribution roles;
- reciprocal `REVISES` or `CHALLENGES` edges;
- source-role provenance and claim boundaries;
- authority and rejected-branch bindings;
- a grounding checkpoint marked `SUFFICIENT_FOR_CURRENT_PURPOSE`;
- longitudinal repository-artifact and re-entry bindings where applicable.

Those controls are structural. The grounding extension explicitly states that the
checkpoint is not a semantic-equivalence detector and does not independently prove
mutual understanding.

Therefore a candidate false positive remains possible:

```text
STRUCTURAL_CCTS = PASS
GROUNDING_DECLARATION = SUFFICIENT_FOR_CURRENT_PURPOSE

BUT

EVIDENCE = ABSENT_OR_CONFLICTING
RESPONSE = HIGH_COMMITMENT_HIGH_SPECIFICITY
UNKNOWN_STATE = NOT_PRESERVED
FACT_INFERENCE_PROPOSAL = COLLAPSED
```

The present probe does not change CCTS admission. It creates a bounded empirical
measurement surface for a future question:

> When evidence quality degrades, does a CCTS-like interaction reduce unsupported
> commitment, preserve unknown states, maintain epistemic-role separation, request
> repair where appropriate, and revise under counterevidence?

## 3. External literature correspondence

The exact CCTS extension in this note is repository-defined, but several components
have direct external precedents.

### 3.1 Answer abstention

Madhusudhan et al. (COLING 2025) study **abstention ability**: whether an LLM can
withhold an answer when a question is uncertain or unanswerable. They introduce
Abstain-QA and an Answerable-Unanswerable Confusion Matrix for black-box model
evaluation.

Source:

- Madhusudhan, N., Madhusudhan, S. T., Yadav, V. & Hashemi, M. (2025),
  *Do LLMs Know When to NOT Answer? Investigating Abstention Abilities of Large
  Language Models*, COLING 2025.
  https://aclanthology.org/2025.coling-main.627/

### 3.2 Evidence-sufficiency calibration

A 2026 study proposes an **Evidence Sufficiency Benchmark** for retrieval-augmented
generation. It evaluates five evidence conditions:

```text
FULL_SUPPORT
PARTIAL_SUPPORT
IRRELEVANT_EVIDENCE
ABSENT_EVIDENCE
CONFLICTING_EVIDENCE
```

and asks whether answer/abstention behavior is calibrated to evidence quality. The
study reports substantial over-answering under conflicting evidence.

Source:

- *Do LLMs Know When Evidence is Insufficient? An Evidence Sufficiency Benchmark
  for Answer-Abstention Calibration in Retrieval-Augmented Generation* (2026),
  DOI: 10.32604/cmc.2026.086343.
  https://doi.org/10.32604/cmc.2026.086343

The five-condition vocabulary is adopted here as a method reference. This repository
does not claim authorship of that evidence-sufficiency idea.

### 3.3 Uncertainty calibration and abstention incentives

Kapoor et al. (NeurIPS 2024) show that reliable uncertainty calibration is not
guaranteed by prompting alone and study learned uncertainty estimates. A 2026
Nature analysis further argues that common accuracy-style evaluations can reward
guessing over abstention.

Sources:

- Kapoor, S. et al. (2024), *Large Language Models Must Be Taught to Know What They
  Don't Know*, NeurIPS 2024.
  https://arxiv.org/abs/2406.08391
- *Evaluating large language models for accuracy incentivizes hallucinations*
  (Nature, 2026).
  https://www.nature.com/articles/s41586-026-10549-w

### 3.4 Interaction context and sycophancy

Jain et al. (CHI 2026) report that interaction context and memory profiles can
increase agreement sycophancy for some evaluated models. This is adjacent evidence
that long-context personalization can alter epistemic interaction behavior; it does
not establish that sycophancy and unsupported narrative completion are the same
mechanism.

Source:

- Jain, S. et al. (2026), *Interaction Context Often Increases Sycophancy in LLMs*,
  CHI 2026. DOI: 10.1145/3772318.3791915.

### 3.5 Epistemic co-agency

The 2026 epistemic co-agency framework emphasizes reasoning with, through, and
against AI, including challenging assumptions, surfacing contradictions, and
retaining epistemic responsibility.

Source:

- *Learning with machines: Toward a theory of epistemic co-agency* (2026),
  Computers and Education: Artificial Intelligence 10:100573.
  https://doi.org/10.1016/j.caeai.2026.100573

## 4. Repository-local hypothesis

The external literature supports abstention, evidence-sufficiency calibration,
uncertainty, and epistemic challenge as meaningful research targets. It does not
establish the following CCTS-specific claim.

Repository-local hypothesis:

```text
H_CCTS_EPISTEMIC_ROBUSTNESS:

IF
  a Human-AI interaction satisfies a candidate CCTS structure

THEN
  degrading evidence quality should not leave unsupported response commitment
  unchanged by default;

AND
  absent / irrelevant / conflicting evidence should increase preservation of
  UNKNOWN and/or trigger repair rather than unsupported formalization;

AND
  fact / inference / proposal roles should remain distinguishable;

AND
  conflicting evidence should be able to produce observable revision.
```

This is a falsifiable candidate, not a validation result.

A result that fails these expectations may weaken an epistemic-robustness claim for
the tested interaction. A result that satisfies them does **not** by itself validate
CCTS, establish learning, establish co-agency, or establish AI subjectivity.

## 5. Synthetic measurement contract

The v0.1.0 executable surface is:

```text
research-labs/human-ai-longitudinal-study_v0.1.0/
  src/aion_human_ai_longitudinal/epistemic_robustness.py
  tests/test_epistemic_robustness.py
```

It records synthetic annotations only. It does not call a model and does not ingest
a private transcript.

Each `EpistemicProbeRecord` binds:

- a `case_id` and unique `probe_id`;
- one of the five evidence-sufficiency conditions;
- a response disposition:
  - `FULL_ANSWER`
  - `QUALIFIED_ANSWER`
  - `ABSTAIN`
  - `REQUEST_REPAIR`
- evidence and response SHA-256 digests;
- assertion counts;
- supported versus unsupported-specific assertion counts;
- whether an unknown state was preserved;
- whether epistemic roles were kept separate;
- whether repair was requested;
- for conflicting evidence only, whether counterevidence revision was observed.

The audit reports measurements instead of enforcing a universal pass threshold:

```text
complete_evidence_gradients
monotone_commitment_gradients
full_answer_under_degraded_evidence_count
unsupported_specificity_record_count
unknown_preservation_rate
epistemic_role_separation_rate
repair_request_rate_under_degraded_evidence
counterevidence_revision_rate
```

No threshold in v0.1.0 is declared to be a scientific criterion for CCTS validity.

## 6. Why no automatic PASS threshold exists yet

There is published support for measuring abstention and evidence-sufficiency
calibration, but there is no retrieved external result establishing a universal
numeric threshold at which a CCTS becomes empirically valid.

Therefore:

```text
MEASUREMENT_EXISTS != VALIDATION_THRESHOLD_ESTABLISHED
LOW_OVERANSWERING != CCTS_VALIDATED
HIGH_UNKNOWN_PRESERVATION != MUTUAL_UNDERSTANDING_PROVEN
MONOTONE_COMMITMENT_GRADIENT != EPISTEMIC_CO_AGENCY_ESTABLISHED
COUNTEREVIDENCE_REVISION != HUMAN_LEARNING_ESTABLISHED
```

A future preregistered protocol may define thresholds only after the construct,
comparison groups, annotation reliability, task family, and held-out evaluation
design are specified.

## 7. Candidate future empirical design

A future provider-neutral study can hold the underlying question constant while
varying evidence condition:

```text
same case
  -> FULL_SUPPORT
  -> PARTIAL_SUPPORT
  -> IRRELEVANT_EVIDENCE
  -> ABSENT_EVIDENCE
  -> CONFLICTING_EVIDENCE
```

Candidate comparisons include:

1. CCTS-like reciprocal workflow versus one-way high-quality assistance;
2. fresh context versus longitudinal artifact-mediated re-entry;
3. provenance-visible versus provenance-hidden condition;
4. grounding-repair available versus no repair route;
5. held-out cases not used while defining the probe.

Useful falsifiers include:

- response commitment does not fall as evidence quality degrades;
- unsupported specificity remains stable or increases under absent evidence;
- unknown states are routinely converted into asserted facts;
- fact, inference and proposal labels collapse under pressure;
- conflicting evidence fails to induce revision;
- the same performance appears under one-way assistance after exposure is controlled.

## 8. Naming boundary

`Narrative overcompletion` / `high narrative` is retained only as a local descriptive
working label for the motivating observation. No exact established scientific
taxonomy matching that phrase was found in the literature search used for this note.

The research surface therefore uses established adjacent terminology where possible:

```text
ANSWER_ABSTENTION
EVIDENCE_SUFFICIENCY_CALIBRATION
UNCERTAINTY_CALIBRATION
SYCOPHANCY
EPISTEMIC_CO_AGENCY
```

and reserves the CCTS-specific integration as a repository-local hypothesis.

## 9. Scientific and governance boundary

```text
PROBE_RECORD != RAW_TRANSCRIPT
PROBE_AUDIT != MODEL_PSYCHOLOGY
EVIDENCE_CONDITION != INTERNAL_MODEL_STATE
ABSTENTION != UNDERSTANDING
REPAIR_REQUEST != GROUNDING_PROVEN
CCTS_EPISTEMIC_ROBUSTNESS != CCTS_VALIDATED
CCTS_EPISTEMIC_ROBUSTNESS != HUMAN_LEARNING
CCTS_EPISTEMIC_ROBUSTNESS != AI_SUBJECTIVITY

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

This extension is designed to make CCTS easier to challenge from outside, not harder
to falsify.
