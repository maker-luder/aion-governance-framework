# Human-AI longitudinal study harness v0.1.0

Status: `IMPLEMENTED_EXPERIMENTAL_HARNESS / SCIENTIFIC_HOLD`

This package turns the controlled study designs in the 2026-09-11 longitudinal
grounding and interaction-knowledge-density notes into typed, fail-closed
engineering records. It records conditions, exact run configuration, metric
evidence and preregistered contrasts. It does not call a model, store a private
transcript, infer product-internal mechanisms or decide whether a hypothesis is
true.

The harness is a study-design surface, not a canonical evidence schema. PR #91 is
now on `main` and provides the repository's provenance-to-claim quality gate. This
harness remains separate: any conversion of its study records into that claim
admission surface requires a separately reviewed mapping rather than implicit
promotion.

All condition fields require exact runtime enum instances; raw strings fail
closed. Contrasts hold evaluator identity/source and held-out status fixed.
`task_domain` and `ai_support` remain recordable labels but cannot be declared as
v0.1.0 manipulations because no exact underlying task/support binding is present.
Metric values accept exact `int` or `float` runtime values only; booleans, strings,
other types and non-finite numbers fail closed.

Key boundaries:

```text
HARNESS_PASS != HYPOTHESIS_CONFIRMED
METRIC_DELTA != CAUSAL_IDENTIFICATION
MEMORY_RETRIEVAL != LEARNING
LONGITUDINAL_ADAPTATION != SUBJECTIVITY
POLICY_SWITCHING_BEHAVIOR != INTERNAL_POLICY_MODULE_PROVEN
HARNESS_RECORD != PR91_CLAIM_ADMISSION
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

## Cross-dyad collaboration-regime extension

The bounded extension in `src/aion_human_ai_longitudinal/collaboration_regime.py`
materializes the condition matrix authorized by the exact PR #102 research
specification. The implementation branch starts from live `main` commit
`d95bc2625e71f1c85a725aaba78cb0feccfc0668`; PR #102 is an explicit unmerged
specification dependency and is **not** the implementation base.

It provides condition packets A-D plus optional closure control E, one synthetic
fixture for each of the nine specified task families, all fifteen observable
metrics as separate dimensions, matched-run validation, and a deterministic
execution receipt. It does not invoke a model or provider, collect private
transcripts, classify people, produce a subjectivity score, merge, deploy, or
write to `main`.

See
[`CROSS_DYAD_COLLABORATION_REGIME_HARNESS.md`](CROSS_DYAD_COLLABORATION_REGIME_HARNESS.md)
for the exact dependency, matrix, reproduction commands, receipt semantics, and
authority boundary.
