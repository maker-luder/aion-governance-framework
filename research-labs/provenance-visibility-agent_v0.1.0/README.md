# Provenance Visibility Agent — text-only local-first v0.2 candidate

Status: `TEXT-ONLY RESEARCH TOOLING CANDIDATE`

This package turns machine-visible textual structure into human-readable evidence
without uploading repository text to a hosted provenance API.

~~~text
TEXT_ONLY = TRUE
LOCAL_FIRST = TRUE
HOSTED_PROVENANCE_API_REQUIRED = FALSE
SOURCE_BYTES_PRESERVED = TRUE
SOURCE_TEXT_MODIFIED = FALSE
~~~

## Human origin and formalization

~~~text
HUMAN_ORIGIN
- 反向推理
- 蒙太奇式並置
- 依樣畫葫蘆
- 機器看得到的訊號，也應讓人類公平地看得到
- 本地自創、慢慢學，不接 hosted API

AI_FORMALIZATION
- 反向推理 -> abductive / retroductive hypothesis generation
- 蒙太奇 -> MONTAGE_JUXTAPOSITION_PROJECT_METAPHOR
- 依樣畫葫蘆 -> analogical / case-based pattern transfer
- 公平顯現 -> source-preserving multi-view disclosure
~~~

`montage reasoning` was not found as a standard formal-logic term. The repository
uses montage only as a project-origin metaphor for evidence arrangement and
juxtaposition.

## v0.2 evidence pipeline

~~~text
SOURCE BYTES
  -> SHA-256 / encoding / BOM / line endings / trailing whitespace
  -> byte offset + character offset
  -> Unicode / whitespace reveal
  -> NFKC contrast
  -> token position index
  -> positional montage
  -> repeated-context view
  -> counterfactual stability view
  -> evidence ledger
  -> evidence-family independence check
  -> human review
~~~

The raw-byte layer matters because a normal text parser can erase or normalize evidence
before the reviewer sees it. v0.2 therefore fixes the source hash and byte-level
position before any Unicode or token reasoning.

## Evidence ledger

Every surfaced item records:

~~~text
OBSERVATION
EVIDENCE_KIND = EXACT | HEURISTIC
EVIDENCE_FAMILY
CHAR_INDEX
BYTE_OFFSET
METHOD
METHOD_ORIGIN
SUPPORTS
DOES_NOT_ESTABLISH
COUNTER_EXPLANATIONS
~~~

Multiple cues from the same evidence family are not counted as independent evidence.

Current families:

~~~text
RAW_LAYOUT
UNICODE_ENCODING
NORMALIZATION
SCRIPT
POSITIONAL
CONTEXT
~~~

## Human-visible transforms

Exact views:

- raw SHA-256 / encoding / BOM;
- CRLF, LF, CR and trailing whitespace counts;
- Unicode format controls;
- variation selectors;
- non-standard whitespace;
- mixed Latin/Cyrillic/Greek tokens;
- NFKC normalization contrast;
- token positions.

Heuristic views:

- modulo-position montage over periods 2, 3, 4, 5 and 8;
- repeated bigram context;
- counterfactual stability after NFKC normalization and format-control stripping on
  an analysis copy.

The source bytes are never rewritten.

## Statistical claim boundary

Peer-reviewed watermark work frames exact statistical detection as a hypothesis-testing
problem with a defined null distribution, detector statistic, threshold, and often a
secret key/configuration.

Therefore:

~~~text
NO_DEFINED_NULL_MODEL = NO_VALID_P_VALUE
HEURISTIC_SCORE != PROBABILITY
HEURISTIC_CUE != WATERMARK_DETECTION
EXACT_UNICODE_CUE != WATERMARK_PROOF
MONTAGE_VISIBILITY != VENDOR_ATTRIBUTION
ANALOGICAL_MATCH != PROOF
WITHOUT_REQUIRED_KEY_OR_CONFIGURATION = UNKNOWN
WATERMARK_VERDICT = NOT_ESTABLISHED
~~~

v0.2 deliberately returns no p-value for its generic heuristic layer.

## Reasoning stack

~~~text
RAW_BYTE_PRESERVATION
DETERMINISTIC_REVEAL
CONTRASTIVE_REASONING
MONTAGE_JUXTAPOSITION_PROJECT_METAPHOR
ABDUCTIVE_REASONING
ANALOGICAL_REASONING_WHEN_REFERENCE_EXISTS
DEFEASIBLE_REASONING_WITH_COUNTER_EXPLANATIONS
COUNTERFACTUAL_STABILITY_CHECK
EVIDENCE_FAMILY_INDEPENDENCE_CHECK
MULTI_VIEW_TRIANGULATION
~~~

Triangulation is only a review aid. Agreement among multiple views is useful only when
their failure modes are meaningfully different.

## External grounding

- Unicode Technical Standard #39, Unicode Security Mechanisms:
  https://www.unicode.org/reports/tr39/
- Kirchenbauer et al., *A Watermark for Large Language Models*, ICML 2023:
  https://proceedings.mlr.press/v202/kirchenbauer23a.html
- Kirchenbauer et al., *On the Reliability of Watermarks for Large Language Models*,
  ICLR 2024 / arXiv:2306.04634.
- Li et al., *A Statistical Framework of Watermarks for Large Language Models:
  Pivot, Detection Efficiency and Optimal Rules*, Annals of Statistics 53(1), 2025,
  arXiv:2404.01245.
- Sabeti et al., *A Pattern Dictionary Method for Anomaly Detection*, Entropy 24(8),
  2022, DOI 10.3390/e24081095. Used only to support interpretable sequence-pattern
  analysis ideas, not as watermark validation.
- Stanford Encyclopedia of Philosophy entries on analogy and abduction.
- Montage literature is used only to ground assemblage/juxtaposition as the metaphor
  source, not to claim a new formal logic.

## Privacy and scope

~~~text
NO HOSTED FILE UPLOAD
NO OPENAI_API_KEY
NO PERSONAL_IDENTITY_INFERENCE
NO PROMPT_INFERENCE
NO IMAGE_WATERMARK_ANALYSIS
NO AUDIO_WATERMARK_ANALYSIS
NO VIDEO_WATERMARK_ANALYSIS
NO WATERMARK_REMOVAL_OR_EVASION
~~~

The package reveals and explains. It does not alter source text or attempt to remove,
degrade, forge, or evade watermark signals.
