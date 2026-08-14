# CSOMI × SLSH Integration Module Status v0.1.0

## Status

`INTEGRATION_MODULE_COMPLETE_PENDING_CHATGPT_OWNER_REVIEW`

The isolated branch `integration/csomi-slsh-semantic-reconciliation-20260814` is based on the CSOMI authority commit `87405c1877c6f016c303971da13923a1ab690aae`. The SLSH authority is read through frozen ref `frozen/slsh-semantic-reconciliation-20260814` at `893d8dc0c1c9d8f9a4188860520143c8d1d3977b`. Both inputs are permanently read-only for this module.

The module has a narrow scope: exact-SHA authority identity, deterministic read-only adapters, shared interface projections, claim-boundary rules, evidence-role boundaries, provenance/lineage assertions, control/falsifier consistency, and fail-closed validation. It does not copy source records, reclassify sources, merge framework-specific claim semantics, or implement the conditional CSOMI interface previously recorded by SLSH.

## Non-equivalence boundaries

> `RESEARCH_TOPIC != CAPABILITY != SCIENTIFIC_CONCLUSION`
>
> `CSOMI_EVIDENCE_CONVERGENCE != SUBJECTIVITY_PROOF`
>
> `SLSH_FUNCTIONAL_LOAD != SUBJECTIVE_LOAD`

CSOMI mind-like inference and SLSH functional-load analysis remain separate namespaces. Controls are diagnostic, falsifiers down-date or hold only local claims, and no combination of records becomes a subjectivity or consciousness proof.

## Frozen input policy

| Framework | Authority ref | Exact SHA | Adapter policy |
|---|---|---|---|
| CSOMI | `research/cross-substrate-other-minds-inference-20260814` | `87405c1877c6f016c303971da13923a1ab690aae` | Read-only git-object adapter; mutation prohibited |
| SLSH | `frozen/slsh-semantic-reconciliation-20260814` | `893d8dc0c1c9d8f9a4188860520143c8d1d3977b` | Read-only git-object adapter; mutation prohibited |

The generated JSON record stores packet and schema SHA-256 hashes in addition to the authority commit SHAs. These hashes are lineage evidence, not scientific evidence.

## Provenance layers

Research-origin provenance is preserved independently by framework. CSOMI records `HUMAN_OWNER_DIRECTION → CHATGPT_ARCHITECTURE_REFINEMENT`. SLSH records `HUMAN_OWNER_ORIGIN → CHATGPT_ARCHITECTURE_REFINEMENT → CODEX_RESEARCH_SYNTHESIS → EXTERNAL_SOURCE`. These are research-origin and architecture/input lineages, not source-audit processing order.

The separate `SOURCE_AUDIT_MATERIALIZATION_WORKFLOW` records `CODEX_RESEARCH_SYNTHESIS → CHATGPT_INDEPENDENT_SOURCE_REVIEW → HUMAN_OWNER_APPROVAL_OR_GOVERNANCE_DECISION → MANUS_IMPLEMENTATION` for source-record review, admission and repository materialization only. It is not a research-origin sequence. Manus remains implementation-only and is not a scientific reviewer. The integration layer does not rewrite or collapse either authority's provenance.

## Fixed execution boundary

`CANONICAL_EFFECT=NONE`, `DEPLOYMENT=FALSE`, `EXPERIMENT_EXECUTED=NO`, `RUNTIME_EXECUTED=NO`, `MODEL_MODIFIED=FALSE`, `LIVE_DATA_COLLECTED=FALSE`, and `SUBJECTIVITY_CONCLUSION=NOT_ESTABLISHED`.

Any future resolution of framework-specific semantic differences remains `PRESERVED_NOT_RECONCILED` and is held for Human Owner or framework-authority review. This branch must not be merged into `main`, promoted canonically, or used to authorize an experiment/runtime/model/data operation.
