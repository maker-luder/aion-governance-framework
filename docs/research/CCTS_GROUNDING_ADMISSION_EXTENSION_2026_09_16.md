# CCTS grounding admission extension — 2026-09-16

Status: `REPOSITORY_DEFINED_EXTENSION / IMPLEMENTATION_CANDIDATE / SCIENTIFIC_HOLD`

## 1. Provenance

This note extends the repository-defined Co-Constructed Thinking Space (CCTS) formalization after a Human Owner observation:

> Before two parties can productively discuss or co-construct around a problem, there must be enough understanding of what is being discussed to support the current interaction.

The observation is recorded as `HUMAN_OWNER_ORIGINAL`. The operational distinction between grounding evidence and proof of internal understanding is a `GPT_PROPOSED_FORMALIZATION`, informed by the repository's existing bidirectional-grounding note and adjacent communication/collaborative-learning literature.

```text
HUMAN_OWNER_ORIGINAL_OBSERVATION
= CO_CONSTRUCTION_REQUIRES_ENOUGH_SHARED_OR_ALIGNED_PROBLEM_UNDERSTANDING_TO_PROCEED

GPT_PROPOSED_OPERATIONALIZATION
= CCTS_GROUNDING_CHECKPOINT

NEW_RESEARCH_AXIS = FALSE
EXTENDS = CO_CONSTRUCTED_THINKING_SPACE
ANCESTRY = HUMAN_AI_BIDIRECTIONAL_GROUNDING_HYPOTHESIS_2026_09_11
SCIENTIFIC_DISPOSITION = HOLD
```

No later operational label is retroactively attributed to the Human Owner.

## 2. Gap identified

The existing CCTS contract already requires an explicit `problem_representation_sha256`, Human and AI contribution roles, and substantive reciprocal `REVISES` or `CHALLENGES` edges.

That is not sufficient to establish that the Human and AI contributions are structurally grounded against the same problem representation.

A false-positive structure is possible:

```text
HUMAN_INTERPRETATION = A
AI_INTERPRETATION = B

HUMAN -> AI = CHALLENGES
AI -> HUMAN = REVISES
GRAPH_CONNECTED = TRUE
PROBLEM_REPRESENTATION_DIGEST_PRESENT = TRUE

BUT
GROUNDING_ADEQUACY = NOT_ESTABLISHED
```

Therefore:

```text
PROBLEM_REPRESENTATION_DIGEST_PRESENT
!= PROBLEM_REPRESENTATION_GROUNDED

RECIPROCAL_REVISION
!= SUFFICIENT_GROUNDING
```

## 3. Adjacent literature correspondence

Clark and Brennan (1991) describe grounding as coordinated communicative work aimed at reaching a criterion adequate for the current purpose. This is used here only as vocabulary for interaction-level coordination; it does not establish mutual belief, symmetric cognition, or an AI mental state.

Teasley and Roschelle (1993), and Roschelle and Teasley (1995), describe collaborative problem solving in terms of negotiating and sharing problem-relevant meanings and constructing a Joint Problem Space. This is an adjacent human-collaboration construct, not direct evidence that a Human–AI dyad has symmetric internal representations.

Sources:

- Clark, H. H. & Brennan, S. E. (1991), *Grounding in Communication*. Stanford-hosted author copy: https://web.stanford.edu/~clark/1990s/Clark%2C%20H.H.%20_%20Brennan%2C%20S.E.%20_Grounding%20in%20communication_%201991.pdf
- Teasley, S. D. & Roschelle, J. (1993), *Constructing a Joint Problem Space: The Computer as a Tool for Sharing Knowledge*. SRI archive: https://www.sri.com/publication/education-learning-pubs/digital-learning-pubs/constructing-a-joint-problem-space-the-computer-as-a-tool-for-sharing-knowledge/
- Roschelle, J. & Teasley, S. D. (1995), *The Construction of Shared Knowledge in Collaborative Problem Solving*. DOI: https://doi.org/10.1007/978-3-642-85098-1_5

## 4. Grounding checkpoint contract

CCTS admission is extended with a typed `GroundingCheckpoint`.

The checkpoint must bind:

```text
ONE HUMAN_OWNER CONTRIBUTION
+ ONE AI_COLLABORATOR CONTRIBUTION
+ THE SAME problem_representation_sha256 USED BY THE CCTS MANIFEST
+ disposition = SUFFICIENT_FOR_CURRENT_PURPOSE
+ unresolved_mismatch = FALSE
```

The purpose is not to claim that the Human and AI possess identical internal representations. The purpose is to prevent the structural contract from admitting reciprocal revision while leaving the interaction-level problem alignment entirely unrepresented.

```text
GROUNDING_CHECKPOINT_PRESENT
!= MUTUAL_BELIEF_PROVEN

GROUNDING_CHECKPOINT_PRESENT
!= IDENTICAL_INTERNAL_REPRESENTATION

GROUNDING_CHECKPOINT_PRESENT
!= AI_UNDERSTANDING_PROVEN

BEHAVIORAL_OR_DECLARED_ALIGNMENT
!= SYMMETRIC_COGNITION

GROUNDING_ADEQUATE_FOR_CURRENT_PURPOSE
!= PERMANENT_UNDERSTANDING
```

## 5. Repair semantics

`GroundingDisposition` has two structural states:

```text
SUFFICIENT_FOR_CURRENT_PURPOSE
REPAIR_REQUIRED
```

A manifest may structurally carry a checkpoint marked `REPAIR_REQUIRED`, but CCTS admission must fail closed until the disposition is `SUFFICIENT_FOR_CURRENT_PURPOSE` and `unresolved_mismatch` is false.

This permits the contract to represent failed or incomplete grounding rather than forcing every recorded interaction to appear successful.

```text
REPAIR_REQUIRED => CCTS_ADMISSION_HOLD
UNRESOLVED_MISMATCH => CCTS_ADMISSION_HOLD
```

## 6. Current implementation boundary

The executable contract remains deterministic synthetic structural QA. It does not inspect a raw conversation, infer semantic equivalence from natural language, inspect model internals, or independently establish that either party psychologically understands the other.

The checkpoint is an explicit structural declaration bound to known contribution roles and the exact problem-representation digest.

```text
STRUCTURAL_GROUNDING_CHECKPOINT
!= SEMANTIC_EQUIVALENCE_DETECTOR

STRUCTURAL_GROUNDING_CHECKPOINT
!= PSYCHOLOGICAL_MEASUREMENT

GROUNDING_ADMISSION_PASS
!= EMPIRICAL_GROUNDING_EFFECT

CCTS_STRUCTURAL_CONFORMANCE
!= AI_SUBJECTIVITY
```

The current contract also does not prove temporal ordering between the checkpoint and every later revision edge. It requires grounding adequacy as part of CCTS admission, but a future empirical protocol would need timestamped interaction evidence to test when grounding was reached and whether it was maintained.

```text
GROUNDING_PRESENT_AT_ADMISSION
!= TEMPORAL_ORDER_PROVEN
```

## 7. Relationship to the central research question

This extension improves the validity of the CCTS research surface by reducing a structural false positive: reciprocal correction without explicit grounding adequacy.

It does not elevate any scientific or ontological conclusion.

```text
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MUTUAL_UNDERSTANDING = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
