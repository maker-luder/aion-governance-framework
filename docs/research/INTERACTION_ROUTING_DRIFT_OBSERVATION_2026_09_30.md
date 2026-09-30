# Interaction-routing drift observation — 2026-09-30

Status: `REPOSITORY_RECORD / NATURALISTIC_OPERATIONAL_OBSERVATION / DOCUMENTATION_ONLY / SCIENTIFIC_EFFECT_NONE`

```text
BASE_MAIN_HEAD = ba764cb735ddbde813378491d582616f071ef32f
WRITE_TO_MAIN = NO
MERGE = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SCIENTIFIC_VALIDATION = NONE

CCTS_EXTENSION = NO
HUMAN_AI_LEARNING_CLAIM = NO
MODEL_QUALITY_CLAIM = NO
PRODUCT_BUG_CLAIM = NO
```

## 1. Purpose

This note preserves one bounded Human Owner–ChatGPT Teacher interaction in which the
Human Owner reported that the collaboration appeared materially less aligned with the
previous working pattern.

The event is retained because one operational deviation can be checked directly
against current repository controls, while several proposed causes cannot currently be
verified.

No private transcript is published. The note records only the minimum public-safe
abstraction needed for provenance and future comparison.

## 2. Human-origin observation

The Human Owner reported the following recent pattern:

- some responses appeared to depart from the previously stable interaction style;
- longitudinal context appeared to become less reliable or to surface stale working
  patterns;
- repository/tool workflow sometimes appeared inconsistent with the repository's
  current recorded practice;
- responses perceived as "fast" sometimes still identified real errors, while the
  overall interaction nevertheless felt contextually misaligned;
- the Human Owner preferred to retain the earlier stable working approach rather than
  immediately rewrite personalization again.

These are Human observations about the interaction surface.

```text
HUMAN_OBSERVATION != VERIFIED_MODEL_ROUTING
VISIBLE_RESPONSE_SPEED_OR_STYLE != VERIFIED_MODEL_CONFIGURATION
DISCOMFORT_OR_MISALIGNMENT_REPORT != PRODUCT_DEFECT_PROOF
```

## 3. Verified operational deviation

During the same discussion, ChatGPT Teacher interpreted a request to use the plugin
pipeline as a reason to invoke a broad set of tools.

A later live reread of
[`docs/governance/PR_TOOL_ROUTING_MATRIX.md`](../governance/PR_TOOL_ROUTING_MATRIX.md)
showed that the current repository rule is instead minimum-sufficient, trigger-based
routing:

```text
TOOL_AVAILABLE != TOOL_RELEVANT
MORE_TOOLS != BETTER_REVIEW
NO_TRIGGER -> DO_NOT_INVOKE
DUPLICATE_CAPABILITY -> USE_MINIMUM_SUFFICIENT_TOOL_SET
```

For the qualitative repository/person-alization/CCTS inspection that triggered this
event, several invoked capabilities had no demonstrated trigger. The broad invocation
was therefore inconsistent with current routing policy.

```text
TOOL_ROUTING_REGRESSION = OBSERVED
ROOT_CAUSE = UNKNOWN
```

This is an operational comparison against current repository policy, not a claim about
model internals.

## 4. Relevant repository ancestry

The current repository already records that the plugin workflow is an operational
artifact rather than a research construct:

- [`PLUGIN_PIPELINE_CONSTRUCT_NON_ADMISSION_RECORD_2026_09_26.md`](PLUGIN_PIPELINE_CONSTRUCT_NON_ADMISSION_RECORD_2026_09_26.md)
  retains selective task-dependent routing while rejecting promotion into a new
  construct;
- [`PR_TOOL_ROUTING_MATRIX.md`](../governance/PR_TOOL_ROUTING_MATRIX.md) requires
  explicit triggers and a minimum sufficient tool set;
- [`HUMAN_AI_BIDIRECTIONAL_GROUNDING_HYPOTHESIS_2026_09_11.md`](HUMAN_AI_BIDIRECTIONAL_GROUNDING_HYPOTHESIS_2026_09_11.md)
  already treats personalization, interaction history, memory and explicit rules as
  separable longitudinal conditions rather than an undifferentiated mechanism;
- [`RESEARCH_SESSION_STABILITY_OBSERVATION_PROTOCOL_2026_09_25.md`](RESEARCH_SESSION_STABILITY_OBSERVATION_PROTOCOL_2026_09_25.md)
  separates visible interaction/transport instability from tool execution and root-cause
  claims.

## 5. Competing explanations retained

The following explanations remain non-exclusive candidates:

```text
CANDIDATE_A = model / reasoning / routing difference
CANDIDATE_B = long-context instruction competition
CANDIDATE_C = stale historical workflow made salient
CANDIDATE_D = current live-state recovery was skipped or delayed
CANDIDATE_E = personalization-rule interaction or conflict
CANDIDATE_F = ordinary response error
CANDIDATE_G = interaction among multiple factors
```

At the time of this record:

```text
VERIFIED_HIDDEN_MODEL_ROUTE = UNKNOWN
PERSONALIZATION_CAUSAL_EFFECT = NOT_ESTABLISHED
LONGITUDINAL_CONTEXT_CAUSAL_EFFECT = NOT_ESTABLISHED
FAST_MODEL_CAUSAL_EFFECT = NOT_ESTABLISHED
```

A fast or short response may still contain a valid correction, and a deep response may
still be wrong. Response speed alone is not a valid proxy for reliability.

```text
FAST_RESPONSE != HIGHER_RELIABILITY
SLOW_RESPONSE != CORRECTNESS
ERROR_FOUND != ROOT_CAUSE_IDENTIFIED
```

## 6. Immediate disposition

The Human Owner chose not to perform another broad personalization rewrite in response
to this single event.

The bounded operational disposition is:

```text
PERSONALIZATION_REWRITE = NOT_AUTHORIZED
EARLIER_STABLE_WORKING_PATTERN = RETAIN_AS_PREFERRED_PRACTICE
LIVE_REPOSITORY_POLICY = RECHECK_WHEN_REPOSITORY_WORK_IS_IN_SCOPE
PLUGIN_PIPELINE = ADAPTIVE / MINIMUM_SUFFICIENT ROUTING
FULL_TOOL_FANOUT_BY_DEFAULT = NO
```

This disposition does not freeze future personalization changes. It records only the
decision made for this event.

## 7. Provenance

```text
CONTRIBUTION_ORIGIN = HUMAN_ORIGIN
CONTRIBUTOR_ACTOR = HUMAN_OWNER
CONTRIBUTION = observed the recent interaction drift, identified the mismatch with the
               previously stable working pattern, rejected immediate personalization
               over-rewrite, and requested preservation of this event in the repository

CONTRIBUTION_ORIGIN = AI_FORMALIZATION
CONTRIBUTOR_ACTOR = CHATGPT_TEACHER
CONTRIBUTION = reread live repository routing controls, confirmed the tool-routing
               regression against current policy, separated verified deviation from
               unverified causal explanations, and drafted this bounded record

REPOSITORY_STATE = EVIDENCE_CONTEXT
EXTERNAL_SOURCE = NONE_REQUIRED_FOR_THIS_RECORD
SOURCE_UNVERIFIED = hidden model/router state and any causal account not independently observed
```

## 8. Claim boundary

This record may be used later as:

- provenance for a known routing-regression episode;
- a comparison point for future interaction-stability observations;
- a prompt to recheck current live repository policy when stale historical workflow
  competes with current instructions.

It must not be used as evidence that:

- personalization caused the event;
- a specific hidden model or "fast model" caused the event;
- long context is inherently harmful;
- CCTS caused the event;
- Human–AI learning was established;
- a platform defect was established.

```text
OBSERVATION_RETAINED = TRUE
OPERATIONAL_DEVIATION_VERIFIED = TRUE
ROOT_CAUSE = UNKNOWN
SCIENTIFIC_EFFECT = NONE
```
