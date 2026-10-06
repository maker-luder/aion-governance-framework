# Provenance Visibility Agent — text-only local research specification

Date: 2026-10-06  
Status: `TEXT-ONLY V0.2 CANDIDATE / NOT_MERGED`

## Research question

Can this public, text-centered repository make machine-visible textual provenance cues
human-visible through local, inspectable transforms without using a hosted provenance
API, while preserving source evidence and keeping heuristic claims below a valid
statistical detector?

~~~text
TEXT_ONLY = TRUE
LOCAL_FIRST = TRUE
SOURCE_BYTES_PRESERVED = TRUE
HOSTED_API_REQUIRED = FALSE
SOURCE_TEXT_MODIFIED = FALSE
~~~

## Recovery provenance

v0.2 is a fresh bounded implementation from current `main`. It reuses the useful
text-only ideas from closed / not-merged PR #281 but does not reopen or retroactively
merge #281.

~~~text
SOURCE_HISTORY = PR_281
PR_281_STATE = CLOSED_NOT_MERGED
REUSE_TYPE = BOUNDED_REIMPLEMENTATION
IMPLEMENTATION_REUSE != PR_MERGE
~~~

## Human origin / formalization

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

`montage reasoning` was not found as a standard formal-logic term. The project uses
montage only as an explicit project-origin metaphor for assemblage / juxtaposition of
evidence views.

## Layer 0 — raw byte preservation

The analysis starts before normal text parsing:

~~~text
SOURCE BYTES
  -> SHA-256
  -> BOM / encoding
  -> CRLF / LF / CR counts
  -> trailing-space / trailing-tab counts
  -> byte offset map
  -> decoded Unicode text
~~~

Reason:

~~~text
PARSER_NORMALIZATION_CAN_DESTROY_EVIDENCE = TRUE
RAW_BYTES_FIRST = REQUIRED_FOR_EXACT_TRACEABILITY
~~~

The implementation currently supports strict local decoding of UTF-8 and BOM-marked
UTF-8 / UTF-16 / UTF-32 variants. Unsupported or malformed input fails closed rather
than silently replacing bytes.

## Layer 1 — deterministic reveal

The exact layer surfaces properties actually present in the source:

1. Unicode format controls;
2. Unicode variation selectors;
3. non-standard whitespace;
4. mixed Latin/Cyrillic/Greek tokens;
5. NFKC normalization differences;
6. BOM and mixed line-ending structure;
7. trailing spaces/tabs;
8. character and byte offsets.

~~~text
EXACT_CUE = DIRECTLY_OBSERVED_PROPERTY
EXACT_CUE != WATERMARK_PROOF
~~~

Unicode UTS #39 supports the security relevance of mixed-script/confusable analysis.
This implementation is a bounded cue surface, not a claim of full UTS #39 conformance.

## Layer 2 — montage / juxtaposition

The same source is rendered through several views:

~~~text
RAW_PROFILE
ORIGINAL
MACHINE_VISIBLE_UNICODE
WHITESPACE_VISIBLE
NORMALIZATION_CONTRAST
TOKEN_INDEX
POSITIONAL_MONTAGE
REPEATED_CONTEXT
COUNTERFACTUAL_STABILITY
~~~

The goal is evidence arrangement, not attribution. A relation that is difficult to
notice in continuous prose can become inspectable after indexing, grouping or
juxtaposition.

## Layer 3 — reverse / abductive reasoning

Abduction is used only to generate candidate explanations:

~~~text
OBSERVED_CUE
  -> CANDIDATE_A
  -> COUNTER_EXPLANATION_B
  -> COUNTER_EXPLANATION_C
  -> FURTHER_TEST_OR_UNKNOWN
~~~

A candidate can be rebutted by later evidence or undercut by a better explanation.

## Layer 4 — analogical transfer

The HUMAN_ORIGIN phrase "依樣畫葫蘆" is formalized as analogical / case-based pattern
transfer.

~~~text
KNOWN_PATTERN
  -> derive inspection strategy
  -> apply to target
  -> compare similarities and differences

ANALOGICAL_MATCH = PLAUSIBILITY_CUE
ANALOGICAL_MATCH != PROOF
~~~

The source pattern and target identity must remain separate.

## Layer 5 — counterfactual stability

Heuristic positional structure is checked on analysis copies after:

- NFKC normalization;
- removal of Unicode format-control characters.

This does not edit the source. It asks whether a candidate depends entirely on a
specific representational artifact.

~~~text
COUNTERFACTUAL_COPY != SOURCE_MUTATION
CANDIDATE_SURVIVES_TRANSFORM != WATERMARK_PROOF
CANDIDATE_DISAPPEARS != WATERMARK_DISPROOF
~~~

## Layer 6 — evidence ledger

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

The ledger is designed so a human reviewer can inspect not only the result, but also
how the result was produced and what it cannot support.

## Layer 7 — evidence-family independence

Multiple cues from one underlying mechanism are not counted as multiple independent
evidence lines.

Current families:

~~~text
RAW_LAYOUT
UNICODE_ENCODING
NORMALIZATION
SCRIPT
POSITIONAL
CONTEXT
~~~

For example, multiple format-control characters remain one `UNICODE_ENCODING`
family, not many independent votes.

~~~text
CUE_COUNT != INDEPENDENT_EVIDENCE_COUNT
MULTI_VIEW_AGREEMENT != PROOF
~~~

## Layer 8 — statistical claim ceiling

Peer-reviewed LLM-watermark work treats exact statistical detection as a hypothesis
test. Valid false-positive control requires a defined null model / pivotal statistic,
detector rule and threshold, and many schemes also require a key/configuration.

Kirchenbauer et al. (ICML 2023) demonstrate a green-list statistical detector.
Li et al. (Annals of Statistics 2025; arXiv:2404.01245) develop a broader hypothesis-
testing framework using pivotal statistics and secret-key-dependent verification to
control Type-I error.

Therefore the generic local heuristic layer explicitly returns:

~~~text
NULL_MODEL_STATUS = UNDEFINED_FOR_GENERIC_HEURISTIC
STATISTICAL_P_VALUE = NONE

NO_DEFINED_NULL_MODEL = NO_VALID_P_VALUE
HEURISTIC_SCORE != PROBABILITY
HEURISTIC_CUE != WATERMARK_DETECTION
~~~

No percentage confidence or p-value is manufactured.

## Pattern analysis

Sequence-pattern literature, including Sabeti et al. (Entropy 2022), shows that pattern
dictionaries and compression-based approaches can support interpretable anomaly
analysis. v0.2 uses this literature only as support for the general idea that repeated
sequence structure can be made inspectable.

~~~text
SEQUENCE_ANOMALY_METHOD != WATERMARK_VALIDATION
PATTERN_REGULARITY != VENDOR_ATTRIBUTION
~~~

The current implementation deliberately stays simpler than a trained pattern dictionary
because the repository does not yet have a justified training corpus / null baseline.

## Architecture

~~~text
RAW LOCAL TEXT BYTES
  |
  +--> hash / encoding / BOM / newline profile
  |
  +--> exact Unicode / script / normalization views
  |
  +--> token position index
  |
  +--> positional montage
  |
  +--> repeated context
  |
  +--> counterfactual stability
  |
  +--> evidence ledger
  |
  +--> evidence-family independence check
  |
  +--> human review
  |
  +--> exact keyed detector only when matching detector material exists
~~~

No new image, audio, video, C2PA, or media-watermark path is retained in this package.

## Claim ceiling

~~~text
HEURISTIC_CUE != WATERMARK_DETECTION
HEURISTIC_SCORE != PROBABILITY
EXACT_UNICODE_CUE != WATERMARK_PROOF
MONTAGE_VISIBILITY != VENDOR_ATTRIBUTION
ANALOGICAL_MATCH != PROOF
MULTI_VIEW_AGREEMENT != PROOF
NO_DEFINED_NULL_MODEL = NO_VALID_P_VALUE
WITHOUT_REQUIRED_KEY_OR_CONFIGURATION = UNKNOWN
DETECTED != AUTHORSHIP
NOT_DETECTED != HUMAN_CREATED
WATERMARK_VERDICT = NOT_ESTABLISHED
NO_WATERMARK_REMOVAL_OR_EVASION
~~~

## Sources checked

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
  2022, DOI 10.3390/e24081095.
- Stanford Encyclopedia of Philosophy entries on analogy and abduction.
- Montage literature was checked only for assemblage / juxtaposition as the metaphor
  source.

Tool availability note: Consensus quota was already exhausted in this session; Scite
required paid/trial access; Hugging Face paper search was unavailable. These tool
limitations are not evidence that relevant literature does not exist.
