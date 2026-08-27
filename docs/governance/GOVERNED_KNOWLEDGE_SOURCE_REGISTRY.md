# Governed Knowledge Source Registry

Status: `CANDIDATE / BOUNDED GOVERNANCE PROFILE`
Canonical effect: `NONE`
Deployment: `FALSE`
Automatic writeback: `NO`
Action authority: `NONE`

## Purpose

AION and Astra may use shared project knowledge without turning that knowledge into shared private memory, shared identity, or automatic truth. This profile defines a bounded registry for source metadata, admission, retrieval, provenance, context budgeting, verification, and cross-agent source-exposure evidence.

The registry is a governance surface, not a memory expansion mechanism.

```text
GOVERNED_SOURCE_REGISTRY != UNBOUNDED_MEMORY
RETRIEVED_CONTENT != ACCEPTED_FACT
SOURCE_SELF_DECLARED_CANONICAL != AION_CANONICAL_STATE
SOURCE_AVAILABILITY != AUTHORITY_TO_USE
SOURCE_USE != WRITEBACK_AUTHORITY
SHARED_SOURCE != SHARED_IDENTITY
AGENT_OUTPUT_INDEPENDENCE != EVIDENCE_SOURCE_INDEPENDENCE
```

## Registry role in the architecture

```text
source discovery / declared source map
              |
              v
Governed Knowledge Source Registry
              |
              v
admission + provenance + verification policy
              |
              v
bounded on-demand retrieval
              |
              v
Context Intake
              |
              v
Epistemic Integrity Gate
              |
              v
AION / Astra analysis
              |
              v
source-exposure evidence + audit
```

A source is not injected into model context merely because it appears in the registry. Retrieval must be task-relevant, bounded, provenance-bearing, and compatible with the source's verification policy.

## Source record

A governed source record should carry at least:

```text
source_id
source_title
source_version
domain
source_class
source_declared_status
registry_status
epistemic_role
provenance
content_hash
verification_policy
freshness_policy
allowed_agents
allowed_tasks
context_policy
context_token_cap
authority_level
writeback_authority
canonical_effect
```

The corresponding machine-readable candidate schema is `schemas/governed_knowledge_source_v0.1.0.schema.json`.

### Status separation

`source_declared_status` records how an upstream source describes itself. It does not create repository authority.

`registry_status` records the AION-side admission state and is restricted to bounded meanings such as:

- `DECLARED_METADATA_ONLY` — title/version/role was declared, but source content was not ingested or verified;
- `CANDIDATE` — source material is available for provenance and policy checks;
- `ACTIVE_REFERENCE` — source is admitted for bounded retrieval as a reference;
- `HOLD` — source must not be used for decision support until a stated issue is resolved;
- `RETIRED` — retained for provenance but not active retrieval.

No registry status creates canonical promotion, deployment authority, or scientific truth.

## Retrieval and context rules

1. Retrieval is `ON_DEMAND` by default. No source receives permanent prompt residency merely by being active.
2. Every injected fragment must have a hard size cap. A source-level `context_token_cap` is mandatory.
3. The consumer must retain source identity and provenance alongside the fragment.
4. A retrieval result is evidence input, not accepted fact.
5. High-risk or time-sensitive claims requiring current official verification must be re-checked against an authoritative current source before they are treated as admissible support.
6. Prompt libraries, workflow recipes, and operational templates are method references, not truth sources.
7. Domain packs are mounted only for relevant tasks and do not become core identity or private memory.
8. Writeback remains separately governed. `writeback_authority = NONE` in this v0.1.0 candidate profile.

## AION / Astra independence accounting

Independent agent execution is not sufficient to establish independent evidence.

For every AION / Astra research comparison, record whether the agents were exposed to the same source or materially overlapping source lineage.

```text
SHARED_SOURCE_EXPOSURE = TRUE | FALSE | UNKNOWN
```

If `TRUE`, the evidence record must not describe agreement between the agents as source-independent replication.

```text
INDEPENDENT_ANALYSIS
requires
DECLARED_INFORMATION_PATH

SOURCE_INDEPENDENCE = UNKNOWN
=> REPLICATION_CLAIM = HOLD
```

Cross-agent communication and source exposure are separate dimensions. Blocking direct communication does not prove source independence.

## Domain-pack policy

Sources may be grouped into bounded domain packs such as:

- `GOVERNANCE`;
- `ENGINEERING`;
- `IMAGE_PROMPT`;
- `REAL_ESTATE_TW`;
- future explicitly declared domains.

A domain pack is a retrieval scope only.

```text
DOMAIN_PACK != CORE_IDENTITY
DOMAIN_PACK != GLOBAL_CONTEXT
DOMAIN_REFERENCE != CURRENT_OFFICIAL_FACT
```

For sources marked `OFFICIAL_CURRENT_REQUIRED`, an admissible high-risk answer requires both the reference and a current official verification step.

```text
DOMAIN_REFERENCE
+
CURRENT_OFFICIAL_VERIFICATION
->
ADMISSIBLE_SUPPORT_CANDIDATE
```

This remains an evidence candidate, not automatic truth.

## 2026-08-27 declared source-map intake

The Human Owner supplied a source-map image describing 11 long-term sources and zero temporary sources. The image is treated only as a metadata declaration. The underlying documents, URLs, hashes, and content were not supplied by that image and are therefore not silently ingested.

| Domain | Declared source | Declared version | Declared role/status | Registry disposition |
|---|---|---:|---|---|
| Governance | Project Constitution | v2.7 | Active Master / Canonical | `DECLARED_METADATA_ONLY` |
| Governance | Knowledge Governance | v1.2 | Active Canonical | `DECLARED_METADATA_ONLY` |
| Governance | OpenWiki x AI-Core Wiki | v1.1 | Active Reference-Governance | `DECLARED_METADATA_ONLY` |
| Engineering | Agent / Harness / Skills / Evals | v2.1 | Active Canonical / Engineering Reference | `DECLARED_METADATA_ONLY` |
| Engineering | Architecture Research | v2.6 | Active Research Index | `DECLARED_METADATA_ONLY` |
| Engineering | AI-Core and Real-Estate App Roadmap | v1.1 | Active Roadmap | `DECLARED_METADATA_ONLY` |
| Engineering | AI Image Interpretation Core Specification | unspecified | Proposed Specification | `DECLARED_METADATA_ONLY` |
| Image / Prompt | Prompt Library | v2.0 | Active Reference | `DECLARED_METADATA_ONLY` |
| Image / Prompt | Image Composition and Floorplan Fidelity Rules | unspecified | Active Canonical Operational Rule | `DECLARED_METADATA_ONLY` |
| Real Estate | Taiwan Building Regulation and AEC Guide | v1.0 | Active Secondary Reference; official verification required | `DECLARED_METADATA_ONLY` |
| Real Estate | Real-Estate Owner Valuation Report | v1.3 | Active Operational Reference; official verification required | `DECLARED_METADATA_ONLY` |

The source-map declaration also states that research is not runtime, a roadmap is not completion evidence, and high-risk information requires current official verification. This profile preserves those separations.

Before any declared source can advance from `DECLARED_METADATA_ONLY`, obtain the actual source material or canonical location and record provenance, version binding, verification policy, and a content hash where technically applicable.

## Generated registry summary

Counts such as `active_sources`, `temporary_sources`, or `retired_sources` should be generated from machine-readable records. They must not be treated as authoritative merely because a diagram or prose summary states them.

```text
DECLARED_COUNT != VERIFIED_REGISTRY_COUNT
ROADMAP != COMPLETION_EVIDENCE
RESEARCH != RUNTIME
```

## Fail-closed conditions

A retrieval request returns `HOLD` when:

- source provenance is missing for a task that requires it;
- required official verification cannot be performed;
- a source is stale under its freshness policy;
- the requested fragment would exceed its hard context cap;
- the source is not admitted for the requesting agent or task;
- source-independence status is required for a replication claim but is unknown;
- use would imply writeback, canonical effect, deployment, or authority not granted elsewhere.

## Non-claims

This registry does not establish that any declared external source is correct, current, canonical to AION, complete, or actually available to AION / Astra. It does not establish shared memory, identity continuity, subjectivity, consciousness, moral authority, deployment readiness, or an independent replication simply because two agents used the registry.
