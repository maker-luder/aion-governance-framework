# AION Native Language Conformance Profile v0.1.0

**Status:** `ESTABLISHED_CANDIDATE / NON_EXECUTABLE`

**Language version:** `0.1`

**IR version:** `0.1.0`

**Canonical effect:** `NONE`

## 1. Purpose

This profile makes the native-language feasibility artifacts testable as repository contracts without creating a source parser, compiler, interpreter, virtual machine, runtime evaluator, or authority bridge. It validates artifact inventory, JSON Schema validity, strict IR fixtures, declared semantic invariants, source-example boundary markers, and workflow wiring.

> **Conformance of the feasibility artifacts is not conformance of a future parser.**

The profile therefore distinguishes **artifact validation** from future **language implementation conformance**. A future parser must additionally prove lexical, grammar, AST, semantic, and cross-parser behavior; this milestone does not implement that parser.

## 2. Artifact inventory

The machine-readable inventory is `language-spec/conformance/aion_native_conformance_manifest_v0.1.0.json`, validated by `language-spec/conformance/aion_native_conformance_manifest_v0.1.0.schema.json`. The negative-vector envelope is separately validated by `language-spec/conformance/aion_native_negative_vectors_v0.1.0.schema.json`.

| Artifact class | Current artifact | Validation performed now |
|---|---|---|
| Grammar candidate | `language-spec/aion_native_language_v0.1.0.ebnf` | Required production / boundary vocabulary checks; no parsing claim |
| IR schema | `language-spec/aion_native_ir_v0.1.0.schema.json` | Draft 2020-12 meta-schema validation and positive/negative fixture validation |
| Accepted source | `language-spec/examples/accepted/aion_runtime_memory_requirements.aion` | Inventory, encoding, required version/effect markers, and banned-token boundary checks |
| Rejected source | `language-spec/examples/rejected/*.aion` | Inventory, expected diagnostic marker, canonical-effect and authority-boundary checks |
| Positive IR | `language-spec/conformance/aion_native_ir_v0.1.0.valid.json` | Schema validation and static symbol / namespace / effect invariants |
| Negative IR | `language-spec/conformance/aion_native_ir_v0.1.0.negative_vectors.json` | Negative-vector schema validation, schema rejection vectors, and semantic mismatch vectors |
| Lifecycle mapping | Source `start` / `stop` to `runtime.started` / `runtime.stopped` | Deterministic documentation and boundary check; no outcome fields |
| Error mapping | `language-spec/conformance/aion_native_error_mapping_v0.1.0.json` plus its schema | All 14 candidate diagnostic codes map to existing Error Envelope categories with canonical effect `NONE` |

## 3. Validation layers

| Layer | What is checked | What is not claimed |
|---|---|---|
| JSON syntax | All manifest, schema, and JSON fixture documents parse as strict JSON | No raw source parsing |
| Schema validity | Each JSON Schema is valid Draft 2020-12; positive IR and manifest validate; negative schema vectors fail closed | Schema cannot establish NFC, symbol resolution, or authority |
| Semantic fixture invariants | Unique local declarations, referenced locals, namespace-kind equality, operation-kind/effect consistency, canonical effect `NONE`, and no authority result fields | This is not a source evaluator or runtime semantic analyzer |
| Source boundary | UTF-8 without BOM, `language 0.1`, expected rejection markers, no authority-grant / execution fields, and `canonical_effect: none` in accepted source | It does not claim grammar acceptance or rejection for arbitrary source |
| CI wiring | Quality, Cross-Language Contract Conformance, and Runtime Strong QA execute the artifact test on relevant path changes | CI does not establish independent IV&V or cross-language parser parity |

## 4. Stable diagnostic mapping

| Native candidate code | Existing Error Envelope category | Mapping rule |
|---|---|---|
| `LEXICAL_ERROR` | `MALFORMED_INPUT` | Invalid source encoding or lexical value |
| `PARSE_ERROR` | `MALFORMED_INPUT` | Source does not match the candidate grammar |
| `TYPE_ERROR` | `MALFORMED_INPUT` | Typed source reference is not well-formed |
| `UNKNOWN_SYMBOL` | `MALFORMED_INPUT` | A local reference is unresolved |
| `DUPLICATE_DECLARATION` | `MALFORMED_INPUT` | Local declaration namespace is not unique |
| `UNSUPPORTED_VERSION` | `UNSUPPORTED_VERSION` | Language / IR / profile version is incompatible |
| `IDENTITY_MISMATCH` | `IDENTITY_MISMATCH` | Typed runtime / namespace relationship is inconsistent |
| `AUTHORITY_REQUIRED` | `AUTHORITY_DENIED` | Source attempts to claim approval or authority |
| `CAPABILITY_DENIED` | `AUTHORITY_DENIED` | Source attempts to grant or admit a capability |
| `INVALID_EFFECT` | `AUTHORITY_DENIED` | Source or IR requests canonical effect other than `NONE` |
| `INVALID_TRANSITION` | `INVALID_TRANSITION` | Lifecycle transition requirement is outside candidate vocabulary |
| `FOUNDATION_CONFLICT` | `INTEGRITY_FAILURE` | Source attempts to freeze an unresolved Event / Lineage / hash foundation |
| `PROVISIONAL_SEMANTIC` | `MALFORMED_INPUT` | Source treats a provisional domain as final v0.1 semantics |
| `RESOURCE_LIMIT_EXCEEDED` | `MALFORMED_INPUT` | Candidate resource bound is exceeded |

This mapping is a candidate adapter rule. It does not change `schemas/aion_error_envelope_v0.1.0.schema.json` or the current Python interop implementation.

## 5. Explicit semantic invariants

The artifact test must fail closed when any of the following occurs: an IR declaration local name is duplicated; a lifecycle or operation runtime reference does not resolve to a runtime declaration; a memory namespace owner does not resolve; namespace kind differs from the owner runtime kind; an operation effect class disagrees with its operation kind and requirements; canonical effect is not `NONE`; an IR declaration contains approval-satisfied, capability-granted, event-hash, predecessor, runtime-admitted, state-mutated, or execution-result fields; a manifest path is absolute or escapes its repository root; a source fixture lacks its expected rejection marker; or an accepted source contains authority-grant or execution syntax.

The lifecycle bridge is checked as a request-only mapping: `start` maps to `runtime.started` and `stop` maps to `runtime.stopped`; `from_state`, `to_state`, `event_sequence`, `event_hash`, and successful outcome fields remain absent. These are bounded static checks over committed artifacts. They do not consume external identity, approval, capability, memory, event, audit, network, filesystem, or runtime state.

## 6. Future parser conformance boundary

A future separately authorized parser must add golden vectors for UTF-8 / BOM, NFC and malformed Unicode, duplicate names, unknown fields, unknown symbols, unsupported versions, invalid effects, namespace mismatch, approval/capability self-grants, resource limits, provisional Event / Lineage use, and formatting equivalence. It must emit the stable semantic codes above and validated IR that conforms to the strict schema. It must not execute source or treat IR as authority.

The current profile intentionally does not call such a parser and does not report parser parity, production readiness, formal verification, or independent IV&V.

## References

[1]: AION_NATIVE_LANGUAGE_FEASIBILITY_V0.1.0.md "Feasibility decision and eligibility matrix"
[2]: AION_NATIVE_LANGUAGE_SEMANTIC_MODEL_V0.1.0.md "Source, AST, semantic analysis, and validated IR model"
[3]: AION_NATIVE_LANGUAGE_SECURITY_MODEL_V0.1.0.md "Threat and resource model"
[4]: AION_INTEROPERABILITY_PROFILE_V0.1.0.md "Current interop profile and error boundary"
[5]: ../schemas/aion_error_envelope_v0.1.0.schema.json "Current Error Envelope schema"
