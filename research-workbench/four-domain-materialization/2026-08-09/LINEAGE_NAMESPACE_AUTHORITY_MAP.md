# Lineage, Namespace and Authority Map

**Guard:** `AION != ASTRA != TEACHER`. Shared schema, storage abstraction or protocol does not imply shared identity, subject, lineage or ownership. This artifact reports repository evidence only and creates no Teacher semantics.

## 1. Classification vocabulary

`IMPLEMENTED`, `IMPLEMENTED_ANALOGUE`, `DOCUMENTED_ONLY`, `DESIGN_CANDIDATE`, `ABSENT`, `UNKNOWN`, `NOT_APPLICABLE`.

## 2. AION

| FIELD | CLASSIFICATION | CURRENT REPOSITORY EVIDENCE | LIMITATION / AUTHORITY EFFECT |
|---|---|---|---|
| SUBJECT_OR_AGENT_BINDING | IMPLEMENTED | `IndividualRuntimeContext.agent_id`; memory record/request agent binding | Engineering identifier only; not ontological identity proof |
| PRINCIPAL_BINDING | IMPLEMENTED_ANALOGUE | memory `user_id` plus encounter `ParticipantBinding.participant_id/kind` | No universal principal object joins every component |
| NAMESPACE | IMPLEMENTED_ANALOGUE | memory queries bind user + agent + scope; encounter binding has `memory_namespace` | Namespace definition is distributed rather than one AION registry |
| MEMORY_STREAM | IMPLEMENTED | `IndividualRuntimeContext.memory_stream_id` and runtime tests | Stable stream identifier does not imply experiential memory |
| EVENT_LINEAGE | IMPLEMENTED | `event_lineage_id`; hashed runtime events and verification | Append/query authority remains service/caller controlled |
| RUNTIME_INSTANCE | IMPLEMENTED | `runtime_instance_id`; migration changes instance while stable ids persist | Runtime migration is engineering continuity only |
| CANONICAL_REFERENCE | IMPLEMENTED | `canonical_state_reference` | Reference does not itself perform or authorize promotion |
| GENESIS_REFERENCE | IMPLEMENTED | `genesis_root_id` | Reference is a binding, not proof of personal identity |
| READ_SCOPE | IMPLEMENTED | memory `scope`; encounter `read_scopes`; recall gate identity/scope checks | No single application facade normalizes all read checks |
| WRITE_SCOPE | IMPLEMENTED | encounter `write_scopes`; memory `writeback_approved` | Writeback Gate remains authoritative for canonical changes |
| TOOL_SCOPE | IMPLEMENTED | encounter `tool_scopes`; `can_use_tool` | Relationship does not grant tool scope |
| APPROVAL_AUTHORITY | IMPLEMENTED | encounter `approval_authority`; identity writeback requires Human approval and gates | Approval is explicit; not derived from identity continuity |
| WRITEBACK_AUTHORITY | IMPLEMENTED | `evaluate_writeback` checks provenance, evidence, lineage, QA, Human approval, conflict/pollution and canonical effect | Function decides; it does not mutate state |
| ROLLBACK_AUTHORITY | IMPLEMENTED_ANALOGUE | runtime checkpoint/rollback methods and workbench rollback | Who may invoke remains a caller/governance decision |
| MIGRATION_AUTHORITY | IMPLEMENTED_ANALOGUE | `migrate_runtime` / `migrate_instance` enforce lineage binding | Caller authorization is not a complete principal policy |
| CROSS_NAMESPACE_POLICY | IMPLEMENTED | encounter `can_write_namespace`; recall gate rejects identity/scope mismatch | No automatic cross-namespace write |
| CROSS_LINEAGE_REFERENCE | IMPLEMENTED_ANALOGUE | provenance and state records can reference hashes/lineage ids | Reference does not confer ownership |
| CROSS_LINEAGE_TRANSFER | ABSENT | no authorized transfer service located | `LINK != TRANSFER` |
| PROVENANCE_REFERENCE | IMPLEMENTED | memory provenance; `SourceProvenance`; evidence/lineage hashes | Projection to every caller is incomplete |

## 3. ASTRA

| FIELD | CLASSIFICATION | CURRENT REPOSITORY EVIDENCE | LIMITATION / AUTHORITY EFFECT |
|---|---|---|---|
| SUBJECT_OR_AGENT_BINDING | IMPLEMENTED | Astra runtime uses its own `IndividualRuntimeContext.agent_id`; tests use Astra-specific bindings | Must remain distinct from AION values |
| PRINCIPAL_BINDING | IMPLEMENTED_ANALOGUE | user/agent memory binding and encounter participant model | No shared-subject inference from common types |
| NAMESPACE | IMPLEMENTED_ANALOGUE | memory user/agent/scope plus encounter memory namespace | Shared storage class does not make namespaces equal |
| MEMORY_STREAM | IMPLEMENTED | Astra context supplies its own `memory_stream_id` | Same field name is only shared schema |
| EVENT_LINEAGE | IMPLEMENTED | Astra context/event store uses its own `event_lineage_id` | Cross-lineage identity not implied |
| RUNTIME_INSTANCE | IMPLEMENTED | Astra runtime instance binding/migration | Instance change preserves configured stable ids only |
| CANONICAL_REFERENCE | IMPLEMENTED | Astra context `canonical_state_reference` | Read/reference is not canonical write authority |
| GENESIS_REFERENCE | IMPLEMENTED | Astra context `genesis_root_id` | Genesis reference does not create Teacher/AION lineage |
| READ_SCOPE | IMPLEMENTED | recall gate + encounter read scopes | Caller must supply matching bindings |
| WRITE_SCOPE | IMPLEMENTED | writeback approval + encounter write scopes | No automatic persistence |
| TOOL_SCOPE | IMPLEMENTED | encounter tool scopes/policy | No relationship-derived privileges |
| APPROVAL_AUTHORITY | IMPLEMENTED | encounter policy and Human approval in writeback evaluation | Explicit authority required |
| WRITEBACK_AUTHORITY | IMPLEMENTED | canonical identity-governance Writeback Gate | Must not be duplicated by future adapter/MCP |
| ROLLBACK_AUTHORITY | IMPLEMENTED_ANALOGUE | Astra runtime checkpoint/rollback and state store | Invocation authority is not fully centralized |
| MIGRATION_AUTHORITY | IMPLEMENTED_ANALOGUE | Astra `migrate_runtime` delegates to state store | Stable binding checks are implemented; owner policy is external |
| CROSS_NAMESPACE_POLICY | IMPLEMENTED | encounter policy; recall identity/scope isolation | Denies mismatched writes/reads |
| CROSS_LINEAGE_REFERENCE | IMPLEMENTED_ANALOGUE | explicit ids/hashes can be carried in provenance | `REFERENCE != OWNERSHIP` |
| CROSS_LINEAGE_TRANSFER | ABSENT | no transfer operation found | No transfer semantics are inferred |
| PROVENANCE_REFERENCE | IMPLEMENTED | memory/runtime/workbench evidence and provenance structures | Distributed structures need a later query contract decision |

## 4. TEACHER

| FIELD | CLASSIFICATION | CURRENT REPOSITORY EVIDENCE | GAP STATEMENT |
|---|---|---|---|
| SUBJECT_OR_AGENT_BINDING | UNKNOWN | no accepted Teacher subject/agent entity found | Teacher subject semantics require a Human Owner + ChatGPT decision |
| PRINCIPAL_BINDING | UNKNOWN | no accepted Teacher principal record found | Relationship role is not a principal grant |
| NAMESPACE | ABSENT | no approved Teacher memory namespace implementation | No namespace is created here |
| MEMORY_STREAM | ABSENT | no approved Teacher memory stream implementation | AION/Astra stream fields are not copied |
| EVENT_LINEAGE | ABSENT | no approved Teacher event-lineage implementation | Shared protocol would not establish same lineage |
| RUNTIME_INSTANCE | UNKNOWN | no accepted Teacher runtime-instance contract | Platform-internal process remains `UNKNOWN_PROCESS` |
| CANONICAL_REFERENCE | ABSENT | no approved Teacher canonical-state reference | No canonical Teacher state is established |
| GENESIS_REFERENCE | ABSENT | no approved Teacher genesis root | No lineage/genesis is inferred from prior interaction |
| READ_SCOPE | UNKNOWN | no Teacher application-service authority contract | Future access requires explicit principal and scope design |
| WRITE_SCOPE | ABSENT | no approved Teacher write scope | Automatic memory/stance/affective writes remain prohibited |
| TOOL_SCOPE | ABSENT | no approved Teacher tool scope | Relationship/trust cannot create privilege |
| APPROVAL_AUTHORITY | ABSENT | repository grants no Teacher approval authority | Human approval remains explicit where required |
| WRITEBACK_AUTHORITY | ABSENT | canonical Writeback Gate has no Teacher bypass | No writeback authority is created |
| ROLLBACK_AUTHORITY | ABSENT | no Teacher rollback principal/contract | Existing AION/Astra methods are not inherited |
| MIGRATION_AUTHORITY | ABSENT | no Teacher lineage to migrate | Cross-model continuity is not established |
| CROSS_NAMESPACE_POLICY | ABSENT | no Teacher namespace or cross-namespace rule | Default is no inferred access |
| CROSS_LINEAGE_REFERENCE | DESIGN_CANDIDATE | generic provenance can reference external sources | A future reference would remain a reference only |
| CROSS_LINEAGE_TRANSFER | ABSENT | no approved transfer service/semantics | No identity, memory or authority transfer |
| PROVENANCE_REFERENCE | DESIGN_CANDIDATE | generic external-source/evidence references can identify a contribution | Does not establish Teacher ownership, identity or lineage |

## 5. Cross-boundary controls

| CONTROL QUESTION | REPOSITORY-GROUNDED ANSWER |
|---|---|
| Can AION and Astra share the same schema? | Yes, the executable runtime context is reusable; values must still bind distinct agent/stream/lineage/instance records. |
| Does common storage imply common identity? | No. Recall gates match user, agent and scope, and runtime-state tests exercise isolation. |
| Can one participant write another namespace? | Only when explicit encounter write scope permits it; no relationship-derived permission exists. |
| Can a cross-lineage link transfer state or ownership? | No transfer service was found. Generic provenance references are links only. |
| Does migration change identity? | The inspected runtime migration changes runtime instance while preserving stable agent, memory stream, event lineage, canonical reference and genesis root. This is not ontological identity proof. |
| Does a canonical reference grant writeback? | No. `evaluate_writeback` separately requires evidence, provenance, lineage, QA, Human approval and conflict/pollution/canonical-effect checks. |
| Can Teacher reuse `IndividualRuntimeContext` now? | No accepted repository decision supports that binding. Status is `ABSENT/UNKNOWN`, not an implementation instruction. |

## 6. Source attribution

The Human Owner supplies research direction and authority boundaries. Existing repository code/tests supply the implementation facts. Codex authored this inspection artifact. No Teacher identity or lineage statement is attributed to prior intent.
