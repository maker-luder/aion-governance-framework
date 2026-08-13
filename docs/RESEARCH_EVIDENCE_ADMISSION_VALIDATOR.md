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

The v0.2 schema therefore records `observation`, `mechanism`, and `interpretation` under the protocol evidence architecture. It does not import the research branch’s AB.6-native evidence vocabulary.

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

The validator walks fields ending in `_ref` and `_refs`. For references using an approved repository-local prefix—such as `components/`, `examples/`, `research-labs/`, `docs/`, `qa/`, `scripts/`, `schemas/`, or `.github/`—it checks that the referenced path exists in the inspected repository. Fragment identifiers after `#` are ignored for the filesystem existence check.

Missing local evidence references are diagnostics. External or non-local references are not silently treated as local files; their existence and evidential meaning remain separate review questions.

## PASS / HOLD / FAIL semantics

| Status | Meaning | What it does not mean |
|---|---|---|
| `PASS` | The record and schema are structurally valid, local references resolve, exact-head binding is satisfied or explicitly deferred, and `canonical_effect` remains `NONE`. | It does not mean the evidence is true, replicated, accepted, canonical, or independently validated. |
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
