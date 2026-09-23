# Embodiment convergence v0.2 hardening implementation plan

**Spec:** `docs/superpowers/specs/2026-09-23-embodiment-convergence-v0.2-hardening-design.md`

## Global constraints

- Continue `research/embodiment-convergence-20260923` from exact head
  `f4031fa0701822a1b1eb15909a8d367ca57134c7`.
- No reset, clean, force push, main mutation, merge, PR reopen, ready transition,
  PR #202 mutation/import, or Phase B work.
- TDD for every production behavior.
- `ENGINEERING_PASS != SCIENTIFIC_VALIDATION` and all phenomenal conclusions
  remain `NOT_ESTABLISHED`.

## Task 1 — Lock inventory definitions and v0.2 schema contract

**Files:**

- Create `tests/test_coverage_matrix_v0_2.py`.
- Create `schemas/EMBODIMENT_ARCHIVE_COVERAGE_MATRIX_SCHEMA.json`.
- Create `data/EMBODIMENT_ARCHIVE_COVERAGE_MATRIX_v0.2.json`.

**RED:** tests require exact heads, the explicit PR #192 19/17/4/15 count
definitions, the PR #202 external source set, all required row fields, all 19
axes, canonical row order, and schema/runtime parity.

**GREEN:** materialize the schema and exact artifact inventory with Git blob
bindings.

## Task 2 — Implement structural and repository binding validation

**Files:**

- Create `src/aion_astra_twin_embodiment/coverage_matrix.py`.
- Extend `tests/test_coverage_matrix_v0_2.py`.
- Export the new public surface from `src/aion_astra_twin_embodiment/__init__.py`.

**RED:** invented source, wrong blob, missing target, fake replacement,
archive-only active ref, deferred active ref, duplicate unit/ownership, uncovered
module, unknown axis, and noncanonical ordering must fail.

**GREEN:** typed loader, structural validation, Git/file/symbol binding
validation, gate counts, and canonical content hash.

## Task 3 — Replace broad Teacher capability bindings

**Files:**

- Modify `src/aion_astra_twin_embodiment/role_extensions.py`.
- Modify `src/aion_astra_twin_embodiment/active_baseline.py`.
- Modify `tests/test_role_extensions.py`.
- Modify `tests/test_active_baseline.py`.

**RED:** every Teacher capability maps to one unique v0.2 semantic unit and no
broad runtime/avatar/channel bucket is accepted.

**GREEN:** bind explicit deferred semantic-unit IDs and the v0.2 matrix hash
without importing archive runtime code.

## Task 4 — Documentation and review surfaces

**Files:**

- Modify `README.md`.
- Modify `docs/EMBODIMENT_CONVERGENCE_CROSSWALK_2026_09_23.md`.

Document exact counts, canonical ordering, binding gates, PR #202 external
deferred status, repository-native test command, and claim boundaries.

## Task 5 — Verification, reverse review, commit, push, and CI

Run focused tests, the component runner, root tests, Ruff, repository-policy
mypy, compile checks, matrix binding verification, and an independent reverse
review of the exact diff. Commit only Phase A v0.2 changes, push fast-forward to
the existing branch, verify the new exact remote head, and obtain/inspect remote
exact-head CI without changing PR #203 from `CLOSED / DRAFT / NOT_MERGED`.
