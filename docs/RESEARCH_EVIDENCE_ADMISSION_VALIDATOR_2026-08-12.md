# Research Evidence Admission Validator v0.1 — Reconciled Candidate

Status: `INSPECTION_ONLY / ADDITIVE / HUMAN_REVIEW_REQUIRED`

`validate_research_evidence.py` validates one declared evidence record against the `schemas/research_evidence_record_v0.2.0.schema.json` that exists on the current branch.

The validator is deliberately **schema-driven**. It does not define the research vocabulary itself:

- on `main`, the v0.2 schema remains bound to the main-native `SUBJECTIVITY_EVIDENCE_PROTOCOL` distinction;
- on the four-domain research branch, the v0.2 schema remains bound to the repository-native standing inference and controlled AB.6 references.

This keeps the authority direction:

```text
WHITEPAPER / REPOSITORY-NATIVE METHOD
        -> BRANCH-NATIVE SCHEMA
        -> ADMISSION VALIDATOR
```

not the reverse.

## Checks

The validator checks:

- JSON Schema 2020-12 validity;
- fixed branch-native non-claim boundaries encoded by the schema;
- declared local repository references where a reference uses a known in-tree path prefix;
- completed-result `code_commit` binding to an explicitly inspected Git head;
- `canonical_effect=NONE`;
- non-mutation of the evidence record.

`NOT_RUN` and `HOLD` records may remain explicitly unbound to the inspected head while execution is incomplete. Completed records may not claim a different source head.

## Outcomes

```text
PASS = structure, declared local references, head binding and fixed boundaries passed
HOLD = record/schema unavailable or incomplete for inspection
FAIL = structural/reference/head/boundary validation failed
```

These statuses are validator outcomes only.

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

The validator does not run the research protocol, inspect a model, infer a scientific result, mutate the record, or promote any claim.

## Local use

```bash
python scripts/validate_research_evidence.py \
  --root . \
  --record path/to/research_evidence_record.json \
  --expected-head "$(git rev-parse HEAD)"
```

Exit code `0` = PASS, `2` = FAIL, `10` = HOLD.

## Historical boundary

The additive v0.2 validator does not rewrite or retroactively require conversion of v0.1 historical evidence records. Historical v0.1 remains governed by its own schema and provenance.

## Provenance

- The need for a repeatable research-evidence admission surface originates in the Manus final delivery audit.
- The schema-driven reconciliation, branch-native vocabulary separation, local-reference traversal, source-head binding, and explicit non-claims in this candidate were added during ChatGPT research review.
- Human Research Owner retains final admission/acceptance authority.
- `CODEX_CONTRIBUTION_THIS_RECONCILIATION = NONE`.
