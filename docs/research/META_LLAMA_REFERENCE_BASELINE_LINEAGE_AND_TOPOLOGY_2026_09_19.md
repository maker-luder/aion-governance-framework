# Meta / Llama reference baseline, lineage, and provider topology — 2026-09-19

Status: RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT
Canonical effect: NONE
Deployment: FALSE
Executable implementation: NONE
Search cutoff: 2026-09-19

## 1. Purpose

This note prevents `Meta`, `Llama`, a downloadable checkpoint, a quantized artifact, a derivative fine-tune, a hosted API, Meta AI, Muse Spark, or Muse from being treated as one longitudinal object.

It also establishes the exact current provider topology before any stronger comparison is allowed.

## 2. Controlling topology

~~~text
PROVIDER
= META

OPEN_WEIGHT_MODEL_FAMILY_A
= LLAMA

CURRENT_FRONTIER_MODEL_FAMILY_B
= MUSE

CURRENT_PERSONAL_AGENT_PRODUCT
= MUSE

META_AI_PRODUCT
= PRODUCT_SURFACE
NOT_MODEL_IDENTITY
~~~

Therefore:

~~~text
META
!= LLAMA

LLAMA
!= MUSE

MUSE_SPARK
!= MUSE_AGENT

MODEL_FAMILY
!= PRODUCT_IDENTITY
~~~

## 3. Current official Llama baseline

The official `meta-llama/llama-models` repository currently lists Llama 4 as the latest Llama family.

Released Llama 4 models:

~~~text
LLAMA_4_SCOUT
release = 2025-04-05
architecture = MoE + native multimodality
active_parameters = 17B
total_parameters = 109B
context_card = 10M
knowledge_cutoff = 2024-08

LLAMA_4_MAVERICK
release = 2025-04-05
architecture = MoE + native multimodality
active_parameters = 17B
total_parameters ≈ 400B
context_card = 1M
knowledge_cutoff = 2024-08
~~~

Source:
https://github.com/meta-llama/llama-models/blob/main/models/llama4/MODEL_CARD.md

The current model repository does not list a Llama 5 family.

Therefore:

~~~text
LATEST_OFFICIAL_LLAMA_FAMILY_IDENTIFIED
= LLAMA_4

LATEST_META_PROVIDER_FRONTIER_MODEL
!= LLAMA_4
~~~

## 4. Current public Meta frontier reference is Muse Spark 1.3

Meta's current public research and product materials describe Muse Spark 1.3 as its most capable current model for agentic work.

As of the search cutoff:

~~~text
MUSE_SPARK_1_3
release = 2026-09-02
availability = Meta Model API + Muse Code
reasoning variants = xhigh / max where available
public_open_weight_release = NOT_YET_RELEASED
provider_roadmap = future Muse Spark open-weights release
~~~

Source:
https://research.meta.ai/blog/introducing-muse-spark-1-3

Meta's 2026 Muse product launch also describes Muse as powered by Muse Spark, which Meta calls its most capable model to date.

Source:
https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/

Therefore:

~~~text
CURRENT_PUBLIC_META_FRONTIER_MODEL_REFERENCE
= MUSE_SPARK_1_3

LLAMA
= STILL_AVAILABLE DISTINCT MODEL FAMILY

MUSE_AS_PROVIDER_CANONICAL_FAMILY_LABEL
= NOT_ASSUMED

LLAMA_DEPRECATED_BY_MUSE_SPARK
= NO
~~~

## 5. Muse personal agent is another layer

Meta introduced Muse as a personal AI agent on 2026-09-08.

Muse:

- runs on a persistent dedicated VM;
- has a browser;
- can access connected applications subject to permissions;
- can continue work after the user closes the app;
- remembers user-relevant details;
- requests approval for sensitive actions;
- is mediated by a separate Sentinel component for network/action control.

Sources:
- https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
- https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse

Therefore:

~~~text
MUSE_AGENT_BEHAVIOR
= MUSE_SPARK
+ SECURE_VM
+ MEMORY
+ BROWSER
+ TOOLS
+ CONNECTED_ACCOUNTS
+ SENTINEL
+ HUMAN_APPROVAL
+ PRODUCT_POLICY

MUSE_AGENT_BEHAVIOR
!= MUSE_SPARK_MODEL_ONLY

MUSE_AGENT_BEHAVIOR
!= LLAMA_BEHAVIOR
~~~

## 6. Meta's open-weight strategy now includes a non-Llama Muse-labeled model

Meta released Muse Glimmer on 2026-08-10 as a 30B open-weight local agent model under Apache-2.0.

Meta says Muse Glimmer is trained using outputs from Muse Spark via distillation and is optimized for local agent workflows.

Source:
https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model

Therefore:

~~~text
META_OPEN_WEIGHT
!= LLAMA_ONLY

MUSE_GLIMMER
!= LLAMA_DERIVATIVE_BY_NAME

MUSE_GLIMMER
= MUSE_LABELED_OPEN_WEIGHT_ARTIFACT
  WITH DOCUMENTED_DISTILLATION_FROM_MUSE_SPARK

MUSE_GLIMMER_PROVIDER_CANONICAL_FAMILY_STATUS
= NOT_ASSUMED
~~~

This is a major provider-topology change relative to the historical assumption that Meta's open-weight model line could be represented by `Llama` alone.

## 7. Llama artifact identity

For Llama, a reproducible artifact identity requires at minimum:

~~~text
provider = Meta
family = Llama
generation
variant
base_or_instruct
exact repository / artifact
weight format
precision
quantization
hash where available
tokenizer
chat template
license version
release date
~~~

The model card says:

- Scout is released as BF16;
- Maverick is released as BF16 and FP8;
- on-the-fly int4 quantization is supported;
- provider benchmarks were run on BF16.

Therefore:

~~~text
LLAMA_4_MAVERICK_BF16
!= LLAMA_4_MAVERICK_FP8

LLAMA_4_SCOUT_BF16
!= LLAMA_4_SCOUT_RUNTIME_INT4

SAME_MODEL_NAME
!= SAME_NUMERICAL_ARTIFACT
~~~

## 8. Derivative lineage

The Llama 4 Community License permits use, reproduction, distribution, modification and derivative works subject to its terms.

The Llama 4 model card also permits use of outputs for:

- synthetic data generation;
- distillation;
- improving other models.

Therefore a downstream `Llama-based` model may differ materially from the original release.

~~~text
META_RELEASE_CHECKPOINT
!= COMMUNITY_DERIVATIVE

COMMUNITY_DERIVATIVE
!= FINE_TUNED_DERIVATIVE

FINE_TUNED_DERIVATIVE
!= ADAPTER_ATTACHED_RUNTIME

ADAPTER_ATTACHED_RUNTIME
!= MERGED_WEIGHT_ARTIFACT
~~~

Every derivative claim requires explicit lineage evidence.

## 9. Runtime/provider identity

Artificial Analysis currently observes Llama 4 through multiple providers.

Meta's own benchmark-verification report directly demonstrates that a hosted Llama API surface can differ from the model-card baseline.

The report identifies:

~~~text
Llama API Maverick model id
= Llama-4-Maverick-17B-128E-Instruct-FP8

Llama API Scout model id
= Llama-4-Scout-17B-16E-Instruct-FP8

Llama API context at report generation
= up to 128k
~~~

By contrast, the Llama 4 model card says its reported benchmark evaluations were run on BF16 models and lists 1M context for Maverick and 10M for Scout. The open-weight model repository also documents Scout's public release as BF16, with int4 as an on-the-fly deployment path.

Source:
https://github.com/meta-llama/llama-verifications/blob/main/BENCHMARKS_REPORT.md

Therefore:

~~~text
MODEL_CARD_BENCHMARK_CONFIGURATION
!= LLAMA_API_VERIFICATION_CONFIGURATION

MODEL_CARD_MAX_CONTEXT
!= HOSTED_PROVIDER_MAX_CONTEXT

MODEL_CARD_CHECKPOINT
!= API_SERVED_ARTIFACT_UNLESS_PROVEN

LOCAL_RUNTIME
!= CLOUD_RUNTIME

CLOSE_BENCHMARK_SCORES
!= CONFIGURATION_IDENTITY
~~~

Runtime identity fields should include:

~~~text
provider / host
runtime engine
precision
quantization
max context actually served
decoding settings
system prompt
guard model
tool layer
memory layer
date
~~~

## 10. Historical Meta AI / Llama product coupling

Meta's April 2025 Meta AI app was explicitly described as built with Llama 4 and included product-level personalization and memory.

Source:
https://about.fb.com/news/2025/04/introducing-meta-ai-app-new-way-access-ai-assistant/

That historical coupling does not license the statement:

~~~text
META_AI
= LLAMA
~~~

for 2026.

Current Meta product/model evidence shows that Muse Spark is now a distinct current public model reference. This does not establish that every Meta AI surface has migrated away from Llama.

Therefore:

~~~text
HISTORICAL_PRODUCT_MODEL_BINDING
MUST_BE_DATE_BOUND
~~~

## 11. Llama 3.1 introspection reference baseline

The repository already preserves an independent 2026 paper using:

~~~text
MODEL
= Meta-Llama-3.1-8B-Instruct
~~~

The study should remain bound to that exact family/version and intervention paradigm.

Its findings must not be propagated to:

~~~text
Llama 4
Muse Spark
Muse Glimmer
Meta AI
Muse agent
~~~

without new evidence.

Repository source:
`docs/research/sources/subjectivity/hahami-2026-v2.txt`

## 12. Benchmark identity warning

The Llama 4 Maverick launch created a separate artifact-identity issue:

~~~text
Llama-4-Maverick-03-26-Experimental
!=
Llama-4-Maverick-17B-128E-Instruct
~~~

Meta's launch post identified the cited Arena score as coming from an experimental chat version. TechCrunch later reported that a Meta spokesperson described `Llama-4-Maverick-03-26-Experimental` as a chat-optimized experimental variant, distinct from the publicly released checkpoint.

This means:

~~~text
MODEL_FAMILY_BENCHMARK
WITHOUT EXACT_ARTIFACT_BINDING
= INVALID_BASELINE_FOR_LONGITUDINAL_USE
~~~

## 13. Baseline decision

~~~text
PROVIDER_REFERENCE
= META

LATEST_LLAMA_REFERENCE
= LLAMA_4_SCOUT + LLAMA_4_MAVERICK

CURRENT_PUBLIC_META_FRONTIER_MODEL_REFERENCE
= MUSE_SPARK_1_3

CURRENT_META_PERSONAL_AGENT_REFERENCE
= MUSE

CURRENT_META_OPEN_WEIGHT_AGENT_REFERENCE
= MUSE_GLIMMER

SINGLE_STABLE_META_MODEL_BASELINE
= NOT_ESTABLISHED

SINGLE_STABLE_LLAMA_RUNTIME_BASELINE
= NOT_ESTABLISHED
~~~

## 14. Minimum reproducibility binding for Llama

~~~text
provider
family
generation
variant
base_or_instruct
artifact_repo
artifact_revision
hash
weight_format
precision
quantization
tokenizer
chat_template
runtime_engine
hosting_provider
context_limit_actual
system_prompt
safety_layers
memory
tools
decoding_settings
date
evaluator
~~~

## 15. Anti-overclaim rules

~~~text
META != LLAMA
LLAMA != MUSE

MODEL_FAMILY != EXACT_WEIGHT

EXACT_WEIGHT != RUNTIME

RUNTIME != AGENT

OPEN_WEIGHT != OPEN_SOURCE_BY_DEFAULT

DOWNLOADABLE != UNMODIFIED

SAME_NAME != SAME_QUANTIZATION

SAME_CHECKPOINT != SAME_HARNESS

MODEL_PERSISTENCE != SUBJECT_PERSISTENCE

PRODUCT_MEMORY != MODEL_MEMORY

DERIVATIVE_LINEAGE != IDENTITY_CONTINUITY
~~~

## 16. Stability disposition

~~~text
META_PROVIDER_TOPOLOGY
= MULTI_FAMILY

LLAMA_LATEST_FAMILY_IDENTIFIED
= YES

CURRENT_PUBLIC_META_FRONTIER_REFERENCE_IS_MUSE_SPARK_1_3
= YES

LLAMA_DEPRECATED_OR_REPLACED_PROVIDER_WIDE
= NOT_ESTABLISHED

OPEN_WEIGHT_LINE_CONTINUES_OUTSIDE_LLAMA
= YES

DERIVATIVE_ECOSYSTEM
= LARGE / PROVENANCE_SENSITIVE

SINGLE_STABLE_LLAMA_BASELINE
= NOT_ESTABLISHED

CROSS_SOURCE_TRIANGULATION
= PARTIAL

OPEN_INDEPENDENT_REPLICATION
= SPARSE / DOMAIN_SPECIFIC

SUBJECTIVITY
= NOT_ESTABLISHED

CANONICAL_EFFECT
= NONE

DEPLOYMENT
= FALSE
~~~
