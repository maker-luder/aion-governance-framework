# IQC Quality Inspection v0.1.0

This component is an **inspection-only** quality gate for the AION repository. It reads existing QA artifacts and emits a machine-readable inspection report. It does not modify source files, status locks, test results, manifests, canonical state, runtime state, deployment state, or research conclusions.

## Inputs

The inspector consumes `qa/CURRENT_TEST_RESULTS.json`, `qa/CURRENT_RELEASE_STATUS_LOCK.json`, `qa/CURRENT_COVERAGE_RESULTS.json`, `qa/CURRENT_COVERAGE_EVIDENCE.json`, and, when strict mode is enabled, `qa/CURRENT_QA_RECONCILIATION.json` and `qa/CURRENT_EVIDENCE_TRACEABILITY.json`. It also checks the external-standards crosswalk at `docs/C0_EXTERNAL_STANDARDS_CROSSWALK_2026-08-08.md`, the NCR/CAPA register at `qa/NCR_CAPA_REGISTER.md`, and the package contract of every test-bearing target. The checks are intentionally small and explicit so the existing Quality and Runtime Strong QA workflows remain the source of test execution evidence. Run the component matrix, `scripts/reconcile_current_qa.py`, `scripts/run_current_coverage.py`, and `scripts/generate_evidence_traceability.py` before strict IQC.

## Verdicts

`PASS` means the inspected artifacts are internally consistent and the closed governance boundaries are present. `HOLD` means evidence is missing, stale, or incomplete; it is not rewritten as a failure and cannot authorize acceptance. `FAIL` means a tested boundary is open or a target test returned a non-zero result.

The report always records `canonical_effect = NONE`, `independent_ivv_status = NOT_ACHIEVED`, `mutation_performed = false`, and `evaluator_role = REPOSITORY_IQC_INSPECTION_ONLY`.

## Local use

From the repository root:

For the current main matrix (19 targets):

```bash
PYTHONPATH=components/iqc_quality_inspection_v0.1.0/src \
python -m aion_iqc.cli \
  --root . \
  --target-head "$(git rev-parse HEAD)" \
  --expected-targets 19 \
  --require-traceability \
  --require-component-contracts \
  --require-qa-reconciliation
```

The main-maturation candidate target count is intentionally checked against the current component runner rather than a historical snapshot. The candidate is not a release, canonical state, or deployment.

A report can be written explicitly when a review artifact is needed:

```bash
PYTHONPATH=components/iqc_quality_inspection_v0.1.0/src \
python -m aion_iqc.cli --root . --target-head "$(git rev-parse HEAD)" \
  --expected-targets 19 \
  --require-traceability \
  --require-component-contracts \
  --require-qa-reconciliation \
  --output /tmp/aion-iqc-report.json
```

Strict mode adds three checks: `IQC-TRACE-001` validates the structural evidence traceability artifact without evaluating Owner acceptance; `IQC-PKG-001` requires `README.md` and `pyproject.toml` for each test-bearing target; and `IQC-RECON-001` compares current test results, the QA status lock, and the reconciliation envelope. Exit codes are `0` for `PASS`, `10` for `HOLD`, and `2` for `FAIL`. The default command emits JSON to stdout and does not create a file. A `PASS` is an internal evidence-consistency result only; it is not certification, deployment readiness, canonical promotion, independent IV&V or whole-system validation.

## Source-state binding

Strict adoption also requires `IQC-SRC-001`: the declared inspected head must match the actual Git HEAD, staged changes must be absent, and non-QA source drift must be absent. Bounded generated QA artifacts may exist after test execution; an uncommitted patched source worktree must not be described as exact HEAD-bound validation.
