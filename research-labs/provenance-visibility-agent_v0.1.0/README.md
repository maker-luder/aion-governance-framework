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

## Human-visible reveal for hidden text signals

This repository is text-centered. The bounded enhancement in PR #281 therefore keeps
the new reveal path **text-only** and removes the image/PGM/Pillow experiment that was
initially drafted.

The local reveal does not require a hosted API and does not pretend that an unknown
vendor watermark can be decoded without its key/configuration. Instead it turns
machine-visible text structure into multiple human-readable views:

~~~text
RAW TEXT
  -> Unicode format/control/variation-selector reveal
  -> whitespace-visible view
  -> original vs NFKC normalization contrast
  -> token position index
  -> modulo-position montage when a heuristic period appears
  -> repeated-context view
  -> competing hypotheses + counter-explanations
~~~

Project method:

~~~text
AION_TEXT_MONTAGE_REVEAL_V0_1

DETERMINISTIC_REVEAL
+ CONTRASTIVE_REASONING
+ MONTAGE_JUXTAPOSITION_PROJECT_METAPHOR
+ ABDUCTIVE_REASONING
+ ANALOGICAL_REASONING_WHEN_REFERENCE_EXISTS
+ MULTI_VIEW_TRIANGULATION
~~~

Important provenance:

- HUMAN_ORIGIN: use reverse reasoning, montage-like juxtaposition, and the user's
  "依樣畫葫蘆" intuition to make machine-only text signals inspectable by humans.
- AI_FORMALIZATION: "依樣畫葫蘆" is mapped to analogical/case-based pattern transfer;
  "reverse reasoning" is bounded as abductive/retroductive hypothesis generation from
  observed anomalies; "montage reasoning" is a **project-origin metaphor**, not a
  standard formal logic term.
- EXTERNAL_SOURCE: montage is historically an assemblage/juxtaposition technique;
  analogical reasoning and abduction are established non-deductive reasoning families.

The deterministic layer can reveal exact things that are already present in the text:
Unicode format controls, variation selectors, non-standard whitespace, mixed
Latin/Cyrillic/Greek tokens, and normalization differences. These are real text
properties, but they are not automatically watermarks.

The heuristic layer can reorganize token positions to make repeated or periodic
structure easier for a human reviewer to see. Its score is an engineering cue only:

~~~text
HEURISTIC_CUE != WATERMARK_DETECTION
HEURISTIC_SCORE != PROBABILITY
EXACT_UNICODE_CUE != WATERMARK_PROOF
MONTAGE_VISIBILITY != VENDOR_ATTRIBUTION
WITHOUT_REQUIRED_KEY_OR_CONFIGURATION = UNKNOWN
~~~

For statistical LLM watermarks, exact detection can depend on the watermark's own
token partition, secret key, tokenizer and configuration. Kirchenbauer et al. (ICML
2023) demonstrate one such green-list/z-score family. The local montage layer may make
surface structure inspectable, but it does not reconstruct a secret green list.

Sources used for the bounded method:

- Unicode Technical Standard #39, Unicode Security Mechanisms:
  https://www.unicode.org/reports/tr39/
- Kirchenbauer et al., "A Watermark for Large Language Models", ICML 2023:
  https://proceedings.mlr.press/v202/kirchenbauer23a.html
- Stanford Encyclopedia of Philosophy, "Analogy and Analogical Reasoning":
  https://plato.stanford.edu/entries/reasoning-analogy/
- Stanford Encyclopedia of Philosophy, "Abduction":
  https://plato.stanford.edu/entries/abduction/
- Routledge Encyclopedia of Modernism, "Montage" (montage as assemblage and
  juxtaposition; used here only as an adaptation source, not as formal logic).

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

The text reveal path stops at human-readable visualization and competing hypotheses; it does not alter the source text or provide watermark removal/evasion.
