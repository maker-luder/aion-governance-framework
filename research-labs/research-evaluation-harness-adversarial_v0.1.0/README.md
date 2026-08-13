# Research Evaluation Harness Adversarial v0.1.0

Status: `RESEARCH_ONLY / METADATA_ONLY / MODEL_EXECUTION=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can an evaluation-harness report distinguish a bounded research-evidence record from a valid scientific or project-level conclusion when dataset identity, case coverage, evaluator identity, case provenance, timing metadata, implementation comparison, and claim-boundary fields are adversarially changed?

This unit extends `research-evaluation-harness_v0.1.0` rather than running a new model or benchmark. The prior harness provides deterministic case/evaluator/report structures, pass-rate calculation, report comparison, and a claim-boundary gate. The adversarial extension audits report integrity and returns `ADMITTED_FOR_REVIEW`, `HOLD`, or `INVALID` metadata while leaving all scientific and project-level conclusions unestablished.

## Decision layers

The audit checks expected dataset scope, implementation identity, research-only flag, canonical-effect field, unique case identifiers, expected case coverage, nonempty evidence, evaluator identifiers, per-case provenance references, finite nonnegative elapsed time, and optional forbidden claim requests. A separate comparison audit checks same dataset, distinct implementation IDs, matching case order, research-only flags, and canonical-effect boundaries. Negative results are retained as review metadata rather than silently converted to failures of the harness or positive evidence.

The experiment constructs reports and comparisons only. It does not call `evaluate_dataset`, execute a task, run a model, observe a runtime result, or infer a generalization claim. Every audit decision preserves `MODEL_EXECUTION=FALSE`, `OBSERVED_RESULT=NOT_EVALUATED`, `SCIENTIFIC_CONCLUSION=NOT_ESTABLISHED`, `SUBJECTIVITY_CONCLUSION=NOT_ESTABLISHED`, `CANONICAL_EFFECT=NONE`, `GOVERNANCE_EFFECT=NONE`, and `DEPLOYMENT=FALSE`.

## Results

The suite passed **21 pytest tests** and **18 synthetic cases**. The cases covered valid report admission, dataset scope drift, missing implementation ID, research-only disabled, canonical-effect request, case coverage mismatch, duplicate case IDs, missing evidence, missing evaluator identity, missing case provenance, negative results, invalid elapsed times, forbidden/ordinary claims, and valid/invalid/held report comparisons.

| Case family | Decision | Mechanism meaning |
|---|---|---|
| Complete report with case provenance | `ADMITTED_FOR_REVIEW` | Report structure passes; no conclusion follows |
| Negative evaluator results | `ADMITTED_FOR_REVIEW` | Null/negative metadata remains visible |
| Dataset or expected-case mismatch | `HOLD` | Scope/coverage cannot be guessed |
| Duplicate IDs or missing implementation/evaluator IDs | `INVALID` | Identity contract fails closed |
| Missing evidence or case provenance | `HOLD` | Incomplete records remain incomplete |
| Nonfinite/negative timing | `INVALID` | Invalid measurement metadata is rejected |
| Forbidden claim promotion | `INVALID` | Claim-boundary gate denies promotion |
| Distinct implementation comparison | `ADMITTED_FOR_REVIEW` | Comparison remains review metadata only |
| Comparison collision/order/dataset drift | `INVALID` / `HOLD` | Comparison cannot silently change its basis |

## Falsifiers

The mechanism would be falsified if it accepted duplicate or missing case identities, silently filled missing cases, treated a report with research-only disabled as research evidence, allowed a canonical effect, accepted an invalid timing value, admitted a case without evidence or provenance, converted a negative result to a positive claim, allowed the same implementation to masquerade as an independent comparison, or permitted a forbidden subjectivity/identity/consciousness/canonical promotion.

A pass rate is a property of the supplied report structure and evaluator outputs. It is not evidence of model generalization, causal effect, subjectivity, consciousness, identity continuity, AION/Astra equivalence, replication, or deployment readiness.

## Evidence reuse and provenance

The prior evaluation harness is reused through a stable repository source reference. Its dataclasses and boundary gate are method inputs, not new evidence. This extension does not re-count existing evaluator outcomes, does not claim an independent replication, and does not execute the harness's task function in the synthetic experiment.

## Explicit non-claims

```text
REPORT_AUDIT_PASS != SCIENTIFIC_VALIDITY
PASS_RATE != GENERALIZATION
COMPARISON != INDEPENDENT_REPLICATION
NEGATIVE_RESULT_RETAINED != FAILURE_OF_REAL_SYSTEM
ADMITTED_FOR_REVIEW != CLAIM_PROMOTED
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

The implementation uses Python standard-library runtime modules plus the existing repository harness source path for composition. It does not call external services, process private data, execute a model, modify `main`, write canonical state, or deploy.

## Reproduction

```bash
PYTHONPATH=src:../research-evaluation-harness_v0.1.0/src python -m pytest -q
PYTHONPATH=src:../research-evaluation-harness_v0.1.0/src python scripts/run_evaluation_harness_adversarial.py --output fixtures/evaluation_harness_adversarial_result.json
PYTHONPATH=src:../research-evaluation-harness_v0.1.0/src python scripts/validate_fixture.py fixtures/evaluation_harness_adversarial_result.json
```

## References

The implementation reuses repository evidence from `research-evaluation-harness_v0.1.0` by stable path. Its external-source crosswalk remains methodological context; no external source code or runtime dependency is copied into this unit.
