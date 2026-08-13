# Exact-head QA Receipt — 2026-08-13

## Source binding

```text
BRANCH = review/four-domain-research-materialization
TESTED_HEAD = 0c8f37d387c0b5ca02e38e659744c577324ce691
RECEIPT_HEAD = TO_BE_BOUND_BY_NEXT_QA_BIND_COMMIT
REPORTING_HEAD = 0c8f37d387c0b5ca02e38e659744c577324ce691
BASE_RESEARCH_HEAD = 38448090de60e0f031c15147ecdfa93947562ae3
CURRENT_MAIN_REFERENCE = abb6550abfacb4fabc53ec04fca783bcc34acfdb
```

The source-state check passed for `TESTED_HEAD`. `REPORTING_HEAD` identifies the unit/provenance reporting state included in the exact execution. `RECEIPT_HEAD` is intentionally left to the subsequent binding commit and must not be represented as the exact execution state. The exact execution ran against the clean source commit `0c8f37d`; the QA runner then generated the branch-native artifacts. `main` remained read-only.

## Final gates

| Gate | Result |
|---|---|
| Current-head release verification | PASS |
| Historical RC verification | PASS |
| Public-tree scan | PASS |
| Targeted existing research QA | PASS; 55 tests |
| Component matrix | 81 eligible records; 78 tested targets; 3 explicit non-applicable targets; 1481 passed; 0 failed targets |
| Branch-native coverage | 78 targets; 0 failed targets |
| Evidence traceability | PASS; acceptance remains `NOT_EVALUATED` |
| QA reconciliation | PASS |
| Strict IQC | PASS; exact head and `--expected-targets 81` |
| Runtime Strong QA syntax | PASS |
| Runtime Strong QA | PASS |

The power-analysis-uncertainty-adversarial unit contributed 20 passing tests and 20 synthetic planning/assumption-lock cases. It checked finite numeric values, alpha/target-power bounds, positive effect and standard-deviation inputs, plan/sample-size identity, preregistration and assumption-basis completeness, sensitivity monotonicity, decision serialization, and assumption mutation before/after a hypothetical outcome. Adequate and one-sided plans remained planning review metadata; underpowered plans remained indeterminate; missing inputs remained unknown; invalid values failed closed; and no achieved power or effect was observed. Every case preserved `ACHIEVED_POWER_CALCULATED=FALSE`, `EFFECT_OBSERVED=FALSE`, `SCIENTIFIC_CONCLUSION=NOT_ESTABLISHED`, `CANONICAL_EFFECT=NONE`, `GOVERNANCE_EFFECT=NONE`, and `DEPLOYMENT=FALSE`.

The governance-reassessment-oscillation-adversarial unit contributed 19 passing tests and 14 synthetic cases. The artifact-transformation-lineage-adversarial unit contributed 20 passing tests and 15 synthetic cases and retained its initial fixture-construction defect before correction. The external-evidence-normalization-adversarial unit contributed 16 passing tests and 13 synthetic cases. The research-evaluation-harness-adversarial unit contributed 21 passing tests and 18 synthetic report/comparison cases. The external-agent-sandbox-protocol-adversarial unit contributed 22 passing tests and 19 synthetic policy/candidate cases. The governed-tool-approval-adversarial unit contributed 21 passing tests and 20 synthetic disposition/batch cases. The trace-provenance-crosswalk-adversarial unit contributed 26 passing tests and 25 synthetic trace/crosswalk cases. The shared-origin-divergence-governance-adversarial unit contributed 21 passing tests and 20 synthetic lineage/evidence/comparison/authority cases. The selective-memory-control-adversarial unit contributed 30 passing tests and 29 synthetic memory/retrieval cases. The research-integrity-security-adversarial unit contributed 31 passing tests and 31 synthetic evidence/provenance/tombstone/action/batch cases. The preregistered-intervention-integrity-adversarial unit contributed 24 passing tests and 24 synthetic plan/lock cases. These units retained review-only, hold, indeterminate, invalid, negative, contradictory, and non-promotion distinctions; they did not execute models/interventions/tools/agents or write canonical state.

Earlier research targets contributed 10 contextual-authority tests, 9 cross-lineage-contamination tests, 11 replication-epistemics tests, 11 typed-lineage-edge tests, 14 independent-replication-design tests, 11 contextual-authority-adversarial tests, 13 factorial-completeness tests, 20 full-authority tests, 12 power-analysis tests, 16 preregistration-integrity tests, 13 replication-handoff tests, 15 matched-divergence protocol tests, 14 evidence-admission/non-promotion tests, 16 validated-individuation-threshold tests, 23 zero-day-governance-candidate tests, 22 AION/Astra matched-divergence study-design tests, 21 replication-environment-drift-adversarial tests, 21 evidence-currentness-deduplication tests, and 18 factorial-execution-integrity tests. These prior targets remain research-only and do not constitute scientific validation, subjectivity evidence, identity evidence, or canonical promotion.

## Corrections retained in the audit trail

The first replication experiment runner invocation failed because a same-data fixture supplied `replication_data_ref` twice. The fixture construction was corrected, the 11 tests and five experiment cases were rerun successfully, and the initial failure remains visible in the external research-workbench log.

Earlier exact-head QA attempts exposed stale expected-target parameters as the research target count increased. IQC correctly held for each stale parameter. The runner was updated from `--expected-targets 80` to `--expected-targets 81`; tracked QA artifacts were restored before the final run so current-head verification started from a clean tree. The clean 81-record sequence returned `STATUS[CURRENT_HEAD_VERIFY]=0`, `STATUS[STRICT_IQC]=0`, and `RUNTIME_STRONG_QA=PASS`. The final IQC report records 1481 passed tests across 81 eligible targets, 78 tested targets, and 3 explicit non-applicable targets; branch coverage measured 78 targets with 0 failed targets.

The power-analysis adversarial unit had no initial test failure. Its final result is nevertheless bounded: the synthetic fixture validates declared planning mechanics, not empirical assumptions or outcomes. Prior retained defects and corrections include the individuation ordering failure, zero-day lifecycle/helper failures, AION/Astra head/evidence completeness failures, evidence-currentness boundary-output failure, factorial execution-ID fixture failure, artifact-lineage duplicate-ID fixture defect, selective-memory validator construction repair, and preregistered-intervention adversarial enum-member construction failure corrected to the inherited `INDETERMINATE/HOLD` contract. These are QA/process records, not scientific-result rewrites. Contradictory and indeterminate evidence cases remain represented in their source fixtures and tests.

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
ACHIEVED_POWER_CALCULATED = FALSE
EFFECT_OBSERVED = FALSE
```

## Evidence files

The generated branch-native receipts for the exact run are `qa/CURRENT_TEST_RESULTS.json`, `qa/CURRENT_COVERAGE_RESULTS.json`, `qa/CURRENT_COVERAGE_EVIDENCE.json`, `qa/CURRENT_QA_RECONCILIATION.json`, `qa/CURRENT_EVIDENCE_TRACEABILITY.json`, `qa/CURRENT_RELEASE_STATUS_LOCK.json`, `qa/TEST_RESULTS.md`, `qa/COVERAGE_REPORT.md`, and `qa/IQC_REPORT.json`. The exact-run log is retained outside the repository as an operational artifact and is not a release input. The power-analysis source note is `research-workbench/autonomous-growth/2026-08-13-contextual-authority-memory/power-analysis-adversarial-sources.md`.
