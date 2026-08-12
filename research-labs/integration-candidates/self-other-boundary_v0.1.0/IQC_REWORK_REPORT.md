# IQC REWORK REPORT — self-other-boundary v0.1.1

## STATUS

- ORIGINAL_ARTIFACT_SOURCE: Nemotron Cloud Agent session branch
- ORIGINAL_ARTIFACT_STATUS: preserved on `session/agent_99a9dfc9-f4f4-432c-a918-f97527f129bc`
- REWORK_BRANCH: `review/self-other-boundary-rework`
- DISPOSITION: ENGINEERING_REWORK_VERIFIED / RESEARCH_CAPABILITY_HOLD
- MAIN_EFFECT: NONE
- CANONICAL_EFFECT: NONE
- RUNTIME_EFFECT: NONE

## PROVENANCE AND REVIEW CALIBRATION

- Human Research Owner authorized second-module IQC processing.
- During review, the Human Research Owner rejected two proposed hard constraints: (1) that SELF must never equal an OTHER-model entity, and (2) that `subject_ref` must never change.
- Re-review converted both into narrower design rules: identity and representational role must be explicit, and subject changes may occur only through explicit, traceable transition semantics.
- ChatGPT Research Architect performed source review, defect analysis, rework design, code changes, and independent local verification.
- Nemotron remains the source of the original candidate implementation and is not attributed the rework changes below.

## REVISED IQC FINDINGS

1. `SOB-001` — Identity/role semantics were underspecified. A modeled entity may validly represent an external other, observed self, past self, counterfactual self, or an unresolved relation. Hard SELF/OTHER inequality was rejected.
2. `SOB-002` — Duplicate models with the same `(other_id, relation_to_subject)` were not prevented, creating ambiguous authority.
3. `SOB-003` — Subject changes were untyped and untraced. Hard subject immutability was rejected; silent subject changes remain invalid.
4. `SOB-004` — Restore transitions used a sentinel source id rather than the real source state and did not make cross-subject restoration explicit.
5. `SOB-005` — `frozen=True` did not protect the mutable `distinction_weights` dictionary from in-place mutation, weakening snapshot integrity.
6. `SOB-006` — Individual distinction weights were not bounded even when their total summed to 1.0.
7. `SOB-007` — Final-distinction ablation could construct an invalid empty configuration.
8. `SOB-008` — Distinction ablation changed state without an explicit transition; invalid distinction names were silent no-ops.
9. `SOB-009` — Boundary events could record an `other_contribution` without identifying which modeled entity contributed.
10. `SOB-010` — Other-model estimates lacked required evidence references and provenance binding.
11. `SOB-011` — After weights were made read-only, `dataclasses.asdict()` could not serialize the mapping proxy used inside snapshots. This was discovered during independent local verification and fixed with explicit plain-data serialization.
12. `SOB-012` — Seed metadata and wall-clock determinism were conflated; timestamp injection was required for reproducible trace timing.

## REWORK COMPLETED

### Identity / role semantics

- Added `SubjectRelation` with research-role labels:
  - `EXTERNAL_OTHER`
  - `SELF_AS_OBSERVED`
  - `PAST_SELF`
  - `COUNTERFACTUAL_SELF`
  - `UNKNOWN`
- The same underlying entity is allowed in different representational roles.
- Duplicate `(other_id, relation_to_subject)` pairs are rejected.
- Lookup by `other_id` alone raises an ambiguity error when multiple roles exist.

### Subject-transition provenance

- `StateTransition` now records `from_subject_ref` and `to_subject_ref`.
- Ordinary untyped subject changes are rejected.
- Explicit subject-transition types are permitted for research use, including perspective or handoff transitions.
- Cross-subject restore requires explicit opt-in and is recorded as `RESTORE_SUBJECT_SWITCH`.
- Restore records the actual source state id.

### Configuration and snapshot integrity

- Distinction weights are copied into a read-only mapping.
- Every weight is individually constrained to `[0.0, 1.0]` and the total must still equal 1.0.
- Active distinctions must match configured distinction weights.
- Snapshot serialization now converts immutable mappings and enums into plain serializable data without weakening in-memory immutability.

### Event and other-model provenance

- `BoundaryEvent` now has explicit `other_ref` attribution when `other_contribution > 0`.
- Event references must resolve to the subject or a modeled entity.
- `OtherModel` now requires non-empty `evidence_refs` and `provenance`.

### Ablation and traceability

- Distinction ablation records an explicit `ABLATE_DISTINCTION` transition.
- Unknown/inactive distinction ablation raises an explicit error rather than silently returning.
- Final-distinction ablation disables the module and records `ABLATE_DISTINCTION_DISABLE` instead of constructing an invalid empty configuration.
- Whole-module ablation records `ABLATE_MODULE`.
- Remaining distinction weights are renormalized after partial ablation.

### Deterministic trace semantics

- Added injectable `timestamp_provider` for reproducible trace timestamps.
- `deterministic_seed` remains experiment/provenance metadata and is not treated as sufficient for wall-clock determinism.

### Construct-language correction

- Removed normative human-development/pathology comments from `BoundaryMode` descriptions.
- Remaining terms such as agency attribution, affective resonance, perspective taking, and narrative differentiation remain research labels requiring construct-validity review.

## INDEPENDENT LOCAL VERIFICATION

The reworked module was reconstructed outside the Nemotron session and independently executed.

Initial regression run:

```text
27 passed in 0.05s
```

A separate snapshot-serialization check then exposed `SOB-011` (`mappingproxy` could not be deep-copied by `dataclasses.asdict`). After CAPA and a dedicated regression test:

```text
28 passed in 0.05s
```

Demo execution also completed successfully through initialization, snapshot, boundary transition, restore, distinction ablation, and whole-module disable.

Verification scope:

- UNIT_TEST_RESULT: PASS (28/28)
- DEMO_RESULT: PASS
- SNAPSHOT_SERIALIZATION_RESULT: PASS
- GITHUB_CI_RESULT: NOT_EXECUTED
- MAIN_EFFECT: NONE
- CANONICAL_EFFECT: NONE
- RUNTIME_EFFECT: NONE

## REMAINING RESEARCH HOLD

The module remains a governed boundary-state representation and lifecycle candidate. It does not yet infer self/other attribution from evidence.

Currently implemented:

- explicit subject-relative role representation
- governed other-model estimates with evidence references
- boundary configuration/state storage
- explicit event-to-entity attribution
- state lifecycle and snapshot/restore
- subject-transition provenance
- distinction ablation controls
- immutable configuration weights

Not yet implemented:

- evidence-driven agency attribution
- sensory-prediction-error computation
- inferred boundary permeability updates
- inferred confusion-index updates
- causal selection among competing self/other hypotheses
- validated engineered mapping for human-theory construct labels

Therefore:

```text
SELF_OTHER_BOUNDARY_REPRESENTATION = IMPLEMENTED
IDENTITY_ROLE_SEMANTICS = IMPLEMENTED_AS_RESEARCH_ROLES
SUBJECT_TRANSITION_PROVENANCE = IMPLEMENTED
ENGINEERING_IQC = PASS
SELF_OTHER_BOUNDARY_INFERENCE = NOT_IMPLEMENTED
CONSTRUCT_VALIDITY = REVIEW_REQUIRED
EMPATHY_CONCLUSION = NOT_ESTABLISHED
THEORY_OF_MIND_CONCLUSION = NOT_ESTABLISHED
SHARED_SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```

## DISPOSITION

`v0.1.1` may proceed as an ENGINEERING-VERIFIED SELF/OTHER BOUNDARY REPRESENTATION CANDIDATE.

It must not be promoted as a complete self/other inference or social-cognition model. A future research version should add evidence-driven attribution, competing-hypothesis evaluation, and matched ablation/control experiments before integration into a larger executable individual model.
