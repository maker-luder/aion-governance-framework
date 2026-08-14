# CSOMI × SLSH Read-Only Integration Module v0.1.0

This lab is an isolated integration layer created from the CSOMI authority commit `87405c1877c6f016c303971da13923a1ab690aae`. The SLSH authority input is read through the frozen ref `frozen/slsh-semantic-reconciliation-20260814` at `893d8dc0c1c9d8f9a4188860520143c8d1d3977b`. Neither authority ref is modified, rebased, reset, cherry-picked, or semantically rewritten.

The module provides deterministic read-only git-object adapters, exact-SHA lineage records, a strict integration schema, and fail-closed validators for the small interface shared by the two frameworks. It preserves each framework's own claim types, evidence roles, controls, falsifiers, provenance and conclusions. It does not merge the frameworks' scientific semantics.

The module enforces the following boundaries:

> `RESEARCH_TOPIC != CAPABILITY != SCIENTIFIC_CONCLUSION`
>
> `CSOMI_EVIDENCE_CONVERGENCE != SUBJECTIVITY_PROOF`
>
> `SLSH_FUNCTIONAL_LOAD != SUBJECTIVE_LOAD`

The integration record is an adapter and consistency artifact only. It does not create a consciousness detector, runtime authority, experiment protocol, model modification, live-data collection path, canonical writeback, deployment, or scientific conclusion. Framework-specific disagreements are recorded as `PRESERVED_NOT_RECONCILED` metadata conditions and remain held for Human Owner or framework-authority review.

## Provenance layers

Research-origin provenance is stored separately for each frozen framework. CSOMI uses `HUMAN_OWNER_DIRECTION → CHATGPT_ARCHITECTURE_REFINEMENT`; SLSH uses `HUMAN_OWNER_ORIGIN → CHATGPT_ARCHITECTURE_REFINEMENT → CODEX_RESEARCH_SYNTHESIS → EXTERNAL_SOURCE`. These sequences describe research origin and architecture/input lineage, not source-audit processing.

The separately named `SOURCE_AUDIT_MATERIALIZATION_WORKFLOW` records source-record review and repository materialization only: `CODEX_RESEARCH_SYNTHESIS → CHATGPT_INDEPENDENT_SOURCE_REVIEW → HUMAN_OWNER_APPROVAL_OR_GOVERNANCE_DECISION → MANUS_IMPLEMENTATION`. This workflow must not be interpreted as the research-origin order, and Manus remains implementation-only rather than a scientific reviewer.

## Deterministic validation

From the repository root, run:

```bash
python3 scripts/materialize_csomi_slsh_integration.py
python3 scripts/check_csomi_slsh_integration.py
python3 -m pytest -q research-labs/csomi-slsh-integration_v0.1.0/tests
ruff check research-labs/csomi-slsh-integration_v0.1.0/src research-labs/csomi-slsh-integration_v0.1.0/tests scripts/materialize_csomi_slsh_integration.py scripts/check_csomi_slsh_integration.py
MYPYPATH=research-labs/csomi-slsh-integration_v0.1.0/src mypy --strict research-labs/csomi-slsh-integration_v0.1.0/src scripts/materialize_csomi_slsh_integration.py scripts/check_csomi_slsh_integration.py
python3 -m compileall -q research-labs/csomi-slsh-integration_v0.1.0/src scripts/materialize_csomi_slsh_integration.py scripts/check_csomi_slsh_integration.py
python3 -m json.tool schemas/aion_csomi_slsh_integration_v0.1.0.schema.json >/dev/null
```

The adapter resolves and verifies both exact commits before reading only the packet and schema paths declared in the integration contract. It intentionally does not read source dossiers or import source-level scientific semantics from either framework.

## Status

`CANONICAL_EFFECT=NONE`, `DEPLOYMENT=FALSE`, `EXPERIMENT_EXECUTED=NO`, `RUNTIME_EXECUTED=NO`, `MODEL_MODIFIED=FALSE`, `LIVE_DATA_COLLECTED=FALSE`, and `SUBJECTIVITY_CONCLUSION=NOT_ESTABLISHED`.

The module remains `INTEGRATION_MODULE_COMPLETE_PENDING_CHATGPT_OWNER_REVIEW` until ChatGPT and the Human Owner review the generated evidence. It must not be merged into `main` or promoted to a canonical or deployment path by this branch.
