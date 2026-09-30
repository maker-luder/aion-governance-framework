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

For the qualitative repository/personalization/CCTS inspection that triggered this
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
EXTERNAL_SOURCE = OPENAI_OFFICIAL + THIRD_PARTY_MONITORING + THIRD_PARTY_PRESS
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


## 9. Recent upstream context and independent third-party cross-check — 2026-09-23 to 2026-09-30

This section was added after the Human Owner requested a bounded check of recent
OpenAI upstream conditions using both provider records and third-party evidence.

The purpose is contextual only:

```text
UPSTREAM_EVENT_PRESENT != CAUSE_OF_LOCAL_INTERACTION_DRIFT
TEMPORAL_OVERLAP != CAUSATION
THIRD_PARTY_CORROBORATION != ROOT_CAUSE_ANALYSIS
```

### 9.1 Provider-recorded events in the same window

OpenAI's own status and release surfaces recorded the following events:

- **2026-09-23:** elevated ChatGPT conversation error rates across Plus and Pro plans;
- **2026-09-23:** mobile users temporarily could not see Work Mode or the model picker;
- **2026-09-24:** elevated error rates on GPT-6 Astra Pro;
- **2026-09-25:** a GPT-6 Sol / GPT-6 Luna image-encoding bug was fixed after degrading
  image understanding in API and Codex visual tasks, including computer use;
- **2026-09-25:** Codex had a full outage affecting Codex Web, Codex API, CLI and the
  VS Code extension;
- **2026-09-29:** GPT-6.1 Sol was introduced and a large DevDay product rollout
  included new Codex cloud / review / security surfaces and other product changes;
- **2026-09-29:** OpenAI reported elevated errors across ChatGPT, Codex and APIs,
  including the Agents API, with failed requests, login/sign-up difficulty and
  incomplete tasks reported as possible symptoms.

Provider sources:

- https://status.openai.com/incidents/thedr16r
- https://status.openai.com/incidents/01M389CDQ97B11QPMSRAAYSE5S
- https://status.openai.com/incidents/m44fs25y
- https://status.openai.com/
- https://openai.com/products/release-notes/
- https://developers.openai.com/api/docs/changelog
- https://deploymentsafety.openai.com/gpt-6-1-sol/respecting-auto-review
- https://developers.openai.com/api/docs/models/gpt-6.1-sol
- https://devday.openai.com/

### 9.2 Independent monitoring corroboration

Independent service-monitoring sites corroborate that multiple OpenAI incidents were
visible during the same week.

IsDown recorded:

- the 2026-09-23 Work Mode / model-picker incident;
- the 2026-09-23 Plus / Pro conversation-error incident;
- the 2026-09-25 Codex outage, which its monitor reports detecting about two minutes
  before the corresponding official status update;
- the 2026-09-29 ChatGPT / Codex / API incident.

Sources:

- https://isdown.app/status/chatgpt
- https://isdown.app/status/openai/incidents/659836-mobile-users-unable-to-see-work-mode-and-the-model-picker
- https://isdown.app/status/openai/incidents/662418-elevated-errors-across-chatgpt-codex-and-the-api

APIStatusCheck independently summarized five OpenAI incidents within seven days at
the time of retrieval and showed the 2026-09-29 cross-product incident as a partial
outage:

- https://apistatuscheck.com/api/openai

These services are independent monitors, but some of their incident detail is sourced
from or reconciled against OpenAI's public status feed. They corroborate event
visibility and timing; they do not independently establish root cause.

### 9.3 Direct-probe evidence narrows the interpretation

A separate third-party monitor, AI API Incident History / llmlatency.dev, probes AI
provider inference endpoints directly from four regions every five minutes and does
not rely on provider status pages to decide whether an API outage occurred.

For the 72-hour window ending on 2026-09-29, its confirmed provider-outage list did
**not** attribute a multi-region API outage to OpenAI, even though OpenAI's status
page reported elevated errors across ChatGPT, Codex and APIs on 2026-09-29.

Source:

- https://llmlatency.dev/incidents

This is useful negative evidence:

```text
OPENAI_STATUS_REPORTED_CROSS_PRODUCT_DEGRADATION = TRUE
INDEPENDENT_FOUR_REGION_API_OUTAGE_CONFIRMATION = NOT_OBSERVED_IN_THIS_MONITOR
```

The two observations are not necessarily contradictory. The OpenAI incident included
login, ChatGPT, Codex, task-completion and API symptoms, while the direct-probe monitor
tests a bounded set of inference endpoints and applies a multi-region attribution
threshold. A partial, endpoint-specific, authentication-related or product-surface
incident could therefore be visible to users without satisfying that monitor's API
outage criterion.

Accordingly:

```text
"GLOBAL OPENAI API OUTAGE" = NOT_ESTABLISHED_BY_THIRD_PARTY_DIRECT_PROBES
"BROAD OPENAI PRODUCT DEGRADATION WAS REPORTED" = SUPPORTED
```

### 9.4 Independent reporting on the rapid product/model transition

Independent technology reporting also confirms that the same window contained a
high-density product/model transition.

VentureBeat independently reported the 2026-09-29 GPT-6.1 Sol launch, its pricing,
and the Ultrafast tier, while explicitly noting that the benchmark comparisons being
reported were OpenAI-run evaluations rather than independent production tests:

- https://venturebeat.com/technology/openais-gpt-6-1-sol-offers-astra-like-performance-at-1-5th-price-a-new-ultrafast-tier-clocks-at-300-tokens-per-second

TechCrunch independently reported the DevDay Codex changes, including reusable cloud
environments, the refreshed CLI, code review and Codex Security Cloud:

- https://techcrunch.com/2026/09/29/openai-gives-codex-reusable-cloud-environments-that-work-across-devices/

The Verge independently summarized the broader DevDay rollout:

- https://www.theverge.com/ai-artificial-intelligence/1001681/openai-devday-2026-biggest-news-announcements

Reuters independently reported the DevDay launch of OpenAI's Dots agent and noted
technical glitches during live demonstrations:

- https://www.reuters.com/business/openai-takes-meta-with-always-on-dots-agent-enterprise-ai-push-2026-09-29/

These reports independently establish that a major model/product rollout was occurring
during the same period. They do **not** establish that rollout activity caused the
Human Owner's reported interaction drift.

### 9.5 Cross-source disposition

The evidence supports a narrower statement than the initial suspicion:

```text
RECENT_UPSTREAM_CHANGE_DENSITY = HIGH
RECENT_OPENAI_INCIDENT_DENSITY = ELEVATED / MULTIPLE_RECORDED_EVENTS
THIRD_PARTY_EVENT_CORROBORATION = PRESENT
THIRD_PARTY_DIRECT_API_CONFIRMATION_FOR_2026_09_29 = MIXED / NOT_CONFIRMED
LOCAL_INTERACTION_DRIFT = OBSERVED
CAUSAL_LINK_TO_UPSTREAM = NOT_ESTABLISHED
```

Therefore the recent upstream environment is retained as a plausible contextual
variable for future comparison, not as the cause of this episode.

Possible future discriminating evidence would include:

- a provider root-cause analysis explicitly identifying routing, context, model-serving
  or personalization changes that overlap the observed period;
- reproducible before/after behavior under the same account, model, context and
  personalization conditions;
- independent telemetry showing the same failure mode rather than only general outage
  or deployment activity.

Until such evidence exists:

```text
UPSTREAM_CONTEXT = RETAIN
UPSTREAM_CAUSAL_ATTRIBUTION = HOLD
ROOT_CAUSE = UNKNOWN
```
