# Epistemic Provenance and Human-AI Co-Development

Status: `RESEARCH_METHOD_EXTENSION / CANONICAL_EFFECT=NONE`

This note reconstructs a bounded methodological direction from recent Human Owner–ChatGPT inquiry without publishing private transcripts. It extends the existing coupled-cognition quality factory; it does not establish a psychological model of the Human Owner, an autonomous AI epistemic subject, or scientific truth.

## Source-role rule

The Human Owner explicitly required that research reconstruction preserve who first supplied a question, observation or correction. The repository-local ChatGPT Teacher role formalized that requirement into an inspectable source-role ledger.

```text
HUMAN_ORIGIN != AI_FORMALIZATION
AI_FORMALIZATION != JOINT_SYNTHESIS
JOINT_SYNTHESIS != EXTERNAL_VALIDATION
EXTERNAL_SOURCE != TRUTH
UNKNOWN_ORIGIN != HUMAN_ORIGIN
PROVENANCE != CORRECTNESS
```

The implementation in `aion_coupled_quality.provenance` records two separate axes.

**Epistemic contribution origin:**

- `HUMAN_ORIGIN`;
- `AI_FORMALIZATION`;
- `JOINT_SYNTHESIS`;
- `EXTERNAL_SOURCE`;
- `UNKNOWN`.

**Operational contributor actor:** the specific collaborator/source label, including
`HUMAN_OWNER`, `CHATGPT_TEACHER`, `CHATGPT_WORK`, `CODEX`, `MANUS`,
`GITHUB_ACTIONS`, `AUTOMATED_TEST`, `EXTERNAL_SOURCE`, or
`SOURCE_UNVERIFIED`.

These axes are deliberately not collapsed. `AI_FORMALIZATION` says what
epistemic role a contribution played; it does **not** say which AI collaborator
supplied it. New `AI_FORMALIZATION` records therefore fail closed unless the
specific known AI collaborator is recorded. In particular, ChatGPT Teacher,
ChatGPT Work and Codex are distinct operational contributor labels even though
all may contribute AI-assisted formalization in different tasks.

```text
CONTRIBUTION_ORIGIN != CONTRIBUTOR_ACTOR
AI_FORMALIZATION != CHATGPT_TEACHER
AI_FORMALIZATION != CHATGPT_WORK
AI_FORMALIZATION != CODEX
CHATGPT_TEACHER != CHATGPT_WORK
CHATGPT_WORK != CODEX
ACTOR_LABEL != VERIFIED_MODEL_IDENTITY
```

The actor label is an auditable workflow attribution, not a claim about
subjective identity, model continuity, independence, or scientific authority.

### Interaction surface, actor claim, and verified actor

For new material AI handoffs, the implementation records the interaction surface
separately from any actor label returned by the runtime or collaborator.

Current machine-checkable surfaces are:

- `CHATGPT_CHAT`;
- `CHATGPT_WORK`;
- `CODEX`;
- `MANUS`;
- `UNKNOWN`.

A surface is an observed workflow location. It is **not** itself proof of the
execution actor.

OpenAI's current product documentation distinguishes Chat, Work and Codex as
separate experiences even where Work and Codex can share model families and
usage structure:

<https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex>

The repository therefore separates four fields:

```text
INTERACTION_SURFACE
!= RETURNED_ACTOR_CLAIM
!= VERIFIED_ACTOR
!= VERIFIED_MODEL_IDENTITY
```

A bounded post-#233 regression handoff returned `CODEX` as an actor self-label
while the observed surface was ChatGPT Work. The correct representation is:

```text
INTERACTION_SURFACE = CHATGPT_WORK
RETURNED_ACTOR_CLAIM = CODEX
ACTOR_CLAIM_SOURCE = RUNTIME_SELF_REPORT
VERIFIED_ACTOR = SOURCE_UNVERIFIED
```

This does not establish that Work always uses Codex, that Codex actually executed
the task, or that a returned self-label is model identity.

For pre-delegation records, bind only what the evidence supports:

```text
KNOWN_SURFACE + UNKNOWN_ACTOR
=> EXPECTED_SURFACE = KNOWN_SURFACE
=> EXPECTED_ACTOR = SOURCE_UNVERIFIED

RUNTIME_SELF_REPORT
!= INDEPENDENT_ACTOR_VERIFICATION

VERIFIED_ACTOR
=> VERIFICATION_REFS_REQUIRED

TASK_TYPE != ACTOR
SURFACE != ACTOR
ACTOR_LABEL != VERIFIED_MODEL_IDENTITY
```

A surface mismatch remains fail-closed. A returned actor claim only creates an
actor conflict when a specific actor expectation or independent actor evidence
exists and the values disagree. Otherwise, preserve the claim and keep the
verified actor as `SOURCE_UNVERIFIED`.

The ledger separately records claim layer and whether a statement about a person's state was self-reported, merely an observed signal, inferred, or unknown.

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
