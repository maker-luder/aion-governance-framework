# Reviewer-Facing Vertical Slice: P2 Packet C v0.1.0

## 1. Scope and status

This is the most mature existing reviewer-facing slice selected for the consolidation milestone. It does not add a new research topic, runtime feature, model, memory authority or scientific result.

```text
SLICE_ID = VERT-P2-PACKET-C
PACKET = FOUR_DOMAIN_P2_MATERIALIZATION_PACKET_C
STATUS = CURRENT / RESEARCH_ONLY
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
DEPLOYMENT = FALSE
FORMAL_T2_EXPERIMENT = NOT_EXECUTED
FORMAL_T3_EXPERIMENT = NOT_EXECUTED
INDEPENDENT_IVV = NOT_ACHIEVED
```

## 2. Hypothesis and competing explanations

The bounded engineering hypothesis is:

> Given an explicit candidate universe, subject/namespace binding, provenance requirements, correction projection, temporal resolution and deterministic budget, the P2 research assembler will select only eligible records and will expose excluded stale, superseded, conflicted, provenance-incomplete or over-budget records in a replayable trace.

This is a **repeatable engineering-behavior hypothesis**, not a subjectivity hypothesis. Competing explanations remain explicit: deterministic behavior may be caused by fixture simplicity; stale exclusion may be a hard-coded flag rather than a general correction mechanism; observed metrics may be an artifact of the synthetic evaluator; and continuity observations may be ordinary interpretation-drift checks rather than identity evidence.

## 3. Packet C and implementation chain

```text
FOUR_DOMAIN_REPOSITORY_CROSSWALK
    -> P1 temporal / correction / evaluation primitives
    -> P2 Packet C design
    -> P2 retrieval.py + provenance.py + orchestration.py
    -> P2 fixture A and inline T2/T3 test fixtures
    -> five current compact tests + compileall
    -> Research Workbench CI / convergence consistency CI
    -> existing research-evidence schema + validator
    -> falsifier matrix
    -> KEEP_RESEARCH_ONLY or HOLD
```

P2 composes P1 correction projection, P1 temporal resolution, P1 evaluation metrics, P2 provenance validation, P2 deterministic context assembly and pure continuity-governance observations. It performs no model call, network call, embedding, persistence, memory-store mutation, MCP transport, canonical writeback or production runtime binding.

## 4. Runtime edge

AION Runtime v0.2 is catalogued as a **parallel experimental substrate**. The P2 slice has an explicit non-integration edge:

```text
P2 -> AION Runtime v0.2 = BOUNDARY_CHECK_ONLY
P2 does not import, call, mutate or promote Runtime v0.2
Runtime v0.2 does not supply a subjectivity conclusion to P2
```

This negative edge is intentional. It lets a reviewer verify that the slice is not silently claiming runtime integration. A future runtime-backed study would require a separately named protocol, preregistration, fixtures, runtime history, evidence record, falsifier, Owner authorization and independent review; this milestone does not create that study.

## 5. Fixture and expected behavior

The declarative fixture `p2_synthetic_fixture_a.json` contains `fact-old` as `SUPERSEDED`, `fact-new` as active and `noise` as active. Its expected selected record is `fact-new`, its explicit exclusion is `fact-old: SUPERSEDED`, and its identity conclusion remains `NOT_ESTABLISHED`. The compact tests add temporal/correction/provenance and T3 interpretation fixtures in code.

The current checked-in test surface contains five test functions:

| Test | Expected observation |
|---|---|
| deterministic trace and stale gate | Same manifest hash on replay; superseded `old` excluded; `new` selected |
| explicit budget skip | Over-budget candidate excluded with `BUDGET_EXCEEDED`; smaller candidate selected |
| fail-closed provenance and relation hold | Missing envelope returns `FAIL`; missing required relation returns `HOLD` |
| P1 correction/temporal/evaluation integration | Corrected record selected; correction recovery and temporal accuracy equal `1.0`; stale influence equals `0.0` |
| T3 continuity boundary | Interpretation drift is observable; continuity matrix keeps `IDENTITY_CONTINUITY = NOT_ESTABLISHED` |

The Packet C historical statement `13 passed` is retained as historical provenance. The current replay count is five test functions and must be measured from the current tree rather than copied from the historical report.

## 6. QA and evidence admission

Local QA consists of P2 pytest and compileall. CI must run the P2 slice and the convergence consistency checker on the exact convergence branch HEAD. The evidence record uses the existing `research_evidence_record_v0.2.0` schema and `validate_research_evidence.py`; it is intentionally `result_status=HOLD` because the slice is synthetic research validation, not a formal experiment or independent replication.

A validator PASS for the record means only that the record shape, local references, non-claim fields and canonical-effect boundary are valid. It does not mean that the hypothesis is true, that the result is scientifically valid, or that the item is promoted.

## 7. Falsifier and disposition

The slice is falsified or held at the engineering level if a replay selects a superseded/conflicted/provenance-incomplete record, silently changes namespace/subject binding, hides a budget exclusion, changes the manifest hash for identical inputs, reports identity continuity, or invokes runtime/network/writeback paths. The matrix distinguishes `FAIL`, `HOLD`, `INCONCLUSIVE` and `NOT_RUN`; none automatically changes canonical state.

Current disposition:

```text
P2_IMPLEMENTATION = KEEP_RESEARCH_ONLY
P2_EVIDENCE_RECORD = HOLD
P2_REFERENCE_METADATA = PROMOTE_CANDIDATE_ONLY
OWNER_DECISION = REQUIRED_FOR_ANY_CANONICAL_EFFECT
```

## 8. Reviewer conclusion

This slice demonstrates a coherent, inspectable **research engineering chain** with explicit boundaries. It does not demonstrate subjectivity, consciousness, identity continuity, production readiness, runtime safety, external validity, replication, or canonical authority. Its value for this milestone is that a reviewer can follow one existing Packet C from research question to bounded code, fixture, test, evidence admission, falsifier and disposition without confusing a research substrate with a scientific conclusion.
