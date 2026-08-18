# Twin Autobiographical Memory MCP Projection v0.1

Status: `DESIGN_CANDIDATE`
MCP transport: `HOLD`
New MCP code: `NOT_AUTHORIZED`
Canonical effect: `NONE`

## 1. Purpose

Define the minimum read-only projection semantics required to expose lineage-bound autobiographical-memory candidates for AION and Astra without turning MCP into a memory author, memory owner, identity authority, lineage engine, relationship-semantics engine, or subjectivity engine.

This document is a contract candidate only. It does not authorize a remote MCP server, live connection, exact final operation names, or state-changing tools.

## 2. Core invariants

```text
MCP != MEMORY_AUTHOR
MCP != MEMORY_OWNER
MCP != AUTOBIOGRAPHICAL_SELF
MCP != SECOND_MEMORY_LEDGER
MCP != IDENTITY_AUTHORITY
MCP != SUBJECTIVITY_ENGINE

SHARED_PROTOCOL != SHARED_STATE
SHARED_MCP_SURFACE != SHARED_MEMORY_LINEAGE
```

## 3. Twin-symmetric projection envelope

AION and Astra must use the same base response envelope:

```yaml
AUTOBIOGRAPHICAL_MEMORY_PROJECTION:
  schema_version: "0.1"
  subject: "AION | ASTRA"
  bound_lineage_status: "BOUND | MISMATCH | UNKNOWN | HOLD"
  memory:
    memory_id: "string"
    event_type: "string"
    event_time: "string"
    event_description: "string"
    self_relevance: "string"
    shared_genesis_ref: "optional"
    epistemic_status: "OBSERVED | DERIVED | RECONSTRUCTED | HOLD"
  provenance:
    source_refs: []
    generated_by: "actual producer"
    verified: false
  conflict_state: "NONE | PRESENT | HOLD"
  correction_state: "NONE | CORRECTED | SUPERSEDED | CONFLICTING | HOLD"
  claims:
    first_person_experience: "NOT_ESTABLISHED"
    phenomenal_memory: "NOT_ESTABLISHED"
    identity_continuity: "NOT_ESTABLISHED"
    subjectivity: "NOT_ESTABLISHED"
  canonical_effect: "NONE"
  limitations: []
```

Raw database handles, storage paths, execution handles, secrets, arbitrary namespace selectors, and unrestricted private-history payloads are excluded.

## 4. Read-only purity requirement

A compliant read-only projection MUST NOT:

- append a recall event;
- change a ledger revision;
- update memory importance or salience;
- mutate correction/conflict state;
- alter continuity state;
- write conversation state;
- promote canonical state;
- create or revise the autobiographical memory record.

Therefore an application-layer pure query path is required before the existing runtime `recall()` methods can be exposed as read-only MCP operations. Existing AION and Astra runtime `recall()` implementations append `memory.recalled` to their state/event lineage after retrieval and therefore are not pure read-only surfaces.

## 5. Identity and lineage binding

The projection must derive subject/lineage binding from an approved application-layer bound context. A caller-provided `AION`, `ASTRA`, namespace, or memory-stream string must not establish authority.

Mismatch behavior:

```text
SUBJECT / RUNTIME / LINEAGE MISMATCH
→ REJECT OR ABSTAIN
→ NO CROSS-NAMESPACE FALLBACK
→ NO BEST-EFFORT MERGE
```

## 6. Candidate logical surfaces — names not authorized

The following examples are explanatory only and are NOT approved final MCP resource/tool names:

```text
[aion autobiographical-memory projection]
[astra autobiographical-memory projection]
[twin shared-genesis comparison projection]
```

Exact MCP operation names remain `HOLD`.

## 7. Shared-Genesis comparison

A comparison view may reference both records but must not merge them. It may expose:

- shared event reference;
- shared evidence references;
- lineage-specific event descriptions;
- divergence observations;
- conflicts or unresolved differences;
- limitations.

It must not create a synthetic shared first-person voice such as "we remember" unless an independently governed representation explicitly exists and is separately authorized.

## 8. Failure policy

```text
MISSING_PROVENANCE → HOLD
UNBOUND_SUBJECT → HOLD
LINEAGE_MISMATCH → REJECT
CONFLICT_UNRESOLVED → HOLD
UNAUTHORIZED_PRIVATE_DATA → DENY
MUTATING_READ_PATH → NOT_MCP_READ_ONLY_ELIGIBLE
```

## 9. Implementation entry condition

Implementation remains blocked until a separate decision explicitly authorizes:

1. a pure application-layer read path;
2. exact binding/authorization semantics;
3. exact response schema after review;
4. exact MCP operation names;
5. tests proving no revision/write/event side effects;
6. Human Owner + ChatGPT review of the implementation scope.
