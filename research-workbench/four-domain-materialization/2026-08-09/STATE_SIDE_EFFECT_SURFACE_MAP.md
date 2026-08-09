# State Side-Effect Surface Map

**Scope:** repository-observed effects at `main@b2fb12c050a9c6f93240106929a282ae8cf88499`. This map supplies evidence for a later policy decision; it does not itself label operations as approved MCP reads or writes.

## 1. Effect vocabulary

- **DOMAIN_STATE_MUTATION:** changes application data such as a memory record, conflict flag, checkpoint or task state.
- **CANONICAL_STATE_MUTATION:** changes an approved/canonical state reference or promotes a candidate.
- **IDENTITY_MUTATION:** changes subject/principal identity binding.
- **LINEAGE_MUTATION:** appends or changes a lineage/event chain.
- **MEMORY_MUTATION:** creates or modifies memory content/flags.
- **OBSERVATION_OR_SECURITY_AUDIT_APPEND:** append-only evidence of an otherwise read/evaluation operation.
- `NO` means no effect found in the inspected implementation. `UNKNOWN` means the dependency or caller contract does not expose enough evidence.

## 2. Operation inventory and storage effects

| SERVICE | PATH | METHOD_OR_FUNCTION | READS | WRITES | DATABASE_TABLE_OR_FILE | APPENDS_RUNTIME_EVENT | APPENDS_MEMORY_EVENT | APPENDS_SECURITY_OR_GOVERNANCE_AUDIT |
|---|---|---|---|---|---|---|---|---|
| Governed recall gate | `components/memory_recall_governance_v0.1.0/src/aion_memory_recall/gate.py` | `decide_recall` | request + record fields | none | none | NO | NO | NO |
| Governed recall gate | same | `rank_candidates` | candidate relevance/eligibility | none | none | NO | NO | NO |
| Persistent memory | `.../aion_memory_recall/store.py` | `write` | write approval + record | inserts record | SQLite memory table | NO | record creation (domain record, not runtime event) | NO |
| Persistent memory | same | `get` | record by id | none | SQLite memory table | NO | NO | NO |
| Persistent memory | same | `list_for_identity` | records by user/agent | none | SQLite memory table | NO | NO | NO |
| Persistent memory | same | `recall` | candidates + gate/ranking | none | SQLite memory table | NO | NO | NO |
| Persistent memory | same | `set_conflict` / `tombstone` / `supersede` | target record | updates flag | SQLite memory table | NO | flag mutation | NO |
| AION runtime | `components/aion_runtime_v0.1.0/src/aion_runtime/runtime.py` | `status` | context/runtime metadata | none | none | NO | NO | NO |
| AION runtime | same | `remember` | context + input | memory record + runtime event | memory SQLite + runtime events | YES (`memory.written`) | YES | NO separate security log |
| AION runtime | same | `recall` | context + memory candidates | runtime observation event | memory SQLite read + runtime events write | YES (`memory.recalled`) | NO | YES, as runtime observation audit |
| AION runtime | same | `checkpoint` | runtime state | checkpoint | runtime checkpoint table | implementation may append state evidence | NO | YES, checkpoint evidence |
| AION runtime | same | `recover` | checkpoint/events | runtime recovery event | runtime tables | YES (`runtime.recovered`) | NO | YES |
| AION runtime | same | `rollback_to_checkpoint` / `migrate_runtime` | checkpoint/lineage | runtime state/events/instance binding | runtime tables | YES | NO | YES |
| Astra runtime | `components/astra_runtime_v0.1.0/src/astra_runtime/runtime.py` | `status` | context/runtime metadata | none | none | NO | NO | NO |
| Astra runtime | same | `remember` | context + input | memory record + runtime event | memory SQLite + runtime events | YES (`memory.written`) | YES | NO separate security log |
| Astra runtime | same | `recall` | context + memory candidates | runtime observation event | memory SQLite read + runtime events write | YES (`memory.recalled`) | NO | YES, as runtime observation audit |
| Astra runtime | same | `checkpoint` / `recover` / `rollback_to_checkpoint` / `migrate_runtime` | runtime state/lineage | checkpoints/events/instance binding | runtime tables | YES where operation records event | NO | YES |
| Runtime state | `components/individual_runtime_state_v0.1.0/src/individual_runtime_state/store.py` + `hardening.py` | `append_event` | prior chain head + binding | event row | `runtime_events` | YES | NO | event itself is audit evidence |
| Runtime state | same | `events` / `verify` / `get_checkpoint` / `latest_checkpoint` / `get_environment_evidence` / `migration_summary` | tables/chain | none | runtime tables | NO | NO | NO |
| Runtime state | same | `register_environment_evidence` | binding + evidence | evidence row | `runtime_environment_evidence` | NO | NO | YES evidence append |
| Runtime state | same | `checkpoint` | events/binding | checkpoint row | `runtime_checkpoints` | may append hardening event | NO | YES |
| Runtime state | same | `recover` | checkpoint/events | implementation recovery evidence | runtime tables | YES | NO | YES |
| Runtime state | same | `rollback_to_checkpoint` | target checkpoint | rollback event/state projection | runtime tables | YES | NO | YES |
| Runtime state | same | `migrate_instance` | source binding/events | destination binding + migration event | runtime tables | YES | NO | YES |
| State lineage | `components/identity_governance_v0.1.0/src/aion_astra_governance/lineage.py` | `append` | prior ledger | append line | JSONL ledger file | NO | NO | YES lineage event |
| State lineage | same | `find` / `states` / `verify` | ledger | none | JSONL ledger file | NO | NO | NO |
| Continuity | `components/continuity_governance_v0.1.0/src/aion_continuity_governance/checks.py` | all four public functions | supplied observations | none | none | NO | NO | NO |
| Workbench evidence | `components/astra_workbench_v1.0.0/src/astra_engineering_workbench/evidence.py` | `environment_fingerprint` | supplied environment | none | none | NO | NO | NO |
| Workbench evidence | same | `save_evidence` / `load_evidence` | evidence or file | file for save; none for load | evidence JSON file | NO | NO | save is evidence materialization |
| Workbench audit | `.../astra_engineering_workbench/audit.py` | `append` | previous chain | append record | append-only audit file | NO | NO | YES |
| Workbench audit | same | `verify` / `events` | audit file | none | append-only audit file | NO | NO | NO |
| Governance kernel | `components/governance_kernel_v0.4.0/src/aion_governance_kernel/risk/policy.py` | `evaluate_risk` | request | none | none | NO | NO | NO |
| Governance kernel | `.../pipeline.py`; `.../audit/repository.py` | `run_pipeline` | request/policy | decision audit row | governance audit SQLite | NO | NO | YES, including evaluated/failed decisions |
| Identity/writeback | `components/identity_governance_v0.1.0/src/aion_astra_governance/governance.py` | `evaluate_writeback` / `qa_gate_status` | candidate evidence/approvals | none | none | NO | NO | NO |
| Encounter governance | `components/encounter_governance_v0.1.0/src/aion_encounter_governance/policy.py` | `can_use_tool` / `can_write_namespace` / `can_approve` / `shared_identity_claim_allowed` | participant bindings/policy | none | none | NO | NO | NO |

## 3. Domain and governance mutation classification

| METHOD_OR_FUNCTION | CHANGES_MEMORY_CONTENT | CHANGES_IMPORTANCE | CHANGES_CONFLICT_STATE | CHANGES_CONTINUITY_STATE | CHANGES_IDENTITY | CHANGES_NAMESPACE | CHANGES_LINEAGE | CHANGES_CANONICAL_STATE | NETWORK_SIDE_EFFECT | ROLLBACK_AVAILABLE |
|---|---|---|---|---|---|---|---|---|---|---|
| `decide_recall`, `rank_candidates` | NO | NO | NO | NO | NO | NO | NO | NO | NO | NOT_APPLICABLE |
| store `write` | YES | NO (field absent) | initial value only | NO | NO | binds existing user/agent, does not change namespace definition | NO | NO | NO | tombstone/supersession are compensating flags; no full content rollback |
| store `get`, `list_for_identity`, `recall` | NO | NO | NO | NO | NO | NO | NO | NO | NO | NOT_APPLICABLE |
| `set_conflict` | NO | NO | YES | NO | NO | NO | NO | NO | NO | flag can be reset through private helper path; no audited history |
| `tombstone`, `supersede` | active-state flag only | NO | NO | NO | NO | NO | NO | NO | NO | no complete version rollback contract |
| runtime `status` | NO | NO | NO | NO | NO | NO | NO | NO | NO | NOT_APPLICABLE |
| runtime `remember` | YES | NO | initial value only | event history grows | NO | NO | YES (runtime event) | NO | NO in core method | partial via flags/checkpoints, not content-history reversal |
| runtime `recall` | NO | NO | NO | runtime event history grows | NO | NO | YES (observation event) | NO | NO in core method | audit append is intentionally immutable |
| runtime `checkpoint` / `recover` / `rollback` | NO memory content | NO | NO | YES | NO | NO | YES | no canonical promotion | NO | YES, checkpoint/rollback mechanisms |
| runtime `migrate_runtime` / state `migrate_instance` | NO | NO | NO | YES | NO stable agent binding | runtime instance changes, memory/event lineage remains stable | YES | NO | NO | migration evidence + source state; reverse migration not promised |
| runtime-state queries/`verify` | NO | NO | NO | NO | NO | NO | NO | NO | NO | NOT_APPLICABLE |
| lineage `append` | NO | NO | NO | lineage history grows | NO | NO | YES | MAY RECORD a state relation; does not itself authorize promotion | NO | append-only; compensating event only |
| lineage queries/`verify` | NO | NO | NO | NO | NO | NO | NO | NO | NO | NOT_APPLICABLE |
| continuity functions | NO | NO | NO | NO (return analysis only) | NO | NO | NO | NO | NO | NOT_APPLICABLE |
| evidence `save_evidence` | NO | NO | NO | NO | NO | NO | evidence file created, not identity lineage | NO | NO | file replacement policy is caller-controlled |
| audit `append` / kernel `run_pipeline` | NO | NO | NO | audit history grows | NO | NO | audit chain/row grows | NO | NO in inspected core | append-only/no deletion contract |
| identity `evaluate_writeback` | NO | NO | NO | NO | NO | NO | NO | NO; returns permission decision only | NO | NOT_APPLICABLE |
| encounter policy methods | NO | NO | NO | NO | NO | NO | NO | NO | NO | NOT_APPLICABLE |

## 4. Authorization and test evidence

| OPERATION_GROUP | AUTHORIZATION_REQUIRED | CURRENT_TEST_EVIDENCE | OBSERVED OPERATION SHAPE |
|---|---|---|---|
| Recall gate | request must match user, agent, scope; provenance/conflict/eligibility checks | `components/memory_recall_governance_v0.1.0/tests/test_recall_gate.py` | observation-only decision |
| Persistent store read/recall | identity binding and recall gate for recall | `.../tests/test_persistent_store.py` | read-only at store layer |
| Persistent store write | `writeback_approved` required | `test_persistent_store.py` | domain/memory mutation |
| Memory flag mutation | direct caller access; complete public authority model not located | `test_persistent_store.py` | domain/memory flag mutation |
| AION/Astra recall | valid runtime context; underlying recall gates | runtime component tests | audited read: memory is read, runtime event is appended |
| AION/Astra remember | valid context + approved writeback | runtime component tests | memory + lineage/event mutation |
| Runtime checkpoint/recovery/migration | stable lineage binding and method inputs; owner policy sits above service | `components/individual_runtime_state_v0.1.0/tests/test_store.py` | state/lineage mutation with verification evidence |
| Runtime-state verification/query | repository binding validation | `test_store.py` includes tamper and isolation cases | observation-only |
| State-lineage append | valid `LineageEvent`; ledger hash validation | identity-governance tests | lineage/audit append |
| State-lineage query/verify | ledger path | identity-governance tests | observation-only |
| Continuity checks | supplied observations; no storage access | continuity tests | pure analysis |
| Evidence save/load | caller controls approved path | workbench tests | save mutates evidence file; load is read-only |
| Workbench audit append/verify | caller controls audit instance; hash chain enforced | workbench audit tests | append vs observation-only verify |
| Governance kernel `run_pipeline` | schema validation + risk policy | governance-kernel tests | policy evaluation plus governance audit append |
| Identity writeback evaluation | provenance, evidence manifest, lineage, QA, human approval, conflict/pollution and canonical-effect checks | identity-governance tests | pure fail-closed authorization decision |
| Encounter policy | participant tool/write/approval scopes | encounter-governance tests | pure authorization decision; shared identity claim is false |

## 5. Special findings

1. `SQLiteMemoryStore.recall` is read-only at the persistent-memory layer.
2. `AIONRuntime.recall` and `AstraRuntime.recall` are **not effect-free**: each reads memory and appends a `memory.recalled` runtime event. The observed effect is an audit/lineage append, not a memory-content mutation.
3. Governance Kernel `evaluate_risk` is pure, while `run_pipeline` records the decision in its audit database; callers must not substitute one contract for the other.
4. `StateLineageLedger.find`, `states`, and `verify` query/verify; `append` mutates the append-only ledger.
5. Continuity functions return analyses and do not persist continuity state in the inspected implementation.
6. No inspected operation changes governed memory importance because no such memory field/service exists.
7. No operation in this task or map authorizes canonical promotion, identity mutation, cross-namespace transfer, or network exposure.
