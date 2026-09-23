# Embodiment convergence v0.2 hardening — design addendum

## Authority and parent

This addendum continues the existing convergence branch at
`f4031fa0701822a1b1eb15909a8d367ca57134c7`. It does not replace the v0.1
foundation or import archive implementations. The repository remains a
synthetic engineering candidate with `CANONICAL_EFFECT=NONE`,
`DEPLOYMENT=FALSE`, and scientific/phenomenal conclusions `NOT_ESTABLISHED`.

## Goal

Replace broad archive buckets with a complete, machine-checkable semantic
coverage matrix for PRs #190, #191, #192, and the externally deferred PR #202.
Every relevant implementation module is inventoried, every semantic unit has
one owner, and source/target/replacement/support bindings are verifiable.

## Inventory definitions

Counts use explicit definitions rather than an ambiguous missing-module number:

- `implementation_module`: a non-plumbing Python module carrying embodiment,
  physiology, governance, role, avatar, or sensorimotor semantics.
- `teacher_module`: a PR #192 implementation module whose basename starts with
  `teacher_`.
- `explicit_v0_1_module`: a module whose basename appears in a PR-scoped v0.1
  ledger row.

Under those definitions PR #192 contains 19 relevant implementation modules:
two shared/provenance modules and 17 `teacher_` modules. Four were explicitly
named by v0.1, leaving 15 without PR-scoped explicit rows. PR #202 adds one
external implementation module, yielding the prior-review lower bound of 16.
These module counts are inventory diagnostics, not semantic-unit counts.

## Data model

`EMBODIMENT_ARCHIVE_COVERAGE_MATRIX_v0.2.json` contains:

1. Exact source heads for PRs #190/#191/#192/#202.
2. A source inventory with exact Git blob bindings and an explicit artifact
   kind for every reviewed source, schema, data, test, or document artifact.
3. Fine-grained semantic units containing primary source binding, source
   locator, embodiment axes, classification, disposition, logical target,
   optional active/replacement refs, explicit supporting artifact IDs, reason,
   claim ceiling, and review status.
4. Locked engineering/scientific boundaries and an inventory summary whose
   definitions are testable.

Classification and disposition are independent. `SHARED_CORE/DEFERRED` is
valid. `DEFERRED` units have no `active_target_ref`; `ADOPTED` units require a
real active target; `SUPERSEDED` units require a real replacement.

## Binding verification

Structural validation is deterministic and repository-independent. Repository
binding validation additionally uses Git object lookup to prove every source
and supporting artifact exists at its declared exact head and blob SHA. Active
targets and replacements must resolve to real current-tree files and optional
Python symbols. PR #202 is represented only as exact deferred provenance.

## Ownership and completeness

Every `semantic_unit_id` is unique. Each source locator has one semantic owner;
supporting artifacts may support multiple units but cannot own them. The source
inventory declares which implementation modules require semantic coverage, and
validation fails if any such module has no semantic unit. Final gates require:

```text
DUPLICATE_SEMANTIC_OWNERSHIP = 0
MISSING_UNACCOUNTED_COUNT = 0
```

## Canonical ordering and hashes

The canonical order is fixed as:

```text
(source_pr, source_path, semantic_unit_id)
```

Axes follow the schema-declared axis order; supporting artifact IDs are sorted.
Loaders reject noncanonical persisted order. Hashing also canonicalizes records,
so field or row input order cannot produce a second receipt for the same
semantic content. A disposition change must change the digest.

## Active baseline integration

The existing shared core and deferred Teacher extension remain the active
foundation. The active baseline binds the v0.2 matrix hash. Teacher extension
capabilities use unique semantic-unit IDs rather than broad source phrases.
The shared core remains independent of Teacher and Work extensions.

## Verification

TDD covers schema/runtime parity, exact heads and blobs, inventory counts,
unique ownership, complete source-module coverage, target/replacement
existence, PR #202 external/deferred boundaries, canonical hashes, and all
scientific/noncanonical locks. Final verification runs focused component tests,
repository root tests, Ruff, repository-policy mypy, a reverse review, and
remote exact-head CI when a matching run can be triggered without reopening the
closed PR.
