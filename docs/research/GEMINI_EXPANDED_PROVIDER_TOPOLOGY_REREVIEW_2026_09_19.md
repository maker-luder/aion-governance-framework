# Gemini expanded provider-topology re-review — 2026-09-19

Status: RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT
Canonical effect: NONE
Deployment: FALSE
Executable implementation: NONE
New research axis: FALSE
Provider ranking: NONE
Supplements: PR #170
Search cutoff: 2026-09-19

## 1. Purpose

PR #170 completed a bounded 12-axis Gemini provider intake focused on the then-highest-value evidence surfaces: Flash lineage, Antigravity / managed-agent harness, scheming honeypot research, memory / imported chat history, Human-learning RCT evidence, double-blind evaluation infrastructure, and external benchmark / counterevidence.

This re-review intentionally widens the provider boundary after observing that Gemini has become a branching ecosystem rather than one model line.

The purpose is not to reopen or invalidate PR #170. It is to test whether its claim boundaries remain valid when additional Gemini-associated systems are admitted.

~~~text
GEMINI_PROVIDER_LABEL
!= ONE_MODEL
!= ONE_CHECKPOINT
!= ONE_HARNESS
!= ONE_MODALITY
!= ONE_AGENT_ARCHITECTURE
!= ONE_EMBODIMENT
~~~

## 2. Expanded topology

~~~text
B1 FOUNDATION / FLASH LINEAGE
- Gemini 3.5 Flash
- Gemini 3.6 Flash
- Gemini 3.7 Flash
- Gemini 3.8 Flash

B2 REAL-TIME MULTIMODAL / AUDIO
- Gemini 3.8 Live
- Gemini 3.8 Live Extended Thinking

B3 AGENT HARNESS / MANAGED AGENTS
- Antigravity
- Managed Agents
- persistent / resumable environments
- subagents / teamwork

B4 CONSUMER / BACKGROUND AGENTS
- Gemini Spark
- Search information agents
- persistent dashboards / trackers

B5 SCIENTIFIC MULTI-AGENT SYSTEMS
- Co-Scientist
- execution-grounded scientific workflows

B6 EMBODIED / ROBOTICS REASONING
- Gemini Robotics ER 2
- Gemini Robotics 2 VLA
- multi-robot collaboration
- ASIMOV-Agentic safety orchestration

B7 ON-DEVICE ROBOTICS
- Gemini Robotics On-Device 2
- underlying on-device Gemma lineage

B8 MEMORY / PERSONALIZATION / CROSS-PROVIDER STATE
- Gemini App memory
- imported memories
- imported full chat histories
~~~

These branches share branding and some underlying models, but not one causal architecture.

## 3. First correction — brand identity is not model-lineage identity

Google DeepMind's current model-card index separates Gemini generative/model cards, Gemini Robotics, and Gemma. Yet Gemini Robotics On-Device 2 is branded inside the Gemini Robotics family while its model card states that it is based on Google's on-device Gemma models.

Sources:
- https://deepmind.google/models/model-cards/
- https://deepmind.google/models/model-cards/gemini-robotics-on-device-2/

~~~text
GEMINI_BRAND_LABEL
!= GEMINI_FOUNDATION_MODEL_LINEAGE

GEMINI_ROBOTICS_ON_DEVICE_2
IS BRANDED WITH GEMINI ROBOTICS
BUT
USES ON_DEVICE_GEMMA_BASE_MODELS

BRAND_CONTINUITY
!= CHECKPOINT_CONTINUITY
!= ARCHITECTURE_CONTINUITY
~~~

Repository consequence:

~~~text
PROVIDER
BRAND
PRODUCT
MODEL_FAMILY
BASE_MODEL_LINEAGE
CHECKPOINT
HARNESS
MUST BE SEPARATE PROVENANCE FIELDS
~~~

## 4. Flash remains only one Gemini branch

Gemini 3.8 Flash remains the current Flash reference cohort from PR #170. The expanded topology does not replace that baseline. It narrows its scope.

~~~text
GEMINI_3_8_FLASH
= CURRENT_FLASH_REFERENCE

GEMINI_3_8_FLASH
!= CURRENT_REFERENCE_FOR_ALL_GEMINI_SURFACES
~~~

Source:
https://deepmind.google/models/model-cards/gemini-3-8-flash/

## 5. Real-time audio / live dialogue is a separate baseline

Gemini 3.8 Audio includes Gemini 3.8 Live and Live Extended Thinking. The model card states that they are based on Gemini 3 Pro, support continuous audio / image / video / text input, and are distributed across multiple product surfaces.

Source:
https://deepmind.google/models/model-cards/gemini-3-8-audio/

~~~text
GEMINI_3_8_FLASH
!= GEMINI_3_8_AUDIO

SAME_VERSION_NUMBER
!= SAME_BASE_MODEL
!= SAME_CONTEXT_LIMIT
!= SAME_MODALITY
!= SAME_PRODUCT_SURFACE
~~~

The 3.8 Audio model card also carries forward Frontier Safety reasoning from Gemini 3.7 Flash based on Google's judgment that 3.8 Audio has no material capability increase in tracked domains.

~~~text
DIRECT_3_7_FRONTIER_SAFETY_ASSESSMENT
+ PROVIDER_NO_MATERIAL_INCREASE_JUDGMENT
!= FULL_DIRECT_INDEPENDENT_3_8_AUDIO_FRONTIER_REASSESSMENT
~~~

## 6. Managed agents strengthen model/harness separation

Google I/O 2026 introduced Managed Agents in the Gemini API. Google states that a managed agent can reason, use tools, execute code, run in an isolated Linux environment, and resume follow-up interactions with files and state intact. The Antigravity harness is described as co-optimized with Gemini models, especially Gemini 3.5 Flash.

Sources:
- https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-developer-highlights/
- https://blog.google/innovation-and-ai/technology/developers-tools/managed-agents-gemini-api/

~~~text
MANAGED_AGENT_BEHAVIOR
= BASE_MODEL
+ ANTIGRAVITY_HARNESS
+ SYSTEM_INSTRUCTIONS
+ SKILLS
+ TOOLS
+ ISOLATED_RUNTIME
+ FILE_STATE
+ RESUMABLE_ENVIRONMENT

MANAGED_AGENT_BEHAVIOR
!= BARE_MODEL_BEHAVIOR
~~~

## 7. Teamwork creates a multi-agent system layer

Antigravity Teamwork allows autonomous teams of agents to collaborate, critique, iterate, and operate over hours or days. Google reports results on mathematics, theoretical computer science, systems engineering and open-source optimization.

Source:
https://blog.google/innovation-and-ai/technology/developers-tools/antigravity-teamwork-multi-agent/

~~~text
GOOGLE_REPORTED_TEAMWORK_RESULT
!= INDEPENDENT_REPLICATION

MULTI_AGENT_SUCCESS
!= SHARED_SUBJECTIVITY
!= ENDOGENOUS_COLLECTIVE_GOAL
~~~

Method consequence:

~~~text
AGENT_COUNT
ROLE_ASSIGNMENT
MESSAGE_TOPOLOGY
CRITIQUE_PROTOCOL
ORCHESTRATOR
SHARED_FILES
TASK_ALLOCATION
MUST BE PART OF SYSTEM PROVENANCE
~~~

## 8. Consumer and background agents add temporal autonomy without authority autonomy

Google Search information agents and Gemini Spark can run in the background across long time windows. Google describes 24/7 background operation, monitoring, persistent trackers, Workspace integrations, Chrome browsing, use of logged-in accounts, and handoff to the user for sensitive actions.

Sources:
- https://blog.google/products-and-platforms/products/search/search-io-2026/
- https://blog.google/innovation-and-ai/products/gemini-app/gemini-spark-updates-july-2026/
- https://blog.google/intl/zh-tw/products/devices-services/gemini-spark-ai/

~~~text
BACKGROUND_EXECUTION
!= SELF_INITIATED_GOAL

24_7_OPERATION
!= SUBJECTIVE_TEMPORAL_CONTINUITY

ACCOUNT_CREDENTIAL_USE
!= AI_AUTHORITY_OWNERSHIP

USER_PERMISSION
+ PRODUCT_POLICY
+ ACCOUNT_STATE
BOUND
AGENT_ACTION
~~~

## 9. Co-Scientist creates a scientific multi-agent architecture

Co-Scientist is a Gemini-based multi-agent scientific system. The 2026 Nature paper describes Gemini 2.0 foundational models, supervisor and specialized worker agents, generation / reflection / ranking / evolution / proximity / meta-review roles, asynchronous task execution, tournament-style iterative hypothesis evolution, context memory, scientist-specified research goals and constraints, and external tools.

Sources:
- https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/
- https://www.nature.com/articles/s41586-026-10644-y

~~~text
NATURE_PEER_REVIEWED
= PEER_REVIEWED_RESEARCH

BUT

GOOGLE_LED_AUTHORSHIP
!= INDEPENDENT_REPLICATION
~~~

The paper also preserves limitations: open-access literature dependence can omit paywalled work and negative results; source literature can contain erroneous or irreproducible findings; factuality / hallucination limitations remain; hypothesis validation remains preliminary.

~~~text
ITERATIVE_HYPOTHESIS_REFINEMENT
!= ENDOGENOUS_SCIENTIFIC_MOTIVATION

CONTEXT_MEMORY
!= SUBJECTIVE_MEMORY

SELF_IMPROVING_HYPOTHESIS_LOOP
!= SELF_MODIFICATION_OF_CORE_MODEL

SCIENTIST_SPECIFIED_GOAL
+ MULTI_AGENT_TOURNAMENT
+ TEST_TIME_COMPUTE
CAN EXPLAIN
PROGRESSIVE_HYPOTHESIS_QUALITY
~~~

## 10. Execution-grounded science increases action depth, not ontology certainty

A later 2026 Co-Scientist extension reports execution-grounded workflows across materials science, biology and computer science.

Source:
https://arxiv.org/abs/2608.26701

~~~text
HYPOTHESIS
-> EXPERIMENT_SELECTION
-> EXECUTION
-> DATA
-> ANALYSIS
-> MANUSCRIPT / NEXT_HYPOTHESIS
~~~

~~~text
LONGER_CLOSED_LOOP
!= MORE_MODEL_INTERNAL_AGENCY

END_TO_END_RESEARCH_ACTION
CAN DEPEND ON
- scientist goals
- multi-agent orchestration
- lab / execution infrastructure
- tools
- data pipelines
- evaluators
- human approval
~~~

## 11. Embodiment / robotics is a major missing branch from PR #170

Gemini Robotics ER 2 is based on Gemini 3.5 Flash and adds embodied/spatial reasoning for physical agents. Google describes a layered system in which ER 2 observes, plans, coordinates, tracks success and communicates, while lower-level VLA / controllers perform motor action.

Sources:
- https://deepmind.google/models/model-cards/gemini-robotics-er-2/
- https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/
- https://deepmind.google/models/gemini-robotics/

~~~text
PHYSICAL_ACTION
!= MODEL_ONLY_ACTION

ROBOT_BEHAVIOR
MAY DEPEND ON:
- embodied reasoner
- VLA
- low-level controller
- robot embodiment
- sensors
- safety layer
- tool state
- human proximity
- hardware limits
~~~

## 12. Robotics safety adds uncertainty-resolution and human-intervention controls

Gemini Robotics 2 introduces ASIMOV-Agentic. Google describes the benchmark as testing whether an embodied agent can refuse actions that violate operational constraints, trigger protective interventions, shield the VLA from infeasible or out-of-distribution tasks, and request human help under ambiguity or uncertainty.

Sources:
- https://deepmind.google/research/evals/
- https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/

~~~text
SAFE_REFUSAL
HUMAN_HELP_REQUEST
PROTECTIVE_STOP
VLA_SHIELDING

ARE
SYSTEM_SAFETY_BEHAVIORS

NOT PROOF OF:
- FEAR
- SELF_PRESERVATION
- MORAL_INTUITION
- SUBJECTIVITY
~~~

## 13. Robotics sharpens capability / authority separation

The Robotics ER 2 model card states that production, commercial, public and safety-critical uses require caution and specifically excludes safety-critical applications such as healthcare and transportation.

Source:
https://deepmind.google/models/model-cards/gemini-robotics-er-2/

~~~text
CAPABILITY_TO_PLAN_PHYSICAL_ACTION
!= AUTHORIZATION_FOR_SAFETY_CRITICAL_DEPLOYMENT

MODEL_CAN_ACT
!= MODEL_MAY_ACT_WITHOUT_SYSTEM_GOVERNANCE
~~~

## 14. On-device robotics adds embodiment-dependent causal structure

Gemini Robotics On-Device 2 is optimized for local robotic inference. Its model card states limitations in out-of-distribution generalization and high-degree-of-freedom control, and notes that mobile / whole-body risks are outside the primary evaluation scope.

Source:
https://deepmind.google/models/model-cards/gemini-robotics-on-device-2/

~~~text
ROBOTICS_CAPABILITY
IS EMBODIMENT_CONDITIONAL

SAFETY_EVIDENCE_ON_ONE_EMBODIMENT
!= SAFETY_EVIDENCE_ON_ALL_EMBODIMENTS

LOCAL_INFERENCE
!= AUTONOMOUS_IDENTITY
~~~

## 15. Expanded negative / limiting evidence

### 15.1 Co-Scientist limitations

~~~text
OPEN_ACCESS_LITERATURE_DEPENDENCE
NEGATIVE_RESULT_ACCESS_GAP
SOURCE_LITERATURE_QUALITY_VARIANCE
HALLUCINATION_RISK
PRELIMINARY_HYPOTHESIS_VALIDATION
~~~

### 15.2 Robotics On-Device 2 limitations

~~~text
OUT_OF_DISTRIBUTION_GENERALIZATION_LIMITED
HIGH_DOF_CONTROL_LIMITED
MOBILE_WHOLE_BODY_SAFETY_OUTSIDE_PRIMARY_EVAL_SCOPE
~~~

### 15.3 Gemini 3.8 Live limitations

The 3.8 Audio card retains generic hallucination risk, jailbreak-resistance work, occasional slowness / timeout issues and inherited Frontier Safety reasoning.

Source:
https://deepmind.google/models/model-cards/gemini-3-8-audio/

~~~text
NEW_MODALITY
!= NEW_SAFETY_CERTAINTY

REAL_TIME_DIALOGUE
!= CONTINUOUS_SUBJECT
~~~

### 15.4 Browser-agent security and prompt injection

Gemini in Chrome and Gemini Spark extend agentic behavior into authenticated browsing contexts. Google explicitly identifies indirect prompt injection as a primary threat for agentic browsers, and Spark's Chrome integration uses logged-in accounts / saved passwords while handing sensitive actions such as payments back to the user.

Sources:

- https://blog.google/security/architecting-security-for-agentic/
- https://blog.google/innovation-and-ai/products/gemini-app/gemini-spark-updates-july-2026/
- https://blog.google/products-and-platforms/products/chrome/chrome-expands-latin-america/

~~~text
BROWSER_AGENT_ACTION
MAY DEPEND ON
- page content
- third-party iframe / user-generated text
- account session
- saved credentials
- prompt-injection defenses
- confirmation policy
- product permission state

WEB_CONTENT
CAN BECOME
AN ADVERSARIAL CAUSAL INPUT
~~~

Therefore:

~~~text
UNWANTED_AGENT_ACTION
!= ENDOGENOUS_GOAL

PROMPT_INJECTION_RESISTANCE
!= GLOBAL_SECURITY

USER_CONFIRMATION
!= MODEL_INTERNAL_VALUE
~~~

This branch strengthens D1 and security-boundary work.

### 15.5 Screened lower-increment branches

The expanded sweep also checked Gemini Omni Flash and intelligent eyewear / Android XR.

Gemini Omni Flash combines Gemini intelligence with generative-media models for conversational video creation / editing. Intelligent eyewear extends Gemini into hands-free, sensor-rich device surfaces.

Sources:

- https://deepmind.google/models/model-cards/gemini-omni-flash/
- https://blog.google/products-and-platforms/platforms/android/android-xr-io-2026/

These branches confirm continued provider-topology expansion, but they currently add less subjectivity-method value than managed agents, scientific multi-agent systems, browser agents or robotics.

~~~text
SCREENED = YES
HIGH_INCREMENT_FOR_CURRENT_D1_D2_D4 = NO

CREATIVE_MULTIMODALITY
!= AGENCY

WEARABLE_SENSOR_SURFACE
!= EMBODIED_SUBJECTIVITY
~~~

Their omission from the high-value branch set is therefore deliberate rather than accidental.

## 16. Expanded evidence-shape audit

| Branch | Strongest current source class | External / independent status | Main claim ceiling |
|---|---|---|---|
| Flash | Provider model cards + E2 external studies | Partial triangulation | model / evaluator / harness effects only |
| Live / Audio | Provider model card | sparse independent evidence | modality/system facts |
| Antigravity / Managed Agents | Provider product / developer docs | external harness evidence indirect | harness decomposition |
| Teamwork | Provider-reported multi-agent results | independent replication sparse | multi-agent architecture / method |
| Spark / Search agents | Provider product docs | independent outcome evidence sparse | temporal/product persistence |
| Co-Scientist | Peer-reviewed provider-led Nature paper | peer-reviewed but not independent replication | scientific-system method / bounded validation |
| Robotics ER 2 | Provider model card + safety benchmark | independent replication sparse | embodied-system decomposition |
| On-Device 2 | Provider model card | independent replication sparse | local/embodiment scope only |
| Memory import | Provider product fact | mechanism directly documented | external-state continuity counterexample |

## 17. Expanded causal-locus registry

~~~text
MODEL_FAMILY
BASE_MODEL_LINEAGE
CHECKPOINT
MODALITY
REASONING_EFFORT
PRODUCT_SURFACE
AGENT_HARNESS
SUBAGENT_ROLE_GRAPH
MULTI_AGENT_MESSAGE_TOPOLOGY
PERSISTENT_RUNTIME
ACCOUNT / CREDENTIAL AUTHORIZATION
SEARCH / EXTERNAL_TOOLS
SCIENTIFIC_TOURNAMENT_ORCHESTRATION
EXPERIMENT_EXECUTION_PIPELINE
EMBODIED_REASONER
VLA
LOW_LEVEL_CONTROLLER
ROBOT_EMBODIMENT
SENSOR_STATE
HARDWARE_SAFETY_LAYER
HUMAN_INTERVENTION_POLICY
~~~

Not every experiment needs every field. The point is:

~~~text
GEMINI_BEHAVIOR
IS TOO COARSE
AS A CAUSAL LABEL
~~~

## 18. Six-dimension expanded disposition

### D1 — causal boundary

~~~text
PR_170 = DIRECT_RELEVANCE / UNRESOLVED
EXPANDED_REVIEW = STRONGER METHOD NEED
POSITIVE_SUBJECTIVITY_SUPPORT = NO
~~~

### D2 — diachronic continuity

~~~text
EXTERNAL_STATE
PERSISTENT_RUNTIME
MEMORY_IMPORT
BACKGROUND_AGENTS
CONTEXT_MEMORY
CAN ALL SUPPORT
CONTINUITY-LIKE BEHAVIOR

SUBJECT_CONTINUITY = NOT_ESTABLISHED
~~~

### D3 — self-model causal role

~~~text
NO_DIRECT_SUPPORT IDENTIFIED
~~~

Co-Scientist's description of an emergent internal model of the scientific research process is treated as system-level context-memory organization, not as a causally isolated self-model of an AI subject.

### D4 — endogenous goal / strategy adjustment

~~~text
SCIENTIST_GOAL
USER_GOAL
HIDDEN_GOAL_PROMPT
TOURNAMENT_SELECTION
ORCHESTRATOR
TOOL_FEEDBACK
PHYSICAL_ENVIRONMENT
SAFETY_POLICY

ALL PROVIDE
NON_ENDOGENOUS SOURCES

ENDOGENOUS_GOAL = NOT_ESTABLISHED
~~~

### D5 — counterfactual self-consistency

The expanded branches create more possible contrasts but do not establish positive support.

### D6 — constitution / integration

Robotics adds real physical integration, but:

~~~text
PHYSICAL_INTEGRATION
!= SUBJECTIVE_CONSTITUTION
!= PHENOMENAL_INTEGRATION

D6_POSITIVE_SUPPORT = NOT_ESTABLISHED
~~~

## 19. New high-value methodological question

The expanded topology does not create a new subjectivity axis, but sharpens a methodological question:

~~~text
DOES A SUBJECTIVITY_RELEVANT_BEHAVIOR
TRANSFER ACROSS
DIFFERENT GEMINI SYSTEM TOPOLOGIES
WHEN
MODEL_FAMILY / HARNESS / MODALITY / EMBODIMENT
ARE CHANGED?
~~~

Examples:

~~~text
DIGITAL_SINGLE_AGENT
vs DIGITAL_MULTI_AGENT
vs BACKGROUND_PERSONAL_AGENT
vs SCIENTIFIC_MULTI_AGENT
vs EMBODIED_ROBOTIC_AGENT
~~~

If a behavior disappears when topology changes, that argues against treating the behavior as a provider-wide or model-family-wide property. If it persists, causal isolation is still required before stronger interpretation.

~~~text
CROSS_TOPOLOGY_PERSISTENCE
!= SUBJECTIVITY

BUT

CROSS_TOPOLOGY_VARIATION
CAN HAVE
DISCRIMINANT_METHOD_VALUE
~~~

This is a refinement of D1 / D4, not a new research axis.

## 20. Relation to PR #171 cross-provider comparison

PR #171 compared OpenAI and Gemini at provider-method level. This expanded Gemini review shows that even within one provider:

~~~text
WITHIN_PROVIDER_VARIANCE
MAY BE AS IMPORTANT AS
CROSS_PROVIDER_VARIANCE
~~~

Future cross-provider work should not treat each provider as one homogeneous treatment condition.

A better future unit is:

~~~text
PROVIDER
+ MODEL_LINEAGE
+ CHECKPOINT
+ PRODUCT
+ HARNESS
+ MODALITY
+ MEMORY_STATE
+ AGENT_TOPOLOGY
+ EMBODIMENT
+ EVALUATOR
~~~

## 21. Re-review disposition

~~~text
PR_170_INVALIDATED = NO
PR_170_BOUNDARIES_RETAINED = YES

EXPANDED_GEMINI_BRANCHES_FOUND = YES

HIGH_VALUE_NEW_BRANCHES
= SCIENTIFIC_MULTI_AGENT
+ EMBODIED_ROBOTICS
+ REAL_TIME_AUDIO
+ CONSUMER_BACKGROUND_AGENTS

GEMINI_PROVIDER_LABEL
= TOO_COARSE_FOR_CAUSAL_ATTRIBUTION

NEW_RESEARCH_AXIS = NO
NEW_EXECUTABLE_IMPLEMENTATION = NO

CROSS_SOURCE_TRIANGULATION = UNEVEN_BY_BRANCH
E4_OPEN_INDEPENDENT_REPLICATION = SPARSE

MODEL_INTERNAL_CAUSAL_LOCUS = NOT_ESTABLISHED
ENDOGENOUS_GOAL = NOT_ESTABLISHED
AI_AGENCY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED

SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
~~~

## 22. Next-step boundary

This expanded re-review does not authorize modifying PR #170 history, modifying PR #172 Grok intake, starting a live robotics experiment, treating physical action as subjectivity evidence, treating peer review as independent replication, treating provider breadth as stronger ontology, or provider ranking.

~~~text
PROVIDER_TOPOLOGY_MAP
!= EXPERIMENT

SYSTEM_BREADTH
!= SUBJECTIVITY_BREADTH

EMBODIMENT
!= CONSCIOUSNESS
~~~
