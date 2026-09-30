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


## 10. CCTS field-integrity observation — hypothesis-generating only

After the initial routing-drift record and upstream cross-check, the Human Owner added
a further observation about the collaboration itself:

> CCTS is jointly constructed by the Human Owner and ChatGPT Teacher; if either side is
> materially degraded, the current co-constructed field can itself be degraded because
> reciprocal revision and grounding no longer operate normally.

The repository already defines CCTS as requiring bounded problem representation,
Human and AI contributions, substantive reciprocal revision, provenance, claim
boundaries, authority separation, rejected-branch preservation and grounding adequate
for the current purpose. It also fails closed when an unresolved grounding mismatch
remains.

Relevant current anchors include:

- [`CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md`](CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md);
- [`CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md`](CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md);
- [`EPISTEMIC_AGENCY_CONTINUITY_AND_EVIDENCE_CEILING_2026_09_16.md`](EPISTEMIC_AGENCY_CONTINUITY_AND_EVIDENCE_CEILING_2026_09_16.md);
- [`CCTS_EPISTEMIC_ROBUSTNESS_PROBE_2026_09_16.md`](CCTS_EPISTEMIC_ROBUSTNESS_PROBE_2026_09_16.md).

The present episode is therefore **consistent with** the existing structural contract:
when one participant's contribution/revision/grounding behavior becomes unreliable,
the current interaction may fail to maintain the conditions needed for a valid CCTS
instance.

The episode additionally suggests a narrower operational burden that may be useful in
future study:

```text
PARTICIPANT_SIDE_DEGRADATION
-> GROUNDING_REPAIR_DEMAND
-> HUMAN_ERROR_DETECTION_AND_RECOVERY_COST
-> ATTENTION_DIVERTED_FROM_OBJECT_LEVEL_RESEARCH
-> CURRENT_CCTS_INTEGRITY_MAY_DEGRADE
```

In the observed interaction, the Human Owner had to spend additional effort detecting
tool-routing regression, re-establishing current repository rules, distinguishing
stale from current workflow, and restoring the earlier stable collaboration pattern.
That is retained as a naturalistic observation, not as a quantified outcome.

A corresponding preservation boundary is also important:

```text
CURRENT_CCTS_DEGRADATION
!= PRIOR_CCTS_ARTIFACT_DESTRUCTION

CURRENT_FIELD_INTEGRITY
!= HISTORICAL_ARTIFACT_SURVIVAL
```

Repository artifacts, provenance records, rejected branches and prior formalizations
can survive an unstable interaction and support later re-entry. Their survival does
not imply that the current interaction remained an intact CCTS during the unstable
period.

### 10.1 Candidate research question

This event may motivate, but does not yet establish, the following bounded question:

```text
RQ_CANDIDATE:
Under otherwise comparable task conditions, does participant-side interaction
degradation increase grounding-repair cost and reduce the ability of the Human-AI dyad
to maintain the repository-defined CCTS structural conditions?
```

Possible bounded observables for a later design could include:

- number of explicit grounding-repair turns;
- number of stale-rule or stale-workflow corrections;
- time or turns spent repairing collaboration rather than the object-level research
  question;
- unresolved grounding mismatch rate;
- reciprocal `REVISES` / `CHALLENGES` continuity before, during and after the
  degradation interval;
- successful re-entry using preserved repository artifacts.

No aggregate "CCTS quality score" is proposed.

### 10.2 Competing explanations and claim ceiling

The observed repair burden does not establish why the interaction degraded.

```text
PERSONALIZATION_REVERSION = HUMAN_OBSERVED_TEMPORAL_REVERSAL
PERSONALIZATION_CAUSAL_EFFECT = NOT_ESTABLISHED
UPSTREAM_CONTRIBUTION = POSSIBLE
LONG_CONTEXT_EFFECT = POSSIBLE
ORDINARY_RESPONSE_ERROR = POSSIBLE
MULTI_FACTOR_INTERACTION = POSSIBLE

EXCLUSIVE_CAUSE = NOT_ESTABLISHED
CCTS_CAUSAL_MECHANISM = NOT_ESTABLISHED
CCTS_EMPIRICAL_VALIDATION = NOT_ESTABLISHED
```

The Human Owner observed that interaction quality appeared to improve after returning
to the earlier personalization configuration. This temporal ordering makes a personalization-related explanation worth testing, but
it is not a controlled
dechallenge/rechallenge experiment and does not isolate personalization from concurrent
context or upstream changes.

```text
TEMPORAL_REVERSAL = OBSERVED_BY_HUMAN
TEMPORAL_REVERSAL != CONTROLLED_CAUSAL_IDENTIFICATION
```

### 10.3 Provenance of this extension

```text
CONTRIBUTION_ORIGIN = HUMAN_ORIGIN
CONTRIBUTOR_ACTOR = HUMAN_OWNER
CONTRIBUTION = identified that CCTS is jointly maintained and that material degradation
               on either participant side can disrupt the current co-constructed field;
               requested preservation of this event because it may have research value
               for CCTS

CONTRIBUTION_ORIGIN = AI_FORMALIZATION
CONTRIBUTOR_ACTOR = CHATGPT_TEACHER
CONTRIBUTION = mapped the observation onto existing CCTS grounding and reciprocal-
               revision requirements; separated current-field degradation from survival
               of prior artifacts; proposed bounded observables and preserved competing
               explanations without promoting a new CCTS definition

JOINT_SYNTHESIS
= participant-side instability may be a useful future stressor for studying CCTS
  field integrity, but this episode remains hypothesis-generating naturalistic evidence
```

Final status of this extension:

```text
CCTS_RESEARCH_RELEVANCE = PLAUSIBLE / HYPOTHESIS_GENERATING
CCTS_EXTENSION = NO
NEW_CANONICAL_DEFINITION = NO
NEW_FORMAL_HYPOTHESIS = NOT_YET
EXPERIMENT_AUTHORIZATION = NO
SCIENTIFIC_EFFECT = NONE
```

## 11. Evidence reconciliation and reverse review — 2026-09-30

This bounded Class D review reread the four CCTS anchors in section 10 at current
`main` `ba764cb735ddbde813378491d582616f071ef32f`, plus the current
bidirectional-grounding and tool-routing notes. The grounding admission contract
requires sufficiency for the current purpose and fails closed on unresolved mismatch;
its declared checkpoint is not an independent measure of mutual understanding.
The formalization requires substantive reciprocal `REVISES`/`CHALLENGES` paths.
Neither structural rule measures the 2026-09-30 episode.

### 11.1 External-source ledger and applicability

- **S1 — Shaikh et al. (2024), NAACL, peer-reviewed empirical generation
  comparison**, [DOI 10.18653/v1/2024.naacl-long.348](https://doi.org/10.18653/v1/2024.naacl-long.348).
  Simulated model turns in human dialogue datasets on teaching, persuasion and
  emotional support; model generations contained fewer grounding acts than human
  responses to the same contexts. This compares generated turns, not longitudinal
  repository research, actual repair cost or this account's model configuration.
- **S2 — Shaikh et al. (2025), ACL, peer-reviewed observational log analysis and
  benchmark**, [DOI 10.18653/v1/2025.acl-long.1016](https://doi.org/10.18653/v1/2025.acl-long.1016).
  WildChat, Bing Chat and human-wizard MultiWOZ interactions: users initiated
  substantially more clarification/follow-up and repair in the human–LLM logs;
  early grounding failures predicted later breakdown in those data. Logs,
  annotated acts and a selected benchmark do not identify a causal mechanism.
  The authors note unavailable Bing system prompts, WildChat-derived task
  selection and imperfect automated annotation. S2 cites S1 and shares a lead
  author: the two are related studies, not independent replication of CCTS.
- **S3 — Hagemann et al. (2023), peer-reviewed perspective**,
  [DOI 10.3389/frai.2023.1252897](https://doi.org/10.3389/frai.2023.1252897).
  A conceptual account of coordination, shared task models and breakdown
  detection in human–AI/multi-team work; no episode-specific experiment.
- **S4 — Zhou et al. (2025), peer-reviewed conference-proceedings research**,
  [DOI 10.1177/10711813251369372](https://doi.org/10.1177/10711813251369372).
  Ten teams in a remotely piloted aircraft simulation with a human teammate
  introducing incorrect information. Qualitative analysis distinguished timely
  verification and structured communication in successful adaptation, but the
  quantitative navigator-influence/performance hypothesis was **not supported**.
  Small sample and one perturbation type; human–human team evidence only.
- **S5 — Graesser et al. (2018), peer-reviewed integrative review**,
  [DOI 10.1177/1529100618808244](https://doi.org/10.1177/1529100618808244).
  The publisher abstract surveys theoretical and empirical collaborative
  problem-solving research; this review checked the abstract-level scope, not a
  direct CCTS result or a specific effect size.
- **S6 — Krzywdzinski et al., published online 2025, 2026 issue, peer-reviewed
  laboratory experiment**,
  [DOI 10.1007/s00146-025-02761-5](https://doi.org/10.1007/s00146-025-02761-5).
  Human teams managed simulated production breakdowns with a fixed-output,
  partially autonomous AI recommendation aid; self-managed teams communicated
  more effectively and performed better than hierarchical teams in that setting.
  The paper explicitly limits transfer beyond simplified tasks. Its AI did not
  serve as a conversational co-researcher, and its mediation analysis cannot be
  transferred to CCTS.
- **S7 — Poelitz et al. (2026), arXiv preprint only**,
  [DOI 10.48550/arXiv.2602.21337](https://doi.org/10.48550/arXiv.2602.21337).
  A puzzle benchmark and confirmatory study with 40 UK English-fluent
  participants interacting with one GPT-4.1 configuration. The authors describe
  common-ground repair and divergences from human–human patterns. A benchmark
  study in a narrow task does not validate our taxonomy; no peer-reviewed
  publication was established in this review.

`EXTERNAL_SOURCE` describes the papers' own populations and tasks.
`REPOSITORY_STATE` describes our local definitions and artifact records.
`HUMAN_ORIGIN` describes the reported episode and temporal recovery;
`AI_FORMALIZATION` maps it to the candidate chain; `JOINT_SYNTHESIS`
is the bounded stressor question. `PROVENANCE != CORRECTNESS`.

### 11.2 Claim–evidence matrix

| Claim | Evidence source | Evidence type | Direct / adjacent | Disposition | Population | Task | Limitation | Claim ceiling |
|---|---|---|---|---|---|---|---|---|
| C1. Participant-side degradation can disrupt coordination | S4; S3 | Human-team simulation; human–AI perspective | Adjacent | Partial | Ten human teams; conceptual human–AI teams | Incorrect teammate information; team coordination | S4 main quantitative hypothesis unsupported; no degraded AI co-researcher | Plausible team-level stressor, not a measured CCTS effect |
| C2. Grounding failure can predict or contribute to later breakdown | S2 | Human–LLM log analysis | Direct for prediction, not causation | Support for prediction; causal contribution unknown | WildChat/Bing users and MultiWOZ comparator | Multi-turn assistant dialogue | Selection, prompts and annotator limits; no randomized failure | Association within studied logs |
| C3. Human–AI grounding burden can become asymmetric | S2; S1; S7 | Logs; generation comparison; preprint task | Direct for S2's acts; adjacent elsewhere | Support | Assistant users; human dialogue comparators; puzzle participants | Clarification, follow-up, repair | Act frequencies are not cognitive-cost measurements; S7 preprint | Asymmetry in observed initiation/repair, not universal burden |
| C4. Repair burden can shift work onto the Human participant | S2; local Human report | Logs plus naturalistic self-report | Direct for who initiates repair; adjacent for effort/cost | Partial | Assistant users; this Human Owner | Dialogue repair; repository-rule recovery | No measured attention, time, or counterfactual in this episode | Candidate human repair cost, unquantified locally |
| C5. Shared understanding/common ground matters in collaborative problem solving | S5; S3; S7 | Integrative review; perspective; preprint | Adjacent | Support for research relevance | Human teams; conceptual human–AI teams; puzzle dyads | Collaborative problem solving and coordination | No exact CCTS structural taxonomy test; S5 abstract checked | Adjacent construct support only |
| C6. A degraded participant can force team-level adaptation | S4; S6 | Human-team simulation; AI-aided production lab | Adjacent | Partial | Ten human teams; production teams with AI aid | Teammate misinformation; automation failure | S4 quantitative null; S6 AI aid and team-organization manipulation differ | Possible adaptation, not inevitable or CCTS-specific |
| C7. Current interaction degradation does not imply historical artifact destruction | Current branch record; repository git state | Logical/state distinction | Direct as repository-state distinction | Support for distinction | This repository | Preserved files and current conversation | Persistence alone does not prove semantic usability or current-field integrity | Artifacts can survive; this episode does not measure their durability |
| C8. Repository artifacts may support re-entry after degradation | Current-main CCTS formalization and grounding hypothesis | Local structural design and candidate hypothesis | Adjacent to empirical claim | Partial | Repository-defined workflow | Artifact binding and future re-entry | No controlled re-entry comparison for this episode | Possible support, not measured recovery mechanism |
| C9. This episode validates CCTS | No direct study | Single naturalistic observation | Neither | Reject / NOT_ESTABLISHED | One Human–AI interaction | Interaction-routing drift | No controls, independent scoring, exact construct test or causal identification | Hypothesis-generating only |

The proposed sequence from participant-side change through mismatch, repair,
attention diversion and reciprocal-revision degradation is **a candidate chain**.
S2 supports some neighboring links in assistant dialogue; no source tests the
whole chain or distinguishes this episode from generic tool reliability and
coordination failure. In particular, the local report of diverted attention
does not quantify lost object-level research, and no `REVISES`/`CHALLENGES`
continuity was independently coded for this episode.

### 11.3 Citation-context and competing-explanation check

The S2 discussion invokes S1 for grounding gaps and adds log-level repair
analysis; S7 invokes S1/grounding theory as background for a different puzzle
benchmark. Those citations do not convert S1 into a replication of S2, or S7
into peer-reviewed confirmation of CCTS. A bounded Scite incoming-citation
graph for S1/S2 was truncated and had zero resolved incoming edges for S2;
the available S1 snippets were primarily **mentioning** contexts. It supplies
no reliable contrast/replication verdict and is not used to strengthen any row.

The same observation could arise from ordinary team coordination failure,
generic human–computer interaction failure, tool unreliability, stale
repository rules, long-context competition, ordinary response error,
upstream change or interacting factors. Neither the chronological improvement
after personalization reversion nor nearby provider incidents isolates one
factor. Provider status describes service events, not this dyad's hidden route;
third-party incident monitors do not prove a model-routing or personalization
defect.

```text
EXTERNAL_ADJACENT_SUPPORT = SUPPORTED_WITH_TASK_AND_POPULATION_LIMITS
EXACT_CCTS_TAXONOMY_MATCH = NOT_ESTABLISHED
CCTS_EMPIRICAL_VALIDATION = NOT_ESTABLISHED
CCTS_CAUSAL_MECHANISM = NOT_ESTABLISHED
PERSONALIZATION_CAUSAL_EFFECT = NOT_ESTABLISHED
UPSTREAM_CAUSAL_EFFECT = NOT_ESTABLISHED
ROOT_CAUSE = UNKNOWN
CURRENT_FIELD_INTEGRITY != HISTORICAL_ARTIFACT_SURVIVAL
```

### 11.4 Conditions that would weaken the candidate account

- A matched fresh interaction or generic coordination repair restores the
  task at comparable cost without repository artifact re-entry.
- Independent coding finds grounding and reciprocal-revision conditions
  intact during the reported drift, or no increase in repair turns.
- Apparent object-level diversion disappears under timestamped turn coding
  or is equally explained by task difficulty and review rigor.
- Repeating the personalization reversal with matched context, model and
  upstream conditions does not reproduce the apparent quality difference.
- Preserved artifacts cannot be retrieved or do not help reconstruct the
  bounded problem, provenance and rejected branches.

These are prospective discriminators, not experiments performed here.
No new CCTS definition, measurement result or main-branch authority follows
from this reconciliation.
