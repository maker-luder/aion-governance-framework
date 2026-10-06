# Provenance Visibility Agent v0.1 — local-first

Status: `CANONICAL RESEARCH TOOLING / LOCAL VERIFIER`

The candidate turns supported hidden provenance signals into explicit,
human-readable disclosures **without making a hosted API the core verifier**.

```text
LOCAL_FIRST = TRUE
FILE_UPLOAD_TO_PROVIDER = FALSE
HOSTED_PROVENANCE_API_REQUIRED = FALSE
NETWORK_REQUIRED_BY_DEFAULT = FALSE
```

## What we can verify ourselves now

### C2PA / Content Credentials

The open C2PA standard has local open-source implementations. This package uses the
official Content Authenticity Initiative Python bindings (`c2pa-python`) when
installed.

The local verifier:

- reads the asset locally;
- disables remote-manifest fetching;
- validates the embedded manifest;
- surfaces validation warnings instead of calling them trusted;
- renders issuer/model/time fields when the local manifest exposes them;
- does not send the asset to OpenAI.

Install:

```text
pip install -e "research-labs/provenance-visibility-agent_v0.1.0[c2pa]"
```

## Heuristic reveal for unknown image signals

Exact watermark decoders remain the preferred evidence when they are available. For an
unknown image signal, this package now also offers a **local heuristic reveal** layer
that tries to make weak structure visible without pretending to know the watermark key,
payload or vendor.

The reveal path is deliberately inferential:

```text
UNKNOWN_SIGNAL
  -> LOCAL_LUMA_RESIDUAL
  -> RGB_LSB_BALANCE
  -> PERIODICITY_SCAN / FOLD
  -> AION_REVERSE_REVEAL_V0_1 composite
  -> HUMAN_REVIEW
```

The custom composite is an engineering heuristic, not a validated detector:

```text
AION_REVERSE_REVEAL_V0_1 =
  50% local residual
  20% RGB least-significant-bit balance
  30% periodic folded residual

HEURISTIC_CUE != WATERMARK_DETECTION
HEURISTIC_SCORE != PROBABILITY
VISIBLE_PATTERN != PROVENANCE_PROOF
```

The core transform works from decoded RGB pixels using the Python standard library.
Common PNG/JPEG/etc. file decoding is an optional local convenience layer:

```text
pip install -e "research-labs/provenance-visibility-agent_v0.1.0[forensics]"
```

The optional dependency is Pillow 12.3.0. Output reveal layers can be written as binary
PGM images without another image-writing dependency.

This approach is motivated by established image-forensics ideas rather than by a claim
that one generic formula can decode arbitrary watermarks. Prior work shows that lower
bit-plane statistics can expose embedding artifacts, while residual correlation and
periodicity analysis can reveal repeated low-energy processing patterns. See:

- Avcıbaş et al., *Image Steganalysis with Binary Similarity Measures*,
  DOI `10.1155/ASP.2005.2749`.
- Butora & Bas, *The Adobe Hidden Feature and its Impact on Sensor Attribution*,
  arXiv `2401.01366`.

False positives are expected. Compression, demosaicing, dithering, scaling, sharpening
and other processing can create similar structures. The output therefore remains
`watermark_verdict = NOT_ESTABLISHED`.

## What we cannot honestly verify locally yet

### OpenAI textGrain

OpenAI published the mathematical detection procedure in its 2026-10-05 technical
report. The detector requires the text plus the matching secret key and deployment
configuration. The deployed OpenAI key is not public, and OpenAI says its implementation
will be open-sourced in the future rather than being public already.

Therefore:

```text
TEXTGRAIN_ALGORITHM_DESCRIPTION = PUBLIC
OPENAI_DEPLOYED_SECRET_KEY = NOT_PUBLIC
GENERIC_LOCAL_OPENAI_TEXTGRAIN_VERDICT = NOT_ESTABLISHED
```

The agent exposes a local keyed-detector interface so a future verified implementation
can plug in without redesigning the reporting layer.

### Google SynthID Text

Google DeepMind has open-sourced SynthID Text detection, including weighted-mean and
Bayesian approaches. But a detector corresponds to its watermark keys/configuration.
A SynthID Text detector is **not** an OpenAI textGrain detector.

### OpenAI-used image/audio SynthID

Our research pass did not find a public, general-purpose local verifier that can
independently decode the OpenAI-used image/audio SynthID signal. We therefore report:

```text
SYNTHID_LOCAL_VERIFIER_NOT_PUBLIC
```

rather than substituting an image/audio AI classifier.

## Interpretation rules

```text
DETECTED != AUTHORSHIP
DETECTED != OWNERSHIP
NOT_DETECTED != HUMAN_CREATED
CLASSIFIER_SCORE != WATERMARK_VERDICT
UNKNOWN = UNKNOWN
```

## Privacy

```text
NO HOSTED FILE UPLOAD
NO OPENAI_API_KEY
NO PERSONAL_IDENTITY_INFERENCE
NO PROMPT_INFERENCE
NO CONVERSATIONAL_NICKNAME IN PUBLIC IDENTIFIERS
```

Watermark removal, degradation and evasion remain out of scope.

The heuristic reveal path also stops at visualization and review; it does not estimate a subtraction pattern or modify the source asset.
