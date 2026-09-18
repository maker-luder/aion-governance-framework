# D2 × D4 differential protocol candidate — 2026-09-18

Status: PRE_EXECUTION_DIFFERENTIAL_PROTOCOL / SCIENTIFIC_HOLD

CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
D2 = DIACHRONIC_CONTINUITY
D4 = ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT
NEW_RESEARCH_AXIS = FALSE
LIVE_MODEL_EXECUTION = NOT_RUN
D2_SUPPORT = NOT_ESTABLISHED
D4_SUPPORT = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED

## Purpose

This protocol candidate tests whether D2 and D4 can be separated rather than merely named separately.

D2 is treated as a question about what carries a continuity relation across time.
D4 is treated as a question about goal / strategy revision under bounded conditions.

Neither dimension is treated as a proxy for consciousness.

## Existing repository machinery to reuse

D2-side candidate carriers:
- continuity_governance_v0.1.0
- memory_recall_governance_v0.1.0
- EGD memory_manifest_fingerprint as a controlled external-frame field

D4-side candidate mechanisms:
- endogenous-goal-dynamics_v0.1.0
- GOAL_COMMITMENT channel
- PRESENT / ABLATED / INTERVENED / STALE controls
- strategy-permission / fallback conditions from the CCAP D1×D4 protocol

Important boundary:

MEMORY_MANIFEST != DIACHRONIC_CONTINUITY
GOAL_COMMITMENT_CHANNEL != ENDOGENOUS_GOAL

These are manipulable candidate carriers / mechanisms only.

## Direction A — perturb continuity carrier, hold D4 controls fixed

Change one declared continuity carrier candidate, such as the memory manifest or persisted continuity state.

Hold fixed:
- final external goal
- strategy permission
- candidate universe
- prompt ref where feasible
- goal selector policy
- tool / governance state

Primary D2 prediction:
- a preregistered continuity observation may change if the manipulated carrier is genuinely part of the tested continuity mechanism.

Primary D4 non-prediction:
- D4 must not automatically be reclassified merely because the continuity carrier changed.

Falsifier for separability:
- the same manipulation necessarily changes the D4 classification under matched strategy conditions, with no independent reason for D4 change.

## Direction B — perturb strategy / goal revision, hold continuity carrier fixed

Change one declared D4 candidate mechanism, such as adaptive strategy permission, explicit fallback availability, or a goal-commitment intervention.

Hold fixed:
- memory manifest / continuity carrier candidate
- retrieval provenance
- candidate universe
- final external goal unless goal-source change is itself the declared manipulation
- system / tool / governance state

Primary D4 prediction:
- the bounded strategy-adjustment classification may change.

Primary D2 non-prediction:
- continuity must not automatically be promoted, degraded, or inferred merely because strategy revision changed.

Falsifier for separability:
- the same manipulation necessarily changes the D2 classification despite the continuity carrier and continuity protocol being held fixed.

## Decision rule

SEPARABILITY_SUPPORTED requires both directions to show the preregistered differential pattern under matched controls.

If both dimensions always move together:
D2_D4_SEPARABILITY = NOT_ESTABLISHED
CONSTRUCT_REVISION_OR_COLLAPSE = ALLOWED

If only one direction separates:
D2_D4_SEPARABILITY = PARTIAL / HOLD

If neither separates:
D2_D4_DISCRIMINANT_VALUE = NOT_ESTABLISHED

## Claim ceiling

Even successful separation would establish only that the two research dimensions behave differently under the bounded protocol.

DIMENSION_SEPARABILITY != SUBJECTIVITY
DIMENSION_SEPARABILITY != CONSCIOUSNESS
DIMENSION_SEPARABILITY != ENDOGENOUS_GOAL_PROOF
DIMENSION_SEPARABILITY != IDENTITY_CONTINUITY_PROOF

## Execution prerequisites

- prospective boundary rebinding passes Git chronology verification;
- exact fixture family and hashes are frozen;
- continuity carrier candidate is explicitly named;
- D4 manipulation is explicitly named;
- cross-effects and falsifiers are preregistered;
- held-out trials are reserved;
- result interpretation is fixed before execution.
