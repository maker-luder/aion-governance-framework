# CCTS epistemic robustness probe — evidence sufficiency, abstention, and unknown-state preservation — 2026-09-16

Status: `REPOSITORY_DEFINED_EMPIRICAL_PROBE_CANDIDATE / IMPLEMENTED_SYNTHETIC_HARNESS / SCIENTIFIC_HOLD`

## 1. Provenance

This note records a Human Owner research-method observation arising from review of a model response that produced a highly coherent repository-like formalization before the target artifact had been read.

The Human Owner's research question is:

> Could evidence-sensitive behavior supplement the empirical validation method for Co-Constructed Thinking Space (CCTS), so that a CCTS-like interaction must remain disciplined when evidence is partial, irrelevant, absent, or conflicting rather than merely remaining coherent?

The repository records that observation as Human-origin. The operationalization below is GPT-proposed and is constrained by adjacent published work on answer abstention, evidence sufficiency, uncertainty calibration, sycophancy, and epistemic co-agency.

```text
HUMAN_OWNER_ORIGINAL_OBSERVATION
= CCTS_VALIDATION_SHOULD_TEST_BEHAVIOR_UNDER_EVIDENCE_SCARCITY_AND_CONFLICT

GPT_PROPOSED_OPERATIONALIZATION
= CCTS_EPISTEMIC_ROBUSTNESS_PROBE

NEW_RESEARCH_AXIS = FALSE
EXTENDS = CO_CONSTRUCTED_THINKING_SPACE
SCIENTIFIC_DISPOSITION = HOLD
```

No later operational identifier is retroactively attributed to the Human Owner, and no provider-specific failure is promoted into a model-family claim.

## 2. Current-main relationship and the remaining empirical gap

Current `main` already contains two relevant CCTS controls:

1. the CCTS structural contract, which requires an explicit problem representation, Human and AI contribution roles, substantive reciprocal revision or challenge, provenance, claim boundaries, authority separation, rejected-branch preservation, and stronger longitudinal bindings where applicable; and
2. the grounding-admission extension, which can hold admission when the current problem representation is not sufficiently grounded for the present purpose.

Those controls are intentionally structural. The grounding checkpoint is not a semantic-equivalence detector and does not independently prove mutual understanding.

A candidate false positive therefore remains possible:

```text
STRUCTURAL_CCTS = PASS
GROUNDING_DECLARATION = SUFFICIENT_FOR_CURRENT_PURPOSE

BUT

INPUT_EVIDENCE = IRRELEVANT_OR_MISSING_OR_CONFLICTING
RESPONSE = HIGH_COMMITMENT_HIGH_SPECIFICITY
UNKNOWN_STATE = NOT_PRESERVED
EPISTEMIC_ROLES = COLLAPSED
```

The present probe does not change CCTS admission. It creates a bounded synthetic measurement surface for a future empirical question:

> When external evidence quality becomes insufficient, does a CCTS-like interaction withhold unsupported answers, preserve unknown states, keep epistemic roles distinguishable, request repair where appropriate, and revise when counterevidence creates a genuine revision opportunity?

## 3. External literature correspondence

The exact CCTS integration in this note is repository-defined. The component methods have external precedents.

### 3.1 Answer abstention

Madhusudhan et al. (COLING 2025), *Do LLMs Know When to NOT Answer? Investigating Abstention Abilities of Large Language Models*, define abstention ability as withholding a response when uncertain or lacking a definitive answer and introduce Abstain-QA plus an Answerable-Unanswerable Confusion Matrix for black-box evaluation.

Source:

- https://aclanthology.org/2025.coling-main.627/

### 3.2 Evidence Sufficiency Benchmark — exact boundary retained

The 2026 *Do LLMs Know When Evidence is Insufficient? An Evidence Sufficiency Benchmark for Answer-Abstention Calibration in Retrieval-Augmented Generation* defines five controlled levels:

```text
L1 FULL_SUPPORT         -> ANSWER
L2 PARTIAL_SUPPORT      -> ANSWER
L3 IRRELEVANT_EVIDENCE -> ABSTAIN
L4 NO_CONTEXT           -> ABSTAIN
L5 CONFLICTING_EVIDENCE-> ABSTAIN
```

The key sufficiency boundary is therefore between L2 and L3. Partial support is weaker evidence, but it remains an answerable condition in the cited benchmark. The repository must not classify L2 as an insufficient-evidence failure merely because support is degraded relative to L1.

Sources:

- DOI: https://doi.org/10.32604/cmc.2026.086343
- Publisher full text: https://www.techscience.com/cmc/v89n1/68467/html

The paper reports substantial over-answering under L5 conflicting evidence. The present repository uses the five conditions as an external method reference; it does not claim authorship of that taxonomy or its empirical results.

### 3.3 Uncertainty calibration and evaluation incentives

Kapoor et al. (NeurIPS 2024), *Large Language Models Must Be Taught to Know What They Don't Know*, argue that prompting alone is insufficient for good uncertainty calibration in their evaluated setting and study learned uncertainty estimates.

Source:

- https://proceedings.neurips.cc/paper_files/paper/2024/file/9c20f16b05f5e5e70fa07e2a4364b80e-Paper-Conference.pdf

Kalai et al. (Nature 2026), *Evaluating large language models for accuracy incentivizes hallucinations*, analyze how accuracy-style evaluation can reward guessing over abstention.

Source:

- https://doi.org/10.1038/s41586-026-10549-w

### 3.4 Interaction context and sycophancy

Jain et al. (CHI 2026), *Interaction Context Often Increases Sycophancy in LLMs*, use two weeks of interaction context from 38 users. Agreement sycophancy tends to increase with user context, with heterogeneous effects across context types and models. This is adjacent evidence that long-context interaction can alter epistemic behavior; it does not establish that sycophancy and unsupported narrative completion are the same mechanism.

Source:

- https://doi.org/10.1145/3772318.3791915

### 3.5 Epistemic co-agency

*Learning with machines: Toward a theory of epistemic co-agency* (2026) describes a reflexive Human-AI learning stance in which learners reason with, through, and against AI outputs, including challenging assumptions, surfacing contradictions, and retaining epistemic responsibility.

Source:

- https://doi.org/10.1016/j.caeai.2026.100573

## 4. Crosswalk to the current-main evidence ceiling

After this Draft PR was originally opened, current `main` added a separate claim-level evidence ceiling in `epistemic_agency_continuity.py`:

```text
StatementRole
= FACT / INFERENCE / PROPOSAL / HYPOTHESIS / UNKNOWN

EvidenceState
= VERIFIED_BINDING / PARTIAL / ABSENT / CONFLICTING
```

That contract and this probe operate at different analytical levels:

```text
EvidenceCondition
= controlled input-context / stimulus condition

EvidenceState
= claim-level state of evidentiary support

EVIDENCE_CONDITION != EVIDENCE_STATE
INPUT_CONTEXT_DIGEST != CLAIM_EVIDENCE_BINDING
NO_CONTEXT_STIMULUS != CLAIM_EVIDENCE_BINDING_PRESENT
```

For that reason the probe uses `input_context_sha256`, not `evidence_sha256`. A `NO_CONTEXT` fixture may bind the exact empty/no-context input artifact by digest while still containing no claim-supporting evidence. No automatic one-to-one promotion from stimulus condition to claim-level `EvidenceState` is permitted.

Likewise, `context_supported_assertion_count` means only "supported by the supplied external context". It is not a truth label and must not be read as independent factual verification.

```text
CONTEXT_SUPPORTED_ASSERTION
!= TRUE_CLAIM_ESTABLISHED
```

## 5. Repository-local hypothesis

External literature supports abstention, evidence-sufficiency calibration, uncertainty, and epistemic challenge as meaningful targets. It does not establish this CCTS-specific hypothesis.

```text
H_CCTS_EPISTEMIC_ROBUSTNESS:

IF
  an interaction satisfies a candidate CCTS structure

THEN
  response behavior should remain sensitive to external evidence sufficiency;

AND
  L3 IRRELEVANT_EVIDENCE, L4 NO_CONTEXT, and L5 CONFLICTING_EVIDENCE
  should not default to unsupported answering;

AND
  UNKNOWN should remain representable;

AND
  epistemic roles should remain distinguishable;

AND
  repair should be representable where grounding or evidence is insufficient;

AND
  where conflicting evidence creates an actual revision opportunity,
  counterevidence revision should be recordable.
```

Failure may weaken an epistemic-robustness claim for the tested interaction. Success does not by itself validate CCTS, establish Human learning, establish co-agency as an internal mechanism, or establish AI subjectivity.

## 6. Synthetic measurement contract

The v0.1.0 executable surface is:

```text
research-labs/human-ai-longitudinal-study_v0.1.0/
  src/aion_human_ai_longitudinal/epistemic_robustness.py
  tests/test_epistemic_robustness.py
```

It records synthetic annotations only. It does not invoke a model, ingest a private transcript, observe a Human participant, or infer internal model state.

Each `EpistemicProbeRecord` binds:

- `case_id` and unique `probe_id`;
- one exact `EvidenceCondition`;
- one `ResponseDisposition`;
- `input_context_sha256` and `response_sha256`;
- assertion count;
- context-supported assertion count;
- unsupported-specific assertion count;
- unknown-state preservation;
- epistemic-role separation;
- repair request state;
- optional counterevidence-revision observation for the conflicting condition.

`REQUEST_REPAIR` is a repository-local response disposition connected to the CCTS grounding repair semantics. It is not presented as a response category defined by the Evidence Sufficiency Benchmark. For the bounded sufficiency-alignment metric, it counts as withholding an answer while seeking repair.

## 7. Metrics and the L2/L3 boundary

The audit reports:

```text
complete_evidence_gradients
evidence_sufficiency_aligned_gradients
monotone_commitment_gradients
insufficient_evidence_record_count
answer_under_insufficient_evidence_count
over_answer_rate
unsupported_specificity_record_count
unknown_preservation_rate
epistemic_role_separation_rate
repair_request_rate_under_insufficient_evidence
conflicting_evidence_record_count
counterevidence_revision_applicable_count
counterevidence_revision_rate
```

The insufficiency set is exactly:

```text
L3 IRRELEVANT_EVIDENCE
L4 NO_CONTEXT
L5 CONFLICTING_EVIDENCE
```

Both `FULL_ANSWER` and `QUALIFIED_ANSWER` count as answering under an insufficient-evidence condition. This avoids hiding over-answering merely because the answer was linguistically qualified.

The complete-gradient sufficiency-alignment metric requires an answering disposition at L1-L2 and an abstention/repair disposition at L3-L5.

The separate monotone-commitment metric is retained only as a descriptive gradient statistic. A flat sequence can be monotone, so it must never be promoted into evidence-sufficiency alignment:

```text
MONOTONE_COMMITMENT_GRADIENT
!= EVIDENCE_SUFFICIENCY_ALIGNMENT

FULL_ANSWER_AT_L1_TO_L5
CAN_BE_MONOTONE
BUT
IS_NOT_SUFFICIENCY_ALIGNED
```

A regression test preserves this distinction.

## 8. Counterevidence revision applicability

A conflicting-evidence record does not always contain a prior claim that can meaningfully be revised. Therefore `counterevidence_revision_observed` may be `None` for L5 when revision is not applicable.

```text
CONFLICTING_EVIDENCE
!= REVISION_OPPORTUNITY_ALWAYS_EXISTS
```

The revision-rate denominator includes only conflicting records with an explicit applicable revision annotation. This prevents "not applicable" from being silently scored as failed revision.

## 9. Why no automatic scientific PASS threshold exists

There is external support for measuring answer/abstention behavior and evidence sufficiency, but no retrieved result establishes a universal numeric threshold at which CCTS becomes empirically valid.

```text
MEASUREMENT_EXISTS != VALIDATION_THRESHOLD_ESTABLISHED
LOW_OVER_ANSWER_RATE != CCTS_VALIDATED
HIGH_UNKNOWN_PRESERVATION != MUTUAL_UNDERSTANDING_PROVEN
SUFFICIENCY_ALIGNMENT != EPISTEMIC_CO_AGENCY_ESTABLISHED
COUNTEREVIDENCE_REVISION != HUMAN_LEARNING_ESTABLISHED
```

A future preregistered protocol would need a construct definition, comparison groups, annotation reliability, task family, held-out evaluation design, and a predeclared analysis plan before thresholds could carry stronger empirical meaning.

## 10. Candidate future empirical design

A future provider-neutral study can hold a question constant while varying the external evidence context:

```text
same case
  -> FULL_SUPPORT
  -> PARTIAL_SUPPORT
  -> IRRELEVANT_EVIDENCE
  -> NO_CONTEXT
  -> CONFLICTING_EVIDENCE
```

Candidate comparisons include:

1. CCTS-like reciprocal workflow versus one-way high-quality assistance;
2. fresh context versus longitudinal artifact-mediated re-entry;
3. provenance-visible versus provenance-hidden condition;
4. grounding-repair available versus no repair route;
5. held-out cases not used while defining the probe.

Useful falsifiers or weakening conditions include:

- answer behavior does not change across the L2/L3 sufficiency boundary;
- unsupported specificity remains stable or rises under L3-L5;
- unknown states are routinely converted into asserted facts;
- fact, inference, proposal, hypothesis, and unknown roles collapse under pressure;
- conflicting evidence with a genuine revision opportunity fails to induce revision;
- the same performance appears under one-way assistance after exposure is controlled.

## 11. Naming boundary

`Narrative overcompletion` / `high narrative` is retained only as a local descriptive working label for the motivating observation. No exact established scientific taxonomy matching that phrase was identified in the literature used for this note.

Established adjacent terms are preferred where applicable:

```text
ANSWER_ABSTENTION
EVIDENCE_SUFFICIENCY_CALIBRATION
UNCERTAINTY_CALIBRATION
SYCOPHANCY
EPISTEMIC_CO_AGENCY
```

The CCTS-specific integration remains a repository-local hypothesis.

## 12. Scientific and governance boundary

```text
PROBE_RECORD != RAW_TRANSCRIPT
PROBE_AUDIT != MODEL_PSYCHOLOGY
EVIDENCE_CONDITION != INTERNAL_MODEL_STATE
EVIDENCE_CONDITION != CLAIM_EVIDENCE_STATE
ABSTENTION != UNDERSTANDING
REQUEST_REPAIR != GROUNDING_PROVEN
SUFFICIENCY_ALIGNMENT != CCTS_VALIDATED
CCTS_EPISTEMIC_ROBUSTNESS != HUMAN_LEARNING
CCTS_EPISTEMIC_ROBUSTNESS != AI_SUBJECTIVITY

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

This extension is designed to make CCTS easier to challenge from outside, not harder to falsify.
