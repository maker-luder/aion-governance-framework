# Exact-head QA Receipt — 2026-08-13

## Source binding

```text
BRANCH = review/four-domain-research-materialization
TARGET_HEAD = 1bcd7c462727f9a850fa980c9284d74ec03d2886
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
| Targeted existing research QA | PASS |
| Component matrix | 52 eligible records; 49 tested targets; 3 explicit non-applicable targets; 939 passed; 0 failed targets |
| Branch-native coverage | 49 targets; 0 failed targets |
| Evidence traceability | PASS; acceptance remains `NOT_EVALUATED` |
| QA reconciliation | PASS |
| Strict IQC | PASS |
| Runtime Strong QA syntax | PASS |
| Runtime Strong QA | PASS |

The two new research targets contributed 10 contextual-authority tests and 9 cross-lineage-contamination tests; both targets passed.

## Correction retained in the audit trail

The first exact-head runner invocation used `--expected-targets 49`, treating tested targets as the IQC record count. The IQC contract counts all 52 records in `CURRENT_TEST_RESULTS.json`, including three explicit non-applicable records, and correctly returned `HOLD` for the mismatched runner parameter. No source or test failure occurred. The runner was corrected to `--expected-targets 52` and the entire sequence was rerun. The corrected sequence returned `STATUS[STRICT_IQC]=0` and `verdict=PASS`.

This correction is a QA-process repair, not a scientific-result rewrite. The initial HOLD remains preserved in the external exact QA log for reproducibility.

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
