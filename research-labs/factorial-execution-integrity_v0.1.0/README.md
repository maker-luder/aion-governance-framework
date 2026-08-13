# Factorial Execution Integrity v0.1.0

Status: `RESEARCH_ONLY / METADATA_ONLY / MODEL_EXECUTION=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a bounded execution ledger extend a planned full-factorial completeness contract so that **planned**, **attempted**, **completed**, **failed**, **aborted**, **excluded**, and **unreported** cells remain distinguishable, attrition requires a declared deviation, negative/null/indeterminate outcomes remain preserved, and post-outcome cell addition is rejected?

The existing `factorial-completeness-contract_v0.1.0` checks the declared Cartesian design and design-level execution metadata. This unit adds a cell-level execution trace and attrition/deviation integrity layer. It does not estimate factor effects, fit a statistical model, execute AION/Astra systems, or decide whether any outcome is scientifically valid.

## Prior-art transformation

NIST's full-factorial example enumerates factor-level combinations and shows why randomizing execution order matters when environmental conditions can be confounded with factor order.[1] NIH reporting guidance asks researchers to report how often experiments were performed, distinguish independent data points from technical replicates, describe randomization/blinding/sample-size decisions, and disclose exclusions or omitted results including results that do not support the main findings.[2]

EQUATOR/CONSORT 2025 guidance emphasizes complete and transparent reporting of trial design, conduct, analysis, results, protocol deviations, and participant flow; it is used here only as a competing reporting framework for explicit attrition accounting, not as a clinical or AION/Astra standard.[3] [4]

The transformation is conservative: a complete trace means that the metadata accounts for all expected cells and terminal states; it does not mean the experiment was valid, unbiased, powered, reproducible, or scientifically informative.

## Contract

A ledger requires factors, preregistration, protocol, randomization reference, and cell-level planned/execution/provenance references. Every expected factorial cell must appear at the expected replication count. Terminal outcomes may be `POSITIVE`, `NEGATIVE`, `NULL`, or `INDETERMINATE`; these labels are preserved as observations in the synthetic trace and are never converted into a conclusion.

Failed, aborted, and excluded cells require a deviation reference and reason. `PLANNED`, `ATTEMPTED`, and `UNREPORTED` states are nonterminal and keep the ledger partial. A completed cell without an outcome reference is indeterminate. An execution planned after an outcome lock is rejected as `POST_OUTCOME_CELL_ADDITION`. Duplicate execution identifiers, out-of-domain cells, missing protocol metadata, and boundary-effect requests are held or invalid.

## Results

The module passed **18 pytest tests** and **14 synthetic cases**. The initial fixture failure is preserved in `factorial-execution-initial-failure.md`: the first collision test accidentally omitted the original `run:1`, so the model correctly returned `COMPLETE`; the fixture was corrected to include both records.

| Case | Status | Meaning |
|---|---|---|
| Complete trace with positive/negative/null/indeterminate outcomes | `COMPLETE` | Trace admissible for review; outcomes preserved |
| Missing or under-replicated cell | `PARTIAL` | No silent completeness claim |
| Failed/aborted/excluded cells with deviations | `COMPLETE` | Attrition preserved and reviewable |
| Attrition without deviation | `INDETERMINATE` | Hold for missing explanation |
| Completed cell without reported outcome | `INDETERMINATE` | Hold for incomplete result record |
| Attempted or unreported cell | `PARTIAL` | Nonterminal execution state |
| Post-outcome cell addition | `INVALID` | Rejects outcome-contingent design expansion |
| Execution ID collision | `INVALID` | Trace identity failure |
| Out-of-domain cell | `INVALID` | Cell does not belong to declared factorial space |
| Missing randomization metadata | `INDETERMINATE` | Design metadata incomplete |
| Boundary-effect request | `INVALID` | Output normalized to NONE/FALSE |

## Falsifiers

The mechanism would be falsified if it accepted a missing cell as complete, treated an unreported or attempted cell as terminal, allowed silent attrition, accepted a completed cell without an outcome record, allowed post-outcome cell addition, collapsed negative/null/indeterminate outcomes into positive findings, or emitted canonical/governance/deployment effects.

The synthetic result does not estimate factor effects, test interaction terms, establish a causal relationship, prove randomization quality, establish power, validate a real experiment, or support any AION/Astra identity, subjectivity, consciousness, governance, or deployment conclusion.

## Explicit non-claims

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
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

The module uses only the Python standard library. It does not run a model, query private data, alter `main`, or change canonical state.

## Reproduction

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_execution_experiment.py --output fixtures/execution_result.json
```

## References

[1]: https://www.itl.nist.gov/div898/handbook/pri/section3/pri3332.htm "NIST Engineering Statistics Handbook — Full factorial example"
[2]: https://grants.nih.gov/policy-and-compliance/policy-topics/reproducibility/principles-guidelines-reporting-preclinical-research "NIH — Principles and Guidelines for Reporting Preclinical Research"
[3]: https://www.equator-network.org/reporting-guidelines/consort/ "EQUATOR Network — CONSORT reporting guidelines"
[4]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11995452/ "CONSORT 2025 explanation and elaboration"
