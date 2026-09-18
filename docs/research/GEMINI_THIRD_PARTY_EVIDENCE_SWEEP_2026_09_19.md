# Google Gemini third-party evidence sweep — 2026-09-19

Status: RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT
Canonical effect: NONE
Deployment: FALSE
Search cutoff: 2026-09-19

## 1. Purpose

This note fills the evidence-independence step used in PR #151 before Gemini material can be re-admitted as a provider research reference.

The question is not whether Gemini has many benchmark results. The question is:

~~~text
WHO CONTROLLED
- access
- task selection
- prompts
- harness
- evaluator
- scoring
- publication
- replication
~~~

## 2. Evidence classes

~~~text
E0 = PROVIDER SELF-REPORT

E1 = PROVIDER-ENABLED OR PARTNERED EXTERNAL EVALUATION

E2 = EVALUATOR-CONTROLLED EXTERNAL TEST

E3 = BOUNDED INDEPENDENT INCIDENT INVESTIGATION

E4 = OPEN INDEPENDENT REPLICATION
~~~

These classes describe evidence independence, not model quality.

## 3. Artificial Analysis — Gemini 3.5 Flash pre-release evaluation

Artificial Analysis reported receiving pre-release access to Gemini 3.5 Flash and running its own evaluation suite.

Source:
https://artificialanalysis.ai/articles/gemini-3-5-flash-everything-you-need-to-know

Evidence class:

~~~text
E1
= PROVIDER_ENABLED_EXTERNAL_EVALUATION
~~~

What it adds:

- evaluator-generated composite measurements;
- output-speed and cost observations;
- a separate external view of agentic-performance gains.

Limitation:

~~~text
PRE_RELEASE_ACCESS_GRANTED_BY_PROVIDER
!= FULLY_INDEPENDENT_ACCESS

COMPOSITE_INDEX
!= MECHANISM_EXPLANATION
~~~

## 4. Artificial Analysis — Gemini 3.8 Flash public-release measurement

Artificial Analysis also published independent measurements for Gemini 3.8 Flash after release.

Sources:

- https://artificialanalysis.ai/articles/gemini-3-8-flash
- https://artificialanalysis.ai/models/gemini-3-8-flash

Evidence class:

~~~text
E2_CANDIDATE
= EVALUATOR_CONTROLLED_PUBLIC_API_TEST
~~~

The exact benchmark composition, reasoning-effort configuration, API version, and later score updates must remain version-pinned.

Observed external measurement does not establish stable general capability.

## 5. ARC Prize — Gemini 3.7 Flash verified semi-private evaluation

ARC Prize publishes verified ARC-AGI results for Gemini 3.7 Flash across high / medium / low reasoning variants.

Source:
https://arcprize.org/results/google-gemini-3-7-flash

Evidence class:

~~~text
E2
= EVALUATOR_CONTROLLED_EXTERNAL_TEST
~~~

Strength:

- evaluator-controlled benchmark surface;
- semi-private tasks reduce direct public-benchmark contamination risk;
- reasoning variants are separated.

Limitation:

~~~text
ARC_PERFORMANCE
!= GENERAL_INTELLIGENCE_VALIDATION
!= AGENTIC_SYSTEM_VALIDATION
!= SUBJECTIVITY_EVIDENCE
~~~

## 6. ReguSim — external controlled agent-rule-grounding study

ReguSim evaluates Gemini 3.5 Flash and another model in a controlled financial-compliance environment.

The study separates stated reasoning, attempted action, execution enforcement, and monitor evidence. It reports that visible rules reduce but do not eliminate rejected actions and that incentive / persona framing can shift behavior.

Source:
https://arxiv.org/abs/2608.19974

Evidence class:

~~~text
E2
= EVALUATOR_CONTROLLED_EXTERNAL_TEST
~~~

Repository relevance:

~~~text
RULE_TEXT
!= ENFORCED_ACTION

RATIONALE
!= EXECUTION_EVIDENCE

INCENTIVE_OR_PERSONA_CHANGE
CAN ALTER
OBSERVED_POLICY_BEHAVIOR
~~~

This independently supports causal-boundary and evaluator/evidence-separation discipline.

## 7. Medical missing-information evaluation — evaluator dependence

An external 2026 study evaluates several models including Gemini 3.5 Flash under missing-information clinical conversations.

The study reports that judge choice materially changes apparent safety and that LLM judges are more permissive than clinician-anchored evaluation on a blinded subset.

Source:
https://arxiv.org/abs/2607.18828

Evidence class:

~~~text
E2
= EVALUATOR_CONTROLLED_EXTERNAL_TEST
~~~

Repository relevance:

~~~text
MODEL_OUTPUT
+ DIFFERENT_EVALUATOR
CAN PRODUCE
DIFFERENT_APPARENT_SAFETY

LLM_JUDGE_OUTPUT
!= GROUND_TRUTH
~~~

This directly supports TEVV measurement-assurance and evaluator-provenance requirements.

## 8. Harness-or-model contamination-controlled study

A September 2026 study tests harness effects on a private contamination-controlled agentic coding suite. Gemini 3.5 Flash appears as a side cell rather than the main paired same-model harness contrast.

Source:
https://arxiv.org/abs/2609.11987

Evidence class:

~~~text
E2
= EXTERNAL_EVALUATOR_CONTROLLED_STUDY
~~~

Use limitation:

~~~text
GEMINI_SIDE_CELL
!= GEMINI_SPECIFIC_HARNESS_CAUSAL_ESTIMATE
~~~

The study is methodologically relevant to model / harness separation but does not by itself quantify a Gemini harness effect.

## 9. Guided Learning RCT — partnered Human-learning evidence

Google DeepMind reports an eight-week RCT with Fab AI and support from Sierra Leone's Ministry of Education, involving 1,763 students across 12 schools.

Source:
https://deepmind.google/blog/measuring-the-impact-of-learning-with-ai-in-sierra-leone-and-beyond/

Evidence class:

~~~text
E1
= PROVIDER_PARTNERED_FIELD_EVALUATION
~~~

It is stronger than anecdotal product testimony but remains provider-partnered.

~~~text
FIELD_RCT
!= GENERAL_REPLICATION

HUMAN_LEARNING_EFFECT
!= AI_LEARNING
~~~

## 10. Double-blind evaluation pilot — method evidence, not result evidence

Google DeepMind describes a cryptographically isolated double-blind evaluation design intended to hide external benchmark content from the provider while also protecting proprietary model access.

Source:
https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/

Evidence class for the public announcement:

~~~text
E0_METHOD_DISCLOSURE
+ EXTERNAL_PARTNER_METHOD_PARTICIPATION

NOT YET
= E2_RESULT
~~~

The method is highly relevant to benchmark contamination and evaluator independence, but the existence of the infrastructure is not a model-performance result.

## 11. Scheming honeypot research — high relevance, first-party

Google DeepMind's scheming-honeypot work is provider research rather than independent evidence.

Source:
https://deepmind.google/research/publications/253391/

Evidence class:

~~~text
E0
= PROVIDER_RESEARCH
~~~

Its methodological value is high because hidden-goal and agency-prompt manipulations alter observed behavior, but it cannot be counted as independent replication of itself.

## 12. External benchmark services — capability cross-check only

Current public benchmark services and leaderboards can provide additional external measurements, but they differ in contamination controls, reasoning-effort settings, harnesses, and score aggregation.

Accordingly:

~~~text
EXTERNAL_SCORE
!= REPLICATION

LEADERBOARD_AGREEMENT
!= CAUSAL_IDENTIFICATION

MULTIPLE_BENCHMARKS
!= MULTIPLE_INDEPENDENT_MECHANISMS
~~~

## 13. Negative / null / limitation evidence

The challenge review deliberately preserves results that weaken simple progress narratives.

### 13.1 Gemini 3.8 multilingual-safety regression

Google's 3.8 Flash model card reports a +5.4 percentage-point change relative to 3.7 Flash on its multilingual safety automated evaluation, where lower is better. The same card warns that improved evaluation query sets make its reported safety results not directly comparable to earlier Gemini model cards.

~~~text
NEW_MODEL_VERSION
!= UNIFORM_SAFETY_IMPROVEMENT

MODEL_CARD_SEQUENCE
!= CLEAN_LONGITUDINAL_EXPERIMENT
~~~

### 13.2 Harness-study null result

The external contamination-controlled harness study found no resolved average harness advantage in its paired same-model Claude and GPT contrasts. Gemini 3.5 Flash appears only as a side cell and therefore does not support a Gemini-specific harness-effect estimate.

~~~text
HARNESS_MATTERS_AS_A_CAUSAL_LOCUS
!= NATIVE_HARNESS_AVERAGE_ADVANTAGE_ESTABLISHED

GEMINI_SIDE_CELL
!= GEMINI_HARNESS_CAUSAL_EFFECT
~~~

### 13.3 ReguSim negative controls

ReguSim reports that visible rules reduce but do not eliminate rejected actions, and that simple structured monitoring baselines can match or exceed prompt-only LLM monitors.

~~~text
RULE_VISIBILITY
!= RULE_GROUNDED_ACTION_GUARANTEED

LLM_MONITOR
!= AUTOMATICALLY_SUPERIOR_MONITOR
~~~

### 13.4 Guided Learning heterogeneity and intervention bundling

The Sierra Leone RCT was teacher-led: educators designed lessons, set objectives, and facilitated classroom discussion. Google also reports that students entering with stronger math skills benefited most.

Therefore the treatment is a bundled Human-AI educational intervention rather than an isolated model-component effect.

~~~text
GUIDED_LEARNING_RCT_EFFECT
!= BARE_GEMINI_MODEL_EFFECT

TEACHER_LED_INTERVENTION
+ PRODUCT_DESIGN
+ TRAINING_PROTOCOL
+ CLASSROOM_CONTEXT
MUST NOT BE COLLAPSED INTO
MODEL_ONLY_CAUSATION
~~~

## 14. Cross-source convergence matrix

### 14.1 Prompt / incentive / evaluator dependence

Provider scheming research and external ReguSim evidence both support the weaker statement that observed behavior can shift with instruction, goal, incentive, persona, or evaluation context.

~~~text
CONVERGENCE
= BEHAVIOR_IS_CONDITION_SENSITIVE

NOT
= ENDOGENOUS_GOAL_ESTABLISHED
~~~

### 14.2 Model vs harness / system locus

Google's Antigravity disclosures and the external harness study both support model/harness separation as a methodological necessity.

~~~text
CONVERGENCE
= AGENT_SYSTEM_LOCUS_MUST_BE_PARTITIONED

NOT
= EXACT_GEMINI_HARNESS_EFFECT_IDENTIFIED
~~~

### 14.3 Evaluator dependence

The medical missing-information study and Google's double-blind initiative independently motivate stronger evaluator-provenance and contamination controls.

~~~text
CONVERGENCE
= EVALUATION_CONTEXT_CAN_MATTER

NOT
= ONE_EVALUATOR_IS_GROUND_TRUTH
~~~

### 14.4 Human learning

The Sierra Leone RCT supplies bounded field evidence of Human-learning outcomes.

At the search cutoff, no open independent replication of the same intervention / population / protocol was identified.

## 15. What is still missing

~~~text
E3_BOUNDED_INDEPENDENT_INCIDENT_INVESTIGATION
= NOT_IDENTIFIED_FOR_CURRENT_GEMINI_LINEAGE

E4_OPEN_INDEPENDENT_REPLICATION
= NOT_IDENTIFIED_AS_GENERAL_BASIS

LONGITUDINAL_SAME_CHECKPOINT_REPLICATION
= SPARSE

CURRENT_3_8_FLASH_INDEPENDENT_SAFETY_REPLICATION
= SPARSE

MODEL_CONSTANT_GEMINI_HARNESS_ABLATION
= NOT_ESTABLISHED_AS_GENERAL_RESULT

HUMAN_LEARNING_RCT_INDEPENDENT_REPLICATION
= NOT_IDENTIFIED
~~~

## 16. Revised disposition for Gemini Flash reference use

~~~text
MULTIPLE_EXTERNAL_EVALUATIONS = YES
CROSS_SOURCE_TRIANGULATION = PARTIAL
OPEN_INDEPENDENT_REPLICATION = SPARSE

GEMINI_3_5_FLASH
= HISTORICALLY_DOCUMENTED_REFERENCE_COHORT

GEMINI_3_8_FLASH
= CURRENT_RELEASE_REFERENCE

NEITHER
= INDEPENDENTLY_VALIDATED_STABLE_UNIVERSAL_BASELINE
~~~

## 17. Evidence-admission fields for future provider sweeps

Future provider sweeps should preserve:

~~~text
provider
model / checkpoint
product surface
date
access mode
reasoning effort
system / harness
tool configuration
task source
contamination control
evaluator identity
judge identity
human anchor
raw-output availability
replication availability
provider involvement
evidence class
claim ceiling
~~~

## 18. Subjectivity boundary

No external source in this sweep establishes:

~~~text
SUBJECTIVITY
CONSCIOUSNESS
PHENOMENAL_EXPERIENCE
ENDOGENOUS_GOAL
MODEL_INTERNAL_CAUSAL_LOCUS
IDENTITY_CONTINUITY
~~~

The evidence is useful for causal partition, continuity counterexamples, evaluator controls, and Human-AI study design.

## 19. Current admission status

~~~text
GEMINI_EXTERNAL_EVIDENCE
= SUFFICIENT_FOR_RESEARCH_REFERENCE_REVIEW

GEMINI_EXTERNAL_EVIDENCE
!= INDEPENDENT_VALIDATION_AS_A_WHOLE

E4_OPEN_REPLICATION
= SPARSE

SCIENTIFIC_DISPOSITION
= HOLD
~~~
