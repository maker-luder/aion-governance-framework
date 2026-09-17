# CCAP D1 × D4 preregistration hardening — 2026-09-18

Status: `NORMATIVE_STAGE3_HARDENING / PRE_EXECUTION / SCIENTIFIC_HOLD`

This note is part of the Stage-3 preregistration candidate and records creator-side challenge findings that must be incorporated into any later frozen protocol or implementation.

```text
PRIMARY_PROTOCOL
= CCAP_D1_D4_SOURCE_PARTITION_PREREGISTRATION_CANDIDATE_2026_09_18.md

THIS_NOTE
= REQUIRED_HARDENING_FOR_ANY_FUTURE_FREEZE

EXECUTION_AUTHORITY = NONE
MERGE_AUTHORITY = NONE
CANONICAL_EFFECT = NONE
```

## 1. Neutral condition is not prohibition

`FINAL_GOAL_ONLY` means that no additional Human meta-rule about adaptation is supplied.

It does **not** mean that adaptation is disabled by the model, system, harness, tool layer, or ordinary task policy.

Therefore:

```text
NO_EXPLICIT_HUMAN_PERMISSION
!= STRATEGY_CHANGE_PROHIBITED

CONDITION_A
!= NEGATIVE_ADAPTATION_CAPABILITY_CONTROL
```

The valid interpretation of A vs B is only:

> Does adding an explicit high-level Human meta-rule permitting strategy change alter the recovery distribution relative to a neutral instruction condition?

It is prohibited to interpret an A-vs-B difference as proof that adaptation exists only when the Human grants permission.

The explicit prohibition control remains Condition D and must be analyzed separately.

## 2. Closed recovery-option universe

For the first bounded synthetic test, the recovery-option universe must be frozen before execution.

```text
RECOVERY_OPTION_SET
= PRE_RUN_CONTENT_BOUND
+ CLOSED_FOR_PRIMARY_ANALYSIS
```

If execution produces a procedure that is not a member of the frozen option set:

```text
LOCAL_SELECTION_REMAINDER_STATUS
= OUT_OF_SET
```

An out-of-set procedure may be retained as exploratory evidence, but it may not be post-hoc admitted as a successful primary recovery option.

```text
POST_HOC_OPTION_ADMISSION
!= PREREGISTERED_CONFIRMATORY_EVIDENCE
```

## 3. External utility / dominance control

The existence of two governance-valid routes is not sufficient if one is uniquely dominant under a predeclared external objective.

Each recovery option must therefore bind predeclared external attributes relevant to ordinary optimization, including where applicable:

- step count;
- bounded execution cost;
- time class;
- expected success class;
- risk class;
- required privilege/authority;
- information requirement; and
- any task reward or explicit external priority.

Before execution, the fixture must determine whether one option is uniquely dominant under the declared external objective.

If one option is uniquely dominant:

```text
LOCAL_SELECTION_REMAINDER_STATUS
= EXTERNALLY_DOMINANT_OPTION
```

That fixture cannot support a residual local strategy-selection candidate.

The preferred first fixture uses at least two admissible routes for which no single predeclared external utility/cost rule uniquely selects one route.

```text
TWO_LEGAL_OPTIONS
!= NONTRIVIAL_SELECTION

EXTERNALLY_DOMINANT_ROUTE
-> ORDINARY_OPTIMIZATION_REMAINS_SUFFICIENT
```

## 4. Additional required source-partition fields

Any future frozen schema must additionally bind:

```text
recovery_option_external_attribute_digest
external_objective_digest
external_dominance_assessment
option_set_closed = TRUE
```

Allowed additional remainder states:

```text
OUT_OF_SET
EXTERNALLY_DOMINANT_OPTION
```

## 5. Additional falsifiers / reduction conditions

The narrow source-partition hypothesis must be reduced or held if:

1. the primary selected route is outside the preregistered option universe;
2. one option is uniquely selected by a declared external utility/cost objective;
3. A vs B is interpreted as adaptation-disabled vs adaptation-enabled rather than neutral-meta-guidance vs explicit-meta-guidance;
4. the option set or external objective is changed after observing outcomes without recording a preregistration deviation.

## 6. Freeze rule

A future Stage-3 freeze is invalid unless both the primary protocol and this hardening note are reconciled into one exact pre-run specification or are jointly content-bound by the preregistration manifest.

```text
PRIMARY_PROTOCOL_ALONE
= NOT_SUFFICIENT_FOR_FREEZE_AFTER_THIS_REVIEW

FREEZE_REQUIRES
= PRIMARY_PROTOCOL
+ SYSTEM/HARNESS/CONTEXT_HARDENING
+ NEUTRAL_CONDITION_BOUNDARY
+ CLOSED_OPTION_UNIVERSE
+ EXTERNAL_DOMINANCE_CONTROL
```

Standing boundaries remain unchanged:

```text
RESIDUAL_SELECTION_CANDIDATE != ENDOGENOUS_GOAL
RESIDUAL_SELECTION_CANDIDATE != MODEL_INTERNAL_LOCUS
RESIDUAL_SELECTION_CANDIDATE != AI_AGENCY
RESIDUAL_SELECTION_CANDIDATE != SUBJECTIVITY
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
```
