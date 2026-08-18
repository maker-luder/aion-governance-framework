# AION / Astra MCP Phase 1 Observation Evidence Bridge

Status: `IMPLEMENTATION_CANDIDATE / PHASE_1_OBSERVATION_EVIDENCE_BRIDGE`

```text
RUNTIME_MEMORY_ACCESS = NO
EXISTING_RUNTIME_RECALL_CALLS = NO
MEMORY_WRITE = NO
IDENTITY_AUTHORITY = NO
CANONICAL_WRITE = NO
PRIVATE_CONVERSATION_BULK_INGEST = NO
PUBLIC_DEPLOYMENT = NO
MAIN_MERGE = NO
INDEPENDENT_IVV = NOT_ACHIEVED
```

This component is a deliberately narrow, fixture-backed MCP bridge for **observation, provenance, research boundary and nonclaims evidence**. It does not implement long-term memory, identity continuity, canonical state, relationship state, subjectivity inference or writeback.

## Why this is not a Runtime recall wrapper

The existing AION and Astra runtime `recall()` methods append a `memory.recalled` event to runtime state/event lineage. Marking a wrapper around those functions as read-only would be inaccurate. This Phase 1 bridge therefore does not import or call AION Runtime, Astra Runtime, memory stores, identity stores, event lineage, or any `recall()` implementation.

## Tools

The server exposes exactly these six closed-world tools:

```text
list_continuity_observations()
get_continuity_observation(observation_id)
search_provenance_records(query)
get_source_attribution(record_id)
get_research_boundary()
get_current_nonclaims()
```

All tools are annotated as read-only, non-destructive, idempotent and closed-world. Missing records fail closed. There are no create/update/promote/merge/write/remember/identity/runtime/deployment tools.

## Returned provenance

The canonical dimensions are:

```text
evidence_source_class
retrieval_mechanism
source_id
source_timestamp
retrieval_timestamp
tool_name
tool_call_id
authority
canonical_effect
accepted_as_fact
memory_write
identity_authority
```

Compatibility aliases remain for older callers only:

```text
source_type = evidence_source_class
recall_source = retrieval_mechanism
```

Do not treat either alias as a separate provenance dimension.

`retrieval_mechanism` vocabulary includes:

```text
INTERNAL_CONTEXT
CHAT_HISTORY_REFERENCE
SAVED_MEMORY
MCP_EXTERNAL_RETRIEVAL
USER_PROMPT
UNKNOWN
```

MCP retrieval is therefore distinguishable from a model's natural/internal continuity behavior. Similar output does not imply identical mechanism.

Source classes distinguish what kind of evidence is being represented. `COMPOSITE_GOVERNANCE_RECORD` is used when the returned governance material contains multiple known provenance contributions and must not be collapsed into Human Owner-only or Teacher-only authorship. `TASK_EXECUTION_PROVENANCE` is used for execution-chain evidence and must not be mislabeled as a jointly authored research record.

When a source time is not independently supported, Phase 1 records use:

```text
source_timestamp = UNKNOWN
```

rather than inventing midnight or another false-precision timestamp.

## Inputs

The initial fixture corpus contains only synthetic observations, explicit observation metadata and public repository provenance. It contains no private conversation transcript, live Runtime, memory database, event lineage, identity store, canonical state reference or deployment endpoint.

## Transport

The executable entrypoint uses local stdio only:

```sh
aion-observation-evidence-mcp
```

HTTP/SSE, remote MCP, authentication, public deployment and connector creation are intentionally outside Phase 1.

## Local validation

From this component directory:

```sh
python -m pip install -e '.[dev]'
python -m pytest -q
```

The tests check the exact tool inventory, read-only annotations, provenance fields, retrieval/source separation, fail-closed lookup, immutable store behavior, absence of runtime imports, absence of write tools, fixed nonclaims and source-attribution boundaries.

## Authority

This is a non-canonical candidate. Teacher review and Human Owner approval are pending. A PASS in these bounded tests would establish only implementation behavior for this bridge; it would not establish subjectivity, identity continuity, memory ownership, canonical authority, scientific validity, independent IV&V, release or deployment readiness.
