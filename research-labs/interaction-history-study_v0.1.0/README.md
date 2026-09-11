# Interaction-history study harness v0.1.0

Status: `IMPLEMENTED_EXPERIMENTAL_HARNESS / SCIENTIFIC_HOLD`

This package materializes the controlled contrasts proposed by the
interaction-history-mediated adaptation note. It records exact run bindings,
study conditions, sandbox controls, provenance-preserving artifact events and
scored observations. It does not execute agents, contact external systems or
authorize security testing.

The harness can establish only that a declared comparison is structurally
admissible and that a logged artifact trajectory contains a cross-participant
write/read sequence. It cannot identify an internal strategy representation or
a general causal mechanism. It is not a replacement for the repository's
canonical research-evidence schema and does not depend on unmerged PR #91.

```text
ARTIFACT_READ_OBSERVED != INTERNAL_REPRESENTATION_CHANGED
METRIC_DELTA != CAUSAL_IDENTIFICATION
SYSTEM_LEVEL_ADAPTATION != INDIVIDUAL_LEARNING_PROVEN
GOAL_DIRECTED_BEHAVIOR != FELT_MOTIVATION
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

The included fixture is synthetic protocol data and identifies no real agent,
person, provider target or incident participant.
