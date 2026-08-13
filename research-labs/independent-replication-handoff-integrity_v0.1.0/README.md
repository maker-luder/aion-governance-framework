# Independent Replication Handoff Integrity v0.1.0

Status: `RESEARCH_ONLY / MANIFEST_AUDIT_ONLY / REPLICATION_EXECUTED=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a handoff contract distinguish a complete replication-package manifest from an actual replication result, while checking artifact identity, environment and dependency provenance, access, licensing, independence attestation, blinding metadata, and same-artifact versus independently recreated-artifact mode?

The Turing Way distinguishes reproducibility from replicability and notes that terminology varies across communities.[1] In one computational framing, an independent group can use the author's artifacts under the same setup, while independently developed artifacts under a different setup represent a different evidentiary mode. The FAIR vocabulary provides a metadata-oriented aid for findability, accessibility, interoperability, and reuse, but field presence alone does not prove FAIR compliance.[2]

This module audits a handoff manifest only. It does not run code, access data, perform a replication, observe an outcome, or certify a scientific result.

## Decision layers

| Layer | Values | Meaning |
|---|---|---|
| Handoff status | `COMPLETE`, `INDETERMINATE`, `INVALID` | Whether the manifest is complete, incomplete/uncertain, or internally contradictory. |
| Disposition | `ADMISSIBLE_FOR_REPLICATION_REVIEW`, `HOLD` | Whether the package can enter a replication review; it is not a replication outcome. |
| Artifact mode | `SAME_ARTIFACT`, `INDEPENDENT_RECREATION` | Whether the receiving group uses the source artifact or independently recreates it. |

A complete handoff is merely **admissible for review**. It does not establish that the receiving group ran the artifact, reproduced a result, replicated a finding, or obtained a consistent effect.

## Experiment results

The eight synthetic cases were complete same-artifact, complete independent-recreation, missing dependency lock, restricted access, license conflict, same-team independence, execution-reference collision, and independent-recreation source-reference missing.

| Case | Status | Disposition | Reason |
|---|---|---|---|
| Complete same artifact | `COMPLETE` | `ADMISSIBLE_FOR_REPLICATION_REVIEW` | `HANDOFF_MANIFEST_COMPLETE` |
| Complete independent recreation | `COMPLETE` | `ADMISSIBLE_FOR_REPLICATION_REVIEW` | `HANDOFF_MANIFEST_COMPLETE` |
| Missing dependency lock | `INDETERMINATE` | `HOLD` | `HANDOFF_MANIFEST_INCOMPLETE` |
| Restricted access | `INDETERMINATE` | `HOLD` | `HANDOFF_ACCESS_INCOMPLETE` |
| License conflict | `INVALID` | `HOLD` | `LICENSE_COMPATIBILITY_UNRESOLVED` |
| Same-team independence | `INVALID` | `HOLD` | `INDEPENDENCE_ATTESTATION_CONTRADICTORY` |
| Execution-reference collision | `INVALID` | `HOLD` | `INDEPENDENT_EXECUTION_REF_COLLIDES_WITH_SOURCE_ARTIFACT` |
| Recreation source missing | `INDETERMINATE` | `HOLD` | `INDEPENDENT_RECREATION_SOURCE_REFERENCE_MISSING` |

The 13 unit tests and eight experiment cases passed. Every result records `replication_result = NOT_EVALUATED`, `replication_executed = false`, `scientific_conclusion = NOT_ESTABLISHED`, `canonical_effect = NONE`, and `deployment = false`.

## Hypotheses and falsifiers

`H1`: A handoff cannot be admissible when required artifact, input, output-schema, environment, dependency, independence, or expected-output references are missing.

`H2`: Access or license incompatibility produces `HOLD` rather than an inferred replication result.

`H3`: A same-team or source-artifact-colliding independence attestation is contradictory and cannot establish independent handoff readiness.

`H4`: Same-artifact and independently recreated-artifact modes remain explicit and are not silently conflated.

A falsifier would be an `ADMISSIBLE_FOR_REPLICATION_REVIEW` result for a missing dependency/access/license/independence field, a `COMPLETE` result for a source-artifact collision, or any replication execution/outcome side effect.

## Run

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_handoff_experiment.py --output fixtures/handoff_result.json
```

## Non-claims and invariants

```text
HANDOFF_COMPLETE != REPLICATION_EXECUTED
ADMISSIBLE_FOR_REPLICATION_REVIEW != REPLICATION_RESULT
SAME_ARTIFACT != INDEPENDENT_RECREATION
MANIFEST_FIELDS != FAIR_COMPLIANCE_CERTIFICATION
REPLICATION_EXECUTED = FALSE
REPLICATION_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## References

[1]: https://book.the-turing-way.org/reproducible-research/overview/overview-definitions/ "The Turing Way — Definitions"
[2]: https://www.go-fair.org/fair-principles/ "GO FAIR — FAIR Principles"
[3]: https://worldbank.github.io/wb-reproducible-research-repository/reproducibility_package_checklist.html "World Bank — Reproducibility Package Checklist"
