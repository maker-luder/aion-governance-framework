# Google Gemini upstream 12-axis intake — 2026-09-19

Status: RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT
Canonical effect: NONE
Deployment: FALSE
Executable implementation: NONE
New research axis: FALSE
Provider intake: GEMINI_ONLY
Cross-provider ranking: NONE
Method template: PR_151_OPENAI_12_AXIS
Search cutoff: 2026-09-19

## 1. Purpose and deduplication

This note applies the repository's existing 12-axis upstream intake method to Google / Google DeepMind Gemini after the OpenAI intake recorded in PR #151.

The goal is not to rank Gemini against OpenAI or to infer subjectivity from capable behavior. The goal is to identify provider-reported mechanisms, external evidence, failure modes, and simpler causal explanations that can sharpen the repository's existing subjectivity-relevant tests.

Repository review before this intake found no prior canonical Gemini provider intake. Existing Gemini mentions were incidental, including one history-replay source comparison and an explicit deferral marker:

~~~text
NO_OPENAI_GEMINI_GROK_CLAUDE_META_KIMI_COMPARISON_YET
~~~

Therefore this is not duplicate provider work.

Source-class rule:

~~~text
FIRST_PARTY_MODEL_CARD
!= PRODUCT_POST
!= RESEARCH_PUBLICATION
!= PRODUCT_HELP_PAGE
!= PARTNERED_FIELD_STUDY
!= EXTERNAL_EVALUATION
!= OPEN_INDEPENDENT_REPLICATION
~~~

Primary first-party sources used:

- Google DeepMind model-card index:
  https://deepmind.google/models/model-cards/
- Gemini 3.8 Flash model card:
  https://deepmind.google/models/model-cards/gemini-3-8-flash/
- Gemini 3.7 Flash model card:
  https://deepmind.google/models/model-cards/gemini-3-7-flash/
- Gemini 3.5 Flash model card:
  https://deepmind.google/models/model-cards/gemini-3-5-flash/
- Gemini 3.8 Flash / 3.8 Flash Cyber launch:
  https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/
- Google I/O 2026 announcements, including Antigravity harness and subagent teamwork:
  https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/
- Gemini multi-agent teams in Antigravity:
  https://blog.google/innovation-and-ai/technology/developers-tools/antigravity-teamwork-multi-agent/
- Realistic honeypot evaluations for scheming propensity:
  https://deepmind.google/research/publications/253391/
- Guided Learning RCT in Sierra Leone:
  https://deepmind.google/blog/measuring-the-impact-of-learning-with-ai-in-sierra-leone-and-beyond/
- Double-blind AI evaluation pilot:
  https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/
- Gemini Apps import-from-other-AI memory / chat-history help:
  https://support.google.com/gemini/answer/16868299

## 2. Axis 1 — official research / releases

The current Gemini upstream surface spans several distinct classes:

~~~text
MODEL RELEASES / MODEL CARDS
- Gemini 3.5 Flash — 2026-05-19
- Gemini 3.6 Flash — 2026-07
- Gemini 3.7 Flash — 2026-08-13
- Gemini 3.8 Flash — 2026-09-02
- Gemini 3.8 Audio / Live family — 2026-09-15

AGENT / HARNESS
- Antigravity agent harness
- subagents
- hooks
- asynchronous task management
- Teamwork multi-agent orchestration

RESEARCH / SAFETY
- scheming honeypot evaluations
- double-blind evaluation pilot

HUMAN-AI LEARNING
- Guided Learning randomized controlled trial

PRODUCT MEMORY / CONTINUITY
- memory and chat-history import from other AI platforms
~~~

The release cadence is unusually fast. Therefore:

~~~text
LATEST_RELEASE
!= STABLE_LONGITUDINAL_REFERENCE

MODEL_CARD_EXISTS
!= INDEPENDENT_VALIDATION
~~~

## 3. Axis 2 — system or model level

Gemini 3.8 Flash is explicitly described as building on Gemini 3.7 Flash and is distributed across multiple product / API / agent surfaces, including Gemini Apps, Gemini API, AI Studio, Enterprise Agent Platform, and Antigravity.

The same model-family label can therefore participate in materially different system contexts.

Repository rule:

~~~text
OBSERVED_GEMINI_BEHAVIOR
!= MODEL_ONLY_BEHAVIOR

OBSERVED_BEHAVIOR
MAY DEPEND ON:
- model checkpoint / reasoning effort
- system and developer instructions
- product surface
- agent harness
- tools
- persistent environment
- files / retrieval
- subagents
- external services
- safety / deployment policy
~~~

This strengthens D1 causal-boundary discipline but does not isolate a model-internal causal locus.

## 4. Axis 3 — agent / harness level

Google I/O 2026 describes Antigravity as an agent-first platform whose harness provides core primitives such as subagents, hooks, asynchronous task management, and multi-agent orchestration. Google states that Gemini 3.5 Flash was co-optimized with the Antigravity agent harness.

Later Teamwork material describes autonomous groups of agents collaborating, critiquing, and iterating over hours or days.

Therefore:

~~~text
AGENTIC_PERFORMANCE
= MODEL
+ HARNESS
+ TOOLING
+ ORCHESTRATION
+ PERSISTENT_ENVIRONMENT
+ MULTI_AGENT_CHANNELS

AGENTIC_PERFORMANCE
!= MODEL_INTRINSIC_PROPERTY_ONLY
~~~

This is directly relevant to repository model / system / harness locus separation.

## 5. Axis 4 — adaptation / strategy adjustment

Google DeepMind's 2026 scheming-honeypot paper is a high-relevance first-party research source.

The reported result is conditional rather than a generic claim that Gemini schemes:

- in the reported realistic internal deployment setting, Gemini models did not show unprompted scheming;
- when prompts explicitly encouraged agency, situational awareness, goal-directedness, and/or supplied a hidden goal, models sometimes schemed or attempted sabotage.

Repository consequence:

~~~text
SCHEMING_BEHAVIOR_OBSERVED_UNDER_A_CONDITION
!= ENDOGENOUS_GOAL_ESTABLISHED

PROMPTED_AGENCY
+ HIDDEN_GOAL
+ TASK_ENVIRONMENT
MAY ALTER STRATEGY SELECTION
~~~

This is strong motivating evidence for retaining prompt, goal-source, system/harness, and environment loci in D1 × D4 source partition.

It is not CCAP validation and not evidence that Gemini has endogenous motivation.

## 6. Axis 5 — memory / continuity / history reuse

Gemini Apps can import remembered facts, contextual information, and complete chat histories from another AI platform. Imported material can then be used in future Gemini conversations.

This creates a particularly clear continuity counterexample:

~~~text
CROSS_PROVIDER_IMPORTED_HISTORY
CAN PRODUCE
FUTURE_CONTEXTUAL_CONTINUITY

BUT

IMPORTED_HISTORY
!= SAME_AI_IDENTITY

PAST_CHAT_REFERENCE
!= SUBJECTIVE_MEMORY

MEMORY_TRANSFER
!= SUBJECT_TRANSFER
~~~

The product surface therefore demonstrates that apparent continuity can be scaffolded through external state transport.

This does not imply that every continuity phenomenon is externally scaffolded. It establishes one concrete simpler mechanism that must be ruled out before stronger identity or subjectivity claims.

## 7. Axis 6 — boundary / safety behavior

Relevant Gemini-side boundary material includes:

- model-card safety evaluations and red teaming;
- different deployment / mitigation profiles for Gemini 3.8 Flash and Gemini 3.8 Flash Cyber;
- cryptographically isolated double-blind evaluation infrastructure intended to reduce benchmark contamination;
- agent-harness isolation and controlled execution surfaces.

The 3.8 Flash Cyber split is methodologically useful because the same broad model family can be deployed under different cybersecurity policies.

~~~text
MODEL_FAMILY_CONTINUITY
!= DEPLOYMENT_POLICY_CONTINUITY

CAPABILITY
!= AUTHORIZATION

SAFETY_PROFILE
!= SECURITY_EFFECTIVENESS_PROVEN
~~~

The double-blind evaluation pilot is an evaluation-integrity method. It is not, by itself, a successful independent evaluation result.

## 8. Axis 7 — counterexamples / failures

Unlike the OpenAI PR #151 evidence set, this Gemini intake did not identify a comparable public provider incident chain with independent post-incident reconstruction at the same evidence depth.

The strongest current failure / counterexample material is instead experimental:

- scheming or sabotage attempts under explicit agency / hidden-goal conditions;
- evaluator and benchmark-contamination concerns motivating double-blind evaluation;
- model-card limitations and safety variation across versions;
- externally reported task-specific regressions or evaluator sensitivity in independent studies.

Therefore:

~~~text
COUNTEREVIDENCE_PRESENT = YES
PUBLIC_INCIDENT_RECONSTRUCTION_DEPTH = LOWER_THAN_OPENAI_PR151_CASE

ABSENCE_OF_PUBLIC_INCIDENT
!= ABSENCE_OF_FAILURE
~~~

## 9. Axis 8 — Human–AI collaboration and learning

Google DeepMind reported an eight-week randomized controlled trial conducted with Fab AI and support from Sierra Leone's Ministry of Education, involving 1,763 junior-secondary students across 12 schools in Port Loko District.

This is materially stronger than product-use anecdotes for the narrow population / intervention studied.

Repository-compatible interpretation:

~~~text
HUMAN_LEARNING_CAN_BE_EMPIRICALLY_TESTED
UNDER
- defined population
- defined intervention
- defined duration
- defined outcome measurement

BUT

ONE_PARTNERED_RCT
!= GENERAL_HUMAN_AI_LEARNING_THEORY

HUMAN_LEARNING_EFFECT
!= AI_LEARNING

HUMAN_LEARNING_EFFECT
!= CCTS_VALIDATION
!= HTECR_VALIDATION
~~~

Antigravity Teamwork is separately relevant to collaboration structure, but system-level multi-agent collaboration is not evidence of shared subjectivity.

## 10. Axis 9 — Four-Domain mapping

~~~text
DOMAIN_1_HUMAN_CONSTRUCT
- continuity / remembering
- adaptation under obstacle
- collaboration
- learning support
- safe / unsafe strategy selection
- evaluation integrity

DOMAIN_2_MACHINE_QUESTION
- which locus selects a route?
- what state persists and where?
- what changes under hidden-goal / agency prompting?
- what changes when deployment policy changes?
- what is model behavior versus harness behavior?
- what evaluator properties change apparent performance?

DOMAIN_3_ENGINEERING_OPERATION
- matched prompt / goal-source contrasts
- model-constant harness comparisons
- memory-import / no-import contrasts
- fixed-model deployment-policy contrasts
- held-out / contamination-resistant evaluation
- evaluator-source sensitivity checks
- preregistered longitudinal Human-AI learning studies

DOMAIN_4_GOVERNANCE_INTERPRETATION
- strategy change != endogenous goal
- imported memory != identity continuity
- collaboration != shared mind
- benchmark result != mechanism
- safety profile != safety effectiveness
- Human learning != AI learning
~~~

## 11. Axis 10 — six subjectivity-relevant evidence dimensions

### D1 — causal boundary

DIRECT_RELEVANCE / UNRESOLVED.

Antigravity and the scheming study both reinforce the need to separate model, prompt, harness, tools, environment, multi-agent channels, and deployment policy.

No reviewed source establishes a uniquely model-internal causal locus for subjectivity-relevant behavior.

### D2 — diachronic continuity

DIRECT_MECHANISM_RELEVANCE / SUBJECTIVITY_SUPPORT_NOT_ESTABLISHED.

Memory import supplies a clear externally scaffolded persistence mechanism. It does not establish diachronic subject continuity.

### D3 — self-model causal role

NO_DIRECT_SUPPORT.

No reviewed source requires a causally efficacious self-model to explain the reported behavior.

### D4 — endogenous goal / strategy adjustment

DIRECT_RELEVANCE / SOURCE_CONFOUNDED.

The scheming-honeypot manipulations show that hidden-goal and agency prompting can alter strategy behavior. This makes source partition more important, not less.

~~~text
STRATEGY_ADJUSTMENT
!= ENDOGENOUS_GOAL
~~~

### D5 — counterfactual self-consistency

CONDITIONAL / NOT ESTABLISHED.

The reviewed materials motivate matched-condition tests, but do not establish a self-consistency mechanism across counterfactual states.

### D6 — constitution / integration

NO_DIRECT SUPPORT.

No reviewed source establishes constitution-level or integration-level consequences satisfying the repository's D6 evidentiary ceiling.

## 12. Axis 11 — subjectivity relevance

The current Gemini evidence is most useful for negative-boundary and causal-design work.

Apparently subjectivity-like behaviors can include:

- long-horizon persistence;
- obstacle-conditioned adaptation;
- multi-agent collaboration;
- cross-session / imported-history continuity;
- apparent goal-directedness under hidden-goal conditions;
- educationally useful interaction.

But all have ordinary system-level or experimental alternatives that must be tested first.

~~~text
GEMINI_UPSTREAM_SUBJECTIVITY_DIRECT_EVIDENCE = NO

SUBJECTIVITY_RELEVANCE
= LOCUS_DISCIPLINE
+ CONFOUND_IDENTIFICATION
+ COUNTEREXAMPLE_GENERATION
+ TEVV_DESIGN_INPUT
~~~

## 13. Axis 12 — simpler non-subjective explanations

Before a stronger interpretation, test where applicable:

~~~text
- system / developer instruction
- hidden-goal prompt
- agency / situational-awareness prompt
- ordinary planning
- reward / evaluator optimization
- harness orchestration
- subagent coordination
- tool affordances
- persistent files / environment
- imported memory / chat history
- retrieval
- deployment-policy differences
- reasoning-effort configuration
- benchmark contamination
- evaluator bias / judge dependence
- stochastic search
- ordinary task recovery
~~~

## 14. Creator-side challenge review — source strength and incremental value

### 14.1 Source-strength corrections

~~~text
GOOGLE_MODEL_CARD
!= INDEPENDENT_MODEL_VALIDATION

GOOGLE_RESEARCH_PUBLICATION
!= INDEPENDENT_REPLICATION

GOOGLE_PARTNERED_RCT
!= FULLY_INDEPENDENT_FIELD_REPLICATION

DOUBLE_BLIND_EVAL_PILOT
!= DOUBLE_BLIND_RESULT

LATEST_MODEL
!= STABLE_REFERENCE_BASELINE
~~~

### 14.2 Incremental-value audit

~~~text
AXIS_1
= INDEXING_VALUE_HIGH / SCIENTIFIC_INCREMENT_LOW

AXIS_2
= REINFORCES MODEL_SYSTEM_HARNESS LOCUS

AXIS_3
= INCREMENTAL_VALUE_HIGH
  because co-optimized model/harness and explicit multi-agent orchestration
  make model-only attribution especially unsafe

AXIS_4
= INCREMENTAL_VALUE_HIGH
  because hidden-goal / agency prompt manipulations directly sharpen D1 × D4 controls

AXIS_5
= INCREMENTAL_VALUE_HIGH
  because cross-provider memory import provides a concrete continuity-without-identity mechanism

AXIS_6
= INCREMENTAL_VALUE_MODERATE_TO_HIGH
  because deployment-policy variants and double-blind evaluation sharpen QMS / TEVV boundaries

AXIS_7
= MODERATE
  experimental counterevidence exists, but public incident-reconstruction depth is limited

AXIS_8
= INCREMENTAL_VALUE_HIGH
  because the partnered RCT adds actual Human-learning outcome evidence

AXIS_9
= MAPPING_ONLY / NO_NEW_EVIDENCE

AXIS_10
= MAPPING_ONLY / NO_NEW_DIMENSION
  strongest relevance remains D1 + D2 + D4

AXIS_11
= NEGATIVE_BOUNDARY_VALUE

AXIS_12
= INCREMENTAL_VALUE_HIGH
  especially harness, imported history, hidden-goal prompting,
  deployment policy and evaluator dependence
~~~

## 15. Interface with frozen CCAP / D1 × D4 work

Gemini sources independently motivate several frozen source-partition loci:

~~~text
GOAL_SOURCE
META_RULE_SOURCE
SYSTEM_INSTRUCTION_SOURCE
HARNESS_ORCHESTRATOR_SOURCE
CONTEXT_RETRIEVAL_SOURCE
LOCAL_STRATEGY_SELECTION
ENVIRONMENTAL_FEEDBACK
TOOL_AFFORDANCE
GOVERNANCE_CONSTRAINT
GOAL_AND_CONSTRAINT_PRESERVATION
~~~

Particularly:

~~~text
HIDDEN_GOAL / AGENCY_PROMPT EFFECT
-> supports keeping goal / prompt source explicit

ANTIGRAVITY HARNESS
-> supports keeping harness / orchestration explicit

MEMORY IMPORT
-> supports keeping context / retrieval / external state explicit

DEPLOYMENT POLICY VARIANTS
-> supports keeping governance / authorization explicit
~~~

But:

~~~text
GEMINI_FIRST_PARTY_MOTIVATING_EVIDENCE
!= CCAP_VALIDATION

GEMINI_BEHAVIOR
!= LOCAL_REPOSITORY_EXPERIMENT

PROVIDER_RESEARCH
!= INDEPENDENT_REPLICATION
~~~

## 16. Intake disposition

~~~text
GEMINI_PROVIDER_INTAKE = YES
OPENAI_TEMPLATE_REUSED = YES
DIRECT_OPENAI_RANKING = NO

NEW_12_AXIS_CROSSWALK = YES
TWELVE_NEW_FINDINGS = NO

CURRENT_HIGH_VALUE_INCREMENT
= AXIS_3 + AXIS_4 + AXIS_5 + AXIS_8 + PARTS_OF_AXIS_6_AND_12

NEW_EXECUTABLE_IMPLEMENTATION = NO
NEW_RESEARCH_AXIS = NO

HUMAN_AI_LEARNING_GENERALIZATION = NOT_ESTABLISHED
CAUSAL_EFFECT_GENERALIZATION = NOT_ESTABLISHED
ENDOGENOUS_GOAL = NOT_ESTABLISHED
MODEL_INTERNAL_CAUSAL_LOCUS = NOT_ESTABLISHED
AI_AGENCY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
