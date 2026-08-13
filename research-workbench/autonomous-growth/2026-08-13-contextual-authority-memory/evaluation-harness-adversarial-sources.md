# Research Evaluation Harness Adversarial — Source Notes

## Unit boundary

`research-evaluation-harness-adversarial_v0.1.0` is a research-only metadata audit extension. It constructs reports and comparisons but does not call the harness task function, execute a model, observe a runtime result, promote a claim, modify canonical state, deploy, or establish subjectivity.

## Reused repository evidence

| Source item | Stable reference | Source kind | Status | Transformation |
|---|---|---|---|---|
| Existing evaluation harness core | `repo:research-labs/research-evaluation-harness_v0.1.0/src/aion_research_eval/core.py` | Repository Evidence | Current within the verified research lineage at the unit commit; exact state is bounded by QA receipt | Reused CaseResult, ExperimentReport, pass-rate, report comparison, and ClaimBoundaryGate structures; no evaluator result was counted as new evidence |
| Existing evaluation harness README/crosswalk | `repo:research-labs/research-evaluation-harness_v0.1.0/README.md` and `docs/EXTERNAL_SOURCE_CROSSWALK.md` | Repository Evidence | Current within branch lineage; external methodological source currentness is not newly asserted | Used as methodological and boundary context; no external source code or runtime dependency copied |
| Current remote main reference | `git:origin/main@abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Tool Output / Repository Evidence | Independently verified by read-only fetch at the latest successful checkpoint | Read-only branch-state reference; no main content or authority modified |

## Synthetic transformation

The audit maps declared report/comparison metadata to `ADMITTED_FOR_REVIEW`, `HOLD`, or `INVALID`. A valid report means only that the supplied structure passed bounded checks. Negative results remain visible and are not transformed into positive evidence. The 18 synthetic cases are fixtures, not external evidence and not replication evidence.

The experiment intentionally does not call `evaluate_dataset`; no task or model is executed and no observed result is asserted.

## Provenance vocabulary

```text
REPORT_AUDIT_PASS != SCIENTIFIC_VALIDITY
PASS_RATE != GENERALIZATION
COMPARISON != INDEPENDENT_REPLICATION
NEGATIVE_RESULT_RETAINED != FAILURE_OF_REAL_SYSTEM
ADMITTED_FOR_REVIEW != CLAIM_PROMOTED
RESEARCH_RESULT != CANONICAL_CONCLUSION
```

## Non-promotion invariants

```text
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```
