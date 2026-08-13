# QA Summary

## Current cleanup-sandbox reconstruction

The repository's existing per-target runner, `scripts/run_component_tests.py`, completed **526 tests across 19 component, example, and research-lab targets** with return code 0 on the current cleanup sandbox. Running `pytest -q` once from the monorepo root is not the supported aggregate method because several targets intentionally reuse test-module basenames and some scopes require target-local import paths; the per-target result is therefore the authoritative local suite evidence for this reconstruction.

Branch-aware coverage remains recorded per target in `COVERAGE_REPORT.md`, and the Runtime Strong QA script completed with **PASS** for strict mypy, four changed Runtime component coverage gates at or above the pre-established 80% threshold, eight wheel builds, clean offline installation, and cold import smoke. The main Language Core and G1 mirror also have current strict mypy and Ruff evidence: 17 and 23 mypy source files respectively, with both configured Ruff scopes passing. The G1 mirror has 67 tests passing, including the model-free offline tokenizer/telemetry contract fixture.

Compileall, secret/privacy deterministic scans, manifest, and SHA-256 evidence remain subject to the scope and limitations stated in their respective reports. The current local results are **Manus-local engineering QA**, not GitHub Actions evidence, an independent IV&V result, a release decision, or scientific validation.

## Historical source evidence

The 2026-08-03 source public candidate reported 232 passing tests, five component mypy passes, wheel builds, and offline cold imports. Those records remain under `qa/historical/` and are not rewritten or treated as independent IV&V. The current cleanup run is a separate evidence layer and does not retroactively alter the locked release records.

## Conclusions and gates not established

Subjectivity, identity continuity, relational continuity, whole-system validation, and independent IV&V remain **not established**. Canonical promotion remains unauthorized, deployment remains false, and the final public license selection remains subject to the Owner gate. A local test, lint, type, coverage, build, or fixture pass does not convert a sandbox result into a canonical or research conclusion.
