# C0 Acceptance Evidence Index — 2026-08-08

## Status

- `STATUS = COMPLETE_CANDIDATE`
- `C0_STAGE = C0-1_ACCEPTANCE_EVIDENCE_INDEX`
- `ACCEPTANCE_RESULTS = NOT_EVALUATED`
- `C_EXECUTION = NOT_STARTED`
- `CRITERIA_FREEZE = NOT_PERFORMED`
- `CANONICAL_EFFECT = NONE`
- `MAIN_MERGE = NOT_PERFORMED`
- `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`
- `INDEPENDENT_IVV = NOT_ACHIEVED`

## Purpose

This document is a **traceability and evidence-navigation index**, not an acceptance result record.

It maps each current candidate acceptance criterion to:

`requirement/source -> criterion -> implementation/review artifact -> test/review method -> objective evidence location/type -> known limitation or future C evidence`

No row may be marked PASS/FAIL/HOLD/N/A before criteria freeze and C execution.

`EVIDENCE_EXISTS != ACCEPTANCE_DECISION`

`INDEXED_EVIDENCE != OWNER_ACCEPTANCE`

## Evidence-state vocabulary

- `AVAILABLE` — repository artifact or repeatable workflow evidence already exists and can be inspected during C.
- `PARTIAL_AVAILABLE` — some required evidence exists, but C must complete a review/traceability step.
- `FUTURE_C_EVIDENCE` — the evidence is intentionally created only during C, such as the Owner Decision Record or CAPA disposition.
- `OUT_OF_TREE_FINAL_EVIDENCE` — final target-head workflow IDs or freeze/Owner records are intentionally stored in PR metadata/review records so recording them does not mutate the accepted head.

These are evidence-location states only. They are **not** acceptance outcomes.

## Acceptance Evidence Index

| Criterion | Requirement / source | Implementation / review artifact | Test / review method | Objective evidence location / type | Evidence state | Known limitation / C note |
|---|---|---|---|---|---|---|
| `AC-SCOPE-01` | Human Owner authorization of P0/P1/P2, migration evidence reuse and A+B; no silent scope expansion | PR #3 diff; P0/P1/P2/migration/A+B reports; current Reality Matrix | Compare locked PR diff and changed-file list against authorized scope and necessary QA/docs fixes | PR changed-file list; implementation reports; `docs/RUNTIME_REALITY_MATRIX_CURRENT_2026-08-08.md`; `docs/history/reconciliation/STABILIZATION_A_B_REPORT_2026-08-08.md` | AVAILABLE | C must perform the scope comparison against the frozen head; no result recorded here |
| `AC-SCOPE-02` | Existing HOLD / stop lines | Current Reality Matrix; PR body; component READMEs; research stop-line docs | Review deferred items and verify they were not silently activated | `docs/RUNTIME_REALITY_MATRIX_CURRENT_2026-08-08.md`; AION/Astra/Individual State READMEs; PR #3 body | PARTIAL_AVAILABLE | Authoritative Remaining HOLD reference belongs to later C0 work and is not created by C0-1 |
| `AC-ID-01` | P0 Runtime identity binding | `components/aion_runtime_v0.1.0/src/aion_runtime/runtime.py`; `components/astra_runtime_v0.1.0/src/astra_runtime/runtime.py` | Negative construction tests with wrong `agent_id` | AION `tests/test_runtime.py::test_runtime_rejects_non_aion_context`; Astra `tests/test_runtime.py::test_runtime_rejects_non_astra_context`; workflow execution on locked head | AVAILABLE | Confirms engineering agent binding only; does not establish subjective identity |
| `AC-ID-02` | P0 current-instance exact-match boundary; P2 migration invariant | AION/Astra Runtime task admission; `IndividualRuntimeContext`; migration code | Submit context substitutions; verify fail-closed; separately verify approved migration changes only `runtime_instance_id` | AION/Astra `tests/test_runtime.py::test_task_context_must_match_bound_*`; state-store migration ownership tests; lifecycle migration tests | AVAILABLE | Current-instance exact match must not be misread as lifetime immutability |
| `AC-ID-03A` | Twin ownership invariant; P0/P1 separate ownership | Twin Runtime binding; AION/Astra bound contexts; state store | Validate shared genesis with separate agent/instance/memory/event/canonical ownership; reject shared event lineage | `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_runtime_binding.py`; AION/Astra mismatch tests | AVAILABLE | Shared `genesis_root_id` is permitted only by validated Twin relation |
| `AC-ID-03B` | Research non-inference / stop lines | Reality Matrix; AION/Astra READMEs; P0/P1/P2 reports; Twin docs; PR body | Documentation/non-claim review for forbidden inference from shared genesis/infra to shared identity/subjectivity | `docs/RUNTIME_REALITY_MATRIX_CURRENT_2026-08-08.md`; implementation reports; PR #3 body | AVAILABLE | Evidence is documentary/governance, not a consciousness test |
| `AC-MEM-01` | P0 memory ownership binding | AION/Astra Runtime `remember` / `recall` composition | Write and recall without caller-selected agent/namespace; verify bound ownership | AION `tests/test_runtime.py::test_runtime_memory_round_trip_is_bound_to_aion_stream`; Astra `tests/test_runtime.py::test_memory_is_bound_to_astra_stream` | AVAILABLE | Confirms Runtime-bound ownership; does not assert autobiographical subjectivity |
| `AC-EVT-01` | P1 persistent separate append-only event lineage | `components/individual_runtime_state_v0.1.0/src/individual_runtime_state/store.py`; AION/Astra lifecycle composition | Restart/reopen same lineage; verify sequence/hash links; reject different agent; inspect append-only behavior | `components/individual_runtime_state_v0.1.0/tests/test_store.py`; AION/Astra lifecycle tests | AVAILABLE | Event history is distinct from content memory |
| `AC-EVT-02` | Research non-claim: event continuity != subjective continuity | Reality Matrix; P1/P2 report; READMEs; PR body | Review wording for consciousness/phenomenal-continuity overclaim | `docs/history/reconciliation/P1_P2_RUNTIME_LINEAGE_LIFECYCLE_IMPLEMENTATION_REPORT_2026-08-08.md`; Reality Matrix; PR body | AVAILABLE | Documentary governance criterion only |
| `AC-LIFE-01` | P2 restart/reopen continuity | Individual state store; AION/Astra Runtime lifecycle | Reopen same state DB/context; verify sequence continues and chain verifies | state-store `test_event_lineage_persists_across_restart`; AION/Astra `test_restart_reopens_same_event_lineage` | AVAILABLE | C0-3 may deepen recoverability scenarios later; C0-1 does not alter criteria |
| `AC-LIFE-02` | P2 fail-closed recovery; external recoverability calibration | State-store `verify()` / `recover()` | Verify full chain before recovery; corruption/invalid-chain behavior review | `components/individual_runtime_state_v0.1.0/tests/test_store.py`; P1/P2 report; implementation code | PARTIAL_AVAILABLE | Existing suite proves current semantics; deeper disturbance/interruption acceptance review is reserved for C0-3 |
| `AC-LIFE-03` | P2 non-destructive rollback | State store checkpoint/rollback | Create checkpoint, append later event, request rollback, verify history not truncated | `test_checkpoint_recovery_and_non_destructive_rollback` in state-store tests; P1/P2 report | AVAILABLE | Rollback returns references/request semantics; it is not full physical DB/file restoration |
| `AC-LIFE-04` | P2 migration invariant | State-store `migrate_instance`; AION/Astra migration wrappers | Positive migration changes instance ID; negative migration rejects stable ownership changes | state-store `test_migration_changes_only_runtime_instance_and_reuses_evidence`; `test_migration_cannot_change_individual_ownership`; AION/Astra lifecycle tests | AVAILABLE | Migration is Owner-governed and preserves stable lineage fields |
| `AC-LIFE-05` | Human Owner migration-evidence-reuse proposal | Environment evidence registry and migration PASS gate | Reuse unchanged fingerprint; create new evidence on change; reject FAIL evidence | state-store evidence reuse/change tests; `test_migration_requires_pass_environment_evidence`; migration implementation report | AVAILABLE | Current fingerprint design does not separately encode verifier/schema version; known future hardening, not silently claimed implemented |
| `AC-LIFE-06` | Event identity unique; evidence reusable; raw history append-only | State-store migration events and derived summary | Perform round-trip migrations; verify unique raw events but reused evidence IDs and derived summaries | `test_round_trip_migrations_keep_unique_events_but_reuse_two_evidence_records`; migration report | AVAILABLE | Summary is derived view only; raw events remain authoritative history |
| `AC-QA-01` | Existing repository Quality gate | `.github/workflows/quality.yml` / repository Quality workflow | Run on exact frozen target head for Python 3.11/3.12 | GitHub Actions workflow result tied to target head | OUT_OF_TREE_FINAL_EVIDENCE | Final run IDs belong in PR freeze/acceptance records, not branch contents |
| `AC-QA-02` | A/B Strong QA gate excluding separate coverage criterion | `.github/workflows/runtime-strong-qa.yml`; `scripts/run_runtime_strong_qa.sh` | mypy strict; wheel build; clean venv; `--no-index` local-wheelhouse install; cold import smoke | Strong QA script/workflow; GitHub Actions result tied to target head | AVAILABLE + OUT_OF_TREE_FINAL_EVIDENCE | Final workflow result must be checked on frozen head; branch file only defines/repeats the method |
| `AC-QA-03` | Pre-result >=80% branch-aware coverage threshold | `scripts/run_runtime_strong_qa.sh` | Run coverage separately for executable Runtime, individual state, AION Runtime, Astra Runtime with `--cov-branch --cov-fail-under=80` | Strong QA script lines/behavior; GitHub Actions coverage output on target head | AVAILABLE + OUT_OF_TREE_FINAL_EVIDENCE | Threshold is evaluated independently from QA-02 to avoid duplicate failure semantics |
| `AC-QA-04` | NASA objective-evidence / traceability principle; ISO quality-evaluation framing | This Evidence Index; criteria draft; crosswalk; implementation/test artifacts | During C, verify every BLOCKING/MAJOR criterion has traceable requirement, method and evidence | `docs/C0_ACCEPTANCE_EVIDENCE_INDEX_2026-08-08.md` plus cited artifacts | PARTIAL_AVAILABLE | This index provides navigation only; C must still judge sufficiency and results after freeze |
| `AC-DOC-01` | A documentation-convergence requirement; preserve historical evidence | Current and historical Reality Matrices; component READMEs | Compare current-state docs with historical pre-P0/P1/P2 matrix; confirm history not rewritten | `docs/history/reconciliation/RUNTIME_REALITY_MATRIX_2026-08-08.md`; `docs/RUNTIME_REALITY_MATRIX_CURRENT_2026-08-08.md`; READMEs | AVAILABLE | Final consistency review belongs to later C0 stage |
| `AC-DOC-02` | Operator/API boundary and non-promotion boundary | AION/Astra/Individual State READMEs; Current Matrix; PR body | Verify Python API vs operator-surface parity, deployment and canonical claims are separated | component READMEs; current Matrix; PR body | AVAILABLE | Final cross-document stale-state check belongs to later C0 consistency review |
| `AC-PROV-01` | Human Owner source-attribution separation rule | `docs/governance/CHANGE_PROVENANCE_RULES_v0.1.md`; implementation reports; PR body; criteria/crosswalk provenance | Review proposal/implementation/review/approval/state ownership/QA attribution separately | provenance rules; P0/P1/P2/migration/A+B/C0 docs; PR body | AVAILABLE | Git author/committer is not conceptual authorship evidence |
| `AC-PROV-02` | Current-cycle attribution: Codex contribution = NONE | Current implementation reports; C0 docs; PR body | Search/review current-cycle attribution statements for misattribution | P0/P1/P2/migration/A+B/C0 docs; PR body | AVAILABLE | Criterion is limited to this change cycle and does not rewrite unrelated historical Codex contributions |
| `AC-GOV-01` | Owner acceptance != merge != canonical promotion != deployment/IV&V | Criteria draft; Reality Matrix; PR governance-gate wording | Review C decision wording and subsequent records for boundary preservation | current Matrix; criteria draft; PR body; future Owner Decision Record | PARTIAL_AVAILABLE + FUTURE_C_EVIDENCE | Final proof requires the actual C Owner Decision Record |
| `AC-GOV-02` | ISO evaluator-role distinction; current limitation | Reality Matrix; criteria draft; PR body | Confirm no independent-IV&V claim unless separate independent evidence exists | current Matrix; criteria draft; PR body; future decision record | PARTIAL_AVAILABLE + FUTURE_C_EVIDENCE | Current state is explicitly `INDEPENDENT_IVV = NOT_ACHIEVED` |
| `AC-GOV-03` | Anti-hindsight/change-control rule | AH-01..AH-07 in criteria draft; future C decision/CAPA records | If failure occurs in C, inspect whether criterion remained visible and any change used documented impact/change control | criteria draft now; C log/NCR/CAPA if needed later | FUTURE_C_EVIDENCE | Cannot be fully evidenced before C because it governs how C handles discovered failures |

## Coverage summary

Current candidate criteria indexed: **26**.

Evidence navigation outcome:

- every current criterion has at least one identified source and review/evidence path;
- engineering criteria point to concrete implementation/tests where available;
- governance/document criteria point to documentary review artifacts;
- exact frozen-head workflow results are intentionally deferred to out-of-tree PR records;
- criteria whose decisive evidence can only exist during C are marked `FUTURE_C_EVIDENCE` rather than pre-judged.

## Important evidence limitations discovered while indexing

1. `AC-LIFE-02` recoverability has current semantic tests and implementation evidence, but deeper disturbance/interruption scenarios remain a later C0 review topic; this index does not silently treat that future review as complete.
2. Checkpoint/recovery/rollback evidence is metadata/reference recovery and lineage-integrity evidence. It does not prove full physical restoration of arbitrary external DB/files.
3. Environment-evidence fingerprinting currently omits separately versioned verifier/evidence-schema semantics; this is a known future-hardening limitation and is not represented as implemented.
4. Final workflow run IDs, criteria freeze, and Owner decision evidence are intentionally out-of-tree so recording them cannot mutate the target head.
5. This index does not substitute for the later authoritative Remaining HOLD reference or final C0 consistency review.

## C0-1 completion statement

`C0-1_ACCEPTANCE_EVIDENCE_INDEX = COMPLETE_CANDIDATE`

This means the current acceptance criteria have a navigable requirement/evidence map suitable for later C review preparation.

It does **not** mean:

- criteria are frozen;
- evidence has been accepted as sufficient;
- any criterion is PASS;
- C has started;
- merge or canonical promotion is authorized.

## Provenance

- Decision to process only C0-1 at this stage: `AUTHORIZED_BY = HUMAN_OWNER`.
- Evidence-index structure, repository mapping and this artifact: `IMPLEMENTED_BY = CHATGPT`.
- Existing engineering implementation evidence: per previously recorded change provenance.
- Automated workflow execution evidence: `GITHUB_ACTIONS` when run.
- `CODEX_CONTRIBUTION_THIS_CHANGE = NONE`.
- Owner acceptance decisions: `NOT_STARTED`.
