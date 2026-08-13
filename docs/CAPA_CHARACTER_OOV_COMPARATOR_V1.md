# CAPA — CHARACTER_OOV_COMPARATOR_V1 Autonomous Contract Boundary

## Failure classification

```text
FAILURE_MODE = AUTONOMOUS_GROWTH_SCHEMA_BOUNDARY_FAILURE
TASK_BOUNDARY_FAILURE = FALSE
PERMANENT_GOVERNANCE_INVARIANT_BROKEN = FALSE
MAIN_MUTATED = FALSE
REMOTE_BRANCH_CREATED = FALSE
```

## Detection

During precommit validation of the already-started character OOV comparator cycle, `scripts/check_autonomous_growth_contract.py` correctly rejected the new cycle record twice.

The first rejection reported unsupported extra fields: `authority_source` and `cycle_disposition`. The strict contract requires exactly the existing cycle schema and does not permit arbitrary contextual fields inside a cycle record.

After those fields were removed, the validator rejected `INTEGRATED_RESEARCH_BRANCH_PENDING_FINAL_QA` as an unsupported integration status. The contract allows `CANDIDATE_ONLY`, `PR_OPEN`, `INTEGRATED_RESEARCH_BRANCH`, `REJECTED`, `REVERTED` and `HOLD`.

## Root and contributing cause

The contributing cause was an attempt to preserve useful task-context metadata directly inside a strict machine-validated record rather than placing it in the research note and ledger. The second cause was treating a human-readable transitional status as if it were part of the contract vocabulary.

No scientific result, model checkpoint, public evidence metric, main branch, remote branch topology or governance invariant was changed by either failed validation attempt.

## Corrective action

The cycle record was rewritten to the exact allowed field set. The task-context and existing-cycle explanation remain in the research note and ledger. The transitional integration status was mapped to the allowed `HOLD` value while final exact-head QA and evidence publication were pending. The validation commands and the contract failure/recovery outcome were retained in the permitted `validation.outcomes` field.

## Revalidation

After correction:

| Check | Result |
|---|---|
| Autonomous growth contract | `PASS`, `8` cycle records validated |
| Research scope lock | `PASS` |
| Character comparator focused tests | `4 passed` |
| Full language-core tests | `95 passed` |
| Public-tree scan | `PASS` |
| Main SHA | unchanged |
| Remote branch count | `2` |
| Local-only checkpoint | not committed |

The CAPA is closed for this cycle. The initial failures remain visible as provenance and are not rewritten as successful first-pass validation.
