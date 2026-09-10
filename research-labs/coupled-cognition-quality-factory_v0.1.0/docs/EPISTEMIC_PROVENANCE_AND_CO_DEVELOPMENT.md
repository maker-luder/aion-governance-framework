# Epistemic Provenance and Human-AI Co-Development

Status: `RESEARCH_METHOD_EXTENSION / CANONICAL_EFFECT=NONE`

This note reconstructs a bounded methodological direction from recent Human Owner–ChatGPT inquiry without publishing private transcripts. It extends the existing coupled-cognition quality factory; it does not establish a psychological model of the Human Owner, an autonomous AI epistemic subject, or scientific truth.

## Source-role rule

The Human Owner explicitly required that research reconstruction preserve who first supplied a question, observation or correction. ChatGPT formalized that requirement into an inspectable source-role ledger.

```text
HUMAN_ORIGIN != AI_FORMALIZATION
AI_FORMALIZATION != JOINT_SYNTHESIS
JOINT_SYNTHESIS != EXTERNAL_VALIDATION
EXTERNAL_SOURCE != TRUTH
UNKNOWN_ORIGIN != HUMAN_ORIGIN
PROVENANCE != CORRECTNESS
```

The implementation in `aion_coupled_quality.provenance` records:

- `HUMAN_ORIGIN`;
- `AI_FORMALIZATION`;
- `JOINT_SYNTHESIS`;
- `EXTERNAL_SOURCE`;
- `UNKNOWN`.

It separately records claim layer and whether a statement about a person's state was self-reported, merely an observed signal, inferred, or unknown.

A specific failure class is prohibited: input content must not silently become a claim about the contributor's internal state. For example, posting a surprising article does not by itself establish that the poster was surprised.

```text
INPUT_CONTENT != USER_AFFECT
OBSERVED_SIGNAL != INTERNAL_STATE
INFERRED_STATE != SELF_REPORT
SELF_REPORT != INDEPENDENT_MEASUREMENT
```

## Problem decomposition as epistemic control

The recent interaction rule can be operationalized as a research discipline:

```text
question
-> definitions
-> premises
-> subquestions
-> observations / source reports
-> inference
-> hypothesis
-> counterevidence / falsifier
-> revision or hold
```

This does not mean every conversation must be mechanically serialized. The point is to prevent a model-generated conclusion from being retroactively rewritten as a Human Owner premise, and to preserve uncertainty when the evidence does not determine an answer.

## Human-AI learning is a separate research object

Recent literature supports studying long-running human-AI inquiry as more than answer retrieval, while also warning against cognitive offloading and displaced human judgment.

Primary/authoritative publication anchors checked in September 2026:

1. Desvaux C, Abdelghani R, Oudeyer P-Y, Sauzéon H (2026), *Curiosity and metacognition: Towards a unified framework for learning and education in the age of AI*, Advances in Child Development and Behavior 70:273-309. DOI `10.1016/bs.acdb.2026.04.005`. The review explicitly discusses transforming generative AI from a cognitive shortcut into a partner for sustained epistemic development.
2. Wu J-Y, Lee Y-H, Chai C-S, Tsai C-C (2025), *Strengthening Human Epistemic Agency in the Symbiotic Learning Partnership With Generative Artificial Intelligence*, Educational Researcher 54(6):358-368. DOI `10.3102/0013189X251333628`. This conceptual work argues for preserving active human epistemic agency in repeated GenAI interaction.
3. *Learning with machines: Toward a theory of epistemic co-agency* (2026), Computers and Education: Artificial Intelligence 10:100573. DOI `10.1016/j.caeai.2026.100573`. It proposes epistemic co-agency as a reflexive stance involving challenge, contradiction surfacing and retained human epistemic responsibility.

These sources motivate a methodological research question; they do not validate this repository's particular interaction history or establish AI subjectivity.

## Bounded research hypothesis

A useful longitudinal human-AI collaboration should preserve or increase the human participant's ability to:

- formulate and decompose questions;
- distinguish observation from inference;
- request and inspect sources;
- generate alternative explanations;
- identify what would falsify a favored hypothesis;
- correct the AI and preserve correction provenance;
- independently restate or apply the resulting method.

A conversation that only increases answer volume, fluency or agreement does not satisfy this hypothesis.

Candidate falsifiers include persistent source-blind acceptance, increasing inability to solve comparable tasks without AI, loss of contribution provenance, systematic confirmation loops, or repeated substitution of AI confidence for independent evidence.

```text
LONG_INTERACTION != EPISTEMIC_DEVELOPMENT
AI_HELP != LEARNING
AGREEMENT != UNDERSTANDING
COHERENCE != TRUTH
CO_AGENCY != AI_SUBJECTIVITY
```

## Implementation boundary

The provenance ledger is an engineering control for source-role integrity. It does not score a person's learning, infer personality, measure intelligence, or assign epistemic worth. Any future co-development evaluation requires explicit longitudinal task design, held-out transfer measures, counterfactual comparison and human-subject research review where applicable.

`CANONICAL_EFFECT = NONE`
`DEPLOYMENT = FALSE`
`SUBJECTIVITY = NOT_ESTABLISHED`
