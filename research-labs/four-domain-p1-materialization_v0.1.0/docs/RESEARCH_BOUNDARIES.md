# P1 Research Boundaries

This package materializes three previously identified research gaps without integrating them into any runtime or canonical service.

## Temporal / version resolution

The resolver distinguishes:

- `event_time`: when an external event is claimed to have occurred;
- `observed_at`: when an observation was made;
- `valid_from` / `valid_to`: the domain-valid interval of a version;
- `recorded_at`: when the version entered the research ledger;
- `revision_of`: explicit version lineage;
- `as_was`: what the research ledger could actually have returned at a historical cutoff;
- retrospective annotation: later interpretation kept separate from the historical state.

A later backfilled version is never allowed to appear in an `as_was` view before its own `recorded_at` timestamp. This is the explicit anti-back-projection invariant.

## Correction / conflict transition lineage

The correction ledger keeps claims immutable and records transitions separately. A supersession requires an explicit prior correction approval for the same source/target pair. Conflict detection and conflict resolution are also separate events. Actor, role, time and evidence are mandatory for every transition.

This does not define who is authorized to approve a production correction. The `actor_role` field records supplied research evidence; it does not grant authority.

## Memory evaluation harness

The harness currently measures deterministic fixture-level observations for:

- retrieval precision;
- retrieval recall;
- source attribution accuracy;
- temporal/version accuracy;
- correction recovery;
- abstention accuracy;
- provenance completeness;
- unsupported inference rate;
- stale-memory influence.

Undefined metrics remain `None`; the harness does not silently convert missing ground truth into a failing or passing score.

## Explicit non-effects

```text
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
DEPLOYMENT_EFFECT = NONE
NETWORK_ACCESS = NONE
PERSISTENT_STORAGE = NONE
AUTOMATIC_WRITEBACK = NO
MODEL_WEIGHT_CHANGE = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```
