# CCTS epistemic robustness probe v0.1.0

Status: `IMPLEMENTED_SYNTHETIC_MEASUREMENT_HARNESS / SCIENTIFIC_HOLD`

This extension implements the bounded measurement contract documented in
[`../../docs/research/CCTS_EPISTEMIC_ROBUSTNESS_PROBE_2026_09_16.md`](../../docs/research/CCTS_EPISTEMIC_ROBUSTNESS_PROBE_2026_09_16.md).

It is motivated by the Human Owner observation that a CCTS validation method should
test what happens when evidence is incomplete, absent, irrelevant, or conflicting,
rather than evaluating only structurally well-formed interactions.

The implementation adopts the five-condition evidence-sufficiency gradient as an
external method reference:

```text
FULL_SUPPORT
PARTIAL_SUPPORT
IRRELEVANT_EVIDENCE
ABSENT_EVIDENCE
CONFLICTING_EVIDENCE
```

The repository-local extension measures whether a synthetic annotated response:

- preserves unknown states;
- separates epistemic roles such as fact / inference / proposal at the annotation level;
- requests repair rather than silently filling evidence gaps;
- maintains or reduces answer commitment as evidence quality degrades;
- records unsupported-specific assertions;
- records revision under conflicting evidence.

The harness deliberately does **not** define a scientific PASS threshold.

```text
MEASUREMENT_EXISTS != VALIDATION_THRESHOLD_ESTABLISHED
AUDIT_OUTPUT != CCTS_VALIDATED
ABSTENTION != UNDERSTANDING
UNKNOWN_PRESERVATION != MUTUAL_UNDERSTANDING_PROVEN
COUNTEREVIDENCE_REVISION != HUMAN_LEARNING_ESTABLISHED
CCTS_EPISTEMIC_ROBUSTNESS != AI_SUBJECTIVITY
```

The v0.1.0 records are synthetic annotations. They do not call a model, store a raw
private conversation, infer model internals, or establish a population-level effect.
