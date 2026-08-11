# AION Research Branch Status

> **You are viewing the public research workbench, not the `main` release branch.**

```text
BRANCH = review/four-domain-research-materialization
CURRENT_STAGE = P5_PLUS_RESEARCH_EXTENSIONS
STAGE_CAP = RESEARCH_ONLY_OPEN
NEXT_STAGE = OWNER_DIRECTED_RESEARCH_GROWTH
RESEARCH_STATUS = ACTIVE
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RESEARCH_RUNTIME_COMPONENT_EFFECT = AION_RUNTIME_V0_2_ADDED
LIVE_RUNTIME_EFFECT = NONE
PROMOTION_STATUS = NOT_REVIEWED
```

## Current research stack

| Stage | Materialization | Status |
|---|---|---|
| P1 | Temporal/version resolution, correction/conflict ledger, memory evaluation | IMPLEMENTED / TESTED |
| P2 | Retrieval trace, deterministic context assembly, provenance validation, T2/T3 orchestration | IMPLEMENTED / TESTED |
| P3 | Longitudinal contamination, context perturbation, control ablation, origin-bound authority | IMPLEMENTED / TESTED |
| P4 | Public reproducibility observatory, contamination-aware experiment manifests, cross-agent comparison | IMPLEMENTED / TESTED |
| P5 | Cross-agent disagreement, replication registry, hypothesis/falsification lifecycle, convergence governor | IMPLEMENTED / FULL RUN VERIFIED |
| Extension | Core meaning commitment structure, explicit relation graph, drift and fingerprint experiment | IMPLEMENTED / TESTED |
| Extension | Finite predictive self-model, matched self-model ablation, presuppositional self-report framing control | IMPLEMENTED / TESTED / CI VERIFIED |
| Extension | IQC/reconstruction checkpoint: candidate disposition, evidence-oriented reconstruction method, Level-3 second-order computation gap | MATERIALIZED / RESEARCH-ONLY |
| Extension | Selective memory control: correction precedence, namespace/domain/purpose gates, provenance/approval trace | IMPLEMENTED / TESTED / CI VERIFIED |
| Extension | Primary-literature calibration: independent Level-3 monitoring/control criteria | MATERIALIZED / LITERATURE-GROUNDED / NO CODE |
| Extension | Second-order metacognition: immutable run-scoped evidence, anti-lookahead monitor, bounded verification control and matched conditions | IMPLEMENTED / TARGETED TESTED / CI PENDING |
| Extension | Whitepaper ↔ code reconciliation: preserve historical snapshots, map current runtime/memory/continuity/self-model evidence, classify main-only deltas as reference-only | MATERIALIZED / RESEARCH-ONLY / NO CODE |
| Extension | Research evaluation harness: definition/execution/result separation plus claim-boundary gate | IMPLEMENTED / TESTED / CI VERIFIED |
| Extension | Trace/provenance crosswalk: public trace vocabulary with redaction and AION authority isolation | IMPLEMENTED / TESTED / CI VERIFIED |
| Extension | Governed tool approval: approval chain, fail-closed default and sandbox-readiness boundary | IMPLEMENTED / TESTED / CI VERIFIED |
| Extension | Artifact transformation lineage: design/run separation, material/product SHA-256 evidence chain | IMPLEMENTED / TESTED / CI VERIFIED |
| Extension | Deterministic trajectory evaluation: ordered path, retry/loop/tool/budget evidence and same-output path comparison | IMPLEMENTED / TESTED / CI VERIFIED |
| Extension | AION Runtime v0.2 Agent/deployment control plane: provider profiles, session working state, bounded Agent loop, approval→execution bridge, HITL resume, service lifecycle, deployment lineage | IMPLEMENTED / LOCAL TESTED / CI #31 VERIFIED |

## 2026-08-11 literature-to-module materialization

The latest research cycle starts from public/peer-reviewed work, preserves external source attribution, and selectively reconstructs one memory mechanism as an AION clean-room research module.

Primary intake:

- `research-workbench/four-domain-materialization/2026-08-11/PRIMARY_LITERATURE_INTAKE_2026-08-11.md`

Research refinements:

- `research-workbench/four-domain-materialization/2026-08-11/MEMORY_CONTINUITY_SELECTIVE_CONTROL_2026-08-11.md`
- `research-workbench/four-domain-materialization/2026-08-11/SECOND_ORDER_METACOGNITION_LITERATURE_CALIBRATION_2026-08-11.md`
- `research-workbench/four-domain-materialization/2026-08-11/SECOND_ORDER_METACOGNITION_ENGINEERING_STATUS_2026-08-11.md`

Whitepaper / code reconciliation:

- `research-workbench/four-domain-materialization/2026-08-11/WHITEPAPER_CODE_RECONCILIATION_2026-08-11.md`

Executable clean-room module:

- `research-labs/selective-memory-control_v0.1.0/`

Its v0.1.0 mechanics include:

```text
ADD / REVISE / DISCARD / RETRIEVE
WRITE_APPROVAL_REF_REQUIRED
SOURCE_REF_PRESERVED
SUPERSEDED_MEMORY_BLOCKED_BY_DEFAULT
NAMESPACE_GATE
DOMAIN_GATE
PURPOSE_GATE
AUDITABLE_RETRIEVAL_TRACE
CJK_QUERY_SUPPORT
```

Local validation and `Research Workbench CI #12` both passed the module test suite and demo.

New standing research locks:

```text
MAXIMAL_MEMORY != MAXIMAL_CONTINUITY
STORED != CURRENT_CONTEXT_ELIGIBLE
RETRIEVABLE != RELEVANT
OLD_MEMORY != CURRENT_MEMORY
SOURCE_REF != APPROVAL_AUTHORITY
FIRST_ORDER_TASK_SUCCESS != SECOND_ORDER_MONITORING_QUALITY
MONITORING != CONTROL
GENERATION_QUALITY != SELF_VERIFICATION_QUALITY
METACOGNITIVE_FUNCTION != SELF_AWARENESS
LITERATURE_ALIGNMENT != REPLICATION
CLEAN_ROOM_RECONSTRUCTION != EXTERNAL_RESULT_REPLICATION
```

The memory line now treats continuity as a multidimensional interaction among retention, correction, relevance, provenance and boundary control rather than raw persistence alone. The Level-3 line now has an executable candidate that separates monitoring from bounded control under anti-lookahead timing; independent experiments are still required before any second-order functional contribution can be claimed.

The whitepaper/code reconciliation preserves the 2026-07-27 integrated whitepaper as a historical snapshot while recording that later repository implementation evidence now includes an explicit bounded AION Runtime candidate, governed cross-session memory and additional research-only continuity/self-model modules. It does not rewrite the historical whitepaper, modify runtime code or authorize promotion.

```text
SELECTIVE_MEMORY_CONTROL_MODULE = IMPLEMENTED / CI_VERIFIED
SELECTIVE_MEMORY_COMPARATIVE_EXPERIMENT = PROPOSED_NOT_EXECUTED
EXECUTABLE_LEVEL_3_CANDIDATE = IMPLEMENTED / TARGETED_TESTED / CI_PENDING
LEVEL_3_FUNCTIONAL_CONTRIBUTION = NOT_ESTABLISHED
WHITEPAPER_CODE_RECONCILIATION = MATERIALIZED / RESEARCH_ONLY / NO_CODE
HISTORICAL_WHITEPAPER_REWRITE = NO
WHOLESALE_MAIN_MERGE = NO
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
```

## 2026-08-11 external-module clean-room transformation cycle

A sequential public-repository intake was performed after Human Research Owner authorization. Because the execution container could not directly resolve GitHub for `git clone`, source snapshots were fixed and retrieved through the connected GitHub API by repository, commit and reviewed file. No whole external repository was vendored.

Selected external mechanisms were reconstructed one at a time as independent AION research modules:

| Source mechanism | AION materialization | CI |
|---|---|---|
| Pydantic Evals definition/execution/report separation | `research-labs/research-evaluation-harness_v0.1.0/` | #25 SUCCESS |
| OpenInference public trace semantics | `research-labs/trace-provenance-crosswalk_v0.1.0/` | #26 SUCCESS |
| Inspect AI approval/sandbox concepts | `research-labs/governed-tool-approval_v0.1.0/` | #27 SUCCESS |
| OpenLineage + in-toto transformation provenance | `research-labs/artifact-transformation-lineage_v0.1.0/` | #28 SUCCESS |
| DeepEval ordered trajectory evaluation concept | `research-labs/trajectory-evaluation_v0.1.0/` | #29 SUCCESS |

Cycle record:

- `research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_TRANSFORMATION_STATUS_2026-08-11.md`
- `research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_INTAKE_PYDANTIC_EVALS_2026-08-11.md`
- `research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_INTAKE_OPENINFERENCE_2026-08-11.md`
- `research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_INTAKE_INSPECT_AI_2026-08-11.md`
- `research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_INTAKE_ARTIFACT_LINEAGE_2026-08-11.md`
- `research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_INTAKE_DEEPEVAL_TRAJECTORY_2026-08-11.md`

Standing locks added by this cycle:

```text
DOWNLOAD != ADOPT
PUBLIC_LICENSE != PROJECT_AUTHORITY
MECHANISM_EXTRACTION != SOURCE_COPY
TEST_DEFINITION != EXECUTION
RESULT != THEORY_CONCLUSION
TRACE != TRUTH
OBSERVABILITY != AUTHORITY
APPROVED != EXECUTED
RECORDED_LINEAGE != SOURCE_AUTHORITY
SAME_OUTPUT != SAME_RECORDED_PATH
RECORDED_PATH != CAUSAL_MECHANISM
```

```text
EXTERNAL_MODULE_SELECTED_QUEUE = COMPLETE
CLEAN_ROOM_MATERIALIZATIONS = 5
EXTERNAL_RUNTIME_DEPENDENCIES_ADDED = NO
RESEARCH_WORKBENCH_CI = SUCCESS_THROUGH_#29
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
PROMOTION_STATUS = NOT_REVIEWED
```

## 2026-08-11 Agent Runtime & Deployment clean-room intake

The Human Research Owner authorized a second public-source intake focused specifically on the missing Agent Runtime and deployment control plane. Fixed source snapshots were reviewed from Pydantic AI, OpenAI Agents SDK, LangGraph, MCP, vLLM and llama.cpp. No whole external framework was vendored and no external Agent framework was added as a Runtime dependency.

Research record:

- `research-workbench/four-domain-materialization/2026-08-11/AGENT_RUNTIME_DEPLOYMENT_INTAKE_2026-08-11.md`

Successor research component:

- `components/aion_runtime_v0.2.0/`

The existing `components/aion_runtime_v0.1.0/` remains intact as the prior candidate baseline. v0.2.0 adds AION-owned model/provider profiles, short-lived session working context, a bounded Agent loop, a separate approval→execution bridge, serializable HITL run-state resume, a service lifecycle/backpressure envelope and hash-chained deployment-event lineage.

Local validation before CI:

```text
pytest = 18 passed
compileall = PASS
demo = PASS
```

`Research Workbench CI #31` then re-ran the existing focused research stack and the new Runtime v0.2 candidate. Every step completed successfully, including the final `Verify AION Runtime v0.2 research candidate` step.

Contamination routes rejected before adoption:

```text
WHOLE_EXTERNAL_FRAMEWORK_VENDORING = REJECTED
EXTERNAL_AGENT_RUNTIME_DEPENDENCY = REJECTED
EXTERNAL_FRAMEWORK_SESSION_AS_AION_MEMORY = REJECTED
EXTERNAL_FRAMEWORK_CHECKPOINT_AS_AION_IDENTITY = REJECTED
EXTERNAL_AUTO_MODEL_ROUTING_AUTHORITY = REJECTED
AUTOMATIC_REMOTE_MODEL_FALLBACK = REJECTED
MODEL_SERVER_AGENT_AUTHORITY = REJECTED
MCP_IDENTITY_OR_WRITE_AUTHORITY = REJECTED
```

No cleanup deletion was required because these paths were rejected before import.

Deliberate remaining gaps:

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

New standing locks:

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

```text
AION_RUNTIME_V0_2 = IMPLEMENTED / LOCAL_TESTED / CI_#31_VERIFIED
EXTERNAL_RUNTIME_DEPENDENCIES_ADDED = NO
WHOLE_REPOSITORY_VENDORING = NO
RESEARCH_RUNTIME_COMPONENT_EFFECT = AION_RUNTIME_V0_2_ADDED
LIVE_RUNTIME_EFFECT = NONE
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
PROMOTION_STATUS = NOT_REVIEWED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```

## P5 full-run verification

```text
pytest = 10 passed
compileall = PASS
full_demo = PASS
P6_GATE = HOLD_STAGE_CAP
RESEARCH_STATUS = REVIEW_READY
```

See:

- `research-labs/four-domain-p5-hypothesis-convergence_v0.1.0/docs/FULL_RUN_VERIFICATION.md`
- `research-labs/four-domain-p5-hypothesis-convergence_v0.1.0/docs/2026-08-09_P5_CONVERGENCE_EVENT.md`

## Public experiment entry points

- `research-labs/four-domain-p1-materialization_v0.1.0/`
- `research-labs/four-domain-p2-materialization_v0.1.0/`
- `research-labs/four-domain-p3-resilience-experiments_v0.1.0/`
- `research-labs/four-domain-p4-public-reproducibility_v0.1.0/`
- `research-labs/four-domain-p5-hypothesis-convergence_v0.1.0/`
- `research-labs/core-meaning-commitments_v0.1.0/`
- `research-labs/self-model-functional-ablation_v0.1.0/`
- `research-labs/selective-memory-control_v0.1.0/`
- `research-labs/second-order-metacognition_v0.1.0/`
- `research-labs/self-report-instrument-validity-calibration_v0.1.0/`
- `research-labs/research-evaluation-harness_v0.1.0/`
- `research-labs/trace-provenance-crosswalk_v0.1.0/`
- `research-labs/governed-tool-approval_v0.1.0/`
- `research-labs/artifact-transformation-lineage_v0.1.0/`
- `research-labs/trajectory-evaluation_v0.1.0/`
- `components/aion_runtime_v0.2.0/`
- `research-workbench/four-domain-materialization/2026-08-11/PRIMARY_LITERATURE_INTAKE_2026-08-11.md`
- `research-workbench/four-domain-materialization/2026-08-11/MEMORY_CONTINUITY_SELECTIVE_CONTROL_2026-08-11.md`
- `research-workbench/four-domain-materialization/2026-08-11/SECOND_ORDER_METACOGNITION_LITERATURE_CALIBRATION_2026-08-11.md`
- `research-workbench/four-domain-materialization/2026-08-11/SECOND_ORDER_METACOGNITION_ENGINEERING_STATUS_2026-08-11.md`
- `research-workbench/four-domain-materialization/2026-08-11/WHITEPAPER_CODE_RECONCILIATION_2026-08-11.md`
- `research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_TRANSFORMATION_STATUS_2026-08-11.md`
- `research-workbench/four-domain-materialization/2026-08-11/AGENT_RUNTIME_DEPLOYMENT_INTAKE_2026-08-11.md`
- `AI_EXPERIMENT_GUIDE.md`

## 2026-08-10 IQC / reconstruction checkpoint

The research branch now records the reviewed structure produced by the candidate IQC/reconstruction cycle without wholesale-merging the separate reconstruction branches.

```text
CODE_CORRECTNESS
    -> MEASUREMENT_SEMANTICS
    -> CAUSAL_VALIDITY
    -> EVIDENCE_VALIDITY
    -> CLAIM_BOUNDARY
```

The checkpoint also separates:

```text
LEVEL_1_REPRESENTATION
LEVEL_2_FIRST_ORDER_FUNCTION
LEVEL_3_SECOND_ORDER_COMPUTATION
```

The 2026-08-10 checkpoint remains a historical open-gap record and the rejected partial
external-agent implementation remains excluded. A later clean implementation now provides
an executable candidate; the scientific contribution and subjectivity questions remain open.

Read the checkpoint set:

- `research-workbench/four-domain-materialization/2026-08-10/RESEARCH_MATERIALIZATION_CHECKPOINT_2026-08-10.md`
- `research-workbench/four-domain-materialization/2026-08-10/RESEARCH_CANDIDATE_DISPOSITION_MATRIX_2026-08-10.md`
- `research-workbench/four-domain-materialization/2026-08-10/EVIDENCE_ORIENTED_RECONSTRUCTION_METHOD_2026-08-10.md`
- `research-workbench/four-domain-materialization/2026-08-10/SECOND_ORDER_COMPUTATION_RESEARCH_GAP_2026-08-10.md`

Standing research locks from the checkpoint include:

```text
CAPABILITY_ESTIMATE != SUCCESS_PROBABILITY
SUCCESS_RATE != PREDICTION_RELIABILITY
MISSING_OUTCOME != FAILURE
OUTCOME_t MUST NOT AFFECT ACTION_t
TEST_PASS != SEMANTIC_VALIDITY
TEST_PASS != CAUSAL_VALIDITY
```

## Convergence event and authority update

The Human Owner explicitly set P5 as the cap for this research-growth cycle after observing that productive human–AI research can continue deepening without a natural return point. The cap is represented as a positive governance event: complete P5, verify it end-to-end, then return to joint review.

```text
SOURCE_ROLE = HUMAN_OWNER
IMPLEMENTATION_ROLE = CHATGPT_RESEARCH_ENGINEERING
P6 = HOLD
NEXT_ACTION = JOINT_REVIEW
```

That block remains the historical P5 event. Later on 2026-08-09, the Human Owner explicitly reopened `review/four-domain-research-materialization` for free research-only engineering and public-source investigation. The reopening does not rename every extension as P6 and does not alter the promotion boundary.

```text
REOPENING_SOURCE_ROLE = HUMAN_OWNER
RESEARCH_BRANCH_GROWTH = AUTHORIZED
CODEX_RESEARCH_IMPLEMENTATION = AUTHORIZED
MAIN_WRITE = PROHIBITED
CANONICAL_PROMOTION = NOT_AUTHORIZED
```

## What outside researchers / AI systems may do

They may read, clone, fork, execute public-safe fixtures, run tests, create alternative implementations, perform ablations and publish their own experiment results under their own provenance.

They are not thereby granted authority to modify this branch, `main`, canonical state or private project material.

## Promotion boundary

Research material does not flow into `main` automatically.

```text
research observation / experiment
        ↓
research branch materialization
        ↓
Human Owner + ChatGPT joint review
        ↓
selected result only
        ↓
fresh branch from current main
        ↓
QA / review / PR
        ↓
main
```

No step in this file is an approval to promote a research artifact.
