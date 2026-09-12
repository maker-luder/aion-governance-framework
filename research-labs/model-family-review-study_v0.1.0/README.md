# Model-family review study harness v0.1.0

Status: `IMPLEMENTED_EXPERIMENTAL_HARNESS / SCIENTIFIC_HOLD`

This package implements the bounded record-and-audit seam proposed by the
[model-family review compatibility hypothesis](../../docs/research/MODEL_FAMILY_REVIEW_COMPATIBILITY_HYPOTHESIS_2026_09_12.md).
It records frozen repository state, review task, prompt, file scope, tool access,
budget, rubric, preregistration, reviewer product labels, session-isolation
evidence, scored observations and evaluator provenance. It does not invoke a
model, conduct a comparison, score outputs, or admit a scientific claim.

In v0.1.0, `provider_relation` is derived from exact reviewer-provider and
repository-formalization-provider IDs and may be used as a manipulation.
`family_relation` is recordable only as `UNKNOWN`, `CANDIDATE_RELATED`, or
`CANDIDATE_DIFFERENT`; a candidate label requires structural evidence references,
and the field cannot be manipulated because commercial model lineage is not
machine-verifiable here. A reference is a structural pointer, not authenticated
proof of lineage.

Contrasts fail closed on repository commit/tree, task, prompt, file scope, tool,
budget, rubric, preregistration, runtime, evaluator, metric-unit, or held-out drift.
They require different reviewers and exact runtime enum/bool values. Admission
also requires a non-empty session-isolation reference and an exact declaration
that prior project memory is absent. The harness cannot verify a provider's hidden
routing, weights, system instructions, memory subsystem, or internal model family.

```text
PROVIDER_RELATION != MODEL_FAMILY_IDENTITY
CANDIDATE_FAMILY_LABEL != VERIFIED_LINEAGE
HIGH_COMPATIBILITY != INDEPENDENT_VALIDATION
LOWER_SEMANTIC_FRICTION != HIGHER_TRUTH
REVIEW_FIDELITY != CLAIM_TRUTH
METRIC_DELTA != CAUSAL_IDENTIFICATION
HARNESS_PASS != HYPOTHESIS_CONFIRMED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

The included fixture contains synthetic protocol metadata only. It contains no
private transcript, third-party identity, external reviewer output, or experiment
result.
