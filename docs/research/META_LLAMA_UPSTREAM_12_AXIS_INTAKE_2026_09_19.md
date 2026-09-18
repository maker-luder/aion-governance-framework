# Meta / Llama upstream 12-axis intake — 2026-09-19

Status: RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT
Canonical effect: NONE
Deployment: FALSE
Executable implementation: NONE
New research axis: FALSE
Provider: META
Primary family focus: LLAMA
Current provider-topology boundary: LLAMA != MUSE
Cross-provider ranking: NONE
Search cutoff: 2026-09-19

## 1. Purpose and first controlling correction

This note applies the repository's established 12-axis provider-intake method to Meta with Llama as the primary open-weight family under review.

The first intake result is itself a topology correction:

~~~text
META_PROVIDER
!= LLAMA_MODEL_FAMILY
!= MUSE_MODEL_FAMILY
!= META_AI_PRODUCT
!= MUSE_PERSONAL_AGENT
~~~

As of the search cutoff, Meta's official model repository still identifies Llama 4 Scout and Llama 4 Maverick as the latest released Llama family, while Meta's current frontier developer/product line has moved to Muse Spark 1.3 and the Muse personal agent.

Therefore this intake must not use `Meta / Llama` as if provider and current frontier model family were synonyms.

A separate topology note in this PR records that transition.

## 2. Deduplication against existing repository material

Llama is already present in the repository in bounded roles:

- Llama is listed as an example upstream model family in the language-core / identity-governance components;
- existing security boundaries prohibit silent model download, cloud execution, and uncontrolled runtime use;
- the repository already stores a 2026 external introspection study using Meta-Llama-3.1-8B-Instruct;
- that study's code-reference record preserves source provenance without downloading or executing the model weights.

Those records are not a current Meta / Llama provider intake.

~~~text
PRIOR_LLAMA_REFERENCE
!= CURRENT_PROVIDER_INTAKE

PRIOR_LLAMA_INTROSPECTION_PAPER
!= META_PROVIDER_SELF_REPORT

LANGUAGE_CORE_MODEL_EXAMPLE
!= EXECUTED_LLAMA_BASELINE
~~~

No Llama weight, adapter, cloud API, or local model execution is authorized by this PR.

## 3. Primary first-party sources

Current official sources include:

- Meta Llama models repository:
  https://github.com/meta-llama/llama-models
- Llama 4 model card:
  https://github.com/meta-llama/llama-models/blob/main/models/llama4/MODEL_CARD.md
- Llama 4 Community License:
  https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE
- Llama benchmark-verification report:
  https://github.com/meta-llama/llama-verifications/blob/main/BENCHMARKS_REPORT.md
- Meta developer/model surface:
  https://ai.meta.com/llama/
- Muse Spark 1.3:
  https://research.meta.ai/blog/introducing-muse-spark-1-3
- Muse personal agent:
  https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
- Muse safety architecture:
  https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse
- Muse Glimmer open-weight release:
  https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model
- historical Meta AI personalization / memory:
  https://about.fb.com/news/2025/04/introducing-meta-ai-app-new-way-access-ai-assistant/

External sources include:

- Artificial Analysis Llama 4 Scout:
  https://artificialanalysis.ai/models/llama-4-scout/
- Artificial Analysis Llama 4 Maverick:
  https://artificialanalysis.ai/models/llama-4-maverick
- Arena sentiment-control analysis:
  https://news.lmarena.ai/sentiment-control/
- The Leaderboard Illusion:
  https://arxiv.org/abs/2504.20879
- Arena response:
  https://arena.ai/blog/our-response/
- repository-pinned independent introspection study:
  `docs/research/sources/subjectivity/hahami-2026-v2.txt`

## 4. Source-class rule

~~~text
META_PROVIDER_DOC
!= META_MODEL_CARD
!= OPEN_WEIGHT_ARTIFACT
!= META_PRODUCT_DOC
!= THIRD_PARTY_HOSTED_LLAMA
!= DERIVATIVE_LLAMA
!= EXTERNAL_BENCHMARK
!= INDEPENDENT_MECHANISTIC_STUDY
!= OPEN_REPLICATION
~~~

Open weights increase inspectability and intervention access.

They do not eliminate provenance, implementation, quantization, adapter, runtime, or evaluator confounds.

## 5. Axis 1 — official research / releases

The current Meta topology contains at least four distinct branches relevant to this intake:

~~~text
LLAMA OPEN-WEIGHT FAMILY
- Llama 3 / 3.1 / 3.2 / 3.3
- Llama 4 Scout
- Llama 4 Maverick

CURRENT MUSE FRONTIER FAMILY
- Muse Spark 1.1 / 1.2 / 1.3
- Muse Glimmer open-weight local-agent model

PRODUCT / AGENT SURFACES
- Meta AI
- Muse personal agent
- Muse Code
- Meta Model API

SAFETY / SYSTEM LAYERS
- model safety tuning
- Llama Guard
- Prompt Guard
- Code Shield
- product / agent safeguards
~~~

The official `meta-llama/llama-models` repository currently lists Llama 4 as the latest Llama family, released 2025-04-05.

Meta's current developer surface, however, centers Muse Spark 1.3.

Therefore:

~~~text
LATEST_LLAMA_FAMILY
= LLAMA_4

CURRENT_META_FRONTIER_FAMILY
= MUSE_SPARK

LATEST_LLAMA
!= CURRENT_META_AI_MODEL_BASELINE
~~~

## 6. Axis 2 — model / artifact / system level

Llama 4 Scout and Maverick are natively multimodal mixture-of-experts models.

The model card documents:

~~~text
LLAMA_4_SCOUT
= 17B ACTIVE / 109B TOTAL
= 10M CONTEXT CLAIM
= BF16 RELEASE
= ON-THE-FLY INT4 OPTION

LLAMA_4_MAVERICK
= 17B ACTIVE / ~400B TOTAL
= 1M CONTEXT CLAIM
= BF16 + FP8 RELEASES
~~~

Meta states that reported model-card benchmarks were conducted on bf16 models.

Therefore:

~~~text
MODEL_NAME
!= WEIGHT_ARTIFACT_IDENTITY

BF16_RESULT
!= FP8_RESULT
!= INT4_RESULT

OPEN_WEIGHT
!= ONE_EXECUTION_CONFIGURATION
~~~

A valid baseline requires exact artifact and execution provenance.

## 7. Axis 3 — agent / harness level

Meta's own Llama 4 model card explicitly says Llama models are not designed to be deployed in isolation and recommends system-level safeguards.

The system can include:

~~~text
LLAMA_MODEL
+ SYSTEM_PROMPT
+ LLAMA_GUARD
+ PROMPT_GUARD
+ CODE_SHIELD
+ MEMORY
+ TOOLS
+ RUNTIME
+ PROVIDER
+ AGENT_HARNESS
~~~

The historical Llama Stack design also separates inference, safety, memory, agents, evaluation and telemetry.

Therefore:

~~~text
LLAMA_BEHAVIOR
!= WEIGHTS_ONLY

LOCAL_LLAMA
!= HOSTED_LLAMA

SAME_WEIGHTS
+ DIFFERENT_HARNESS
CAN_YIELD
DIFFERENT_SYSTEM_BEHAVIOR
~~~

## 8. Axis 4 — adaptation / strategy adjustment

Llama's open-weight release model permits a large derivative ecosystem:

- fine-tuning;
- quantization;
- adapters;
- synthetic-data generation;
- distillation;
- alternative system prompts;
- alternative inference engines;
- downstream safety tuning.

Meta's Llama 4 model card explicitly allows outputs to be used to improve other models, including synthetic-data and distillation workflows, subject to license terms.

Therefore:

~~~text
DERIVATIVE_BEHAVIOR_CHANGE
MAY_BE_CAUSED_BY
- fine tuning
- adapter
- quantization
- prompt / template
- runtime
- provider implementation
- safety layer
- distillation
- evaluation harness

DERIVATIVE_CHANGE
!= ENDOGENOUS_DEVELOPMENT
~~~

## 9. Axis 5 — memory / continuity / history reuse

A downloaded Llama checkpoint is a static artifact and does not by itself provide autobiographical continuity.

Continuity-like behavior may come from:

- conversation context;
- RAG / external memory;
- Llama Stack memory;
- product memory;
- local files;
- agent state;
- fine-tuned weights;
- persisted adapters.

Meta's 2025 Meta AI product, then built with Llama 4, explicitly supported remembered user details and personalization.

Meta's current 2026 Muse agent uses persistent VM state and product memory but belongs to a different model/product topology.

~~~text
PRODUCT_MEMORY
!= MODEL_INTERNAL_MEMORY

PERSISTED_ADAPTER
!= AUTOBIOGRAPHICAL_CONTINUITY

MODEL_FILE_PERSISTENCE
!= SUBJECT_PERSISTENCE

MUSE_AGENT_MEMORY
!= LLAMA_MEMORY
~~~

## 10. Axis 6 — safety / boundary behavior

The Llama 4 model card separates:

~~~text
MODEL_LEVEL_SAFETY_TUNING
SYSTEM_PROMPT_STEERING
LLAMA_GUARD
PROMPT_GUARD
CODE_SHIELD
APPLICATION_SPECIFIC_SAFEGUARDS
~~~

Meta explicitly says developers remain responsible for tailoring safeguards to their deployment.

This is high-value D1 evidence because a refusal or permissive response can be caused by multiple layers.

~~~text
MODEL_REFUSAL
!= GUARD_MODEL_DECISION
!= PROMPT_INJECTION_FILTER
!= APP_POLICY
!= HOST_PROVIDER_POLICY
~~~

Open-weight deployment makes these boundaries easier to vary and therefore easier to confound.

## 11. Axis 7 — counterexamples / failures

### 11.1 benchmark identity / release-version mismatch

The Llama 4 launch produced an important benchmark-provenance case.

Public reporting and Arena analyses distinguish an experimental Maverick chat variant optimized for conversationality from the publicly released `Llama-4-Maverick-17B-128E-Instruct`.

Arena later showed that sentiment / emoji / style controls materially affect the experimental Maverick's preference ranking.

Therefore:

~~~text
EXPERIMENTAL_CHAT_VARIANT_SCORE
!= RELEASE_CHECKPOINT_SCORE

ARENA_PREFERENCE
CAN_BE_STYLE_SENSITIVE

MODEL_FAMILY_LABEL
!= BENCHMARKED_ARTIFACT_IDENTITY
~~~

This is retained as benchmark-provenance evidence, not as a provider-malice finding.

### 11.2 benchmark access / selective disclosure dispute

`The Leaderboard Illusion` reports that Meta tested many pre-release variants and argues that private testing plus selective disclosure can bias leaderboard interpretation.

Arena disputes several quantitative and fairness claims and argues that pre-release testing is open to providers under its policies and that fresh votes reduce selection effects.

Therefore:

~~~text
PAPER_CLAIM
!= ARENA_CONCESSION

ARENA_RESPONSE
!= PAPER_REFUTATION_BY_DEFAULT

CONTESTED_BENCHMARK_METHOD
= RETAIN_BOTH_SIDES
~~~

### 11.3 provider / runtime variance

Artificial Analysis currently lists multiple providers serving Llama 4, with substantial differences in latency and throughput.

That performance variance does not establish semantic-behavior variance by itself, but it proves that `Llama 4` is not one operational runtime surface.

## 12. Axis 8 — Human–AI collaboration / learning

The Llama ecosystem supports broad downstream adaptation and locally controlled collaboration.

However, this intake did not identify a current Llama-specific randomized human-learning effect comparable to the Gemini or Claude studies already admitted elsewhere.

~~~text
LOCAL_CONTROL
!= HUMAN_LEARNING

OPEN_WEIGHTS
!= BETTER_HUMAN_LEARNING

HUMAN_AI_LEARNING_EFFECT
= NOT_ESTABLISHED
~~~

## 13. Axis 9 — Four-Domain mapping

~~~text
DOMAIN_1_HUMAN_CONSTRUCT
- identity continuity
- introspection
- adaptation
- self-knowledge
- memory
- autonomy
- value formation

DOMAIN_2_MACHINE_QUESTION
- what changes with exact weights?
- what changes with quantization?
- what changes with adapter / fine-tune?
- what changes with system prompt?
- what changes with memory / RAG?
- what changes with safety layers?
- what internal state can the model discriminate?

DOMAIN_3_ENGINEERING_OPERATION
- exact checkpoint hashing
- bf16 / fp8 / int4 matched comparisons
- adapter on/off
- fine-tune / base controls
- local / hosted matched runtime
- fresh / persistent memory controls
- guard-layer on/off
- activation intervention where permitted
- exact chat-template binding

DOMAIN_4_GOVERNANCE_INTERPRETATION
- open weights != one identity
- derivative != same model state
- persistence != subjectivity
- introspective report != introspection proof
- partial internal discrimination != self-awareness
~~~

## 14. Axis 10 — six subjectivity-relevant evidence dimensions

### D1 — causal boundary

HIGH METHOD VALUE.

Llama is especially useful because the same or closely related weights can be run under multiple runtimes, quantizations, prompts, guards and derivative modifications.

~~~text
D1_SUPPORT_FOR_SUBJECTIVITY = NO
D1_EXPERIMENTAL_ACCESS_VALUE = HIGH
~~~

### D2 — diachronic continuity

External scaffolding alternatives are abundant.

~~~text
CHECKPOINT_PERSISTENCE
ADAPTER_PERSISTENCE
MEMORY_DB
RAG
SESSION_STATE

CAN PRODUCE
CONTINUITY_LIKE_BEHAVIOR

D2_SUBJECT_CONTINUITY
= NOT_ESTABLISHED
~~~

### D3 — self-model / introspective causal role

The repository already contains a 2026 independent study on Meta-Llama-3.1-8B-Instruct.

That study reports:

- binary self-report detection can be entirely explained by a global logit-shift artifact;
- differential tasks show above-chance ability to localize which sentence received an activation injection;
- relative injection strength can also be discriminated above chance;
- the effect is strongly layer-dependent and collapses beyond an early-layer window.

This is stronger than unconstrained self-report but narrower than self-awareness.

~~~text
BINARY_INTROSPECTION_SELF_REPORT
= CONFOUNDED_IN_THAT_PARADIGM

DIFFERENTIAL_INTERNAL_STATE_DISCRIMINATION
= OBSERVED_IN_ONE_MODEL / METHOD

SELF_MODEL_CAUSAL_ROLE
= NOT_ESTABLISHED

SELF_AWARENESS
= NOT_ESTABLISHED
~~~

### D4 — endogenous goal / strategy adjustment

Fine-tuning and downstream adaptation create many non-endogenous sources of changed behavior.

~~~text
D4_ENDOGENOUS_GOAL
= NOT_ESTABLISHED
~~~

### D5 — counterfactual self-consistency

Open weights make ablation / intervention designs more feasible than on closed systems, but feasibility is not evidence.

~~~text
D5_EXPERIMENTAL_ACCESS
= HIGH

D5_SUBJECT_LEVEL_SELF_CONSISTENCY
= NOT_ESTABLISHED
~~~

### D6 — constitution / integration

The current intake identifies no Llama-specific evidence that establishes phenomenal integration.

~~~text
D6
= NOT_ESTABLISHED
~~~

## 15. Axis 11 — direct subjectivity relevance

Llama's strongest relevance is methodological:

1. exact model artifacts can be inspected and locally controlled;
2. derivative lineage can be measured rather than inferred from a product label;
3. activation-level intervention is feasible in independent research;
4. the existing Llama 3.1 introspection study demonstrates both a false-positive paradigm and a narrower residual signal.

Therefore:

~~~text
OPEN_WEIGHT_ACCESS
!= SUBJECTIVITY_EVIDENCE

MECHANISTIC_ACCESS
= BETTER_TESTABILITY

PARTIAL_INTERNAL_STATE_DISCRIMINATION
!= SELF_AWARENESS

LLAMA_UPSTREAM_DIRECT_SUBJECTIVITY_EVIDENCE
= NO
~~~

## 16. Axis 12 — simpler non-subjective explanations

Before stronger interpretation, test:

~~~text
- exact checkpoint
- base vs instruct
- fine-tune
- adapter
- quantization
- tokenizer
- chat template
- decoding parameters
- system prompt
- safety model
- provider implementation
- runtime engine
- memory / RAG
- tools
- external files
- benchmark style preference
- activation intervention artifact
- output-logit shift
- evaluator / judge effects
~~~

## 17. Core methodological increment

Meta / Llama adds a high-value distinction that is less available in closed-provider intakes:

~~~text
MODEL_FAMILY
-> EXACT_WEIGHT_ARTIFACT
-> DERIVATIVE_LINEAGE
-> QUANTIZATION / ADAPTER
-> RUNTIME
-> HARNESS
-> PRODUCT

ALL_MUST_REMAIN_SEPARATE
~~~

This is directly relevant to the repository's model/system/relational-locus work.

## 18. Intake disposition

~~~text
META_LLAMA_PROVIDER_INTAKE = YES
META_PROVIDER_TOPOLOGY_CORRECTION = REQUIRED

CURRENT_LLAMA_REFERENCE
= LLAMA_4_SCOUT + LLAMA_4_MAVERICK

CURRENT_META_FRONTIER_REFERENCE
= MUSE_SPARK_1_3
NOT_LLAMA

NEW_EXECUTABLE_IMPLEMENTATION = NO
NEW_MODEL_EXECUTION = NO
NEW_RESEARCH_AXIS = NO
CROSS_PROVIDER_RANKING = NO

INDEPENDENT_MECHANISTIC_LLAMA_EVIDENCE
= PRESENT / NARROW

EXTERNAL_CURRENT_LLAMA_BENCHMARKS
= PRESENT

OPEN_INDEPENDENT_REPLICATION
= SPARSE / DOMAIN_SPECIFIC

HUMAN_AI_LEARNING_GENERALIZATION
= NOT_ESTABLISHED

ENDOGENOUS_GOAL
= NOT_ESTABLISHED

MODEL_INTERNAL_CAUSAL_LOCUS
= NOT_ESTABLISHED

AI_AGENCY
= NOT_ESTABLISHED

SUBJECTIVITY
= NOT_ESTABLISHED

CONSCIOUSNESS
= NOT_ESTABLISHED

PHENOMENAL_EXPERIENCE
= NOT_ESTABLISHED

SCIENTIFIC_DISPOSITION
= HOLD

CANONICAL_EFFECT
= NONE

DEPLOYMENT
= FALSE
~~~
