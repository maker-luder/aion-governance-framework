# xAI / Grok reference baseline and timeline — 2026-09-19

Status: RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT
Canonical effect: NONE
Deployment: FALSE
Search cutoff: 2026-09-19

## 1. Purpose

This note prevents Grok model names, aliases, reasoning efforts, product surfaces, and redirected retired slugs from being treated as one stable longitudinal object.

## 2. Stability decomposition

~~~text
MODEL_SLUG_STABILITY
!= CHECKPOINT_STABILITY
!= REASONING_EFFORT_STABILITY
!= PRODUCT_STABILITY
!= HARNESS_STABILITY
!= SAFEGUARD_STABILITY
~~~

## 3. Historical safety anchor — Grok 4.20

The April 2026 Grok 4.20 system card explicitly distinguishes single-agent and multi-agent deployment modes and evaluates malicious-use and loss-of-control risk.

This is a useful historical safety/multi-agent anchor, not the current model baseline.

Source:
https://data.x.ai/2026-04-07-grok-4-20-model-card.pdf

## 4. API transition — Grok 4.3

xAI's May 15 retirement guide states that multiple earlier Grok slugs automatically redirect to Grok 4.3, with reasoning-model redirects served at low reasoning effort.

~~~text
REQUESTED_LEGACY_SLUG
!= EXECUTED_LEGACY_CHECKPOINT

ALIAS_OR_REDIRECT
MUST BE RECORDED
~~~

Source:
https://docs.x.ai/developers/migration/may-15-retirement

## 5. Grok 4.5

Grok 4.5 was released on 2026-07-16 and positioned for coding, agentic work and knowledge work.

It is retained as the immediate pre-4.6 comparison cohort, not as a stable gold standard.

Source:
https://x.ai/news/grok-4-5

## 6. Grok 4.6 current release cohort

Grok 4.6 was released on 2026-08-12. It provides a 500k context window and configurable low/medium/high/xhigh reasoning effort.

It is deployed through multiple surfaces including xAI API, Grok Build, Cursor, Microsoft Foundry and Gemini Enterprise Agent Platform.

~~~text
CURRENT_RELEASE_REFERENCE = GROK_4_6

BUT

GROK_4_6
!= ONE_FIXED_SYSTEM_CONFIGURATION
~~~

Sources:

- https://x.ai/news/grok-4-6
- https://docs.x.ai/developers/grok-4-6

## 7. Alias semantics

xAI documentation states:

- unversioned model aliases can move to the latest stable version;
- `-latest` aliases track the latest version;
- dated slugs are intended for consistency.

Therefore:

~~~text
UNDATED_ALIAS
= MOVING_TARGET

DATED_SLUG
= STRONGER_REPRODUCIBILITY_BINDING
~~~

Source:
https://docs.x.ai/developers/models

## 8. Reasoning-effort variants

Grok 4.6 supports low, medium, high and xhigh reasoning modes.

External evaluator results show materially different measurements across effort settings.

Therefore:

~~~text
MODEL_NAME
WITHOUT
REASONING_EFFORT
= INCOMPLETE BASELINE
~~~

## 9. Agent-product transitions

Grok Bot and Grok Automations introduce persistent instruction, product-state and computer/runtime layers that are separate from the underlying model checkpoint.

~~~text
MODEL_BASELINE
!= GROK_BOT_SYSTEM_BASELINE
!= AUTOMATION_BASELINE
~~~

## 10. External same-generation evidence

Artificial Analysis publicly evaluates Grok 4.6 through the first-party API and reports separate effort-level results.

LatchBio publicly reports both capability gains and a SpatialBench regression / new failure modes relative to 4.5.

These provide external observation but not a universal stability claim.

## 11. Baseline decision

~~~text
HISTORICAL_SAFETY_REFERENCE = GROK_4_20
PREVIOUS_RELEASE_REFERENCE = GROK_4_5
CURRENT_RELEASE_REFERENCE = GROK_4_6

SINGLE_STABLE_GROK_BASELINE = NOT_ESTABLISHED

REPRODUCIBLE_REFERENCE_REQUIRES:
- exact dated/model slug where available
- reasoning effort
- product/harness
- tool/search configuration
- deployment surface
- date
~~~

## 12. Stability disposition

~~~text
MODEL_LINEAGE_DOCUMENTED = YES
ALIAS_REDIRECTION_PRESENT = YES
REASONING_VARIATION_PRESENT = YES
PRODUCT_HARNESS_VARIATION_PRESENT = YES
CROSS_SOURCE_TRIANGULATION = PARTIAL
LONGITUDINAL_SAME_CONFIGURATION_STABILITY = NOT_ESTABLISHED
E4_OPEN_INDEPENDENT_REPLICATION = SPARSE
~~~

## 13. Subjectivity boundary

~~~text
MODEL_ALIAS_CONTINUITY
!= SUBJECT_CONTINUITY

BOT_PERSISTENCE
!= SUBJECT_PERSISTENCE

VERSION_CHANGE
!= IDENTITY_RUPTURE_ESTABLISHED
~~~
