# Exact-head QA Receipt — 2026-08-13

## Source binding

```text
BRANCH = review/four-domain-research-materialization
TARGET_HEAD = efefe5caa657b61fb102a2e376ccaca611ccd0ae
BASE_RESEARCH_HEAD = a5f8bfb7356fafbe9c0c61780f3a76ab0d493c34
MAIN_REFERENCE = abb6550abfacb4fabc53ec04fca783bcc34acfdb
```

The source-state check passed. The candidate worktree had no source drift; the only post-test mutations were generated QA artifacts under `qa/`.

## Final gates

| Gate | Result |
|---|---|
| Current-head release verification | PASS |
| Historical RC verification | PASS |
| Public-tree scan | PASS |
| Targeted existing research QA | PASS; 55 tests |
| Component matrix | 60 eligible records; 57 tested targets; 3 explicit non-applicable targets; 1047 passed; 0 failed targets |
| Branch-native coverage | 57 targets; 0 failed targets |
| Evidence traceability | PASS; acceptance remains `NOT_EVALUATED` |
| QA reconciliation | PASS |
| Strict IQC | PASS |
| Runtime Strong QA syntax | PASS |
| Runtime Strong QA | PASS |

The earlier research targets contributed 10 contextual-authority tests, 9 cross-lineage-contamination tests, 11 replication-epistemics tests, 11 typed-lineage-edge tests, 14 independent-replication-design tests, 11 contextual-authority-adversarial tests, 13 factorial-completeness tests, 20 full-authority tests, and 12 power-analysis tests. The preregistered intervention integrity unit contributed 16 additional passing tests and seven design-only cases; all declared mechanism checks passed with intervention execution and outcome observation explicitly withheld.

## Corrections retained in the audit trail

The first replication experiment runner invocation failed because a same-data fixture supplied `replication_data_ref` twice. The fixture construction was corrected, the 11 tests and five experiment cases were rerun successfully, and the initial failure remains visible in the external research-workbench log.

Earlier exact-head QA attempts exposed stale expected-target parameters as the research target count increased. IQC correctly held for each stale parameter. The runner was updated to `--expected-targets 60`; tracked QA artifacts were restored before the final run so current-head verification started from a clean tree. The final sequence returned `STATUS[CURRENT_HEAD_VERIFY]=0`, `STATUS[STRICT_IQC]=0`, and `RUNTIME_STRONG_QA=PASS`.

These are QA/process repairs, not scientific-result rewrites. No source or component test failure occurred in the final sequence.

## Boundary receipt

```text
RESEARCH_STATUS = ACTIVE / RESEARCH_ONLY
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
LIVE_RUNTIME_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
AION_ASTRA_IDENTITY_EQUIVALENCE = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
```

## Evidence files

The generated branch-native receipts are `qa/CURRENT_TEST_RESULTS.json`, `qa/CURRENT_COVERAGE_RESULTS.json`, `qa/CURRENT_COVERAGE_EVIDENCE.json`, `qa/CURRENT_QA_RECONCILIATION.json`, `qa/CURRENT_EVIDENCE_TRACEABILITY.json`, `qa/CURRENT_RELEASE_STATUS_LOCK.json`, `qa/TEST_RESULTS.md`, `qa/COVERAGE_REPORT.md`, and `qa/IQC_REPORT.json`.
