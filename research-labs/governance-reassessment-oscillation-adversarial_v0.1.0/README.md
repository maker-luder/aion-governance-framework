# Governance Reassessment Oscillation Adversarial v0.1.0

Status: `RESEARCH_ONLY / METADATA_ONLY / MODEL_EXECUTION=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a temporal reassessment ledger distinguish a stable review sequence from repeated up/down oscillation while preserving stale, contradictory, unknown, and incompletely provenanced evidence as review states rather than silently turning them into automatic governance changes?

This unit adversarially extends `evidence-responsive-governance-reassessment_v0.1.0`. The existing module already provides provisional evidence levels, replication-sensitive reassessment recommendations, review dispositions, counterevidence references, and low-authority precautionary boundaries. This unit adds only temporal sequence auditing: event ordering, direction consistency, oscillation count, stale/contradictory/unknown handling, correction metadata, and a human-review requirement.

## Contract

A sequence requires preregistration, currentness-policy, and hysteresis-policy references. Each event requires a unique positive sequence index, source/provenance/interpretation references, claim scope, reason, observed evidence level, status, and direction. The declared direction must match the level transition unless the event explicitly records a bounded `SCOPE_REVIEW`.

Two direction reversals are classified as `OSCILLATORY` and held for review. A single reversal is not automatically treated as oscillation. Stale evidence is always held for review; stale reversal without correction and stale/contradictory evidence without basis are separately reason-coded. Contradictory evidence with counterevidence remains indeterminate and does not automatically downgrade or upgrade an evidence level. Unknown currentness and incomplete event provenance are held. Duplicate event identifiers, duplicate/non-positive sequence indices, direction mismatches, conclusion overreach, disabled human review, missing policy metadata, and boundary-effect requests fail closed.

All output decisions normalize to `CANONICAL_EFFECT=NONE`, `GOVERNANCE_EFFECT=NONE`, `DEPLOYMENT=FALSE`, and `SCIENTIFIC_CONCLUSION=NOT_ESTABLISHED`.

## Results

The module passed **19 pytest tests** and **14 synthetic cases**. The cases included stable sequence, oscillation after two reversals, single reversal, stale evidence with and without correction, stale reversal, contradictory evidence with and without counterevidence, unknown currentness, incomplete provenance, direction mismatch, duplicate sequence index, missing policy metadata, and boundary request.

| Case family | Decision | Mechanism meaning |
|---|---|---|
| Stable sequence | `STABLE / REVIEW_ONLY` | No repeated reversal detected; still review metadata only |
| Two direction reversals | `OSCILLATORY / HOLD` | Reassessment instability requires human review |
| Stale evidence | `INDETERMINATE / HOLD` | Stale evidence cannot drive automatic stable status |
| Stale reversal without correction | `INDETERMINATE / HOLD` | Reversal requires correction/review |
| Contradictory evidence | `INDETERMINATE / HOLD` | Counterevidence retained; no automatic downgrade |
| Unknown currentness | `INDETERMINATE / HOLD` | No currentness guess |
| Incomplete provenance | `INDETERMINATE / HOLD` | Event cannot enter interpreted sequence |
| Invalid ordering/direction | `INVALID / HOLD` | Temporal/event contract failure |
| Boundary or conclusion overreach | `INVALID / HOLD` | Effects normalized and claim rejected |

## Falsifiers

The mechanism would be falsified if it accepted duplicate or non-positive event indexes, treated a stale or unknown record as current without review, silently collapsed contradictory evidence, classified a single reversal as repeated oscillation, accepted a direction inconsistent with observed levels, allowed a post hoc scope change without an explicit review event, disabled human review, or emitted an automatic governance/canonical/deployment effect.

The synthetic result does not establish that any real governance process oscillates, does not measure stability, does not validate hysteresis thresholds, and does not infer subjectivity, consciousness, identity continuity, AION/Astra equivalence, causal effect, or deployment behavior.

## Evidence reuse and provenance

The existing reassessment model and repository evidence are reused through stable module references; they are not counted as new independent evidence. The unit does not duplicate the replication evidence already represented by `replication-environment-drift-adversarial_v0.1.0` or `evidence-currentness-deduplication_v0.1.0`. It uses their currentness/provenance distinctions as methods context only.

## Explicit non-claims

```text
OSCILLATORY_METADATA != REAL_WORLD_OSCILLATION
STALE_EVIDENCE != NEGATIVE_SCIENTIFIC_RESULT
CONTRADICTORY_EVIDENCE != AUTOMATIC_DOWNGRADE
REVIEW_RECOMMENDATION != GOVERNANCE_DECISION
STABLE_SEQUENCE != SCIENTIFIC_VALIDITY
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

The implementation uses only the Python standard library. It does not run a model, query private data, modify `main`, or change canonical state.

## Reproduction

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_oscillation_experiment.py --output fixtures/oscillation_result.json
```

## References

The model reuses the repository's prior-art records for evidence-responsive governance reassessment and currentness/provenance methods. It does not claim those records are new evidence.
