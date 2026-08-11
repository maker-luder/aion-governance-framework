# Agent Runtime & Deployment Clean-room Intake — 2026-08-11

Status: `RESEARCH_ONLY / CLEAN_ROOM_MATERIALIZATION_ACTIVE`  
Branch: `review/four-domain-research-materialization`  
Main effect: `NONE`  
Canonical effect: `NONE`  
Deployment: `FALSE`

## Authority and scope

```text
SOURCE_ROLE = HUMAN_OWNER
RESEARCH_BRANCH_GROWTH = AUTHORIZED
AGENT_RUNTIME_DEPLOYMENT_INTAKE = AUTHORIZED
CLEAN_ROOM_TRANSFORMATION = AUTHORIZED
MAIN_WRITE = PROHIBITED
CANONICAL_PROMOTION = NOT_AUTHORIZED
```

The Human Research Owner authorized a bounded public-source intake for missing Agent Runtime and deployment mechanisms, including removal/rejection of mechanisms that would contaminate AION's existing memory, identity, governance, provenance, or authority boundaries.

Source snapshots were fixed through the connected GitHub API. No whole external repository was vendored. No external Agent framework was added as a Runtime dependency.

```text
DOWNLOAD != ADOPT
PUBLIC_LICENSE != PROJECT_AUTHORITY
MECHANISM_EXTRACTION != SOURCE_COPY
EXTERNAL_FRAMEWORK_STATE != AION_STATE
EXTERNAL_FRAMEWORK_IDENTITY != AION_IDENTITY
```

## Fixed public-source snapshots

| Source | Fixed commit | License reviewed | Reviewed surface / purpose |
|---|---|---|---|
| `pydantic/pydantic-ai` | `d995cfee9fa4243e3a6f5d8e6762b841f7fde839` | MIT | `toolsets/abstract.py` blob `d4e9bfb5cfe48fadf62391385e46369105816584`; `providers/__init__.py` blob `a3cb1e1e6c3467cad08e3725fb0d4436afbac1a0`; tool listing/validation/call separation and provider/profile boundary |
| `openai/openai-agents-python` | `863b96cfe99b5388910ff5b8cd85329003330132` | MIT | `src/agents/run_state.py` blob `adc44c3228def32003336001997eecdf2fd88e09`; run-loop / serializable HITL pause-resume semantics |
| `langchain-ai/langgraph` | `d56666f7fbf0d380ad84cdf0cbe5aa48ab0cc086` | MIT | `libs/checkpoint/langgraph/checkpoint/base/__init__.py` blob `6e42061190d539c20c4358771824837e8598da6c`; `libs/langgraph/langgraph/types.py` blob `ac9aa9b00565ec20476b4d00a3847f6b7e8fda34`; checkpoint/thread and interrupt semantics |
| `modelcontextprotocol/modelcontextprotocol` | `b25c0874bf0ba699a58e21ef06f659d839659de3` | licensing transition: Apache-2.0 / retained MIT contributions; documentation rules separate | protocol semantics only; MCP remains a context/tool/resource transport boundary, not Agent authority |
| `vllm-project/vllm` | `be2e274ef504a09a622a4ea3bf7603b9a41b866f` | Apache-2.0 | `docs/serving/online_serving/openai_compatible_server.md` blob `dfb78245b4461d3474ef50e684c980230e82331f`; OpenAI-compatible local inference endpoint / tool-capable profile |
| `ggml-org/llama.cpp` | `153d324bcf86d220b235ca010eeb11213f32b5d1` | MIT | `tools/server/README.md`; `tools/server/README-dev.md` blob `613017acff66df6e4fcb80876385f3cf078ae1e7`; portable inference profile and explicit server-side Agent-loop separation |

The MCP source is treated especially conservatively because the project is in a licensing transition. Only abstract protocol boundaries are retained; specification/source text is not copied into the AION implementation.

## Mechanism transformation matrix

| External mechanism | AION clean-room transformation | Authority boundary |
|---|---|---|
| Provider/model/profile separation | `provider.py`: `EndpointProfile`, capability declaration, `ProviderRegistry` | provider selection does not establish identity or authority |
| Toolset list/validate/call lifecycle | `tools.py`: AION-owned `ToolRegistry` and separate execution bridge | tool discovery does not grant execution permission |
| Agent run loop | `loop.py`: bounded model → tool → observation → model loop | max turns/tool calls/retries; no framework runtime dependency |
| Serializable HITL run state | `RunState` + explicit pending approval + resume | resuming execution state does not establish identity continuity |
| Checkpoint/thread/interrupt semantics | bounded execution-state inspiration only | external thread/checkpoint IDs never become AION identity/canonical authority |
| MCP transport concepts | future adapter boundary only | `MCP != AGENT`; MCP cannot own AION state |
| vLLM OpenAI-compatible serving | local standard inference profile | model server remains below Agent Runtime |
| llama.cpp server | local portable inference profile | server-side Agent loop deliberately remains outside model server |
| Deployment lifecycle | AION-owned deployment ledger | deployment event classification does not prove subject genesis/continuity |

## Implemented research candidate

New successor component:

`components/aion_runtime_v0.2.0/`

The existing `components/aion_runtime_v0.1.0/` is preserved unchanged as the prior candidate baseline.

v0.2.0 currently materializes:

```text
SESSION_WORKING_CONTEXT
MODEL_PROVIDER_ADAPTER
BOUNDED_AGENT_RUN_LOOP
TOOL_REGISTRY
SEPARATE_APPROVAL_DISPOSITION_INPUT
TOOL_EXECUTION_BRIDGE
SYNTHETIC_EXECUTOR_INTERFACE
HITL_INTERRUPT_RESUME
SERVICE_LIFECYCLE_AND_BACKPRESSURE
DEPLOYMENT_EVENT_TAXONOMY
HASH_CHAINED_DEPLOYMENT_LINEAGE
```

Local validation before CI integration:

```text
pytest = 18 passed
compileall = PASS
demo = PASS
```

## Contamination rejection / removal gate

The following candidate imports were rejected before adoption, so no cleanup deletion was required:

```text
WHOLE_EXTERNAL_FRAMEWORK_VENDORING = REJECTED
EXTERNAL_AGENT_RUNTIME_DEPENDENCY = REJECTED
EXTERNAL_FRAMEWORK_SESSION_AS_AION_MEMORY = REJECTED
EXTERNAL_FRAMEWORK_CHECKPOINT_AS_AION_IDENTITY = REJECTED
EXTERNAL_FRAMEWORK_IDENTITY_NAMESPACE = REJECTED
EXTERNAL_AUTO_MODEL_ROUTING_AUTHORITY = REJECTED
AUTOMATIC_REMOTE_MODEL_FALLBACK = REJECTED
MODEL_SERVER_AGENT_AUTHORITY = REJECTED
MCP_IDENTITY_OR_WRITE_AUTHORITY = REJECTED
```

This is contamination prevention, not a claim that external frameworks are unsafe in general. The rejection is architectural: those concerns already belong to AION-owned governance/state layers.

## Current deliberate gaps after v0.2.0

```text
REAL_OS_PROCESS_SANDBOX = NOT_IMPLEMENTED
REAL_PROVIDER_HTTP_TRANSPORT = NOT_IMPLEMENTED
STATE_CHANGING_HTTP_API = DISABLED
AUTHENTICATION = NOT_IMPLEMENTED_FOR_V0_2_NETWORK_SURFACE
TLS_TERMINATION = NOT_IMPLEMENTED
RATE_LIMITING = NOT_IMPLEMENTED
PERSISTENT_SERVICE_SUPERVISOR = NOT_IMPLEMENTED
WINDOWS_BOOTSTRAP_V0_2 = NOT_IMPLEMENTED
MODEL_WEIGHT_DEPLOYMENT = NOT_EXECUTED
LIVE_VLLM_INTEGRATION = NOT_EXECUTED
LIVE_LLAMA_CPP_INTEGRATION = NOT_EXECUTED
FORMAL_DEPLOYMENT_RUN = NOT_EXECUTED
INDEPENDENT_IVV = NOT_ACHIEVED
```

The current executor is a synthetic pure-function test backend. It is explicitly not an OS/process isolation claim. A real sandbox backend must remain a separate reviewed implementation step.

The current provider interface and local profiles are contracts; no live model server is silently started, downloaded, or called by this research commit.

Long-term governed memory is not duplicated. v0.2.0 keeps short-lived session state separate and leaves long-term memory integration behind an explicit projection boundary.

## Research locks

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

## Current disposition

```text
AION_RUNTIME_V0_2 = IMPLEMENTED_RESEARCH_CANDIDATE
LOCAL_VALIDATION = PASS
RESEARCH_WORKBENCH_CI = PENDING
EXTERNAL_RUNTIME_DEPENDENCIES_ADDED = NO
WHOLE_REPOSITORY_VENDORING = NO
LIVE_RUNTIME_EFFECT = NONE
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
PROMOTION_STATUS = NOT_REVIEWED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```
