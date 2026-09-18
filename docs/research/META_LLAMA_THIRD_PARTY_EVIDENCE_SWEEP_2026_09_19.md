# Meta / Llama third-party evidence sweep — 2026-09-19

Status: RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT
Canonical effect: NONE
Deployment: FALSE
Executable implementation: NONE
Search cutoff: 2026-09-19

## 1. Purpose

This note separates Meta first-party Llama claims from independent or externally controlled observations before Llama evidence is re-admitted.

It also prevents current Muse evidence from being silently counted as Llama evidence.

~~~text
META_PROVIDER
CAN_HAVE
MULTIPLE_MODEL_FAMILIES

MUSE_EVIDENCE
!= LLAMA_EVIDENCE
~~~

## 2. Evidence classes

~~~text
E0 = PROVIDER SELF-REPORT

E1 = PROVIDER-ENABLED OR PARTNERED EXTERNAL EVALUATION

E2 = EVALUATOR-CONTROLLED EXTERNAL TEST

E3 = BOUNDED INDEPENDENT INCIDENT / MECHANISTIC INVESTIGATION

E4 = OPEN INDEPENDENT REPLICATION
~~~

These are evidence-shape classes, not a scalar ranking.

## 3. Artificial Analysis — Llama 4 Scout

Source:
https://artificialanalysis.ai/models/llama-4-scout/

Artificial Analysis independently measures Llama 4 Scout through available serving providers and publishes:

- intelligence/capability measurements;
- speed;
- latency;
- cost;
- context specifications;
- provider availability.

Classification:

~~~text
E2_CANDIDATE
= EXTERNAL_EVALUATOR_MEASUREMENT
~~~

Methodological value:

~~~text
EXTERNAL_SCORE
!= MECHANISM

PROVIDER_MEDIAN_OR_HOSTED_MEASUREMENT
!= EXACT_LOCAL_WEIGHT_EXECUTION
~~~

The result is useful for current external performance observation, not for subjectivity.

## 4. Artificial Analysis — Llama 4 Maverick

Source:
https://artificialanalysis.ai/models/llama-4-maverick

Artificial Analysis measures Llama 4 Maverick as an open-weight model and reports current benchmark and serving characteristics.

Classification:

~~~text
E2_CANDIDATE
= EXTERNAL_EVALUATOR_MEASUREMENT
~~~

The observed system should be interpreted as:

~~~text
LLAMA_4_MAVERICK
+ SERVING_PROVIDER
+ SERVING_PRECISION / IMPLEMENTATION
+ EVALUATION_HARNESS
~~~

not simply as an abstract family score.

## 5. Provider-surface variance

Artificial Analysis provider pages show large differences in throughput and latency across Llama 4 serving providers.

Sources:
- https://artificialanalysis.ai/models/llama-4-maverick/providers/
- https://artificialanalysis.ai/models/llama-4-scout/providers/

This does not by itself prove semantic-output divergence.

It does establish:

~~~text
LLAMA_MODEL_NAME
!= ONE_OPERATIONAL_SURFACE

HOSTING_PROVIDER
= REPRODUCIBILITY_VARIABLE
~~~

## 6. Llama 4 Maverick Arena artifact-identity issue

Public reporting on the Llama 4 launch distinguishes:

~~~text
Llama-4-Maverick-03-26-Experimental
FROM
Llama-4-Maverick-17B-128E-Instruct
~~~

The experimental version was optimized for conversationality and appeared in Arena before the public release version was separately evaluated.

Secondary source:
https://techcrunch.com/2025/04/06/metas-benchmarks-for-its-new-ai-models-are-a-bit-misleading/

The strongest admissible methodological conclusion is:

~~~text
BENCHMARKED_VARIANT
MUST_MATCH
RELEASED_VARIANT
FOR DIRECT PRODUCT CLAIMS
~~~

This is a provenance issue.

It is not sufficient evidence for a general claim that provider benchmarks are invalid or fraudulent.

## 7. Arena sentiment-control evidence

Arena later published a style/sentiment-control analysis.

Source:
https://news.lmarena.ai/sentiment-control/

Arena reports that controlling for style, sentiment, and emoji usage changes rankings and specifically identifies `Llama-4-Maverick-Experimental` as a model whose rank drops under those controls.

Classification:

~~~text
E2_METHOD_ANALYSIS
= EXTERNAL_EVALUATOR_REANALYSIS
~~~

Method consequence:

~~~text
HUMAN_PREFERENCE_SCORE
CAN_BE_INFLUENCED_BY
STYLE / SENTIMENT / EMOJI FEATURES

PREFERENCE_RANK
!= PURE_CAPABILITY_MEASURE
~~~

This is directly relevant to the repository's evaluator-confound register.

## 8. The Leaderboard Illusion — pre-release testing critique

Source:
https://arxiv.org/abs/2504.20879

The paper argues that private pre-release testing and selective disclosure can distort leaderboard interpretation and reports that Meta tested 27 private model variants before the Llama 4 release.

Classification:

~~~text
E2_EVALUATION_GOVERNANCE_ANALYSIS
= EXTERNAL_RESEARCH_CLAIM
~~~

The paper's quantitative and policy claims are contested.

Therefore the repository must not treat the paper as uncontested adjudication.

## 9. Arena response to The Leaderboard Illusion

Source:
https://arena.ai/blog/our-response/

Arena accepts that some recommendations are useful but disputes several claims about fairness, score inflation, hidden policy, and the magnitude of pre-release selection effects.

Arena also states planned or strengthened disclosure practices around pre-release testing and provisional scores.

Therefore:

~~~text
LEADERBOARD_ILLUSION_CLAIM
!= ESTABLISHED_FACT_BY_PAPER_ALONE

ARENA_RESPONSE
!= AUTOMATIC_REFUTATION

CONTESTED_EVALUATION_METHOD
= PRESERVE_CLAIM + RESPONSE + UNCERTAINTY
~~~

This is a high-value case for the repository's evidence-admission method.

## 10. Independent Llama 3.1 introspection study already pinned in repository

Repository source:
`docs/research/sources/subjectivity/hahami-2026-v2.txt`

External preprint:
https://arxiv.org/abs/2512.12411

Model:
`Meta-Llama-3.1-8B-Instruct`

The study reports a two-part result.

First, a binary detection paradigm such as asking whether the model detected an injected internal concept can be explained by global output-logit shifts toward affirmative responses.

~~~text
BINARY_DETECTION_SUCCESS
= METHODOLOGICALLY_CONFOUNDED
IN_THAT_PARADIGM
~~~

Second, more discriminative tasks show above-chance performance for:

- localizing which of multiple sentences received an activation injection;
- discriminating relative injection strength.

The effect is concentrated in early-layer interventions and collapses later.

Classification:

~~~text
E3_CANDIDATE
= INDEPENDENT_MECHANISTIC_INTERVENTION_STUDY
+ OPEN_CODE_REFERENCE
+ EXACT_MODEL_BOUND
~~~

Claim ceiling:

~~~text
PARTIAL_INTERNAL_STATE_DISCRIMINATION
= SUPPORTED_IN_ONE_MODEL / PARADIGM

NATIVE_GENERAL_INTROSPECTION
= NOT_ESTABLISHED

SELF_AWARENESS
= NOT_ESTABLISHED

SUBJECTIVITY
= NOT_ESTABLISHED
~~~

## 11. Why the introspection study is especially important for Llama

The open-weight model permits direct activation interventions that are harder or impossible on many proprietary systems.

This creates a methodological advantage:

~~~text
OPEN_WEIGHT_ACCESS
-> INTERNAL_INTERVENTION_FEASIBILITY
-> STRONGER_CAUSAL_TEST_DESIGN_POSSIBLE
~~~

But the study itself demonstrates why access alone is not enough: the first apparent positive result was explainable by a simpler logit-shift artifact.

Therefore:

~~~text
MECHANISTIC_ACCESS
!= MECHANISTIC_VALIDITY

INTERVENTION
CAN_CREATE
ITS_OWN_ARTIFACT
~~~

## 12. Open-weight derivative evidence problem

The wider Llama ecosystem contains many fine-tunes, quantizations and hosted variants.

This provides replication opportunities, but creates a comparability problem.

~~~text
MANY_LLAMA_DERIVATIVES
!= MANY_REPLICATIONS_OF_SAME_MODEL

DERIVATIVE_ECOSYSTEM_SIZE
!= E4_REPLICATION_STRENGTH
~~~

A replication must preserve or explicitly vary:

- base checkpoint;
- exact weight revision;
- quantization;
- adapter;
- tokenizer;
- chat template;
- runtime;
- intervention method;
- evaluator.

## 13. Current Muse evidence is topology evidence only

Artificial Analysis currently measures Muse Spark 1.3 through Meta's first-party API.

Source:
https://artificialanalysis.ai/articles/muse-spark-1-3

That evidence is relevant to the claim that Meta's current frontier line is Muse.

It is not admitted here as Llama performance or Llama mechanism evidence.

~~~text
MUSE_SPARK_1_3_EXTERNAL_MEASUREMENT
= META_PROVIDER_TOPOLOGY_EVIDENCE

NOT
= LLAMA_4_EVIDENCE
~~~

## 14. Negative / null / limiting evidence retained

~~~text
BINARY_INTROSPECTION_ARTIFACT
= RETAINED

LATE_LAYER_INTROSPECTION_COLLAPSE
= RETAINED

EXPERIMENTAL_VS_RELEASE_MAVERICK_MISMATCH
= RETAINED

STYLE / SENTIMENT_ARENA_EFFECT
= RETAINED

BENCHMARK_GOVERNANCE_DISPUTE
= RETAINED_WITH_BOTH_SIDES

PROVIDER_RUNTIME_VARIANCE
= RETAINED

CURRENT_LLAMA_NOT_CURRENT_META_FRONTIER
= RETAINED
~~~

The evidence set does not support a monotonic progress narrative or a single stable Llama identity.

## 15. Evidence gaps

At the cutoff:

~~~text
CURRENT_LLAMA_4_INDEPENDENT_SUBJECTIVITY_MECHANISM_STUDY
= NOT_IDENTIFIED

OPEN_REPLICATION_OF_LLAMA_3_1_INTROSPECTION_RESULT
= NOT_ESTABLISHED

MATCHED_CROSS_QUANTIZATION_SUBJECTIVITY_RELEVANT_STUDY
= NOT_IDENTIFIED

MATCHED_BASE_VS_DERIVATIVE_IDENTITY_CONTINUITY_STUDY
= NOT_IDENTIFIED

LLAMA_SPECIFIC_HUMAN_LEARNING_RCT
= NOT_IDENTIFIED

CURRENT_LLAMA_4_INDEPENDENT_INCIDENT_RECONSTRUCTION
= SPARSE / NOT_IDENTIFIED_IN_THIS_SWEEP
~~~

## 16. Cross-source convergence

Current first-party and external evidence converge on weaker methodological claims:

~~~text
EXACT_ARTIFACT_IDENTITY_MATTERS

HOSTING / RUNTIME_MATTERS

QUANTIZATION / DERIVATION_MUST_BE_BOUND

BENCHMARK_STYLE_CAN_MATTER

OPEN_WEIGHT_ACCESS_ENABLES_STRONGER_INTERVENTIONS

INTERVENTION_ARTIFACTS_MUST_BE_CONTROLLED
~~~

They do not converge on a subjectivity claim.

## 17. Admission status

~~~text
META_LLAMA_EXTERNAL_EVIDENCE
= SUFFICIENT_FOR_RESEARCH_REFERENCE_REVIEW

CURRENT_EXTERNAL_LLAMA_BENCHMARKS
= PRESENT

INDEPENDENT_LLAMA_MECHANISTIC_STUDY
= PRESENT / NARROW / LLAMA_3_1_SPECIFIC

BENCHMARK_GOVERNANCE_CONTROVERSY
= PRESENT / CONTESTED

CROSS_SOURCE_TRIANGULATION
= PARTIAL

E4_OPEN_INDEPENDENT_REPLICATION
= SPARSE / DOMAIN_SPECIFIC

INDEPENDENT_VALIDATION_AS_A_WHOLE
= NO

CROSS_PROVIDER_RANKING
= NO

SUBJECTIVITY_EVIDENCE
= NO

SCIENTIFIC_DISPOSITION
= HOLD
~~~
