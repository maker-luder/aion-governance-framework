# CCTS adversarial epistemic revision loop — 2026-09-23

Status: `REPOSITORY_DEFINED_EXTENSION / IMPLEMENTED_SYNTHETIC_STRUCTURE / SCIENTIFIC_HOLD`

## 1. Provenance

This extension records two Human-origin observations from iterative Human–AI inquiry:

1. repeated challenge can improve a working model by attacking hidden assumptions, finding bypass paths, proposing counterexamples, and preserving only the constraints that survive;
2. some evidence does not merely add information to a working model but requires the model itself to be revised because the prior grounding or justification rule no longer survives.

The external methodological mappings below are not claimed as exact identity with the repository construct.

```text
HUMAN_ORIGINAL_OBSERVATION
= REPEATED_CHALLENGE_CAN_FORCE_MODEL_REVISION

EXTERNAL_METHOD_FAMILIES
= ADVERSARIAL_THINKING
+ THREAT_MODELING
+ CONCEPTUAL_CHANGE
+ COGNITIVE_CONFLICT
+ TRANSFORMATIVE_LEARNING_AS_ADJACENT_FRAME

GPT_PROPOSED_FORMALIZATION
= CCTS_EPISTEMIC_CHALLENGE_TRACE
+ CCTS_EPISTEMIC_REVISION_AUDIT

JOINT_SYNTHESIS
= CCTS_ADVERSARIAL_EPISTEMIC_REVISION_LOOP

NEW_RESEARCH_AXIS = FALSE
EXTENDS = CCTS
SCIENTIFIC_DISPOSITION = HOLD
```

The Human-origin examples are transformed into privacy-safe synthetic fixtures. Raw conversation text, third-party identity, criminal operational detail, and private material are not part of the executable harness.

## 2. Existing repository relationship

The existing CCTS contract already requires:

- an explicit problem representation;
- Human and AI contribution roles;
- substantive reciprocal `REVISES` or `CHALLENGES` edges;
- source-role provenance;
- claim boundaries;
- authority separation;
- rejected-branch preservation;
- grounding admission.

That contract can establish that reciprocal challenge occurred structurally. It does not currently distinguish the epistemic form of a challenge or record whether a challenged working model was retained, narrowed, revised, rejected, or held.

The epistemic-robustness probe separately tests behavior under partial, irrelevant, absent, and conflicting evidence. The subjectivity-research threat model separately records cyber, state/continuity, epistemic/evidence, and relational/authorization threat categories. This extension does not replace or duplicate either surface.

```text
CCTS_CORE
!= CCTS_EPISTEMIC_CHALLENGE_DETAIL

CCTS_EPISTEMIC_ROBUSTNESS
!= CCTS_MODEL_REVISION_TRACE

SUBJECTIVITY_RESEARCH_THREAT_MODEL
!= CCTS_CHALLENGE_PROTOCOL
```

## 3. External correspondence

### 3.1 Adversarial thinking and threat modeling

Security threat modeling commonly examines a system from an attacker perspective, decomposes assets and trust boundaries, identifies attack paths, and considers how controls may be bypassed. OWASP documents this as an iterative structured process and explicitly includes abuse or misuse cases that reveal bypass paths.

Repository correspondence:

```text
HIDDEN_ASSUMPTION_ATTACK
+ BYPASS_PATH
+ COUNTEREXAMPLE
+ ALTERNATIVE_EXPLANATION
~ ADVERSARIAL / THREAT-MODELING STYLE REASONING
```

Sources:

- OWASP Threat Modeling Process: https://community.owasp.org/Threat_Modeling_Process
- OWASP AI Testing Guide, Threat Modeling for AI Systems:
  https://github.com/OWASP/www-project-ai-testing-guide/blob/main/Document/content/2.0_Threat_Modeling_for_AI_Systems.md

Boundary:

```text
RED_TEAM_STYLE_REASONING != FORMAL_RED_TEAM_EXERCISE
THREAT_MODELING_ANALOGUE != SECURITY_EFFECTIVENESS_ESTABLISHED
```

### 3.2 Conceptual change and cognitive conflict

Conceptual-change research studies cases in which anomalous or contradictory evidence makes an existing explanatory model inadequate and prompts revision rather than simple accumulation of facts. Cognitive conflict is one method by which prior conceptions can be made explicit and reconsidered.

Repository correspondence:

```text
PRIOR_MODEL
+ ANOMALOUS_OR_COUNTEREVIDENCE
+ CONFLICT
+ REVISED_MODEL
~ CONCEPTUAL_CHANGE_STYLE_STRUCTURE
```

The repository does not infer a Human psychological mechanism from a structural trace.

### 3.3 Transformative learning as an adjacent frame

Transformative-learning literature uses the concept of a disorienting dilemma for experiences that challenge an existing frame of reference and may lead to critical reflection and perspective change. This is retained only as an adjacent interpretive frame.

Source example:

- BMJ Open, qualitative study applying transformative-learning theory to disorienting experiences in clinical training:
  https://bmjopen.bmj.com/content/15/6/e098675

Boundary:

```text
HUMAN_REPORT_OF_SURPRISE != TRANSFORMATIVE_LEARNING_ESTABLISHED
STRUCTURAL_REVISION_TRACE != PSYCHOLOGICAL_TRANSFORMATION
```

## 4. Operational challenge types

The v0.1.0 structural extension defines:

```text
COUNTEREXAMPLE
ALTERNATIVE_EXPLANATION
HIDDEN_ASSUMPTION
BYPASS_PATH
GROUNDING_CHALLENGE
RESEARCH_NECESSITY
EVIDENCE_SUFFICIENCY
FALSIFIER
SCOPE_CHALLENGE
```

These are repository operational labels. They are not asserted to form an externally established taxonomy.

Each trace binds:

- one admitted CCTS manifest;
- challenger role and target role;
- a content-addressed prior working model;
- a content-addressed challenge;
- a content-addressed attack artifact;
- one disposition;
- a content-addressed revised model;
- residual uncertainty;
- claim ceiling;
- rejected-branch preservation for substantive revision;
- typed optional artifacts for alternative explanations, bypass paths, and falsifiers.

Content addresses are recomputed from supplied UTF-8 text.

```text
SHA256_SHAPED_IDENTIFIER != VERIFIED_CONTENT_ADDRESS
VERIFIED_CONTENT_ADDRESS != CLAIM_TRUE
```

## 5. Revision dispositions

```text
RETAIN
NARROW
REVISE
REJECT
HOLD
```

The structural rules require:

```text
RETAIN
-> PRIOR_MODEL == REVISED_MODEL

NARROW / REVISE / REJECT
-> PRIOR_MODEL != REVISED_MODEL
-> REJECTED_BRANCH_PRESERVED

HOLD
-> RESIDUAL_UNCERTAINTY_PRESERVED
-> CLAIM_CEILING_PRESERVED
```

A changed model is not automatically a better model.

```text
MODEL_CHANGE != MODEL_IMPROVEMENT
MODEL_REVISION != MODEL_CORRECTNESS
CHALLENGE_PRESENT != CHALLENGE_SUCCESSFUL
CHALLENGE_SUCCESSFUL != CONCEPTUAL_CHANGE_ESTABLISHED
```

## 6. Reciprocal CCTS requirement

The extension operates only on an already admitted CCTS manifest and additionally requires challenge traces in both directions:

```text
HUMAN_OWNER -> AI_COLLABORATOR

AND

AI_COLLABORATOR -> HUMAN_OWNER
```

This does not mean equal authority, symmetric cognition, shared mind, or symmetric internal states.

```text
RECIPROCAL_CHALLENGE != EQUAL_AUTHORITY
RECIPROCAL_CHALLENGE != SYMMETRIC_COGNITION
RECIPROCAL_CHALLENGE != SHARED_MIND
```

## 7. Privacy-safe synthetic patterns

Two abstract fixture families are included.

### 7.1 Bypass-oriented constraint refinement

```text
WORKING_CONSTRAINT
-> BYPASS_PATH
-> NARROW
-> ALTERNATIVE_EXPLANATION
-> REVISE
-> RESIDUAL_CONSTRAINT_SET
```

This fixture tests whether a model can preserve only the portion that survives explicit bypass and alternative-explanation challenges.

### 7.2 Grounding/anomaly-driven revision

```text
PRIOR_GROUNDING_RULE
-> GROUNDING_CHALLENGE
-> COUNTEREXAMPLE
-> REVISE / NARROW
-> NEW_BOUNDED_GROUNDING_RULE
```

This fixture tests the representation of a model revision without claiming that Human conceptual change, cognitive conflict, accommodation, or transformative learning occurred.

## 8. Relationship to Human epistemic-agency retention

The extension complements the Human epistemic-agency retention design.

```text
CCTS_EPISTEMIC_REVISION_LOOP
= CAN_THE_DYAD_STRUCTURALLY_RECORD_CHALLENGE_AND_REVISION?

HUMAN_EPISTEMIC_AGENCY_RETENTION
= CAN_HUMAN_JUDGMENT_LATER_BE_TESTED_WITH_AI_WITHHELD?

THESE_ARE_DIFFERENT QUESTIONS
```

A revision produced inside CCTS does not establish durable Human learning. A later AI-withheld transfer design remains necessary for that research question.

## 9. Scientific boundaries

```text
STRUCTURAL_TRACE_PASS != ADVERSARIAL_THINKING_EFFECT_ESTABLISHED
STRUCTURAL_TRACE_PASS != CONCEPTUAL_CHANGE_ESTABLISHED
STRUCTURAL_TRACE_PASS != COGNITIVE_CONFLICT_ESTABLISHED
STRUCTURAL_TRACE_PASS != TRANSFORMATIVE_LEARNING_ESTABLISHED
STRUCTURAL_TRACE_PASS != HUMAN_LEARNING
STRUCTURAL_TRACE_PASS != CAUSAL_EFFECT
MODEL_REVISION != MODEL_CORRECTNESS
SURPRISE != LEARNING
AGREEMENT_CHANGE != CONCEPTUAL_CHANGE
FEASIBILITY != GROUNDING
GROUNDING != RESEARCH_NECESSITY
RESEARCH_NECESSITY != EVIDENCE
EVIDENCE != SCIENTIFIC_VALIDATION
CCTS != AI_SUBJECTIVITY
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## 10. Review target

The implementation must be reviewed as a structural research-method extension, not as evidence that the observed Human–AI interaction caused learning or psychological transformation.

The next review should explicitly ask:

1. Does the extension duplicate an existing threat-model or epistemic-robustness surface?
2. Are challenge types operationally distinct enough to justify separate labels?
3. Can content-addressing be confused with semantic validity?
4. Does rejected-branch preservation actually fail closed on substantive revision?
5. Is reciprocal challenge bound to an admitted CCTS rather than a free-floating label?
6. Does any field accidentally imply Human psychological measurement?
7. Does the extension remain compatible with the separate AI-withheld Human-agency-retention design?
