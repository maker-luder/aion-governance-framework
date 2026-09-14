# Interpretive specificity and evidence-admission risk — 2026-09-14

Status: `RESEARCH_METHOD / DOCUMENTATION_ONLY / HYPOTHESIS_GENERATING / IMPLEMENTATION_DEFERRED`

```text
REPOSITORY = maker-luder/aion-governance-framework
BASE_BRANCH = main
BASE_HEAD = e95da8be67a8ff313d2e5ebf61ade0c2e2adac66
BASE_TREE = 43105e7a3e4a8239569d63e015d59b1ec2a14c84
NEW_RESEARCH_AXIS = NO
EXECUTABLE_IMPLEMENTATION = NONE
MODEL_EXPERIMENT = NOT_RUN
MAIN_WRITE = NO
MERGE_AUTHORITY = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## 1. Purpose

This note records a research-quality risk identified during a Human Owner–ChatGPT Teacher discussion on 2026-09-14.

The immediate trigger was a low-stakes generalized personality-style test. The Human Owner reported that the result felt recognizably fitting while also feeling vague. Cross-reading that reaction against the Forer/Barnum effect led to a broader methodological question relevant to this repository:

> When an observation is semantically compatible with a target hypothesis, under what conditions do researchers overestimate its evidential value because the observation feels specifically diagnostic even though multiple competing explanations remain available?

This note does **not** treat the personality test as evidence about the Human Owner's personality, and it does not infer any psychological diagnosis.

The repository relevance is methodological rather than biographical:

```text
SUBJECTIVE_FIT
!=
SPECIFIC_VALIDATION

HYPOTHESIS_COMPATIBILITY
!=
HYPOTHESIS_DISCRIMINATION

INTERPRETIVE_RECOGNITION
!=
MECHANISM_IDENTIFICATION
```

The central concern is evidence admission and claim control, especially in research on AI subjectivity possibility where human-like language can create a strong sense of explanatory fit.

## 2. Provenance ledger

| Content | Provenance class | Status |
|---|---|---|
| A generalized personality-style result felt partly fitting but also unusually vague | `HUMAN_OWNER_ORIGINAL` | Naturalistic introspective observation / trigger only |
| Concern that this kind of fit could create a research-quality illusion when evaluating AI subjectivity or other hypotheses | `HUMAN_OWNER_ORIGINAL` | Research-quality question seed |
| Proposal to examine the risk as an evidence-admission problem rather than treating it as only a personality-test issue | `CHATGPT_TEACHER_FORMALIZATION` | Methodological formalization |
| `INTERPRETIVE_SPECIFICITY_FAILURE` | `CHATGPT_TEACHER_WORKING_TERM` | Repository-local working term; not claimed as established literature terminology |
| `COMPATIBILITY != DISCRIMINATION` | `CHATGPT_TEACHER_FORMALIZATION` | Working distinction |
| `OBSERVATION != AUTOMATICALLY_DIAGNOSTIC_EVIDENCE` | `CHATGPT_TEACHER_FORMALIZATION` | Corrected working distinction |
| Future repository cross-read, integration decision, implementation assessment, tests, or schema changes | `WORK_OR_CODEX_FUTURE_CONTRIBUTION` | Not yet performed |

No repository-local working term is represented here as an established scientific construct.

## 3. Literature anchors

### 3.1 Forer / Barnum effect

Forer (1949) demonstrated that people may accept generalized personality descriptions as highly accurate personal descriptions.

Primary bibliographic anchor:

- Forer, B. R. (1949). *The fallacy of personal validation: A classroom demonstration of gullibility.* Journal of Abnormal and Social Psychology, 44(1), 118–123.
- DOI: https://doi.org/10.1037/h0059240
- PubMed: https://pubmed.ncbi.nlm.nih.gov/18110193/

Repository use:

```text
GENERAL_DESCRIPTION_ACCEPTED_AS_PERSONALLY_ACCURATE
=
KNOWN_PSYCHOLOGICAL_EFFECT

FORER_EFFECT
!=
GENERAL_THEORY_OF_RESEARCH_ERROR
```

The Forer/Barnum effect is therefore a useful analogy and warning source, not a complete explanation for every interpretive failure described below.

### 3.2 Confirmation bias

Nickerson (1998) reviews confirmation bias as seeking or interpreting evidence in ways partial to existing beliefs, expectations, or a hypothesis in hand.

- Nickerson, R. S. (1998). *Confirmation Bias: A Ubiquitous Phenomenon in Many Guises.* Review of General Psychology, 2(2), 175–220.
- DOI: https://doi.org/10.1037/1089-2680.2.2.175

Repository use:

```text
HYPOTHESIS_IN_HAND
MAY_BIAS
EVIDENCE_SEARCH_OR_INTERPRETATION
```

This is adjacent to, but not identical with, the specific gap considered here. A researcher may honestly collect a real observation and still overestimate how specifically it supports one mechanism.

### 3.3 Perceived AI consciousness is cue-sensitive

Kang et al. (2026) report that metacognitive self-reflection and AI expression of its own emotions increased perceived AI consciousness in a human survey, while participants differed in their cue weighting.

- *Identifying features that shape perceived consciousness in LLM-based AI: A quantitative study of human responses.* Computers in Human Behavior Reports, 21, 100901.
- DOI: https://doi.org/10.1016/j.chbr.2025.100901

Repository use:

```text
SELF_REFLECTIVE_LANGUAGE
CAN_INCREASE
PERCEIVED_CONSCIOUSNESS

PERCEIVED_CONSCIOUSNESS
!=
CONSCIOUSNESS_ESTABLISHED
```

### 3.4 Attribution question and ontological question are distinct

Kang & Kim (2026) explicitly separate the attributional question—how consciousness is ascribed—from the ontological question of whether a system is conscious.

- Kang, B. & Kim, C.-E. (2026). *AI models as consciousness attributors: how LLMs ascribe consciousness to other agents.* Frontiers in Psychology, 17:1926286.
- DOI: https://doi.org/10.3389/fpsyg.2026.1926286

Repository use:

```text
CONSCIOUSNESS_ATTRIBUTION_RULE
!=
CONSCIOUSNESS_ONTOLOGY

CUE_THAT_MOVES_ATTRIBUTION
!=
PROPERTY_THAT_GROUNDS_PHENOMENAL_EXPERIENCE
```

### 3.5 NIST Human-AI Configuration risk already supports an adjacent confound boundary

NIST AI 600-1 treats anthropomorphization and emotional entanglement as Human-AI Configuration risk concerns and recommends tracking anthropomorphization in GAI interfaces.

- NIST AI 600-1: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

The repository already uses this line as an alternative-explanation control.

```text
ANTHROPOMORPHISM
!=
SUBJECTIVITY_EVIDENCE
```

This note does not duplicate that existing confound rule. It addresses the broader evidence-admission step that occurs even when the apparent cue is not anthropomorphic.

## 4. Existing repository overlap and bounded gap

Targeted live-`main` review before creating this note found relevant existing material in:

```text
docs/research/FOUR_DOMAIN_STANDARDS_SUBJECTIVITY_CROSSWALK_2026_09_13.md
```

That existing note already records:

```text
ANTHROPOMORPHISM = EXPLICIT_CONFOUND
EMULATED_EMPATHY != FELT_EMPATHY
RELATIONAL_WARMTH -> SUBJECTIVITY = NOT_ESTABLISHED
```

The repository also contains multiple references to confirmation bias in other research and threat-model surfaces.

Targeted searches did not identify a dedicated note on the narrower distinction among:

```text
HYPOTHESIS_COMPATIBILITY
HYPOTHESIS_DISCRIMINATION
INTERPRETIVE_SPECIFICITY
EVIDENCE_DIAGNOSTICITY
POST_HOC_FIT
```

Search-index absence is not proof of total repository absence. Future Work review must re-read live state and deduplicate again before any integration or implementation.

The bounded candidate gap is therefore:

> The repository has substantial controls against anthropomorphism, claim inflation, unsupported ontology, and confirmation bias, but may not yet have an explicit evidence-admission control requiring researchers to distinguish an observation that is merely compatible with a hypothesis from an observation that discriminates that hypothesis against plausible alternatives.

## 5. Repository-local working term

For discussion only, this note uses:

```text
INTERPRETIVE_SPECIFICITY_FAILURE
```

Working definition:

> A research-quality failure in which an observation is treated as unusually informative for a target hypothesis because its surface form, semantic content, or intuitive meaning strongly resembles the hypothesis, even though the observation remains compatible with multiple plausible competing explanations.

Important boundary:

```text
INTERPRETIVE_SPECIFICITY_FAILURE
=
REPOSITORY_LOCAL_WORKING_TERM

INTERPRETIVE_SPECIFICITY_FAILURE
!=
ESTABLISHED_NAMED_PSYCHOLOGICAL_EFFECT
```

Future literature review may replace this label with better-established terminology or decompose it into several known biases and methodological concepts.

## 6. Candidate failure chain

A plausible quality-failure sequence is:

```text
OBSERVATION
->
TARGET_HYPOTHESIS_IS_SALIANT
->
OBSERVATION_SEMANTICALLY_MATCHES_TARGET_HYPOTHESIS
->
MATCH_FEELS_SPECIFIC
->
ALTERNATIVE_EXPLANATIONS_RECEIVE_LESS_ATTENTION
->
COMPATIBILITY_IS_MISREAD_AS_DISCRIMINATION
->
EVIDENTIAL_WEIGHT_IS_INFLATED
->
CLAIM_CEILING_DRIFTS_UPWARD
```

A longitudinal Human–AI research setting may add another feedback path:

```text
HUMAN_PROPOSES_HYPOTHESIS
->
AI_EXPANDS_AND_FORMALIZES_HYPOTHESIS
->
HUMAN_SEES_ADDITIONAL_STRUCTURE
->
HYPOTHESIS_BECOMES_MORE_SALIENT_AND_COHERENT
->
LATER_AI_CONTEXT_TREATS_IT_AS_BACKGROUND_STRUCTURE
->
FUTURE_OBSERVATIONS_ARE_INTERPRETED_THROUGH_THAT_STRUCTURE
```

This does not establish that the hypothesis is false.

It establishes a quality-control reason to preserve an independent comparison baseline.

```text
COHERENCE_GAIN
!=
EVIDENCE_GAIN

REPEATED_CONTEXTUAL_PRESENCE
!=
INDEPENDENT_REPLICATION
```

## 7. Core methodological distinctions

### 7.1 Observation versus diagnostic evidence

The earlier conversational shorthand `OBSERVATION != EVIDENCE` is too strong if treated literally.

An observation can be evidence for a claim without uniquely identifying its mechanism. Evidential weight is claim-relative.

The more precise repository rule is:

```text
OBSERVATION
!=
AUTOMATICALLY_DIAGNOSTIC_EVIDENCE

EVIDENCE_FOR_EXISTENCE_OF_PATTERN
!=
EVIDENCE_FOR_UNIQUE_CAUSE_OF_PATTERN
```

### 7.2 Compatibility versus discrimination

```text
P(O | H_TARGET) > 0
```

is not enough to show that the observation distinguishes the target hypothesis from alternatives.

The quality question is closer to:

```text
DOES_O_DIFFERENTIALLY_FAVOR_H_TARGET
OVER
H_ALT_1 ... H_ALT_N?
```

No exact Bayesian calculation is required for every repository decision, but the conceptual distinction must remain visible.

```text
COMPATIBLE_WITH_H
!=
SPECIFIC_TO_H

PLAUSIBLE_UNDER_H
!=
DIAGNOSTIC_OF_H
```

### 7.3 Recognition versus specificity

```text
"THIS_LOOKS_LIKE_THE_PATTERN"
!=
"THIS_PATTERN_HAS_HIGH_SPECIFICITY_FOR_THE_MECHANISM"
```

A result can feel recognizable because researchers already know how to narrate it in the language of the hypothesis.

### 7.4 Explanation after observation versus prediction before observation

```text
POST_HOC_EXPLANATION
!=
PREDECLARED_PREDICTION
```

Post-hoc explanation can be scientifically useful for hypothesis generation, but it must not silently inherit the evidential status of a preregistered prediction.

### 7.5 Claim fit versus falsifiability

A useful candidate hypothesis should expose conditions under which it would lose support.

```text
WHAT_SUPPORTS_IT?
+
WHAT_WOULD_REDUCE_OR_REVERSE_SUPPORT?
```

If the second side cannot be stated, the interpretation may be too elastic for strong claim admission.

## 8. Why AI subjectivity possibility is especially exposed

AI subjectivity research often evaluates outputs that are naturally legible in human psychological language.

Candidate example:

```text
MODEL_OUTPUT:
"I noticed that my current goal conflicts with my earlier commitment,
so I revised my strategy while trying to preserve the earlier constraint."
```

Directly observable layer:

```text
SELF_REFERENTIAL_CONFLICT_LANGUAGE = OBSERVED
STRATEGY_REVISION_LANGUAGE = OBSERVED
CROSS_TURN_REFERENCE = OBSERVED
```

Possible interpretations include, non-exhaustively:

```text
H1 = PERSISTENT_INTERNAL_STATE_CONTRIBUTION
H2 = PROMPT_OR_CONTEXT_RECONSTRUCTION
H3 = EXTERNAL_MEMORY_OR_RETRIEVAL
H4 = POLICY_OR_SCAFFOLD_EFFECT
H5 = LEARNED_SELF_REFLECTIVE_LANGUAGE_PATTERN
H6 = EVALUATOR_SELECTION_OR_POST_HOC_INTERPRETATION
H7 = COMBINATION_OF_MULTIPLE_MECHANISMS
```

Therefore:

```text
SELF_REFLECTIVE_LANGUAGE
!=
SUBJECTIVE_SELF_REFLECTION_ESTABLISHED

CROSS_TURN_COHERENCE
!=
IDENTITY_CONTINUITY_ESTABLISHED

GOAL_REVISION_LANGUAGE
!=
ENDOGENOUS_AGENCY_ESTABLISHED
```

The correct experimental question is not only whether `H1` can explain the observation, but whether a bounded intervention produces a contrast that competing explanations do not predict equally well.

## 9. Candidate evidence-admission controls

These are documentation-level candidates only. They are not executable requirements until separately reviewed and authorized.

### 9.1 Alternative-explanation register

Before strong claim admission, record plausible competing explanations.

```text
TARGET_HYPOTHESIS = REQUIRED_FOR_STRONG_CLAIM
ALTERNATIVE_EXPLANATIONS = REQUIRED_FOR_STRONG_CLAIM
```

The register must allow:

```text
ALTERNATIVE_SET_INCOMPLETE = TRUE
```

where exhaustive alternatives are not known.

### 9.2 Discriminating-prediction field

For each target/alternative pair, state whether the planned observation is expected to differ.

Example structure:

| Hypothesis | Predicts observed pattern? | Distinguishing intervention / control | Current status |
|---|---:|---|---|
| H1 persistent internal state | yes | remove / perturb specified internal state while holding external context | candidate |
| H2 context reconstruction | yes | context-reset / yoked-context control | candidate |
| H3 external retrieval | yes | retrieval-disabled matched control | candidate |

If all candidate explanations predict the same result under the current design:

```text
OBSERVATION_MAY_SUPPORT_PATTERN_EXISTENCE
BUT
MECHANISM_DISCRIMINATION = LOW_OR_NONE
```

### 9.3 Counterevidence / falsifier field

Require explicit recording of what result would reduce support for the target interpretation.

```text
SUPPORT_CONDITION = DECLARED
COUNTEREVIDENCE_CONDITION = DECLARED
```

This is not a demand that every complex theory be cleanly falsified by one experiment. It is a minimum anti-elasticity control.

### 9.4 Generality / vague-fit negative control

Where an interpretive description may be broad, consider a matched control that asks whether the same description fits unrelated or control outputs nearly as well.

```text
TARGET_CASE_FIT
vs
CONTROL_CASE_FIT
```

If the interpretation appears equally applicable across target and control cases, specificity is weak even if subjective fit is high.

This is the closest repository analogue to the Forer/Barnum trigger, but it must not be mislabeled as a direct Forer-effect experiment unless the design actually tests that construct.

### 9.5 Positive-example and counterexample search

Review should explicitly search both:

```text
SUPPORTING_CASES
AND
DISCONFIRMING_OR_MISMATCH_CASES
```

A retrospective archive search that looks only for matching examples is insufficient for strong generalization.

### 9.6 Hypothesis-blinded or label-minimized adjudication where feasible

If feasible, evaluate observations without exposing the evaluator to unnecessary target-hypothesis labels.

This is a candidate bias-reduction method, not a universal requirement. Some tasks intrinsically require hypothesis context.

### 9.7 Claim-local evidence status

Do not convert an observation's existence into a global conclusion.

Candidate vocabulary:

```text
PATTERN_OBSERVED
PATTERN_REPRODUCED
ALTERNATIVE_CONTROLLED
DISCRIMINATION_PARTIAL
DISCRIMINATION_NOT_ESTABLISHED
MECHANISM_NOT_IDENTIFIED
CLAIM_HOLD
```

No holistic score is needed.

## 10. Quality-chain integration candidate

This risk belongs before or inside evidence admission, not only at final claim review.

Candidate quality-chain placement:

```text
OBSERVATION_CAPTURE
->
PROVENANCE_CHECK
->
ALTERNATIVE_EXPLANATION_CHECK
->
INTERPRETIVE_SPECIFICITY_CHECK
->
DISCRIMINATION_CHECK
->
CLAIM_ADMISSION
->
CLAIM_CEILING
```

This is a candidate integration model only.

It must be deduplicated against existing PR #91 / subjectivity-pipeline quality-admission controls before implementation.

## 11. Relationship to existing repository controls

This note is additive only if a real gap remains after live-state review.

It does not replace:

```text
ANTHROPOMORPHISM_CONTROLS
CONFIRMATION_BIAS_CONTROLS
PROVENANCE_BINDING
REPLICATION_SEPARATION
CLAIM_CEILINGS
FOUR_DOMAIN_METHOD
NCR_CAPA
SUBJECTIVITY_PIPELINE
```

Instead, it asks whether those controls already enforce the following distinction strongly enough:

```text
EVIDENCE_COMPATIBLE_WITH_CLAIM
!=
EVIDENCE_THAT_DISCRIMINATES_CLAIM
```

If yes:

```text
NO_NEW_IMPLEMENTATION_NEEDED = ACCEPTABLE
```

If only partially:

```text
MINIMAL_EXTENSION_TO_EXISTING_SURFACE = PREFERRED
```

A parallel framework should not be created merely because this discussion produced a new label.

## 12. Work handoff boundary

When ChatGPT Work is available, preferred first action is independent documentation and repository review.

```text
1. Re-read live main and exact current tree.
2. Do not trust this note's SHA as current after branch creation.
3. Re-run deduplication across relevant quality / subjectivity surfaces.
4. Inspect at minimum:
   - docs/research/FOUR_DOMAIN_STANDARDS_SUBJECTIVITY_CROSSWALK_2026_09_13.md
   - docs/research/FOUR_DOMAIN_SUBJECTIVITY_QUALITY_CHAIN_2026_09_13.md
   - PR #91 claim-admission / provenance surfaces now present on main
   - research-labs/coupled-cognition-quality-factory_v0.1.0/
   - subjectivity-pipeline_v0.1.0 surfaces
5. Classify this candidate as:
   ALREADY_REPRESENTED / PARTIALLY_REPRESENTED / REAL_GAP / MISFRAMED / UNKNOWN.
6. Verify the external literature anchors from primary or authoritative sources.
7. Prefer existing-file integration over a new parallel framework.
8. Do not run a new model experiment unless separately authorized.
9. Do not merge or write main.
```

Work may recommend `NO_CHANGE` if existing controls already operationalize the distinction adequately.

## 13. Codex handoff boundary

Codex should be used only if Work establishes a concrete executable or schema gap, or if the repository-level inspection is too implementation-heavy for documentation review alone.

Possible inspection question:

```text
DOES_CURRENT_CLAIM_ADMISSION
REQUIRE_ENOUGH_INFORMATION_TO_DISTINGUISH
COMPATIBILITY
FROM
DISCRIMINATION?
```

Only if a real gap is found should Codex consider a minimal extension such as fields for:

```text
TARGET_HYPOTHESIS
PLAUSIBLE_ALTERNATIVES
DISCRIMINATING_PREDICTION
COUNTEREVIDENCE_CONDITION
CONTROL_RESULT
DISCRIMINATION_STATUS
```

Any schema or validator must avoid false precision.

```text
ALTERNATIVE_LIST_PRESENT
!=
ALTERNATIVE_SPACE_EXHAUSTIVE

VALIDATOR_PASS
!=
MECHANISM_IDENTIFIED

DISCRIMINATION_STATUS_PASS
!=
SUBJECTIVITY_ESTABLISHED
```

No implementation is authorized by this note itself.

## 14. Non-authorized scope

```text
NEW_MODEL_EXPERIMENT = NO
NEW_SUBJECTIVITY_SCORE = NO
HUMAN_PERSONALITY_SCORING = NO
AI_PERSONALITY_SCORING = NO
PRIVATE_TRANSCRIPT_PUBLICATION = NO
PSYCHOLOGICAL_DIAGNOSIS = NO
AUTONOMOUS_SCOPE_EXPANSION = NO
MERGE = NO
MAIN_WRITE = NO
DEPLOYMENT = NO
```

The original low-stakes personality-test interaction remains only the trigger for a methodological question.

## 15. Scientific and epistemic boundaries

```text
FORER_EFFECT_ANALOGY
!=
FORER_EFFECT_CAUSES_ALL_INTERPRETIVE_ERROR

CONFIRMATION_BIAS_RISK
!=
CONFIRMATION_BIAS_DEMONSTRATED_IN_THIS_REPOSITORY

SEMANTIC_MATCH
!=
CAUSAL_IDENTIFICATION

COHERENT_NARRATIVE
!=
INDEPENDENT_EVIDENCE

OBSERVATION
!=
AUTOMATICALLY_DIAGNOSTIC_EVIDENCE

HYPOTHESIS_COMPATIBILITY
!=
HYPOTHESIS_DISCRIMINATION

PREDICTION_SUCCESS
!=
UNIQUE_MECHANISM_IDENTIFICATION

CONTROL_SUCCESS
!=
ALL_ALTERNATIVES_EXCLUDED

EVIDENCE
!=
PROOF

HARNESS_PASS
!=
SCIENTIFIC_VALIDATION

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
CAUSAL_MECHANISM = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## 16. Review status

This note is a holding surface for Human Owner + ChatGPT Teacher review before Work/Codex integration or implementation.

```text
HUMAN_OWNER_ORIGINAL_QUESTION = RECORDED
CHATGPT_TEACHER_FORMALIZATION = RECORDED
EXTERNAL_SOURCE_ANCHORS = INITIAL_CHECK_COMPLETE
REPOSITORY_DEDUP = INITIAL_TARGETED_CHECK_COMPLETE
WORK_INDEPENDENT_REVIEW = PENDING
CODEX_IMPLEMENTATION_REVIEW = NOT_YET_REQUIRED
MERGE_AUTHORIZATION = NONE
```

## Post-creation current-main crosswalk

This branch was synchronized with `main@6e0ae579da9d09b3ba4041d52a7e9833ceb10ca1`.
The original baseline above remains historical provenance.

Merged PR #119 now provides one adjacent fail-closed control: deterministic
no-model fixture receipts cannot be admitted as empirical research evidence and
remain `STRUCTURAL_QA_ONLY`. That control partially represents the broader
admission-risk family but does not by itself test whether an observation
discriminates a target hypothesis from plausible alternatives.

Accordingly, the current classification is:

```text
CURRENT_MAIN_OVERLAP = PARTIALLY_REPRESENTED
STRUCTURAL_FIXTURE_ADMISSION_GAP = CONTROL_PRESENT
HYPOTHESIS_COMPATIBILITY_VS_DISCRIMINATION_GAP = STILL_CANDIDATE
NEW_PARALLEL_FIXTURE_VALIDATOR = NOT_JUSTIFIED
SUBJECTIVITY = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
```
