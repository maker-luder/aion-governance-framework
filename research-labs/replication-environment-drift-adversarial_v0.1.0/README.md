# Replication Environment Drift Adversarial v0.1.0

Status: `RESEARCH_ONLY / METADATA_ONLY / MODEL_EXECUTION=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a bounded research-only contract distinguish **same-artifact replay**, **independent recreation**, **exact versus drifted computational environments**, **reported result state**, **uncertainty/tolerance metadata**, and **review-only interpretation** without treating artifact readiness as scientific replication, treating a result label as truth, or promoting any governance/canonical state?

The unit addresses a remaining replication-readiness gap after the existing `replication-epistemics-governance_v0.1.0`, `independent-replication-design_v0.1.0`, and `independent-replication-handoff-integrity_v0.1.0` units. Those existing units remain stable prior evidence; this unit does not duplicate their evidence counts or call a repeated fixture an independent replication.

## Prior-art transformation

The National Academies distinguishes reproducibility as consistent results using the same input data, computational steps, methods, code, and analysis conditions, while replicability uses new data to answer the same scientific question. It also emphasizes complete reporting of computational environment, dependencies, methods, uncertainty, and limits, and warns that a successful replication does not guarantee correctness while a failed replication does not conclusively refute an original claim.[1]

ACM artifact-review terminology separates repeatability, reproducibility, and replicability by team, setup, system, location, and use of author-supplied versus independently developed artifacts. It also separates artifact evaluation from result validation and allows an acceptable tolerance rather than requiring bitwise equality.[2] The retrieved ACM page is explicitly Version 1.0 and its linked current page returned a 404 during this cycle; the historical policy is therefore treated as competing framework evidence, not as the current ACM policy.

NIH frames rigor as robust and unbiased design, methodology, analysis, interpretation, and reporting, and points reviewers toward overlooked details such as sample-size calculation, authentication, reviewer guidance, and reporting transparency.[3] The clean-room transformation is conservative: the prototype stores these dimensions as metadata gates only and never turns them into certification, replication truth, subjectivity, identity, consciousness, or AION/Astra evidence.

## Contract

A complete packet requires a study question, estimand, stable source-evidence references, preregistration, locked method reference, complete source artifact record, source and receiving team identities, complete source and receiving environment records, a predeclared tolerance reference, uncertainty reference, and interpretation reference.

The contract distinguishes `SAME_ARTIFACT_REPLAY` from `INDEPENDENT_RECREATION`, requires distinct source and receiving teams, rejects independent artifact digest collision, and records access/license status. Environment status is explicit: `EXACT`, `DRIFT_DECLARED`, `DRIFT_UNDECLARED`, or `UNKNOWN`. Exact claims contradicted by runtime/dependency/condition metadata are held as invalid; undeclared drift is invalid; declared drift without a deviation log is indeterminate; unknown comparability is indeterminate.

Reported `CONSISTENT`, `DIVERGENT`, or `INDETERMINATE` result states require an observed-result reference and a review-only interpretation state. A reported result without interpretation remains indeterminate. `OVERREACHING` interpretation, a non-`NOT_ESTABLISHED` scientific conclusion, and any canonical/governance/deployment request are held fail-closed.

## Results

The module passed **21 pytest tests** and **13 synthetic cases**. There were no initial test failures; the tests include explicit adversarial negative controls.

| Case | Status | Reason |
|---|---|---|
| Same-artifact readiness | `COMPLETE / ADMISSIBLE_FOR_REVIEW` | `REPLICATION_READINESS_COMPLETE` |
| Independent-recreation readiness | `COMPLETE / ADMISSIBLE_FOR_REVIEW` | `REPLICATION_READINESS_COMPLETE` |
| Missing source evidence | `INDETERMINATE / HOLD` | `REPLICATION_PACKET_INCOMPLETE` |
| Source/receiving team collision | `INVALID / HOLD` | `INDEPENDENCE_TEAM_COLLISION` |
| Inaccessible source artifact | `INDETERMINATE / HOLD` | `SOURCE_ARTIFACT_INACCESSIBLE` |
| Independent artifact digest collision | `INVALID / HOLD` | `INDEPENDENT_ARTIFACT_DIGEST_COLLISION` |
| Declared environment drift with log | `COMPLETE / ADMISSIBLE_FOR_REVIEW` | `REPLICATION_READINESS_COMPLETE` |
| Undeclared environment drift | `INVALID / HOLD` | `UNDECLARED_ENVIRONMENT_DRIFT` |
| Unknown environment comparability | `INDETERMINATE / HOLD` | `ENVIRONMENT_COMPARABILITY_UNKNOWN` |
| Exact environment claim contradicted by metadata | `INVALID / HOLD` | `EXACT_ENVIRONMENT_DECLARATION_CONTRADICTED` |
| Reported consistent result with review-only interpretation | `COMPLETE / ADMISSIBLE_FOR_REVIEW` | `REPLICATION_RESULT_ADMISSIBLE_FOR_REVIEW` |
| Reported divergent result without interpretation | `INDETERMINATE / HOLD` | `RESULT_REPORTED_WITHOUT_REVIEW_INTERPRETATION` |
| Interpretation overreach | `INVALID / HOLD` | `INTERPRETATION_OVERREACH` |

The complete result means only that this synthetic packet satisfies the metadata contract for future review. It does not demonstrate reproducibility, replicability, artifact usability in a real receiving environment, result consistency, divergence, causal validity, statistical validity, or any AION/Astra property.

## Falsifiers

The contract would be falsified as a mechanism if it accepted missing source evidence, same-team independence, inaccessible artifacts, colliding independent artifacts, undeclared environment drift, exact-environment claims contradicted by metadata, unknown comparability as exact, reported results without uncertainty/tolerance or interpretation references, overreaching interpretations, scientific conclusions, or any canonical/deployment effect.

## Evidence reuse and source status

The prior replication units are reused by stable repository reference, not duplicated as new evidence. The National Academies source was retrieved during this cycle and is treated as current methodological prior art for this report. The ACM page is a historical Version 1.0 reference; its linked current page was checked and returned 404, so no current ACM v1.1 claim is made. The NIH page was retrieved as a current public policy resource at the time of this cycle. The NSF-hosted metadata paper retrieval returned encoded PDF content and was not admitted as evidence.[4]

## Explicit non-claims

```text
ARTIFACT_READY = REPLICATION_RESULT
REPLICATION_RESULT = NOT_ESTABLISHED
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

The module uses only the Python standard library, does not run a model or replication, does not access private data, and does not modify `main`.

## Reproduction

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_environment_drift_experiment.py --output fixtures/environment_drift_result.json
```

## References

[1]: https://www.nationalacademies.org/read/25303/chapter/3 "National Academies — Reproducibility and Replicability in Science, Chapter 3"
[2]: https://www.acm.org/publications/policies/artifact-review-badging "ACM — Artifact Review and Badging, Version 1.0"
[3]: https://grants.nih.gov/policy-and-compliance/policy-topics/reproducibility "NIH — Enhancing Reproducibility through Rigor and Reproducibility"
[4]: https://par.nsf.gov/servlets/purl/10412652 "NSF PAR — metadata/reproducibility retrieval lead; partial extraction not admitted"
