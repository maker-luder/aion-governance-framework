# AION / Astra Agent Execution Substrate Architecture

## Purpose

AION and Astra already have distinct individual Runtime contexts over shared bounded engineering mechanisms. This component adds a shared execution-substrate interface without collapsing those individual contexts.

The substrate is the **execution plane**. Existing AION governance and evidence mechanisms remain the **governance/evidence plane**.

```text
execution substrate -> normalized events -> governance decision -> evidence record -> interop
```

A substrate may expose models, tools, skills, sessions, sandboxes, storage, agent loops, subagents, teams, plugins, or UI surfaces. Exposing a capability never grants permission to use it.

## Runtime binding

`RuntimeBinding` carries the existing engineering identifiers:

- `agent_id`
- `runtime_instance_id`
- `memory_stream_id`
- `event_lineage_id`
- `canonical_state_reference`
- `genesis_root_id`

and adds:

- `substrate_id`
- `session_id`

Only `AION` and `ASTRA` are admitted. Sharing a substrate, plugin implementation, model provider, sandbox backend, or genesis root does not merge the two individual Runtime contexts.

`SHARED_SUBSTRATE != SHARED_IDENTITY`

## Governance

Observation-only capabilities may be inspected without creating mutation authority.

Mutating/executing capabilities require explicit Owner approval plus an authority reference. v0.1.0 additionally fails closed when a request asks for:

- network access;
- deployment;
- a canonical effect other than `NONE`.

Plugin creation, plugin mounting, Creator-style composition, or agent-loop replacement never self-authorizes.

`SELF_COMPOSITION != SELF_AUTHORIZATION`

## Event evidence

The evidence plane consumes normalized event facts. It does not require raw prompts, raw assistant text, raw tool results, or model hidden reasoning.

A normalized event preserves:

- event order;
- event family and source event type;
- bound substrate session;
- sorted payload-key names;
- SHA-256 over the complete source payload;
- a bounded reasoning-visibility label.

This keeps the source payload hash-bound while minimizing replication of potentially sensitive content.

## DSH profile

The first external adapter targets DeepSeek Harness at exact upstream ref
`b150a551b8d465e31e418e1b2eaf5e79bbb7d28e`.

Only durable session-event families are admitted as durable evidence:

- `turn/*`
- `step/*`
- `user/message`
- `assistant/*`
- `tool/*`

Live extension events such as `agent/*`, `llm/stream`, and `tools/*` are not silently upgraded into durable evidence.

The adapter is inspection-only. It performs no DSH installation, launch, model call, subagent delegation, network access, or plugin mutation.

## Fork and team semantics

A fork records parent session, child session, and boundary. It establishes engineering lineage only.

`FORK_LINEAGE != IDENTITY_CONTINUITY`

A team snapshot records the team id and unique member session ids. It establishes roster membership only.

`AGENT_TEAM != COLLECTIVE_IDENTITY`

## Evidence Interop path

A normalized trajectory can materialize a HOLD-status `research_evidence_record_v0.2.0`.

The record deliberately keeps:

- `canonical_effect = NONE`
- `result_status = HOLD`
- `independent_validation_status = IVV_NOT_ACHIEVED`
- subjectivity/consciousness/identity conclusions `NOT_ESTABLISHED`.

The existing AION Evidence Interop component may then project that record into W3C PROV, RO-Crate, unsigned in-toto, OPA/Rego input, Inspect AI static artifacts, and the OpenSSF-aligned crosswalk.

`EXPORT_PROJECTION != SOURCE_REPLACEMENT`

## Non-claims

Engineering event continuity is not phenomenal continuity. Session identity is not ontological identity. A provider-exposed reasoning field is not a complete record of internal cognition. Multi-agent coordination is not evidence of a collective subject.

`OBSERVATION != MECHANISM != INTERPRETATION`
