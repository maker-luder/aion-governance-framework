# P2 Materialization Packet C

## Status

```text
PACKET = FOUR_DOMAIN_P2_MATERIALIZATION_PACKET_C
BRANCH_SCOPE = review/four-domain-research-materialization
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
MAIN_BRANCH_EFFECT = NONE
FORMAL_T2_EXPERIMENT = NOT_EXECUTED
FORMAL_T3_EXPERIMENT = NOT_EXECUTED
```

## 1. Research gaps carried from the workbench

The four-domain workbench identified three immediately materializable gaps:

1. a query/context layer that returns candidate decisions, ranking evidence and exact selected context;
2. a bounded provenance projection that can fail closed before evidence is used;
3. a condition runner that composes retrieval, temporal/version resolution, correction and continuity evidence without claiming a formal experiment.

P2 implements those gaps as isolated research primitives.

## 2. Materialized primitives

### Retrieval trace

Implemented:

- deterministic candidate-universe hashing;
- subject/namespace isolation;
- explicit ineligibility reasons;
- explicit ranking basis;
- deterministic budget selection;
- context manifest fingerprint;
- no silent truncation of an item that exceeds remaining budget.

### Provenance completeness

Implemented:

- required-field validation;
- authority-status validation;
- source/evidence hash presence;
- relation validation;
- fail-closed result;
- completeness score for research measurement.

### T2/T3 synthetic orchestration

Implemented:

- P1 correction projection -> retrieval eligibility;
- P1 temporal resolver -> expected/current version observation;
- P1 evaluation harness -> retrieval/correction/stale/provenance metrics;
- existing continuity-governance functions -> T3 dimension observations;
- no model invocation and no runtime mutation.

## 3. Design choices

- No second recall policy is created. The P2 assembler consumes explicit candidate facts and research scores.
- No relationship text can create authority or selection priority.
- Missing provenance is a retrieval rejection, not a request to infer missing data.
- Superseded, withdrawn and unresolved-conflict records remain in the trace so exclusion is observable.
- Context ordering is deterministic and its fingerprint is reproducible from the same inputs.
- T3 continuity results remain engineering observations; identity continuity is not established.

## 4. External research translation

Public research inspected for this packet supports three engineering questions:

- LongMemEval-V2: can long history be converted into compact, attributable evidence for downstream answering?
- MemoryAgentBench / evolving-memory benchmarks: can long-range memory behavior be evaluated beyond simple retrieval?
- W3C PROV: can source, activity, agent, revision, derivation and invalidation relations be represented without collapsing them into authority?

External sources provide research concepts only. They do not authorize architecture, identity claims or canonical state.

## 5. Validation

The original packet record reported the following historical validation at materialization time:

```text
HISTORICAL_REPORTED_TEST_COUNT = 13 passed
HISTORICAL_COMPILEALL = PASS
```

The current checked-in test surface is smaller and is the source of truth for present replay:

```text
CURRENT_TEST_FUNCTION_COUNT = 5
CURRENT_EXPECTED_RESULT = 5 passed
CURRENT_COMPILEALL = PASS
```

The five current tests cover deterministic replay, stale/superseded exclusion, fail-closed provenance, explicit budget behavior, P1 correction/temporal/evaluation integration and T3 continuity-boundary checks. The historical count is retained as provenance and is not silently rewritten.

## 6. Attribution

- HUMAN_OWNER: authorized free growth and engineering implementation only on `review/four-domain-research-materialization`, with main explicitly prohibited.
- ChatGPT: public research inspection, P2 architecture, implementation, tests and this packet.
- Codex: earlier four-domain repository materialization and gap maps remain prior source artifacts; no new Codex implementation is asserted in this packet.
- JOINT: no new jointly authored scientific conclusion is asserted here.

## 7. Stop boundary

Promotion to main, formal experiment execution, runtime integration, persistent production storage, transport exposure and canonical writeback remain outside this packet.
