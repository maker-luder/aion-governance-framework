# Provenance Visibility Agent — local-first research specification

Date: 2026-10-06  
Status: `BRANCH-ONLY RESEARCH CANDIDATE`

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
