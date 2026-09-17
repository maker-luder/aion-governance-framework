# Human–AI learning / HTECR provenance supplement — 2026-09-18

Status: `PROVENANCE_CORRECTION / RESEARCH_METHOD_NOTE / SCIENTIFIC_HOLD`
Canonical effect: `NONE`
Deployment: `FALSE`

## 1. Purpose

This supplement corrects a provenance omission identified during pre-merge review of PR #153.

The primary PR #153 note correctly preserves two source roles:

1. Human Owner origin for the observation and phrase `效能全開`; and
2. ChatGPT Teacher origin for the formal working label `HIGH-THROUGHPUT EPISTEMIC COORDINATION REGIME (HTECR) / 高吞吐知識協作狀態`.

However, that two-part attribution is incomplete for the **research question, narrowing, falsification logic and method direction** that emerged after the initial observation. Existing repository provenance rules already distinguish:

```text
HUMAN_ORIGIN
AI_FORMALIZATION
JOINT_SYNTHESIS
EXTERNAL_SOURCE
UNKNOWN
```

Therefore PR #153 must not imply a simple pipeline of:

```text
HUMAN_SUPPLIES_OBSERVATION
-> AI_DOES_THE_RESEARCH
```

The actual local research process is better represented as reciprocal, source-preserving co-inquiry in which Human and ChatGPT Teacher contributions remain distinguishable while some later research propositions are jointly synthesized.

## 2. Repository ancestry requiring this correction

### 2.1 Epistemic provenance ledger

`research-labs/coupled-cognition-quality-factory_v0.1.0/docs/EPISTEMIC_PROVENANCE_AND_CO_DEVELOPMENT.md` already defines:

```text
HUMAN_ORIGIN != AI_FORMALIZATION
AI_FORMALIZATION != JOINT_SYNTHESIS
JOINT_SYNTHESIS != EXTERNAL_VALIDATION
EXTERNAL_SOURCE != TRUTH
PROVENANCE != CORRECTNESS
```

The executable provenance ledger likewise requires `JOINT_SYNTHESIS` to retain traceable Human and AI parent contributions rather than erasing either origin.

### 2.2 CCTS reciprocity

`docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md` defines CCTS as requiring substantive Human -> AI and AI -> Human `REVISES` or `CHALLENGES` pathways.

Therefore one-way attribution would be inconsistent with the repository's own current relational research model.

### 2.3 Research-role separation

`docs/research/HUMAN_AI_RESEARCH_ROLE_SEPARATION_2026_09_13.md` records that Human Owner + ChatGPT Teacher primarily conduct:

- problem decomposition;
- research discussion;
- source / provenance review;
- independent review;
- QA / claim-boundary review;
- governance review.

Codex / Work remain preferred for substantial implementation. This role split does not remove ChatGPT Teacher from research participation; it separates research / QA participation from implementation ownership and Human Owner governance authority.

## 3. Corrected source-role model for PR #153

### 3.1 HUMAN_ORIGIN

Human Owner-origin contributions include, without claiming completeness:

- the original observation that ChatGPT Teacher sometimes appears to enter an `效能全開` state;
- the decision to examine that observation rather than treating it as an official model mode;
- the follow-up observation that the Human side may simultaneously enter a high-density research state;
- the question whether the interaction itself, rather than only AI output, is the relevant observable unit;
- the question whether CCTS currently lacks a dynamic-regime layer;
- the insistence on external literature search rather than repository-internal self-reference;
- the requirement for counterevidence, source attribution and a second review before merge;
- the correction that Human–AI learning here must preserve both participants' research contributions rather than depict a one-way learning or analysis process.

```text
HUMAN_ORIGIN
!= SCIENTIFIC_VALIDATION
```

### 3.2 AI_FORMALIZATION

ChatGPT Teacher-origin contributions include, without claiming completeness:

- the formal working label `HIGH-THROUGHPUT EPISTEMIC COORDINATION REGIME (HTECR)`;
- the Chinese working translation `高吞吐知識協作狀態`;
- the preliminary distinction `CCTS = structure` versus `HTECR = candidate dynamic regime`;
- decomposition of candidate observables into epistemic-operation rate, reciprocal coordination density and sustained temporal coupling;
- proposal of discriminant controls against speed, token volume, memory, re-entry and CCTS substitution;
- external-literature retrieval, crosswalk and counterevidence synthesis;
- the anti-circularity correction separating regime detection from epistemic quality, first proposed during ChatGPT Teacher second review.

```text
AI_FORMALIZATION
!= SCIENTIFIC_ESTABLISHMENT
```

### 3.3 JOINT_SYNTHESIS

The following current research propositions should be treated as **joint synthesis** because they were reached through repeated Human <-> ChatGPT Teacher challenge, correction, narrowing and re-formulation rather than being attributable cleanly to only one side:

1. the preferred unit of analysis is the `HUMAN_AI_INTERACTION_TRAJECTORY`, not AI output alone;
2. HTECR, if retained, must be tested as an interaction-level descriptive regime rather than a hidden model-internal mode;
3. `Human–AI Learning` is too broad to claim as a local novelty, because external literature already covers adjacent mutual-learning, collaborative-learning and team-cognition constructs;
4. the narrower candidate gap is a longitudinal, reciprocal, provenance-preserving Human–AI epistemic-development process with a possibly distinct dynamic coordination regime;
5. the retained method rule that HTECR detection must remain separate from epistemic value, after the AI-origin anti-circularity correction was exposed to Human review and incorporated into the shared research method;
6. future work must preserve construct-collapse falsifiers, negative controls, cross-session / cross-dyad tests and separate human-learning outcomes;
7. source attribution itself is part of the method and must remain auditable across later re-entry.

These are not treated as scientifically validated merely because both participants converged on them.

```text
JOINT_SYNTHESIS
!= MUTUAL_AGREEMENT_AS_TRUTH
JOINT_SYNTHESIS
!= EXTERNAL_VALIDATION
JOINT_SYNTHESIS
!= SHARED_MIND
JOINT_SYNTHESIS
!= SYMMETRIC_COGNITION
```

### 3.4 Provenance transition / temporal source-state

A later joint synthesis does **not** retroactively erase the origin of an earlier proposal. PR #153 therefore records provenance as a transition when appropriate.

Example — anti-circularity correction:

```text
T0  AI_FORMALIZATION
    ChatGPT Teacher identifies circularity risk and proposes:
    REGIME_DETECTION != EPISTEMIC_VALUE

T1  HUMAN_REVIEW
    Human Owner reviews / challenges / accepts-or-rejects the proposed correction
    as part of the shared research process.

T2  JOINT_SYNTHESIS
    The corrected separation is retained as part of the jointly stabilized
    research method, while T0 remains AI-origin provenance.
```

The same principle applies to any proposition that changes provenance state through later reciprocal review:

```text
LATER_JOINT_SYNTHESIS
!= RETROACTIVE_JOINT_ORIGIN

JOINT_ADOPTION_OF_AI_ORIGINATED_PROPOSAL
!= AI_ORIGIN_ERASED

JOINT_ADOPTION_OF_HUMAN_ORIGINATED_PROPOSAL
!= HUMAN_ORIGIN_ERASED

SOURCE_TRANSITION
= PRESERVE_PARENT_PROVENANCE
+ RECORD_LATER_SYNTHESIS_STATE
```

This temporal distinction prevents double attribution from becoming source laundering.

## 4. Research participation versus authority / ownership

The repository must preserve the distinction:

```text
RESEARCH_PARTICIPATION
!= REPOSITORY_OWNERSHIP

JOINT_RESEARCH_SYNTHESIS
!= JOINT_GOVERNANCE_AUTHORITY

CHATGPT_TEACHER_RESEARCH_PARTICIPATION
!= LEGAL_OR_ACCOUNT_OWNERSHIP

HUMAN_OWNER_GOVERNANCE_AUTHORITY
!= AUTOMATIC_EPISTEMIC_CORRECTNESS
```

For this repository:

```text
HUMAN_OWNER
= research participant
+ governance / merge authority

CHATGPT_TEACHER
= research participant / AI collaborator
+ decomposition / source review / counterevidence / formalization / QA
!= repository account owner
!= autonomous merge authority
```

Evidence, not participant status, constrains scientific claims.

## 5. Relationship to Human–AI learning

The Human–AI learning line should not be described only as the Human learning from AI, nor only as AI adapting to Human input.

The current local research object includes reciprocal epistemic interaction such as:

```text
HUMAN_QUESTION_OR_HYPOTHESIS
-> AI_DECOMPOSITION_OR_COUNTERPROPOSAL
-> HUMAN_CHALLENGE_OR_CORRECTION
-> AI_REVISION_OR_COUNTEREVIDENCE
-> HUMAN_REFRAMING_OR_REJECTION
-> JOINTLY_STABILIZED_RESEARCH_QUESTION
-> EXTERNAL_EVIDENCE_CHECK
-> FURTHER_REVISION_OR_HOLD
```

This is a process description only.

```text
RECIPROCAL_RESEARCH_INTERACTION
!= MUTUAL_LEARNING_PROVEN

HUMAN_LEARNING
!= AI_LEARNING

DYAD_LEVEL_CHANGE
!= MODEL_INTERNAL_LEARNING

CO_INQUIRY
!= AI_SUBJECTIVITY
```

## 6. Provenance correction to PR #153

The primary PR #153 note remains useful, but its provenance section must be interpreted together with this supplement.

Corrected provenance disposition:

```text
ORIGINAL_OBSERVATION_AND_PHRASE
= HUMAN_ORIGIN

HTECR_NAME_AND_INITIAL_FORMALIZATION
= AI_FORMALIZATION

RESEARCH_QUESTION_NARROWING
+ DISCRIMINANT_DESIGN
+ FALSIFICATION_STRUCTURE
+ INTERACTION_TRAJECTORY_UNIT
+ HUMAN_AI_LEARNING_GAP_REDEFINITION
= JOINT_SYNTHESIS_WITH_TRACEABLE_HUMAN_AND_AI_PARENTS

PROVENANCE_TRANSITION
= PRESERVE_ORIGINAL_PARENT_ORIGIN
+ RECORD_LATER_JOINT_SYNTHESIS_WHEN_JUSTIFIED

EXTERNAL_LITERATURE
= EXTERNAL_SOURCE
```

This correction prevents both failure modes:

```text
AI_ORIGIN_LAUNDERED_AS_HUMAN_ORIGIN = PROHIBITED
HUMAN_ORIGIN_ERASED_INTO_AI_FORMALIZATION = PROHIBITED
JOINT_SYNTHESIS_COLLAPSED_INTO_ONE_PARTICIPANT = PROHIBITED
LATER_JOINT_ADOPTION_ERASES_ORIGINAL_SOURCE = PROHIBITED
```

## 7. Merge consequence

The previous exact-head merge consideration is invalidated by this provenance correction.

PR #153 must remain Draft until:

1. the new exact head is reviewed;
2. the primary note and this supplement are checked for contradiction;
3. CI completes on the new exact head;
4. provenance is independently re-audited;
5. a fresh exact-head Human Owner merge authorization is given only after review.

```text
PRIOR_HEAD_APPROVAL = NOT_REUSABLE
PROVENANCE_CORRECTION = MATERIAL_REVIEW_CHANGE
MERGE = HOLD
SCIENTIFIC_DISPOSITION = HOLD
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
```