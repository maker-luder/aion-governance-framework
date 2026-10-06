# Provenance Visibility Agent v0.1 — text-only / local-first

Status: `CANONICAL RESEARCH TOOLING / LOCAL TEXT VERIFIER`

This package makes supported hidden **text** signals explicit and human-readable
without uploading repository text to a hosted provenance API.

```text
TEXT_ONLY = TRUE
LOCAL_FIRST = TRUE
HOSTED_PROVENANCE_API_REQUIRED = FALSE
NETWORK_REQUIRED_BY_DEFAULT = FALSE
SOURCE_TEXT_MODIFIED = FALSE
```

## Human origin and formalization

```text
HUMAN_ORIGIN
- 反向推理
- 蒙太奇式並置：把機器可見訊號轉成人類可檢查的排列
- 依樣畫葫蘆：從已知 pattern 類推未知 pattern
- 本地自創、慢慢學、不要 hosted API

AI_FORMALIZATION
- 反向推理 -> abductive / retroductive hypothesis generation
- 蒙太奇 -> MONTAGE_JUXTAPOSITION_PROJECT_METAPHOR
- 依樣畫葫蘆 -> analogical / case-based pattern transfer
- 公平顯現 -> source-preserving multi-view human-readable disclosure
```

`montage reasoning` was not found as a standard formal-logic term. The repository
uses montage only as an explicit project-origin metaphor derived from assemblage and
juxtaposition.

## Human-visible reveal

`AION_TEXT_MONTAGE_REVEAL_V0_1` produces multiple local views of the same text:

```text
ORIGINAL
MACHINE_VISIBLE_UNICODE
WHITESPACE_VISIBLE
NFKC_NORMALIZATION_CONTRAST
TOKEN_POSITION_INDEX
POSITIONAL_MONTAGE
REPEATED_CONTEXT
COMPETING_HYPOTHESES
```

The deterministic layer can surface exact properties already present in the source:

- Unicode format controls;
- Unicode variation selectors;
- non-standard whitespace;
- mixed Latin/Cyrillic/Greek tokens;
- NFKC normalization differences;
- explicit token positions.

The heuristic layer can reorganize token positions and repeated contexts so patterns
that are easy for a machine to count are easier for a human reviewer to inspect.

## Reasoning stack

```text
DETERMINISTIC_REVEAL
CONTRASTIVE_REASONING
MONTAGE_JUXTAPOSITION_PROJECT_METAPHOR
ABDUCTIVE_REASONING
ANALOGICAL_REASONING_WHEN_REFERENCE_EXISTS
DEFEASIBLE_REASONING_WITH_COUNTER_EXPLANATIONS
MULTI_VIEW_TRIANGULATION
```

Every heuristic hypothesis remains defeasible. Normal typography, multilingual text,
templates, punctuation rhythm, copy/paste artifacts, and formatting remain competing
explanations.

## Statistical text watermarks

### OpenAI textGrain

The published method requires the generated text plus a matching secret key and
tokenizer/configuration. Without those required materials, this package reports:

```text
TEXTGRAIN_ALGORITHM_DESCRIPTION = PUBLIC
EXACT_LOCAL_VENDOR_VERDICT_WITHOUT_KEY = NOT_ESTABLISHED
```

### Other keyed text detectors

The agent exposes a local keyed-detector interface so a known, authorized text detector
can be plugged into the same human-readable reporting layer without a hosted API.

A detector for one watermark family is not silently treated as a detector for another.

## Interpretation rules

```text
HEURISTIC_CUE != WATERMARK_DETECTION
HEURISTIC_SCORE != PROBABILITY
EXACT_UNICODE_CUE != WATERMARK_PROOF
MONTAGE_VISIBILITY != VENDOR_ATTRIBUTION
ANALOGICAL_MATCH != PROOF
WITHOUT_REQUIRED_KEY_OR_CONFIGURATION = UNKNOWN
DETECTED != AUTHORSHIP
DETECTED != OWNERSHIP
NOT_DETECTED != HUMAN_CREATED
UNKNOWN = UNKNOWN
```

## External grounding

- Unicode Technical Standard #39, Unicode Security Mechanisms:
  https://www.unicode.org/reports/tr39/
- Kirchenbauer et al., *A Watermark for Large Language Models*, ICML 2023:
  https://proceedings.mlr.press/v202/kirchenbauer23a.html
- Kirchenbauer et al., *On the Reliability of Watermarks for Large Language Models*,
  ICLR 2024 / arXiv:2306.04634.
- Stanford Encyclopedia of Philosophy, *Analogy and Analogical Reasoning*:
  https://plato.stanford.edu/entries/reasoning-analogy/
- Stanford Encyclopedia of Philosophy, *Abduction*:
  https://plato.stanford.edu/entries/abduction/
- Montage literature is used only to ground the assemblage/juxtaposition metaphor,
  not to claim a new formal logic.

## Privacy and scope

```text
NO HOSTED FILE UPLOAD
NO OPENAI_API_KEY
NO PERSONAL_IDENTITY_INFERENCE
NO PROMPT_INFERENCE
NO IMAGE_WATERMARK_ANALYSIS
NO AUDIO_WATERMARK_ANALYSIS
NO VIDEO_WATERMARK_ANALYSIS
NO WATERMARK_REMOVAL_OR_EVASION
```

The package reveals and explains; it does not alter source text or attempt to remove,
degrade, forge, or evade watermark signals.
