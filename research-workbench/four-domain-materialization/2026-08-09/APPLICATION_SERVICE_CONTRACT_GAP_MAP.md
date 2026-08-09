# Application Service Contract Gap Map

**Architecture guard:** existing application service -> future thin adapter -> future MCP transport. This artifact defines neither MCP tool names nor request/response schemas and creates no facade or transport. The existing Writeback Gate remains authoritative.

## 1. Capability crosswalk

| CAPABILITY | EXISTING_SERVICE | SOURCE_OF_TRUTH | CURRENT_INPUT | CURRENT_OUTPUT | CLASSIFICATION |
|---|---|---|---|---|---|
| Governed recall candidate query | `decide_recall`, `rank_candidates`, `SQLiteMemoryStore.recall` | recall gate/store code + tests | `RecallRequest`, records/candidates | gate decision internally; store returns ranked records | REQUIRES_QUERY_FACADE |
| Memory read/query | `get`, `list_for_identity` | persistent store code + tests | record id or user/agent | record(s) | REUSABLE_WITH_ADAPTER |
| Runtime binding/status | `AIONRuntime.status`, `AstraRuntime.status`, context | runtime code + tests | constructed runtime/context | `RuntimeStatus` | DIRECTLY_REUSABLE |
| Lineage/state verification | runtime-state `verify`; lineage ledger `verify/find/states` | code + tamper/lineage tests | bound store/ledger and optional identifiers | boolean/records/states | REUSABLE_WITH_ADAPTER |
| Environment evidence/provenance | runtime evidence registration/query; workbench evidence; research-integrity assessment | component code + tests | evidence/fingerprint/source context | evidence record or assessment | REUSABLE_WITH_ADAPTER |
| Correction/conflict | store flags; continuity correction observation; research-integrity conflict handling | component code + tests | record id/flag or before-after observations | in-place flag state or analysis result | PARTIAL |
| Continuity assessment | continuity check/matrix/recovery/status functions | continuity code + tests | explicit observations | `DriftResult`, matrix/status/observation | DIRECTLY_REUSABLE |
| Governance decision/status | identity `evaluate_writeback`; `qa_gate_status`; kernel `evaluate_risk`/`run_pipeline`; encounter policy | governance code + tests | candidate/evidence/request/binding | decision/status/response | REUSABLE_WITH_ADAPTER |
| Canonical writeback | identity `evaluate_writeback` is the authoritative gate | identity governance code + tests | provenance/evidence/lineage/QA/Human approval/conflict/canonical-effect facts | allow/reject decision | REJECT_DUPLICATE_CONTROL |
| Memory flag mutation | `set_conflict`, `tombstone`, `supersede` | persistent store code | record id + boolean | no rich transformation record | HOLD |
| Runtime checkpoint/recovery/migration | runtime/state services | runtime-state code + tests | bound context, checkpoint or destination instance | state/checkpoint/migration results + audit events | HOLD for any future external adapter until authority contract is frozen |

## 2. Caller, authority and effect analysis

| CAPABILITY | CALLER_BINDING | AUTHORIZATION_CHECK | PROVENANCE_OUTPUT | PRIVACY_EXPOSURE | DOMAIN_STATE_MUTATION | AUDIT_SIDE_EFFECT | FAIL_CLOSED_BEHAVIOR |
|---|---|---|---|---|---|---|---|
| Governed recall candidate query | request carries user/agent/scope/cue | gate checks identity, scope, provenance, conflict, tombstone/supersession and relevance | `RecallDecision.reason` at gate level; not returned by store/runtime as a full trace | record content, ids, scope and provenance | NO in store; runtime wrapper does not change memory | runtime wrappers append `memory.recalled`; store/gate do not | rejects on missing cue/provenance, mismatch, conflict or inactive record |
| Memory read/query | constructed store; `list_for_identity` user/agent filter | `get` by id has no separate principal check visible; list filters identity | record provenance field | full stored content and metadata | NO | NO | missing record returns absence; principal policy for `get` is incomplete |
| Runtime binding/status | runtime constructed with explicit context | `_require_context` for stateful operations | status exposes binding/status, not full provenance | ids/references may be sensitive | NO | NO | invalid/missing context errors |
| Lineage/state verification | bound DB/ledger path and stable context | lineage-binding validation and hash chain | event/state hashes and bindings | exposes identifiers, payload metadata and history | NO | NO | tamper/binding mismatch fails verification/raises |
| Evidence/provenance | caller supplies evidence/path/source | integrity gate rejects missing/conflicting/roleplay/prompt-induced evidence as applicable | rich evidence/source records by subsystem | environment data and source metadata may retain secrets if callers fail to minimize | registration/save is evidence-domain mutation | YES for registration/save; query/load/assessment pure | assessment/writeback gates fail closed on required deficiencies |
| Correction/conflict | direct store caller or explicit analysis inputs | no complete public principal check on flag setters; writeback gate is separate | correction observation inputs; record provenance only | record state and potentially corrected content | YES for flags; NO for continuity observation | flag history audit absent; analysis pure | conflict blocks recall; missing correction semantics do not auto-resolve |
| Continuity assessment | explicit observations | no storage authority needed; caller controls inputs | observations/results are explicit | longitudinal content may be sensitive | NO | NO | invalid/missing observations produce bounded results/errors, not promotion |
| Governance decision/status | request/candidate and participant binding | schema, risk, writeback and encounter checks | response/reason varies by service | request metadata/evidence can expose details | `evaluate_risk`/writeback/encounter pure | kernel `run_pipeline` writes audit DB | validation/risk/writeback gates reject unmet conditions |
| Canonical writeback | candidate bound to provenance/lineage/approval | canonical `evaluate_writeback` requirements | decision reasons/status | candidate/evidence can be sensitive | decision itself NO | NO in pure evaluator | unmet evidence, QA, Human approval, conflict/pollution or effect condition rejects |
| Memory flag mutation | record id only at method surface | incomplete at store surface | original provenance remains; transition provenance absent | existence/status of memory | YES | NO complete transition audit | unknown id/update behavior is local; no full governance facade |
| Runtime checkpoint/recovery/migration | stable runtime context | lineage/checkpoint binding checks; principal grant outside service | checkpoint/migration/runtime events | state payload/environment may be sensitive | YES | YES | tamper, lineage or isolation violations fail |

## 3. Tests and missing contract decisions

| CAPABILITY | EXISTING_TESTS | MISSING_CONTRACT_DECISION | ADAPTER_REUSE_POTENTIAL |
|---|---|---|---|
| Governed recall candidate query | recall `test_recall_gate.py`, `test_persistent_store.py`; AION/Astra runtime tests | return candidate universe, rejection reasons, rank decomposition, pagination/limits, stable error taxonomy and audited-read semantics | High after query facade; reuse gate/store, do not rebuild retrieval control |
| Memory read/query | persistent store tests | principal authorization for direct id lookup, field-level privacy/redaction and not-found semantics | Medium/high with strict adapter binding |
| Runtime binding/status | AION/Astra runtime tests | which binding fields may be exposed; stable status/error contract | High |
| Lineage/state verification | runtime-state `test_store.py`; identity-governance tests | bounded query ranges, payload redaction, verification evidence projection and error taxonomy | High |
| Evidence/provenance | workbench, runtime-state, integrity and identity tests | common minimal evidence envelope, retention/redaction, secret scanning and fingerprint reuse rules | Medium; reuse structures through adapter |
| Correction/conflict | memory/continuity/integrity tests | correction entity, actor/evidence/reason/time, successor link, resolver authority, immutable transition history and current projection | Low until research/governance decisions; no duplicate correction engine |
| Continuity assessment | continuity tests | accepted observation schema at application boundary, versioning and criteria ownership | High for pure analysis adapter |
| Governance decision/status | governance-kernel, identity and encounter tests | distinguish pure evaluation from audited pipeline; expose bounded reasons without sensitive policy leakage | High if authoritative services remain unchanged |
| Canonical writeback | identity-governance tests | later external exposure is not authorized; no bypass/duplicate gate | Reuse only as authoritative internal gate; `REJECT_DUPLICATE_CONTROL` |
| Memory flag mutation | persistent store tests | full authorization/provenance/rollback contract | HOLD |
| Runtime checkpoint/recovery/migration | runtime-state tests | principal/approval, concurrency/idempotency, bounded payload, rollback and external exposure decision | HOLD |

## 4. Required stable contract properties before an adapter

These are gaps to decide, not frozen schemas:

1. **Explicit caller binding:** principal, subject/agent, namespace, scope, runtime instance and lineage must be supplied or derived from an authoritative local binding, never from relationship text.
2. **Operation effect class:** each contract must disclose observation-only, audited read, domain mutation, lineage mutation and canonical mutation separately.
3. **Provenance projection:** selected records, source/evidence identifiers and gate reasons need a privacy-bounded response projection.
4. **Fail-closed errors:** missing provenance, scope mismatch, conflict, tamper and unavailable state must not be converted to guessed data.
5. **Privacy/retention:** no raw secrets, private paths, cookies or conversation history in evidence fingerprints/logs; define minimization and retention before exposure.
6. **Idempotency/concurrency:** any later state-changing contract requires explicit semantics; none is authorized here.
7. **No duplicate governance:** adapters must call recall, identity, encounter, continuity and Writeback Gate services rather than reimplement them.
8. **Versioning:** contract and evidence schema versions must be explicit before a transport is selected.

## 5. Duplicate-risk findings

- A new MCP-side retrieval policy would duplicate `decide_recall` and create divergent scope/provenance/conflict behavior.
- A new MCP-side canonical promotion rule would duplicate/bypass `evaluate_writeback` and is classified `REJECT_DUPLICATE_CONTROL`.
- A second identity/namespace/lineage store would conflict with stable runtime bindings and encounter policy.
- Treating runtime `recall` as an effect-free query would hide its runtime audit append; a future adapter must make that distinction visible.
- Combining evidence saving, policy evaluation and domain mutation in one opaque call would prevent effect inspection and rollback design.

## 6. Stop boundary

No final tool name, wire schema, service facade, transport, server, writeback path or Teacher binding is defined or implemented in this workbench.
