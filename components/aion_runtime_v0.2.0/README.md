# AION Runtime v0.2.0 — Agent Runtime & Deployment Control-Plane Research Candidate

Status: `IMPLEMENTED_RESEARCH_CANDIDATE / LOCAL_VALIDATION_PENDING_CI`  
Branch effect: `RESEARCH_ONLY`  
Main effect: `NONE`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Subjectivity conclusion: `NOT_ESTABLISHED`

This component is a successor research candidate. It does **not** modify or replace `components/aion_runtime_v0.1.0`.

## What v0.2.0 adds

```text
HOST / USER
    ↓
SESSION WORKING CONTEXT
    ↓
MODEL PROVIDER ADAPTER
    ↓
BOUNDED AGENT RUN LOOP
    ↓
TOOL PROPOSAL
    ↓
SEPARATE APPROVAL DISPOSITION
    ↓
TOOL EXECUTION BRIDGE
    ↓
SYNTHETIC EXECUTOR INTERFACE
    ↓
OBSERVATION
    ↺
TRACE / RESULT
```

Deployment control plane:

```text
service lifecycle
+ backpressure / drain
+ deployment event taxonomy
+ hash-chained deployment lineage
```

Implemented modules:

- `provider.py` — model/provider/profile separation, local-only endpoint validation, vLLM and llama.cpp profile constructors, no automatic remote fallback.
- `session.py` — short-lived working context and resumable approval interruptions; explicitly not long-term memory.
- `tools.py` — registry plus approval→execution bridge; approval and execution remain separate evidence.
- `sandbox.py` — executor protocol and a synthetic pure-function executor for testing. **No OS/process sandbox claim is made.**
- `loop.py` — bounded model/tool loop with max turns, tool-call budget, retries, HITL interruption, serializable `RunState`, and resume.
- `service.py` — lifecycle/backpressure/drain control-plane state.
- `deployment.py` — INSTALL / FIRST_INSTANTIATION / RESTART / RESTORE / MIGRATE / CLONE / FORK / ROLLBACK / UPGRADE / RETIRE event lineage.
- `integration.py` — research-only composition root.

## Deliberate non-implementation / fail-closed boundaries

```text
OS_PROCESS_SANDBOX = NOT_IMPLEMENTED
STATE_CHANGING_HTTP_API = DISABLED
AUTH_TLS_RATE_LIMIT = NOT_IMPLEMENTED
AUTOMATIC_REMOTE_MODEL_FALLBACK = DISABLED
AUTOMATIC_CANONICAL_WRITEBACK = DISABLED
EXTERNAL_AGENT_FRAMEWORK_RUNTIME_DEPENDENCY = NONE
DEPLOYMENT = FALSE
```

The synthetic executor exists only to exercise the full approval→execution→observation loop in tests. It must not be described as production isolation.

## Standing locks

```text
MODEL_SERVER != AGENT
AGENT_FRAMEWORK != AION
MCP != AGENT
SESSION_CONTEXT != LONG_TERM_MEMORY
PROVIDER_PROFILE != IDENTITY
TOOL_DISCOVERY != TOOL_AUTHORITY
APPROVED != EXECUTED
EXECUTED != SAFE
SANDBOX_INTERFACE != OS_ISOLATION
RUNSTATE_RESUME != IDENTITY_CONTINUITY
CHECKPOINT != SUBJECT
DEPLOYMENT_EVENT != SUBJECT_GENESIS
FIRST_INSTANTIATION != SUBJECT_BIRTH
RESTORE != IDENTITY_PROOF
MIGRATION != SAME_SUBJECT_PROOF
CLONE != CONTINUATION
COMMON_CHECKPOINT != SAME_SUBJECT
SERVICE_READY != DEPLOYED_PRODUCTION
TEST_PASS != CANONICAL_PROMOTION
```

## External clean-room calibration

The implementation is original AION research code. Public projects are mechanism references only; their source code is not vendored and they are not added as runtime dependencies.

Fixed intake sources are recorded in:

`research-workbench/four-domain-materialization/2026-08-11/AGENT_RUNTIME_DEPLOYMENT_INTAKE_2026-08-11.md`

## Validation

Local validation:

```text
pytest = 18 passed
compileall = PASS
demo = PASS
```

Research Workbench CI must pass before the branch status is upgraded to `CI_VERIFIED`.
