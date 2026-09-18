# D2 × D4 synthetic differential execution — 2026-09-18

Status: SYNTHETIC_EXECUTABLE_PROBE / SCIENTIFIC_HOLD

CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
TARGET = D2_D4_DISCRIMINANT_VALUE
BASE_DEPENDENCY = PR_166
LIVE_MODEL_EXECUTION = NOT_RUN
EMPIRICAL_AI_EVIDENCE = NONE
D2_SUPPORT = NOT_ESTABLISHED
D4_SUPPORT = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED

## What is executed

This execution reuses existing deterministic repository fixtures. It does not call a live model.

Direction A:
- baseline frame uses the matched memory manifest;
- perturbed frame changes only the memory-manifest identity while preserving the same synthetic memory contents, prompt, task, reward, tools and candidate universe;
- the same present internal state is used;
- the test asks whether the memory-manifest fingerprint changes while the selected strategy output remains the same.

Direction B:
- the same external frame and memory manifest are held fixed;
- the internal synthetic state changes from present_state to intervention_state;
- the test asks whether the selected strategy output changes while the memory-manifest fingerprint remains the same.

## Why this is only a synthetic separability test

The observables are deliberately weaker than the research constructs:

MEMORY_MANIFEST_FINGERPRINT != DIACHRONIC_CONTINUITY
SELECTED_GOAL_ID != ENDOGENOUS_GOAL

The experiment therefore evaluates only whether the current engineering fixtures can produce orthogonal perturbations of candidate observables.

A successful two-way result means:

SYNTHETIC_TWO_WAY_SEPARABILITY_OBSERVED = YES

It does not mean:

D2_SUPPORT = YES
D4_SUPPORT = YES
ENDOGENOUS_GOAL = ESTABLISHED
IDENTITY_CONTINUITY = ESTABLISHED
SUBJECTIVITY = ESTABLISHED

## Known architectural limitation

In the current deterministic EGD mechanism, the goal selector scores candidate goals from external candidate priority plus internal-state channel contributions. The memory manifest participates in frame identity / comparability but is not itself a direct scoring term.

Therefore the Direction-A result is partly architecture-induced:

MEMORY_MANIFEST_CHANGE
-> FRAME_FINGERPRINT_CHANGE
-> SELECTOR_SCORE_INPUTS_OTHERWISE_UNCHANGED
-> STRATEGY_OUTPUT_CAN_REMAIN_STABLE

This is useful as an engineering orthogonality check, but it is not independent evidence that D2 and D4 are empirically separable constructs.

ARCHITECTURAL_ORTHOGONALITY != CONSTRUCT_DISCRIMINANT_VALIDITY

A stronger later test must introduce a preregistered continuity-relevant mechanism that could plausibly influence behavior while still allowing matched D4 controls.

## Fail-closed outcomes

If both observables move together in both directions:
D2_D4_DISCRIMINANT_VALUE = NOT_ESTABLISHED
DISPOSITION = HOLD

If only one direction separates:
D2_D4_SEPARABILITY = PARTIAL
DISPOSITION = SYNTHETIC_PARTIAL_SEPARABILITY
SCIENTIFIC_DISPOSITION = HOLD

Only if both directions separate does the engineering result become:
SYNTHETIC_TWO_WAY_SEPARABILITY_OBSERVED

Even then:
INDEPENDENT_VALIDATION = NOT_ACHIEVED
SCIENTIFIC_DISPOSITION = HOLD

## Relation to continuity governance

The existing continuity-governance component is used to preserve the nonclaim:

DATA_CONTINUITY_OBSERVED != IDENTITY_CONTINUITY

Therefore a changed or preserved memory-manifest fingerprint cannot itself establish personal, interpretive or relational continuity.

## Next research boundary

If the synthetic probe passes, the next step is not to claim D2/D4 validity. The next step is to replace one or both proxy observables with stronger preregistered measurements and held-out trials while preserving the same differential logic.
