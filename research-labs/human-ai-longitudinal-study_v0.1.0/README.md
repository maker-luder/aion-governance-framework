# Human-AI longitudinal study harness v0.1.0

Status: `IMPLEMENTED_EXPERIMENTAL_HARNESS / SCIENTIFIC_HOLD`

This package turns the controlled study designs in the 2026-09-11 longitudinal
grounding and interaction-knowledge-density notes into typed, fail-closed
engineering records. It records conditions, exact run configuration, metric
evidence and preregistered contrasts. It does not call a model, store a private
transcript, infer product-internal mechanisms or decide whether a hypothesis is
true.

The harness is a study-design surface, not a canonical evidence schema. A later
evidence claim must still pass the repository's canonical evidence admission
protocol. PR #91 is not a dependency; after it lands, records produced here may be
adapted to its admission view through a separately reviewed mapping.

All condition fields require exact runtime enum instances; raw strings fail
closed. Contrasts hold evaluator identity/source and held-out status fixed.
`task_domain` and `ai_support` remain recordable labels but cannot be declared as
v0.1.0 manipulations because no exact underlying task/support binding is present.

Key boundaries:

```text
HARNESS_PASS != HYPOTHESIS_CONFIRMED
METRIC_DELTA != CAUSAL_IDENTIFICATION
MEMORY_RETRIEVAL != LEARNING
LONGITUDINAL_ADAPTATION != SUBJECTIVITY
POLICY_SWITCHING_BEHAVIOR != INTERNAL_POLICY_MODULE_PROVEN
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

The fixture in `fixtures/minimal_contrast.json` is synthetic protocol data. It
contains no raw conversation and no third-party identity.
