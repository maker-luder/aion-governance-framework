# Exact-head QA Receipt — 2026-08-13

## Source binding

```text
BRANCH = review/four-domain-research-materialization
TESTED_HEAD = 1a9cd4e88d274cf5547bf82234a8e87770dc7c6e
RECEIPT_HEAD = TO_BE_BOUND
REPORTING_HEAD = TO_BE_BOUND
BASE_RESEARCH_HEAD = 6425262527f893138afe3c4e64a0cd2052d8353a
CURRENT_MAIN_REFERENCE = abb6550abfacb4fabc53ec04fca783bcc34acfdb
```

The source-state check passed for `TESTED_HEAD`. `RECEIPT_HEAD` and `REPORTING_HEAD` are deliberately left unbound until the evaluation-harness QA artifact and provenance/reporting commits are complete. Neither is presented as the exact execution state. The exact execution ran against the clean source commit `1a9cd4e`; the QA runner then generated the branch-native QA artifacts.

## Final gates

| Gate | Result |
|---|---|
| Current-head release verification | PASS |
| Historical RC verification | PASS |
| Public-tree scan | PASS |
| Targeted existing research QA | PASS; 55 tests |
| Component matrix | 73 eligible records; 70 tested targets; 3 explicit non-applicable targets; 1286 passed; 0 failed targets |
| Branch-native coverage | 70 targets; 0 failed targets |
| Evidence traceability | PASS; acceptance remains `NOT_EVALUATED` |
| QA reconciliation | PASS |
| Strict IQC | PASS; exact head and `--expected-targets 73` |
| Runtime Strong QA syntax | PASS |
| Runtime Strong QA | PASS |

The governance-reassessment-oscillation-adversarial unit contributed 19 passing tests and 14 synthetic cases. It classified stable sequences, a two-reversal oscillatory sequence, stale and contradictory evidence, unknown currentness, incomplete provenance, ordering and direction mismatches, missing policy metadata, and a boundary-effect request. Its synthetic metadata remained review-only; no model was executed and no observed result was asserted. All per-decision outputs preserved `CANONICAL_EFFECT=NONE`, `GOVERNANCE_EFFECT=NONE`, and `DEPLOYMENT=FALSE`. The artifact-transformation-lineage-adversarial unit contributed 20 passing tests and 15 synthetic cases, audited event ordering, job/provenance drift, secret redaction, artifact path/source and digest integrity, and retained one initial fixture-construction defect before correction; no transformation was executed and no artifact was promoted. The external-evidence-normalization-adversarial unit contributed 16 passing tests and 13 synthetic cases, retained base normalizer distinctions, and added report-ID, branch, actor, execution-mode, result-observation, and non-promotion audits; no external result was verified or promoted. The research-evaluation-harness-adversarial unit contributed 21 passing tests and 18 synthetic report/comparison cases, retained negative results and case provenance distinctions, and did not call `evaluate_dataset` or execute a task/model.

Earlier research targets contributed 10 contextual-authority tests, 9 cross-lineage-contamination tests, 11 replication-epistemics tests, 11 typed-lineage-edge tests, 14 independent-replication-design tests, 11 contextual-authority-adversarial tests, 13 factorial-completeness tests, 20 full-authority tests, 12 power-analysis tests, 16 preregistration-integrity tests, and 13 replication-handoff tests. The matched-divergence protocol unit contributed 15 additional passing tests and eight design-only cases; all declared mechanism checks passed with model execution and outcome observation explicitly withheld. The evidence-admission/non-promotion unit contributed 14 passing tests and eight synthetic cases; its admissibility statuses remained review metadata only and did not promote evidence, establish a scientific conclusion, or request governance effects. The validated-individuation-thresholds unit contributed 16 passing tests and eight synthetic cases; its reviewable criterion profile did not validate a threshold, establish identity continuity, or execute a perturbation. The zero-day-governance-candidate unit contributed 23 passing tests and 12 synthetic cases; its provisional classification was `USEFUL_SYNTHESIS_ONLY`, with novelty remaining `NOT_ESTABLISHED` and cybersecurity zero-day exploit scope explicitly excluded. The AION/Astra matched-divergence study-design unit contributed 22 passing tests and 13 synthetic cases; it bound intended system/source metadata and explicitly withheld model execution and outcome observation. The replication-environment-drift-adversarial unit contributed 21 passing tests and 13 synthetic cases; it separated artifact readiness, environment drift, reported result state, uncertainty/tolerance metadata, and review-only interpretation without certifying replication. The evidence-currentness-deduplication unit contributed 21 passing tests and 15 synthetic cases; it separated current/stale/historical/retrieved-only/remembered/unknown status, duplicate underlying evidence, derived records, and replication mislabeling without promoting evidence. The factorial-execution-integrity unit contributed 18 passing tests and 14 synthetic cases; it separated planned/attempted/completed/failed/aborted/excluded/unreported cells, required deviation metadata for attrition, preserved negative/null/indeterminate outcomes, and rejected post-outcome cell additions without executing a model.

## Corrections retained in the audit trail

The first replication experiment runner invocation failed because a same-data fixture supplied `replication_data_ref` twice. The fixture construction was corrected, the 11 tests and five experiment cases were rerun successfully, and the initial failure remains visible in the external research-workbench log.

Earlier exact-head QA attempts exposed stale expected-target parameters as the research target count increased. IQC correctly held for each stale parameter. The runner was updated from `--expected-targets 72` to `--expected-targets 73`; tracked QA artifacts were restored before the final run so current-head verification started from a clean tree. The clean 73-record sequence returned `STATUS[CURRENT_HEAD_VERIFY]=0`, `STATUS[STRICT_IQC]=0`, and `RUNTIME_STRONG_QA=PASS`. The final IQC report records 1286 passed tests across 73 eligible targets and coverage over 70 tested targets.

These are QA/process repairs, not scientific-result rewrites. No source or component test failure occurred in the final sequence. Contradictory and indeterminate evidence cases remain represented in the evidence-admission, individuation-threshold, zero-day-governance, AION/Astra study-design, replication-environment-drift, evidence-currentness-deduplication, factorial-execution-integrity, and governance-reassessment-oscillation fixtures and tests. The individuation ordering failure, zero-day lifecycle/helper failures, AION/Astra head/evidence completeness failures, currentness boundary-output failure, and factorial execution-ID fixture failure remain preserved in their initial-failure records; the replication-drift unit and governance-oscillation unit had no initial test failure; the artifact-lineage unit's initial duplicate-ID fixture defect remains preserved in its module record; the external-evidence adversarial unit and research-evaluation-harness adversarial unit had no initial test failure.

## Boundary receipt

```text
RESEARCH_STATUS = ACTIVE / RESEARCH_ONLY
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
LIVE_RUNTIME_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
AION_ASTRA_IDENTITY_EQUIVALENCE = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
```

## Evidence files

The generated branch-native receipts for the exact run are `qa/CURRENT_TEST_RESULTS.json`, `qa/CURRENT_COVERAGE_RESULTS.json`, `qa/CURRENT_COVERAGE_EVIDENCE.json`, `qa/CURRENT_QA_RECONCILIATION.json`, `qa/CURRENT_EVIDENCE_TRACEABILITY.json`, `qa/CURRENT_RELEASE_STATUS_LOCK.json`, `qa/TEST_RESULTS.md`, `qa/COVERAGE_REPORT.md`, and `qa/IQC_REPORT.json`. The exact-run log is retained outside the repository as an operational artifact and is not a release input.
