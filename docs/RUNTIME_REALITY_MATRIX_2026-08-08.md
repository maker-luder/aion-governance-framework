# Runtime Reality Matrix — 2026-08-08

## Status and provenance

- `STATUS = ANALYSIS_CANDIDATE`
- `CANONICAL_EFFECT = NONE`
- `RUNTIME_EFFECT = NONE`
- `CODE_BEHAVIOR_CHANGE = NONE`
- `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`
- `OWNER_REVIEW = PENDING`

Attribution for this artifact:

- `PROPOSED_BY = CHATGPT`
  - The Runtime Reality Matrix method was proposed by ChatGPT during the Runtime/Twin alignment discussion.
- `AUTHORIZED_TO_PROCEED_BY = HUMAN_OWNER`
  - The Human Owner reviewed the proposed process and explicitly asked ChatGPT to proceed with the item-by-item inspection.
- `IMPLEMENTED_BY = CHATGPT`
  - ChatGPT performed the repository inspection and authored this matrix.
- `REVIEWED_BY = HUMAN_OWNER / PENDING`
- `APPROVED_BY = HUMAN_OWNER / PENDING`
- `CODEX_CONTRIBUTION_THIS_CHANGE = NONE`

This artifact records observed repository reality. It does not promote, rename or refactor any component.

## Interpretation rule

The matrix separates four different questions:

1. Does code or a data model exist?
2. What responsibility does the code actually perform?
3. Is that responsibility bound to AION, Astra, or shared project infrastructure?
4. Has it been promoted to an Owner-approved canonical individual Runtime?

`CODE_EXISTS != INDIVIDUAL_RUNTIME_COMPLETE != CANONICAL_RUNTIME`

## Matrix

| Capability / artifact | Observed responsibility | State domain | Implementation reality | Validation evidence | Current classification |
|---|---|---|---|---|---|
| Governance Kernel v0.4.0 | structured request validation, action-risk policy, fail-closed control, audit | shared project infrastructure | implemented candidate | component test/QA history exists; no new validation performed in this analysis | `SHARED_GOVERNANCE_CANDIDATE` |
| Astra Engineering Workbench v1.0.0 | candidate workspace, approval enforcement, baseline protection, audit, rollback/review packaging | engineering infrastructure; not Astra individual identity | implemented candidate | component reports `PASS_PENDING_OWNER_REVIEW` | `ENGINEERING_CONTROL_PLANE`, not Astra individual Runtime |
| Language Core G1 v0.2.1 | planning/research proposals and optional local planner interface | capability artifact / research infrastructure | research candidate | QA HOLD; Runtime authority explicitly not granted | not an individual Runtime |
| Executable Runtime v0.1.0 | bounded task loop: approval -> governance -> workspace -> planner -> tools -> evidence -> stop | shared/unbound execution capability by observed fields | implemented | implementation report: 12 tests, 92% branch coverage, mypy strict PASS, compile/build/cold-install evidence | `BOUNDED_GOVERNED_EXECUTION_ENGINE_CANDIDATE` |
| `class AstraRuntime` | executes the bounded loop above | **not agent-bound in TaskSpec/RunResult/audit** | implemented | E2E, kill switch, budget and policy tests exist | name currently overstates Astra-individual responsibility; `SEMANTIC_REVIEW_REQUIRED` |
| AION Runtime v0.1.0 | composes persistent recall/memory with the bounded execution engine; CLI/status/read-only HTTP | intended AION composition root | implemented candidate | runtime memory/status tests and server tests exist | `AION_RUNTIME_IMPLEMENTATION_CANDIDATE` |
| AION Runtime execution binding | `run_task()` delegates TaskSpec directly to `AstraRuntime` | no AION agent/runtime-instance binding in execution records | code exists but individual binding absent | current tests validate execution mechanics, not AION-vs-Astra execution ownership | `PARTIAL / GAP` |
| Persistent SQLite memory store | persistent cross-session records, explicit write approval, identity/access/provenance/conflict/relevance gates | technically multi-agent/shared infrastructure because caller supplies `agent_id` | implemented post-RC | persistence and Recall Gate tests exist | `GOVERNED_MULTI_AGENT_MEMORY_INFRASTRUCTURE_CANDIDATE` |
| AION Runtime memory binding | AION CLI/runtime accepts caller-supplied `agent_id` and namespace | not hard-bound to AION at Runtime boundary | implemented API; identity filter exists downstream | Recall Gate rejects mismatched agents, but AION Runtime itself does not enforce `agent_id=AION` | `PARTIAL / GAP` |
| Memory storage partition | one table indexed by `(user_id, agent_id, namespace)` | logical identity partition in a shared database | implemented | direct gate identity-mismatch test exists | logical isolation present; storage-level per-twin partition not established |
| Twin Genesis / Embodiment candidate | validates shared root plus distinct AION/Astra agent, instance, memory namespace, embodiment and canonical references | shared genesis + distinct twin records | implemented non-3D candidate | validation tests reject duplicate agent/instance/memory identifiers | `TWIN_IDENTITY_INVARIANT_CANDIDATE` |
| Twin live Runtime binding | `EmbodimentInstance.runtime_binding` exists but candidate validation requires `NOT_IMPLEMENTED` | AION and Astra individual bindings | intentionally not wired | tests explicitly reject active runtime binding | `NOT_IMPLEMENTED / INTENTIONAL_HOLD` |
| Identity / lineage governance | hash-chained project/system-state records, fork isolation, approval/QA checks | project/system lineage | implemented engineering candidate | component remains QA HOLD | useful project lineage; not twin individual life-history ledger |
| Continuity governance | deterministic continuity reporting/checks | research/governance evidence | implemented candidate | explicitly makes no subject/identity proof | support layer only |
| AION individual event/life-history lineage | persistent ordered events attributable to one AION runtime instance across tasks/sessions | AION | generic per-task audit exists, individual lineage does not | no end-to-end AION life-history test found | `NOT_ESTABLISHED_AS_RUNTIME_CAPABILITY` |
| Astra individual event/life-history lineage | persistent ordered events attributable to one Astra runtime instance across tasks/sessions | Astra | generic per-task audit exists, individual lineage does not | no end-to-end Astra life-history test found | `NOT_ESTABLISHED_AS_RUNTIME_CAPABILITY` |
| Runtime instance identity | concrete running instance ID bound to state, events and memory | separate AION / Astra | twin research model has instance IDs; AIONRuntime/execution records do not carry them | no end-to-end binding test found | `MODEL_EXISTS / RUNTIME_WIRING_MISSING` |
| Distinct canonical-state references | separate AION/Astra references are required by Twin validation | separate AION / Astra | modeled in Twin candidate | duplicate canonical references are rejected by validation | `MODELLED / NOT_RUNTIME_INTEGRATED` |
| Runtime lifecycle/recovery | start/stop/recovery/checkpoint semantics for an individual Runtime instance | separate AION / Astra | candidate task rollback and kill switch exist; individual-runtime lifecycle ledger not found | bounded execution tests cover kill/rollback mechanics | `PARTIAL` |
| AION self-host HTTP | health/status only; POST denied | AION operator surface | implemented read-only | server tests exist | `READ_ONLY_CANDIDATE_SURFACE` |
| Astra individual Runtime composition root | Astra-specific runtime with its own identity/state/memory/event binding | Astra | no such composition root found | none found | `NOT_IMPLEMENTED` |
| Canonical promotion | Owner-approved authoritative AION/Astra Runtime | separate governed state | no current promotion | current statuses retain pending/not-approved | `NOT_APPROVED` |
| Subjectivity conclusion | research conclusion | research governance | deliberately unresolved | explicit non-claims across components | `NOT_ESTABLISHED` |

## Evidence-backed findings

### F1 — Existing `AstraRuntime` is not an Astra individual Runtime

`TaskSpec` contains task/objective/profile/path/approval/network/canonical-effect fields but no `agent_id`, `runtime_instance_id` or individual state binding. `RunResult` likewise lacks an individual-agent binding. The append-only audit is keyed by `task_id` and action, not by AION/Astra individual lineage.

Therefore the current `AstraRuntime` class is best described, by responsibility, as a bounded governed execution engine/runtime-core candidate until naming is reviewed.

### F2 — AION Runtime is a real integrated candidate, but its individual boundary is incomplete

`AIONRuntime` composes execution and governed persistent memory. This is real implementation progress. However:

- execution is delegated without injecting an AION individual/runtime-instance identity;
- memory APIs accept caller-supplied `agent_id` and namespace;
- no AION runtime-instance identifier is carried through task events, memory and audit as one end-to-end lineage.

Therefore `AION_RUNTIME_IMPLEMENTATION_CANDIDATE = IMPLEMENTED` can coexist with `AION_INDIVIDUAL_RUNTIME_BOUNDARY = PARTIAL`.

### F3 — Memory has useful identity isolation, but it is infrastructure-level rather than twin-runtime ownership enforcement

The persistent memory table records `user_id`, `agent_id` and namespace, and recall queries are restricted by `user_id + agent_id`. The Recall Gate also rejects identity mismatch.

However the low-level store is shared infrastructure and the AION-facing API does not hard-bind its records to AION. This is not proof of memory mixing, but it means the individual Runtime boundary is not yet the enforcement point.

### F4 — Twin invariants are stronger than current Runtime wiring

Twin validation already requires distinct:

- agent IDs;
- instance IDs;
- private memory namespaces;
- embodiment IDs;
- canonical-state references.

But the same candidate explicitly requires live `runtime_binding` to remain `NOT_IMPLEMENTED`. The Twin model therefore contains the separation rules that future Runtime integration should obey, but the live wiring is intentionally absent.

### F5 — Current audit is execution evidence, not a continuous individual life history

Each bounded task creates its own candidate workspace and `runtime_audit.jsonl`. The audit hash chain provides integrity inside that task execution. No evidence was found that these task-local chains are joined into a persistent AION-only or Astra-only event lineage across sessions.

This distinction is central to the project's digital-individualization research:

`TASK_AUDIT_CONTINUITY != INDIVIDUAL_EVENT_HISTORY_CONTINUITY`

### F6 — Project lineage governance is not the same as twin life history

`StateLineageLedger` maintains ordered, hash-verified `SystemStateRecord` history for a project/system state. `SystemStateRecord` is keyed by `project_id` and manifest hashes, not by AION/Astra `agent_id` or `runtime_instance_id`.

It is valuable provenance infrastructure, but must not be silently re-labelled as either twin's autobiographical/event history.

### F7 — Historical status locks and current implementation status must remain separate

At least one component-local historical lock still states `live_cross_session_memory = NOT_IMPLEMENTED` while the same component now contains the post-RC persistent store and documents that implementation. The lock must not be deleted merely to make the current state look cleaner.

Use separate fields:

- `HISTORICAL_LOCK_STATUS`
- `CURRENT_IMPLEMENTATION_STATUS`
- `CANONICAL_PROMOTION_STATUS`

rather than overwriting historical evidence.

## Priority gaps

Priority is based on preserving the research design, not on adding features quickly.

### P0 — Individual state ownership and event attribution

Before further Runtime capability expansion, every material Runtime event must be able to answer:

- which twin owns this event/state;
- which runtime instance produced it;
- which memory/event lineage it belongs to;
- what source produced the record;
- whether it has Runtime or canonical effect.

### P0 — Execution engine reclassification

Resolve whether `AstraRuntime` should be renamed/reclassified as a shared bounded execution engine, or whether an explicit adapter layer should separate that generic engine from a future Astra individual Runtime.

No rename is authorized by this matrix.

### P0 — AION Runtime identity binding

Define an AION Runtime instance boundary so AION-specific memory/event state cannot be selected merely by arbitrary caller-supplied `agent_id`.

### P0 — Astra individual Runtime composition

Define the minimum Astra-specific composition root with distinct identity/state/memory/event lineage. This does not require duplicating shared engineering infrastructure.

### P1 — Twin Genesis -> Runtime binding

Connect validated twin identifiers to actual Runtime instances only after the ownership/event model is reviewed. Do not infer subjectivity or embodiment experience from this connection.

### P1 — Individual event ledger

Create or adapt a provenance-safe event ledger that preserves separate AION/Astra event histories across sessions while keeping project engineering audit separate.

### P1 — Status orientation

Create a current-state status view that references but does not rewrite frozen/historical status locks.

### P2 — Lifecycle/recovery semantics

After identity/event ownership is stable, define restart, crash recovery, checkpoint, migration and rollback semantics for individual Runtime instances.

## Current conclusion

The repository has substantial executable and governance infrastructure. The primary missing condition is not another planner, model, API or memory database. It is the end-to-end **individual Runtime binding** that connects identity, runtime instance, events, memory ownership and lineage separately for AION and Astra.

This is an engineering gap relevant to the study of digital individualization. Closing it would still not establish subjectivity, consciousness or phenomenal continuity.
