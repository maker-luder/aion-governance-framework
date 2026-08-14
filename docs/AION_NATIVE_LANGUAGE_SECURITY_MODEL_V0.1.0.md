# AION Native Language Security Model v0.1.0

**Status:** `ESTABLISHED_CANDIDATE / NON_EXECUTABLE`

**Canonical effect:** `NONE`

**Execution capability:** `NOT_AUTHORIZED`

## 1. Security objective

The AION Native Language v0.1 candidate is a declaration format, not an authority or execution mechanism. Its security objective is to reject ambiguous, self-authorizing, identity-substituting, capability-escalating, or contract-free source before it can produce validated semantic IR. A parsed document is not an admitted runtime request, and validated IR is not external authorization evidence.

## 2. Threat model

| Threat | Example | Required v0.1 control | Residual boundary |
|---|---|---|---|
| Authority forgery | `owner_approved: true` or `authority: owner` | Grammar has no approval-satisfaction or authority-grant field; static analysis rejects self-authenticating terms in authority positions | External approval evidence remains a governed runtime concern |
| Canonical-effect escalation | `canonical_effect: write` | Grammar / schema admit only `none` / `NONE`; semantic analysis emits `INVALID_EFFECT` | Any future canonical write needs a separate governance program |
| Capability escalation | `capability memory.read = granted` | Source can contain only `requires capability`; no grant production | Capability admission remains external |
| Identity substitution | Changing `AION` to `ASTRA` or relabeling a runtime | Typed agent/runtime/namespace references; owner reference compatibility is checked statically | Real identity binding remains external runtime evidence |
| Namespace crossing | An AION runtime names an Astra-owned namespace | Memory namespace declaration binds to a typed runtime declaration; mismatch rejects | Existing memory access / mutation semantics remain partial |
| Parser differential | Different parsers accept authority-sensitive source differently | Formal grammar, strict lexical model, stable error categories, future golden vectors | Cross-parser parity is not established in this milestone |
| Unicode confusion | Non-NFC or invisible-variant authority identifier | ASCII local names; external identifier literals require NFC and valid Unicode | Contract-specific identifier policies may be narrower |
| Duplicate declaration | Two declarations share a local name | Semantic duplicate-symbol check, stable `DUPLICATE_DECLARATION` code | Parser implementation must preserve source locations for diagnosis |
| Version downgrade | Language `0.1` silently read with different semantics | Explicit language / IR / profile versions; unknown incompatible versions fail closed | Evolution changes require documented classification |
| Event / lineage semantic freeze | Source specifies a hash frame or genesis predecessor | No persisted EventEnvelope / hash / genesis syntax in v0.1; unresolved use is provisional or blocked | Future migration requires a separate contract decision |
| Unsafe deserialization | Malformed IR or unknown authority field | Strict JSON Schema, explicit versions, `additionalProperties: false` in authority-sensitive IR | Host adapters still need their own safe input handling |
| Resource exhaustion | Huge source, nesting, literals, diagnostics, or declarations | Candidate source / token / nesting / declaration / diagnostic limits; fail closed with `RESOURCE_LIMIT_EXCEEDED` | Limits need measured review before a production parser |
| Arbitrary execution creep | Grammar grows eval, commands, plugins, filesystem, sockets, or network | No executable grammar productions, no parser implementation, no runtime adapter, and explicit boundary audit | Any execution request is a stop condition |
| Confused deputy | Semantic IR treated as an approval or capability proof | Separate source-derived requirements from external runtime admission envelope | Future adapter must preserve this boundary |

## 3. Resource-bound model

The following are `CANDIDATE_LIMIT`, not permanent language law. They are selected to keep future parser attack surfaces bounded while avoiding unmeasured claims of adequacy.

| Resource | Candidate limit | Failure behavior |
|---|---:|---|
| UTF-8 source document | 1 MiB | `RESOURCE_LIMIT_EXCEEDED` before semantic analysis |
| External identifier literal | 256 code points | `LEXICAL_ERROR` / malformed identifier |
| String literal | 4 KiB UTF-8 encoded | `RESOURCE_LIMIT_EXCEEDED` |
| Local declaration identifier | 64 ASCII characters | `LEXICAL_ERROR` |
| Block nesting | 128 levels | `RESOURCE_LIMIT_EXCEEDED` |
| Declarations per document | 1,024 | `RESOURCE_LIMIT_EXCEEDED` |
| Emitted diagnostics | 100 | Stop after bounded diagnostics and indicate truncation |
| IR semantic payload | 64 KiB canonical UTF-8 | `RESOURCE_LIMIT_EXCEEDED` |

No source construct may depend on local timezone, process environment, filesystem state, network lookup, implicit current time, random input, locale, dynamic import, or host-language object ordering.

## 4. Invalid states made difficult or impossible to represent

| Invalid state | Why it is not representable in the candidate syntax / IR |
|---|---|
| Self-created approval | There is no `approval_satisfied`, `owner_approved`, inherited approval, or permanent approval syntax |
| Self-created authority | There is no owner / administrator / bypass grant grammar production |
| Canonical write request | The only canonical effect enum value is `NONE` |
| Caller-controlled lifecycle state | Source states transition requirement only; it cannot name current state, derived state, atomicity, committed event, or success |
| Capability grant | Source has requirement syntax but no `granted` state or capability-admission evidence |
| Identity ownership transfer by label | Reference type and external binding are distinct; no ownership-transfer syntax exists |
| Silent AION/Astra namespace crossing | Namespace owner is a typed runtime reference and semantic mismatch is rejected |
| Persisted event / audit hash rewrite | There is no hash, predecessor, rehash, migration, or lineage-commit syntax |
| Executable arbitrary behavior | No functions, calls, loops, VM, host bridge, network, or filesystem syntax exists |

## 5. Non-executable boundary audit criteria

A branch passes the language boundary audit only when it contains no production parser, compiler, interpreter, VM, bytecode engine, source evaluator, code generator, filesystem executor, network executor, runtime authority bridge, or source-to-runtime execution path. Safe validation may inspect grammar structure, schema validity, fixture consistency, or semantic classification without evaluating AION source.

## 6. Security validation requirements

Future parser implementations must run lexical, syntax, semantic, authority, identity, capability, version, and provisional-contract negative vectors. They must report stable semantic codes, but need not share human-readable wording. Parser disagreement on authority-sensitive source is a `CONFORMANCE_DEFECT`.

This document does not claim formal verification, complete security coverage, cross-parser parity, production readiness, or independent IV&V.

## References

[1]: AION_NATIVE_LANGUAGE_SEMANTIC_MODEL_V0.1.0.md "Source / AST / IR boundary and semantic checks"
[2]: AION_INTEROPERABILITY_PROFILE_V0.1.0.md "Strict JSON, Unicode, version, and error-envelope candidate rules"
[3]: AION_CROSS_LANGUAGE_CONTRACT_SURFACE_MAP_V0.1.0.md "Current Event / Lineage / audit divergence boundary"
