# Four-Domain P2 Materialization Lab v0.1.0

## Status

```text
MODULE_STATUS = RESEARCH_CANDIDATE
BRANCH_SCOPE = review/four-domain-research-materialization
MAIN_BRANCH_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
DEPLOYMENT_EFFECT = NONE
AUTOMATIC_WRITEBACK = NO
NETWORK_ACCESS = NONE
MODEL_CALLS = NONE
MCP_SERVER = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
PHENOMENAL_AFFECT = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

This lab materializes the P2 layer above the P1 temporal, correction and evaluation
primitives. It does not replace the repository recall gate, memory store, Writeback Gate,
continuity governance, runtime state, or any future transport.

## What is implemented

### 1. Retrieval Trace / Deterministic Context Assembly

`DeterministicContextAssembler` accepts an explicit candidate universe and produces:

- fail-closed subject and namespace gating;
- future-record, tombstone, supersession, withdrawal and conflict gating;
- provenance-gate enforcement;
- caller-supplied relevance / temporal / priority signals in integer basis points;
- explicit score-basis references;
- deterministic ordering and budget selection;
- per-candidate selection/exclusion reasons;
- candidate-universe and manifest SHA-256 fingerprints.

No embedding, semantic inference, hidden ranking signal, network call or writeback occurs.

### 2. Provenance Completeness Validator

`ProvenanceCompletenessValidator` validates a bounded evidence envelope containing
entity, subject, namespace, source, actor, activity, operation, time, hash and authority
status. It also supports research relations inspired by W3C PROV concepts:

- `DERIVED_FROM`
- `REVISION_OF`
- `ATTRIBUTED_TO`
- `INVALIDATED_BY`
- `PRIMARY_SOURCE`

This is **PROV-inspired**, not a PROV-O conformance claim or serializer.

### 3. T2 Synthetic Orchestration

`T2SyntheticOrchestrator` composes:

```text
P1 correction projection
        +
P2 provenance validation
        +
P2 deterministic context assembly
        +
P1 temporal resolution
        +
P1 evaluation harness
```

The correction ledger can mark superseded / withdrawn / unresolved-conflict records before
selection. Provenance failures are converted into a fail-closed retrieval gate. The final
P1 observation is generated from the selected evidence manifest.

### 4. T3 Synthetic Orchestration

`T3SyntheticOrchestrator` adds the existing pure continuity-governance checks to ordered T2
episodes. It records interpretive observations and correction-recovery evidence while
preserving the repository continuity matrix's `IDENTITY_CONTINUITY = NOT_ESTABLISHED`
boundary.

## Why context assembly is evidence-bearing

LongMemEval-V2 frames long-term memory as history ingestion followed by compact evidence
gathering for downstream answering. This lab therefore treats the selected context as an
inspectable evidence manifest rather than an opaque prompt-construction side effect.

Recent long-horizon memory benchmarks also show that obsolete or contaminated memories can
remain behaviorally influential. P2 therefore keeps stale/superseded/conflicted records
visible in the trace even when they are excluded from context.

## Monorepo research dependencies

P2 intentionally reuses, rather than duplicates:

- `research-labs/four-domain-p1-materialization_v0.1.0`
- `components/continuity_governance_v0.1.0`

The `pyproject.toml` test path binds those local research/component sources. There is no
published runtime dependency or deployment integration.

## Validation

From this directory:

```powershell
python -m pytest -q
```

## Stop boundary

Not implemented or authorized here:

- production retrieval facade;
- direct memory-store mutation;
- canonical writeback;
- runtime integration;
- model calls;
- embeddings or RAG service;
- persistent experiment database;
- MCP tool/server transport;
- Teacher binding;
- identity or subjectivity conclusions.
