# Provenance Visibility Agent — local-first research specification

Date: 2026-10-06  
Status: `MAIN-INTEGRATED RESEARCH TOOLING`

## Research question

Can this public, text-centered repository make machine-visible textual provenance cues human-visible through local, inspectable transforms without using a hosted provenance API?

## Pipeline findings

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

## Hidden text signals: human-visible montage reveal

The repository's bounded transparency need is text-first. PR #281 therefore removes
the drafted image heuristic path and replaces it with a local text-only reveal layer.

The research problem is not "guess the secret watermark key." It is:

> If a signal is machine-visible but difficult for a human to notice, can we transform
> the same local text into transparent, inspectable views without changing the source
> and without claiming more than the evidence supports?

### Deterministic reveal

These views expose properties that are exactly present in the input:

1. Unicode format controls;
2. Unicode variation selectors;
3. non-standard whitespace;
4. mixed Latin/Cyrillic/Greek tokens;
5. NFKC normalization differences;
6. explicit token-position indexing.

~~~text
DETERMINISTIC_REVEAL = SOURCE-PRESERVING DISPLAY TRANSFORM
DETERMINISTIC_CUE != WATERMARK_PROOF
~~~

Unicode UTS #39 is relevant to the security side of confusable and mixed-script
analysis. The implementation does not claim complete UTS #39 conformance; it exposes a
bounded mixed-script cue using the Python standard library.

### Montage / juxtaposition

"Montage reasoning" was not found as a standard formal logic term in the external
review. Montage is established as an assemblage/juxtaposition technique in film,
literature and analysis. We therefore use:

~~~text
MONTAGE_JUXTAPOSITION_PROJECT_METAPHOR
~~~

as an explicitly project-origin research interface.

The implementation places several views of the same text next to each other:

~~~text
ORIGINAL
MACHINE_VISIBLE_UNICODE
WHITESPACE_VISIBLE
NORMALIZATION_CONTRAST
TOKEN_INDEX
POSITIONAL_MONTAGE
REPEATED_CONTEXT
~~~

The point is human inspectability: a relation that was hard to see in the continuous
text can become visible after indexing, grouping or juxtaposition.

### Reverse / abductive reasoning

The user's "反向推理" is bounded as abductive/retroductive hypothesis generation:

~~~text
OBSERVED_CUE
  -> candidate explanation A
  -> competing explanation B
  -> competing explanation C
  -> further test / remain UNKNOWN
~~~

Stanford Encyclopedia of Philosophy describes abduction as explanatory reasoning /
inference to the best explanation, while emphasizing that abductive conclusions are
non-necessary. In this project, a cue can generate a candidate hypothesis but must not
erase counter-explanations.

### "依樣畫葫蘆" / analogical reasoning

HUMAN_ORIGIN uses the phrase "依樣畫葫蘆" for learning from a known pattern and trying
an analogous view on an unknown case. AI_FORMALIZATION maps this to
analogical/case-based pattern transfer.

Stanford Encyclopedia of Philosophy characterizes analogical reasoning as drawing on
accepted similarities between a source and target while noting that analogical
conclusions generally do not follow with certainty.

Therefore:

~~~text
ANALOGICAL_MATCH = PLAUSIBILITY_CUE
ANALOGICAL_MATCH != PROOF
SOURCE_PATTERN != TARGET_IDENTITY
~~~

### Local periodic montage

For texts long enough to inspect, the current engineering candidate groups token
positions by modulo periods 2, 3, 4, 5 and 8. It compares token-length and terminal
punctuation dispersion only to choose a view worth showing to a human.

~~~text
PERIODIC_CUE_THRESHOLD = PROJECT_ORIGIN_ENGINEERING_CHOICE
HEURISTIC_SCORE != PROBABILITY
POSITIONAL_PATTERN != WATERMARK_DETECTION
~~~

This is intentionally weaker than a keyed LLM-watermark detector. Kirchenbauer et al.
(ICML 2023) show that one watermark family relies on pseudorandom token partitions and
a statistical green-token test. Without the matching scheme/key/configuration, a local
generic analysis cannot honestly reconstruct the detector's hidden partition.

### Fairness / transparency rule

The fairness target is epistemic visibility, not forced attribution:

~~~text
MACHINE_VISIBLE_CUE
  -> HUMAN_READABLE_VIEW
  -> METHOD_DISCLOSURE
  -> ALTERNATIVE_EXPLANATIONS
  -> CLAIM_CEILING

NO_HOSTED_API = TRUE
SOURCE_TEXT_MODIFIED = FALSE
WATERMARK_VERDICT = NOT_ESTABLISHED
~~~

A human reviewer should be able to see what transformation produced each cue and why
the result is uncertain.

### Defeasible reasoning and triangulation

Heuristic conclusions are defeasible: later information can rebut the candidate
conclusion or undercut the assumed connection between cue and watermark. The report
therefore keeps counter-explanations visible rather than collapsing them into one
story.

Multiple views are used as a qualitative triangulation aid only when their failure
modes differ. Agreement among views can justify further inspection, but it does not
convert an unkeyed heuristic into a keyed watermark detector.

~~~text
DEFEASIBLE_REASONING = IMPLEMENTED_AS_COUNTER_EXPLANATIONS
MULTI_VIEW_TRIANGULATION = REVIEW_AID
MULTI_VIEW_AGREEMENT != PROOF
~~~

## Architecture

```text
LOCAL TEXT
  |
  +--> Unicode / whitespace reveal ------> exact human-readable view
  |
  +--> normalization contrast -----------> exact human-readable diff
  |
  +--> token position index -------------> exact positional view
  |
  +--> positional montage ---------------> heuristic review cue
  |
  +--> repeated-context view ------------> heuristic review cue
  |
  +--> known keyed text detector --------> exact detector adapter
  |
  +--> required key/config unavailable --> UNKNOWN
```

PR #281 retains no new image, audio, video, C2PA, or media-watermark implementation in this package. The enhancement is text-only. Unrelated multimodal components elsewhere in the repository are outside this PR.

## Sources checked

- Unicode Technical Standard #39, Unicode Security Mechanisms:
  https://www.unicode.org/reports/tr39/
- Kirchenbauer et al., "A Watermark for Large Language Models", ICML 2023:
  https://proceedings.mlr.press/v202/kirchenbauer23a.html
- Kirchenbauer et al., "On the Reliability of Watermarks for Large Language Models",
  ICLR 2024 / arXiv:2306.04634.
- Stanford Encyclopedia of Philosophy, "Analogy and Analogical Reasoning":
  https://plato.stanford.edu/entries/reasoning-analogy/
- Stanford Encyclopedia of Philosophy, "Abduction":
  https://plato.stanford.edu/entries/abduction/
- Routledge Encyclopedia of Modernism, "Montage": montage as assemblage and
  juxtaposition. This supports the metaphor source, not a claim that montage is a
  formal inference rule.
- OpenAI textGrain technical report, 2026-10-05.
- Google DeepMind synthid-text reference implementation.

Tool availability note: Consensus search quota was exhausted until 2026-11-01; Scite
MCP required a paid plan/free trial; the Hugging Face paper-search endpoint was
unavailable in this session. TOOL_UNAVAILABLE != EVIDENCE_ABSENT.
