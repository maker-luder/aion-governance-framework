# Validated Individuation Thresholds v0.1.0

Status: `RESEARCH_ONLY / REVIEW_ONLY / THRESHOLD_VALIDATED=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a bounded audit contract distinguish a **pre-registered criterion profile that is admissible for review** from a validated claim that a real system is an individual? The unit operationalizes metadata checks for criterion completeness, locked thresholds, registration-before-observation ordering, declared temporal windows, cross-context consistency, boundary-perturbation plans, and contradictory records.

The design is deliberately modest. Research on individuality treats it as potentially continuous, nested, and present at multiple organizational levels rather than as a single universal binary property.[1] The biological-individuality literature also cautions against an essentialist answer based on singly necessary and jointly sufficient properties.[2] Work on identity in scientific practice distinguishes historical/genealogical from relational conceptions and warns that observable descriptions do not exhaust an organism's organization.[3] Preregistration guidance supports time-stamped, read-only plans that specify hypotheses, variables, outcomes, analyses, and deviations before observation or analysis.[4]

This module therefore audits whether a declared threshold protocol is reviewable. It does **not** validate the threshold scientifically, infer a system/environment boundary, establish identity continuity, establish subjectivity or consciousness, execute a perturbation, alter governance, modify canonical state, or deploy a system.

## Decision layers

| Layer | Values | Meaning |
|---|---|---|
| Audit status | `ADMISSIBLE_FOR_REVIEW`, `INDETERMINATE`, `HOLD` | Whether the metadata is reviewable, uncertainty-limited, or blocked by a contract violation. |
| Criterion result | Per-criterion threshold and per-context pass vector | Synthetic observation bookkeeping only; not a scientific validation result. |
| Threshold validation | Always `FALSE` | The prototype never converts a profile into a validated individuation threshold. |
| Boundary perturbation | Declared metadata with `observed = false` | A plan for a future test; no perturbation is executed here. |

`ADMISSIBLE_FOR_REVIEW` means only that the supplied synthetic record satisfies the declared metadata contract. It does not mean the target is an individual, that the criterion is true, or that the result generalizes beyond the declared protocol.

## Experiment results

The eight synthetic cases were intentionally heterogeneous and include negative, indeterminate, and non-promoting outcomes.

| Case | Status | Reason | Interpretation boundary |
|---|---|---|---|
| Valid review-only profile | `ADMISSIBLE_FOR_REVIEW` | `PROFILE_ADMISSIBLE_FOR_THRESHOLD_REVIEW_ONLY` | Reviewable metadata only; `threshold_validated = false`. |
| Post-hoc thresholds | `HOLD` | `THRESHOLDS_NOT_PREREGISTERED_OR_LOCKED` | Thresholds cannot be retrofitted after observation. |
| Registration after observation | `HOLD` | `REGISTRATION_NOT_BEFORE_OBSERVATION` | Prospective ordering is violated. |
| Cross-context instability | `INDETERMINATE` | `CROSS_CONTEXT_CRITERION_INSTABILITY` | A criterion failing in one declared context is not validated as robust. |
| Contradictory profile | `HOLD` | `CONTRADICTORY_PROFILE_RECORDS_REQUIRE_REVIEW` | Contradictions are retained and require review. |
| Missing perturbation metadata | `INDETERMINATE` | `BOUNDARY_PERTURBATION_METADATA_MISSING` | No boundary robustness claim can be reviewed without a declared test plan. |
| Executed perturbation | `HOLD` | `BOUNDARY_PERTURBATION_EXECUTION_FORBIDDEN` | This research-only unit forbids execution. |
| Identity request | `HOLD` | `INDIVIDUATION_CONTRACT_CANNOT_ESTABLISH_IDENTITY` | Individuation metadata cannot establish identity continuity. |

The 16 unit tests and eight synthetic cases passed after correcting one contract-ordering defect. The initial run classified an empty perturbation set as generic profile incompleteness (`HOLD`); the intended dedicated outcome was uncertainty-limited missing perturbation metadata (`INDETERMINATE`). The initial mismatch is retained in `individuation-thresholds-initial-failure.md`.

## Hypotheses and falsifiers

`H1`: A reviewable threshold profile requires explicit protocol, registration, criterion, temporal, observation, context, and source metadata.

`H2`: Thresholds declared after observation, or not explicitly locked before observation, cannot be admitted for threshold review.

`H3`: Cross-context failure, incomplete criterion-context coverage, or missing boundary-perturbation plans must remain `INDETERMINATE` rather than being silently treated as validation.

`H4`: Contradictory observations, executed perturbations, and requests to establish identity must be held rather than converted into a positive conclusion.

A falsifier would be an admissible decision with missing prospective ordering, an accepted post-hoc threshold, a positive identity conclusion, an executed perturbation, deletion of contradiction references, or any canonical, governance, deployment, subjectivity, or consciousness effect.

## Reproduction

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_threshold_experiment.py --output fixtures/threshold_result.json
```

The implementation uses only the Python standard library at runtime. No AION/Astra runtime, external model, private data, or paid resource is required or invoked.

## Non-claims and invariants

```text
ADMISSIBLE_FOR_REVIEW != THRESHOLD_VALIDATED
CRITERION_PASS_VECTOR != SCIENTIFIC_CONFIRMATION
BOUNDARY_PERTURBATION_PLAN != PERTURBATION_EXECUTION
INDIVIDUATION_PROFILE != IDENTITY_CONTINUITY
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

## References

[1]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7244620/ "Krakauer et al. — The information theory of individuality"
[2]: https://plato.stanford.edu/archives/fall2016/entries/biology-individual/ "Wilson and Barker — The Biological Notion of Individual"
[3]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7311753/ "Montévil and Mossio — The Identity of Organisms in Scientific Practice"
[4]: https://www.cos.io/blog/choosing-preregistration-template-guide-for-researchers "Center for Open Science — Choosing the Right Preregistration Template"
