# AION Interoperability Profile v0.1.0

**Status:** `ESTABLISHED_CANDIDATE`

**Canonical effect:** `NONE`

**Deployment:** `FALSE`

This document defines the first shared semantic profile below the schema-field level. It is a language-neutral candidate contract. The Python functions in `aion_astra_runtime.interop` are a reference implementation and must not silently become the universal AION definition.

## Profile

| Primitive | v0.1.0 rule |
|---|---|
| Profile identifier | `AION-JCS-COMPATIBLE-0.1.0` |
| Schema version | Exact `0.1.0`; incompatible versions fail closed |
| Wire and canonical encoding | UTF-8 without a byte-order mark |
| Strings | Must be valid Unicode and NFC-normalized at security-sensitive admission; canonical serialization preserves accepted code points rather than normalizing them as a side effect |
| Identifiers | Non-empty, untrimmed, NFC-normalized strings with a maximum length of 256 code points; each contract may impose a narrower character policy |
| Timestamps | Exact UTC form `YYYY-MM-DDTHH:MM:SS.ffffffZ`; local offsets and unqualified local time are not admitted by this profile |
| Numbers | Safe integers only, bounded to `[-(2^53-1), 2^53-1]`; floats, NaN, Infinity, and ambiguous high-precision numbers are rejected |
| Missing / null / empty | Missing fields, `null`, empty strings, and empty collections are distinct; schemas explicitly state which are allowed |
| Duplicate JSON members | Rejected at raw-text parsing for security-sensitive contracts |
| Unknown fields | Rejected by default for authority-sensitive contracts |
| Enums | Unknown values fail closed; no silent defaulting |
| Object member order | Recursive lexicographic order over UTF-16 code units |
| Array order | Preserved; array order is semantic unless a contract explicitly says otherwise |
| Whitespace | No inter-token whitespace in canonical JSON |
| Hash | SHA-256 over the exact canonical UTF-8 bytes of the profile-defined object |
| Canonical effect | Always `NONE` in this candidate profile |

The profile is intentionally compatible in shape with the JSON Canonicalization Scheme, but AION explicitly chooses a narrower input subset for security-sensitive contracts. RFC 8785 is a technical reference, not an automatic authority for AION semantics. The profile preserves accepted Unicode strings as-is during canonicalization; NFC admission is a separate validation rule.

## Raw JSON admission

Raw JSON is parsed with duplicate-key detection and non-finite-number rejection before the value reaches schema or application validation. A parser must not silently coerce booleans to integers, strings to numbers, `null` to empty values, or repeated object members to whichever value happens to win in a language-specific parser.

A valid parsed value is recursively checked for supported JSON types, valid Unicode, NFC-normalized strings, safe integers, and finite numeric behavior. The candidate profile currently rejects floating-point numbers rather than attempting to standardize every implementation's binary64 edge case. A future profile may widen this only through a versioned contract and golden vectors.

## Timestamp admission

The profile uses a strict UTC microsecond representation. This is narrower than the full RFC 3339 grammar and deliberately excludes local offsets and leap-second text from v0.1.0. If a future contract needs those values, it requires a versioned profile and explicit conformance vectors rather than an implicit parser extension.

## Error semantics

Native exceptions are implementation details. Interoperable admission results use the Error Envelope fields `error_code`, `category`, `retryable`, `state_mutated`, `canonical_effect`, `message`, and `details`. Messages are diagnostic and may vary; error code and semantic outcome must not.

The current category set is `MALFORMED_INPUT`, `UNKNOWN_FIELD`, `UNSUPPORTED_VERSION`, `IDENTITY_MISMATCH`, `AUTHORITY_DENIED`, `INVALID_TRANSITION`, `CONFLICT`, `PERSISTENCE_FAILURE`, and `INTEGRITY_FAILURE`. No error in this profile may report a canonical effect other than `NONE`.

## Hash and compatibility boundary

The existing individual-runtime event chain and Astra workbench audit chain predate this profile and use different envelope shapes and genesis predecessor conventions. This profile therefore does not rewrite their persisted hashes. A future event-integrity implementation must use an explicit versioned hash profile and migration or legacy adapter vectors.

## Acceptance

Acceptance for this profile requires schema validity, raw parser rejection vectors, canonical text and byte golden vectors, timestamp vectors, version vectors, error-envelope vectors, and dependent runtime regression suites. Passing the Python reference tests is local implementation evidence; it is not cross-language parity or independent IV&V.

## References

[1]: https://unicode.org/reports/tr15/ "Unicode Standard Annex #15 — Unicode Normalization Forms"
[2]: https://www.rfc-editor.org/info/rfc3339/ "RFC 3339 — Date and Time on the Internet: Timestamps"
[3]: https://www.rfc-editor.org/rfc/rfc8259 "RFC 8259 — The JavaScript Object Notation (JSON) Data Interchange Format"
[4]: https://datatracker.ietf.org/doc/html/rfc8785 "RFC 8785 — JSON Canonicalization Scheme"
