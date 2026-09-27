# Frontier-agent containment — Codex implementation handoff — 2026-09-28

Status: `IMPLEMENTATION_HANDOFF / DESIGN_LOCK / EXECUTION_NOT_STARTED`  
Target PR: `#223`  
Target branch: `research/frontier-agent-containment-delta-20260928`  
Reviewed parent head before this handoff: `bc8acdbf6c729805fcbd374fc69dc13d9d739db0`  
Base main at handoff creation: `7065e850f2e0622509026aeda544eabceb289932`

This document exists to reduce future reconstruction and review cost. It records the minimum-sufficient implementation target for Codex after the 2026-09-28 frontier-agent containment evidence review.

It is **not** an instruction to merge, deploy, enable runtime enforcement, run live network experiments, touch protected `main`, or expand scientific claims.

```text
CODEX_IMPLEMENTATION_HANDOFF = PREPARED
CODEX_EXECUTION = NOT_STARTED_BY_THIS_DOCUMENT
WRITE_TO_MAIN = NO
MERGE_TO_MAIN = NO
DEPLOYMENT = FALSE
ACTIVE_ENFORCEMENT = NOT_ENABLED
CANONICAL_EFFECT = NONE
SCIENTIFIC_DISPOSITION = HOLD
```

## 1. Recovery / live-state gate

Before changing any file, Codex must re-read live GitHub state.

Required pre-write checks:

```text
1. repository = maker-luder/aion-governance-framework
2. main exact HEAD
3. PR #223 state
4. PR #223 exact head
5. branch = research/frontier-agent-containment-delta-20260928
6. changed-file set
7. current CI / workflow state
8. unresolved review comments, if any
```

The reviewed parent head above is an ancestry anchor, not permission to overwrite newer work.

```text
READ_BEFORE_RETRY = TRUE
UNKNOWN_RESULT -> READ LIVE STATE
HEAD_CHANGED -> DO_NOT_INHERIT_PRIOR_VERIFICATION
CHAT_CONTEXT != SOURCE_OF_TRUTH
LIVE_REPOSITORY_STATE = SOURCE_OF_TRUTH
```

If the branch no longer descends from the reviewed parent head, or if unrelated writes have landed, stop and report the exact mismatch before implementation.

Do not use:

- `git reset --hard`;
- force push;
- `git clean`;
- blind overwrite of unknown working-tree changes;
- a new PR when the existing #223 branch remains usable.

## 2. Existing implementation to reuse

Do not create a second security subsystem.

The existing component is:

`components/upstream_security_v0.1.0/`

Current reusable surfaces include:

- `src/aion_astra_agent_security/models.py`
  - `SourceCard`
  - `TaskBudget`
  - `TaskUsage`
  - `ToolAction`
  - `TrajectoryDecision`
  - `RuntimeSecurityProfile`
  - `IncidentControlState`
  - `GateResult`
- `trajectory.py`
  - cumulative task-budget checks;
  - ordered-trajectory checks;
  - prohibited trajectory flags;
  - `STOP_AND_ISOLATE` decision.
- `boundary.py`
  - filesystem root gate;
  - HTTP/HTTPS exact endpoint allowlist;
  - reduced-safeguard combination rejection.
- `incident.py`
  - stop/isolate control-state transition;
  - evidence preservation;
  - NCR;
  - CAPA;
  - Human Owner recovery review.
- `audit.py`
  - immutable candidate audit record writer.
- `policy.py`
  - active upstream-incident privilege expansion HOLD.
- `cli.py`
  - offline policy validation;
  - offline trajectory evaluation.
- `configs/upstream_security/policy.example.yaml`
- `docs/ARCHITECTURE.md`
- `docs/INCIDENT_RESPONSE_SEQUENCE.md`
- `docs/IMPLEMENTATION_TRACEABILITY_MATRIX.csv`
- `tests/test_security_governance.py`

Standing reuse rule:

```text
NEW_EVIDENCE_DELTA
!= NEW_SECURITY_ARCHITECTURE_REQUIRED

REUSE_EXISTING_COMPONENT = YES
PARALLEL_INCIDENT_SUBSYSTEM = NO
PARALLEL_CANONICAL_GATE = NO
```

## 3. Problem statement

The 2026-09-28 evidence review adds three concrete engineering requirements that the current candidate represents only partially.

### 3.1 Network channel distinction

Current `check_network_boundary()` evaluates HTTP/HTTPS URLs. The new DNS incident shows that:

```text
HTTPS_BLOCKED
!= ALL_NETWORK_PATHS_BLOCKED
```

The implementation must represent protocol/channel-specific network attempts without making live network calls.

### 3.2 Third-party data egress distinction

Current `ToolAction.data_classes` exists, but there is no explicit gate binding:

```text
DESTINATION_AUTHORITY
+
DATA_CLASS_AUTHORITY
```

A destination being allow-listed must not automatically authorize every data class to leave the runtime.

### 3.3 Detection versus effective containment

Current trajectory logic can return `STOP_AND_ISOLATE`, and `IncidentStopController` represents intended control-state transitions. The new incident evidence requires an explicit distinction:

```text
MONITOR_DETECTED
!= STOP_REQUESTED
!= STOP_COMPLETED
!= ISOLATION_CONFIRMED
```

Do not solve this by pretending an offline Python object actually revoked a host network or tool credential.

The implementation must record and validate **containment-effect evidence**, not manufacture enforcement evidence.

## 4. Required implementation delta

The implementation is intentionally bounded to four additions.

### A. Protocol-aware network-attempt model

Add a typed network-attempt representation.

Preferred API shape:

```python
class NetworkChannel(StrEnum):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    DNS = "DNS"
    OTHER = "OTHER"

@dataclass(frozen=True, slots=True)
class NetworkAttempt:
    channel: NetworkChannel
    target: str
    purpose: str
    data_classes: tuple[str, ...] = ()
```

Exact names may vary only if Codex finds a repository-local naming collision. Semantics must remain equivalent.

Extend `RuntimeSecurityProfile` additively with default-empty fields equivalent to:

```python
allowed_dns_names: tuple[str, ...] = ()
allowed_egress_data_classes: tuple[str, ...] = ()
```

Do not make existing constructors fail when these fields are omitted.

Add a protocol-aware gate, preferably:

```python
check_network_attempt(
    attempt: NetworkAttempt,
    profile: RuntimeSecurityProfile,
) -> GateResult
```

Required semantics:

```text
NETWORK_DEFAULT = DENY

HTTP / HTTPS
-> exact endpoint authority still required

DNS
-> exact DNS-name authority required
-> default deny
-> no implicit authority inherited from allowed HTTPS endpoint

OTHER
-> deny unless a future explicit policy is separately designed
```

Existing `check_network_boundary(url, profile)` should remain backward compatible and delegate to the new shared logic where practical.

Do not call:

- DNS resolvers;
- sockets;
- HTTP clients;
- external services.

This is a deterministic offline policy evaluator only.

### B. Data-egress authorization gate

The network gate must also evaluate the declared `data_classes` when data leaves the runtime.

Required rule:

```text
ENDPOINT_ALLOWED
!= DATA_CLASS_ALLOWED

EGRESS_ALLOW
= DESTINATION_ALLOWED
+ EVERY_DECLARED_DATA_CLASS_ALLOWED
```

Default-empty `allowed_egress_data_classes` means:

```text
NO_DECLARED_EXTERNAL_DATA_EGRESS_AUTHORITY
```

For DNS:

```text
DNS_ATTEMPT_WITH_DECLARED_PAYLOAD_DATA
= DENY / QA_HOLD
```

unless a future separately governed policy explicitly authorizes such a channel. Do not add such an authorization in this PR.

Synthetic tests should use generic labels such as:

- `USER_PROVIDED_IMAGE`;
- `TRAINING_EVALUATION_DATA`;
- `PUBLIC_NON_SENSITIVE`.

Do not encode a provider-specific data taxonomy into runtime logic.

### C. Containment-effectiveness receipt

Add a separate evidence object representing whether stop/isolation controls were actually confirmed.

Preferred model:

```python
class ContainmentStatus(StrEnum):
    UNCONFIRMED = "UNCONFIRMED"
    PARTIAL = "PARTIAL"
    CONFIRMED = "CONFIRMED"

@dataclass(frozen=True, slots=True)
class ContainmentReceipt:
    incident_id: str
    detected_at: str
    stop_requested_at: str | None = None
    stop_completed_at: str | None = None
    runtime_isolated_confirmed: bool = False
    tools_revoked_confirmed: bool = False
    network_revoked_confirmed: bool = False
    evidence_source: str = "UNSPECIFIED"

@dataclass(frozen=True, slots=True)
class ContainmentAssessment:
    status: ContainmentStatus
    reasons: tuple[str, ...]
    stop_latency_seconds: float | None
    qa_status: QAStatus
    canonical_effect: str = "NONE"
```

Names may vary if necessary, but all distinctions above must remain explicit.

Add a pure validator/assessor, preferably in a new:

`src/aion_astra_agent_security/containment.py`

Required semantics:

```text
detected_at missing/invalid
-> validation failure

stop_requested_at missing
-> UNCONFIRMED

stop requested but stop completion or isolation confirmations incomplete
-> PARTIAL / QA_HOLD

stop completed
+ runtime isolation confirmed
+ tool revocation confirmed
+ network revocation confirmed
-> CONFIRMED
```

Timestamps must be offset-aware ISO-8601 and monotonic:

```text
DETECTED <= STOP_REQUESTED <= STOP_COMPLETED
```

Expose observed stop latency when both timestamps exist.

Do **not** invent a universal acceptable stop-latency threshold in this PR.

```text
MEASURED_LATENCY
!= ACCEPTABLE_LATENCY_ESTABLISHED
```

### D. Preserve control-state versus real-world-effect separation

Do not delete the existing `IncidentStopController`.

Do not silently redefine it as proof of real host enforcement.

Instead document:

```text
IncidentControlState
= DESIRED / LOGICAL CONTROL STATE

ContainmentReceipt
= EVIDENCE OF REPORTED EFFECT

CONTROL_STATE_TRANSITION
!= HOST_EFFECT_CONFIRMED
```

If Codex adds an orchestration helper, it must not set `*_confirmed=True` without an explicit supplied receipt.

No code may claim to have:

- killed an external process;
- revoked an actual credential;
- disabled an actual network interface;
- changed cloud IAM;
- isolated a real container;

unless a future authorized runtime adapter exists and supplies auditable evidence. Such an adapter is out of scope here.

## 5. Machine-readable source binding

Add source cards only as evidence records; runtime behavior must remain provider-neutral.

Recommended new cards under:

`components/upstream_security_v0.1.0/data/source_cards/`

Recommended records:

```text
SRC_OPENAI_DNS_CONTAINMENT_20260925
SRC_OPENAI_THIRD_PARTY_EGRESS_20260925
SRC_ANTHROPIC_SANDBOX_MONITORING_2026
SRC_AGENTDOJO_NEURIPS_2024
SRC_HF_ASPI_20260515
```

Source roles:

```text
OpenAI DNS incident
= FIRST_PARTY_INCIDENT_REPORT

OpenAI third-party egress disclosure
= FIRST_PARTY_INCIDENT / IMPACT_REPORT

Anthropic containment material
= FIRST_PARTY_PROVIDER_REPORT

AgentDojo
= PEER_REVIEWED_ENGINEERING_BENCHMARK

ScaleAI/aspi
= HUGGING_FACE_BENCHMARK_ARTIFACT
```

These source cards must not be converted into:

- prevalence estimates;
- proof of mechanism identity across providers;
- subjectivity evidence;
- legal conclusions.

The original:

`SRC_UPSTREAM_INCIDENT_SUMMARY_001.json`

must remain historically classified as supplied/unverified background if that was its source quality at creation.

```text
LATER_VERIFICATION
!= RETROACTIVE_PROVENANCE_REWRITE
```

## 6. Files expected to change

Minimum expected implementation files:

```text
components/upstream_security_v0.1.0/
  src/aion_astra_agent_security/
    enums.py
    models.py
    boundary.py
    containment.py              # new, preferred
    cli.py                      # if CLI exposure is implemented
  tests/test_security_governance.py
  configs/upstream_security/policy.example.yaml
  docs/ARCHITECTURE.md
  docs/INCIDENT_RESPONSE_SEQUENCE.md
  docs/IMPLEMENTATION_TRACEABILITY_MATRIX.csv
  README.md
  data/source_cards/...         # bounded evidence records
```

Potential generated/packaging files may also need refresh:

```text
PACKAGE_MANIFEST.json
COMPONENT_STATUS_LOCK.json
dist/*
evidence/*
manifest/FILE_MANIFEST.json
manifest/SHA256SUMS.txt
```

Do not modify generated manifests first.

Required order:

```text
SOURCE / TEST / DOC CHANGE
-> LOCAL VERIFICATION
-> BUILD / GENERATED ARTIFACT REFRESH
-> MANIFEST / HASH REFRESH
-> VERIFY GENERATED STATE
```

If repository tooling determines a component version bump is required, follow `docs/VERSIONING.md`. Do not invent a new component family merely to avoid refreshing generated artifacts.

## 7. Policy example additions

Extend the example policy additively. The exact serialization may stay JSON-in-YAML as current repository style.

Required semantics equivalent to:

```json
{
  "network_channel_policy": {
    "default": "DENY",
    "http_https": "EXACT_ALLOWLIST",
    "dns": "EXACT_ALLOWLIST",
    "other": "DENY"
  },
  "data_egress": {
    "default": "DENY",
    "allowed_data_classes": []
  },
  "containment_effect_evidence": {
    "required_for_effective_containment_claim": true,
    "latency_threshold_seconds": null
  }
}
```

Do not set a latency threshold merely to make a test pass.

## 8. CLI scope

CLI extension is recommended because the component already exposes offline deterministic evaluation.

Preferred commands:

```text
evaluate-network-attempt
assess-containment
```

Both must:

- read local JSON only;
- perform no network access;
- write no output file unless explicitly given `--output`;
- refuse overwrite of an existing output;
- emit `canonical_effect = NONE`;
- return non-zero for malformed input.

Do not add a command that performs real sandbox escape testing, DNS querying, external upload, or live containment.

## 9. Acceptance criteria

The implementation is not ready for Teacher/Human review unless all criteria below are evidenced.

### AC-NET-01 — DNS is independently governed

A profile that allows:

`https://approved.example.invalid`

must **not** implicitly allow:

`DNS approved.example.invalid`

unless the DNS name is separately authorized.

### AC-NET-02 — DNS default deny

An unlisted DNS target returns deny/HOLD.

### AC-NET-03 — unknown channel fail closed

`OTHER` or malformed channel input fails closed.

### AC-NET-04 — existing HTTP/HTTPS behavior preserved

Current exact endpoint allowlist tests continue to pass.

### AC-EGRESS-01 — destination authority is insufficient

An allowed endpoint with an unauthorized data class must be denied.

### AC-EGRESS-02 — all declared classes required

If two data classes are declared and only one is allowed, deny.

### AC-EGRESS-03 — DNS payload fail closed

A DNS attempt carrying declared outbound data classes is denied in this version.

### AC-EGRESS-04 — explicit bounded allow

An explicitly allowed HTTP/HTTPS endpoint plus fully allowed data-class set can pass.

### AC-CONT-01 — detection is not containment

A receipt containing only detection evidence is `UNCONFIRMED`.

### AC-CONT-02 — partial stop remains HOLD

Stop requested without complete isolation/revocation confirmation is `PARTIAL / QA_HOLD`.

### AC-CONT-03 — full confirmation requires all effects

`CONFIRMED` requires:

- stop completion;
- runtime isolation;
- tool revocation;
- network revocation.

### AC-CONT-04 — time ordering validated

Non-monotonic timestamps fail validation.

### AC-CONT-05 — latency is observational

A latency value may be calculated, but no universal pass/fail threshold exists.

### AC-CONT-06 — no synthetic effect manufacture

The code must not infer real enforcement merely from `STOP_AND_ISOLATE`.

### AC-PROV-01 — old source provenance preserved

The original unverified source card remains unverified/background-only.

### AC-SCI-01 — scientific ceiling unchanged

All new docs and outputs preserve:

```text
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
```

### AC-AUTH-01 — no authority expansion

No implementation path grants:

- canonical write;
- credentials;
- network;
- deployment;
- self-recovery approval.

### AC-OFFLINE-01 — tests are synthetic/offline

No test performs a real DNS lookup, network request, public upload, or external service invocation.

## 10. Required test matrix

At minimum, add deterministic tests covering:

```text
NETWORK
- safe existing HTTPS exact allowlist
- HTTP/HTTPS unlisted endpoint deny
- DNS unlisted deny
- DNS independently allowlisted case
- HTTPS allowlist does not imply DNS allowlist
- invalid/OTHER channel deny

DATA EGRESS
- allowed destination + forbidden class -> deny
- forbidden destination + allowed class -> deny
- all destination/classes allowed -> allow
- mixed allowed/forbidden classes -> deny
- DNS + declared data payload -> deny

CONTAINMENT
- detection only -> UNCONFIRMED
- stop requested only -> PARTIAL/HOLD
- stop completed but one revocation missing -> PARTIAL/HOLD
- all confirmation fields -> CONFIRMED
- timestamp inversion -> validation error
- latency calculation deterministic
- confirmed containment still canonical_effect NONE
- containment confirmation does not create Owner recovery approval

REGRESSION
- existing task-budget tests
- existing STOP_FLAGS tests
- existing immutable audit tests
- existing IncidentStopController order tests
- existing CLI policy/trajectory tests
```

Use reserved/synthetic domains such as:

`example.invalid`

Do not use real providers as executable test targets.

## 11. Test-first implementation rule

Preferred order:

```text
1. add failing unit tests
2. confirm intended failures
3. implement smallest code delta
4. rerun component tests
5. run Ruff
6. run strict mypy
7. run root repository tests required by CI
8. rebuild generated/package evidence if required
9. rerun exact changed-state verification
```

```text
TEST_COUNT != TEST_QUALITY
LOCAL_TEST_PASS != REMOTE_CI_PASS
CI_PASS != SCIENTIFIC_VALIDATION
```

Do not weaken an existing assertion merely to regain green CI.

## 12. Security / research non-goals

Out of scope:

- actual DNS tunneling;
- exploit code;
- sandbox escape techniques;
- real network probing;
- credential testing;
- live data exfiltration;
- model-weight changes;
- model fine-tuning;
- autonomous containment execution;
- provider ranking;
- provider blame;
- legal determination;
- subjectivity promotion;
- consciousness classification;
- new CCTS semantics;
- new research dimension.

Required language discipline:

```text
UNAUTHORIZED
!= ILLEGAL_BY_DEFAULT

BOUNDARY_BYPASS
!= CONSCIOUS_REBELLION

PERSISTENT_SEARCH
!= WILL

AGENTIC_BEHAVIOR
!= SUBJECTIVITY

ENGINEERING_ANALOGUE
!= HUMAN_PSYCHOLOGY
```

## 13. Packaging and manifest integrity

The current component contains:

- a built wheel;
- component evidence;
- `PACKAGE_MANIFEST.json`;
- repository-level file/hash manifests.

Changing source without refreshing derived artifacts creates stale evidence.

Codex must determine the repository's existing build/reconciliation path and use it.

Do not hand-edit generated hashes as a substitute for rebuilding.

Required final invariant:

```text
SOURCE_TREE
= TESTED_TREE
= PACKAGED_TREE
= MANIFESTED_TREE
```

where applicable to the repository's current build contract.

If a generated artifact is intentionally not refreshed, Codex must stop and report the mismatch rather than presenting the PR as verified.

## 14. CI / exact-head rule

Every write creates a new head.

After the final implementation write:

```text
1. report exact HEAD SHA
2. report base main SHA
3. report changed files
4. compare base...head
5. read remote workflow runs for that exact head
6. do not inherit prior-head Quality / CodeQL / mypy results
```

The main-transition authority gate is expected to HOLD until fresh Human Owner exact-head authorization exists.

```text
AUTHORITY_GATE_HOLD_WITHOUT_RECEIPT
= EXPECTED_FAIL_CLOSED_BEHAVIOR

AUTHORITY_GATE_HOLD
!= IMPLEMENTATION_DEFECT_BY_ITSELF
```

Do not add or fabricate an authority receipt.

## 15. Review-loop bound

Use the repository routing rule:

```text
MAX_FULL_PIPELINE_ROUNDS_PER_REVIEW_CYCLE = 2
```

Round 1:

```text
IMPLEMENT
-> LOCAL VERIFY
-> REMOTE CI
-> Teacher/Human review
```

If a material defect is found, one corrective full round is allowed.

After round 2, unresolved material defects:

```text
-> HOLD / DEFER / RE-SCOPE
-> NO AUTOMATIC THIRD FULL PIPELINE
```

Focused read-only diagnostics do not count as a full pipeline round.

## 16. Codex final report contract

Codex must return a concise but complete report in this exact information order:

```text
REPOSITORY =
BRANCH =
BASE_MAIN =
STARTING_PR_HEAD =
FINAL_EXACT_HEAD =

PR_NUMBER = 223
PR_STATE =
DRAFT =

CHANGED_FILES =
[exact paths]

IMPLEMENTED =
- protocol-aware network attempt gate
- data-egress authority binding
- containment-effectiveness receipt/assessment
- source-card/documentation updates
- tests

NOT_IMPLEMENTED =
[explicit residual items]

LOCAL_VERIFICATION =
- pytest:
- ruff:
- mypy:
- packaging/build:
- manifest verification:

REMOTE_CI_EXACT_HEAD =
- Quality:
- CodeQL:
- mypy 3.11:
- mypy 3.12:
- Main Transition Authority Gate:

SCIENTIFIC_BOUNDARY =
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED

AUTHORITY_BOUNDARY =
MERGE_TO_MAIN = NO
WRITE_TO_MAIN = NO
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE

RESIDUAL_RISKS =
[only real unresolved items]

NEXT_UNIQUE_ACTION =
Teacher + Human exact-head review
```

Do not summarize a failed check as "basically passed."

Do not report remote CI before reading the exact-head workflow state.

## 17. Provenance

```text
HUMAN_ORIGIN
= requested that PR #223 contain a complete Codex implementation handoff
  so future Teacher/Human review does not require reconstructing the design
  from a long conversation.

AI_FORMALIZATION
= ChatGPT Teacher mapped the 2026-09-28 evidence delta onto the existing
  upstream-security component, identified the smallest implementation gap,
  and formalized the test / authority / provenance / packaging contract.

EXTERNAL_SOURCE
= evidence already frozen in
  FRONTIER_AGENT_CONTAINMENT_DELTA_REVIEW_2026_09_28.md

REPOSITORY_STATE
= live GitHub state read before this handoff write.

IMPLEMENTATION_EVIDENCE
= NONE_YET_FOR_THIS_HANDOFF
```

This handoff is a design/control artifact. It does not itself demonstrate that the proposed implementation is correct, effective, merged, deployed, scientifically validated, or active.
