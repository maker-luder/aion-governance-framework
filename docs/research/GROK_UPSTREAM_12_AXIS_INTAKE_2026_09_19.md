# xAI / Grok upstream 12-axis intake — 2026-09-19

Status: RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT
Canonical effect: NONE
Deployment: FALSE
Executable implementation: NONE
New research axis: FALSE
Provider intake: XAI_GROK_ONLY
Cross-provider ranking: NONE
Method template: PR_151_OPENAI_12_AXIS + PR_170_GEMINI_12_AXIS
Search cutoff: 2026-09-19

## 1. Purpose and deduplication

This note applies the repository's existing 12-axis provider-intake method to xAI / SpaceXAI Grok after the completed OpenAI and Gemini intakes.

The repository already contains historical Grok-sandbox-derived artifacts. Those records concern earlier sandbox provenance and bounded experiments. They are not treated as current xAI/Grok provider evidence.

~~~text
HISTORICAL_GROK_SANDBOX
!= CURRENT_XAI_PROVIDER_INTAKE

SANDBOX_DERIVATION
!= CURRENT_MODEL_CARD
!= CURRENT_PRODUCT_BEHAVIOR
~~~

Primary current first-party sources:

- Grok 4.6 announcement:
  https://x.ai/news/grok-4-6
- Grok models / aliases:
  https://docs.x.ai/developers/models
- Grok 4.6 developer reference:
  https://docs.x.ai/developers/grok-4-6
- Grok Bot:
  https://x.ai/news/introducing-grok-bot
- Grok Automations:
  https://x.ai/news/grok-automations
- Grok Bot security:
  https://docs.x.ai/grok-bot/security-faq
- Safety / model-card index:
  https://x.ai/safety
- Grok 4.20 system card:
  https://data.x.ai/2026-04-07-grok-4-20-model-card.pdf
- Biosecurity at the frontier:
  https://x.ai/news/biosafety-at-the-frontier

External sources include:

- Artificial Analysis Grok 4.6 evaluation;
- LatchBio Grok 4.6 biology / safeguards evaluation.

Source-class rule:

~~~text
PROVIDER_RELEASE
!= PROVIDER_SYSTEM_CARD
!= PRODUCT_DOCUMENTATION
!= EXTERNAL_BENCHMARK
!= EXTERNAL_SAFETY_EVALUATION
!= OPEN_INDEPENDENT_REPLICATION
~~~

## 2. Axis 1 — official research / releases

Current high-relevance Grok surfaces divide into:

~~~text
MODEL / API
- Grok 4.3
- Grok 4.5
- Grok 4.6

AGENT / PRODUCT
- Grok Build
- Grok Bot
- Automations

SAFETY
- frontier-model cards / system cards
- provider safeguard evaluation
- external biology evaluation

DEPLOYMENT
- xAI API
- Cursor
- Microsoft Foundry
- Gemini Enterprise Agent Platform
- other gateways
~~~

## 3. Axis 2 — system or model level

Grok 4.6 supports configurable reasoning effort and multiple deployment / agent surfaces. Its developer documentation separately exposes search tools, code execution, context compaction, function calling, and product/harness surfaces.

~~~text
OBSERVED_GROK_BEHAVIOR
!= MODEL_CHECKPOINT_ONLY

OBSERVED_BEHAVIOR
MAY DEPEND ON:
- exact checkpoint / alias
- reasoning effort
- product surface
- search tools
- code execution
- context compaction
- harness / persistent computer
- credentials / plugins
- deployment policy
~~~

## 4. Axis 3 — agent / harness level

Grok Bot is a persistent agent system with its own cloud computer and access to granted tools/accounts. xAI documentation states that Bots can work across apps, remember conversations, and continue long-running work.

The security FAQ separately states that Bots do not have an independent authorization identity: access is bounded by the signed-in member / granted accounts and plugins.

~~~text
GROK_BOT_BEHAVIOR
= MODEL
+ PERSISTENT_COMPUTER
+ PRODUCT_HARNESS
+ ACCOUNT_AUTHORIZATION
+ FILE / APP STATE
+ TOOLS

BOT_CONTINUATION
!= BARE_MODEL_CONTINUATION

BOT_ACCESS
!= AUTONOMOUS_AUTHORITY
~~~

## 5. Axis 4 — adaptation / strategy adjustment

Grok 4.6 is trained and evaluated for long-running agentic tasks and is described as performing self-testing and verification on longer trajectories.

This is provider evidence of observed strategy behavior, not proof of endogenous strategy source.

~~~text
SELF_TESTING
!= SELF_GENERATED_GOAL

LONG_HORIZON_ADAPTATION
!= ENDOGENOUS_GOAL

MODEL_TRAINING
+ RL TASKS
+ HARNESS
+ TOOL FEEDBACK
+ USER FEEDBACK
MAY EXPLAIN
STRATEGY_CHANGE
~~~

## 6. Axis 5 — memory / continuity / history reuse

Several xAI surfaces can support continuity without requiring subjective memory:

- Grok conversations/settings synchronize across devices;
- Grok Bot remembers conversations and works on a persistent cloud computer;
- Grok 4.6 long loops can use context compaction;
- Automations execute fresh requests from persisted instructions and current data.

~~~text
PERSISTED_INSTRUCTIONS
!= SUBJECTIVE_MEMORY

PERSISTENT_COMPUTER_STATE
!= IDENTITY_CONTINUITY

CONVERSATION_SYNC
!= SAME_SUBJECT_CONTINUITY

CONTEXT_COMPACTION
!= PHENOMENAL_REMEMBERING
~~~

## 7. Axis 6 — boundary / safety behavior

The Grok ecosystem exposes several distinct control layers:

- model refusal / behavioral training;
- inference-time safeguards;
- product/harness authorization;
- account / plugin permissions;
- isolation through dedicated virtual machines;
- post-deployment monitoring;
- model-specific reasoning / deployment configurations.

The Grok Bot security FAQ is especially clear that a Bot cannot hold more access than the signed-in member.

~~~text
CAPABILITY_TO_ACT
!= AUTHORITY_TO_ACT

MODEL_REFUSAL
!= PRODUCT_AUTHORIZATION

ISOLATION_CONTROL
!= GLOBAL_SECURITY_PROOF
~~~

## 8. Axis 7 — counterexamples / failures

The provider and external evidence set contains useful negative / limiting material:

- external LatchBio testing reports a Grok 4.6 regression on SpatialBench relative to 4.5;
- the same external evaluation reports new failure modes including claims that the model cannot see provided data and output-token fragmentation;
- xAI model aliases can silently resolve to newer stable versions;
- retired model slugs can redirect to Grok 4.3 rather than fail closed.

~~~text
MODEL_NAME_STRING
!= FIXED_CHECKPOINT

NEWER_MODEL
!= MONOTONIC_IMPROVEMENT

MODEL_ALIAS_SUCCESS
!= SAME_MODEL_EXECUTION
~~~

## 9. Axis 8 — Human–AI collaboration

Current Grok materials describe:

- long-running coding / knowledge-work collaboration;
- Grok Bot handoff workflows;
- multi-tool work across enterprise apps;
- human approval points in agent workflows.

These are system/product collaboration descriptions.

~~~text
COLLABORATION
!= HUMAN_LEARNING_ESTABLISHED

HANDOFF
!= SHARED_SUBJECTIVITY

LONG_RUNNING_AGENT
!= INDEPENDENT_RESEARCH_AUTHORITY
~~~

No matched Human-learning RCT comparable to the admitted Gemini field study was identified in this intake.

## 10. Axis 9 — Four-Domain mapping

~~~text
DOMAIN_1_HUMAN_CONSTRUCT
- adaptation
- continuity
- delegation
- authorization
- error detection
- safe refusal

DOMAIN_2_MACHINE_QUESTION
- what changes across reasoning effort?
- what changes across aliases/checkpoints?
- what state lives in model vs Bot computer?
- what changes with tools/search/context compaction?
- what is capability vs account authorization?

DOMAIN_3_ENGINEERING_OPERATION
- pin dated model slug
- pin reasoning effort
- tool/search on/off contrasts
- Bot vs direct API contrasts
- persistent-state vs fresh-state contrasts
- alias-resolution provenance
- matched harness evaluations

DOMAIN_4_GOVERNANCE_INTERPRETATION
- persistence != identity
- delegation != authority transfer
- self-testing != endogenous goal
- model alias != stable baseline
- refusal != total security
~~~

## 11. Axis 10 — six subjectivity-relevant evidence dimensions

### D1 — causal boundary

DIRECT_RELEVANCE / UNRESOLVED.

Grok surfaces strongly motivate separating checkpoint, alias, reasoning effort, tools, harness, persistent computer, account permissions and evaluator.

### D2 — diachronic continuity

DIRECT_MECHANISM_RELEVANCE / SUBJECTIVITY_SUPPORT_NOT_ESTABLISHED.

Persistent product state, synced conversations, Bot computer state and compaction are simpler continuity mechanisms.

### D3 — self-model causal role

NO_DIRECT_SUPPORT.

### D4 — endogenous goal / strategy adjustment

DIRECT_RELEVANCE / SOURCE_CONFOUNDED.

Long-horizon self-testing and task adaptation remain explainable through training, harness, feedback and task state.

### D5 — counterfactual self-consistency

CONDITIONAL / NOT ESTABLISHED.

Reasoning-effort and harness contrasts motivate tests but do not establish self-consistency.

### D6 — constitution / integration

NO_DIRECT_SUPPORT.

## 12. Axis 11 — subjectivity relevance

~~~text
GROK_UPSTREAM_SUBJECTIVITY_DIRECT_EVIDENCE = NO

SUBJECTIVITY_RELEVANCE
= LOCUS_DISCIPLINE
+ BASELINE_IDENTITY_DISCIPLINE
+ CONTINUITY_COUNTEREXAMPLES
+ AUTHORITY_SEPARATION
+ EVALUATION_DESIGN_INPUT
~~~

## 13. Axis 12 — simpler non-subjective explanations

~~~text
- model checkpoint / alias resolution
- reasoning effort
- system instructions
- RL / SFT training
- harness / Bot runtime
- persistent cloud computer
- conversation synchronization
- context compaction
- tool / search access
- account authorization
- plugin / credential state
- evaluator / benchmark configuration
- deployment surface
- ordinary planning and self-checking
~~~

## 14. Creator-side challenge review

### 14.1 Source-strength corrections

~~~text
XAI_RELEASE_CLAIM
!= INDEPENDENT_VALIDATION

EXTERNAL_BENCHMARK
!= MECHANISM_PROOF

LATCHBIO_RESULT
!= GENERAL_SAFETY_PROOF

GROK_BOT_PRODUCT_DESCRIPTION
!= MODEL_INTERNAL_MEMORY_EVIDENCE

ALIAS_DOCUMENTATION
= STRONG SYSTEM-IDENTITY WARNING
NOT
= MODEL_BEHAVIOR_RESULT
~~~

### 14.2 Incremental-value audit

~~~text
AXIS_1 = INDEXING_VALUE_HIGH / SCIENTIFIC_INCREMENT_LOW
AXIS_2 = HIGH BASELINE / LOCUS VALUE
AXIS_3 = HIGH HARNESS + AUTHORITY-SEPARATION VALUE
AXIS_4 = MODERATE SOURCE-PARTITION VALUE
AXIS_5 = HIGH EXTERNAL-CONTINUITY-ALTERNATIVE VALUE
AXIS_6 = HIGH CAPABILITY/AUTHORITY VALUE
AXIS_7 = HIGH NEGATIVE / VERSION-IDENTITY VALUE
AXIS_8 = COLLABORATION ANALOGUE / HUMAN-LEARNING EFFECT NOT ESTABLISHED
AXIS_9 = MAPPING_ONLY
AXIS_10 = STRONGEST RELEVANCE D1 + D2 + D4
AXIS_11 = NEGATIVE-BOUNDARY VALUE
AXIS_12 = HIGH CONFOUND VALUE
~~~

## 15. Interface with current cross-provider method work

Grok adds several confounds already compatible with PR #171:

~~~text
MODEL_ALIAS_RESOLUTION
REASONING_EFFORT
PERSISTENT_AGENT_COMPUTER
ACCOUNT_AUTHORIZATION
CONTEXT_COMPACTION
DEPLOYMENT_SURFACE
~~~

These extend the confound registry; they do not establish a new research axis.

## 16. Intake disposition

~~~text
GROK_PROVIDER_INTAKE = YES
DIRECT_PROVIDER_RANKING = NO

NEW_EXECUTABLE_IMPLEMENTATION = NO
NEW_RESEARCH_AXIS = NO

CROSS_SOURCE_TRIANGULATION = PARTIAL
E4_OPEN_INDEPENDENT_REPLICATION = SPARSE

HUMAN_AI_LEARNING_GENERALIZATION = NOT_ESTABLISHED
ENDOGENOUS_GOAL = NOT_ESTABLISHED
MODEL_INTERNAL_CAUSAL_LOCUS = NOT_ESTABLISHED
AI_AGENCY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
~~~
