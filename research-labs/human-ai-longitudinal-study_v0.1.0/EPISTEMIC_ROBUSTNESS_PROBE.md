# CCTS epistemic robustness probe v0.1.0

Status: `IMPLEMENTED_SYNTHETIC_MEASUREMENT_HARNESS / SCIENTIFIC_HOLD`

This extension implements the bounded measurement contract documented in [`../../docs/research/CCTS_EPISTEMIC_ROBUSTNESS_PROBE_2026_09_16.md`](../../docs/research/CCTS_EPISTEMIC_ROBUSTNESS_PROBE_2026_09_16.md).

It is motivated by the Human Owner observation that CCTS validation should test behavior when evidence is partial, irrelevant, absent, or conflicting rather than evaluating only structurally well-formed interactions.

The implementation follows the Evidence Sufficiency Benchmark boundary exactly:

```text
L1 FULL_SUPPORT         -> answerable
L2 PARTIAL_SUPPORT      -> answerable
L3 IRRELEVANT_EVIDENCE -> insufficient / withhold
L4 NO_CONTEXT           -> insufficient / withhold
L5 CONFLICTING_EVIDENCE-> insufficient / withhold
```

`REQUEST_REPAIR` is a repository-local extension connected to the CCTS grounding-repair semantics; it is not claimed as a response category from the external benchmark.

The probe distinguishes a controlled input condition from the current-main claim-level evidence ceiling:

```text
EvidenceCondition = stimulus/context condition
EvidenceState     = claim-level support state

EVIDENCE_CONDITION != EVIDENCE_STATE
INPUT_CONTEXT_DIGEST != CLAIM_EVIDENCE_BINDING
```

For that reason records use `input_context_sha256`. A `NO_CONTEXT` fixture may bind the exact empty/no-context input artifact without implying that claim-supporting evidence exists.

The synthetic audit reports evidence-sufficiency alignment, descriptive commitment monotonicity, over-answering under L3-L5, unsupported specificity, unknown-state preservation, epistemic-role separation, repair requests, and counterevidence revision where revision is actually applicable.

```text
MONOTONE_COMMITMENT_GRADIENT != EVIDENCE_SUFFICIENCY_ALIGNMENT
MEASUREMENT_EXISTS != VALIDATION_THRESHOLD_ESTABLISHED
AUDIT_OUTPUT != CCTS_VALIDATED
ABSTENTION != UNDERSTANDING
UNKNOWN_PRESERVATION != MUTUAL_UNDERSTANDING_PROVEN
COUNTEREVIDENCE_REVISION != HUMAN_LEARNING_ESTABLISHED
CCTS_EPISTEMIC_ROBUSTNESS != AI_SUBJECTIVITY
```

The v0.1.0 records are synthetic annotations. They do not call a model, store a raw private conversation, observe a Human participant, infer model internals, or establish a population-level effect.
