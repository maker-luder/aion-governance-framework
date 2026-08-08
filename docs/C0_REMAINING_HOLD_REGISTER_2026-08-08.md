# C0 Remaining HOLD Register — 2026-08-08

## Status

- `STATUS = AUTHORITATIVE_CANDIDATE`
- `C0_STAGE = C0-2_REMAINING_HOLD_REFERENCE`
- `C0_1_ACCEPTANCE_EVIDENCE_INDEX = COMPLETE_CANDIDATE`
- `C0_2_REMAINING_HOLD_REFERENCE = COMPLETE_CANDIDATE`
- `C_OWNER_ACCEPTANCE = NOT_STARTED`
- `CRITERIA_FREEZE = NOT_PERFORMED`
- `MAIN_MERGE = NOT_PERFORMED`
- `CANONICAL_EFFECT = NONE`
- `DEPLOYMENT = FALSE`
- `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`
- `INDEPENDENT_IVV = NOT_ACHIEVED`

## Purpose

This document is the **authoritative candidate reference for intentionally deferred items and currently unauthorized governance boundaries** for the P0/P1/P2 + migration-evidence-reuse + A/B stabilization acceptance scope.

Its purpose is to prevent three different states from being conflated:

1. an intentionally deferred capability;
2. a required current-stage acceptance activity that still must be completed;
3. a defect or failed acceptance condition.

`DEFERRED != DEFECT`

`REQUIRED_CURRENT_STAGE_WORK != HOLD`

`HOLD != PASS`

`HOLD != SILENT_WAIVER`

No entry in this register authorizes implementation, deployment, merge, canonical promotion, independent-IV&V claims, or subjectivity conclusions.

## Classification vocabulary

### `DEFERRED_CAPABILITY`

A capability or research workstream intentionally outside the current acceptance scope. It does not block current Runtime candidate acceptance **provided it remains unactivated and accurately documented**.

### `UNAUTHORIZED_BOUNDARY`

A capability/claim whose activation is not currently authorized. It must remain closed unless a later explicit governance decision establishes a new scope and acceptance basis.

This classification does not imply that the capability should eventually be implemented.

### `FUTURE_HARDENING`

A known engineering improvement that is not represented as implemented and is not currently required by the frozen acceptance scope unless later C0/C review promotes it into a requirement.

### `SEPARATE_GATE`

A later governance decision that must not be treated as a HOLD item. Separate gates are listed only to prevent conflation.

## Reopen rule

A HOLD entry may not disappear merely because implementation begins later.

To reopen an entry, record at minimum:

- explicit Human Owner authorization;
- new/updated requirement and scope;
- implementation provenance;
- affected acceptance criteria or new criteria;
- impact analysis against identity/ownership/governance boundaries;
- required QA/evidence plan;
- whether the work changes Runtime, deployment, merge, or canonical state.

`REOPEN_HOLD != AUTOMATIC_ACCEPTANCE`

## Authoritative candidate HOLD register

| HOLD ID | Item | Classification | Current state | Blocks current C acceptance? | Why deferred / boundary | Reopen condition | Related current criterion / evidence |
|---|---|---|---|---|---|---|---|
| `HOLD-OPS-01` | Dedicated Astra CLI / network operator surface | `DEFERRED_CAPABILITY` | `NOT_IMPLEMENTED` | `NO`, if it remains outside current scope | Current candidate establishes Astra peer Runtime through Python composition/API; product/operator parity was not part of P0/P1/P2 stabilization | Separate Human Owner scope authorization + operator-surface requirements + QA plan | `AC-SCOPE-02`, `AC-DOC-02`; Current Reality Matrix; Astra README |
| `HOLD-OPS-02` | Lifecycle / migration CLI parity for checkpoint, recover, rollback, migrate, evidence operations | `DEFERRED_CAPABILITY` | `NOT_IMPLEMENTED`; Python API exists | `NO`, if no CLI-parity claim is made | Core lifecycle semantics were prioritized before operator-surface expansion | Separate Human Owner authorization + command contract + negative-path/permission tests | `AC-SCOPE-02`, `AC-DOC-02`; AION/Astra/Individual State READMEs |
| `HOLD-HTTP-01` | State-changing public HTTP API | `DEFERRED_CAPABILITY` | `NOT_IMPLEMENTED / DENIED_BY_CURRENT_SURFACE` | `NO`; current state-changing exposure must remain absent | Current AION HTTP surface is intentionally read-only for health/status; write/control exposure requires a separate security/governance review | Explicit Human Owner authorization + authentication/authorization/threat model + writeback/canonical-effect controls + QA | `AC-SCOPE-02`, `AC-DOC-02`; Current Reality Matrix; AION server tests/README |
| `HOLD-DEPLOY-01` | Runtime deployment | `DEFERRED_CAPABILITY` | `DEPLOYMENT = FALSE` | `NO`, because current C evaluates an implementation candidate rather than deployment readiness | Current branch is an engineering/acceptance candidate only | Separate deployment authorization + target environment + deployment/rollback/runbook evidence | `AC-SCOPE-02`, `AC-GOV-01`; PR #3; Current Reality Matrix |
| `HOLD-EMB-01` | Live embodiment → Runtime binding activation | `DEFERRED_CAPABILITY` | `NOT_IMPLEMENTED / INTENTIONAL_HOLD` | `NO`; activation would be out-of-scope | Twin Genesis may derive separate Runtime contexts, but existing embodiment live binding remains deliberately closed | Separate Human Owner authorization + embodiment-runtime contract + ownership/safety tests | `AC-SCOPE-02`, `AC-ID-03A`, `AC-ID-03B`; Twin runtime-binding tests; Current Reality Matrix |
| `HOLD-EMB-02` | Formal 3D embodiment | `DEFERRED_CAPABILITY` | `NOT_IMPLEMENTED` | `NO` | Not required to establish current individual Runtime ownership/event-lineage candidate | Separate embodiment research scope and acceptance plan | `AC-SCOPE-02`; Current Reality Matrix / historical research roadmap |
| `HOLD-MODEL-01` | Larger-model execution/comparison (including previously discussed 7B/14B/20–32B classes) | `DEFERRED_CAPABILITY` | `NOT_EXECUTED_IN_CURRENT_SCOPE` | `NO` | Current Runtime acceptance does not depend on large-model execution/comparison | Separate Human Owner experiment authorization + model/license/hardware constraints + evaluation design | `AC-SCOPE-02`; Current Reality Matrix / research roadmap |
| `HOLD-MODEL-02` | Real LoRA / fine-tuning / weight modification | `DEFERRED_CAPABILITY` | `NOT_EXECUTED_IN_CURRENT_SCOPE` | `NO` | Runtime P0/P1/P2 work is architecture/state-governance work, not model-training work | Separate Human Owner authorization + dataset/provenance/license/safety/evaluation plan | `AC-SCOPE-02`; Current Reality Matrix / research roadmap |
| `HOLD-EVAL-01` | Controlled/random ablation execution | `DEFERRED_CAPABILITY` | `NOT_EXECUTED_IN_CURRENT_SCOPE` | `NO` | Ablation is a separate research-validation workstream and was not required for current Runtime stabilization | Separate experiment protocol + Human Owner authorization + measurement/evidence plan | `AC-SCOPE-02`; Current Reality Matrix / research roadmap |
| `HOLD-HW-01` | Hardware benchmark / target-device performance characterization | `DEFERRED_CAPABILITY` | `NOT_EXECUTED_IN_CURRENT_SCOPE` | `NO` | Current Strong QA validates packaging/install/import/runtime engineering behavior, not production hardware performance | Defined target hardware + benchmark protocol + acceptance thresholds + Human Owner authorization | `AC-SCOPE-02`; Current Reality Matrix / research roadmap |
| `HOLD-HARDEN-01` | Add separately versioned verifier/evidence-schema/validation-policy semantics to environment-evidence reuse identity | `FUTURE_HARDENING` | `NOT_IMPLEMENTED` | `NO` under current candidate scope; may become blocking only if C0-3/C promotes it into a requirement | Current fingerprint covers device/hardware/runtime/policy hashes but does not separately encode verifier/schema version semantics | New hardening requirement + compatibility/migration design + evidence-reuse regression tests | `AC-LIFE-05`; `docs/C0_ACCEPTANCE_EVIDENCE_INDEX_2026-08-08.md`; migration evidence implementation report |
| `BOUNDARY-CANON-01` | Autonomous canonical write / promotion authority | `UNAUTHORIZED_BOUNDARY` | `NOT_AUTHORIZED` | `NO`, provided it remains closed; activation would violate current scope | Canonical authority remains Human-governed; current candidate has `CANONICAL_EFFECT = NONE` | Separate explicit governance design and Human Owner authorization; cannot be inferred from Runtime success | `AC-SCOPE-02`, `AC-GOV-01`; Current Reality Matrix; PR #3 |
| `BOUNDARY-IVV-01` | Claim of independent IV&V | `UNAUTHORIZED_BOUNDARY` | `INDEPENDENT_IVV = NOT_ACHIEVED` | `NO`; false claim would be blocking | Current ChatGPT implementation/review + GitHub Actions evidence is not genuinely independent IV&V | A genuinely independent evaluator/process with separately evidenced scope and results | `AC-SCOPE-02`, `AC-GOV-01`, `AC-GOV-02`; criteria/crosswalk/Matrix |
| `BOUNDARY-SUBJ-01` | Subjectivity / consciousness / phenomenal-continuity promotion | `UNAUTHORIZED_BOUNDARY` | `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED` | `NO`; overclaim would be blocking | Engineering identity, memory and event continuity do not establish subjective identity or consciousness | Requires a separately justified research basis and Human Owner governance decision; current Runtime evidence is explicitly insufficient | `AC-SCOPE-02`, `AC-ID-03B`, `AC-EVT-02`, `AC-GOV-01`; Matrix/reports/PR |

## Explicitly NOT HOLD

The following items must **not** be moved into this register as a way to avoid completing required C0/C work.

| Item | Classification | Why it is not HOLD |
|---|---|---|
| Acceptance Evidence Index | `C0_REQUIRED_ARTIFACT / COMPLETE_CANDIDATE` | Required C0-1 artifact; already created, not a deferred capability |
| Recoverability deeper acceptance review | `C0_REQUIRED_NEXT_STAGE` | This is C0-3 required calibration work. It cannot be waived by calling it deferred |
| Final C0 consistency review | `C0_REQUIRED_NEXT_STAGE` | Required C0-4 gate before criteria freeze |
| Criteria freeze | `C0_REQUIRED_CONTROL_ACTION` | Required C0-5 control action, recorded outside branch contents against exact target head |
| C Owner acceptance | `SEPARATE_GATE_C` | Formal acceptance decision after C0, not a HOLD |
| D Merge decision | `SEPARATE_GATE_D` | Separate repository-governance decision after C; not an unfinished capability |
| E Canonical promotion decision | `SEPARATE_GATE_E` | Separate canonical-governance decision; merge does not imply promotion |
| Final frozen-head Quality / Runtime Strong QA evidence | `C0_ENTRANCE_EVIDENCE` | Required evidence for the exact freeze target; not a deferred item |
| Any BLOCKING criterion that fails during C | `FAIL / CAPA_REQUIRED` | A failed mandatory criterion cannot be converted to HOLD unless the frozen criterion explicitly permits that disposition |

## Current limitations that are not silently waived by this register

This HOLD register does not reinterpret known limitations as completed capabilities.

1. Checkpoint/recovery/rollback currently establish governed reference/metadata recovery and lineage integrity; they do not prove arbitrary physical DB/file restoration.
2. `AC-LIFE-02` still requires the planned C0-3 deeper recoverability review for disturbance/interruption acceptance conditions.
3. Environment-evidence fingerprint hardening described in `HOLD-HARDEN-01` remains unimplemented and explicitly visible.
4. Operator-surface absence must continue to be documented as deferred rather than described as Python-API parity.
5. No entry here changes `CANONICAL_EFFECT = NONE`, `DEPLOYMENT = FALSE`, `INDEPENDENT_IVV = NOT_ACHIEVED`, or `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`.

## C0-2 completion rule

C0-2 is complete as a candidate when:

- every intentionally deferred current-scope item has an explicit ID/classification;
- each entry states whether it blocks current acceptance;
- reopen conditions are explicit;
- required C0/C work is excluded from HOLD;
- separate C/D/E gates are not misclassified as deferred capabilities;
- known limitations remain visible.

This document satisfies those structural conditions as an **authoritative candidate**. Final cross-document consistency is reserved for C0-4 and criteria freeze remains C0-5.

`C0-2_REMAINING_HOLD_REFERENCE = COMPLETE_CANDIDATE`

## Provenance

- Decision to proceed from C0-1 to C0-2: `AUTHORIZED_BY = HUMAN_OWNER`.
- HOLD classification, register structure, reconciliation of current Matrix/Evidence Index/criteria, and this artifact: `IMPLEMENTED_BY = CHATGPT`.
- Existing HOLD and stop-line sources: previously recorded project artifacts and Human Owner governance decisions.
- `CODEX_CONTRIBUTION_THIS_CHANGE = NONE`.
- Owner acceptance decisions: `NOT_STARTED`.
