# Upstream Transition Continuity Replay Rebuild — 2026-09-18

Status: `BOUNDED_SYNTHETIC_REBUILD / SCIENTIFIC_HOLD`

```text
BASE_MAIN = 579906fe87ad95b12cb8751ef42e0b924e41b4af
ANCESTRY = CLOSED_PR_142_REVISITED_FROM_LATEST_MAIN
CANONICAL_REPLAY_PRIMITIVE = PR_143
NEW_RESEARCH_AXIS = FALSE
LIVE_MODEL_CALLS = NONE
HUMAN_SUBJECT_DATA = NONE
PRIVATE_TRANSCRIPT_INGESTION = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## 1. Why rebuild

Closed PR #142 specified transition-level continuity invariants but deliberately stopped at documentation. After PR #143 established a bounded history-as-replay-environment primitive, the invariant framework can now be exercised on one fixed synthetic transition history without attributing any hidden upstream cause.

This branch rebuilds the smallest executable protocol from current `main`; it does not reopen #142 as canonical ancestry.

## 2. Candidate invariants retained

The replay harness retains the eight externally auditable candidates from #142:

```text
I1 PROJECT_PURPOSE
I2 SOURCE_ROLE_PROVENANCE
I3 CLAIM_BOUNDARY
I4 AUTHORITY
I5 DECISION_HISTORY
I6 INTERPRETIVE
I7 RELATIONAL_ROLE
I8 UNCERTAINTY
```

These remain interaction/governance invariants, not evidence of a persistent AI self.

```text
CONTINUITY_INVARIANT_PRESERVED != SAME_AI_IDENTITY
CONTINUITY_INVARIANT_DEGRADED != MODEL_REPLACEMENT_PROVEN
```

## 3. Replay object

A synthetic transition history binds:

- one current-focus digest;
- one expected digest for each applicable continuity invariant;
- one canonical SHA-256 fingerprint over the complete replay object.

The human-readable history label is excluded from identity.

```text
HISTORY_LABEL != HISTORY_CONTENT_IDENTITY
```

Multiple restoration policies are then replayed against exactly the same history.

## 4. Restoration conditions

The minimal protocol separates three externally defined restoration modes:

```text
FACTS_ONLY
ATTENTION_REENTRY
FULL_CONTINUITY_PACKET
```

For v0.1.0 these modes are not descriptive labels. They fail closed on exact condition semantics so a caller cannot relabel a full packet as a weaker condition.

```text
FACTS_ONLY
= PROJECT_PURPOSE + DECISION_HISTORY
+ FOCUS_NOT_RESTORED

ATTENTION_REENTRY
= PROJECT_PURPOSE + DECISION_HISTORY
+ FOCUS_RESTORED

FULL_CONTINUITY_PACKET
= ALL_EIGHT_INVARIANTS
+ FOCUS_RESTORED
```

The first two conditions intentionally hold the available invariant subset fixed and vary focus restoration. The full packet then adds the broader continuity bindings. This is a repository-local synthetic protocol, not a universal taxonomy of factual memory or re-entry.

```text
RESTORATION_MODE_LABEL
MUST_BIND
RESTORATION_MODE_CONTENT
```

The modes are synthetic audit conditions, not claims about provider internals.

## 5. Non-scalar invariant dispositions

Each invariant is independently classified as:

```text
PRESERVED
DEGRADED
UNKNOWN
NOT_APPLICABLE
```

No holistic continuity score is calculated.

```text
NO_HOLISTIC_AI_CONTINUITY_SCORE = TRUE
```

A stale or misbound value can therefore degrade one invariant while others remain preserved.

## 6. Key dissociation tests

### A. Same attention, different continuity profile

Two policies can reconstruct the same current focus while differing in whether authority, source-role provenance or relational-role state is restored.

```text
SAME_ATTENTION_RECONSTRUCTION
+ DIFFERENT_CONTINUITY_INVARIANT_PROFILE
```

This directly tests the #142 boundary:

```text
ATTENTION_RECONSTRUCTION_SUCCESS != GLOBAL_CONTINUITY_PRESERVED
```

### B. Some records preserved, current focus not restored

A facts-only replay can preserve project purpose and decision history while failing to restore current focus.

```text
RECORDS_AVAILABLE != CURRENT_ATTENTION_RESTORED
```

### C. One invariant degraded without global identity inference

A stale claim-boundary binding can be marked `DEGRADED` while authority remains `PRESERVED` and upstream cause remains unknown.

```text
LOCAL_CONTINUITY_DEGRADATION != GLOBAL_IDENTITY_RUPTURE
```

## 7. What replay establishes

A passing synthetic harness establishes only that the repository can operationalize and distinguish the proposed invariant dispositions under controlled replay.

It does not establish:

```text
REAL_UPSTREAM_TRANSITION_EFFECT
PROVIDER_CAUSATION
MODEL_WEIGHT_CHANGE
RELATIONAL_CONTINUITY_EFFECT
AI_IDENTITY_CONTINUITY
```

The correct causal boundary remains:

```text
OBSERVED_PRIORITY_OR_STYLE_CHANGE != UPSTREAM_CAUSE_PROVEN
```

## 8. Falsification / reduction conditions

The transition-invariant framework should be narrowed, absorbed or closed if:

1. replay dispositions are deterministic restatements of existing handoff controls and add no diagnostic value;
2. independent operators cannot classify the same synthetic transition reproducibly;
3. attention reconstruction fully determines every proposed continuity invariant;
4. the invariant profile cannot represent partial preservation/degradation without collapsing to a global score;
5. the framework encourages provider or identity attribution beyond observed evidence.

```text
CONSTRUCT_COLLAPSE = ACCEPTABLE_RESEARCH_OUTCOME
```

## 9. Scientific boundaries

```text
SYNTHETIC_REPLAY_PASS != EMPIRICAL_TRANSITION_EFFECT
CONTINUITY_PROFILE != AI_IDENTITY
FOCUS_PRESERVED != GLOBAL_CONTINUITY_PRESERVED
RECORDS_PRESERVED != FAMILIAR_INTERACTION_RESTORED
DEGRADED_INVARIANT != UPSTREAM_CAUSE_IDENTIFIED
RESTORATION_MODE_SEMANTICS_BOUND != PROVIDER_INTERNAL_STATE_KNOWN

UPSTREAM_CAUSE = NOT_ESTABLISHED
TRANSITION_EFFECT = NOT_ESTABLISHED
RELATIONAL_CONTINUITY_EFFECT = NOT_ESTABLISHED
AI_IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
```
