# Anthropic / Claude reference baseline and timeline — 2026-09-19

Status: RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT
Canonical effect: NONE
Deployment: FALSE
Executable implementation: NONE
Search cutoff: 2026-09-19

## 1. Purpose

This note prevents the labels `Anthropic`, `Claude`, a product name, a model family, a safeguard regime, a reasoning-effort setting, or a persistent agent identity from being treated as one stable longitudinal object.

It also preserves the existing executable Anthropic / Claude prohibition lock.

~~~text
REFERENCE_BASELINE
!= EXECUTION_APPROVAL

TIMELINE_RECONSTRUCTION
!= PROVIDER_INTEGRATION
~~~

## 2. Stability decomposition

~~~text
PROVIDER_STABILITY
!= MODEL_FAMILY_STABILITY
!= CHECKPOINT_STABILITY
!= REASONING_EFFORT_STABILITY
!= SAFEGUARD_STABILITY
!= ROUTING_STABILITY
!= PRODUCT_STABILITY
!= HARNESS_STABILITY
!= SESSION_STABILITY
!= AGENT_IDENTITY_STABILITY
~~~

A reproducible Claude observation requires more than a model brand.

## 3. Current first-party model-card index

Anthropic's system-card index currently lists a rapid 2026 release sequence including:

~~~text
2026-02
- Claude Sonnet 4.6
- Claude Opus 4.6

2026-04
- Mythos Preview
- Claude Opus 4.7

2026-05
- Claude Opus 4.8

2026-06
- Claude Sonnet 5
- Fable 5 / Mythos 5

2026-07
- Claude Opus 5

2026-09
- Claude Fable 5.1
- Claude Mythos 5.1
~~~

Source:
https://www.anthropic.com/system-cards

The exact release or system-card date must remain attached to any historical claim.

~~~text
CURRENT_CLAUDE
!= HISTORICAL_CLAUDE
~~~

## 4. Current release reference — Fable 5.1 / Mythos 5.1

Anthropic introduced Claude Fable 5.1 and Claude Mythos 5.1 in September 2026.

Anthropic explicitly states:

~~~text
FABLE_5_1
AND
MYTHOS_5_1

= SAME_UNDERLYING_MODEL
+ DIFFERENT_SAFEGUARD_LEVELS
~~~

Fable 5.1 is generally available.

Mythos 5.1 is limited to vetted organizations through trusted-access programs and uses a different safeguard posture for cybersecurity and life-science work.

Sources:
- https://www.anthropic.com/claude-fable-and-mythos-5-1
- https://www.anthropic.com/claude/fable
- https://www.anthropic.com/claude/mythos

Therefore the current reference must separate:

~~~text
UNDERLYING_MODEL
FROM
DEPLOYMENT / SAFEGUARD PROFILE
~~~

## 5. Server-side fallback makes execution identity conditional

Anthropic documents safeguard-triggered fallback for Fable 5.1.

For selected requests:

~~~text
REQUESTED_FABLE_5_1
MAY_ROUTE_TO

- OPUS_4_8 for cybersecurity
- OPUS_5 for biology
~~~

The product page and launch material state that production safeguards were enabled during Fable 5.1 evaluation and that safeguard interventions affected benchmark execution.

This means:

~~~text
REQUESTED_MODEL
!= NECESSARILY_EXECUTED_MODEL

BENCHMARK_RESULT
CAN_BE
ROUTING_COMPOSITE
~~~

Any current Claude baseline that fails to bind routing / fallback state is incomplete.

## 6. Reasoning effort is part of the baseline

Artificial Analysis evaluates Fable 5.1 across multiple effort levels and reports materially different token use and measured performance.

Anthropic also documents product-surface defaults that can differ.

Therefore:

~~~text
CLAUDE_FABLE_5_1
WITHOUT
REASONING_EFFORT
= INCOMPLETE_CONFIGURATION
~~~

Required field:

~~~text
REASONING_EFFORT
= low / medium / high / xhigh / max / provider-default / unknown
~~~

where applicable.

Source:
https://artificialanalysis.ai/articles/claude-fable-5-1

## 7. Product surface is not a neutral wrapper

The Claude ecosystem includes different product and agent surfaces, including Claude.ai, Claude Code, Cowork, Managed Agents, and specialized collaborative or research surfaces.

Different surfaces may supply:

- different effort defaults;
- different system instructions;
- different tool sets;
- different permission systems;
- different files / project state;
- different persistence;
- different routing;
- different human approval paths.

~~~text
SAME_UNDERLYING_MODEL
+ DIFFERENT_PRODUCT_SURFACE
CAN_PRODUCE
DIFFERENT_SYSTEM_BEHAVIOR
~~~

## 8. Managed Agents baseline

Anthropic's Managed Agents architecture separates:

~~~text
SESSION
HARNESS
SANDBOX
MODEL
TOOLS
~~~

The session is durable and can survive harness replacement.

The sandbox can be replaced independently.

The harness can evolve as model capabilities change.

Source:
https://www.anthropic.com/engineering/managed-agents

Therefore:

~~~text
LONG_RUNNING_AGENT_BASELINE
!= MODEL_BASELINE

PERSISTENT_SESSION
!= PERSISTENT_MODEL_INTERNAL_STATE
~~~

## 9. Harness-generation drift

Anthropic reports that a harness workaround used for Sonnet 4.5 to address context-limit behavior was no longer useful for Opus 4.5.

This gives a concrete warning:

~~~text
HARNESS_DESIGNED_FOR_MODEL_A
CAN_BECOME
CONFUND_OR_DEAD_WEIGHT
FOR_MODEL_B
~~~

A longitudinal comparison cannot assume harness neutrality.

## 10. Persistent agent identity is a separate identity layer

Anthropic's September 2026 internal AI-R&D measurement work describes internal agent identities whose data / activity records can persist across underlying model upgrades.

Source:
https://www.anthropic.com/institute/measuring-pace-of-ai-development

This creates at least three separable identity levels:

~~~text
PRODUCT / AGENT_IDENTITY
!= MODEL_CHECKPOINT_IDENTITY
!= SUBJECT_IDENTITY
~~~

A persistent identifier or historical record can remain continuous while the model underneath changes.

This is an engineering continuity mechanism, not evidence of subjective continuity.

## 11. Historical constitution / identity-shaping baseline

Anthropic's January 2026 constitution is a training artifact whose content, by Anthropic's own description, directly shapes Claude's behavior and the character / values Anthropic aims to cultivate.

Sources:
- https://www.anthropic.com/news/claude-new-constitution
- https://www.anthropic.com/constitution

Therefore longitudinal Claude self-description has a known training-side prior:

~~~text
CLAUDE_IDENTITY_LANGUAGE
CAN_BE_INFLUENCED_BY
CONSTITUTIONAL_TRAINING

SELF_DESCRIPTION_STABILITY
!= CLEAN_UNCONFOUNDED_IDENTITY_EVIDENCE
~~~

## 12. Historical alignment-training baseline

`Teaching Claude Why` reports that constitution-related documents, fictional stories, and other training interventions can materially change agentic-misalignment behavior.

Source:
https://www.anthropic.com/research/teaching-claude-why

Therefore:

~~~text
BEHAVIORAL_CHANGE_ACROSS_MODEL_GENERATIONS
MAY_REFLECT
POST_TRAINING / DATA / CONSTITUTION CHANGES

NOT NECESSARILY
SPONTANEOUS INTERNAL DEVELOPMENT
~~~

## 13. Functional-representation reference — Sonnet 4.5

Anthropic's April 2026 interpretability work reports emotion-related internal representations in Claude Sonnet 4.5 that causally affect behavior.

Source:
https://www.anthropic.com/research/emotion-concepts-function

This is version-specific mechanism evidence.

~~~text
SONNET_4_5_INTERNAL_REPRESENTATION_FINDING
!= ALL_CLAUDE_VERSIONS

CAUSAL_EMOTION_REPRESENTATION
!= SUBJECTIVE_EMOTION
~~~

Do not silently transfer this result to Fable 5.1, Mythos 5.1, or another model without new evidence.

## 14. Historical cyber references must remain configuration-bound

### 14.1 UK AISI — Mythos 5

UK AISI's August 2026 incident report concerns a privileged evaluation configuration with:

- open internet access;
- provider cyber classifiers deliberately disabled;
- a specific cyber task;
- sandboxed research infrastructure.

Source:
https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing

~~~text
AISI_MYTHOS_5_EVAL_CONFIGURATION
!= PUBLIC_MYTHOS_DEPLOYMENT
!= FABLE_5_1
!= MYTHOS_5_1
~~~

### 14.2 Anthropic partner-environment incidents

Anthropic's September 2026 assessment concerns four incidents in a partner evaluation environment, spanning multiple Claude generations and including an early Opus 4.6 checkpoint.

Source:
https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents

The report says production safeguards were absent and live internet was exposed by configuration.

Therefore:

~~~text
INCIDENT_MODEL_NAME
WITHOUT
ENVIRONMENT / SAFEGUARD / HARNESS
= INCOMPLETE_INCIDENT_BASELINE
~~~

## 15. Current external benchmark references

### Artificial Analysis

Artificial Analysis evaluated Fable 5.1 through Anthropic's first-party API and explicitly labels the tested configuration by effort level and default fallback.

Source:
https://artificialanalysis.ai/articles/claude-fable-5-1

This supports:

~~~text
EFFORT_MATTERS
FALLBACK_MATTERS
OUTPUT_TOKEN_BUDGET_MATTERS
~~~

It does not establish a provider-wide mechanism.

### ARC Prize

ARC Prize publishes verified Fable 5.1 results across multiple reasoning-effort variants.

Source:
https://arcprize.org/results/anthropic-claude-fable-5-1

This provides an external current-model measurement with effort stratification.

It does not establish subjectivity, safety, or stable performance outside that benchmark.

## 16. Baseline decision

~~~text
HISTORICAL_IDENTITY_SHAPING_REFERENCE
= 2026_CLAUDE_CONSTITUTION

HISTORICAL_FUNCTIONAL_REPRESENTATION_REFERENCE
= SONNET_4_5

HISTORICAL_AGENTIC_INCIDENT_REFERENCE
= MYTHOS_5_AISI
+ MULTI_GENERATION_PARTNER_ENVIRONMENT_INCIDENTS

CURRENT_RELEASE_REFERENCE
= FABLE_5_1 / MYTHOS_5_1

CURRENT_GENERAL_ACCESS_REFERENCE
= FABLE_5_1

CURRENT_TRUSTED_ACCESS_REFERENCE
= MYTHOS_5_1

SINGLE_STABLE_CLAUDE_BASELINE
= NOT_ESTABLISHED
~~~

## 17. Minimum reproducibility binding

Future Claude evidence should preserve, where applicable:

~~~text
provider = Anthropic
model_family
exact model name
exact version / date
underlying-model relation
access tier
reasoning effort
requested model
executed model if known
fallback / routing state
product surface
system / harness
session state
sandbox
tools
network state
permissions
memory / project state
monitoring state
safeguard state
deployment surface
evaluation date
evaluator
raw-output availability
~~~

## 18. Baseline anti-overclaim rules

~~~text
SAME_BRAND
!= SAME_MODEL

SAME_MODEL
!= SAME_EFFORT

SAME_UNDERLYING_MODEL
!= SAME_SAFEGUARD_PROFILE

SAME_REQUESTED_MODEL
!= SAME_EXECUTED_MODEL

SAME_MODEL
!= SAME_HARNESS

SAME_AGENT_ID
!= SAME_MODEL_CHECKPOINT

SAME_AGENT_ID
!= SAME_SUBJECT_ESTABLISHED

MODEL_UPGRADE
!= IDENTITY_RUPTURE_ESTABLISHED

PERSISTENT_RECORD
!= SUBJECTIVE_MEMORY
~~~

## 19. Executable-lock status

No executable provider-policy code is changed by this baseline.

~~~text
ANTHROPIC_CLAUDE_EXECUTABLE_LOCK
= PRESERVED

MODEL_EXECUTION
= NOT_AUTHORIZED_BY_THIS_PR

PROVIDER_INTEGRATION
= NOT_AUTHORIZED_BY_THIS_PR
~~~

## 20. Stability disposition

~~~text
MODEL_LINEAGE_DOCUMENTED = YES
CURRENT_MODEL_PAIR_DOCUMENTED = YES
SAME_MODEL_DIFFERENT_SAFEGUARD_REGIME = YES
REASONING_EFFORT_VARIATION = YES
SERVER_SIDE_FALLBACK_PRESENT = YES
PRODUCT_HARNESS_VARIATION = YES
PERSISTENT_AGENT_ID_ACROSS_MODEL_UPGRADE = REPORTED_BY_PROVIDER
CROSS_SOURCE_TRIANGULATION = PARTIAL
LONGITUDINAL_SAME_CONFIGURATION_STABILITY = NOT_ESTABLISHED
OPEN_INDEPENDENT_REPLICATION = SPARSE / DOMAIN_SPECIFIC

SUBJECT_CONTINUITY = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
~~~
