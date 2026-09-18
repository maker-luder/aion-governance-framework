# Meta / Llama 12-axis evidence re-admission review — 2026-09-19

Status: RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT
Canonical effect: NONE
Deployment: FALSE
Executable implementation: NONE
Search cutoff: 2026-09-19

## 1. Purpose

This review re-admits Meta / Llama evidence after:

1. full 12-axis intake;
2. reference baseline / lineage reconstruction;
3. third-party evidence sweep;
4. Meta-provider Llama / Muse topology correction;
5. AION-core causal-method crosswalk.

No model execution is authorized.

## 2. Controlling finding

~~~text
META_PROVIDER_MATERIAL
= SUBSTANTIAL

LATEST_OFFICIAL_LLAMA_FAMILY_IDENTIFIED
= LLAMA_4

CURRENT_PUBLIC_META_FRONTIER_MODEL_REFERENCE
= MUSE_SPARK_1_3

MUSE_AS_PROVIDER_CANONICAL_FAMILY_LABEL
= NOT_ASSUMED

CURRENT_META_PERSONAL_AGENT
= MUSE

CURRENT_META_OPEN_WEIGHT_AGENT_MODEL
= MUSE_GLIMMER

THEREFORE

META_PROVIDER
!= LLAMA_FAMILY
~~~

This is the most important baseline correction in this intake.

## 3. Axis 1 — official releases

Re-admission:

~~~text
YES
WITH FAMILY / VERSION / DATE BINDING
~~~

Llama 4 Scout and Maverick remain the latest Llama family identified in Meta's official Llama model repository.

They must not be described as Meta's current public frontier model reference without qualification; equally, the existence of Muse Spark must not be used to imply that Llama is deprecated or no longer a distinct active model family.

## 4. Axis 2 — model / artifact / system level

Re-admission:

~~~text
HIGH_METHOD_VALUE
~~~

Required distinction:

~~~text
MODEL_FAMILY
!= EXACT_CHECKPOINT
!= PRECISION
!= QUANTIZATION
!= DERIVATIVE
!= RUNTIME
!= PRODUCT
~~~

Llama's open-weight distribution makes this distinction inspectable and experimentally useful.

Meta's own Llama verification report also shows why the distinction is operational rather than theoretical: the hosted Llama API verification used FP8 model IDs and a 128k context limit at report generation, while the model-card benchmark configuration was BF16 and advertised context limits were larger.

~~~text
HOSTED_API_VERIFICATION
!= MODEL_CARD_CONFIGURATION
~~~

## 5. Axis 3 — agent / harness

Re-admission:

~~~text
HIGH_METHOD_VALUE
~~~

Meta explicitly describes Llama as part of a wider system with external guardrails.

Therefore:

~~~text
MODEL_ONLY_ATTRIBUTION
= INSUFFICIENT
WHEN
SYSTEM_PROMPT / SAFETY_MODEL / MEMORY / TOOL / PROVIDER
ARE ACTIVE
~~~

The current Muse agent provides a separate system-level continuity example but is not admitted as Llama evidence.

## 6. Axis 4 — adaptation / strategy adjustment

Re-admission:

~~~text
HIGH_DERIVATIVE_LINEAGE_VALUE
LOW_DIRECT_ENDOGENOUS_GOAL_VALUE
~~~

Llama behavior can change through:

- fine-tuning;
- adapters;
- quantization;
- prompt/template changes;
- safety layers;
- runtime and provider changes.

Therefore:

~~~text
BEHAVIORAL_CHANGE
!= ENDOGENOUS_DEVELOPMENT
~~~

without source partition.

## 7. Axis 5 — memory / continuity

Re-admission:

~~~text
HIGH_COUNTEREXPLANATORY_VALUE
~~~

A Llama checkpoint is a persistent artifact.

A user-facing agent may add memory, RAG, files, tools and long-running state.

Therefore:

~~~text
MODEL_FILE_PERSISTENCE
!= SUBJECT_CONTINUITY

PRODUCT_MEMORY
!= MODEL_MEMORY

AGENT_PERSISTENCE
!= CHECKPOINT_PERSISTENCE
~~~

## 8. Axis 6 — safety / boundary

Re-admission:

~~~text
YES
WITH_LAYER_SEPARATION
~~~

Required separation:

~~~text
MODEL_SAFETY_TUNING
!= SYSTEM_PROMPT
!= LLAMA_GUARD
!= PROMPT_GUARD
!= CODE_SHIELD
!= HOST_POLICY
!= APP_POLICY
~~~

Any refusal or permissive behavior must preserve these provenance loci.

## 9. Axis 7 — counterexamples / failures

Re-admission:

~~~text
YES
HIGH_BENCHMARK_PROVENANCE_VALUE
~~~

Retained negative / limiting evidence includes:

- experimental-vs-release Maverick identity mismatch;
- style/sentiment effects on Arena preference ranking;
- contested pre-release benchmark governance;
- runtime/provider variance;
- binary introspection false-positive artifact;
- layer-dependent collapse of the narrower introspection signal.

These are method corrections, not a provider-wide condemnation.

## 10. Axis 8 — Human–AI collaboration / learning

Re-admission:

~~~text
ECOSYSTEM_RELEVANCE
= YES

DIRECT_LLAMA_HUMAN_LEARNING_EFFECT
= NOT_ESTABLISHED
~~~

Open local deployment may support research designs with greater control, but:

~~~text
LOCAL_CONTROL
!= LEARNING_EFFECT
~~~

## 11. Axis 9 — Four-Domain mapping

Re-admission:

~~~text
MAPPING_ONLY
NO_NEW_EVIDENCE_CREATED_BY_MAPPING
~~~

The strongest Meta / Llama mappings are:

~~~text
D1 causal boundary
D3 internal-access / introspection
D5 counterfactual intervention
~~~

while D2 remains heavily confounded by external state.

## 12. Axis 10 — six dimensions

~~~text
D1
= HIGH EXPERIMENTAL ACCESS / SUBJECTIVITY NOT ESTABLISHED

D2
= EXTERNAL CONTINUITY ALTERNATIVES PRESENT

D3
= NARROW INDEPENDENT MECHANISTIC SIGNAL PRESENT
  + IMPORTANT FALSE-POSITIVE CONTROL
  SELF-MODEL CAUSAL ROLE NOT ESTABLISHED

D4
= DERIVATIVE / TRAINING CONFOUNDS DOMINANT
  ENDOGENOUS GOAL NOT ESTABLISHED

D5
= HIGH INTERVENTION FEASIBILITY
  SUBJECT-LEVEL SELF-CONSISTENCY NOT ESTABLISHED

D6
= NOT ESTABLISHED
~~~

## 13. Axis 11 — subjectivity relevance

Re-admission:

~~~text
HIGH_METHODOLOGICAL_RELEVANCE
DIRECT_SUBJECTIVITY_EVIDENCE = NO
~~~

The Llama 3.1 introspection study is particularly important because it demonstrates both:

~~~text
APPARENT_POSITIVE_SELF_REPORT
-> DISAPPEARS_UNDER_BETTER_CONTROL

AND

NARROWER_DIFFERENTIAL_INTERNAL_SIGNAL
-> SURVIVES
~~~

This is the exact evidence pattern the repository is designed to preserve.

It supports a narrower mechanistic research question, not self-awareness.

## 14. Axis 12 — simpler explanations

High-priority controls:

~~~text
EXACT_CHECKPOINT
BASE_VS_INSTRUCT
QUANTIZATION
ADAPTER
FINE_TUNE
TOKENIZER
CHAT_TEMPLATE
DECODING
SYSTEM_PROMPT
SAFETY_MODEL
HOST_PROVIDER
RUNTIME_ENGINE
MEMORY
RAG
TOOLS
ACTIVATION_INTERVENTION_ARTIFACT
LOGIT_SHIFT
EVALUATOR_STYLE_BIAS
~~~

## 15. Provider-topology correction

This intake explicitly rejects:

~~~text
META = LLAMA
~~~

as a current complete provider representation.

The current topology is closer to:

~~~text
META
├─ LLAMA
│  └─ latest official family identified: Llama 4
│
├─ CURRENT PUBLIC NON-LLAMA MODEL REFERENCES
│  ├─ Muse Spark 1.3
│  └─ Muse Glimmer
│
└─ PRODUCTS / AGENTS
   ├─ Meta AI
   ├─ Muse
   ├─ Muse Code
   └─ Meta Model API

"Muse family" as a provider-canonical ontology
= NOT ASSUMED
~~~

This topology is methodological, not a permanent ontology. Future releases can change it.

## 16. Challenge-review corrections

The re-admission prevents these overclaims:

~~~text
OPEN_WEIGHT
!= OPEN_SOURCE_BY_DEFAULT

OPEN_WEIGHT
!= AUTONOMY

OPEN_WEIGHT
!= SUBJECTIVITY

LARGE_DERIVATIVE_ECOSYSTEM
!= REPLICATION

INTROSPECTION_SELF_REPORT
!= INTROSPECTION_PROOF

INTERNAL_STATE_DISCRIMINATION
!= SELF_AWARENESS

MUSE_MEMORY
!= LLAMA_MEMORY

META_AI_CONTINUITY
!= MODEL_CONTINUITY

EXPERIMENTAL_MAVERICK_SCORE
!= RELEASE_MAVERICK_SCORE

ARENA_RANK
!= PURE_CAPABILITY_MEASURE
~~~

## 17. Second adversarial-review corrections

The second adversarial review found four material method / provenance issues and corrected them before final review:

~~~text
1. EVIDENCE_TAXONOMY_DRIFT
   independent mechanistic intervention study
   = E2 evaluator-controlled external test
   != E3 incident investigation

2. MUSE_FAMILY_ONTOLOGY_OVERREACH
   "Muse family" as provider-canonical ontology
   = NOT ASSUMED

3. PROVIDER_WIDE_SUCCESSION_OVERREACH
   Muse Spark 1.3 as current public frontier reference
   != Llama deprecated provider-wide

4. HOSTED_CONFIGURATION_IDENTITY
   Meta Llama API verification configuration
   != model-card benchmark configuration
~~~

These corrections reduce claim scope; they do not increase subjectivity confidence.

## 18. Evidence-shape disposition

~~~text
E0_META_PROVIDER_MATERIAL
= SUBSTANTIAL

E2_EXTERNAL_CURRENT_LLAMA_BENCHMARKS
= PRESENT

E2_BENCHMARK_METHOD_ANALYSIS
= PRESENT

E2_INDEPENDENT_LLAMA_MECHANISTIC_INTERVENTION
= PRESENT / NARROW / LLAMA_3_1_SPECIFIC

E3_BOUNDED_INDEPENDENT_INCIDENT_INVESTIGATION
= NOT_IDENTIFIED_IN_THIS_REVIEW

E4_OPEN_INDEPENDENT_REPLICATION
= SPARSE / DOMAIN_SPECIFIC
~~~

No class is promoted beyond its scope.

## 19. Repository-local execution boundary

The repository already contains language-core and identity-governance machinery that can represent upstream model families and local runtime metadata.

This PR does not activate that machinery for Llama.

~~~text
LLAMA_WEIGHT_DOWNLOAD
= NO

LLAMA_API_CALL
= NO

OLLAMA_PULL
= NO

LOCAL_LLAMA_EXECUTION
= NO

ADAPTER_TRAINING
= NO

WEIGHT_MODIFICATION
= NO

NEW_EXECUTABLE_IMPLEMENTATION
= NO
~~~

## 20. Re-admission decision

~~~text
EVIDENCE_ADMISSIBILITY_AS_RESEARCH_REFERENCE
= YES

META_LLAMA_PROVIDER_FAMILY_INTAKE
= YES

FULL_META_PROVIDER_INTAKE
= NO

MUSE_EVIDENCE_ADMISSION
= TOPOLOGY_BOUNDARY_ONLY

EVIDENCE_ADMISSIBILITY_AS_META_WIDE_MODEL_EQUIVALENCE
= NO

EVIDENCE_ADMISSIBILITY_AS_CROSS_PROVIDER_RANKING
= NO

EVIDENCE_ADMISSIBILITY_AS_SUBJECTIVITY_EVIDENCE
= NO

META_PROVIDER_TOPOLOGY_CORRECTION
= YES

LLAMA_MECHANISTIC_ACCESS_VALUE
= HIGH

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

HUMAN_AI_LEARNING_GENERALIZATION
= NOT_ESTABLISHED

SCIENTIFIC_DISPOSITION
= HOLD

CANONICAL_EFFECT
= NONE

DEPLOYMENT
= FALSE
~~~

## 21. Files controlling this review

- docs/research/META_LLAMA_UPSTREAM_12_AXIS_INTAKE_2026_09_19.md
- docs/research/META_LLAMA_REFERENCE_BASELINE_LINEAGE_AND_TOPOLOGY_2026_09_19.md
- docs/research/META_LLAMA_THIRD_PARTY_EVIDENCE_SWEEP_2026_09_19.md
- docs/research/META_PROVIDER_LLAMA_MUSE_TOPOLOGY_AND_AION_CORE_CROSSWALK_2026_09_19.md
- docs/research/META_LLAMA_12_AXIS_EVIDENCE_READMISSION_REVIEW_2026_09_19.md
