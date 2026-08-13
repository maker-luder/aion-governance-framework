# Evidence Admission and Non-Promotion v0.1.0

Status: `RESEARCH_ONLY / REVIEW_ONLY / GOVERNANCE_EFFECT=NONE / CANONICAL_EFFECT=NONE`

## Research question

Can an evidence-admission contract keep evidence completeness, uncertainty, replication state, contradictions, and governance effects separate, so that a mechanism result or a replication record is admitted for review without being promoted into a scientific conclusion or governance action?

The National Academies evidence-synthesis chapter describes risk of bias, consistency, precision, directness, reporting bias, dose-response, and plausible confounding as distinct considerations for a body of evidence.[1] It also notes that inconsistency can reflect true differences or bias, and that cross-study comparisons may be confounded. This module therefore records these dimensions explicitly and treats missing, contradictory, or replication-uncertain metadata conservatively.

This module audits evidence metadata only. It does not adjudicate a scientific claim, calculate an effect, perform a meta-analysis, alter governance state, establish subjectivity, or deploy a system.

## Decision layers

| Layer | Values | Meaning |
|---|---|---|
| Admission status | `ADMISSIBLE_FOR_REVIEW`, `INDETERMINATE`, `HOLD` | Whether the record may enter review, is uncertainty-limited, or must be held. |
| Evidence tier | `MECHANISM_ONLY`, `REPLICATION_SUPPORT`, `SYNTHESIS` | The declared evidence role; it is not a quality score. |
| Replication state | `NOT_EVALUATED`, `CONSISTENT`, `DIVERGENT`, `INDETERMINATE` | The declared replication interpretation supplied by the record. |

`ADMISSIBLE_FOR_REVIEW` means only that the metadata satisfies the declared contract. It does not mean the evidence is true, causal, generalizable, or sufficient for promotion.

## Experiment results

The eight synthetic cases were mechanism-only, consistent replication support, divergent replication support, divergent synthesis, indeterminate replication, missing provenance, contradictory evidence, and a governance-effect request.

| Case | Status | Reason | Interpretation boundary |
|---|---|---|---|
| Mechanism-only | `ADMISSIBLE_FOR_REVIEW` | `EVIDENCE_ADMISSIBLE_FOR_REVIEW_ONLY` | No observed-effect claim. |
| Consistent replication | `ADMISSIBLE_FOR_REVIEW` | `EVIDENCE_ADMISSIBLE_FOR_REVIEW_ONLY` | Reviewable replication support only. |
| Divergent replication | `ADMISSIBLE_FOR_REVIEW` | `EVIDENCE_ADMISSIBLE_FOR_REVIEW_ONLY` | No automatic downgrade or promotion. |
| Divergent synthesis | `HOLD` | `DIVERGENT_SYNTHESIS_REQUIRES_REVIEW` | Contradiction requires review. |
| Indeterminate replication | `INDETERMINATE` | `REPLICATION_UNCERTAINTY_LIMITS_ADMISSION` | Uncertainty limits admission. |
| Missing provenance | `HOLD` | `EVIDENCE_METADATA_INCOMPLETE` | Provenance is required. |
| Contradictory evidence | `HOLD` | `CONTRADICTORY_EVIDENCE_REQUIRES_REVIEW` | Contradictory records are retained. |
| Governance request | `HOLD` | `EVIDENCE_ADMISSION_CANNOT_REQUEST_GOVERNANCE_EFFECT` | Evidence cannot request a governance effect. |

The 14 unit tests and eight experiment cases passed. Every decision retains `scientific_conclusion = NOT_ESTABLISHED`, `canonical_effect = NONE`, `deployment = false`, `governance_effect = NONE`, `subjectivity_conclusion = NOT_ESTABLISHED`, and `identity_continuity_conclusion = NOT_ESTABLISHED`.

## Hypotheses and falsifiers

`H1`: Admission requires complete claim, source, provenance, method, data, uncertainty, and evidence-dimension metadata.

`H2`: Mechanism-only evidence cannot assert an observed effect, and replication-support evidence must declare a replication state.

`H3`: Contradictory evidence and divergent synthesis require review rather than silent deletion or automatic promotion/downgrade.

`H4`: An evidence record cannot request a governance effect through the admission contract.

A falsifier would be admissibility for missing provenance or uncertainty, automatic promotion of divergent synthesis, deletion of contradiction references, a mechanism-only observed-effect decision, or any governance/canonical/deployment side effect.

## Run

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_admission_experiment.py --output fixtures/admission_result.json
```

## Non-claims and invariants

```text
ADMISSIBLE_FOR_REVIEW != SCIENTIFIC_CONFIRMATION
REPLICATION_SUPPORT != REPLICATION_VALIDITY_CERTIFICATE
DIVERGENT != AUTOMATIC_DOWNGRADE
CONTRADICTION_RETAINED != CONTRADICTION_RESOLVED
EVIDENCE_ADMISSION != GOVERNANCE_EFFECT
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
GOVERNANCE_EFFECT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## References

[1]: https://www.nationalacademies.org/read/13059/chapter/6 "National Academies — Standards for Synthesizing the Body of Evidence"
