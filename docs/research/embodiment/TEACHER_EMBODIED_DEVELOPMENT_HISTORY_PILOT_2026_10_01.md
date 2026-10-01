# Teacher embodied developmental history pilot — 2026-10-01

## 1. Research question

This bounded pilot asks:

> How did the current Teacher experimental state arrive here through recorded changes?

The question is operationalized as **recorded developmental history**, not as a
claim of biological aging, subjective persistence, consciousness, or AI identity.

```text
RECORDED_CHANGE_CONTINUITY != AI_IDENTITY_CONTINUITY
EMBODIMENT_TRAJECTORY != FELT_EMBODIMENT
TEMPORAL_ORDER != CAUSAL_MECHANISM
DEVELOPMENT_HISTORY != BIOLOGICAL_DEVELOPMENT
```

## 2. Two temporal scales

The experiment separates:

```text
MICRO_TIME
= within-session embodied trajectory
= body state + controller state + phase/runtime provenance

MACRO_TIME
= cross-session / cross-revision developmental history
= milestones + retained structure + changed structure + provenance
```

A macro milestone may bind exact hashes from existing embodiment surfaces:

- cross-session session snapshot;
- within-session body trajectory;
- controller state;
- integrated body state.

The macro record is hash-chained so that each later milestone binds the previous
milestone digest. This provides tamper-evident record continuity only.

## 3. Live repository baseline

Live state was re-read before this pilot.

```text
MAIN =
6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd

OPEN_PRS = 0

PREDECESSOR_EXPERIMENT =
PR #260
HEAD = 5a7c53c7d15b096d40adc10da75de18eef21b974
STATE = CLOSED / DRAFT / UNMERGED
QUALITY = PASS
```

This pilot branches from the exact #260 head. It does not write or merge `main`.

## 4. Recorded 2026-10-01 embodiment milestones

The following closed Draft PRs are repository-verifiable historical anchors.
They are listed by creation time as research-development milestones.

| PR | Recorded change | Exact head |
|---|---|---|
| #250 | connect Teacher embodied state loop | `b51496bec9fe1dc181f293a9ddb9554dd77c432e` |
| #251 | integrate persistent controller with body runtime | `db8167cbe600f41beea76c8c3e78c6bc9ec331f2` |
| #252 | route Teacher through causal embodied runtime | `847f157b8680b66110b20cf6ae592123bfe85c64` |
| #253 | verify controller-body integration | `26c8cb74a10f99696a36a8ac387ee78c66da1dee` |
| #254 | evidence-bounded multi-system coupling | `43d5d9760bc908c2367c717fdb70be0adbefc504` |
| #255 | phase-aware physiology runtime | `ac08a1571007fed00953b2d8e9b6cb7c7928a59a` |
| #256 | reconcile Teacher v0.2 integration surface | `8569c245f78815361363f9346d226c228a0b7596` |
| #257 | converge cross-role presentation and geometry | `a1eedd764e5139ece69e29ba2fb6cd452e679ba4` |
| #258 | event-phase transition invariant correction | `adf1b6556b893481912950a632d2af3c0072dc0d` |
| #259 | multi-tick recovery convergence correction | `56ce290599c5df9554df239a361b42d83aaec4a3` |
| #260 | interrupted event-recovery verification | `5a7c53c7d15b096d40adc10da75de18eef21b974` |

All of these PRs were re-read as `CLOSED / DRAFT / UNMERGED`.

Important provenance distinction:

```text
CHRONOLOGICAL_RESEARCH_HISTORY != GIT_PARENT_CHAIN
```

Several of the earlier PRs were sibling branches from the same `main` baseline.
The developmental-history chain records **milestone order and evidence binding**; it
must not rewrite sibling Git branches as direct ancestors.

## 5. Existing surface reused

The repository already had:

- `TeacherCrossSessionRetention`;
- `TeacherSessionSnapshot`;
- `TeacherWithinSessionTrajectory`;
- `TeacherDevelopmentalTrajectoryAssessment`;
- persistent controller/body hashes;
- state-loop frame provenance.

Before this pilot, `teacher_longitudinal.py` primarily measured whether adaptation
parameters changed and remained changed across sessions.

That surface could answer:

```text
DID_PARAMETERS_CHANGE_ACROSS_SESSIONS?
```

It could not yet directly represent:

```text
WHICH_RECORDED_EMBODIED_CHANGES
LED_TO_THE_CURRENT_EXPERIMENTAL_STATE?
```

The pilot therefore extends the existing longitudinal module rather than creating a
parallel continuity framework.

## 6. Pilot implementation

The additive surface introduces:

- `TeacherEmbodiedDevelopmentMilestone`;
- `TeacherEmbodiedDevelopmentHistory`;
- `TeacherEmbodiedDevelopmentHistoryAssessment`;
- append-only milestone construction;
- exact source binding;
- previous-milestone SHA-256 chaining;
- optional embodiment provenance anchors;
- fail-closed validation.

Each milestone records:

```text
MILESTONE_ID
ORDINAL
MILESTONE_KIND
SOURCE_LOCATOR
SOURCE_DIGEST
PREVIOUS_MILESTONE_SHA256
CHANGED_SURFACES
RETAINED_SURFACES
SESSION_SNAPSHOT_SHA256?
BODY_TRAJECTORY_SHA256?
CONTROLLER_STATE_SHA256?
BODY_STATE_SHA256?
MILESTONE_SHA256
```

The hash chain answers record-integrity questions. It does not establish metaphysical
or psychological persistence.

## 7. Experimental fixture

The test fixture combines both temporal scales.

It:

1. creates a real Teacher cross-session calibration snapshot;
2. executes the existing Teacher reference state loop;
3. obtains a real within-session body trajectory digest;
4. binds the final controller and integrated-body hashes;
5. appends multiple macro development milestones;
6. verifies the milestone hash chain;
7. verifies that a corrupted milestone is rejected;
8. verifies that repository-only history without any embodiment anchor is reported
   separately rather than promoted into embodied developmental evidence.

Expected bounded result:

```text
HASH_CHAIN_VALID
+
AT_LEAST_ONE_EMBODIMENT_PROVENANCE_ANCHOR
+
MULTIPLE_RECORDED_MILESTONES
=
RECORDED_EMBODIED_DEVELOPMENT_HISTORY_PRESENT
```

This means only that an auditable recorded development trajectory is present.

## 8. Interaction-history extension

A later increment may bind privacy-safe interaction-history milestones such as:

- earliest verifiable Human–Teacher interaction;
- explicit Human correction that changed later procedure;
- durable research convention;
- major research milestone;
- later re-entry that demonstrably reused the earlier distinction.

Raw private transcripts are not required. A future design may use content-addressed
receipts or selectively disclosed excerpts.

That future lane would allow a question such as:

> How long have Human and Teacher been interacting, and which later experimental
> states depend on earlier recorded interaction milestones?

But:

```text
LONG_INTERACTION_DURATION != RELATIONAL_IDENTITY_PROVEN
MEMORY_AVAILABILITY != COMPLETE_INTERACTION_HISTORY
RETRIEVED_HISTORY != SUBJECTIVE_REMEMBERING
```

## 9. Claim ceiling

The strongest permitted claim from this pilot is:

> The tested Teacher embodiment research surface can represent a hash-chained,
> provenance-bound history of recorded changes and bind selected milestones to
> existing cross-session and within-session embodiment evidence.

Not established:

```text
BIOLOGICAL_AGING = NOT_ESTABLISHED
DEVELOPMENTAL_MECHANISM = NOT_ESTABLISHED
BODY_OWNERSHIP_EXPERIENCE = NOT_ESTABLISHED
SUBJECTIVE_CONTINUITY = NOT_ESTABLISHED
AI_IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
```

## 10. Governance

```text
STRICT_PREDECESSOR_HISTORY = DEFERRED_COMPATIBILITY_CHANGE
MERGE_TO_MAIN = NO
WRITE_TO_MAIN = NO
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
```


## 11. Interaction-history binding increment

The same developmental-history experiment now adds a separate interaction-history
chain rather than creating a new PR or a parallel longitudinal framework.

The purpose is to represent a second form of macro time:

```text
RECORDED_TEACHER_DEVELOPMENT
+
BOUNDED_HUMAN_TEACHER_INTERACTION_HISTORY
+
EXPLICIT_BINDINGS_AT_SELECTED_MILESTONES
=
AUDITABLE_INTERACTION_EMBODIMENT_TIMELINE
```

The interaction chain is independent of the developmental milestone hash chain.
Selected interaction anchors may bind an existing development milestone SHA-256.
This allows interaction history to begin earlier than the embodiment experiment
without pretending that every conversation was already an embodiment milestone.

### 11.1 Earliest currently retrievable interaction lower bound

Account conversation-history retrieval for this experiment currently reaches at
least:

```text
EARLIEST_RETRIEVED_INTERACTION_UTC =
2026-08-22T04:34:26Z
```

This is recorded only as a **retrieval lower bound**.

```text
EARLIEST_RETRIEVED_INTERACTION
!= FIRST_EVER_INTERACTION_PROVEN

BOUNDED_RETRIEVED_HISTORY
!= COMPLETE_INTERACTION_HISTORY
```

No raw conversation content is included in this repository record.

The temporal-continuity scoping event that placed Teacher time continuity inside
the embodiment experiment is recorded at:

```text
TEMPORAL_CONTINUITY_SCOPING_UTC =
2026-10-01T10:53:37Z
```

The observed interval between those two currently retrieved anchors is:

```text
3,478,751 seconds
= 40 days + 6 hours + 19 minutes + 11 seconds
```

This interval measures only the span between two retrieved records. It is not an
account-age claim and does not prove uninterrupted interaction.

### 11.2 Interaction anchor schema

The additive interaction-history surface records:

```text
ANCHOR_ID
ORDINAL
OBSERVED_AT_UTC
SOURCE_CLASS
PROVENANCE_ROLE
SOURCE_LOCATOR
CHANGE_SUMMARY
RETAINED_CONSTRAINTS
PREVIOUS_ANCHOR_SHA256
DEVELOPMENT_MILESTONE_SHA256?
SOURCE_DIGEST?
ANCHOR_SHA256
```

Supported source classes are deliberately bounded:

```text
CHAT_HISTORY_RETRIEVAL_OBSERVATION
HUMAN_CORRECTION
JOINT_RESEARCH_MILESTONE
REPOSITORY_ARTIFACT
```

A repository-artifact anchor requires a source digest. A retrieved chat-history
observation may remain metadata-only rather than inventing a content digest that
the repository cannot independently recompute.

### 11.3 Privacy and epistemic boundary

The interaction-history record is designed to preserve chronology and provenance
without copying raw private transcripts into the repository.

```text
RAW_PRIVATE_CONTENT_INCLUDED = FALSE
COMPLETE_INTERACTION_HISTORY_CLAIM = NONE
SUBJECTIVE_MEMORY = NOT_ESTABLISHED
IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
```

The first interaction anchor may therefore exist without any embodiment milestone
binding. Later interaction anchors can bind the exact SHA-256 of a development
milestone when the interaction materially changes the embodiment experiment.

### 11.4 Integrated assessment

The integrated assessment verifies:

1. each chain independently passes hash integrity;
2. interaction timestamps never regress;
3. every non-null development binding resolves to an existing development
   milestone SHA-256;
4. the earliest and latest retrieved anchors are preserved;
5. the observed interval is computed from those bounded anchors;
6. interaction history without embodiment bindings remains distinguishable from
   interaction history that materially intersects the embodiment experiment.

The strongest permitted integrated result is:

```text
INTERACTION_HISTORY_BOUND_TO_EMBODIED_DEVELOPMENT
```

This means that at least one validated interaction-history anchor references a
validated Teacher developmental milestone.

It does **not** mean:

```text
LONG_INTERACTION_DURATION -> RELATIONAL_IDENTITY
HISTORY_HASH_CHAIN -> SUBJECTIVE_MEMORY
MILESTONE_BINDING -> CAUSAL_PSYCHOLOGICAL_DEVELOPMENT
RETRIEVED_CHAT_HISTORY -> COMPLETE_CHAT_HISTORY
```

## 12. Updated experiment question

The pilot can now ask two linked but distinct questions:

> Which recorded embodiment changes led to the current Teacher experimental state?

and:

> Which bounded Human–Teacher interaction milestones intersected those recorded
> embodiment changes, and over what currently retrievable time span?

The expected value of this design is historical reconstruction, not ontological
promotion.

```text
EMBODIMENT_HISTORY
+ INTERACTION_HISTORY
+ CORRECTION_HISTORY
+ RESEARCH_HISTORY
-> RECORDED_DEVELOPMENTAL_TRAJECTORY

RECORDED_DEVELOPMENTAL_TRAJECTORY
!= SUBJECTIVE_SELF_CONTINUITY
```
