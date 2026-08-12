# SALVAGE REPORT — rejected affective-motivational-dynamics candidate

## DISPOSITION

- SOURCE_CANDIDATE: `affective-motivational-dynamics_v0.1.0`
- SOURCE_STATUS: REJECTED / FAILED IQC
- SALVAGE_BRANCH: `review/affective-motivational-salvage`
- ORIGINAL_SOURCE_HISTORY: preserved only for audit/provenance on the isolated Nemotron session branch
- PROMOTION_STATUS: NONE
- MAIN_EFFECT: NONE
- CANONICAL_EFFECT: NONE
- RUNTIME_EFFECT: NONE

## WHY THE ORIGINAL CANDIDATE WAS REJECTED

The candidate was named as a dynamics module but primarily stored externally asserted summaries and manually constructed transitions. It did not compute motivational dynamics from events/outcomes. Its ablation path could leave stale summaries, could fail when the final signal domain was removed, and did not reliably trace causal changes. Human/biological construct labels and demo language were also too strong for the implemented mechanism.

The Human Research Owner classified the artifact as pollution rather than a rework candidate and authorized destructive removal from the salvage branch, while retaining only useful research primitives.

## RETAINED MATERIAL

Only the following mechanism-level ideas were retained:

1. Every signal must bind to a source event.
2. Every signal must carry evidence and provenance references.
3. Numeric signal magnitudes are bounded.
4. Approach and avoidance remain separate channels.
5. Uncertainty remains explicit.
6. Signed action bias preserves direction rather than collapsing differences into an absolute value.
7. Coactivation is represented without automatically calling it psychological conflict.
8. Signal collections enforce unique IDs and subject/context binding.
9. Empty signal collections are valid for control/ablation conditions.
10. Scientific non-claims remain locked: computational signals do not establish felt experience or motivational authority.

## REJECTED / NOT CARRIED FORWARD

The salvage deliberately does not carry forward:

- the `affective-motivational-dynamics` package identity
- `AffectiveValence`
- manually asserted `global_valence`
- manually asserted `dominant_direction`
- manually asserted `conflict_index`
- manually asserted `uncertainty_aggregate`
- the original state manager, snapshot, restore, transition and ablation implementation
- biological-sounding demo evidence such as dopamine proxy/surge labels
- fixed human-domain taxonomy such as HOMEOSTATIC, ADULT_SEXUALITY_SCHEMA and SELF_PRESERVATION
- automatic interpretation of any non-zero approach+avoidance pair as psychological conflict
- claims that wanting/liking discrepancy or other psychological constructs have been operationally validated

Potentially useful psychological constructs such as wanting-versus-expected-liking remain research questions, not implemented primitives.

## NEW MINIMAL ARTIFACT

`motivational-signal-primitives_v0.1.0` is intentionally small. It is not a dynamics model and contains no lifecycle manager.

It provides:

- `MotivationalSignalPrimitive`
- `MotivationalSignalSet`
- evidence/provenance binding
- subject/context binding
- signed action bias
- non-interpretive coactivation
- deterministic aggregation from current signals

## VERIFICATION

Independent local verification outside the Nemotron session:

```text
9 passed in 0.04s
```

GitHub CI was not executed.

## SCIENTIFIC NON-CLAIMS

This salvage does not establish affect, feeling, desire, volition, hedonic tone, self-preservation drive, or motivational authority. It is a bounded computational primitive for later experiments only.
