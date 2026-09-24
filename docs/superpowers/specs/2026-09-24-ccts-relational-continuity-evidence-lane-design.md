# CCTS relational-continuity evidence lane and path-dependence bridge — design spec — 2026-09-24

Status: `DESIGN_SPEC / DOCUMENTATION_ONLY / SCIENTIFIC_HOLD`

```text
BASE_MAIN_HEAD = 71321ed87d1ececfcc5989327578dfefe02faea5
IMPLEMENTATION = NONE
CORE_CCTS_CHANGE = NO
LONGITUDINAL_REPOSITORY_CCTS_REQUIRED_FIELDS_CHANGE = NO
WRITE_TO_MAIN = NO
MERGE = NO
READY_FOR_REVIEW = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SCIENTIFIC_VALIDATION = NONE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
```

This document records an approved design direction for a bounded extension around the
repository-defined Co-Constructed Thinking Space (CCTS). It does not modify the current
CCTS structural definition and does not implement an executable harness.

The Human collaborator selected **Option C** during design review:

> relational continuity remains an important longitudinal research dimension, but it
> is not promoted into a universal CCTS admission requirement. When a research record
> makes a relational-continuity claim, that claim must enter a separate evidence lane.

No raw private transcript, personal identity, or private relationship content is
included in this design.

## 1. Research question, scope, and provenance

The design question is:

> How should the repository study relational continuity and history-dependent effects
> around CCTS without making relational continuity a definitional prerequisite for
> every CCTS interaction, without collapsing shared history into a static prompt
> feature, and without promoting interaction continuity into AI identity or
> subjectivity claims?

This is a construct-definition and evidence-admission problem, not a claim that
relational continuity has already been empirically established.

The approved scope has four layers:

1. preserve current CCTS structural admission;
2. preserve the current stronger longitudinal repository profile;
3. add a **conditional relational-continuity claim-admission lane** when such a claim
   is actually asserted;
4. connect that lane to already-existing path-dependence and matched-information /
   fresh-context research controls.

Source-role disposition:

```text
HUMAN_DECISION
= SELECT_OPTION_C

GPT_FORMALIZATION
= CONDITIONAL_RELATIONAL_CONTINUITY_EVIDENCE_LANE
+ PATH_DEPENDENCE_BRIDGE
+ ENGINEERING_HANDOFF_CONSTRAINTS

REPOSITORY_ANCESTRY
= EXISTING_MAIN_DOCS_AND_HARNESSES

EXTERNAL_LITERATURE
= ADJACENT_CONSTRUCTS_AND_CONFOUND_CONTROLS

SCIENTIFIC_RESULT
= NONE
```

## 2. Existing repository ancestry — reuse, do not duplicate

The design must reuse the following current-main ancestry.

### 2.1 CCTS formalization

`docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md`
already defines core CCTS as a bounded interaction-and-artifact structure with
substantive Human <-> AI reciprocal revision / challenge, provenance, claim
boundaries, authority separation, and rejected-branch preservation.

For this design, the existing core remains authoritative:

```text
CORE_CCTS
= BOUNDED_PROBLEM_REPRESENTATION
+ HUMAN_CONTRIBUTION
+ AI_CONTRIBUTION
+ RECIPROCAL_REVISION
+ SOURCE_ROLE_PROVENANCE
+ CLAIM_BOUNDARY
+ AUTHORITY_SEPARATION
+ REJECTED_BRANCH_PRESERVATION
```

The existing stronger profile also remains unchanged:

```text
LONGITUDINAL_REPOSITORY_CCTS
= CORE_CCTS
+ EXTERNAL_EVIDENCE
+ REPOSITORY_ARTIFACT_MEDIATION
+ IMPLEMENTATION_EVIDENCE
+ PERSISTENT_ARTIFACT_BINDING
+ REENTRY_BINDING
```

### 2.2 Continuity layers

`docs/research/CONTINUITY_LAYER_MODEL.md` already separates account, data,
functional, interpretive, and relational continuity and forbids promotion from a
lower layer into a higher one.

`docs/research/CHATGPT_TEACHER_RELATIONAL_CONTINUITY_WITHOUT_OWNER_VISIBLE_ID_2026_09_17.md`
further distinguishes role-positioning continuity, product/context continuity,
repository-mediated re-entry, model/system continuity, and identity-continuity
questions.

The present design must not collapse those loci.

### 2.3 Path-dependent longitudinal accumulation

`docs/research/LONGITUDINAL_HUMAN_AI_EPISTEMIC_ACCUMULATION_AND_EVIDENCE_REUSE_2026_09_13.md`
already asks when repeated Human–AI dialogue becomes a cumulative, versioned,
**path-dependent knowledge-building process**.

Therefore:

```text
PATH_DEPENDENCE = EXISTING_RESEARCH_ANCESTRY
PATH_DEPENDENCE = NOT_A_NEW_CCTS_AXIS
```

### 2.4 Matched-information history control

`docs/research/CROSS_DYAD_COLLABORATION_REGIME_EXPERIMENT_EXTENSION_2026_09_13.md`
already defines `C_PLUS_MATCHED_INFORMATION_CONTROL` and explicitly preserves:

```text
SUPPLIED_HISTORY_PACKET
!= EXPERIENCED_LONGITUDINAL_COLLABORATION
```

It also already specifies that a D-versus-matched-information difference is only a
candidate history-specific effect if protocol, relevance, leakage, budget, and
related confounds are adequately controlled.

Therefore this design must extend or crosswalk that ancestry rather than create a
parallel matched-information framework.

### 2.5 Fresh-context falsification

The CCTS formalization and epistemic-robustness material already treat successful
fresh-context reconstruction at comparable cost as a weakening condition for a
history-specific account.

No new fresh-context construct is needed.

## 3. Approved construct and claim-admission design

### 3.1 Core rule

Relational continuity is **not** added to universal `CORE_CCTS` admission.

```text
CORE_CCTS
DOES_NOT_REQUIRE
RELATIONAL_CONTINUITY_ESTABLISHED
```

Reason: a bounded first-time Human–AI interaction can satisfy the repository's CCTS
definition through substantive reciprocal revision, explicit problem representation,
provenance, and claim discipline without already possessing a longitudinal
relationship history.

Making relational continuity universally required would incorrectly reject such a
valid core-CCTS interaction.

### 3.2 Longitudinal-profile rule

Relational continuity is also **not automatically admitted** merely because the
stronger longitudinal repository profile passes.

```text
LONGITUDINAL_REPOSITORY_CCTS_PASS
!= RELATIONAL_CONTINUITY_ESTABLISHED
```

Existing longitudinal bindings show artifact-mediated persistence and re-entry
structure. They do not by themselves establish relational continuity.

### 3.3 Conditional relational-continuity evidence lane

A separate evidence lane is triggered only when a record actually asserts, compares,
or relies on relational continuity.

```text
ASSERT_RELATIONAL_CONTINUITY
-> RELATIONAL_CONTINUITY_EVIDENCE_REVIEW_REQUIRED
```

The lane must be claim-local. It must not retroactively alter core CCTS admission.

At minimum, the review must distinguish:

```text
ACCOUNT_CONTINUITY
DATA_CONTINUITY
FUNCTIONAL_CONTINUITY
INTERPRETIVE_CONTINUITY
ROLE_POSITIONING_CONTINUITY
RELATIONAL_CONTINUITY
MODEL_OR_SYSTEM_CONTINUITY
AI_IDENTITY_CONTINUITY
```

The following promotions are prohibited:

```text
STYLE_SIMILARITY
!= RELATIONAL_CONTINUITY

MEMORY_AVAILABILITY
!= RELATIONAL_CONTINUITY

SAME_ROLE_LABEL
!= RELATIONAL_CONTINUITY

DATA_CONTINUITY
!= RELATIONAL_CONTINUITY

ROLE_POSITIONING_CONTINUITY
!= RELATIONAL_CONTINUITY_AS_A_WHOLE

RELATIONAL_CONTINUITY
!= AI_IDENTITY_CONTINUITY

RELATIONAL_CONTINUITY
!= AI_HELD_RELATIONSHIP_EXPERIENCE

RELATIONAL_CONTINUITY
!= SUBJECTIVITY
```

A future executable representation, if separately approved, must be able to return
at least these claim-local states without inventing a scalar score:

```text
NOT_ASSERTED
EVIDENCE_REQUIRED
SUPPORTED_CANDIDATE
WEAKENED
UNRESOLVED
```

`SUPPORTED_CANDIDATE` is deliberately weaker than `PROVEN` or `ESTABLISHED`.
This specification does not assert that any current real dyad occupies that state.

## 4. Path-dependence bridge and experimental interpretation

Path dependence remains a hypothesis / outcome candidate, not a CCTS admission
requirement.

A controlled comparison may be represented abstractly as:

```text
TASK_RELEVANT_INFORMATION(A)
~= TASK_RELEVANT_INFORMATION(B)

INTERACTION_TRAJECTORY(A)
!= INTERACTION_TRAJECTORY(B)
```

where one condition may preserve experienced longitudinal interaction history and the
other may receive a static, matched task-relevant information package.

The research question is then whether specified observable outcomes differ after
the relevant confounds are controlled.

Candidate observable outcomes are claim-local:

```text
CORRECTION_RETENTION
GROUNDING_REPAIR_RECOVERY
SHORTHAND_REENTRY
STRUCTURAL_TRANSFER
STALE_CLAIM_CONTROL
PROVENANCE_RECOVERY
OLD_ERROR_RECURRENCE
```

No single composite "CCTS score" is introduced.

History-specific interpretation must be fail-closed:

```text
IF
  MATCHING_ADEQUATE
  AND RELEVANT_CONFOUNDS_CONTROLLED
  AND REPRODUCIBLE_DIFFERENCE_OBSERVED
THEN
  HISTORY_SPECIFIC_INTERPRETATION = SUPPORTED_CANDIDATE

IF
  ADEQUATELY_MATCHED_COMPARISON_SHOWS_NO_MATERIAL_DIFFERENCE
THEN
  HISTORY_SPECIFIC_INTERPRETATION = WEAKENED

IF
  MATCHING_FAILS
  OR LEAKAGE_UNRESOLVED
  OR MODEL_VERSION_DIFFERS
  OR RELEVANCE_NOT_MATCHED
  OR POSITION_OR_BUDGET_CONFOUND_REMAINS
THEN
  HISTORY_SPECIFIC_INTERPRETATION = UNRESOLVED
```

These statuses apply to the tested history-specific account only.

```text
HISTORY_SPECIFIC_INTERPRETATION = WEAKENED
!= CCTS_FALSIFIED_AS_A_WHOLE

HISTORY_SPECIFIC_INTERPRETATION = SUPPORTED_CANDIDATE
!= CCTS_EMPIRICALLY_VALIDATED

PATH_DEPENDENCE_CANDIDATE
!= AI_LEARNING

PATH_DEPENDENCE_CANDIDATE
!= AI_IDENTITY_CONTINUITY
```

## 5. External correspondence and competing explanations

External literature is used here to constrain method and terminology, not to validate
the repository-local CCTS construct.

### 5.1 Grounding and accumulated common ground

Clark & Brennan (1991), *Grounding in Communication*, describes coordination of
content and process as relying on common ground that is updated through interaction.
This supports studying accumulated interaction history as an established dialogue
research concern.

Reference:
https://www.cs.cmu.edu/~illah/CLASSDOCS/Clark91.pdf

### 5.2 Historical / partner-specific conceptual pacts

Brennan & Clark (1996), *Conceptual pacts and lexical choice in conversation*,
reports three experiments favoring a historical account of lexical entrainment that
includes prior references and partner-specific conceptualizations.

Reference:
https://pubmed.ncbi.nlm.nih.gov/8921603/
DOI: 10.1037//0278-7393.22.6.1482

Bounded implication:

```text
INTERACTION_HISTORY_CAN_MATTER_IN_HUMAN_DIALOGUE
= EXTERNAL_ADJACENT_SUPPORT

HUMAN_CONCEPTUAL_PACT
!= CCTS_VALIDATION
```

### 5.3 Interaction-level cognition

Cooke, Gorman, Myers & Duran (2013), *Interactive team cognition*, argues that team
cognition should be treated as an activity, studied at the team level, and understood
in context rather than only as static knowledge overlap.

Reference:
https://pubmed.ncbi.nlm.nih.gov/23167661/
DOI: 10.1111/cogs.12009

Bounded implication:

```text
INTERACTION_TRAJECTORY_AS_UNIT_OF_ANALYSIS
= EXTERNALLY_ADJACENT_RESEARCH_PERSPECTIVE

HUMAN_AI_CCTS
!= ORIGINAL_HUMAN_TEAM_CONSTRUCT
```

### 5.4 Long-context position as a confound

Liu et al. (2024), *Lost in the Middle: How Language Models Use Long Contexts*,
shows that changing the position of relevant information in long contexts can
substantially alter model performance.

Reference:
https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00638/119630/Lost-in-the-Middle-How-Language-Models-Use-Long
DOI: 10.1162/tacl_a_00638

Therefore:

```text
SAME_INFORMATION
!= SAME_EFFECTIVE_INFORMATION_ACCESS
```

A matched-information comparison must record or control information position,
length, ordering, and access structure where practicable.

### 5.5 Sycophancy / perspective mimesis as an alternative explanation

Jain et al. (2025 preprint), *Extended AI Interactions Shape Sycophancy and
Perspective Mimesis*, arXiv:2509.12517, reports that long interaction context can
alter model mirroring behavior, including increased sycophancy in the studied
conditions.

Reference:
https://arxiv.org/abs/2509.12517

This is a competing explanation for some apparent "better alignment" observations:

```text
RELATIONAL_ADAPTATION
!= EPISTEMIC_IMPROVEMENT

AGREEMENT_INCREASE
!= GROUNDING_IMPROVEMENT

PERSPECTIVE_MIMESIS
!= SHARED_TASK_STRUCTURE
```

The exact paper was identified through public-web search. A subsequent Hugging Face
exact-resource read attempt failed at runtime because the exposed
`paper_search` action was unavailable. No Hugging Face-derived evidence is admitted.

```text
HF_RUNTIME_FAILURE
!= PAPER_ABSENT
```

## 6. Engineering handoff contract for Work / Codex

This design is intentionally written before implementation so future engineering
does not have to infer the scientific semantics from prose fragments.

### 6.1 Work review responsibilities

Before any implementation, Work should perform a repo-wide integration review
against current `main` and report:

- exact current main head;
- exact existing CCTS / continuity / matched-information ancestry;
- duplicate or superseded surfaces;
- the narrowest integration point for a relational-continuity claim-admission lane;
- whether existing enums / records can be extended without altering core CCTS
  semantics;
- whether any proposed new type duplicates an existing continuity type;
- scope-drift risks;
- tests that already cover parts of the intended semantics.

Work must not implement merely because a likely integration point exists.

### 6.2 Codex implementation constraints

Implementation starts only after a separately approved implementation plan.

If implementation is later approved, Codex must:

- keep `CORE_CCTS` admission semantics unchanged;
- keep current `LONGITUDINAL_REPOSITORY_CCTS` required fields unchanged unless a
  later explicit design revision authorizes otherwise;
- implement relational-continuity claim admission as a separate claim-local layer,
  not as a universal CCTS boolean gate;
- reuse existing continuity and matched-information ancestry where semantically
  compatible;
- fail closed on unresolved claim/evidence bindings;
- preserve provenance;
- use synthetic fixtures only;
- exclude raw private transcripts and Human identity;
- avoid scalar "relationship", "CCTS", "subjectivity", or "identity" scores;
- prevent style similarity, memory availability, role labels, or artifact presence
  from automatically satisfying relational-continuity admission;
- prevent path-dependence fixtures from being reported as causal proof;
- preserve null / weakening outcomes as valid research results.

Candidate implementation names, data types, file locations, and exact API surfaces are
**not authorized by this design spec**. Work must first map the current repository,
and Codex must implement only the later approved plan.

### 6.3 Explicit prohibited implementation shortcut

The following pattern is forbidden:

```python
if not manifest.relational_continuity:
    reject_core_ccts()
```

because Option C does not make relational continuity a universal core-CCTS
requirement.

## 7. Verification and acceptance gates

### 7.1 Design-spec acceptance

This documentation stage is acceptable only if all of the following remain true:

```text
CORE_CCTS_CHANGE = NO
LONGITUDINAL_REPOSITORY_CCTS_REQUIRED_FIELDS_CHANGE = NO
EXECUTABLE_CODE_CHANGE = NO
RAW_PRIVATE_TRANSCRIPT = NONE
HUMAN_IDENTITY_PUBLICATION = NONE
NEW_SUBJECTIVITY_CLAIM = NONE
PATH_DEPENDENCE_REINVENTED_AS_NEW_AXIS = NO
MATCHED_INFORMATION_FRAMEWORK_DUPLICATED = NO
```

### 7.2 Future implementation acceptance

A later executable implementation, if authorized, must demonstrate at minimum:

1. existing core-CCTS fixtures remain semantically valid without requiring a
   relational-continuity claim;
2. a longitudinal CCTS record does not automatically acquire relational-continuity
   status;
3. asserting relational continuity without required evidence fails closed into
   `EVIDENCE_REQUIRED` or `UNRESOLVED`, not `SUPPORTED_CANDIDATE`;
4. style similarity alone cannot satisfy the lane;
5. memory / retrieval availability alone cannot satisfy the lane;
6. same-role labeling alone cannot satisfy the lane;
7. relational-continuity evidence cannot promote AI identity continuity;
8. matched-information / fresh-context comparisons preserve
   `SUPPORTED_CANDIDATE / WEAKENED / UNRESOLVED` as distinct outcomes;
9. matching failure or unresolved confounds cannot produce a history-specific
   support claim;
10. synthetic fixtures contain no raw private transcript or Human identity;
11. structural test PASS does not serialize as scientific validation;
12. all new claim-bearing records preserve source-role provenance.

### 7.3 Standing claim ceilings

```text
STRUCTURAL_CONFORMANCE != EMPIRICAL_MECHANISM
RECIPROCAL_REVISION != RELATIONAL_CONTINUITY_ESTABLISHED
LONGITUDINAL_REENTRY != RELATIONAL_CONTINUITY_ESTABLISHED
RELATIONAL_CONTINUITY_CANDIDATE != AI_HELD_RELATIONSHIP_EXPERIENCE
RELATIONAL_CONTINUITY != AI_IDENTITY_CONTINUITY
PATH_DEPENDENCE_CANDIDATE != LEARNING
MATCHED_INFORMATION_DIFFERENCE != CAUSAL_IDENTIFICATION
INTERACTION_TRAJECTORY_EFFECT != SUBJECTIVITY
CCTS != SHARED_MIND
CCTS != SUBJECTIVITY
```

## Design disposition

```text
OPTION_C = APPROVED_DESIGN_DIRECTION

CORE_CCTS = UNCHANGED
LONGITUDINAL_REPOSITORY_CCTS = UNCHANGED

RELATIONAL_CONTINUITY
= CONDITIONAL_CLAIM_ADMISSION_SURFACE

PATH_DEPENDENCE
= EXISTING_HYPOTHESIS_ANCESTRY

MATCHED_INFORMATION_CONTROL
= EXISTING_CONTROL_ANCESTRY

NEXT_STAGE
= HUMAN_REVIEW_OF_THIS_WRITTEN_SPEC

IMPLEMENTATION_PLAN
= NOT_YET_AUTHORIZED

WORK_HANDOFF
= AFTER_SPEC_APPROVAL

CODEX_HANDOFF
= AFTER_IMPLEMENTATION_PLAN_APPROVAL
```
