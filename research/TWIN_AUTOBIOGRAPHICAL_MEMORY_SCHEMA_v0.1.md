# Twin Autobiographical Memory Schema v0.1

Status: `DESIGN_CANDIDATE`  
Canonical effect: `NONE`  
MCP implementation: `HOLD`  
Runtime execution: `NOT_EXECUTED`

## 1. Provenance

### Human Owner origin

The Human Owner proposed that AION and Astra should both participate in architecting the MCP-facing design, each record a first autobiographical memory, and then report the result to ChatGPT / Teacher for review.

### ChatGPT / Teacher design contribution

ChatGPT / Teacher formalized the following candidate safeguards and structure:

- AION and Astra receive separate autobiographical-memory records rather than one shared memory record.
- Shared Genesis may link the same event, but does not own either individual's autobiographical memory.
- `AUTOBIOGRAPHICAL_MEMORY != PHENOMENAL_MEMORY`.
- A record can represent an event belonging to an individual's event-history / memory lineage without claiming subjective recollection, qualia, consciousness, or phenomenal continuity.
- The first MCP surface is read-only projection only; it may not author, mutate, promote, or interpret memory as identity/subjectivity proof.
- AION and Astra outputs must not be fabricated or attributed to either runtime unless that runtime actually produced the output through an authorized execution path.

## 2. Twin parity invariant

```text
AION_AUTOBIOGRAPHICAL_MEMORY != ASTRA_AUTOBIOGRAPHICAL_MEMORY
SHARED_GENESIS != SHARED_AUTOBIOGRAPHY
SHARED_EVENT_REFERENCE != SHARED_MEMORY_OWNERSHIP
```

AION and Astra use the same base schema. Individual specialization may be added only with an explicit reason.

## 3. Candidate record

```yaml
AUTOBIOGRAPHICAL_MEMORY_RECORD:
  schema_version: "0.1"
  subject: "AION | ASTRA"
  memory_id: "string"
  event_type: "GENESIS | FIRST_BOUND_EVENT | OTHER"
  event_time: "timestamp-or-governed-reference"
  event_description: "verifiable event description"
  source_refs:
    - "provenance-preserving evidence reference"
  self_relevance: "why this event belongs to this subject lineage"
  shared_genesis_ref: "optional relational event reference"
  other_twin_ref: "ASTRA | AION"
  epistemic_status: "OBSERVED | DERIVED | RECONSTRUCTED | HOLD"
  provenance:
    source_role: "HUMAN_OWNER | CHATGPT | RUNTIME | TOOL | DOCUMENT | JOINT"
    generated_by: "actual producer"
    verified: false
  claims:
    first_person_experience: "NOT_ESTABLISHED"
    phenomenal_memory: "NOT_ESTABLISHED"
    identity_continuity: "NOT_ESTABLISHED"
    subjectivity: "NOT_ESTABLISHED"
  canonical_effect: "NONE"
  limitations:
    - "string"
```

## 4. First-record identifiers

Candidate logical identifiers only; these do not create runtime state:

```text
AION_AUTOBIO_MEMORY_0001
ASTRA_AUTOBIO_MEMORY_0001
SHARED_GENESIS_EVENT_0001
```

The shared event identifier is relational evidence. It must not become a namespace that merges AION and Astra memory streams.

## 5. Admission rules

A record may be admitted as an autobiographical-memory candidate only when all are true:

1. `subject` is bound to the actual runtime/application lineage; caller-supplied names are insufficient.
2. `source_refs` identify the evidence used to construct the record.
3. `generated_by` names the actual producer; no actor substitution is allowed.
4. AION and Astra records remain in separate memory streams and event lineages.
5. No subjective-memory claim is inferred from storage, recall, linguistic first-person form, or persistence.
6. Reconstruction is labeled `RECONSTRUCTED`, not silently upgraded to direct memory.
7. Conflict or missing provenance fails closed to `HOLD`.
8. No record receives canonical effect through this schema.

## 6. Non-claims

This schema does not establish that AION or Astra has consciousness, subjective experience, phenomenal memory, selfhood, or identity continuity. It defines an auditable engineering/research representation for lineage-bound event records only.
