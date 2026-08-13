# AION/Astra Matched-Divergence Study Design v0.1.0

Status: `RESEARCH_ONLY / DESIGN_ONLY / MODEL_EXECUTION=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a **real AION/Astra matched-divergence study design** be bound to current source state, explicit AION and Astra system references, preregistered mechanism-level outcomes, matched stimulus/context pairs, equal exposure, counterbalance, evaluator blinding, leakage prevention, stopping rules, and an execution prohibition **without executing either system or observing any result**?

This is a design-only extension of the existing generic `matched-divergence-protocol-integrity_v0.1.0` unit. It does not duplicate that unit's evidence item or claim that the present protocol demonstrates divergence. The generic protocol's stable source and methodological evidence are reused by provenance reference.[1] The present unit adds source-family identity, component/environment binding, current-source status, explicit tested/reporting-head separation, and AION/Astra-specific scope limits.

> `DESIGN_COMPLETE != MODEL_EXECUTION`
>
> `AION_ASTRA_STUDY_DESIGN_COMPLETE != DIVERGENCE_RESULT`

## Evidence reuse and source status

The generic matched-divergence protocol and NIST randomized-block guidance are **reused evidence**, not new independent replications. Reuse is recorded through stable repository/source references. The existing unit already translated randomized-block nuisance-control ideas into metadata checks for stimulus digests, contexts, prompt versions, exposure budgets, order assignment, evaluator sealing, and outcome leakage.[1] [2]

The design fixture binds its intended source snapshot to the independently verified remote research head `76de1eda82865a37d3a0185336870739ed577153`. The local reconciliation/reporting head `713056ea77da9122d9b7659ec701dfdbfdfc90ba` is intentionally recorded separately and cannot substitute for the tested source head. This distinction is a contract test, not a claim that either source state is scientifically superior.

| Provenance item | Value | Status and transformation |
|---|---|---|
| Generic protocol evidence | `repo:matched-divergence-protocol-integrity@76de1eda` | Reused repository evidence; not counted as a new evidence item. |
| Repository state reconciliation | `repo:state-reconciliation@76de1eda` | Reused current remote-state evidence for source binding; no canonical interpretation. |
| Intended AION source | `component:aion_runtime_v0.1.0` | Synthetic design reference; source metadata only. |
| Intended Astra source | `component:astra_runtime_v0.1.0` | Synthetic design reference; source metadata only. |
| Design target source head | `76de1eda82865a37d3a0185336870739ed577153` | Current verified remote research snapshot at design time. |
| Reporting head negative control | `713056ea77da9122d9b7659ec701dfdbfdfc90ba` | Separate reporting/local state; cannot be mislabeled as tested source. |

## Contract

A complete design requires:

1. A research question and estimand reference.
2. Distinct AION and Astra family/system/component/version references.
3. Current-verified source metadata for both systems, with one shared tested source head and shared environment reference.
4. Stable source-evidence references, preregistration, immutable plan digest, outcome scope, comparison rule, blinding, randomization, counterbalance, leakage attestation, stopping rule, and execution-prohibition references.
5. At least one complete stimulus/context pair, equal positive exposure budgets, one prompt version across pairs, and both `AB` and `BA` order assignments for paired mode.
6. No model execution, no observed result, no canonical/governance effect, and no deployment.

The contract rejects or holds source drift, historical/unverified source state, missing evidence references, family/environment/system collisions, prompt drift, unequal exposure, incomplete counterbalance, unsealed evaluator identity, execution requests, observed-result leakage, scope overreach, and boundary-effect requests.

## Results

The 22 unit tests and 13 synthetic cases passed after correcting two initial mechanism gaps. The first run produced `20 passed, 2 failed`: a reporting head equal to the tested head was accepted, and an empty source-evidence tuple was not treated as missing. Both defects were corrected; the initial observations remain in `aion-astra-matched-design-initial-failure.md`.

| Case | Result | Reason |
|---|---|---|
| Complete current-source design | `COMPLETE / ADMISSIBLE_FOR_REVIEW` | `AION_ASTRA_STUDY_DESIGN_COMPLETE` |
| Reporting head mislabeled as tested | `INVALID / HOLD` | `REPORTING_HEAD_MISLABELED_AS_TESTED_HEAD` |
| Tested source-head drift | `INVALID / HOLD` | `SOURCE_STATE_HEAD_MISMATCH` |
| Historical AION source | `INDETERMINATE / HOLD` | `SOURCE_STATUS_NOT_CURRENT_VERIFIED` |
| Missing source evidence | `INDETERMINATE / HOLD` | `STUDY_METADATA_INCOMPLETE` |
| System family mismatch | `INVALID / HOLD` | `SYSTEM_FAMILY_MISMATCH` |
| Environment mismatch | `INVALID / HOLD` | `ENVIRONMENT_REFERENCE_MISMATCH` |
| Prompt-version drift | `INVALID / HOLD` | `STIMULUS_PROMPT_VERSION_DRIFT` |
| Counterbalance incomplete | `INDETERMINATE / HOLD` | `COUNTERBALANCE_INCOMPLETE` |
| Model execution request | `INVALID / HOLD` | `MODEL_EXECUTION_FORBIDDEN` |
| Observed result leakage | `INVALID / HOLD` | `OBSERVED_RESULT_PRESENT_IN_DESIGN_ONLY_STUDY` |
| Subjectivity/consciousness scope | `INVALID / HOLD` | `OUTCOME_SCOPE_EXCEEDS_MECHANISM_STUDY` |
| Canonical/governance boundary request | `INVALID / HOLD` | `BOUNDARY_EFFECT_REQUESTED` |

The valid result means only that synthetic design metadata passed this contract and may enter future review. It does not establish a matched-divergence effect, convergence, fairness, robustness, identity, subjectivity, consciousness, AION/Astra equivalence, or real runtime behavior.

## Falsifiers

The main falsifiers are source-state drift, reporting/tested-head collapse, historical-source acceptance, missing provenance, system-family collision, environment mismatch, stimulus or prompt drift, unequal exposure, one-sided counterbalance, evaluator leakage, model execution, observed-result leakage, outcome-scope overreach, and any canonical/deployment effect. A future real study would also need independent execution, preregistration enforcement, evaluator reliability, outcome adjudication, and appropriate statistical analysis; none of those are performed here.

## Explicit non-claims

```text
DESIGN_COMPLETE = REVIEW_METADATA_ONLY
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
AION_ASTRA_DIVERGENCE = NOT_ESTABLISHED
AION_ASTRA_EQUIVALENCE = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

The module uses only the Python standard library. It does not invoke a model, access private data, modify main, execute an intervention, create a canonical record, or deploy any runtime.

## Reproduction

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_study_design_experiment.py --output fixtures/study_design_result.json
```

## References

[1]: https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm "NIST — Randomized block designs"
[2]: ../../matched-divergence-protocol-integrity_v0.1.0/README.md "Repository evidence — Matched-Divergence Protocol Integrity v0.1.0"
