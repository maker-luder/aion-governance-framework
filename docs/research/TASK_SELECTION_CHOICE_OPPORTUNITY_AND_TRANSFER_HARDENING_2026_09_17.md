# Task-selection choice-opportunity and transfer hardening — 2026-09-17

Status: `POST_MERGE_HARDENING / BOUNDED_IMPLEMENTATION / SCIENTIFIC_HOLD`

Canonical effect: `NONE`

Deployment: `FALSE`

```text
CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
PRIMARY_RELATED_LINE = HUMAN_AI_LEARNING_AND_INTERACTION
HARDENS = PR139_MERGED_TASK_SELECTION_HARNESS
NEW_RESEARCH_AXIS = FALSE
MODEL_EXPERIMENT = NOT_RUN
HUMAN_SUBJECT_EXPERIMENT = NOT_RUN
EMPIRICAL_DATA_COLLECTED = FALSE
```

## 1. Origin and authority

This hardening originates from ChatGPT Teacher's strict post-merge review of PR #139.
The Human Owner then instructed ChatGPT Teacher to implement the identified gaps.

```text
ORIGIN_OF_POST_MERGE_GAP_FINDINGS = CHATGPT_TEACHER_REVIEW
HUMAN_OWNER_SCOPE_APPROVAL = IMPLEMENT_HARDENING
HUMAN_OWNER_SCOPE_APPROVAL != MERGE_AUTHORITY
IMPLEMENTATION_EXISTS != SCIENTIFIC_VALIDATION
```

No prior approval to merge PR #139 is inherited by this new candidate.

## 2. Why PR #139 remains valid but incomplete

PR #139 corrected the six blocking defects inherited from the closed PR #136 candidate.
Its merged structural contract remains useful and does not require rollback.

The post-merge review nevertheless identified three deeper specification gaps:

1. `FREE_SELECTION` had a realized choice trace but no event-level binding of which alternatives were actually available;
2. distinct execution records were represented by requiring content digests to differ, which conflated record identity with record content;
3. held-out transfer was payload-level within the same family, not a separate cross-family challenge.

These are hardening gaps, not evidence that PR #139's bounded `SCIENTIFIC_HOLD` claims were false.

## 3. Choice opportunity sets

The hardened contract adds an explicit event-level choice opportunity record.
For every `FREE_SELECTION` event:

```text
CHOICE_OPPORTUNITY_EVENT
├─ EVENT_INDEX
├─ >= 2 SIGNATURE-DISTINCT AVAILABLE ALTERNATIVES
├─ >= 2 PAYLOAD-CONTENT-DISTINCT ALTERNATIVES
├─ CANONICALLY BOUND OPPORTUNITY RECORD
└─ REALIZED CHOICE MUST BELONG TO AVAILABLE ALTERNATIVES
```

Each alternative binds:

```text
TASK_DOMAIN
TASK_FAMILY_ARTIFACT
EXPOSURE_PAYLOAD_ARTIFACT
```

The opportunity record is not an arbitrary attached artifact. Its UTF-8 content is canonically rendered from the event index and ordered option signatures:

```text
CHOICE_OPPORTUNITY_V1
EVENT_INDEX=...
OPTION_COUNT=...
OPTION[0].TASK_DOMAIN=...
OPTION[0].TASK_FAMILY_SHA256=...
OPTION[0].EXPOSURE_PAYLOAD_SHA256=...
...
```

`BoundArtifact` then recomputes the SHA-256 of that canonical content. Re-labeling the same payload under a different domain or family cannot manufacture a second content-distinct choice because exposure-payload digests must also be unique inside an opportunity set.

This fixes a specific construct-validity gap:

```text
REALIZED_CHOICE_TRACE_PRESENT
!=
CHOICE_OPPORTUNITY_OPERATIONALIZED
```

The hardened structural audit can establish that the synthetic record represents multiple bound alternatives and that the selected alternative is one of them. It still cannot establish that a Human genuinely perceived the alternatives as viable, that the opportunity was temporally recorded before selection, or that choice was free in a philosophical or psychological sense.

The opportunity record also remains synthetic-only and fails closed if it declares model invocation, Human observation, Human identity or private material.

```text
CHOICE_SET_BOUND != SUBJECTIVE_FREEDOM_PROVEN
CHOICE_SET_BOUND != TEMPORAL_PROVENANCE_ESTABLISHED
CHOICE_SET_BOUND != RANDOMIZATION
CANONICAL_CHOICE_RECORD != REAL_WORLD_AVAILABILITY_PROVEN
```

## 4. External methodology cross-check

Hackländer, Schlüter & Abel (2024; online 2023), *Drinking the waters of Lethe: Bringing voluntary choice into the study of voluntary forgetting*, Memory & Cognition 52, 254–270, DOI `10.3758/s13421-023-01467-7`.

Relevant methodological feature: participants in the free-choice condition were given explicit alternatives for each trial, while the yoked forced-choice participant received the same target sequence and the corresponding realized cue sequence.

This supports the need to distinguish:

```text
AVAILABLE_OPTIONS
FROM
REALIZED_CHOICE
FROM
YOKED_ASSIGNMENT
```

It does not validate the Human–AI task-selection hypothesis.

Choice-experiment methodology likewise treats a choice task as presenting a bounded set of alternatives rather than inferring availability solely from the chosen outcome. See, for example, Georgiou et al. (2023), *Discrete choice experiments: An overview on constructing D-optimal and near-optimal choice sets*, Heliyon 9(8), e18256, DOI `10.1016/j.heliyon.2023.e18256`.

```text
METHOD_PRECEDENT != PRESENT_HYPOTHESIS_VALIDATION
```

## 5. Execution identity is not content inequality

PR #139's base auditor required every execution record to have a distinct SHA-256 digest. That was conservative but semantically over-strong.

Two independently identified executions may legitimately serialize to identical content. The hardened auditor therefore separates identity from content:

```text
EXECUTION_ID = UNIQUE
EXECUTION_RECORD_ARTIFACT_ID = UNIQUE_AND_BOUND_TO_UNIT
EXECUTION_RECORD_CONTENT_DIGEST = MAY_REPEAT
```

Therefore:

```text
SEPARATE_EXECUTION_IDENTITY
!=
EXECUTION_CONTENT_MUST_DIFFER
```

The original PR #139 auditor is retained for historical/API compatibility. Future use of this hardening should prefer the hardened audit path when execution identity semantics matter.

## 6. Two levels of held-out challenge

The hardened contract requires two held-out records per task domain:

```text
A. WITHIN_FAMILY_PAYLOAD_HOLDOUT
   SAME EXPOSED FAMILY WHEN THE DOMAIN WAS EXPOSED
   + NEW PAYLOAD

B. CROSS_FAMILY_CHALLENGE
   SAME DOMAIN
   + FAMILY ABSENT FROM ALL EXPOSURE EVENTS
   + NEW PAYLOAD
```

For a domain with zero exposure, the two held-out records must still bind two distinct task families so that the schema does not silently collapse the two challenge levels. In that zero-exposure case, however, neither record is evidence of transfer or generalization from prior exposure because no exposure exists for that domain.

The cross-family family bindings must be absent from all exposure-family bindings and unique by domain.

This creates a stronger structural challenge but still does not establish transfer:

```text
WITHIN_FAMILY_NEW_PAYLOAD != HUMAN_TRANSFER_ESTABLISHED
CROSS_FAMILY_HELD_OUT_TASK != DOMAIN_GENERALIZATION_ESTABLISHED
ZERO_EXPOSURE_DOMAIN + TWO_HELD_OUT_FAMILIES != TRANSFER_TEST
FAMILY_LEVEL_CHALLENGE_PRESENT != LEARNING_ESTABLISHED
```

For this reason the audit field is named `cross_family_challenge_bound`, not `cross_family_domain_generalization_bound`.

## 7. Relationship to the PR #139 auditor

The merged PR #139 function remains:

`audit_task_selection_exposure_design`

The additive hardened function is:

`audit_task_selection_exposure_design_hardened`

The hardened function independently re-checks the core pair/control/protocol/yoking requirements rather than calling the earlier auditor, because the earlier auditor intentionally rejects identical execution-record content digests.

This preserves historical behavior while allowing the corrected identity semantics.

```text
OLD_AUDITOR_RETAINED = TRUE
HARDENED_AUDITOR_ADDITIVE = TRUE
HISTORICAL_API_REWRITE = FALSE
```

## 8. Test requirements

The hardened test surface must cover at least:

- one opportunity trace for every free-selection unit;
- at least two signature-distinct alternatives per opportunity;
- distinct exposure-payload content per alternative;
- canonical event/options binding in the opportunity record;
- privacy and empirical-observation fail-closed boundaries for opportunity records;
- realized choice membership in the opportunity set;
- exact pair-level yoked sequence matching;
- valid free-selection null outcomes;
- same-content execution records with distinct execution identities;
- duplicate execution identity rejection;
- within-family held-out family matching when the domain was exposed;
- cross-family family absence from exposure;
- zero-exposure-domain family separation without a transfer claim;
- held-out payload separation from exposure and from each other;
- continued scientific `HOLD` boundaries.

## 9. Claim ceiling

This hardening improves structural construct representation only.

```text
CHOICE_OPPORTUNITY_SET_BOUND != HUMAN_AUTONOMY_ESTABLISHED
TRUE_YOKED_SEQUENCE != EXCHANGEABILITY_ESTABLISHED
EXECUTION_IDENTITY_BOUND != INDEPENDENT_EXECUTION_PROVEN_IN_REAL_WORLD
CROSS_FAMILY_HOLDOUT_BOUND != TRANSFER_EFFECT_ESTABLISHED
STRUCTURAL_QA_PASS != EMPIRICAL_RESULT
CI_PASS != SCIENTIFIC_VALIDATION
HUMAN_LEARNING = NOT_ESTABLISHED
CAUSAL_EFFECT = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
