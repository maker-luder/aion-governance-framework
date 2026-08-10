# External Source Crosswalk — Selective Memory Control v0.1.0

```text
COPY_POLICY = CLEAN_ROOM
THIRD_PARTY_CODE_COPIED = NO
THIRD_PARTY_BENCHMARK_RESULT_REUSED_AS_AION_RESULT = NO
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
```

This file records the public research and implementation sources that informed the
research question and mechanism decomposition. It does not transfer authorship.

| Source | Public license / venue | Mechanism used as stimulus | AION disposition |
|---|---|---|---|
| infinigence/Infini-Memory | Apache-2.0; arXiv:2606.10677 | maintainable memory, conflict/fact revision, metadata/evidence organization | clean-room revision lineage + provenance gates |
| zjunlp/LightMem | MIT; ICLR 2026 | modular write/retrieve/consolidate; bounded retrieval | clean-room modular selective retrieval |
| Yu et al., Agentic Memory (AgeMem) | ACL 2026 | explicit store/retrieve/update/summarize/discard operations | operation taxonomy only |
| Yan et al., Memory-R1 | ACL 2026 | ADD/UPDATE/DELETE/NOOP memory management | operation taxonomy only |
| mem0ai/mem0 | Apache-2.0 | mature explicit memory layer and evaluation ecosystem | implementation comparison only |

## Primary/public references

- https://aclanthology.org/2026.acl-long.981/
- https://aclanthology.org/2026.acl-long.583/
- https://github.com/infinigence/Infini-Memory
- https://github.com/zjunlp/LightMem
- https://github.com/mem0ai/mem0

## What was intentionally not imported

- vendor-specific storage backends;
- model API configuration;
- vector databases;
- reinforcement-learning policies;
- benchmark datasets or reported scores;
- autonomous memory-write authority;
- third-party prompts or source-code structure.

The first AION module uses deterministic, inspectable mechanics so each governance
property can be isolated in tests before any learned retrieval layer is introduced.
