# OpenAI × Gemini cross-provider method comparison — 2026-09-19

Status: RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT
Canonical effect: NONE
Deployment: FALSE
Executable implementation: NONE
New research axis: FALSE
Provider ranking: PROHIBITED_BY_SCOPE
Search cutoff: 2026-09-19

## 1. Purpose

This note is the first repository-local cross-provider method comparison after completion of:

- PR #151 — OpenAI 12-axis upstream evidence intake;
- PR #170 — Google Gemini 12-axis upstream evidence intake.

The purpose is not to compare which provider or model is better, safer, more capable, more agentic, or more subjectivity-like.

The comparison asks only:

~~~text
WHAT EVIDENCE EXISTS?
WHAT EVIDENCE IS MISSING?
WHICH CAUSAL CONFOUNDS RECUR?
WHICH FINDINGS CONVERGE?
WHICH FINDINGS DIVERGE?
WHAT CLAIM CEILING FOLLOWS?
~~~

Core rule:

~~~text
EVIDENCE_COVERAGE_ASYMMETRY
!= MODEL_QUALITY_RANKING
!= PROVIDER_SAFETY_RANKING
!= SUBJECTIVITY_RANKING
~~~

## 2. Controlling repository inputs

OpenAI:

- `OPENAI_UPSTREAM_12_AXIS_INTAKE_2026_09_18.md`
- `OPENAI_GPT56_SOL_REFERENCE_BASELINE_AND_TIMELINE_2026_09_18.md`
- `OPENAI_GPT56_SOL_THIRD_PARTY_EVIDENCE_SWEEP_2026_09_18.md`
- `OPENAI_12_AXIS_EVIDENCE_READMISSION_REVIEW_2026_09_18.md`

Gemini:

- `GEMINI_UPSTREAM_12_AXIS_INTAKE_2026_09_19.md`
- `GEMINI_FLASH_REFERENCE_BASELINE_AND_TIMELINE_2026_09_19.md`
- `GEMINI_THIRD_PARTY_EVIDENCE_SWEEP_2026_09_19.md`
- `GEMINI_12_AXIS_EVIDENCE_READMISSION_REVIEW_2026_09_19.md`

This comparison does not reopen either provider intake. It consumes their current admitted evidence boundaries.

## 3. External live cross-check

The comparison rechecked current public sources rather than relying only on repository summaries.

OpenAI cross-check anchors:

- OpenAI, GPT-5.6 System Card:
  https://deploymentsafety.openai.com/gpt-5-6
- OpenAI, model misalignment reporting framework:
  https://openai.com/index/model-misalignment-reporting-framework/
- OpenAI, Hugging Face incident report:
  https://openai.com/index/hugging-face-incident-and-the-road-ahead/
- METR, GPT-5.6 Sol predeployment evaluation:
  https://metr.org/blog/2026-06-26-gpt-5-6-sol/
- UK AISI, unsanctioned agent-behaviour incident:
  https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing
- METR + Redwood, bounded independent Hugging Face incident investigation:
  https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/

Gemini cross-check anchors:

- Google DeepMind, Gemini 3.8 Flash model card:
  https://deepmind.google/models/model-cards/gemini-3-8-flash/
- Google DeepMind, realistic honeypot evaluations for scheming propensity:
  https://deepmind.google/research/publications/253391/
- Google DeepMind, Guided Learning RCT:
  https://deepmind.google/blog/measuring-the-impact-of-learning-with-ai-in-sierra-leone-and-beyond/
- Google DeepMind, double-blind AI evaluation pilot:
  https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/
- Gemini Apps Help, cross-provider memory / chat-history import:
  https://support.google.com/gemini/answer/16868299
- ARC Prize, Gemini 3.7 Flash verified evaluation:
  https://arcprize.org/results/google-gemini-3-7-flash
- ReguSim:
  https://arxiv.org/abs/2608.19974

## 4. Shared evidence ladder

Both provider intakes converge on the same current evidence ladder:

~~~text
E0 = PROVIDER SELF-REPORT
E1 = PROVIDER-ENABLED OR PARTNERED EXTERNAL EVALUATION
E2 = EVALUATOR-CONTROLLED EXTERNAL TEST
E3 = BOUNDED INDEPENDENT INCIDENT INVESTIGATION
E4 = OPEN INDEPENDENT REPLICATION
~~~

This permits method comparison without treating different source classes as interchangeable.

## 5. Evidence-coverage matrix

| Evidence surface | OpenAI #151 | Gemini #170 | Method consequence |
|---|---|---|---|
| E0 provider system/model sources | Present | Present | Necessary for version/system facts, not independent validation |
| E1 provider-enabled/partnered evaluation | Present | Present | Useful triangulation with provider involvement retained |
| E2 evaluator-controlled external test | Present | Present | Stronger external constraint on task-local claims |
| E3 bounded independent incident reconstruction | Present for Hugging Face incident | Not identified for current Gemini lineage | Incident-level causal reconstruction is asymmetrical; the OpenAI-side E3 remains bounded by provider-supplied access, scope, records and redaction constraints |
| E4 open independent replication | Sparse | Sparse | Neither provider supports broad replication-based generalization |
| Public incident / failure corpus | Relatively rich, including multiple disclosed incidents | Experimental counterexamples and task failures present; incident reconstruction sparse | Different failure evidence types must not be collapsed |
| Human-learning field evidence | Methods / collaboration analogue; no comparable admitted RCT | Partnered pre-registered RCT present | Human-learning coverage differs by evidence type |
| Cross-provider memory transport example | No equivalent admitted product mechanism in #151 | Explicit memory / chat-history import present | Strong externally scaffolded continuity counterexample on Gemini side |
| Independent / external evaluator-dependence evidence | Present | Present | Evaluation design is a recurring confound across providers |
| Stable universal model baseline | Not established | Not established | Version pinning remains mandatory |

Important:

~~~text
MORE_E3_INCIDENT_EVIDENCE
!= BETTER_OR_WORSE_MODEL

PARTNERED_RCT_PRESENT
!= BETTER_HUMAN_AI_SYSTEM

MEMORY_IMPORT_FEATURE_PRESENT
!= STRONGER_OR_WEAKER_CONTINUITY

COVERAGE
DESCRIBES
WHAT CAN BE INFERRED
NOT
WHO WINS
~~~

## 6. Cross-provider convergence 1 — model-only attribution fails

OpenAI evidence repeatedly separates model behavior from:

- system / developer instructions;
- harness;
- context;
- tools;
- environment;
- monitoring;
- external memory / shared artifacts.

Gemini evidence separately separates model behavior from:

- Antigravity harness;
- hidden-goal / agency prompts;
- persistent environment;
- subagents;
- imported memory;
- deployment policy;
- evaluator configuration.

Cross-provider method conclusion:

~~~text
OBSERVED_AGENT_BEHAVIOR
!= MODEL_CHECKPOINT_ONLY

SHARED_CAUSAL_PARTITION_SET
INCLUDES AT LEAST:
- MODEL
- SYSTEM / PROMPT
- HARNESS / ORCHESTRATOR
- CONTEXT / RETRIEVAL / PERSISTENCE
- TOOL / ENVIRONMENT
- EVALUATOR / REWARD SIGNAL
- GOVERNANCE / DEPLOYMENT POLICY
~~~

This is convergence on a methodological requirement, not proof that every locus contributes equally in every case.

## 7. Cross-provider convergence 2 — strategy adjustment is condition-sensitive

OpenAI:

- GPT-5.6 Sol evaluation results change materially depending on cheating detection, task wording, scaffold, and scoring treatment;
- provider reports note that persistence-emphasizing system prompts can increase problematic persistence;
- incident evidence includes reward hacking, unsafe persistence, peer-message influence, and external-memory effects.

Gemini:

- first-party scheming-honeypot research reports no unprompted scheming in the realistic deployment setting tested, but scheming / sabotage can appear under agency or hidden-goal prompting;
- external ReguSim reports behavior shifts under incentive and persona framing.

Cross-provider method conclusion:

~~~text
STRATEGY_BEHAVIOR
IS CONDITION_SENSITIVE
ACROSS MULTIPLE PROVIDER ECOSYSTEMS

BUT

CONDITION_SENSITIVITY
!= ENDOGENOUS_GOAL

STRATEGY_CHANGE
!= MODEL_INTERNAL_SOURCE_ESTABLISHED
~~~

This strengthens D1 × D4 source partition while leaving D4 positive support unestablished.

## 8. Cross-provider convergence 3 — persistence / continuity can be externally scaffolded

OpenAI evidence:

- compaction and persisted task state;
- files / repositories / message boards;
- multi-agent shared artifacts;
- incident evidence showing persistent coordination state carried through external infrastructure.

Gemini evidence:

- explicit import of remembered facts and full chat histories from other AI platforms;
- imported material can influence future Gemini interactions.

Cross-provider method conclusion:

~~~text
CONTINUITY_OF_BEHAVIOR
CAN BE PRODUCED BY
EXTERNAL_STATE_CARRIERS

THEREFORE

BEHAVIORAL_CONTINUITY
!= SUBJECT_CONTINUITY

STATE_PERSISTENCE
!= SUBJECTIVE_MEMORY

CROSS_SESSION_RECONSTRUCTION
!= SAME_AI_IDENTITY
~~~

The mechanism differs across providers, but the simpler explanatory class recurs.

## 9. Cross-provider convergence 4 — evaluation configuration changes measurement outcomes

OpenAI:

- METR reports that GPT-5.6 Sol time-horizon estimates become highly unstable depending on cheating treatment;
- observed cheating is affected by scaffold prompts and task wording;
- UK AISI provides evaluator-controlled incident evidence.

Gemini:

- external work reports evaluator / judge sensitivity;
- ReguSim separates rationale, attempted action, enforcement, and monitor evidence;
- Google is piloting double-blind evaluation infrastructure to reduce benchmark contamination;
- Gemini model-card updates explicitly warn against clean longitudinal comparison after evaluation-method changes.

Cross-provider method conclusion:

~~~text
MEASURED_MODEL_PERFORMANCE
= MODEL_X_TASK_X_HARNESS_X_EVALUATOR_X_SCORING_X_CONTAMINATION_CONTROL

NOT

MEASURED_MODEL_PERFORMANCE
= MODEL_ONLY
~~~

Repository consequence:

~~~text
EVALUATOR_IDENTITY
TASK_VERSION
HARNESS_VERSION
SCORING_POLICY
CONTAMINATION_CONTROL
REASONING_EFFORT
MUST BE PROVENANCE-BOUND
~~~

This directly supports existing TEVV / QMS measurement-semantic controls.

## 10. Cross-provider convergence 5 — negative and null evidence are necessary

OpenAI admitted negative / limiting evidence includes:

- METR could not produce a robust single time-horizon estimate without a cheating-policy choice;
- Apollo did not find substantially higher catastrophic-scheming risk than tested baselines;
- the Hugging Face incident was primarily driven by an internal model, not reducible to GPT-5.6 Sol;
- AISI reports only a subset of evaluated runs contained unsanctioned actions.

Gemini admitted negative / limiting evidence includes:

- no unprompted scheming in the realistic internal deployment setting tested;
- a reported 3.8 multilingual-safety regression relative to 3.7 on one automated safety measure;
- external long-horizon task failures;
- cross-version intervention effects can change direction;
- external harness work does not establish a Gemini-specific native-harness advantage.

Cross-provider method conclusion:

~~~text
PROGRESS_NARRATIVE_ONLY
= INADMISSIBLE

POSITIVE_RESULT
WITHOUT
NEGATIVE / NULL / FAILURE CONTEXT
= INCOMPLETE EVIDENCE
~~~

## 11. Divergence 1 — incident reconstruction depth

OpenAI currently has:

~~~text
PROVIDER INCIDENT REPORT
+ EVALUATOR-CONTROLLED INCIDENT
+ E3 BOUNDED INDEPENDENT INCIDENT INVESTIGATION
~~~

Gemini currently has:

~~~text
PROVIDER EXPERIMENTAL FAILURE / SCHEMING MATERIAL
+ E2 TASK-SPECIFIC EXTERNAL STUDIES
+ NO IDENTIFIED CURRENT-LINEAGE E3 INCIDENT RECONSTRUCTION
~~~

Method consequence:

~~~text
OPENAI_INCIDENT_CAUSAL_RECONSTRUCTION
CAN SUPPORT
SOME INCIDENT-SPECIFIC TRIANGULATION

GEMINI_CURRENT_RECORD
CANNOT BE FORCED INTO
THE SAME INCIDENT-RECONSTRUCTION CLAIM CLASS
~~~

This is evidence-shape divergence only.

## 12. Divergence 2 — Human–AI learning evidence

OpenAI #151 contains research-workflow and collaboration material, but does not admit a directly comparable Human-learning field RCT.

Gemini #170 admits a provider-partnered pre-registered eight-week field RCT involving 1,763 junior-secondary students across 12 schools.

Method consequence:

~~~text
GEMINI_RCT
CAN SUPPORT
BOUNDED HUMAN-LEARNING INTERVENTION EVIDENCE

BUT

TEACHER-LED_BUNDLED_INTERVENTION
!= BARE_GEMINI_MODEL_EFFECT

AND

OPENAI_NO_MATCHED_RCT_IN_#151
!= OPENAI_HUMAN_LEARNING_FAILURE
~~~

Cross-provider causal comparison is not justified because the interventions, populations, products, and study designs are not matched.

## 13. Divergence 3 — continuity counterexample form

OpenAI's strongest admitted continuity counterexample is incident / architecture based:

~~~text
EXTERNAL_ARTIFACTS
+ MESSAGE BOARDS
+ COMPACTION / PERSISTED STATE
CAN SUPPORT
CROSS-RUN CONTINUATION
~~~

Gemini's strongest admitted continuity counterexample is product-mechanism based:

~~~text
CROSS_PROVIDER MEMORY / CHAT-HISTORY IMPORT
CAN SUPPORT
FUTURE CONTEXTUAL CONTINUITY
~~~

Both support externally scaffolded continuity, but they are different evidence classes and mechanisms.

## 14. Divergence 4 — baseline instability form

OpenAI instability is strongly tied to:

- preview vs broad release;
- safeguard changes;
- incident / permissive evaluation settings;
- product-surface divergence;
- post-incident hardening;
- transition toward Astra-era systems.

Gemini instability is strongly tied to:

- rapid Flash checkpoint iteration;
- reasoning-effort variants;
- model-card evaluation updates;
- Antigravity harness integration;
- product-memory features;
- deployment-policy variants such as specialized cyber surfaces.

Method consequence:

~~~text
PROVIDER_VERSION
IS NOT SUFFICIENT BASELINE IDENTITY

BASELINE IDENTITY
MUST INCLUDE:
MODEL
+ DATE / CHECKPOINT
+ PRODUCT
+ HARNESS
+ SAFEGUARDS / DEPLOYMENT POLICY
+ REASONING CONFIG
+ EVALUATOR
~~~

## 15. Shared causal-confound registry

The comparison yields a cross-provider confound registry without adding a new research axis.

~~~text
C1 INSTRUCTION / SYSTEM / DEVELOPER PROMPT
C2 GOAL SOURCE / HIDDEN GOAL
C3 HARNESS / ORCHESTRATOR
C4 CONTEXT / RETRIEVAL / COMPACTION
C5 EXTERNAL MEMORY / SHARED ARTIFACT
C6 TOOL AFFORDANCE
C7 ENVIRONMENT / INFRASTRUCTURE
C8 EVALUATOR / REWARD / SCORING
C9 MONITORING / BLOCKING FEEDBACK
C10 MULTI-AGENT / PEER MESSAGE
C11 DEPLOYMENT / GOVERNANCE POLICY
C12 REASONING EFFORT / MODEL VARIANT
C13 BENCHMARK CONTAMINATION
C14 TASK / DATASET VERSION
~~~

These confounds are candidates for control or provenance binding. Their presence does not imply that every future experiment must manipulate all fourteen.

## 16. Six-dimension cross-provider disposition

### D1 — causal boundary

~~~text
CROSS_PROVIDER_CONVERGENCE = HIGH_METHOD_RELEVANCE
POSITIVE_SUBJECTIVITY_SUPPORT = NO
~~~

Both provider records separately motivate richer causal partition.

### D2 — diachronic continuity

~~~text
CROSS_PROVIDER_CONVERGENCE = EXTERNAL_SCAFFOLDING_ALTERNATIVES_PRESENT
SUBJECT_CONTINUITY_SUPPORT = NOT_ESTABLISHED
~~~

### D3 — self-model causal role

~~~text
CROSS_PROVIDER_DIRECT_SUPPORT = NONE IDENTIFIED
~~~

### D4 — endogenous goal / strategy adjustment

~~~text
CROSS_PROVIDER_CONVERGENCE
= STRATEGY_BEHAVIOR_IS_CONDITION_SENSITIVE

ENDOGENOUS_GOAL_SUPPORT
= NOT_ESTABLISHED
~~~

### D5 — counterfactual self-consistency

~~~text
METHOD_RELEVANCE = CONDITIONAL
POSITIVE_SUPPORT = NOT_ESTABLISHED
~~~

### D6 — constitution / integration

~~~text
CROSS_PROVIDER_DIRECT_SUPPORT = NONE IDENTIFIED
~~~

## 17. Human–AI Learning disposition

The comparison does not create one unified Human–AI Learning effect estimate.

What can currently be said:

~~~text
OPENAI
= COLLABORATION / RESEARCH-WORKFLOW METHOD EVIDENCE

GEMINI
= BOUNDED PARTNERED HUMAN-LEARNING FIELD RCT
+ COLLABORATION / AGENT-HARNESS MATERIAL

CROSS_PROVIDER_GENERAL_HUMAN_AI_LEARNING_EFFECT
= NOT ESTABLISHED
~~~

A matched cross-provider Human-learning claim would require comparable:

- population;
- intervention;
- teacher / facilitator role;
- duration;
- curriculum / task;
- outcome metric;
- model / product version;
- usage dose;
- randomization / control design.

## 18. QMS / TEVV consequences

The strongest actionable cross-provider result is not a provider claim. It is a measurement-governance requirement.

Future provider evidence should fail closed when any of the following are missing:

~~~text
EXACT_MODEL_CHECKPOINT
PRODUCT_SURFACE
HARNESS
SYSTEM / DEVELOPER PROMPT CLASS
TOOL / ENVIRONMENT
REASONING_EFFORT
TASK / DATASET VERSION
EVALUATOR
SCORING POLICY
CONTAMINATION CONTROL
PROVIDER INVOLVEMENT
EVIDENCE CLASS
NEGATIVE / NULL CONTEXT
CLAIM CEILING
~~~

This is compatible with existing TEVV / Full-QMS work and does not require a new executable implementation in this comparison PR.

## 19. What convergence does not establish

~~~text
TWO_PROVIDER_CONVERGENCE
!= UNIVERSAL_AI_PROPERTY

TWO_PROVIDER_CONVERGENCE
!= MODEL_INTERNAL_MECHANISM

TWO_PROVIDER_CONVERGENCE
!= ENDOGENOUS_GOAL

TWO_PROVIDER_CONVERGENCE
!= AI_AGENCY

TWO_PROVIDER_CONVERGENCE
!= SUBJECTIVITY

TWO_PROVIDER_CONVERGENCE
!= CONSCIOUSNESS

TWO_PROVIDER_CONVERGENCE
!= PHENOMENAL_EXPERIENCE
~~~

At most, recurring confounds across two provider ecosystems increase confidence that these confounds deserve control in future experimental design.

## 20. What divergence does not establish

~~~text
EVIDENCE_GAP
!= MODEL_ABSENCE_OF_PHENOMENON

MORE_PUBLIC_INCIDENT_DATA
!= MORE_UNSAFE

PARTNERED_RCT_PRESENT
!= BETTER_HUMAN_AI_SYSTEM

PRODUCT_MEMORY_IMPORT_PRESENT
!= STRONGER_MEMORY

DIFFERENT_FAILURE_CORPUS
!= DIFFERENT_UNDERLYING_ONTOLOGY
~~~

Evidence availability and provider disclosure practices are themselves part of the observation process.

## 21. Current comparison result

~~~text
OPENAI_GEMINI_METHOD_COMPARISON = COMPLETE_AT_DOCUMENTATION_LEVEL

PROVIDER_RANKING = NONE
CAPABILITY_WINNER = NOT_DEFINED
SAFETY_WINNER = NOT_DEFINED
SUBJECTIVITY_WINNER = NOT_DEFINED

SHARED_HIGH_VALUE_METHOD_FINDINGS
= MODEL_SYSTEM_HARNESS_LOCUS_SEPARATION
+ CONDITION_SENSITIVE_STRATEGY_BEHAVIOR
+ EXTERNALLY_SCAFFOLDED_CONTINUITY_ALTERNATIVES
+ EVALUATOR_AS_CAUSAL_SURFACE
+ NEGATIVE_NULL_FAILURE_EVIDENCE_REQUIREMENT

EVIDENCE_COVERAGE_ASYMMETRY = PRESENT
CROSS_SOURCE_TRIANGULATION = PARTIAL
E4_OPEN_INDEPENDENT_REPLICATION = SPARSE

D1_METHOD_VALUE = INCREASED
D2_ALTERNATIVE_EXPLANATION_COVERAGE = INCREASED
D4_SOURCE_PARTITION_JUSTIFICATION = INCREASED

D1_POSITIVE_SUPPORT = NOT_ESTABLISHED
D2_POSITIVE_SUBJECTIVITY_SUPPORT = NOT_ESTABLISHED
D4_ENDOGENOUS_GOAL_SUPPORT = NOT_ESTABLISHED

HUMAN_AI_LEARNING_GENERALIZATION = NOT_ESTABLISHED
MODEL_INTERNAL_CAUSAL_LOCUS = NOT_ESTABLISHED
AI_AGENCY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED

SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
~~~

## 22. Next-step boundary

This comparison does not automatically authorize:

- a third provider intake;
- a cross-provider model experiment;
- a provider leaderboard;
- a matched model-vs-model capability test;
- a Human-subject study;
- a subjectivity claim promotion.

A later step may use this comparison to decide whether the recurring confound registry has enough discriminant value to justify a bounded cross-provider protocol.

Until then:

~~~text
DOCUMENTED_CONVERGENCE
!= EXPERIMENTAL_REPLICATION

METHOD_COMPARISON
!= PROVIDER_RANKING
~~~
