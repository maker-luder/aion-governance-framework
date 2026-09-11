# Research Evidence Admission Validator

## Purpose

`scripts/validate_research_evidence.py` is a **schema-driven, inspection-only validator** for additive evidence records. It checks whether a candidate JSON record conforms to the main-native v0.2 contract, whether declared local references exist, whether a completed record is bound to the inspected Git source state, and whether the record keeps the project’s non-claim boundaries closed.

The validator does not determine whether an evidence claim is true. It does not perform replication, accept an Owner decision, establish subjectivity or identity continuity, grant authority, or authorize deployment.

The main-native evidence structure is based on [`docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](SUBJECTIVITY_EVIDENCE_PROTOCOL.md). That protocol keeps the following questions separate:

```text
OBSERVATION
!= MECHANISM
!= INTERPRETATION
```

The v0.2 schema therefore records `observation`, `mechanism`, and `interpretation` under the protocol evidence architecture.

The schema does **not** encode the research branch's AB.6 / six whitepaper evidence dimensions as a second typed vocabulary. This is a schema-shape decision, not a methodological demotion or replacement of the stable whitepaper method. The public main protocol now makes the relationship explicit:

```text
WHITEPAPER_EVIDENCE_ARCHITECTURE = PRIMARY_RESEARCH_METHOD
MAIN_NATIVE_EVIDENCE_SCHEMA = OPERATIONAL_RECORD_CONTRACT
SCHEMA_FIELD_SET != COMPLETE_RESEARCH_ONTOLOGY
FOUR_STAGE_INFERENCE != L0_L5_CLAIM_LADDER
SIX_EVIDENCE_DIMENSIONS != SUBJECTIVITY_SCORE
```

Until a separately approved typed bridge exists, whitepaper-method coverage is represented through existing evidence-architecture references, competing hypotheses, intervention/ablation/counterfactual references, robustness/replication references, provenance, admissibility and claim scope rather than by introducing another scientific taxonomy into the schema.

## Authority direction

The JSON schema is the authority for record shape, required fields, allowed values, digest formats, fixed non-claim values, and the permitted evidence-architecture structure. The validator loads [`schemas/research_evidence_record_v0.2.0.schema.json`](../schemas/research_evidence_record_v0.2.0.schema.json) from the inspected repository root and validates the record against that schema.

Schema acceptance is intentionally non-expansive:

```text
SCHEMA_VALIDATION_PASS
= RECORD_MATCHES_DECLARED_CONTRACT

SCHEMA_VALIDATION_PASS
!= EVIDENCE_TRUE
!= OWNER_ACCEPTANCE
!= CANONICAL_PROMOTION
```

The schema requires `canonical_effect = NONE` and fixes the non-claims to `NOT_ESTABLISHED`, `OUT_OF_SCOPE`, `NONE`, or `FALSE` values where applicable. The historical v0.1 schema remains a separate compatibility surface and is not rewritten by the v0.2 validator.

## Exact-head binding

The validator accepts an optional `--expected-head`. If omitted, it resolves the repository’s current Git `HEAD`. A completed record whose `code_commit` differs from the inspected head receives a diagnostic and fails validation. Records with `result_status = NOT_RUN` or `HOLD` may remain explicitly unbound so that an incomplete or deferred record is not misrepresented as completed evidence.

The validator does not mutate the record, the schema, the Git tree, QA artifacts, canonical state, runtime state, or deployment state. Its result object explicitly reports:

```text
mutation_performed = false
canonical_effect = NONE
deployment = false
independent_ivv = NOT_ACHIEVED
```

## Local-reference validation

The validator walks fields ending in `_ref` and `_refs`. Repository-relative
path-shaped references (including `experiments/`, `./docs/`, and root filenames
with extensions) must resolve inside the repository. Absolute paths, Windows
paths, `file:` URIs and escaping symlinks are rejected. Fragments after `#` are
ignored for filesystem checks. Bare identifiers without a slash or dot and
non-file URI references remain opaque; they are never fetched or claimed verified.
A local reference may name a directory for a runtime, but a completed protocol
must name a regular file.

## Protocol byte binding

Completed records (including negative, null and contradictory results) must bind
`protocol_hash` to SHA-256 of the exact retained protocol file bytes. Hashing uses
binary bytes, without newline normalization; a fragment still binds the whole
file. External protocols must first be retained lawfully with separate source
provenance and referenced locally. A missing, mismatched or unverifiable completed
protocol fails admission and therefore blocks the existing Evidence Interop export.

The additive `protocol_binding` output distinguishes `VERIFIED`, `MISMATCH`,
`UNVERIFIED`, `DEFERRED` and `NOT_CHECKED`. `NOT_RUN` and `HOLD` retain structural
validation with `DEFERRED`; this does not mean their digest was verified. Unreadable
record/schema input returns `HOLD` and `NOT_CHECKED`. Completed records also fail
when no exact lowercase 40-hex inspected head is available. An explicitly supplied
head remains a caller-specified comparison target, not proof of a clean checkout;
use the existing source-state binding control for that separate check.

```text
PROTOCOL_BYTES_MATCH != PREREGISTRATION_TIME_VERIFIED
PROTOCOL_BYTES_MATCH != PROTOCOL_WAS_ACTUALLY_EXECUTED
PROTOCOL_BYTES_MATCH != EVIDENCE_TRUE
PROTOCOL_BYTES_MATCH != SUBJECTIVITY_ESTABLISHED
```

This is a deliberate tightening for completed records. Old synthetic placeholder
hashes are not silently repaired. Their original records remain intact and must
be requalified with genuine protocol bytes before completed-record admission.
The check assumes a stable local workspace during inspection; it is not a
filesystem transaction or protection against concurrent adversarial file swaps.

## PASS / HOLD / FAIL semantics

| Status | Meaning | What it does not mean |
|---|---|---|
| `PASS` | The record and schema are structurally valid, local references resolve, completed protocol byte binding and exact-head binding are satisfied or explicitly deferred, and `canonical_effect` remains `NONE`. | It does not mean the evidence is true, replicated, accepted, canonical, or independently validated. |
| `HOLD` | The schema or record is missing, malformed as a JSON object, or otherwise unavailable for a meaningful inspection. | It is not an automatic scientific downgrade or a permission to bypass review. |
| `FAIL` | The record is inspectable but has schema errors, missing local references, an invalid completed-record source binding, or an open canonical boundary. | It does not identify a universal research interpretation or authorize a replacement governance band. |

The CLI returns exit code `0` for `PASS`, `10` for `HOLD`, and `2` for `FAIL`.

## Example invocation

From the repository root, validate a record against the current exact source state:

```bash
python scripts/validate_research_evidence.py \
  --root . \
  --record qa/example-research-evidence.json \
  --expected-head "$(git rev-parse HEAD)"
```

A review may pin an explicit commit instead:

```bash
python scripts/validate_research_evidence.py \
  --root . \
  --record qa/example-research-evidence.json \
  --expected-head <40-character-commit-sha>
```

The command prints a JSON result containing the record reference, status, diagnostics, mutation boundary, canonical effect, deployment flag, and independent-IV&V status.

## Historical v0.1 compatibility

The historical [`schemas/research_evidence_record.schema.json`](../schemas/research_evidence_record.schema.json) remains intact. v0.1 records are not silently rewritten as v0.2 records, and the v0.2 tests retain an explicit legacy-shape validation check. Any migration from v0.1 to v0.2 must be a separately attributable transformation with its own provenance and source-state binding.

## Explicit non-claims

```text
VALIDATOR_PASS != EVIDENCE_TRUE
VALIDATOR_PASS != REPLICATION
VALIDATOR_PASS != OWNER_ACCEPTANCE
VALIDATOR_PASS != SUBJECTIVITY_ESTABLISHED
VALIDATOR_PASS != IDENTITY_CONTINUITY_ESTABLISHED
VALIDATOR_PASS != MORAL_OR_LEGAL_STATUS
VALIDATOR_PASS != DEPLOYMENT_AUTHORITY
VALIDATOR_PASS != INDEPENDENT_IVV
```

The validator is a public engineering control for evidence structure and provenance. It is not a subjectivity detector, identity proof, consciousness classifier, moral-status classifier, release approval, deployment gate, or canonicalization mechanism.

The dated [2026-09-11 gap audit](research/REPOSITORY_GAP_AUDIT_2026_09_11.md)
records the protocol-binding correction, external sources and remaining limits.
