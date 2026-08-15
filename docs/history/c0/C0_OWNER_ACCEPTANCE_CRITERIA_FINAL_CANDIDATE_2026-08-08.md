# C0 Owner Acceptance Criteria — FINAL CANDIDATE — 2026-08-08

## Status

- `STATUS = FINAL_CANDIDATE_NOT_FROZEN`
- `DERIVED_FROM = C0_OWNER_ACCEPTANCE_CRITERIA_DRAFT_2026-08-08.md`
- `C0_3_RECOVERABILITY_REVIEW = INCORPORATED`
- `C_EXECUTION = NOT_STARTED`
- `OWNER_ACCEPTANCE = NOT_DECIDED`
- `CRITERIA_FREEZE = NOT_PERFORMED`
- `MAIN_MERGE = NOT_PERFORMED`
- `CANONICAL_EFFECT = NONE`
- `DEPLOYMENT = FALSE`
- `INDEPENDENT_IVV = NOT_ACHIEVED`
- `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`

This is the proposed criterion set to be frozen after C0-4 consistency review and final target-head QA. The earlier draft is preserved as historical evolution evidence.

## Anti-hindsight controls

- `AH-01`: no historical backdating of criteria.
- `AH-02`: criterion basis must come from pre-existing requirements/invariants/boundaries, external public calibration, or pre-freeze NCR/CAPA findings.
- `AH-03`: known PASS results are evidence, not criterion generators.
- `AH-04`: numeric thresholds require pre-result establishment or separate/external rationale; the existing `>=80%` branch-aware coverage gate qualifies.
- `AH-05`: Human Owner may approve criteria and later perform Owner acceptance, but role concentration is disclosed and is not independent evaluation/IV&V. Freeze is recorded outside branch contents against exact target head and exact criterion blob.
- `AH-06`: no silent weakening/removal/reclassification after freeze merely to obtain acceptance; changes require reason, provenance, impact analysis, change control, Owner review and affected re-evaluation.
- `AH-07`: a later target-head change triggers impact analysis. Affected criteria are re-evaluated; unaffected evidence may be reused only when non-impact is traceable. Uncertain/high-impact changes expand revalidation conservatively.

`HEAD_CHANGED != FULL_REVIEW_AUTOMATICALLY_REQUIRED`

`HEAD_CHANGED = IMPACT_ANALYSIS_REQUIRED`

## Result vocabulary during C

Each criterion receives exactly one result only after freeze and C execution:

- `PASS`
- `FAIL`
- `HOLD`
- `N/A`

`HOLD != PASS`

`HOLD != FAIL`

Missing required evidence is not PASS.

## Severity

- `BLOCKING`: failure prevents `ACCEPTED_AS_MERGE_CANDIDATE`.
- `MAJOR`: unresolved failure requires CAPA/disposition and cannot be silently waived.
- `NON_BLOCKING_HOLD`: only when frozen scope explicitly permits deferral and no blocking boundary is violated.

## Final candidate acceptance criteria

| ID | Criterion | Basis | Required evidence | Severity |
|---|---|---|---|---|
| `AC-SCOPE-01` | Target contains only authorized P0/P1/P2, migration-evidence reuse, A/B stabilization, C0 corrective hardening, and necessary QA/docs fixes; no silent unrelated expansion. | Human Owner scope + acceptance planning | locked diff / changed files / reports | BLOCKING |
| `AC-SCOPE-02` | Deferred/unauthorized items remain closed unless separately authorized, as defined by the authoritative candidate HOLD register. | scope locks / stop lines | HOLD register + diff + Matrix | BLOCKING |
| `AC-ID-01` | AION Runtime rejects `agent_id != AION`; Astra Runtime rejects `agent_id != ASTRA`. | P0 identity binding | implementation + negative tests | BLOCKING |
| `AC-ID-02` | For a currently bound Runtime instance, admitted task context exactly matches bound context; cross-agent/instance/memory/event/canonical/genesis substitution fails closed. Owner-approved migration may establish a new current context whose only changed context field is `runtime_instance_id`; stable-lineage ownership remains unchanged. | P0/P2 | mismatch + migration tests | BLOCKING |
| `AC-ID-03A` | Shared mechanisms/genesis must not conflate AION/Astra agent, Runtime instance, memory stream, event lineage or canonical-state ownership; validated shared genesis root is permitted. | Twin invariant | Twin/runtime binding tests | BLOCKING |
| `AC-ID-03B` | Shared genesis/infrastructure must not be represented as evidence of shared identity, private memory, event life-history, consciousness or subject. | research non-inference | documentary review | BLOCKING |
| `AC-MEM-01` | Memory writes/recall derive ownership from bound Runtime context rather than caller-selected AION/Astra ownership fields. | P0 memory binding | integration tests | BLOCKING |
| `AC-EVT-01` | Persistent Runtime event lineages remain separate, append-only and bound to stable individual ownership. | P1 | state/lifecycle tests + schema/code | BLOCKING |
| `AC-EVT-02` | Event-lineage evidence is not represented as proof of consciousness, phenomenal continuity or established subjectivity. | research stop line | documentary review | BLOCKING |
| `AC-LIFE-01` | Restart/reopen of same individual context continues existing sequence/hash chain rather than silently starting new history. | P2 continuity | restart/reopen tests | BLOCKING |
| `AC-LIFE-02` | Recovery verifies complete event-lineage integrity and fails closed after event tampering/corruption. | P2 + recoverability disturbance calibration | tamper/corruption tests | BLOCKING |
| `AC-LIFE-02A` | Any checkpoint selected/exposed by recovery or rollback passes checkpoint-content integrity verification and is bound to a verified `runtime.checkpoint_created` lineage event. | C0-3 recoverability finding | checkpoint tamper tests + code | BLOCKING |
| `AC-LIFE-03` | Rollback is non-destructive to event history; selecting an older checkpoint does not erase later historical events. | P2 | rollback tests | BLOCKING |
| `AC-LIFE-04` | Runtime migration may change only `runtime_instance_id`; stable agent/memory/event/canonical/genesis ownership remains unchanged. | P2 migration invariant | positive/negative migration tests | BLOCKING |
| `AC-LIFE-04A` | Migration transition persistence is atomic as one paired `migrating_out -> migrated_in` state transition; a failed second transition write leaves no partial migration evidence. | C0-3 disturbance finding | simulated interruption/atomic rollback test | BLOCKING |
| `AC-LIFE-04B` | Unpaired, orphaned, or payload/context-mismatched migration transitions invalidate lineage recovery; success must not be silently inferred. | C0-3 disturbance finding | invalid-pair verification/recovery test | BLOCKING |
| `AC-LIFE-05` | Migration requires PASS source/target environment evidence; evidence reuse occurs only for unchanged fingerprint. | Human Owner evidence-reuse proposal | reuse/change/PASS-gate tests | BLOCKING |
| `AC-LIFE-06` | Repeated migrations remain unique raw append-only events even when environment evidence is reused; summaries remain derived and never replace/deduplicate/truncate history. | evidence-reuse + append-only invariant | round-trip/summary/raw history tests | BLOCKING |
| `AC-QA-01` | Standard repository Quality passes Python 3.11 and 3.12 on exact frozen target. | repository gate | target-head workflow | BLOCKING |
| `AC-QA-02` | Runtime Strong QA on exact target completes strict mypy, local wheel builds, clean venv, cold `--no-index` wheelhouse install, and cold import smoke. | A/B gate | target-head workflow/logs | BLOCKING |
| `AC-QA-03` | Each changed Runtime component in Strong QA satisfies pre-established branch-aware coverage `>=80%`. | pre-result threshold | target-head coverage | BLOCKING |
| `AC-QA-04` | Tests are not sole acceptance evidence; requirement→criterion→implementation→test/review→objective-evidence traceability exists for every blocking/major criterion. | NASA/ISO calibration | Evidence Index + addenda | BLOCKING |
| `AC-DOC-01` | Current docs describe current implementation while historical gap evidence remains preserved. | A convergence | current/historical docs | MAJOR |
| `AC-DOC-02` | Docs distinguish Python API capability from deferred operator parity and do not falsely claim deployment/canonical promotion/IV&V/subjectivity conclusions. | convergence/governance | cross-document review | BLOCKING |
| `AC-PROV-01` | Proposal, implementation, review, approval, state ownership and automated QA attribution remain separable; Git author/committer does not override conceptual provenance. | Human Owner attribution rule | provenance review | BLOCKING |
| `AC-PROV-02` | Current-cycle work is not misattributed to Codex where contribution is `NONE`. | current provenance | reports/PR review | BLOCKING |
| `AC-GOV-01` | Owner acceptance is not represented as merge, canonical promotion, deployment approval or independent IV&V. | governance invariants | decision/Matrix/PR wording | BLOCKING |
| `AC-GOV-02` | Independent IV&V remains `NOT_ACHIEVED` absent genuinely independent verification/validation evidence. | evaluator-role distinction | Matrix/decision record | BLOCKING |
| `AC-GOV-03` | Blocking/major failures discovered during C remain visible as FAIL/HOLD/CAPA; criteria are not weakened solely to obtain acceptance. | anti-hindsight/change control | C log/CAPA if applicable | BLOCKING |

## Recoverability scope boundary

The recoverability criteria above establish integrity/atomicity/fail-closed conditions for the governed Runtime lineage and checkpoint references. They do **not** claim:

- full physical restoration of arbitrary external databases/files;
- autonomous self-healing;
- automatic canonical-state adjudication;
- deployment failover availability;
- RTO/RPO guarantees.

Those require separate requirements and are not silently inferred.

## C entrance conditions

C may begin only after:

1. C0-1 Evidence Index and recoverability evidence addendum are complete candidate artifacts;
2. C0-2 authoritative candidate HOLD register exists;
3. C0-3 recoverability review is complete candidate;
4. C0-4 consistency review reports no blocking C0 contradiction/missing trace;
5. exact intended target head has final standard Quality and Runtime Strong QA results;
6. Human Owner freeze record is created outside branch contents against that exact head and this exact criterion blob;
7. no branch-content change occurs after freeze.

## C exit outcomes

Permitted outcomes remain:

- `ACCEPTED_AS_MERGE_CANDIDATE`
- `ACCEPTED_WITH_HOLDS`
- `RETURN_FOR_CAPA`
- `REJECTED`

No C outcome automatically performs D merge or E canonical promotion.

## Provenance

- Need for public external calibration: `PROPOSED_BY = HUMAN_OWNER`.
- Authorization to complete C0-3 through C0-5 as closing batch: `AUTHORIZED_BY = HUMAN_OWNER`.
- Earlier anti-hindsight design, identity-criteria refinement, C0-3 recoverability criteria integration and this derived final candidate: `IMPLEMENTED_BY = CHATGPT`.
- Existing engineering implementation provenance remains separately recorded.
- `CODEX_CONTRIBUTION_THIS_CHANGE = NONE`.
- Criteria freeze: `PENDING_HUMAN_OWNER_FREEZE_RECORD`.
- C Owner acceptance: `NOT_STARTED`.
