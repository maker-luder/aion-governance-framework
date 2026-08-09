# P2 Research Basis and Translation Boundary

## Public sources inspected on 2026-08-09

### LongMemEval-V2 (2026)

- arXiv: `2605.12493`
- Relevant idea: memory systems consume long environment histories and return compact
  evidence for downstream question answering.
- Translation: P2 records candidate-universe, selection and context-manifest evidence.
- Limit: this lab does not reproduce the benchmark or claim equivalent performance.

### LongMemEval (2024)

- arXiv: `2410.10813`
- Relevant abilities: information extraction, multi-session reasoning, temporal reasoning,
  knowledge updates and abstention.
- Translation: these remain evaluation dimensions; they do not become authority rules.

### MemoryAgentBench (2025)

- arXiv: `2507.05257`
- Relevant abilities: accurate retrieval, test-time learning, long-range understanding and
  selective forgetting under incremental multi-turn interactions.
- Translation: P2 keeps retrieval and exclusion behavior separately inspectable.
- Limit: no autonomous learning or forgetting mechanism is added.

### MemEvoBench (2026)

- arXiv: `2604.15774`
- Relevant observation: misleading/noisy memory accumulation can produce long-horizon
  behavioral drift.
- Translation: provenance failures, unresolved conflicts and stale states remain visible
  and fail closed in synthetic orchestration.
- Limit: this lab is not a safety benchmark implementation.

### Memora (2026)

- arXiv: `2604.20006`
- Relevant observation: long-term memory systems can continue using obsolete/invalidated
  memories; FAMA penalizes such behavior.
- Translation: P1 `stale_memory_influence` is retained and P2 excludes known superseded or
  withdrawn records while preserving exclusion evidence.

### W3C PROV-O

- W3C Recommendation, 2013: `https://www.w3.org/TR/prov-o/`
- Relevant concepts: Entity, Activity, Agent, derivation, attribution, revision and
  invalidation.
- Translation: P2 uses a small local provenance vocabulary.
- Limit: no RDF/OWL serialization and no PROV-O conformance claim.

### MCP specification 2026-07-28

- Official release note: `https://blog.modelcontextprotocol.io/posts/2026-07-28/`
- Relevant architecture fact: the protocol core is stateless; application state may use
  explicit handles rather than hidden transport session state.
- Translation: P2 keeps memory/context state at the application research layer.
- Limit: no MCP server, tool schema or transport is implemented here.

## Attribution

- **HUMAN_OWNER:** authorized continued free research/engineering on
  `review/four-domain-research-materialization` and explicitly prohibited changes to
  `main`.
- **ChatGPT:** selected this P2 materialization design, performed current public-source
  review, implemented the research code/tests and prepared this handoff.
- **Codex:** authored earlier repository-inspection/materialization artifacts that exposed
  several gaps reused as inputs here; Codex did not implement this P2 packet.
- **External sources:** supplied the research/standards concepts listed above.
