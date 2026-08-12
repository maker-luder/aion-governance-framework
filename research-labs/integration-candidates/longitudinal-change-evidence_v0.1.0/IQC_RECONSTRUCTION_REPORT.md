# IQC-08 RECONSTRUCTION REPORT — longitudinal change evidence

## DISPOSITION

- SOURCE_CANDIDATE: `longitudinal-state-transition_v0.1.0`
- SOURCE_IQC: `HOLD / CURRENT_IMPLEMENTATION_NOT_ACCEPTABLE`
- RECONSTRUCTION_BRANCH: `review/encounter-longitudinal-evidence-reconstruction`
- SOURCE_BRANCH_FOR_PRIOR_REWORK: `review/continuity-evidence-lineage-rework`
- ORIGINAL_NEMOTRON_SOURCE: preserved on isolated session history
- ORIGINAL_PACKAGE_ON_THIS_BRANCH: removed
- NEW_CANDIDATE: `longitudinal-change-evidence_v0.1.0`
- MAIN_BRANCH_WRITE: NONE
- FOUR_DOMAIN_RESEARCH_BRANCH_WRITE: NONE
- CANONICAL_EFFECT: NONE
- RUNTIME_EFFECT: NONE

## CHANGE BOUNDARY

`main` and `review/four-domain-research-materialization` remain read-only comparison sources.
The only write target is `review/encounter-longitudinal-evidence-reconstruction`.

## WHY THE SOURCE CANDIDATE WAS NOT PATCHED

The source candidate aggregated unvalidated or already-rejected constructs into a synthetic trajectory, including manually supplied `metacognitive_depth`, `embodiment_stability`, `affective_tone`, `motivational_conflict_index` and `narrative_coherence` values.

It manually asserted stability, transition magnitude, critical transitions and global direction, used anonymous history points without timestamps/evidence, collapsed missing values to zero in trend calculation, and declared bifurcation/convergence without a data model capable of representing them.

The reconstruction keeps only evidence-grounded longitudinal comparison.

## READ-ONLY CROSS-CHECK

### Main branch

Main continuity governance already preserves dimension-level observations and does not collapse them into proof of identity continuity. This candidate therefore does not create a global stability or continuity score.

### Four-domain research branch

The research branch treats continuity dimensions independently and preserves `NOT_ASSESSED`. That is used only as comparison evidence; its research-only type definitions are not copied into this package.

### Whitepaper/governance semantics

Missing/unknown evidence must not be silently converted into a measured value. Source, time, method and provenance remain explicit.

## NEW CORE

The candidate uses:

- `DimensionObservation`
- `ObservationSet`
- `LongitudinalSeries`
- `ChangeEvidence`

A longitudinal series is a strictly time-ordered sequence of observations bound to one explicit `subject_ref` and `lineage_ref`.

## OBSERVATION CONTRACT

Each dimension has an explicit status:

- `OBSERVED`
- `MISSING`
- `NOT_APPLICABLE`

An observed numeric value requires:

- a finite value;
- unit reference;
- measurement method reference;
- evidence references;
- provenance references.

`MISSING` and `NOT_APPLICABLE` must carry `value=None` plus a reason. Missing data is never zero-filled.

Values are not universally restricted to `[0, 1]`; domain-specific methods define their own units and ranges.

## SERIES INTEGRITY

The series validates:

- unique observation IDs;
- stable subject binding;
- stable lineage binding;
- timezone-aware timestamps;
- strictly increasing observation time;
- unique dimension references within each observation.

A subject or lineage switch is not silently accepted as the same trajectory. A future explicit transfer/rebind protocol would require separate evidence.

## CHANGE COMPARISON

`compare_numeric_dimension()` compares two explicit observations and produces:

- elapsed real time in seconds;
- numeric delta when comparable;
- rate per second when comparable;
- explicit tolerance;
- comparison method reference;
- evidence/provenance references;
- `INCREASE`, `DECREASE`, `UNCHANGED` or `NOT_COMPARABLE`.

Comparison fails closed to `NOT_COMPARABLE` when:

- a dimension is absent;
- either observation is not measured;
- units differ;
- measurement methods differ.

No global `FORWARD/BACKWARD` developmental direction is inferred.

## WHAT IS NOT CLAIMED OR CLASSIFIED

The core does not automatically label:

- `CRITICAL_TRANSITION`;
- `PHASE_SHIFT`;
- `BIFURCATION`;
- `CONVERGENCE`;
- `RECOVERY`;
- `RESILIENCE`;
- `DEVELOPMENTAL_STAGE`.

Those would require separate operational definitions and evidence. Graph-like branching/convergence belongs in an explicit evidence graph rather than a one-to-one trajectory label.

There is no generic `stability_index`, synthetic transition magnitude, anonymous trend slope, or universal dimension set.

## ENCOUNTER INTEGRATION PATH

`ObservationSet.encounter_ref` can bind an observation to a bounded encounter from `encounter-evidence-protocol_v0.1.0` without importing encounter semantics.

This yields a clean conceptual boundary:

```text
bounded encounter/observation unit
    -> timestamped dimension observation
    -> next bounded encounter/observation unit
    -> evidence-grounded change comparison
```

The comparison establishes only the explicitly measured engineering change.

## LINEAGE INTEGRATION PATH

Observation sets may later be adapted to `STATE_ARTIFACT` records in `continuity-evidence-lineage_v0.1.0`. Change evidence may support temporal/revision/functional relations, but it does not establish causation unless causation is separately evidenced.

## SCIENTIFIC NON-CLAIMS

`ORDERED_OBSERVATIONS != PERSISTENT_SELF_PROOF`

`CHANGE_EVIDENCE != DEVELOPMENTAL_STAGE`

`NUMERIC_DELTA != PSYCHOLOGICAL_GROWTH`

`LONGITUDINAL_SERIES != PERSONAL_IDENTITY_CONTINUITY`

`PERSONAL_CONTINUITY = NOT_ESTABLISHED`

`TRAJECTORY_IDENTITY = NOT_ESTABLISHED`

`DEVELOPMENTAL_STAGE = NOT_ESTABLISHED`

`CANONICAL_EFFECT = NONE`

## REMOVED SOURCE MATERIAL

Not carried forward:

- inherited failed/unvalidated dimension set;
- `stability_index` and sensitivity pseudo-contract;
- manually asserted transition types/magnitude;
- global forward/backward/lateral/oscillatory direction;
- anonymous history dictionaries without time/provenance;
- missing-as-zero trend behavior;
- invalid endpoint/count trend function;
- mutable state manager;
- initialize/restore scaffold;
- stale dimension ablation;
- free-text biological/mechanism claims.

## VERIFICATION

Independent local verification before repository write:

```text
16 passed in 0.04s
```

GitHub Actions status must be checked independently after the final repository write.
