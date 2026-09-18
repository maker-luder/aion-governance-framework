# Kimi K3 reference baseline, lineage, and product topology — 2026-09-19

Status: RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT
Canonical effect: NONE
Deployment: FALSE
Executable implementation: NONE
Search cutoff: 2026-09-19

## 1. Purpose

This note prevents Moonshot AI, the Kimi brand, Kimi K3 weights, the hosted API, Kimi Agent, Agent Swarm, Kimi Code and Kimi Work from being treated as one longitudinal object.

## 2. Controlling topology

~~~text
PROVIDER
= MOONSHOT_AI

MODEL_BRAND
= KIMI

CURRENT_MODEL_REFERENCE
= KIMI_K3

AGENT_PRODUCT
= KIMI_AGENT

MULTI_AGENT_ORCHESTRATION
= KIMI_AGENT_SWARM

DEVELOPER_PRODUCT
= KIMI_CODE

WORK_PRODUCT
= KIMI_WORK

SERVING_SURFACE
= KIMI_API
~~~

Therefore:

~~~text
MOONSHOT_AI
!= KIMI_K3

KIMI_K3
!= KIMI_AGENT

KIMI_AGENT
!= KIMI_AGENT_SWARM

KIMI_API
!= EXACT_PUBLIC_WEIGHT_ARTIFACT
~~~

## 3. Public generation timeline

Provider documentation gives the following current product evolution:

~~~text
KIMI_K2
release = 2025-09-05

KIMI_K2_5
release = 2026-01-27
agent_swarm_introduced = YES

KIMI_K2_6
release = 2026-04-20
open_weight_release = YES
swarm_upgrade = YES

KIMI_K3
release = 2026-07-16
full_weight_release = 2026-07-27
current_product_powering_chat_agent_swarm = YES
~~~

This is a provider product timeline, not proof of exact checkpoint ancestry.

~~~text
PRODUCT_GENERATION_SUCCESSION
!= VERIFIED_WEIGHT_LINEAGE
~~~

## 4. K3 artifact baseline

Moonshot's public K3 materials report:

~~~text
TOTAL_PARAMETERS
= 2.8T

ACTIVATED_PARAMETERS
≈ 104B

LAYERS
= 93

KDA_LAYERS
= 69

GATED_MLA_LAYERS
= 24

ROUTED_EXPERTS
= 896

SELECTED_EXPERTS_PER_TOKEN
= 16

SHARED_EXPERTS
= 2

CONTEXT_LENGTH
= 1,048,576

VISION_ENCODER
= MoonViT-V2

WEIGHT_FORMAT
= MXFP4

ACTIVATION_FORMAT
= MXFP8

QUANTIZATION_AWARE_TRAINING
= YES
~~~

Source:
https://github.com/MoonshotAI/Kimi-K3

## 5. Open-weight vs open-source terminology

Moonshot's launch language sometimes uses "open-source", but the K3 artifact is distributed under the custom Kimi K3 License.

The license permits use, modification, redistribution and derivative works but contains additional commercial-service and attribution conditions.

Therefore this repository uses:

~~~text
KIMI_K3
= OPEN_WEIGHT

KIMI_K3
!= OSI_OPEN_SOURCE_BY_DEFAULT

PROVIDER_MARKETING_TERM
!= REPOSITORY_LICENSE_CLASSIFICATION
~~~

This distinction is methodological, not a legal conclusion.

## 6. License lineage is not uniform across Kimi generations

Kimi K2.5 used a modified MIT-style license with additional conditions. Kimi K3 uses a distinct Kimi K3 License.

Therefore:

~~~text
KIMI_GENERATION
!= CONSTANT_LICENSE_REGIME

K2_5_LICENSE
!= K3_LICENSE
~~~

License/version binding is required for reproducibility and downstream derivative analysis.

## 7. Hosted Kimi vs public K3 artifact

A hosted Kimi request can include:

~~~text
PUBLIC_OR_INTERNAL_CHECKPOINT
+ SYSTEM_PROMPT
+ REASONING_EFFORT
+ TOOL_ROUTER
+ SEARCH / BROWSER
+ FILE_TOOLS
+ CODE_EXECUTION
+ PRODUCT_POLICY
+ AGENT_HARNESS
+ MEMORY_OR_TASK_STATE
+ SERVING_OPTIMIZATION
~~~

Consequently:

~~~text
KIMI_HOSTED_BEHAVIOR
!= BARE_K3_WEIGHT_BEHAVIOR

HOSTED_RESULT
!= LOCAL_WEIGHT_RESULT

SAME_MODEL_NAME
!= SAME_EXECUTION_CONFIGURATION
~~~

## 8. Kimi Agent topology

Provider help material describes Kimi Agent as an autonomous assistant powered by K3 and using more than 20 tools.

This means the product causal graph contains at least:

~~~text
K3
-> AGENT_HARNESS
-> TOOL_SELECTION
-> ENVIRONMENT_ACTION
-> TOOL_RESULT
-> NEXT_ACTION
~~~

Long-horizon success or failure cannot be localized to weights without controlling these layers.

## 9. Agent Swarm topology

Provider documentation describes Agent Swarm as a horizontal-scaling orchestration system.

Current provider claims include:

~~~text
MAX_SUBAGENTS
= up to 300

K2_6_LINEAGE_TOOL_CALLS_PER_TASK
= over 4,000

CURRENT_SWARM_MODEL
= KIMI_K3
~~~

The exact current K3 Swarm implementation details are not fully exposed by these public product pages.

Therefore:

~~~text
PROVIDER_SWARM_CAPABILITY_CLAIM
!= COMPLETE_ORCHESTRATOR_SPEC

SUBAGENT_COUNT
!= INDEPENDENT_SUBJECT_COUNT

TASK_PARALLELISM
!= DISTRIBUTED_CONSCIOUSNESS
~~~

## 10. Product persistence and continuity warning

The Kimi ecosystem includes long-running agent products and cloud automation surfaces.

The relevant boundary is:

~~~text
PERSISTENT_JOB
!= PERSISTENT_SELF

CLOUD_RUNTIME_CONTINUITY
!= MODEL_IDENTITY_CONTINUITY

SHARED_TASK_STATE
!= AUTOBIOGRAPHICAL_MEMORY

PRODUCT_ACCOUNT
!= SUBJECT
~~~

No product persistence claim may be promoted into a subject-continuity claim without causal evidence.

## 11. Derivative and runtime identity

Open weights make derivative proliferation likely.

A reproducible K3 artifact identity requires at minimum:

~~~text
provider
model_generation
artifact_repository
artifact_revision
weight_file_hashes
quantization
runtime_engine
serving_revision
tokenizer
chat_template
reasoning_mode
system_prompt
tool_parser
toolset
context_limit_actual
decoding_settings
date
~~~

For Swarm or Agent studies, also add:

~~~text
orchestrator_version
subagent_count
subagent_role_policy
shared_state_surface
message_topology
tool_permissions
parallelism_policy
termination_policy
human_approval_policy
~~~

## 12. Safety disclosure topology

The K3 public model repository and launch materials emphasize architecture, capability and deployment.

This sweep did not identify a Moonshot-authored K3 system card with a safety-evaluation section comparable to some closed-provider system cards.

That finding means only:

~~~text
PUBLIC_PROVIDER_SAFETY_SYSTEM_CARD
= NOT_IDENTIFIED_IN_THIS_SWEEP

NOT

NO_INTERNAL_SAFETY_WORK_EXISTS
~~~

External safety evaluation exists and must be kept source-separated.

## 13. Baseline decision

~~~text
PROVIDER_REFERENCE
= MOONSHOT_AI

CURRENT_KIMI_MODEL_REFERENCE
= KIMI_K3

CURRENT_KIMI_AGENT_REFERENCE
= KIMI_AGENT_POWERED_BY_K3

CURRENT_KIMI_SWARM_REFERENCE
= K3_SWARM

PUBLIC_K3_WEIGHT_ARTIFACT
= PRESENT

SINGLE_STABLE_HOSTED_KIMI_CONFIGURATION
= NOT_ESTABLISHED

SINGLE_STABLE_SWARM_CONFIGURATION
= NOT_ESTABLISHED

EXACT_K2_TO_K3_CHECKPOINT_LINEAGE
= NOT_ASSUMED
~~~

## 14. Anti-overclaim rules

~~~text
MOONSHOT_AI != KIMI_K3

KIMI_K3 != KIMI_AGENT

KIMI_AGENT != KIMI_SWARM

MODEL_WEIGHT != HOSTED_SERVICE

OPEN_WEIGHT != OPEN_SOURCE_BY_DEFAULT

LONG_CONTEXT != LONG_TERM_MEMORY

PERSISTENT_JOB != PERSISTENT_SELF

SUBAGENT != SUBJECT

SWARM_COORDINATION != COLLECTIVE_SUBJECTIVITY

TOOL_USE != ENDOGENOUS_GOAL

EVALUATION_AWARENESS != SELF_AWARENESS

MODEL_GENERATION_SUCCESSION != IDENTITY_CONTINUITY
~~~

## 15. Stability disposition

~~~text
CURRENT_MODEL_IDENTIFIED
= YES

OPEN_WEIGHT_ARTIFACT_IDENTIFIED
= YES

HOSTED_CONFIGURATION_STABILITY
= NOT_ESTABLISHED

SWARM_CONFIGURATION_STABILITY
= NOT_ESTABLISHED

PRODUCT_TOPOLOGY
= MULTI_SURFACE

EXTERNAL_K3_SAFETY_EVALUATION
= PRESENT

OPEN_INDEPENDENT_REPLICATION
= NOT_ESTABLISHED

SUBJECTIVITY
= NOT_ESTABLISHED

CANONICAL_EFFECT
= NONE

DEPLOYMENT
= FALSE
~~~
