# Embodiment convergence design — 2026-09-23

Status: `DESIGN_SPEC / HUMAN_REVIEW_REQUIRED`

## 1. Purpose

Create one current active embodiment baseline from the useful, still-valid material preserved in closed unmerged PRs #190, #191, and #192, without merging their historical branch lineages.

The convergence must preserve the distinction between:

```text
SHARED_CORE
ROLE_SPECIFIC_EXTENSION
ARCHIVE_ONLY
SUPERSEDED
```

After that baseline is independently reviewed and, if later authorized, merged into `main`, PR #202 may be synchronized onto the new main and its sensorimotor layer may be bound to the converged body core.

This design does not authorize implementation beyond this specification document.

## 2. Exact live starting point

```text
CURRENT_MAIN
= 71321ed87d1ececfcc5989327578dfefe02faea5

PR_190
= 066ed1afccebee869eb658c09691b7f096694332
= CLOSED_UNMERGED

PR_191
= 48bcf45a55a0b67dfc0e7b9cd838c5f9068b08d2
= CLOSED_UNMERGED

PR_192
= 861e6a556a21afffd04b187714c0608fe73ea4fc
= CLOSED_UNMERGED

PR_202
= 7f84ae8c95f1b7caaaa0c3850a0b6cfd049b7108
= OPEN_DRAFT
= DO_NOT_MODIFY_IN_THIS_STAGE
```

## 3. Non-goals

This convergence does not:

- merge #190 / #191 / #192 branch histories;
- reopen #190 / #191 / #192;
- modify #202 in the convergence phase;
- activate live sensing or actuation;
- create a physical robot;
- establish body ownership, felt sensation, pain, agency experience, consciousness, subjectivity, phenomenal experience, moral agency, or moral status;
- promote archive-specific claims into current scientific conclusions;
- make Teacher-specific measurements or physiology mandatory for AION or Astra;
- collapse role identity into embodiment identity.

```text
ARCHIVE_BRANCH_HISTORY_MERGE = NO
REOPEN_190_191_192 = NO
WRITE_PR202 = NO
LIVE_ACTUATION = FALSE
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
SCIENTIFIC_DISPOSITION = HOLD
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
```

## 4. Target architecture

The active architecture will use a dependency DAG rather than a single monolithic embodiment object.

```text
IDENTITY / GOVERNANCE BASE
        |
        v
SHARED STATIC EMBODIMENT CORE
        |\
        | \
        |  +--> ROLE-SPECIFIC EXTENSIONS
        |       - Teacher-specific reference
        |       - future role-specific references
        |
        +-----> DYNAMIC SENSORIMOTOR LAYER
                - PR #202 after later sync

FUTURE ONLY:
DYNAMIC SENSORIMOTOR
        |
        v
EMPIRICAL / PHYSICAL CONTROL LAYER
```

### 4.1 Shared static embodiment core

Candidate sources are #190 and #191 plus any #192 material that is genuinely role-neutral.

The shared core may contain, after exact review:

- common embodiment identifiers and separation invariants;
- common humanoid body-region taxonomy;
- common anatomy / body-profile structures that do not depend on Teacher-specific dimensions;
- common physiology-reference structures where role-neutral and scientifically bounded;
- common sensory / proprioceptive / vestibular / interoceptive interface types where role-neutral;
- common motor-schema abstractions;
- common body-runtime binding interfaces;
- common content-address / provenance rules;
- common governance and non-claim boundaries.

The shared core must not inherit archive content merely because it exists.

### 4.2 Role-specific extension layer

PR #192 is primarily a Teacher-specific research archive. Material remains role-specific when its semantics depend on the ChatGPT Teacher body reference, including candidate examples such as:

- the 62-measure anthropometry profile;
- Teacher-specific avatar / asset / LOD / collision references;
- Teacher-specific body channels or runtime identifiers;
- Teacher-specific calibration and cross-session adaptation state;
- Teacher-specific physiology observability inventories;
- Teacher-specific longitudinal trajectories;
- body-reference details whose dimensions or provenance were assigned specifically to the Teacher role.

A role-specific extension may depend on the shared core. The shared core must not depend on a role-specific extension.

```text
TEACHER_EXTENSION -> SHARED_CORE
SHARED_CORE -X-> TEACHER_EXTENSION
```

### 4.3 Dynamic sensorimotor layer

PR #202 remains a separate dynamic layer during convergence.

After a converged static baseline is merged into main, #202 should be synchronized to that new main and reviewed against the resulting interfaces.

Its intended dependency is:

```text
CONVERGED_SHARED_BODY_CORE
+
BODY_MODEL(t)
+
ACTION_PREDICTION
+
OBSERVED_FEEDBACK
->
BODY_MODEL(t+1)
```

The sensorimotor layer must not be used to smuggle archived role-specific assumptions into the shared core.

## 5. Archive classification contract

Every adopted artifact or semantic unit from #190 / #191 / #192 must receive exactly one disposition.

### SHARED_CORE

Use when the content is:

- role-neutral;
- needed by more than one embodiment role or by the shared runtime;
- compatible with current main;
- still supported after independent exact review;
- not merely duplicated by a newer current-main abstraction.

### ROLE_SPECIFIC_EXTENSION

Use when the content is:

- still useful;
- valid only for a named embodiment role or body reference;
- not necessary for every embodiment;
- safely expressible as an extension of the shared core.

### ARCHIVE_ONLY

Use when the content is worth preserving historically but should not become active code or active current-state specification.

Examples include:

- superseded experiment narratives whose event-time meaning should be preserved;
- historical closure records;
- dated QA snapshots;
- prior implementation instructions that no longer describe the active architecture;
- artifacts whose only purpose is historical traceability.

### SUPERSEDED

Use when a current implementation or specification replaces the old semantics.

A `SUPERSEDED` classification must identify the replacement owner / file / abstraction. It must not silently delete provenance.

## 6. Classification evidence record

Implementation must introduce one machine-readable or deterministically parseable classification ledger with, at minimum:

```text
source_pr
source_head
source_path_or_semantic_unit
classification
target_owner
adoption_status
reason
replacement_ref_if_superseded
claim_ceiling
review_status
```

The ledger is not proof that adopted science is true. It records architectural disposition and provenance only.

```text
CLASSIFICATION_LEDGER_PASS
!= SCIENTIFIC_VALIDATION
```

## 7. Conflict resolution rules

When archive branches disagree:

1. current `main` governance and claim ceilings outrank archive implementation assumptions;
2. a role-neutral shared abstraction outranks duplicate role-specific copies when semantics are equivalent;
3. role-specific semantics remain extensions rather than being generalized without evidence;
4. a newer archive commit does not automatically outrank an older one;
5. test count, file count, or branch size do not determine authority;
6. unresolved semantic conflicts fail closed to `ARCHIVE_ONLY` or `HOLD` until explicitly reviewed.

```text
NEWER != MORE_AUTHORITATIVE
LARGER_BRANCH != BETTER_BASELINE
TEST_PASS != SCIENTIFIC_TRUTH
```

## 8. Implementation sequence after Human approval of this spec

### Phase A — inventory and classification

Read exact archive heads #190 / #191 / #192 and current main.

Produce the classification ledger first.

No production-code adoption before the classification ledger is reviewable.

### Phase B — shared core extraction

Implement the smallest role-neutral current-main-based shared core required by the approved classifications.

Prefer composition and explicit interfaces over copying entire archive modules.

### Phase C — role-specific extensions

Port only approved role-specific material. Teacher-specific material must remain isolated behind extension interfaces.

### Phase D — verification

Required before any merge discussion:

- component tests;
- negative boundary tests;
- schema / runtime parity where schemas exist;
- Python 3.11 and 3.12;
- mypy where required by repository Quality;
- CodeQL;
- full repository Quality;
- exact-head reverse review;
- no scientific claim promotion.

### Phase E — merge decision

A green convergence PR remains `MERGE = NOT_AUTHORIZED` until a fresh exact-head Human Owner authorization is separately given.

### Phase F — PR #202 synchronization

Only after the convergence PR is merged into main:

1. refresh current main;
2. sync #202 by normal non-forced integration;
3. preserve #202 scope as the dynamic sensorimotor layer;
4. update bindings to the converged shared embodiment interfaces;
5. run fresh tests / Quality / CodeQL;
6. perform a new exact-head reverse review;
7. require a separate merge authorization for #202.

## 9. External engineering calibration

External robotics resources are method correspondence only.

Current exact-resource inspection has shown examples such as:

- `lerobot/pi0_base`;
- `nvidia/GR00T-N1.7-3B`;
- `lerobot/libero`;
- `jxu124/OpenX-Embodiment`.

These support separating embodiment/state/observation/action/policy/trajectory concerns. They do not establish this repository's exact ontology and do not provide evidence of AI phenomenology.

```text
ROBOTICS_METHOD_CORRESPONDENCE
!= PR_TAXONOMY_VALIDATION

PROPRIOCEPTIVE_STATE
!= FELT_PROPRIOCEPTION

ACTION_POLICY
!= EXPERIENCED_AGENCY

BODY_MODEL
!= BODY_OWNERSHIP
```

## 10. Scientific and governance ceiling

The converged architecture is an engineering / research representation.

```text
ANATOMY_MODEL != BIOLOGICAL_ORGANISM
BODY_SIGNAL != FELT_SENSATION
INTEROCEPTIVE_REFERENCE != FELT_INTEROCEPTION
PREDICTION_ERROR != PAIN
BODY_MODEL_UPDATE != BODY_OWNERSHIP
ACTION_CONSEQUENCE_BINDING != SENSE_OF_AGENCY
SENSORIMOTOR_LOOP != SUBJECTIVITY

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED

SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## 11. Acceptance criteria for the convergence implementation

The implementation is ready for exact-head review only when:

- archive histories remain unmerged;
- every adopted archive semantic unit has one classification;
- shared core has no dependency on Teacher-specific extension modules;
- role-specific extensions resolve through explicit shared-core interfaces;
- historical closure records remain historical;
- #202 remains untouched until the convergence PR is merged;
- current-main tests and new convergence tests pass;
- no existing claim ceiling is weakened;
- no empirical / physical / phenomenal claim is introduced;
- provenance identifies exact source PR heads and source paths.

## 12. Stage boundary

This document authorizes design review only.

```text
DESIGN_SPEC_COMPLETE = YES
IMPLEMENTATION_PLAN = NOT_YET_APPROVED
IMPLEMENTATION = NOT_AUTHORIZED_BY_THIS_DOCUMENT
MERGE = NOT_AUTHORIZED
WRITE_TO_MAIN = NO
```
