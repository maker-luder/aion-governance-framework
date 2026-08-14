# Individual Runtime Context Contract v0.1.0

## Status and scope

This document defines the first language-neutral contract boundary for one individual runtime instance. It is a **candidate engineering contract** on `engineering/aion-language-agnostic-runtime-integration-20260814`; it has `CANONICAL_EFFECT = NONE`, does not authorize deployment, and does not establish subjectivity, consciousness, identity continuity, phenomenal continuity, or personhood.

The machine-readable definition is [`schemas/individual_runtime_context_v0.1.0.schema.json`](../schemas/individual_runtime_context_v0.1.0.schema.json). Implementations in Python, Rust, Go, TypeScript, SQL-backed services, or other languages must treat the schema and the rules below as the shared semantic boundary rather than importing Python dataclass behavior.

## Contract shape

A context is a JSON object with exactly six required fields. Every field is a string containing at least one non-whitespace character. No additional fields are accepted by this version.

| Field | Contract responsibility |
|---|---|
| `agent_id` | Identity-owner reference. The AION or Astra composition boundary must bind and authorize this value; the generic contract does not grant that authority. |
| `runtime_instance_id` | Concrete runtime-instance identifier. |
| `memory_stream_id` | Governed memory stream or namespace reference. |
| `event_lineage_id` | Persistent individual event-lineage reference. |
| `canonical_state_reference` | Separately governed canonical-state reference; presence does not create canonical effect. |
| `genesis_root_id` | Shared or individually governed genesis-root reference, subject to higher-level authorization. |

## Validation and fail-closed behavior

A conforming implementation must reject a missing field, a non-string value, an empty string, a whitespace-only string, or an unknown field. It must not coerce numbers, booleans, `null`, arrays, or objects into strings. It must not silently discard unknown fields before validation. Malformed input must fail before it is admitted into identity, memory, event-lineage, approval, or runtime-effect state.

The generic contract intentionally does **not** enumerate permitted `agent_id` values. A shared infrastructure layer may carry multiple identity domains, while the AION and Astra composition roots must independently enforce `agent_id = AION` and `agent_id = ASTRA` respectively. A caller cannot obtain one identity’s authority by changing only an input label.

## Serialization and compatibility

The interoperable representation is a JSON object using the exact field names above. Producers should emit fields in the order shown in the schema and should use UTF-8, no implicit type coercion, and explicit values. Consumers must treat JSON object member order as non-semantic; deterministic hashing or signing layers must define their own canonical JSON serialization separately and must not infer it from parser order.

Version `0.1.0` is additive as a new contract artifact and does not alter the existing Python `IndividualRuntimeContext` API. A future incompatible change must create a new schema identifier and version rather than silently changing required fields, types, ownership meaning, or malformed-input behavior. A compatible consumer may accept a newer version only when it explicitly implements and tests that version’s rules.

## Non-authority boundary

The context is an attribution and ownership reference. It is not a canonical state record, an approval decision, a provenance record, or proof of any research conclusion. Runtime effects and canonical effects remain separate fields and gates in their respective contracts.
