# Selective Memory Control — v0.1.0

Status: `RESEARCH_MODEL / CLEAN_ROOM / CANONICAL_EFFECT=NONE / MAIN_EFFECT=NONE`

This lab is an executable AION research module for **selective long-term memory control**.
It does not import a third-party memory framework and does not claim to reproduce any
external benchmark result.

## Why this module exists

The 2026-08-11 literature intake sharpened a core research question:

```text
MAXIMAL_MEMORY != MAXIMAL_CONTINUITY
```

A memory can be stored and retrievable while still being ineligible for the present
context because it is superseded, belongs to another namespace/domain/purpose, or lacks
the correct provenance/approval path.

The clean-room module therefore treats retrieval as a governed selection problem:

```text
stored record
    ↓
status gate
    ↓
namespace gate
    ↓
domain gate
    ↓
purpose gate
    ↓
query relevance
    ↓
retrieval trace
```

## Implemented mechanisms

`SelectiveMemoryStore` currently provides:

- explicit `ADD`, `REVISE`, `DISCARD`, and `RETRIEVE` operations;
- required `source_ref` and `approval_ref` on writes;
- immutable revision lineage through `supersedes`;
- default exclusion of superseded and discarded records;
- namespace, domain, and purpose isolation before relevance scoring;
- deterministic English/alphanumeric plus Chinese CJK token matching;
- auditable `RetrievalTrace` showing considered, blocked, and returned memories.

The relevance scorer is deliberately simple. It is not an embedding model and is not
presented as state of the art. The purpose of v0.1.0 is to isolate the memory-governance
mechanism before adding learned retrieval.

## Research locks

```text
STORED != CURRENT_CONTEXT_ELIGIBLE
RETRIEVABLE != RELEVANT
OLD_MEMORY != CURRENT_MEMORY
REVISION_HISTORY != SIMULTANEOUS_TRUTH
SOURCE_REF != APPROVAL_AUTHORITY
MEMORY_RECALL != IDENTITY_CONTINUITY
MEMORY_MODULE_UTILITY != SUBJECTIVITY
```

## External methodological stimuli

The design is a clean-room AION implementation informed by public work including:

- **Infini Memory** (Apache-2.0): topic-maintained memory, conflict/revision concerns,
  provenance-preserving evidence organization.
- **LightMem** (MIT): modular memory writing/retrieval/consolidation and bounded retrieval.
- **Agentic Memory / AgeMem** (ACL 2026): memory operations as explicit agent actions,
  including store, retrieve, update, summarize, and discard.
- **Memory-R1** (ACL 2026): explicit ADD / UPDATE / DELETE / NOOP management actions.
- **Mem0** (Apache-2.0): mature implementation reference for explicit memory operations.

No source code from those projects is copied into this lab. See
`docs/EXTERNAL_SOURCE_CROSSWALK.md`.

## Run

```bash
python -m pip install -e .
python -m compileall -q src
python -m pytest -q
python scripts/run_demo.py
```

Expected v0.1.0 local validation:

```text
8 passed
old superseded record = blocked
new corrected record = retrieved
```

## Provenance

- Human Research Owner: proposed using public modules/research as material that can be
  reconstructed into usable modules on `review/four-domain-research-materialization`.
- ChatGPT: searched public/academic sources, selected the clean-room selective-memory
  formulation, implemented the module, Chinese-compatible deterministic retrieval,
  revision/approval/provenance gates, tests, and demo.
- External authors/projects: methodological sources only; their code and experimental
  results remain theirs.
- Codex: no contribution to v0.1.0 unless separately documented.
