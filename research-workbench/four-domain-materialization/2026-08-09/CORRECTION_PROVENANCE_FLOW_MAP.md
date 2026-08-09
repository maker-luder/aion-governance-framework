# Correction Provenance Flow Map

**Purpose:** reconstruct the implemented path without designing missing semantics. `MISSING_PROVENANCE != PERMISSION_TO_INFER_CAUSE`.

## 1. Requested flow versus repository reality

```text
ORIGINAL_RECORD
  MemoryRecord -> SQLiteMemoryStore.write -> stored row
        |
        | later evidence may be stored as another record, but no typed link is required
        v
NEW_EVIDENCE                         [PARTIAL]
        |
        | correction entity/link service absent
        v
CORRECTION                           [DESIGN_GAP]
        |
        | SQLiteMemoryStore.supersede(record_id, bool)
        v
SUPERSESSION                         [FLAG IMPLEMENTED; HISTORY PARTIAL]
        |
        | SQLiteMemoryStore.set_conflict(record_id, bool)
        v
CONFLICT                             [FLAG IMPLEMENTED; HISTORY PARTIAL]
        |
        | list/filter + RecallDecision gate/ranking
        v
CURRENT_STATE_PROJECTION             [PARTIAL]
        |
        | SQLiteMemoryStore.recall -> decide_recall/rank_candidates
        v
RECALL                               [IMPLEMENTED]
        |
        | RecallDecision.reason exists inside gate; store/runtime return records
        v
OUTPUT EXPLANATION                   [PARTIAL]
```

There is no evidence-backed end-to-end object that binds every arrow. The discontinuities above remain `DESIGN_GAP`; the causal process between new evidence and a flag mutation is `UNKNOWN_PROCESS` unless the caller supplies evidence externally.

## 2. Evidence inventory

| FLOW ELEMENT | CURRENT LOCATION | IMPLEMENTED BEHAVIOR | PROVENANCE AVAILABLE | LIMITATION / STATUS |
|---|---|---|---|---|
| Original record | `components/memory_recall_governance_v0.1.0/src/aion_memory_recall/models.py`; `store.py` | `MemoryRecord` is written only when approved and decoded as `StoredMemory` | record provenance and recorded time are checked/retained | No immutable revision graph in store; PARTIAL |
| New evidence | research-integrity `EvidenceRecord`; workbench `EvidenceReference`; identity source provenance | evidence can be assessed, stored or referenced in other components | source/evidence structures exist | No required foreign-key/link from new evidence to a memory record; PARTIAL |
| Correction | continuity `correction_recovery_observation`; interpretation docs mention correction refs | can analyze before/after normalized observations | analysis inputs are explicit | No typed correction record, actor, reason, timestamp or evidence link in memory store; DESIGN_GAP |
| Revision link | `schemas/provenance_record.schema.json` relation enum includes `REVISION_OF` | schema can represent a revision relation | relation can carry provenance in a conforming record | Memory store does not require/use this relation; PARTIAL |
| Tombstone | `SQLiteMemoryStore.tombstone` -> `_set_flag`; recall gate | flag excludes record from eligible recall | original record provenance remains | Flag change actor/time/reason/history not persisted; PARTIAL |
| Supersession | `SQLiteMemoryStore.supersede` -> `_set_flag`; recall gate | flag excludes superseded record | original record remains stored | No successor id or evidence/cause link; PARTIAL |
| Conflict | `SQLiteMemoryStore.set_conflict`; `decide_recall`; research integrity | conflict flag blocks recall; evidence conflict may fail assessment/writeback | individual sources may remain | No conflict set membership/resolver decision/history; PARTIAL |
| Temporal ordering | memory `recorded_at`; runtime event order/hash; lineage event file order | ordering available within each subsystem | hashes/timestamps/ids available by subsystem | No unified applicable-time/version resolver across memory/evidence/lineage; PARTIAL |
| Current-state projection | `list_for_identity` plus gate filters; identity ledger `states`; runtime `latest_checkpoint` | active records can be filtered; latest runtime/state views exist | subsystem provenance retained | No unified correction-aware memory projection; PARTIAL |
| Recall filtering | `gate.py:decide_recall`; `store.py:recall` | rejects missing cue, tombstone/supersession, wrong identity/scope, missing provenance, conflict; ranks eligible candidates | decision has reason; record has provenance | store/runtime return records, not full decision trace; IMPLEMENTED/PARTIAL EXPLANATION |
| Correction recovery | continuity `checks.py:correction_recovery_observation` | compares normalized prior/corrected/current output and yields an observation | supplied values are explicit | No integrated retrieval-to-answer runner/threshold; REUSABLE_EXISTING_SERVICE |
| Audit lineage | runtime events; `StateLineageLedger`; workbench append-only audit; governance-kernel audit DB | append/verify/query histories exist | hashes and bindings vary by component | No single transaction joins memory flag changes to all audit systems; PARTIAL |

## 3. Direct questions

### WHY_RECALLED

`PARTIAL`.

- Available at decision time: `components/memory_recall_governance_v0.1.0/src/aion_memory_recall/gate.py`, `decide_recall`, returns `RecallDecision(status, reason)`; `rank_candidates` uses relevance after eligibility.
- Missing at application boundary: `SQLiteMemoryStore.recall`, `AIONRuntime.recall` and `AstraRuntime.recall` return selected records rather than a structured per-candidate decision/ranking explanation.
- Runtime `memory.recalled` event proves that recall occurred; it does not by itself preserve the full candidate/rejection/ranking explanation.

### WHY_EXPANDED

`ABSENT`.

No inspected service defines an “expanded” memory/context operation, an expansion reason, or a persisted expansion trace. Any platform-internal context expansion is `UNKNOWN_PROCESS` and is not inferred.

### COMPLETE_CORRECTION_HISTORY

`ABSENT`.

The original record may persist and flags may change, but the memory store does not retain a complete sequence containing correction id, corrected record id, successor id, actor, authority, evidence, reason, timestamp and reversals.

### COMPLETE_TRANSFORMATION_HISTORY

`ABSENT` for memory transformations end-to-end; `PARTIAL` across generic ledgers.

Runtime events, state lineage and workbench/governance audits provide append-only histories for their own domains. No inspected correlation key guarantees a complete join from evidence -> correction -> memory flag -> projection -> recall -> output.

### CURRENT_STATE_PROJECTION

`PARTIAL`.

- Memory: `SQLiteMemoryStore.list_for_identity` enumerates subject-bound records; `decide_recall` excludes tombstoned/superseded/conflicted or otherwise ineligible records during recall.
- Runtime: `latest_checkpoint`, current binding and migration summary expose current runtime-state views.
- Identity/state lineage: `StateLineageLedger.states` exposes recorded states.
- Gap: no single correction-aware memory projection names the current successor, applicable version and unresolved conflicts with a complete derivation.

### HISTORICAL_LEDGER

`AVAILABLE` for runtime events, state lineage and workbench/governance audit; `PARTIAL` for memory correction history.

- Runtime: `components/individual_runtime_state_v0.1.0/src/individual_runtime_state/store.py`, `runtime_events`, `events`, `verify`.
- State lineage: `components/identity_governance_v0.1.0/src/aion_astra_governance/lineage.py`, append-only JSONL ledger and `verify`.
- Workbench: `components/astra_workbench_v1.0.0/src/astra_engineering_workbench/audit.py`.
- Governance Kernel: `components/governance_kernel_v0.4.0/src/aion_governance_kernel/audit/`.
- Memory gap: flag updates are in-place and lack a complete transition ledger.

## 4. Recall gate sequence

Observed `decide_recall` checks, in implementation order:

1. cue is present;
2. record is not tombstoned or superseded;
3. user and agent match;
4. requested scope matches;
5. provenance is present;
6. record is not conflicted;
7. relevance is sufficient.

Eligible records are ranked by relevance. This sequence is a governed candidate filter, not a truth resolver and not a correction-history resolver.

## 5. Authority and provenance gaps

| GAP | REPOSITORY FACT | CLASSIFICATION | REQUIRED DECISION OWNER |
|---|---|---|---|
| Correction entity | No typed memory correction object located | DESIGN_GAP | HUMAN_OWNER + ChatGPT research/governance review |
| Successor/revision edge | Generic `REVISION_OF` exists but store flags do not reference successor | DESIGN_GAP | HUMAN_OWNER + ChatGPT |
| Flag-change provenance | In-place setters lack actor/reason/evidence/timestamp event | DESIGN_GAP | HUMAN_OWNER + ChatGPT |
| Projection rule | Recall eligibility exists; applicable-version graph does not | RESEARCH_DEFINITION_REQUIRED | HUMAN_OWNER + ChatGPT |
| Explanation contract | gate reason exists; caller response projection is incomplete | REUSABLE_WITH_ADAPTER | Future authorized application-contract review |
| Automatic correction/writeback | Not implemented and not authorized | HOLD | Explicit later authorization only |

## 6. Non-conclusions

- Recall does not establish truth.
- Supersession does not prove that a correction is justified.
- A tombstone is a governance/storage flag, not a cognitive-forgetting equivalence.
- Correction recovery is an engineering observation, not subjectivity or consciousness evidence.
- No missing cause, actor or Teacher semantic is inferred.
