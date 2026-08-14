# AION Promotion Readiness Matrix v0.1.0

> **This is a readiness recommendation, not a promotion operation.** `PROMOTE` means a candidate for a future Owner-controlled canonical metadata batch. `KEEP_RESEARCH_ONLY` means the item is useful and validated as research material but must remain outside canonical state. `HOLD` means the item cannot advance until the named blocker is resolved. `CANONICAL_EFFECT=NONE` for this entire branch.

## 1. Decision vocabulary

| Status | Meaning | Promotion implication |
|---|---|---|
| `CURRENT` | Current artifact or claim for its scoped purpose | May be reviewed for promotion, but only with explicit Owner approval |
| `SUPERSEDED` | Later scoped source is current; earlier record retained | Never promote as current authority; retain as historical navigation |
| `HISTORICAL` | Earlier dated record or prior-branch handoff | Retain for provenance; do not promote as current |
| `HOLD` | Source, evidence, validation, license, IV&V or Owner decision is incomplete | Do not promote |
| `REJECT` | Interpretation conflicts with standing method or non-claim boundary | Do not promote; retain only as rejected-boundary evidence |

## 2. Matrix

| ID | Artifact/claim | Status | Readiness | Disposition | Reason / required gate |
|---|---|---|---|---|---|
| `PR-001` | Research Index and machine-readable inventory | CURRENT | READY_FOR_OWNER_REVIEW | PROMOTE | Navigation/governance metadata only; canonical effect remains NONE |
| `PR-002` | Claim Dependency Graph | CURRENT | READY_FOR_OWNER_REVIEW | PROMOTE | Resolves Four-Domain↔G1 direction without adding authority |
| `PR-003` | Source-of-Truth Map | CURRENT | READY_FOR_OWNER_REVIEW | PROMOTE | Consistency metadata; no scientific conclusion |
| `PR-004` | External Literature Crosswalk | CURRENT | READY_FOR_OWNER_REVIEW | PROMOTE | Primary URLs and narrow claim labels are recorded; all AION translations remain bounded |
| `PR-005` | Supersession Map | CURRENT | READY_FOR_OWNER_REVIEW | PROMOTE | Preserves dates/history and prevents stale source reuse |
| `PR-006` | Promotion Readiness Matrix | CURRENT | READY_FOR_OWNER_REVIEW | PROMOTE | Governance metadata only; does not execute a promotion |
| `PR-007` | P2 Packet C vertical-slice navigation and boundary artifact | CURRENT | READY_FOR_OWNER_REVIEW | PROMOTE | Promotable only as a research metadata/reference link, not as runtime or scientific result |
| `PR-008` | Convergence consistency schema/checker/tests/CI wiring | CURRENT | READY_FOR_OWNER_REVIEW | PROMOTE | Machine-enforced repository consistency; no runtime authority |
| `PR-009` | P2 Packet C implementation | CURRENT | RESEARCH_ONLY_VALIDATED | KEEP_RESEARCH_ONLY | Synthetic research substrate; no formal experiment, runtime integration, canonical writeback or IV&V |
| `PR-010` | P2 fixture and five compact tests | CURRENT | RESEARCH_ONLY_VALIDATED | KEEP_RESEARCH_ONLY | Deterministic engineering evidence only; test pass is not theory confirmation |
| `PR-011` | P2 evidence-admission record | CURRENT | ADMITTED_SHAPE_HOLD | HOLD | Record shape can validate, but result is HOLD because formal experiment and independent validation are absent |
| `PR-012` | P2 falsifier matrix | CURRENT | RESEARCH_ONLY_VALIDATED | KEEP_RESEARCH_ONLY | Falsifier conditions are explicit; no automatic scientific judgment |
| `PR-013` | P1/P3/P5 research candidates | CURRENT | RESEARCH_ONLY_VALIDATED | KEEP_RESEARCH_ONLY | Existing bounded research implementations; no canonical effect |
| `PR-014` | AION Runtime v0.2 | CURRENT | RESEARCH_ONLY_CI_VERIFIED | KEEP_RESEARCH_ONLY | Experimental substrate, not deployed; no P2 integration edge |
| `PR-015` | G1 Language Core and registered proposals | CURRENT | QA_HOLD | KEEP_RESEARCH_ONLY | Proposals not started; no identity, subjectivity, memory, tool, release or canonical authority |
| `PR-016` | Whitepaper v0.14.23 stable/frozen baseline | CURRENT | REVIEWABLE_REFERENCE | KEEP_RESEARCH_ONLY | Stable research reference, not canonical promotion authorization |
| `PR-017` | Whitepaper v0.14.24 internal research candidate | CURRENT | OWNER_REVIEW_REQUIRED | HOLD | Candidate does not auto-supersede v0.14.23 or promote itself |
| `PR-018` | Kimi external project intake | CURRENT | DISCOVERY_ONLY | KEEP_RESEARCH_ONLY | Static external lead, not verified repository fact or replication |
| `PR-019` | Verified external primary sources | CURRENT | SOURCE_GROUNDED_REFERENCE | KEEP_RESEARCH_ONLY | External methodological evidence; not AION evidence |
| `PR-020` | Unverified additional external projects | HOLD | PRIMARY_SOURCE_GAP | HOLD | Repository/artifact/license verification incomplete |
| `PR-021` | Existing Scope Lock | CURRENT | EXISTING_GATE | KEEP_RESEARCH_ONLY | Already enforced; not recreated in this milestone |
| `PR-022` | Existing evidence schema/validator | CURRENT | READY_FOR_OWNER_REVIEW | PROMOTE | Existing admission infrastructure and canonical NONE invariant |
| `PR-023` | Older C0 traceability snapshot | SUPERSEDED | NOT_CURRENT | KEEP_RESEARCH_ONLY | Stale head and older acceptance program; retain as history |
| `PR-024` | Earlier v2 review handoff | HISTORICAL | NOT_CURRENT | KEEP_RESEARCH_ONLY | Different review branch and merge base |
| `PR-025` | Four-Domain and G1 are one scientific authority | REJECT | INADMISSIBLE | HOLD | Conflicts with G1 governance and whitepaper-primary architecture |
| `PR-026` | Any first/only/unprecedented claim from Kimi or README | REJECT | INADMISSIBLE | HOLD | Primary-source and independent-evidence burden not met |
| `PR-027` | Test/CI pass as subjectivity, identity, consciousness or canonical proof | REJECT | INADMISSIBLE | HOLD | Explicit standing non-claim violation |

## 3. First recommended canonical promotion batch

The first batch should contain **only reference and governance metadata**, after explicit Owner review and any repository policy approval:

```text
RESEARCH_INDEX_V0.1.0
CLAIM_DEPENDENCY_GRAPH_V0.1.0
SOURCE_OF_TRUTH_MAP_V0.1.0
EXTERNAL_LITERATURE_CROSSWALK_V0.1.0
SUPERSESSION_MAP_V0.1.0
PROMOTION_READINESS_MATRIX_V0.1.0
CONVERGENCE_CONSISTENCY_CHECKER_AND_TESTS
```

The batch must exclude all P2/P1/P3/P5 runtime-like research behavior, AION Runtime v0.2, G1 proposals, whitepaper v0.14.24, external repositories, unverified literature claims, evidence results, subjectivity/identity/consciousness interpretations, canonical memory, deployment configuration and any authority envelope.

## 4. Promotion blockers

Even the metadata batch remains `OWNER_DECISION_REQUIRED` until the Human Owner decides whether these reference artifacts belong in canonical state. Independent IV&V is not achieved. The P2 evidence record remains `HOLD`; there is no formal T2/T3 experiment, real runtime history, independent replication, validated individuation threshold or full authority semantics. The branch therefore reports **readiness**, not promotion.

## 5. Boundary

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
MERGE_MAIN = PROHIBITED
OWNER_APPROVAL = REQUIRED_FOR_ANY_PROMOTION
INDEPENDENT_IVV = NOT_ACHIEVED
```
