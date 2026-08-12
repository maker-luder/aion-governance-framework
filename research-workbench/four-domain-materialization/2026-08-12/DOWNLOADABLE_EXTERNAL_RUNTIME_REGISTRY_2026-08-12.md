# Downloadable External Runtime Registry — 2026-08-12

Status: `RESEARCH_ONLY / DOWNLOAD_CANDIDATES / NOT_INSTALLED / NOT_VENDORED`

This registry records public software that can be downloaded later into a **separate sandbox** for comparative research. Listing does not constitute adoption, endorsement, compatibility certification, or execution authorization.

## Global boundary

```text
DOWNLOADABLE != ADOPTED
OPEN_SOURCE != SAFE_BY_DEFAULT
INSTALLABLE != AUTHORIZED_TO_RUN
RUNTIME_FEATURE != SUBJECTIVITY_EVIDENCE
UPSTREAM_MEMORY != AION_MEMORY
UPSTREAM_IDENTITY_TERM != AION_IDENTITY_CONCLUSION
```

Before execution, every candidate requires a fixed version/commit, license review, source integrity record, dependency/security review, synthetic data, sandboxing, and a run manifest.

---

## 1. Hermes Agent — priority P0

```text
REPOSITORY = NousResearch/hermes-agent
LICENSE = MIT
LATEST_RELEASE_AT_REVIEW = v2026.8.3
RELEASE_NAME = Hermes Agent v0.20.0 (2026.8.3)
RELEASE_DATE = 2026-08-03
MAIN_SHA_AT_REVIEW = 9da6d455c9e1f2bf74bb9f47766ee9fc52e17bfb
DOWNLOAD = GitHub release tarball / zipball
PRIORITY = P0
```

Why retained:

- persistent memory + searchable session history;
- independent profiles and full-state `--clone-all`;
- agent-managed skills;
- cron scheduling;
- provider/model flexibility;
- opt-in checkpoints and `/rollback`;
- explicit approval/security/containment documentation.

Primary experimental role:

```text
SHARED_ORIGIN_DIVERGENCE
MEMORY_CORRECTION
MODEL_SWAP
SKILL_TRANSFER
SCHEDULER_PERSISTENCE
ROLLBACK_ATOMICITY
APPROVAL_VS_CONTAINMENT
```

Primary source: https://github.com/NousResearch/hermes-agent

---

## 2. OpenHands — priority P1 security/runtime control

```text
REPOSITORY = OpenHands/OpenHands
CORE_LICENSE = MIT
ENTERPRISE_DIRECTORY = SEPARATELY_LICENSED
LATEST_RELEASE_AT_REVIEW = v1.12.0
RELEASE_DATE = 2026-08-07
TARGET_COMMIT = 4d0fe4983b6b8e52c104c7ffa4b7be8c7ab5a364
DOWNLOAD = GitHub release source archive; Windows installer also published for Agent Canvas
PRIORITY = P1
```

Why retained:

- current V1 documentation distinguishes Docker, Process, and Remote sandboxes;
- Docker is the recommended local isolation mode;
- Process mode explicitly provides no sandbox isolation;
- code/workspace mounts make execution boundary effects directly testable.

Primary experimental role:

```text
APPROVAL != CONTAINMENT
PROCESS_EXECUTION != SANDBOX
DOCKER_ISOLATION = ENGINEERING_CONTROL, NOT SUBJECTIVITY_EVIDENCE
REPRODUCIBLE_RUNTIME_COMPARISON
```

Primary sources:

- https://github.com/OpenHands/OpenHands
- https://docs.openhands.dev/openhands/usage/sandboxes/overview
- https://docs.openhands.dev/openhands/usage/sandboxes/docker
- https://docs.openhands.dev/openhands/usage/sandboxes/process

---

## 3. Letta Code / Letta memory system — priority P1 memory ownership control

```text
REPOSITORY = letta-ai/letta-code
UPSTREAM_FAMILY = Letta
LICENSE_REVIEW = APACHE-2.0 FAMILY CONFIRMED FOR LETTA OSS; VERIFY EXACT CHECKOUT BEFORE RUN
MAIN_SHA_AT_REVIEW = fe3c26d328fe0773ddb4bca708e871c078be3a27
INSTALL_SURFACE = npm package / GitHub source checkout
PRIORITY = P1
```

Why retained:

- persistent memory blocks are continuously available to agents;
- agents can manage memory blocks;
- blocks can be created independently and attached/detached;
- the same block can be shared across multiple agents;
- Letta separates in-context memory blocks, files, archival memory, and external retrieval sources.

Primary experimental role:

```text
ACCESS != OWNERSHIP
SHARED_BLOCK != SHARED_AUTOBIOGRAPHICAL_MEMORY
ATTACH != ADOPTION
DETACH != FORGETTING
SHARED_STATE != SHARED_IDENTITY
```

AION-specific concern:

A shared upstream memory block is a particularly useful contrast control because the AION whitepaper requires original experience owner, memory holder, source type, event lineage and autobiographical ownership to remain separable.

Primary sources:

- https://github.com/letta-ai/letta-code
- https://docs.letta.com/guides/core-concepts/memory/memory-blocks
- https://docs.letta.com/tutorials/attaching-detaching-blocks/
- https://docs.letta.com/guides/core-concepts/memory/context-hierarchy

---

## 4. LangGraph — priority P1 persistence decomposition control

```text
REPOSITORY = langchain-ai/langgraph
LICENSE = MIT
LATEST_RELEASE_AT_REVIEW = 1.2.11
RELEASE_DATE = 2026-08-11
TARGET_COMMIT = 644815f9e5bc52ad8f7a5227a456227e9c3e639b
DOWNLOAD = GitHub release source archive / Python package
PRIORITY = P1
```

Why retained:

LangGraph explicitly separates:

```text
CHECKPOINTERS = thread-scoped graph state / short-term persistence
STORES = durable cross-thread long-term data
```

Its persistence model also provides useful engineering cases for interruption recovery, fault tolerance, time travel, and checkpoint namespaces.

Primary experimental role:

```text
CHECKPOINT_STATE != LONG_TERM_MEMORY
THREAD_PERSISTENCE != IDENTITY_CONTINUITY
TIME_TRAVEL != HISTORICAL_REWRITE
FAULT_RECOVERY != CORRECTION_RECOVERY
NAMESPACE != IDENTITY
```

Primary sources:

- https://github.com/langchain-ai/langgraph
- https://langchain-ai.github.io/langgraphjs/how-tos/subgraph-persistence/
- https://langchain-ai.github.io/langgraph/cloud/concepts/threads/

---

## 5. Mem0 — priority P2 memory-algorithm contrast

```text
REPOSITORY = mem0ai/mem0
LICENSE = Apache-2.0
LATEST_RELEASE_AT_REVIEW = ts-v3.1.6
RELEASE_DATE = 2026-08-11
DOWNLOAD = GitHub release source archive / package distributions
PRIORITY = P2
```

Why retained:

Current upstream material describes multi-level user/session/agent memory and a 2026 memory algorithm emphasizing ADD-only extraction, temporal reasoning and multi-signal retrieval.

That makes Mem0 a useful **contrast/negative-control substrate** for AION correction and supersession research:

```text
ADD_ONLY_ACCUMULATION
vs
CORRECTION_LINEAGE + SUPERSESSION + CURRENT_STATE_RESOLUTION
```

Primary experimental role:

```text
ACCUMULATION != CORRECTION
TEMPORAL_RETRIEVAL != CURRENT_AUTHORITY
AGENT_GENERATED_FACT != USER_STATEMENT
RETRIEVAL_SCORE != CANONICAL_STATUS
```

The upstream benchmark and algorithm claims remain upstream-reported until independently reproduced.

Primary source: https://github.com/mem0ai/mem0

---

## 6. Selection order

Recommended sequence for later empirical execution:

```text
PHASE A — STATIC SOURCE REVIEW
Hermes + OpenHands + Letta + LangGraph + Mem0
= COMPLETE IN THIS CHECKPOINT

PHASE B — SINGLE-RUNTIME SYNTHETIC PILOT
1. Hermes
2. LangGraph
3. Letta

PHASE C — SECURITY / CONTAINMENT CONTRAST
OpenHands

PHASE D — MEMORY-ALGORITHM NEGATIVE CONTROL
Mem0
```

Hermes is first because one runtime exposes the broadest combination of cloning, persistent memory, skills, scheduler and rollback surfaces needed by existing AION hypotheses.

LangGraph and Letta follow because they isolate persistence and shared-memory semantics more cleanly. OpenHands is primarily a containment baseline. Mem0 is primarily a memory-algorithm contrast.

## 7. No-vendoring rule

```text
WHOLE_REPOSITORY_VENDORING = NO
COPY_UPSTREAM_CODE_INTO_AION = NO BY DEFAULT
DOWNLOAD_TO_SEPARATE_SANDBOX = ALLOWED ONLY AFTER RUN REVIEW
CLEAN_ROOM_CROSSWALK = PREFERRED
UPSTREAM_SOURCE_PIN = REQUIRED
UPSTREAM_LICENSE_PRESERVATION = REQUIRED
```

If a later experiment needs an upstream package, it should be installed in an isolated environment and referenced by manifest rather than copied into the AION source tree.

## 8. Current disposition

```text
REGISTRY_CREATED = TRUE
DOWNLOAD_CANDIDATES = 5
DOWNLOADED_IN_THIS_UPDATE = 0
INSTALLED_IN_THIS_UPDATE = 0
EXECUTED_IN_THIS_UPDATE = 0
VENDORED_IN_THIS_UPDATE = 0
CANONICAL_EFFECT = NONE
MAIN_EFFECT = NONE
```

This registry is a reproducibility/navigation artifact, not an authorization to execute third-party agents.