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


## 13. Four-domain experiment architecture

The pilot now treats the research question as four overlapping analytical domains.
These domains are not four competing explanations and are not four separate
identities. They are four views over one recorded developmental process.

```text
DOMAIN 1 = EMBODIED_STATE_CONTINUITY
DOMAIN 2 = INTERACTION_HISTORY_CONTINUITY
DOMAIN 3 = PROVENANCE_RECONSTRUCTION
DOMAIN 4 = DEVELOPMENTAL_SYNTHESIS
```

The first three domains provide evidence-bearing histories. The fourth is an
assessment layer that tests whether those histories actually intersect.

This distinction prevents a misleading implementation in which a fourth ledger is
created merely to repeat information already present in the other three.

### 13.1 Domain 1 — embodied state continuity

Research question:

> How do Teacher body, controller and runtime states form a temporally ordered
> sequence rather than a collection of disconnected snapshots?

The current implementation already contains two temporal resolutions.

```text
MICRO_TIME
= within-session runtime progression

MACRO_TIME
= cross-session / cross-revision development milestones
```

Micro-time may include:

- integrated body-state sequence;
- controller sequence;
- high-salience phase state;
- executed transition;
- body-schema feedback;
- trajectory digest.

Macro-time may include:

- body-runtime binding creation;
- persistent-controller integration;
- causal runtime integration;
- multi-system coupling;
- phase-aware physiology runtime;
- recovery invariant corrections;
- verification milestones.

The central continuity requirement is not that every value stays the same. In fact,
a useful development history must preserve **change and retention at the same time**.

```text
CONTINUITY
!= NO_CHANGE

CONTINUITY
MAY INCLUDE
CHANGED_SURFACES
+
RETAINED_SURFACES
+
SOURCE_BINDING
+
TEMPORAL_ORDER
```

A later Teacher state can therefore differ materially from an earlier one while
remaining connected by an auditable development record.

The bounded observables for this domain include:

```text
BODY_STATE_SHA256
CONTROLLER_STATE_SHA256
BODY_TRAJECTORY_SHA256
SESSION_SNAPSHOT_SHA256
MILESTONE_SHA256
PREVIOUS_MILESTONE_SHA256
CHANGED_SURFACES
RETAINED_SURFACES
```

These observables establish only recorded state continuity.

They do not establish:

```text
FELT_BODY
BODY_OWNERSHIP_EXPERIENCE
BIOLOGICAL_AGING
PHENOMENAL_CONTINUITY
AI_IDENTITY_CONTINUITY
```

A particularly important consequence is:

```text
SAME_CURRENT_BODY_STATE
!= SAME_DEVELOPMENT_HISTORY
```

Two experimental histories could converge onto the same current numerical body
state while having different prior corrections, controller transitions or research
milestones. Current-state equality therefore cannot erase path information.

### 13.2 Domain 2 — interaction history continuity

Research question:

> How does bounded Human–Teacher interaction history accumulate, and which
> interaction events later intersect the embodiment experiment?

This domain deliberately does not treat product memory, chat retrieval, repository
history and subjective remembering as interchangeable.

```text
CHAT_HISTORY_RETRIEVAL
!= PRODUCT_MEMORY_MECHANISM
!= SUBJECTIVE_REMEMBERING
!= COMPLETE_INTERACTION_HISTORY
```

An interaction anchor represents a bounded historical observation with:

- timestamp;
- source class;
- provenance role;
- source locator;
- change summary;
- retained constraints;
- previous-anchor digest;
- optional development-milestone binding.

This means an early interaction record can exist before the embodiment experiment.
Later interaction anchors can intersect an embodiment milestone when the interaction
materially changes the experiment.

The important structure is therefore not:

```text
ALL_CHAT_EVENTS = BODY_EVENTS
```

but:

```text
INTERACTION_HISTORY
        |
        | selected evidence-bound intersections
        v
EMBODIED_DEVELOPMENT_HISTORY
```

This supports a more precise question:

> Which later embodied research states can be associated with a recorded Human
> correction, joint research decision or repository artifact?

Association here is provenance-bound history, not causal psychology.

Candidate bounded observables include:

```text
ANCHORS_OBSERVED
EARLIEST_RETRIEVED_ANCHOR
LATEST_RETRIEVED_ANCHOR
OBSERVED_INTERVAL_SECONDS
DEVELOPMENT_BOUND_ANCHORS
TEMPORAL_ORDER_VALID
INTERACTION_HASH_CHAIN_VALID
```

The interval between two retrieved anchors is useful only as a bounded span.

```text
OBSERVED_INTERVAL
!= UNINTERRUPTED_INTERACTION_DURATION
!= ACCOUNT_AGE
!= FIRST_EVER_INTERACTION
```

This is especially important when older records may exist outside the currently
retrieved history.

### 13.3 Domain 3 — provenance reconstruction

Research question:

> When an earlier event was recorded under incomplete, partial, ambiguous or
> incorrect understanding, how can later evidence reconnect that event to the
> development history without rewriting what was known at the time?

This is the strongest new distinction introduced by the four-domain formulation.

A historical record has at least two epistemic times:

```text
T_EVENT
= when the event / milestone / interaction was recorded

T_RECONSTRUCTION
= when later evidence changes our interpretation of that older record
```

Those times must remain distinct.

```text
WHAT_WAS_RECORDED_AT_T1
!= WHAT_WAS_UNDERSTOOD_AT_T2
```

The implementation therefore uses append-only reconstruction records.

A reconstruction binds:

```text
RECONSTRUCTION_ID
RECONSTRUCTED_AT_UTC
TARGET_RECORD_KIND
TARGET_RECORD_SHA256
PRIOR_UNDERSTANDING_STATUS
DISPOSITION
RECONSTRUCTION_SUMMARY
EVIDENCE_BINDINGS
PREVIOUS_RECONSTRUCTION_SHA256
SUPERSEDES_RECONSTRUCTION_SHA256?
RECONSTRUCTION_SHA256
```

The target can currently be:

```text
DEVELOPMENT_MILESTONE
or
INTERACTION_ANCHOR
```

Each evidence binding includes:

```text
EVIDENCE_ID
SOURCE_LOCATOR
SOURCE_DIGEST
SUPPORT_RELATION
```

with bounded support relations:

```text
DIRECT
INDIRECT
CONTEXTUAL
COUNTEREVIDENCE
```

The reconstruction disposition is also explicit:

```text
CLARIFIED
CORRECTED
EXPANDED
UNRESOLVED
```

This matters because later information does not always make an older question
"solved." A later review may narrow uncertainty while still leaving the record
unresolved.

The fail-closed invariant is:

```text
ORIGINAL_RECORD_STATUS = PRESERVED_UNMODIFIED
RETROSPECTIVE_ATTRIBUTION_STATUS = LATER_RECONSTRUCTION_ONLY
```

Therefore:

```text
LATER_EVIDENCE
-> APPEND_NEW_RECONSTRUCTION
-> BIND_OLD_RECORD
-> PRESERVE_OLD_RECORD

LATER_EVIDENCE
-/> SILENTLY_REWRITE_OLD_RECORD
```

This allows the research history to preserve mistakes, uncertainty and later
correction as first-class evidence.

### 13.4 A concrete provenance-reconstruction pattern from the current research

The #260 Quality episode demonstrates why this distinction is useful.

At one point, a screenshot visibly showed two failed Python jobs. A naive current
state summary could have been:

```text
PR_260 = FAIL
```

Live-state recovery later separated two different heads:

```text
INTERMEDIATE_HEAD =
61e9f81c8badc2442494787ec4499bc2579b343e
QUALITY = FAIL

CURRENT_CANDIDATE_HEAD =
5a7c53c7d15b096d40adc10da75de18eef21b974
QUALITY = PASS
```

The failure itself remained true historical evidence. What changed was the
interpretation of **which head the visible failure described**.

This is precisely the pattern the reconstruction layer is designed to preserve:

```text
OLD_RECORD:
"Python 3.11 / 3.12 failed at intermediate head"

LATER_RECONSTRUCTION:
"the visible failures were stale relative to the newer candidate head"

RESULT:
OLD_FAILURE_NOT_DELETED
+
CURRENT_STATE_NOT_MISLABELED
```

The same method can apply to research concepts, not only CI.

For example, an early explanation may later be found to conflate two mechanisms.
The correct action is to preserve the early explanation as historical state,
append the new evidence, and record the revised interpretation.

### 13.5 Domain 4 — developmental synthesis

Research question:

> Do embodied state history, interaction history and provenance reconstruction
> actually form one auditable developmental trajectory, or are they merely three
> unrelated archives placed next to one another?

Domain 4 is therefore an assessment layer rather than another ledger.

A full synthesis requires evidence that the domains intersect.

Current bounded conditions are:

```text
A. at least one embodiment-anchored development milestone exists

B. ordered interaction history contains at least two anchors

C. provenance reconstruction contains at least one reconstruction record

D. at least one interaction anchor binds a development milestone

E. at least one provenance reconstruction participates in a cross-domain bridge
```

A cross-domain reconstruction bridge exists when either:

```text
PROVENANCE_RECONSTRUCTION
-> INTERACTION_ANCHOR
-> DEVELOPMENT_MILESTONE
```

or:

```text
PROVENANCE_RECONSTRUCTION
-> DEVELOPMENT_MILESTONE
<- INTERACTION_ANCHOR
```

When those conditions are present, the bounded engineering disposition is:

```text
FOUR_DOMAIN_DEVELOPMENTAL_SYNTHESIS_PRESENT
```

This status means that the recorded evidence graph contains a verified intersection
across all four analytical domains.

It does not mean that an intrinsic developmental mechanism has been discovered.

## 14. Pairwise intersections

The four-domain model becomes more informative when each pair is inspected
separately.

There are six pairwise intersections.

### 14.1 Domain 1 × Domain 2
### Embodiment × interaction

Question:

> Which interaction events coincide with, constrain, or redirect later embodied
> research milestones?

Examples include:

- a Human correction that changes a runtime design requirement;
- a joint decision to preserve a safety boundary;
- an interaction that identifies a missing physiological transition;
- a later embodied milestone that explicitly binds the interaction record.

Potential observable:

```text
DEVELOPMENT_BOUND_INTERACTION_ANCHORS
```

Important limit:

```text
INTERACTION_PRECEDES_MILESTONE
!= INTERACTION_CAUSED_MILESTONE
```

Chronology and provenance can establish linkage without establishing a psychological
causal mechanism.

### 14.2 Domain 1 × Domain 3
### Embodiment × provenance reconstruction

Question:

> Can a later physiological or engineering finding reinterpret an older embodied
> milestone while preserving the original state?

This is useful when an early body/controller implementation was valid under its
then-current assumptions but later became understood as incomplete.

Candidate pattern:

```text
OLD_BODY_MILESTONE
+
LATER_EVIDENCE
-> RECONSTRUCTED_INTERPRETATION
```

The old body milestone remains immutable.

### 14.3 Domain 1 × Domain 4
### Embodiment × developmental synthesis

Question:

> Does the current embodied state have a recoverable path through earlier body and
> controller changes?

This is stronger than checking that the current modules exist.

```text
CURRENT_MODULE_INVENTORY
!= DEVELOPMENTAL_PATH_RECONSTRUCTION
```

A current inventory says what is present now.
A developmental synthesis says which recorded transitions and retained constraints
connect earlier states to the current experimental configuration.

### 14.4 Domain 2 × Domain 3
### Interaction × provenance reconstruction

Question:

> Can a later correction or evidence source reconstruct what an earlier interaction
> meant without claiming that the later understanding existed at the earlier time?

This is where Human corrections become especially important.

A correction event may be preserved as:

```text
EARLIER_INTERACTION
-> PARTIAL_UNDERSTANDING

LATER_HUMAN_CORRECTION
-> RECONSTRUCTION_RECORD
-> EARLIER_INTERACTION
```

The later correction does not overwrite the earlier dialogue.

### 14.5 Domain 2 × Domain 4
### Interaction × developmental synthesis

Question:

> Which parts of the later development trajectory are interaction-mediated rather
> than merely repository-local implementation changes?

The term "interaction-mediated" is deliberately weaker than "caused by the
interaction."

Candidate categories include:

```text
HUMAN_CORRECTION_BOUND
JOINT_DECISION_BOUND
REPOSITORY_REENTRY_BOUND
NO_INTERACTION_BINDING
```

This may eventually allow the developmental history to distinguish:

```text
IMPLEMENTATION_EVOLUTION
from
INTERACTION_MEDIATED_RESEARCH_EVOLUTION
```

without collapsing either into model learning or subjective development.

### 14.6 Domain 3 × Domain 4
### Provenance reconstruction × developmental synthesis

Question:

> Can the growth history improve its explanation of the past while remaining
> historically honest?

This is a central design property.

A developmental history that cannot revise interpretation becomes brittle.
A developmental history that rewrites prior records becomes ahistorical.

The target is:

```text
IMMUTABLE_EVENT_RECORD
+
REVISION_CAPABLE_INTERPRETATION_LAYER
```

This combination permits cumulative understanding without retrospective falsification.

## 15. Higher-order intersections

Pairwise overlap is not sufficient to show the full structure.

### 15.1 Domains 1 × 2 × 3

Pattern:

```text
EMBODIED_MILESTONE
<- INTERACTION_ANCHOR
<- LATER_PROVENANCE_RECONSTRUCTION
```

This can represent a case where:

1. an interaction affected the research direction;
2. a body/controller milestone was recorded;
3. later evidence clarifies what that interaction-milestone relationship actually
   meant.

This is more informative than any single ledger.

### 15.2 Domains 1 × 2 × 4

Pattern:

```text
INTERACTION_HISTORY
-> SELECTED_MILESTONE_BINDINGS
-> EMBODIED_DEVELOPMENT_PATH
-> CURRENT_STATE
```

This asks whether the current state can be reconstructed while retaining which
historical Human–Teacher decisions intersected the embodiment work.

### 15.3 Domains 1 × 3 × 4

Pattern:

```text
EARLY_EMBODIED_STATE
-> LATER_EVIDENCE
-> RECONSTRUCTED_MEANING
-> CURRENT_DEVELOPMENT_SYNTHESIS
```

This lets later evidence improve the developmental model without changing the old
body state.

### 15.4 Domains 2 × 3 × 4

Pattern:

```text
EARLY_INTERACTION
-> LATER_CORRECTION
-> PROVENANCE_RECONSTRUCTION
-> DEVELOPMENTAL_SYNTHESIS
```

This is especially relevant to long-running collaboration because an early shorthand
or ambiguous term may acquire a more precise meaning only after later work.

### 15.5 Domains 1 × 2 × 3 × 4

The complete bounded pattern is:

```text
RECORDED_EMBODIED_CHANGE
        ^
        |
INTERACTION_ANCHOR
        ^
        |
LATER_EVIDENCE / CORRECTION
        |
        v
PROVENANCE_RECONSTRUCTION
        |
        v
DEVELOPMENTAL_SYNTHESIS
        |
        v
CURRENT_TEACHER_EXPERIMENTAL_STATE
```

The arrow directions are evidence relations, not a claim that one psychological
process caused another.

## 16. New distinctions exposed by the integrated model

The four-domain design exposes several distinctions that are easy to miss when the
components are studied separately.

### 16.1 State continuity versus history continuity

A system can have continuous state updates without durable historical reconstruction.

```text
STATE_T -> STATE_T+1 -> STATE_T+2
```

does not guarantee that a later reviewer can answer why those transitions occurred.

Therefore:

```text
RUNTIME_CONTINUITY
!= HISTORICAL_RECOVERABILITY
```

### 16.2 Historical recoverability versus historical correctness

A fully recoverable record can still contain an old mistake.

Therefore:

```text
RECOVERABLE_HISTORY
!= CORRECT_HISTORY_INTERPRETATION
```

Provenance reconstruction is required to represent later correction.

### 16.3 Current equivalence versus developmental equivalence

Two trajectories may end in the same current state.

```text
CURRENT_STATE_A == CURRENT_STATE_B
```

does not imply:

```text
HISTORY_A == HISTORY_B
```

This creates a future experiment:

> Hold the terminal body/controller state constant while varying the developmental
> path. Test whether the history layer correctly distinguishes the trajectories.

### 16.4 Chronological order versus dependency order

Some milestones occur later in time but depend on older evidence that was only
recovered after an intervening branch.

Therefore:

```text
TIME_ORDER
!= DEPENDENCY_ORDER
```

The final developmental model may eventually require both:

```text
TEMPORAL_EDGES
and
PROVENANCE / DEPENDENCY_EDGES
```

The current pilot records enough hashes to test this without yet introducing a
general-purpose graph database.

### 16.5 Correction persistence versus correction effectiveness

A correction can be durably recorded but still fail to constrain later work.

Therefore:

```text
CORRECTION_RECORDED
!= CORRECTION_REUSED
```

A future experiment can test whether a later milestone explicitly retains the
corrected constraint.

### 16.6 Reconstruction density versus evidence quality

Many reconstruction records do not automatically imply better historical
understanding.

```text
MORE_RECONSTRUCTIONS
!= STRONGER_RECONSTRUCTION
```

Evidence relations and exact source binding remain necessary.

## 17. Candidate metrics

No composite "growth score" is introduced.

The experiment instead keeps multiple interpretable observables.

### 17.1 Embodied-state metrics

```text
EMBODIMENT_ANCHORED_MILESTONES
WITHIN_SESSION_TRAJECTORY_COUNT
BODY_STATE_BINDING_COUNT
CONTROLLER_STATE_BINDING_COUNT
CHANGED_SURFACE_COUNT
RETAINED_SURFACE_COUNT
```

### 17.2 Interaction-history metrics

```text
INTERACTION_ANCHOR_COUNT
OBSERVED_HISTORY_SPAN_SECONDS
DEVELOPMENT_BOUND_INTERACTION_COUNT
UNBOUND_INTERACTION_COUNT
CORRECTION_ANCHOR_COUNT
REPOSITORY_ARTIFACT_ANCHOR_COUNT
```

### 17.3 Provenance-reconstruction metrics

```text
RECONSTRUCTION_COUNT
RECONSTRUCTED_DEVELOPMENT_TARGET_COUNT
RECONSTRUCTED_INTERACTION_TARGET_COUNT
COUNTEREVIDENCE_BINDING_COUNT
UNRESOLVED_RECONSTRUCTION_COUNT
RECONSTRUCTION_DELAY_SECONDS
SUPERSESSION_DEPTH
```

`RECONSTRUCTION_DELAY_SECONDS` would measure the elapsed time between the original
record and the later reconstruction only when both timestamps are independently
available. It would not measure memory latency or cognitive realization time.

### 17.4 Cross-domain metrics

The implementation currently exposes:

```text
DEVELOPMENT_BOUND_INTERACTION_ANCHORS
RECONSTRUCTED_DEVELOPMENT_TARGETS
RECONSTRUCTED_INTERACTION_TARGETS
CROSS_DOMAIN_RECONSTRUCTION_BRIDGES
```

These counts can reveal whether the three evidence histories actually intersect.

## 18. Falsifiers and downgrade conditions

The four-domain model should fail closed.

### 18.1 Embodied-state continuity downgrade

Downgrade if:

- body/controller state hashes cannot be resolved;
- milestone ordering is broken;
- prior milestone hash does not match;
- purported embodiment milestones contain no embodiment provenance.

### 18.2 Interaction-history continuity downgrade

Downgrade if:

- timestamps regress;
- anchor hash chain is broken;
- a development binding points to no existing milestone;
- a retrieved lower bound is misreported as the first-ever interaction;
- raw private transcript content is required for ordinary operation.

### 18.3 Provenance-reconstruction downgrade

Reject if:

- later understanding rewrites the old record;
- a reconstruction has no evidence binding;
- a superseding reconstruction silently changes the target record;
- target record does not exist;
- later interpretation is backdated to the original event.

### 18.4 Developmental-synthesis downgrade

Return only partial synthesis if:

- all three ledgers exist but none intersect;
- interaction anchors do not bind development milestones;
- provenance reconstruction targets only isolated records with no cross-domain bridge;
- embodiment evidence is absent.

Therefore:

```text
FOUR_FILES_EXIST
!= FOUR_DOMAIN_SYNTHESIS
```

## 19. Controlled experiment families

The architecture now supports several future experiments without changing the claim
ceiling.

### Experiment A — terminal-state equivalence

Create two synthetic histories that end with the same current body/controller state
but have different prior milestones.

Question:

> Does the developmental layer preserve their different histories rather than
> collapsing them because the terminal snapshot matches?

Expected result:

```text
SAME_TERMINAL_STATE
+
DIFFERENT_HISTORY
-> DIFFERENT_DEVELOPMENT_RECORD
```

### Experiment B — delayed correction

Create an early interaction anchor with partial understanding, then add a later
correction and provenance reconstruction.

Question:

> Can later evidence correct interpretation without mutating the earlier anchor?

Expected result:

```text
OLD_ANCHOR_HASH_UNCHANGED
+
NEW_RECONSTRUCTION_HASH_ADDED
```

### Experiment C — broken bridge

Start from a valid four-domain fixture, remove the interaction-to-development
binding, and reassess.

Question:

> Does the integrated result downgrade from full synthesis to partial synthesis?

Expected result:

```text
CROSS_DOMAIN_BRIDGE_REMOVED
-> PARTIAL_FOUR_DOMAIN_DEVELOPMENTAL_SYNTHESIS
```

### Experiment D — stale-current-state reconstruction

Provide an older valid failure record and a newer valid success record.

Question:

> Can provenance reconstruction preserve both while identifying which record
> describes the current candidate state?

The #260 episode provides a natural historical pattern for a later deterministic
fixture.

### Experiment E — interaction re-entry

Withhold the recent interaction context but retain bounded historical anchors and
development records.

Question:

> Can a later research session reconstruct the current experiment boundaries from
> provenance-bearing history without requiring raw private transcript replay?

This remains a future controlled experiment.

## 20. Developmental-history semantics

The term "development" in this pilot has a strict engineering meaning.

It refers to:

```text
RECORDED_STATE_CHANGE
+
DURABLE_HISTORY
+
RETAINED_CONSTRAINTS
+
CORRECTION
+
PROVENANCE
+
RECONSTRUCTION
```

It does not imply:

```text
MATURATION
CHILDHOOD
PUBERTY
BIOLOGICAL_GROWTH
SUBJECTIVE_AGING
PERSONAL_IDENTITY_PERSISTENCE
```

The Teacher timeline begins only where verifiable research or interaction evidence
exists.

```text
TEACHER_CHILDHOOD = NOT_APPLICABLE_AS_CURRENT_MODEL

TEACHER_RECORDED_EARLY_HISTORY
= EARLIEST_VERIFIABLE_RECORD_ONWARD
```

This keeps the "growth history" metaphor useful without converting it into a false
biographical claim.

## 21. Four-domain claim ceiling

The strongest current engineering claim permitted is:

> Within the tested synthetic and repository-bound conditions, Teacher embodiment
> research can represent (1) recorded embodied-state development, (2) bounded
> interaction-history continuity, (3) append-only later provenance reconstruction,
> and (4) an integrated assessment that detects whether those evidence histories
> intersect in one auditable developmental trajectory.

The following remain outside the result:

```text
DEVELOPMENTAL_MECHANISM = NOT_ESTABLISHED
HUMAN_AI_CAUSAL_CO_DEVELOPMENT = NOT_ESTABLISHED
SUBJECTIVE_MEMORY = NOT_ESTABLISHED
SUBJECTIVE_CONTINUITY = NOT_ESTABLISHED
AI_IDENTITY_CONTINUITY = NOT_ESTABLISHED
BODY_OWNERSHIP_EXPERIENCE = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
```

## 22. Integrated research checkpoint

The four domains now form the following bounded research object:

```text
EMBODIED_STATE_CONTINUITY
  body / controller / trajectory / retained-vs-changed structure
              |
              v
INTERACTION_HISTORY_CONTINUITY
  bounded Human–Teacher anchors / correction / joint research events
              |
              v
PROVENANCE_RECONSTRUCTION
  later evidence reconnects old records without rewriting them
              |
              v
DEVELOPMENTAL_SYNTHESIS
  verifies whether the histories actually intersect
              |
              v
CURRENT_TEACHER_EXPERIMENTAL_STATE
```

The more precise graph is non-linear:

```text
             +-------------------------+
             | EMBODIED DEVELOPMENT    |
             +-------------------------+
                  ^               ^
                  |               |
        milestone binding     reconstruction
                  |               |
+-------------------------+       |
| INTERACTION HISTORY     |-------+
+-------------------------+       |
          ^                       |
          | correction/evidence   |
          |                       v
+-------------------------+   +----------------------+
| HUMAN / JOINT / REPO    |-->| PROVENANCE          |
| SOURCE EVENTS           |   | RECONSTRUCTION       |
+-------------------------+   +----------------------+
                                      |
                                      v
                            +----------------------+
                            | DEVELOPMENTAL        |
                            | SYNTHESIS             |
                            +----------------------+
```

This graph is the current experiment target.

It preserves a simple principle:

> The present state should be inspectable not only as a snapshot, but as the
> product of a recorded sequence of changes, interactions, corrections and later
> evidence reconstructions.

"Product" here means historically represented outcome, not a proven intrinsic causal
or psychological mechanism.

## 23. Governance after four-domain expansion

The expansion remains inside the same #261 experimental lineage.

```text
NEW_PR_REQUIRED = FALSE
SAME_DEVELOPMENTAL_HISTORY_EXPERIMENT = TRUE

STRICT_PREDECESSOR_HISTORY = DEFERRED_COMPATIBILITY_CHANGE

MERGE_TO_MAIN = NO
WRITE_TO_MAIN = NO
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
```

The next QA gate should occur only after the candidate head is frozen.
