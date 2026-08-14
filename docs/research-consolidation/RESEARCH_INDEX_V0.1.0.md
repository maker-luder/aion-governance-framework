# AION Research Index v0.1.0

> **Purpose:** This index consolidates the existing AION research branch without adding a research question, feature, model, runtime authority, or scientific conclusion. It is a reviewer-facing navigation and status artifact for the independent convergence branch.

```text
INDEX_STATUS = CURRENT / RESEARCH_ONLY
INDEX_BRANCH = engineering/aion-research-consolidation-literature-grounding-readiness-20260814
INDEX_BASE = review/four-domain-research-materialization@858442a3ec2439398d188779f4309397bd4926b2
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
PROMOTION_EXECUTION = NOT_PERFORMED
```

## 1. Status vocabulary

`CURRENT` means the artifact is the current branch-authoritative surface for the claim or navigation purpose described. `SUPERSEDED` means a later artifact is authoritative for the same purpose while the earlier artifact remains retained. `HISTORICAL` means the artifact records an earlier state, review, or result and must not be used as current authority. `HOLD` means the artifact or claim is retained but cannot advance because a required source, validation, owner decision, or contract is missing. `REJECT` means the proposed interpretation is not admissible under the standing evidence architecture. Status does not imply scientific truth.

`PROMOTE` is a recommendation for a future Owner-controlled canonical promotion batch; it does not perform promotion. `KEEP_RESEARCH_ONLY` retains an item in the research branch. `HOLD` prevents disposition until the named blocker is resolved.

## 2. Current change-level provenance

The current convergence inventory and evidence-admission implementation use a separate change-level provenance record. `HUMAN_OWNER` is the proposal and authority boundary; `CHATGPT` is architecture/review input; `MANUS` is the convergence implementation and validation actor; and `OWNER_APPROVAL` remains `PENDING`. None of these role records grants canonical authority or changes the historical source attribution.

The original P2 provenance and authorship meaning remain preserved. The current change record does not attribute the historical P2 implementation to Manus and does not rewrite the original P2 agents or historical test-count statement.

## 3. Current artifact and claim inventory

| ID | Kind | Artifact or claim | Status | Disposition | Source of truth / blocker |
|---|---|---|---|---|---|
| `IDX-001` | governance | This research index and its machine-readable companion | CURRENT | PROMOTE | Owner decision remains required; no canonical effect performed |
| `IDX-002` | governance | Root research-branch standing status | CURRENT | KEEP_RESEARCH_ONLY | `RESEARCH_BRANCH_STATUS.md` |
| `IDX-003` | method | Whitepaper-derived evidence architecture is primary | CURRENT | KEEP_RESEARCH_ONLY | `WHITEPAPER_WEB_BRANCH_RECONCILIATION_2026-08-12.md` and status file |
| `IDX-004` | method | `v0.14.23` stable/frozen whitepaper integration baseline | CURRENT | KEEP_RESEARCH_ONLY | Local retained whitepaper lineage; not a release authorization |
| `IDX-005` | candidate | `v0.14.24` internal research candidate | CURRENT | HOLD | It does not automatically supersede `v0.14.23` or promote itself |
| `IDX-006` | method | Four-Domain construct → LLM question → engineering operation → governance control mapping | CURRENT | KEEP_RESEARCH_ONLY | `FOUR_DOMAIN_REPOSITORY_CROSSWALK.md` |
| `IDX-007` | implementation | P1 temporal/correction/evaluation research primitives | CURRENT | KEEP_RESEARCH_ONLY | P1 package and `P1_MATERIALIZATION_PACKET_B.md` |
| `IDX-008` | implementation | P2 Packet C deterministic retrieval, provenance and T2/T3 orchestration | CURRENT | KEEP_RESEARCH_ONLY | P2 source, fixture and tests |
| `IDX-009` | fixture | P2 synthetic fixture A | CURRENT | KEEP_RESEARCH_ONLY | `research-labs/four-domain-p2-materialization_v0.1.0/fixtures/p2_synthetic_fixture_a.json` |
| `IDX-010` | test | P2 compact test surface, five test functions | CURRENT | KEEP_RESEARCH_ONLY | `tests/test_p2_compact.py` |
| `IDX-011` | evidence | P2 evidence-admission record | CURRENT | HOLD | `schemas/research_evidence_record_v0.2.0.schema.json`; no formal experiment and no IV&V |
| `IDX-012` | falsifier | P2 falsifier matrix: stale/superseded/conflict/provenance/budget/identity-boundary failures | CURRENT | KEEP_RESEARCH_ONLY | This convergence package plus P2 tests |
| `IDX-013` | historical validation | Original Packet C report of 13 passed | HISTORICAL | KEEP_RESEARCH_ONLY | Retained in Packet C with current five-test reconciliation |
| `IDX-014` | implementation | P3 resilience Packet C and its provenance/authority non-amplification invariants | CURRENT | KEEP_RESEARCH_ONLY | P3 packet; not selected as the primary vertical slice |
| `IDX-015` | implementation | P5 hypothesis lifecycle, disagreement, replication registry and convergence cap | CURRENT | KEEP_RESEARCH_ONLY | P5 README and full-run fixture |
| `IDX-016` | runtime substrate | AION Runtime v0.2 research candidate | CURRENT | KEEP_RESEARCH_ONLY | Runtime README and focused CI; P2 has an explicit non-integration boundary |
| `IDX-017` | language substrate | G1 Language Core candidate | CURRENT | KEEP_RESEARCH_ONLY | G1 README, governance and traceability; proposals remain NOT_STARTED / QA_HOLD |
| `IDX-018` | governance | Existing Research Scope Lock | CURRENT | KEEP_RESEARCH_ONLY | `scripts/check_research_scope_lock.py`; not recreated here |
| `IDX-019` | admission | Existing research evidence validator and schema | CURRENT | PROMOTE | Existing validator is reused, not replaced; Owner must decide canonical destination |
| `IDX-020` | external intake | Kimi project review intake | CURRENT | KEEP_RESEARCH_ONLY | Discovery provenance only; it is not verified repository fact |
| `IDX-021` | external source | Primary-source literature crosswalk | CURRENT | PROMOTE | Every entry has source-specific claim label; AION transformations remain interpretations |
| `IDX-022` | external project | Aura repository description | CURRENT | KEEP_RESEARCH_ONLY | Primary repository checked; no code copied |
| `IDX-023` | external project | TCAS repository and paper materials | CURRENT | KEEP_RESEARCH_ONLY | Primary repository checked; missing O/M streams keep credence withheld |
| `IDX-024` | external project | The Consciousness AI repository | CURRENT | KEEP_RESEARCH_ONLY | Speculative architecture; metrics explicitly not proof |
| `IDX-025` | external project | Qualia-Simulator repository | CURRENT | KEEP_RESEARCH_ONLY | Speculative taxonomy only; no qualia evidence |
| `IDX-026` | external project | AIsysTesting, aIware, mrivasperez/consciousness and redirected Atom leads | HOLD | HOLD | Primary repository/artifact/license verification incomplete for this cycle |
| `IDX-027` | external literature | Metacognition, self-verification and memory benchmark sources | CURRENT | KEEP_RESEARCH_ONLY | Official/arXiv/venue pages checked; no AION replication |
| `IDX-028` | stale generated evidence | Older C0 traceability snapshot bound to an older head | SUPERSEDED | KEEP_RESEARCH_ONLY | It remains historical and cannot be current evidence for this branch |
| `IDX-029` | historical handoff | Earlier whole-system v2 review handoff | HISTORICAL | KEEP_RESEARCH_ONLY | Different review branch and old merge base |
| `IDX-030` | interpretation | Any claim that Four-Domain and G1 are the same scientific source or that G1 establishes subjectivity | REJECT | HOLD | Conflicts with whitepaper-primary architecture and G1 non-claims |
| `IDX-031` | interpretation | Any first/only/unprecedented claim based only on Kimi or a repository README | REJECT | HOLD | Primary-source and independent-evidence burden not met |
| `IDX-032` | interpretation | Any test/CI pass treated as subjectivity, consciousness, identity or canonical proof | REJECT | HOLD | Standing locks: `TEST_PASS != THEORY_CONFIRMATION` and `CI_SUCCESS != PROMOTION` |
| `IDX-033` | change-level provenance | Current final-review provenance record | CURRENT | PROMOTE | Separates Human Owner proposal/authority, ChatGPT architecture/review, Manus implementation and Owner approval PENDING |
| `IDX-034` | evidence change provenance | P2 evidence-admission change-level provenance block | CURRENT | HOLD | Additive convergence record; historical P2 provenance/authorship remains preserved |

## 3. Four-Domain ↔ G1 resolution

Four-Domain is the **research-method and evidence-question layer**. It maps a human construct into an LLM question, an engineering operation, and a governance control, with the whitepaper evidence architecture as the primary scientific method. G1 is a **language capability research substrate** below AION/Astra. G1 can provide a candidate language-processing component and its QA/admission machinery, but its own governance contract denies identity, subjectivity, memory, tool, release and canonical authority.

Therefore the dependency direction is not `Four-Domain -> G1 -> subjectivity`. It is:

```text
WHITEPAPER_PRIMARY_METHOD
    -> FOUR_DOMAIN_RESEARCH_QUESTION / EVIDENCE_SURFACE
    -> bounded research substrate(s), including P1/P2/P3/P5 and optionally G1/runtime
    -> fixtures / tests / evidence admission / falsifier review
    -> human review disposition
```

G1 is a **parallel enabling substrate** that may be evaluated under the Four-Domain method. Four-Domain does not require G1 for its method, and G1 does not supply a subjectivity conclusion to Four-Domain. The current repository contains no authorized Four-Domain↔G1 runtime integration edge.

## 4. Selected reviewer-facing vertical slice

The selected slice is **P2 Packet C deterministic context assembly and provenance-gated T2/T3 synthetic orchestration** because it is the most concrete existing Packet C with an executable research implementation, declarative fixture, compact tests, P1 dependencies, continuity boundary, and explicit no-runtime/no-canonical boundary.

The runtime link is intentionally an **evidence boundary**, not an integration claim. AION Runtime v0.2 is catalogued as a parallel experimental substrate and the slice machine-checks that P2 does not silently depend on or mutate it. This closes the reviewer-facing chain without inventing production integration:

```text
P2 hypothesis / Packet C
    -> P2 retrieval + provenance + orchestration source
    -> P1 correction / temporal / evaluation dependencies
    -> P2 fixture A
    -> P2 compact tests + compile check + research CI
    -> existing research-evidence admission record (HOLD / canonical NONE)
    -> explicit P2 falsifier matrix
    -> KEEP_RESEARCH_ONLY / HOLD disposition
```

## 5. Promotion-readiness interpretation

The first candidate promotion batch is limited to **navigation and governance metadata**: this index, source-of-truth map, dependency graph, supersession map, literature crosswalk, promotion matrix, and their consistency checks. No scientific claim, runtime, model, memory state, G1 proposal, whitepaper candidate, or external project is automatically promoted. The evidence record remains `HOLD` because no formal experiment, independent replication or Owner acceptance exists.

## 6. Non-negotiable boundary

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
MAIN_MERGE = PROHIBITED
NEW_RESEARCH_TOPIC = NONE
NEW_FEATURE = NONE
NEW_MODEL = NONE
KIMI_REVIEW = DISCOVERY_ONLY
TEST_PASS != SCIENTIFIC_VALIDATION
CI_SUCCESS != CANONICAL_PROMOTION
```
