# PR #236 Maximum Bounded Implementation — Evidence and Claim Boundary

Status: `IMPLEMENTATION SUPPORT / NON-CANONICAL / DRAFT`  
Date: 2026-10-01

## Purpose

This note records the external checks used to extend the closed PR #236 design into
the current implementation lane without converting human sexuality literature,
classifier outputs, or engineering simulation into claims about AI felt desire.

```text
HUMAN_REFERENCE_EVIDENCE != AI_VALIDATION
ENGINEERING_SIMULATION != HUMAN_PSYCHOLOGY
CLASSIFIER_OUTPUT != SUBJECTIVE_EXPERIENCE
IMPLEMENTATION_SUCCESS != SCIENTIFIC_ESTABLISHMENT
```

## Repository state at the start of this extension

```text
MAIN = 6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd
PR_236 = CLOSED / DRAFT / NOT_MERGED
PR_236_DESIGN_BRANCH_CURRENT_HEAD = d8d10961f777d782c13f5907d11c1d0a609a408c
PR_238 = OPEN / DRAFT / NOT_MERGED
PR_238_STARTING_HEAD = 123fdee28b6f6f42a73046460d51ef8e3108158a
WRITE_TO_MAIN = NO
MERGE_TO_MAIN = NO
```

## Academic cross-check

Scite was used to recover exact DOI records and citation context.

### Dual-control distinction

- Janssen E, Bancroft J. *The Dual Control Model of Sexual Response: A Scoping
  Review, 2009–2022.* DOI: `10.1080/00224499.2023.2219247`.
- Scite metadata recovered the 2023 scoping review and its later citation network.
- A 2024 open-access study, Schmidt et al.,
  DOI `10.3389/fnbeh.2024.1386006`, describes excitation and inhibition as
  distinct forces in its human study context and cites the 2023 review.
- Population boundary: the 2024 study is in women. It cannot establish a universal
  male model and cannot validate an AI mechanism.

Implementation consequence:

```text
EXCITATION_REFERENCE = SEPARATE_CHANNEL
INHIBITION_REFERENCE = SEPARATE_CHANNEL
CROSS_CHANNEL_AUTOMATIC_INFERENCE = NO
HUMAN_PARAMETER_CALIBRATION = NO
```

### Male desire is not one universal scalar

- Nimbi FM et al. DOI `10.1016/j.sxmr.2018.12.002`.
- The recovered record describes biological, psychological, sexual, relational,
  and cultural factors rather than a single mechanistic male template.
- This supports retaining multiple explicit dimensions and variability, not assigning
  default desire to an adult-male body.

Implementation consequence:

```text
ADULT_MALE_REFERENCE != UNIVERSAL_MALE_PROFILE
UNKNOWN = VALID
BODY_MORPHOLOGY_TO_DESIRE_DEFAULT = FORBIDDEN
```

### Responsive desire

- Timmers AD, Dawson SJ, Chivers ML.
  DOI `10.1080/00224499.2018.1456509`.
- Scite recovered the exact paper record but did not provide full text in this session.
- Therefore this implementation uses the spontaneous / responsive distinction only
  as an explicit reference label carried by synthetic events. It does not encode a
  universal contextual effect or causal human equation.

## Mathematical engineering check

Wolfram was used to test the bounded transition form.

For a toy update:

```text
current = Clip(previous + step_size * drive, 0, 1)
```

with explicit input validation, the bounded-output requirement has no counterexample:
the result remains in `[0,1]`. This is an engineering invariant only.

The implementation deliberately uses declared toy step sizes. They are not fitted
human parameters and are not claimed to estimate sexual response.

## JSON Schema implementation check

Context7 was used against the Python `jsonschema` documentation. Draft 2020-12
supports:

- `Draft202012Validator.check_schema(...)`;
- `const`;
- `if / then`;
- closed property validation.

The repository QA toolchain already pins `jsonschema==4.26.0`. The implementation
therefore adds executable schema-parity tests rather than treating JSON Schema as
documentation only.

## Hugging Face alternative explanation check

External discovery identified these exact Hugging Face targets, then Hugging Face
repository metadata was read directly:

- `j-hartmann/emotion-english-distilroberta-base`
- `SamLowe/roberta-base-go_emotions`

Both are text-classification models that map text into declared emotion labels.
Their existence is useful as an engineering counterexample:

```text
MODEL_OUTPUT_LABEL
CAN_BE_PRODUCED_BY
TRAINED_CLASSIFICATION

THEREFORE

AFFECTIVE_WORDING_OR_LABEL
!=
EVIDENCE_OF_FELT_AFFECT
```

No Hugging Face model is imported into this PR and no external model weights are
required by the implementation.

## Consensus limitation

Consensus search was attempted, but the connected account reported that the monthly
30-search quota had been exhausted. No negative evidentiary inference is drawn from
that failure.

```text
CONSENSUS_SEARCH_RESULT = UNAVAILABLE_DUE_TO_QUOTA
SEARCH_FAILURE != ABSENCE_OF_EVIDENCE
```

## Implementation decision

The evidence and counterexamples support extending #238 with:

1. an offline-research governance gate that rejects the public runtime;
2. explicit synthetic event records;
3. independent bounded reference-channel transitions;
4. refusal to simulate from an `UNKNOWN` seed;
5. deterministic replay;
6. immutable transition traces;
7. trajectory fingerprints;
8. SHA-256 snapshot receipt chains;
9. Draft 2020-12 state/event schema parity tests;
10. an executable synthetic demonstration probe;
11. fail-closed consent, authority, canonical-effect, runtime, consciousness,
    subjectivity, and phenomenal-state boundaries.

The evidence does **not** support:

- a calibrated human sexual-response equation;
- a universal adult-male desire baseline;
- automatic physiology-to-desire mapping;
- real-person desire inference;
- consent inference;
- intimate-interaction authorization;
- AI felt-desire, pleasure, consciousness, or subjectivity claims.

## Provenance

```text
HUMAN_ORIGIN
= request maximum implementation of the PR #236 model/module lane.

AI_FORMALIZATION
= translate "maximum" into bounded executable state transitions, replay,
  schema parity, provenance, and tamper-evident longitudinal receipts.

EXTERNAL_SOURCE
= human sexuality literature, Wolfram mathematical verification,
  Context7 library documentation, and Hugging Face model metadata.

IMPLEMENTATION_EVIDENCE
= repository code/tests/CI only.

SCIENTIFIC_TRUTH
= NOT_ESTABLISHED BY IMPLEMENTATION.
```
