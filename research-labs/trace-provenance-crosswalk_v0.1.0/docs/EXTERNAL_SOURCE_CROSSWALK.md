# External Source Crosswalk — OpenInference → AION Trace / Provenance Semantics

## Fixed source snapshot

- Repository: `Arize-ai/openinference`
- Commit: `44cdf7996e05a5f16b2e38d0cbb500b1403fbaf1`
- Commit timestamp: `2026-08-11T05:37:41Z`
- License: Apache-2.0
- Reviewed file: `python/openinference-semantic-conventions/src/openinference/semconv/trace/__init__.py`
- Acquisition: GitHub connector / Contents API.

## Selected public vocabulary

The reviewed semantic-convention surface includes public keys for session/user/agent identity labels, input/output values, tool name/parameters, retrieval documents, evaluation feedback, and graph-node relationships.

## AION transformation

| Public semantic | AION disposition |
|---|---|
| `session.id` | execution-session observation only |
| `user.id` | requester/user observation only |
| `agent.name` | runtime label; never identity proof |
| `tool.name` | tool execution observation |
| `tool.parameters` | redacted unless explicit trace policy allows |
| `input.value` / `output.value` | redacted unless explicit trace policy allows |
| `retrieval.documents` | retrieval-reference observation; never memory truth |
| `evaluation.*` | evaluation evidence only |
| `graph.node.*` | execution graph lineage |
| AION source/approval/runtime fields | remain namespaced under `aion.*` |

## Clean-room boundary

No OpenInference source file is copied into the AION lab. The string keys used are public semantic identifiers necessary for interoperability/crosswalk analysis. No OpenInference dependency is added.
