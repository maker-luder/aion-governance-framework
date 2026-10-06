# Provenance Visibility Agent — local-first research specification

Date: 2026-10-06  
Status: `MAIN-INTEGRATED RESEARCH TOOLING`

## Research question

Can the repository make hidden provenance signals visible using reproducible local
verification rather than uploading private files to a hosted provenance API?

## Pipeline findings

### C2PA

The C2PA specification and Content Authenticity Initiative SDKs are open. The
`contentauth/c2pa-python` library can read and validate embedded manifests locally.
Its verification settings allow remote manifest fetching to be disabled.

Disposition:

```text
C2PA_LOCAL_VERIFICATION = IMPLEMENTABLE
```

### OpenAI textGrain

OpenAI's 2026-10-05 technical report specifies the generation and detection
mathematics. It states that detection requires the generated text and secret key; the
detector also needs matching tokenizer/block/column/context configuration. OpenAI
currently limits detector access and says it plans to release textGrain as open source.

Disposition:

```text
TEXTGRAIN_TECHNICAL_METHOD = PUBLIC
DEPLOYED_SECRET_KEY = NOT_PUBLIC
CURRENT_GENERIC_LOCAL_DETECTION = NOT_ESTABLISHED
```

### Google DeepMind SynthID Text

The reference implementation is open source. It provides weighted-mean and Bayesian
detectors. Detection is configuration/key-specific; the Bayesian detector is trained
per watermarking key.

Disposition:

```text
SYNTHID_TEXT_REFERENCE_DETECTOR = OPEN_SOURCE
SYNTHID_TEXT_DETECTOR != OPENAI_TEXTGRAIN_DETECTOR
```

### Image/audio SynthID

OpenAI documents SynthID as an embedded signal in supported image/audio output, but
our current public-source pass did not identify a general-purpose local decoder for
the OpenAI-used signal.

Disposition:

```text
OPENAI_MEDIA_SYNTHID_LOCAL_DECODER = NOT_ESTABLISHED
DO_NOT_SUBSTITUTE_AI_CLASSIFIER = TRUE
```

## Unknown image signals: heuristic reveal

The lack of a public vendor-specific decoder does not require the repository to stop at
`LOCAL_VERIFIER_NOT_PUBLIC`. A separate **heuristic visualization** path may surface
low-energy structure for human review, provided it does not promote that structure into
a watermark verdict.

The v0.1 implementation uses three independent local cues:

1. an 8-neighbour luminance residual;
2. an RGB least-significant-bit balance view;
3. a horizontal/vertical residual autocorrelation scan over candidate periods
   `4, 8, 16, 32, 64, 128`, followed by modulo-period folding when a cue crosses the
   engineering threshold.

A custom composite combines those views:

```text
AION_REVERSE_REVEAL_V0_1 =
  0.50 * LOCAL_RESIDUAL
+ 0.20 * LSB_BALANCE
+ 0.30 * PERIODIC_FOLD
```

The weights and the current periodicity threshold are repository-origin engineering
choices. They are not externally validated probabilities or watermark confidence
scores.

```text
HEURISTIC_CUE != WATERMARK_DETECTION
HEURISTIC_SCORE != PROBABILITY
PATTERN_VISIBILITY != PAYLOAD_DECODING
PATTERN_VISIBILITY != VENDOR_ATTRIBUTION
PATTERN_VISIBILITY != AUTHORSHIP
```

This is the bounded meaning of “reverse reasoning” here: start from observable weak
residual/bit-plane/periodic structure and infer a **candidate visualization target**,
not the hidden key, payload, author or generator.

Related external evidence:

- Avcıbaş et al. (2005), *Image Steganalysis with Binary Similarity Measures*,
  DOI `10.1155/ASP.2005.2749`: lower bit-plane statistics can carry embedding
  artifacts.
- Butora & Bas (2023/2024), *The Adobe Hidden Feature and its Impact on Sensor
  Attribution*, arXiv `2401.01366`: residual cross-correlation exposed a periodic
  128×128 processing pattern, while also demonstrating that such patterns can create
  forensic false positives.

The second source is particularly important for the claim boundary: a visible periodic
pattern can come from image processing such as dithering rather than a provenance
watermark. Therefore the heuristic path always returns
`watermark_verdict = NOT_ESTABLISHED`.

## Architecture

```text
LOCAL FILE
  |
  +--> C2PA local reader/verifier --------> visible report
  |
  +--> textGrain -------------------------> KEY_REQUIRED
  |
  +--> SynthID image/audio ---------------> LOCAL_VERIFIER_NOT_PUBLIC
  |
  +--> unknown image signal --------------> heuristic reveal -> review-only layers
  |
  +--> future verified local detector ----> adapter -> visible report
```

## Sources checked

- OpenAI textGrain technical report, 2026-10-05.
- OpenAI provenance/help documentation, checked 2026-10-06.
- C2PA open specification and Content Authenticity Initiative c2pa-python/c2pa-rs.
- Google DeepMind `synthid-text` reference implementation.
- Hugging Face/Google documentation for SynthID Text integration.

Tool availability note: Scite required a paid plan in this session; Hugging Face MCP
search endpoints returned unavailable. `TOOL_UNAVAILABLE != EVIDENCE_ABSENT`.
