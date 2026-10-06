# Provenance Visibility Agent v0.1 — local-first

Status: `RESEARCH CANDIDATE / LOCAL VERIFIER`

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
