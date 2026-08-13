# Factorial Execution Integrity Research Checkpoint

Date: 2026-08-13

## Classification

This is a **research-only metadata mechanism check**. It audits whether a declared full-factorial execution trace accounts for planned cells, terminal states, attrition, deviations, and reported outcomes. It does not execute AION/Astra models, estimate factor effects, fit a statistical model, or establish a scientific conclusion.

```text
PLANNED_CELL != EXECUTED_CELL
EXECUTED_CELL != VALID_RESULT
EXCLUDED_CELL != DELETED_EVIDENCE
FAILED_CELL != NEGATIVE_SCIENTIFIC_RESULT
REPORTING_COMPLETENESS != SCIENTIFIC_VALIDITY
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

## Prior-art transformation

NIST's full-factorial methods example enumerates factor-level cells and shows how execution order can confound factor effects with environmental conditions, motivating explicit cell and order metadata.[1] NIH reporting guidance emphasizes transparent methods, replicate distinction, randomization/blinding/sample-size reporting, exclusion criteria, omitted results, and disclosure of unsupported results.[2] EQUATOR/CONSORT 2025 supplies a competing reporting-framework analogy for complete flow and deviation accounting, not a validity standard for this repository.[3] [4]

The clean-room transformation is limited to metadata: expected factorial cell identity, preregistration/protocol/randomization references, cell-level state, deviation reference/reason, outcome state/reference, replicate identity, and an outcome-lock sequence. No scientific effect is computed.

## Results

The module passed **18 pytest tests** and **14 synthetic cases**. A complete trace may contain positive, negative, null, indeterminate, failed, aborted, or excluded cells as long as all expected cells are accounted for and attrition has explicit deviations. Missing/under-replicated cells remain partial. Planned/attempted/unreported cells are nonterminal. Completed cells without outcomes are held. Post-outcome cell addition, duplicate execution identifiers, out-of-domain cells, incomplete design metadata, and boundary requests are invalid or indeterminate.

The initial fixture failure is retained in `factorial-execution-initial-failure.md`: the collision test accidentally omitted the original `run:1`, so the mechanism correctly returned `COMPLETE`; the fixture was corrected to include the actual duplicate.

## Exact-head QA and repository state

| Item | Result |
|---|---|
| `TESTED_HEAD` | `64e1ea712b892c7535c0778da6492feec0d7f5e7` |
| `RECEIPT_HEAD` | `2ae477bef808dac4fac282cb273e132bbc7ec152` |
| `REPORTING_HEAD` | `2ae477bef808dac4fac282cb273e132bbc7ec152` |
| Local/reporting head before this report | `d384e3e9bb8c01ea9e93e73c61fa032074462e93` |
| Last independently verified remote research head | `bf23594f1c78c7a037ba3929edf6c6f1ae21c10a` |
| Last independently verified current remote main | `abb6550abfacb4fabc53ec04fca783bcc34acfdb` |
| Eligible targets | 69 |
| Tested targets | 66 |
| Non-applicable targets | 3 |
| Total passed | 1210 |
| Total failed | 0 |
| Strict IQC | PASS; expected targets 69 |
| Current-head/source binding | PASS |
| Branch-native coverage | PASS; 66 targets |
| Evidence traceability/reconciliation | PASS; acceptance remains `NOT_EVALUATED` |
| Runtime Strong QA | PASS |

`TESTED_HEAD` is the exact source state used for final QA execution. `RECEIPT_HEAD` and `REPORTING_HEAD` are later receipt commits and are not the tested execution head. The report commit and operational record remain reporting state until a normal push is independently confirmed.

## Limitations and non-claims

A complete execution ledger does not prove that a run was valid, randomized, powered, unbiased, reproducible, or causally informative. It does not verify the truth of a positive, negative, null, or indeterminate label. It does not establish AION/Astra equivalence, identity continuity, subjectivity, consciousness, governance effect, canonical effect, or deployment.

## References

[1]: https://www.itl.nist.gov/div898/handbook/pri/section3/pri3332.htm "NIST — Full factorial example"
[2]: https://grants.nih.gov/policy-and-compliance/policy-topics/reproducibility/principles-guidelines-reporting-preclinical-research "NIH — Principles and Guidelines for Reporting Preclinical Research"
[3]: https://www.equator-network.org/reporting-guidelines/consort/ "EQUATOR Network — CONSORT reporting guidelines"
[4]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11995452/ "CONSORT 2025 explanation and elaboration"
