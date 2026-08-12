# Review v2 CI Applicability and Evidence

## Local checks

| Check | Result | Evidence |
|---|---|---|
| Dynamic component matrix | PASS | `qa/CURRENT_TEST_RESULTS.json`: 48 eligible, 46 tested, 2 explicit non-applicable, 866 passed, 0 failed |
| Whole-system validation | PASS | `qa/WHOLE_SYSTEM_VALIDATION.json`: 21 test cases, 11 scenario classes, exact node IDs |
| Branch coverage | PASS measured | `qa/CURRENT_COVERAGE_RESULTS.json` and `qa/coverage/` |
| Runtime Strong QA | PASS local | `scripts/run_runtime_strong_qa.sh` returned exit code 0 in this sandbox |
| Research Scope Lock | PASS local | `scripts/check_research_scope_lock.py` returned exit code 0 |
| Autonomous-growth contract | PASS local | `scripts/check_autonomous_growth_contract.py` returned exit code 0 |
| Public tree scan | PASS | `scripts/scan_public_tree.py` |
| Sensitive material scan | PASS | `scripts/scan_sensitive_material.py` and `qa/SENSITIVE_MATERIAL_SCAN.json` |

## GitHub workflow applicability

The repository's `Quality` workflow was extended to include `review/aion-astra-whole-system-completion-v2` push events. The final handoff records its exact GitHub Actions run ID and head SHA only after the v2 branch is pushed and the workflow reaches a terminal conclusion.

`Research Workbench CI` is configured to run on pushes to `review/four-domain-research-materialization`, on pull requests targeting that formal research branch, or by manual dispatch. A push to the v2 review branch is therefore **not automatically in scope** for that workflow. The v2 branch locally runs the same relevant research-lab package/test checks where applicable, but no GitHub Research Workbench run is claimed unless an exact run is actually dispatched and completed.

`Research Scope Lock` has the same branch-specific push behavior, with PR targets including `main` and the formal research branch. Local checks pass; GitHub run applicability is recorded as exact non-applicability for a standalone v2 branch push unless manually dispatched.

`Runtime Strong QA` is PR/path-filtered. Its repository driver passed locally. No GitHub run is represented as PASS without an exact run ID and head SHA.

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
```
