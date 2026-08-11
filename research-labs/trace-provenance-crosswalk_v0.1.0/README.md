# Trace / Provenance Semantic Crosswalk — v0.1.0

Status: `RESEARCH_MODEL / CLEAN_ROOM / OBSERVABILITY_ONLY / CANONICAL_EFFECT=NONE / MAIN_EFFECT=NONE`

This lab maps selected public OpenInference trace semantics into an AION research-safe
observability envelope without replacing AION provenance, identity, authority, or Audit Sink logic.

## Purpose

OpenInference provides useful public vocabulary for session, user, agent, input/output,
tool use, retrieval, evaluations, and execution-graph relationships. AION needs those
execution observations, but it must keep them separate from source authority and canonical state.

```text
AION EVENT
   ↓
TRACE POLICY / REDACTION
   ↓
PUBLIC SEMANTIC CROSSWALK
   ↓
OBSERVABILITY ATTRIBUTES
   ↓
AUDIT / EVAL CONSUMER
```

## Implemented controls

- maps `session.id`, `user.id`, `agent.name`, span kind, tool name, retrieval refs, evaluations, and graph lineage;
- raw input/output content is excluded by default;
- tool parameters are excluded by default;
- AION-specific `runtime_event_id`, `subject_id`, `source_ref`, and `approval_ref` remain under the `aion.*` namespace;
- imported external attributes are always `EXTERNAL_OBSERVATION_ONLY`;
- external `aion.*` fields are never accepted as project authority;
- canonical effect is fixed to `NONE`.

## Standing locks

```text
TRACE != TRUTH
OBSERVABILITY != AUTHORITY
SESSION_ID != SUBJECT_ID
AGENT_NAME != IDENTITY_PROOF
RETRIEVAL_DOCUMENT != MEMORY_TRUTH
EVALUATION_SCORE != THEORY_VALIDITY
EXTERNAL_ATTRIBUTE != APPROVAL_AUTHORITY
TRACE_EXPORT != CANONICAL_WRITEBACK
```

## Fixed external source

```text
repository = Arize-ai/openinference
commit = 44cdf7996e05a5f16b2e38d0cbb500b1403fbaf1
license = Apache-2.0
reviewed_surface = python OpenInference semantic conventions
source_code_copied = NO
runtime_dependency_added = NO
```

See `docs/EXTERNAL_SOURCE_CROSSWALK.md`.

## Run

```bash
python -m pip install -e .
python -m compileall -q src
python -m pytest -q
python scripts/run_demo.py
```

Local validation before branch materialization:

```text
pytest = 12 passed
compileall = PASS
demo = PASS
```
