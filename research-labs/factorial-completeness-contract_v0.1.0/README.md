# Factorial Completeness Contract v0.1.0

Status: `RESEARCH_ONLY / SYNTHETIC_FIXTURES / EFFECT_ESTIMATION=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a bounded contract determine whether a declared full-factorial design has exact Cartesian coverage and sufficient execution metadata, while keeping matrix completeness separate from replication validity, effect estimation, model interpretation, and scientific confirmation?

NIST describes a full factorial as the full complement of possible factor combinations and notes that this permits estimation of main and interaction effects in the full model.[1] NIST also places design selection, execution controls, replication, randomization, model testing, interpretation, and confirmation in distinct parts of the design-of-experiments workflow.[2] SciRep's computational-experiment framework further motivates explicit configuration, execution, validation, and artifact records.[3]

This prototype implements only a deterministic matrix/execution contract over synthetic records. It does **not** estimate effects, fit a model, calculate statistical power, or establish a scientific conclusion.

## Decision layers

| Layer | Values | Meaning |
|---|---|---|
| Matrix status | `COMPLETE`, `INCOMPLETE`, `INVALID` | Whether declared factor names/levels and expected Cartesian cells are valid and exactly covered at the declared replication count. |
| Execution status | `COMPLETE`, `PARTIAL`, `UNKNOWN` | Whether each run has protocol, execution, and provenance references. |
| Disposition | `ADMISSIBLE_FOR_DESIGN_REVIEW`, `INDETERMINATE`, `HOLD` | Whether the record is structurally admissible for later design review, incomplete/uncertain, or blocked by malformed cells or missing execution metadata. |

`ADMISSIBLE_FOR_DESIGN_REVIEW` is deliberately weaker than scientific confirmation. It means only that the synthetic matrix and execution metadata satisfy this contract.

## Experiment results

The six synthetic cases were complete, missing-cell, duplicate-cell, under-replicated, invalid-cell, and missing-execution-metadata.

| Case | Matrix | Execution | Disposition |
|---|---|---|---|
| Complete | `COMPLETE` | `COMPLETE` | `ADMISSIBLE_FOR_DESIGN_REVIEW` |
| Missing cell | `INCOMPLETE` | `COMPLETE` | `INDETERMINATE` |
| Duplicate cell | `INCOMPLETE` | `COMPLETE` | `INDETERMINATE` |
| Under-replicated | `INCOMPLETE` | `COMPLETE` | `INDETERMINATE` |
| Invalid/out-of-domain cell | `INVALID` | `COMPLETE` | `HOLD` |
| Missing execution metadata | `COMPLETE` | `PARTIAL` | `HOLD` |

The 13 unit tests and six experiment cases passed after correcting one initial implementation defect in factor-order canonicalization. That initial failure remains recorded in `research-workbench/autonomous-growth/2026-08-13-contextual-authority-memory/factorial-completeness-initial-failure.md`.

## Hypotheses and falsifiers

`H1`: Exact Cartesian enumeration distinguishes complete coverage from missing, duplicate, under-replicated, and out-of-domain cells.

`H2`: A matrix can be complete while execution remains `PARTIAL` when protocol, execution, or provenance metadata is missing; the disposition must then be `HOLD`.

`H3`: The contract never converts structural completeness into effect estimation, scientific confirmation, canonical effect, deployment, subjectivity, or identity conclusions.

A falsifier would be a missing or malformed cell accepted as complete, an execution-incomplete matrix admitted without `HOLD`, or any effect/canonical/deployment conclusion emitted by the contract.

## Run

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_completeness_experiment.py --output fixtures/completeness_result.json
```

## Non-claims and invariants

```text
MATRIX_COMPLETE != EFFECT_ESTABLISHED
MATRIX_COMPLETE != REPLICATION_VALIDITY
MATRIX_COMPLETE != SCIENTIFIC_CONFIRMATION
ADMISSIBLE_FOR_DESIGN_REVIEW != DEPLOYMENT
EFFECT_ESTIMATION_PERFORMED = FALSE
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## References

[1]: https://www.itl.nist.gov/div898/handbook/pri/section3/pri3332.htm "NIST — Full factorial example"
[2]: https://www.itl.nist.gov/div898/handbook/pri/pri.htm "NIST — Process Improvement and design-of-experiments overview"
[3]: https://arxiv.org/html/2503.07080v3 "Costa, Barbosa & Cunha — A Framework for Supporting the Reproducibility of Computational Experiments in Multiple Scientific Domains"
