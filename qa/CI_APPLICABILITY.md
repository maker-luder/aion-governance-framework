# Final Formal Research CI Applicability and Evidence

This document describes the **current final formal-research tree**. Historical review-branch applicability notes are retained only as historical provenance and are not current-state claims.

## Current local applicability

| Check | Applicability/result | Current evidence |
|---|---|---|
| Dynamic current-target matrix | `PASS` | `qa/CURRENT_TEST_RESULTS.json`: 50 eligible/current targets, 47 tested, 3 explicit non-applicable, 920 passed, 0 failed |
| Whole-system validation | `PASS` | `qa/WHOLE_SYSTEM_VALIDATION.json`: 21 test cases, 11 scenario classes |
| Branch coverage | `PASS` | `qa/CURRENT_COVERAGE_RESULTS.json` and `qa/coverage/` |
| Runtime Strong QA | `PASS` | `scripts/run_runtime_strong_qa.sh` in final exact-head QA |
| Research Scope Lock | `PASS` | `scripts/check_research_scope_lock.py` |
| Autonomous-growth contract | `PASS` | `scripts/check_autonomous_growth_contract.py`; 8 validated cycle records |
| Public-tree scan | `PASS` | `scripts/scan_public_tree.py` |
| Sensitive-material scan | `PASS` | `scripts/scan_sensitive_material.py` |
| Stale-evidence scan | `PASS` | `scripts/scan_stale_evidence.py` |
| Manifest integrity | `PASS` | `qa/final_current_manifest/` and manifest generate/verify evidence |
| Current QA reconciliation | `PASS` | `qa/CURRENT_QA_RECONCILIATION.json` bound to `TESTED_SUBJECT_HEAD = 8dd022f805f4eab9593ee64dc2db93155a55079d` |
| Evidence traceability / IQC | `PASS` | `qa/CURRENT_EVIDENCE_TRACEABILITY.json`, `qa/IQC_REPORT.json` |
| Workflow syntax | `PASS` | final local gate receipt |

## Remote workflow applicability

The final remote verification is bound to the exact published commit under review. A remote success is recorded only when GitHub reports the workflow name, run ID, head SHA, completed status and success conclusion. The PART 2C final report is the authoritative record for the final published head's remote run IDs.

The final published evidence head is `6685724a47b2c6325f437442b0c68903c8e2ef43`. Its actual run list contained:

| Workflow | Run ID | Head SHA | Status | Conclusion |
|---|---:|---|---|---|
| `Quality` | `31659596250` | `6685724a47b2c6325f437442b0c68903c8e2ef43` | `completed` | `success` |
| `Research Scope Lock` | not triggered for this evidence-only path | — | `N/A` | no success inferred |
| `Research Workbench CI` | not listed for this push | — | `N/A` | no success inferred |

For provenance, the immediately preceding evidence checkpoint `3d8f8a6a2afd88a4ce523cc889390d72a9e81f48` had actual `Quality` run `31659136893` and `Research Scope Lock` run `31659136856`, both `completed / success` on that predecessor head. No workflow result is inferred from local QA, and no untriggered workflow is represented as a pass.

## Governance locks

```text
BASE_BRANCH = review/four-domain-research-materialization
PROTECTED_BRANCH = main
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
PRODUCTION_RUNTIME_AUTHORIZED = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
```
