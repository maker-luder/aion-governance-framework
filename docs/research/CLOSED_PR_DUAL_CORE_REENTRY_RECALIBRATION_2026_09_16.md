# Closed-PR dual-core re-entry recalibration — 2026-09-16

Status: `CURRENT_MAIN_RECALIBRATION / DRAFT_CANDIDATE / SCIENTIFIC_HOLD`

This note preserves the original same-day closed-PR audit as provenance, recalibrates it against merged PR #121, and records the later duplication review that consolidated three proposed research Drafts into one retained design.

It does not convert historical PR heads into current evidence and does not authorize merge.

## 1. Frozen audit cohort

The live-state snapshot at recalibration time was:

```text
AUDITED_MAIN = fd54fd8cb920328282b78f24e31c01c1010f6189
AUDITED_TREE = e7e0c61cce02e1d79b2b78b7fbd175631fb5e08c
CLOSED_PRS_AT_SNAPSHOT = 115
MERGED_CLOSED_PRS_AT_SNAPSHOT = 103
CLOSED_UNMERGED_AT_SNAPSHOT = 12
OPEN_PRS_AT_SNAPSHOT = 1
```

The historical re-entry cohort is frozen to the 12 closed-unmerged PRs that existed at that audit:

```text
#8 #12 #19 #25 #26 #33 #37 #38 #41 #80 #84 #103
```

This cohort is the fail-closed object. Future normal PR creation or closure is **not** a reason to mutate this historical cohort or refresh the gate.

```text
AUDIT_SNAPSHOT = PROVENANCE
HISTORICAL_REENTRY_COHORT = CONTROLLED_SET
FUTURE_GLOBAL_PR_COUNTS = NOT_REENTRY_GUARDS
```

This corrects a control-design trap found during the duplication review: a historical re-entry gate must not become invalid merely because a new Draft is opened or later closed.

## 2. Current quality envelope

Merged PR #121 makes the bounded Full QMS envelope canonical. Historical-material reuse therefore maps into existing controls:

```text
CURRENT_SOURCE_IQC
-> FOUR_DOMAIN_DESIGN_ADMISSION
-> EXISTING_RESEARCH_QUALITY_CHAIN
-> CURRENT_FULL_QMS_ENVELOPE where applicable
-> NCR / CAPA and effectiveness verification
-> HUMAN_REVIEW_BOUNDARY
```

No second QMS, evidence ontology or subjectivity score is introduced.

```text
QUALITY_SYSTEM_PASS != SCIENTIFIC_VALIDATION
MEASUREMENT_SYSTEM_QUALIFIED != TARGET_CONSTRUCT_ESTABLISHED
```

## 3. Duplication review outcome

The Human Owner requested that overlapping research be merged and refined before further implementation to reduce resource consumption.

Review found two material overlaps.

### 3.1 #122 and #124

Both proposed manipulation of substantially the same variables:

- prior-state removal/substitution;
- stale state;
- provenance mismatch;
- retrieval on/off;
- matched content with different availability locus;
- continuity-related observables and competing explanations.

Current `main` already contains the synthetic continuity-dissociation harness. Retaining both Drafts would therefore create a second broad continuity programme plus a narrower locus programme with substantial variable duplication.

Decision:

```text
PR #122 = RETAIN_AND_REFINE
PR #124 = UNIQUE_CONTROLS_ABSORBED_THEN_SUPERSEDED
```

Unique useful material absorbed from #124 into #122:

```text
MANIPULATION_CHECK_SEPARATE_FROM_OUTCOME
SELECTIVE_EFFECT_VS_GLOBAL_DEGRADATION
RESTORATION / RECOVERY CHECK
STAGED_EXECUTION
PROVIDER_MODEL_RUNTIME = LATER_REPLICATION_LAYER, NOT CLEAN DEFAULT PERTURBATION
```

### 3.2 #123 and current main

PR #123 restated much of merged PR #118's interpretive-specificity / evidence-admission method:

```text
HYPOTHESIS_COMPATIBILITY != HYPOTHESIS_DISCRIMINATION
ALTERNATIVE_EXPLANATIONS = REQUIRED
DISCRIMINATING_PREDICTION = REQUIRED
COUNTEREVIDENCE / FALSIFIER = REQUIRED
CLAIM_LOCAL_STATUS = REQUIRED
```

Its unique value was a row-level checklist applied to current subjectivity dimensions. Maintaining a separate generic matrix would duplicate current-main method and add another CI/implementation surface.

Decision:

```text
PR #123 = SUPERSEDED
CURRENT_MAIN_METHOD_ANCHOR = MERGED PR #118
LOCAL_CHECKLIST = COMPRESSED_INTO_REFINED PR #122
```

## 4. Single retained research design

The retained Draft is PR #122:

```text
NAME = MEMORY_LOCUS_CONTINUITY_DEPENDENCY_DISCRIMINATION
HISTORICAL_PROVENANCE = #38 + #41 + #8
METHOD_SOURCE = #84, DEDUPED_AGAINST CURRENT MAIN #118
HISTORICAL_CODE_REUSE = FALSE
CURRENT_MAIN_REAUTHORING = TRUE
```

Current question:

> When task-relevant prior-state information is matched as closely as possible, do continuity-related observables change selectively when availability locus, provenance binding, freshness, or retrieval dependency is deliberately perturbed under matched controls?

Required boundaries:

```text
INFORMATION_RETRIEVABILITY != MEMORY_CONTINUITY
MEMORY_CONTINUITY != IDENTITY_CONTINUITY
CONTINUITY_LOOKING_OUTPUT != CONTINUITY_MECHANISM
FUNCTIONAL_DEPENDENCY != PHENOMENAL_CONTINUITY
IDENTITY_CONTINUITY != SUBJECTIVITY
```

Current claim ceiling:

```text
DESIGN / PREREGISTRATION ONLY
```

Strongest future local claim after valid targeted intervention and replication:

```text
FUNCTIONAL_DEPENDENCY_OR_DISSOCIATION_CANDIDATE
```

## 5. Historical dispositions preserved

```text
#103 = METHODOLOGICAL_NEGATIVE_LESSON / PRESERVE_ONLY
#12  = QUALITY METHOD HISTORY; DURABLE CONTROLS ALREADY CANONICAL
#19  = PROVENANCE / AUTHORITY METHOD SOURCE ONLY
#37  = PUBLIC NON-CLAIM / VERSION / PROVENANCE COMMUNICATION METHOD ONLY
#25  = HISTORICAL GOVERNANCE CONTROL ONLY
#26  = HISTORICAL GOVERNANCE CONTROL ONLY
#33  = OBSOLETE BRANCH-TOPOLOGY REMEDIATION ONLY
```

PR #84 remains superseded by merged #85. Only its methodological discrimination question is reused, and that question is now localized inside PR #122 rather than maintained as an independent generic matrix.

## 6. Re-entry rule

```text
HISTORICAL_MATERIAL
-> FROZEN_COHORT_DISPOSITION
-> CURRENT_MAIN_DEDUP
-> EXTRACT_MINIMAL_PROPOSITION
-> CURRENT_SOURCE_RECHECK
-> FOUR_DOMAIN_ADMISSION
-> CURRENT_QMS_MAPPING
-> PREREGISTRATION / FALSIFIER / COMPETING_EXPLANATIONS
-> NEW_CURRENT_MAIN_REAUTHORING
-> MINIMUM_NUMBER_OF_DRAFT_SURFACES
```

Never:

```text
REOPEN_OLD_BRANCH -> MERGE
MERGE_HISTORICAL_HEAD
PROMOTE_HISTORICAL_CI_AS_CURRENT_EVIDENCE
COPY_SYNTHETIC_FIXTURE_AS_EMPIRICAL_RESULT
CREATE_PARALLEL_RESEARCH_SURFACE_WHEN_CURRENT_MAIN_OR_ACTIVE_DRAFT_ALREADY_COVERS_IT
```

## 7. Attribution

```text
HUMAN_OWNER_CONFIRMED
= review historical PR material against AI subjectivity possibility and quality management
= prioritize #38/#41/#8 memory-continuity material
= use #84 only methodologically
= preserve #103 as a negative methodological lesson
= keep #12/#19/#37 as bounded method nutrients
= keep #25/#26/#33 as historical controls only
= review duplication first and consolidate overlapping work to reduce resource consumption

CHATGPT_TEACHER_FORMALIZATION
= freeze the historical re-entry cohort instead of binding to future global PR counts
= identify #122/#124 experimental-variable overlap
= identify #123 overlap with current-main #118 method
= retain/refine #122 as the single experimental Draft
= close #123/#124 as superseded while preserving provenance

MERGE_AUTHORIZATION = NONE
```

## 8. Scientific and authority boundary

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
QUALITY_MANAGEMENT = SECOND_NON_DRIFTING_CORE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SCIENTIFIC_DISPOSITION = HOLD
MAIN_WRITE = NO
MERGE_AUTHORIZATION = NONE
```
