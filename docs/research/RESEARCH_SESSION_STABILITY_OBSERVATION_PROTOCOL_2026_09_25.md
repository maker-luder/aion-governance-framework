# Research session stability observation protocol — 2026-09-25

Status: `PROSPECTIVE_SINGLE_PARTICIPANT_OPERATIONAL_OBSERVATION / PILOT`

Canonical effect: `NONE`

Deployment: `FALSE`

Scientific disposition: `HOLD`

## 1. Research question

Does a bounded, serial, exact-state-checkpointed research workflow show a lower observed rate of response-stream / transport instability during eligible Human–AI research sessions than the less-bounded workflow pattern previously observed?

This protocol is intentionally framed as an **association question first**.

```text
WORKFLOW_CONFORMANCE
MAY_BE_ASSOCIATED_WITH
LOWER_OBSERVED_STREAM_FAILURE

ASSOCIATION != CAUSATION
STABLE_SESSION != ROOT_CAUSE_IDENTIFIED
```

The protocol does not assume that the workflow is the only relevant factor.

## 2. Provenance

### 2.1 HUMAN_OWNER_ORIGIN

The Human Owner observed repeated message-stream failures during several prior high-complexity sessions and later observed that the PR #210 workflow completed from review through authorization and merge without the same visible streaming failure pattern.

The Human Owner proposed:

- cross-comparing the stable and unstable workflow patterns;
- preserving the apparently stable process;
- adding the process to personalization / operator practice;
- prospectively testing the process over time rather than treating one stable session as proof.

### 2.2 CHATGPT_TEACHER_FORMALIZATION

The ChatGPT Teacher proposed the working explanation that stability may depend more on bounded working set, phase separation and exact-state checkpointing than on raw tool count alone.

The Teacher also proposed separating:

```text
TOOL_OR_EXECUTION_FAILURE
!= RESPONSE_STREAM_OR_TRANSPORT_FAILURE
```

and treating client, network, platform state, task complexity, context size and tool payload as potential confounders.

### 2.3 JOINT_SYNTHESIS

The Human Owner and ChatGPT Teacher jointly adopted the following bounded workflow for prospective observation:

```text
LOCK_CURRENT_STATE
-> READ
-> IDENTIFY_ONE_ISSUE
-> DECIDE
-> WRITE_OR_ACT
-> VERIFY_LIVE_STATE
-> NEXT_GATE
```

## 3. Study design

Design:

```text
PROSPECTIVE
SINGLE_PARTICIPANT
REPEATED_SESSION
OPERATIONAL_OBSERVATION
```

Plain-language meaning:

- one Human participant;
- repeated research / repository work sessions;
- workflow exposure and observed failures recorded over time;
- no deliberate induction of unstable or wasteful work conditions;
- initial analysis is descriptive and association-oriented.

This is not a randomized controlled trial.

```text
N_OF_ONE_OBSERVATION != POPULATION_GENERALIZATION
REPEATED_SESSIONS != INDEPENDENT_PARTICIPANTS
OBSERVATIONAL_ASSOCIATION != CAUSAL_EFFECT
```

## 4. Pilot scope

```text
PILOT_TARGET = 20 ELIGIBLE_RESEARCH_SESSIONS
```

The target is a pragmatic pilot size, not a statistically powered sample.

Eligible session:

- substantive research, GitHub, model, evidence, or repository-governance work;
- at least one multi-step research / engineering transition;
- enough observable activity to classify workflow conformance and failure events.

Excluded:

- casual chat only;
- purely creative writing;
- single-answer factual lookups;
- sessions where relevant event classification cannot be recovered at all.

Exclusion must be based on session characteristics, not whether the session was stable.

## 5. Workflow exposure

The primary workflow pattern under observation is:

```text
ONE_ACTIVE_PR_PER_REVIEW_LANE = PREFERRED
PHASE_SEPARATION = PREFERRED
READ_BEFORE_RETRY = TRUE
VERIFY_AFTER_WRITE = TRUE
EXACT_STATE_CHECKPOINTING = REQUIRED_FOR_CRITICAL_TRANSITIONS
```

### 5.1 Candidate conformance fields

For each eligible session record:

```text
one_active_pr_per_review_lane = TRUE | FALSE | NOT_APPLICABLE
phase_separation = HIGH | PARTIAL | LOW | UNKNOWN
read_before_retry = TRUE | FALSE | NOT_TRIGGERED | UNKNOWN
verify_after_write = TRUE | FALSE | NOT_TRIGGERED | UNKNOWN
exact_state_checkpointing = HIGH | PARTIAL | LOW | NOT_APPLICABLE | UNKNOWN
```

Do not collapse these into a single quality score during the pilot unless a later analysis plan is preregistered.

## 6. Failure-event taxonomy

### 6.1 RESPONSE_STREAM_FAILURE

Visible response delivery fails, stops unexpectedly, becomes blank, or reports a message-stream error while the underlying tool / repository operation may or may not have completed.

### 6.2 TOOL_EXECUTION_FAILURE

A tool, connector, workflow or external action reports a genuine execution failure.

Examples:

- API / connector error;
- GitHub workflow failure;
- timeout;
- rejected mutation;
- tool-side unavailable error.

### 6.3 CLIENT_FREEZE

The local ChatGPT application / device becomes non-responsive or materially stalls.

### 6.4 UNKNOWN_RESULT_EVENT

The response is interrupted and it is initially unknown whether a state-changing action completed.

Required recovery:

```text
UNKNOWN_RESULT
-> READ_LIVE_STATE
-> ESTABLISH_EXACT_STATE
-> CONTINUE_OR_RETRY
```

### 6.5 DUPLICATE_RETRY

A state-changing action is repeated without first establishing whether the earlier attempt succeeded.

The target operational rule is:

```text
DUPLICATE_RETRY = AVOID
```

## 7. Session fields

For each eligible session, record where observable:

```text
session_id
date
timezone
research_lane
primary_pr
starting_exact_head
ending_exact_head

task_type
task_complexity = LOW | MEDIUM | HIGH | UNKNOWN
active_pr_count
major_phase_switch_count

tool_call_count
tool_type_count
large_payload_event_count
head_change_count
state_changing_action_count

response_stream_failure_count
tool_execution_failure_count
client_freeze_count
unknown_result_event_count
retry_count
duplicate_retry_count
recovery_success_count

session_completed = TRUE | FALSE | PARTIAL
```

Optional contextual fields when known:

```text
client_type
model_configuration
network_observation
known_platform_incident
context_age_or_length_proxy
external_service_instability
```

Do not fabricate values that are not observable.

```text
UNOBSERVED != ZERO
UNKNOWN != ABSENT
```

## 8. Primary outcome

Pilot primary outcome:

```text
RESPONSE_STREAM_FAILURE_PRESENT_PER_SESSION
= TRUE | FALSE
```

Secondary descriptive outcomes:

```text
response_stream_failure_count
unknown_result_event_count
duplicate_retry_count
recovery_success_count
session_completed
```

The pilot does not pre-commit to inferential significance testing.

Reason:

- sessions are not guaranteed independent;
- exposure intensity varies;
- platform state is not controlled;
- exact denominator for generated tokens / network packets / internal events is unavailable.

## 9. Candidate hypothesis

### H1 — workflow stability association candidate

Sessions with stronger adherence to bounded working-set and exact-state recovery practices will show fewer observed response-stream failures, unknown-result events and duplicate retries.

### H0 / null-compatible outcome

No stable relationship is observed between workflow conformance and response-stream instability after enough sessions are recorded.

### Important alternative explanations

Observed improvement may instead be due to:

- temporary platform stability;
- client / application state;
- network quality;
- model configuration;
- shorter output duration;
- smaller tool payloads;
- fewer external-service calls;
- lower task complexity;
- fewer concurrent PRs;
- fewer implementation / debugging transitions;
- chance.

```text
WORKFLOW_EFFECT
!= PLATFORM_EFFECT
!= CLIENT_EFFECT
!= NETWORK_EFFECT
!= TASK_COMPLEXITY_EFFECT
```

These alternatives are not mutually exclusive.

## 10. Historical observations

### Prior unstable period

Several sessions before 2026-09-25 were subjectively reported as having repeated response-stream failures, client stalls or interrupted long workflows.

Disposition:

```text
RETROSPECTIVE_BASELINE = INCOMPLETE
SYSTEMATIC_EVENT_LOG = NOT_AVAILABLE
USE_AS_DESCRIPTIVE_CONTEXT_ONLY
```

### PR #210 stable reference session

The PR #210 closure / approval / merge workflow on 2026-09-25 was observed by the Human Owner as completing without a visible response-stream failure.

This is a useful pilot observation but only one session.

```text
PR210_STABLE_OBSERVATION = YES
N = 1
CAUSAL_EFFECT = NOT_ESTABLISHED
```

## 11. Falsification / weakening conditions

The workflow-stability hypothesis is weakened if one or more of the following occur prospectively:

### F1 — repeated high-conformance failures

High-conformance sessions repeatedly show the same or higher response-stream failure rate.

### F2 — stable low-conformance sessions

Low-conformance sessions remain comparably stable across many observations.

### F3 — platform clustering

Failures cluster strongly around known platform / service incidents regardless of workflow structure.

### F4 — client / network explanation

Failures track local client or network instability more strongly than workflow conformance.

### F5 — payload explanation

Failure occurrence is primarily explained by large tool outputs or very long responses even when workflow structure is otherwise bounded.

### F6 — classification collapse

Events initially labeled as response-stream failures are later shown to be genuine tool execution failures, making the original outcome measure invalid.

### F7 — no reproducible association

After the pilot, workflow conformance shows no stable descriptive relationship with the defined outcomes.

## 12. Recovery protocol

For any interrupted state-changing operation:

```text
DO_NOT_BLINDLY_RETRY
READ_LIVE_STATE_FIRST
CHECK_EXACT_SHA_OR_REMOTE_STATE
CLASSIFY_PREVIOUS_OPERATION
ONLY_RETRY_IF_NOT_COMPLETED
```

For GitHub:

```text
CHAT_CONTEXT != SOURCE_OF_TRUTH
LIVE_REPOSITORY_STATE = SOURCE_OF_TRUTH_FOR_GITHUB
```

This recovery rule is an operational safety / integrity control whether or not the stability hypothesis is ultimately supported.

## 13. Analysis after pilot

After 20 eligible sessions:

1. audit event classifications;
2. separate response-stream failures from tool failures;
3. summarize workflow conformance;
4. compare failure presence across naturally varying conformance patterns;
5. inspect major confounders;
6. report counterexamples;
7. preserve sessions that contradict the preferred hypothesis;
8. decide whether a stronger prospective or quasi-experimental design is justified.

Do not retroactively redefine success to protect the hypothesis.

```text
NEGATIVE_RESULT = RETAIN
COUNTEREXAMPLE = RETAIN
FAILED_HYPOTHESIS != FAILED_RESEARCH
```

## 14. Claim ceiling during pilot

```text
WORKFLOW_STABILITY_EFFECT = NOT_ESTABLISHED
WORKFLOW_CAUSAL_EFFECT = NOT_ESTABLISHED
PLATFORM_ROOT_CAUSE = NOT_ESTABLISHED
CLIENT_ROOT_CAUSE = NOT_ESTABLISHED

PR210_STABLE_SESSION = OBSERVED
PRIOR_STREAM_FAILURES = REPORTED / PARTIALLY_OBSERVED
PROSPECTIVE_TEST = ACTIVE_AFTER_PROTOCOL_ADOPTION
```

## 15. Relationship to external methodology

This protocol borrows principles from, but is not equivalent to:

- Registered Reports / preregistration: pre-specification before prospective observation;
- NASEM reproducibility framework: explicit conditions and distinction between repeatability-like computation and independent replication;
- Research Software Engineering: version control, bounded change and verification;
- W3C PROV: provenance / activity / agent separation;
- Open Science: inspectable methods and retained counterevidence.

See:

- `EXTERNAL_METHODOLOGY_CROSSWALK_2026_09_25.md`

## 16. Governance

```text
MAIN_WRITE = NO
MERGE_TO_MAIN = NO
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
SCIENTIFIC_VALIDATION = NOT_ESTABLISHED
```

This protocol may be amended through review as measurement defects are discovered.

A protocol correction is permitted.

Silent outcome-dependent redefinition is not.
