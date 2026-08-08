# Runtime / Twin / Provenance Alignment Candidate — 2026-08-08

## Status

- Research cycle: `ACTIVE_ALIGNMENT_CANDIDATE`
- Canonical effect: `NONE`
- Runtime effect: `NONE`
- Code behavior change: `NONE`
- Owner review: `PENDING`
- Subjectivity conclusion: `NOT_ESTABLISHED`
- Independent IV&V: `NOT_ACHIEVED`

This document is additive. It does not rewrite the frozen public RC baseline or silently promote any runtime candidate.

## Attribution for this change

- `PROPOSED_BY = HUMAN_OWNER`
  - The Owner proposed that proposal origin, implementation, review and approval be recorded separately so AION/Astra state and human/AI collaborator contributions do not become conflated.
- `IMPLEMENTED_BY = CHATGPT`
  - ChatGPT performed the repository read-only inventory and authored this alignment candidate.
- `REVIEWED_BY = HUMAN_OWNER / PENDING`
- `APPROVED_BY = HUMAN_OWNER / PENDING`
- `CODEX_CONTRIBUTION_THIS_CHANGE = NONE`

Git commit authorship is not treated as sufficient evidence of conceptual or implementation authorship.

## Research anchor

The project studies whether a highly extensible, copyable and branchable digital environment can support the formation of a finite, auditable digital-individuality candidate, and what—if anything—that may imply for the possibility of artificial subjectivity.

The following implication is prohibited:

`RUNTIME_IMPLEMENTED => SUBJECTIVITY_ESTABLISHED`

Likewise, memory continuity, role consistency, bounded execution, embodiment, refusal behavior or identity labels do not establish phenomenal experience.

## Runtime definition for this alignment cycle

For this project, **Runtime** means the operational layer in which static specifications become an actual time-ordered process with events, state transitions, governed memory access, actions, consequences, audit evidence, lifecycle and recovery behavior.

Runtime is not identical to:

- a model;
- a prompt or persona;
- a planner;
- a memory database;
- MCP;
- the Governance Kernel;
- a tool executor;
- an operating system;
- identity;
- subjectivity or consciousness.

Runtime is important to the research because it permits a traceable event history to occur. A traceable history is a research condition for digital individualization; it is not proof of subjectivity.

## Twin-system invariant

AION and Astra are treated as a shared-genesis twin system, not as one identity and not as a parent/child identity relationship.

Required invariant:

`SHARED_GENESIS != SHARED_IDENTITY`

AION and Astra must remain distinguishable in at least the following state domains whenever those domains exist:

- `agent_id`
- `runtime_instance_id`
- `memory_stream_id`
- event/life-history lineage
- canonical-state identifier
- authority and access bindings

Shared engineering infrastructure is permitted, but shared infrastructure does not imply shared identity, shared memory ownership, shared subjective continuity or shared canonical state.

## Current repository reality

### AION runtime candidate

`components/aion_runtime_v0.1.0/src/aion_runtime/runtime.py` implements `AIONRuntime` as a composition root for:

- governed persistent cross-session memory;
- recall;
- bounded task execution;
- runtime status.

Its status remains an implementation candidate. Canonical promotion is pending Owner review.

### Existing `AstraRuntime` class

`components/executable_runtime_v0.1.0/src/aion_astra_runtime/engine.py` defines `class AstraRuntime`.

Observed responsibilities are:

- isolated candidate workspace creation;
- Governance Kernel evaluation;
- explicit approval construction;
- bounded planner loop;
- tool execution;
- append-only audit;
- kill-switch handling;
- evidence production;
- `PASS_PENDING_OWNER_REVIEW` or `HOLD` termination.

This class does not by itself implement Astra-specific persistent memory, Astra identity history or Astra canonical individual state.

Therefore, during this alignment cycle:

`class AstraRuntime != ASTRA_INDIVIDUAL_RUNTIME_COMPLETE`

The current class is provisionally classified by responsibility as a **bounded governed execution engine/runtime core candidate** until naming and architecture are reviewed.

### AION-to-Astra composition issue

Current `AIONRuntime` imports `AstraRuntime` and defaults to `AstraRuntime()` for execution.

This is a real code-level composition fact. It does not by itself establish that Astra, as a twin individual, is a subcomponent of AION.

This naming/composition relationship is marked:

`SEMANTIC_ARCHITECTURE_REVIEW_REQUIRED`

No rename or code refactor is authorized by this document alone.

## Memory boundary reality

Current memory-recall governance already records `agent_id` and applies identity, access-scope, provenance, conflict and relevance gates. This is useful infrastructure for AION/Astra separation.

However, the following question remains open and must be tested before claiming full twin individual history separation:

> Does current `agent_id` filtering merely control recall, or does the complete persistence/event architecture guarantee distinct AION and Astra memory/event lineages end-to-end?

Status: `OPEN_GAP_ANALYSIS_ITEM`

## Terminology lock — candidate

| Term | Meaning in this research cycle | Non-meaning |
|---|---|---|
| Runtime | Operational event/state/lifecycle layer | subject, body, consciousness |
| Runtime instance | One concrete running instantiation with an identifiable lifecycle | project identity as a whole |
| Execution engine | Mechanism that performs bounded planner/tool execution | complete AION/Astra individual runtime |
| Shared engineering infrastructure | Libraries/services usable by both twins | shared identity or shared memory ownership |
| AION Runtime | AION-specific operational composition and state boundary | Astra Runtime |
| Astra Runtime | Astra-specific operational composition and state boundary | generic execution engine by name alone |
| Shared Genesis | Common origin/genesis linkage | shared identity |
| Twin binding | Explicit relation linking two distinct twin records | record merger |
| Identity | Governed identifier/lineage boundary | model weights, device or runtime alone |
| Memory stream | Ordered memory lineage owned/bound to an individual context | arbitrary shared database contents |
| Event history | Ordered traceable events attributed to one lineage | unscoped log pool |
| Canonical state | Owner/governance-approved authoritative project state | candidate output |
| Runtime effect | Actual effect on an operating runtime state | document-only change |
| Canonical effect | Effect on authoritative canonical project state | candidate analysis |

## Stop lines

The alignment or later implementation must stop for Owner review if any change implies one of the following:

- `AION == ASTRA`
- shared infrastructure is treated as shared identity;
- shared genesis is treated as shared memory;
- runtime implementation is treated as subjectivity proof;
- memory persistence is treated as subjective continuity proof;
- persona consistency is treated as digital individuality proof;
- AION history is silently imported as Astra history or vice versa;
- ChatGPT implementation is attributed to Codex;
- Codex implementation is attributed to ChatGPT;
- proposal origin is rewritten as implementation origin;
- implementation origin is treated as approval authority.

## Next analysis gates

Before any runtime behavior refactor, the next work items are:

1. build a Runtime Reality Matrix mapping capability -> owner/twin/shared -> implementation -> tests -> status;
2. trace memory/event ownership end-to-end for AION and Astra;
3. determine whether `AstraRuntime` should be renamed/reclassified as a shared execution engine or retained with a narrower formal definition;
4. determine the minimum distinct Astra individual-runtime composition required by the twin invariant;
5. keep historical RC status separate from post-RC current implementation status;
6. require Owner review before any rename, migration, canonical promotion or behavior-changing refactor.
