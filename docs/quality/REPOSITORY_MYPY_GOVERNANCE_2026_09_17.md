# Repository-wide mypy governance — 2026-09-17

Status: `IMPLEMENTATION_CANDIDATE / QC_QA_CONTROL / NO_REPOSITORY_WIDE_PASS_CLAIM`

## 1. Purpose

This control implements the follow-up to `MYPY_QA_COVERAGE_GAP_RECORD_2026_09_17.md` without pretending that every existing Python package is already ready for identical strict typing.

The Human Owner approved the following quality architecture:

```text
existing mypy==2.3.1
        ↓
GitHub-hosted runner
        ↓
repository Python package discovery
        ↓
every active package receives one explicit disposition
        ↓
package-local mypy configuration where checking is required
        ↓
MYPYPATH / local source / PEP 561 boundary handling
        ↓
exact-head mypy evidence
        ↓
Quality / QMS
```

Source attribution:

```text
HUMAN_OWNER_APPROVAL
= approved repository-wide mypy governance as a QC/QA pillar

GPT_PROPOSED_OPERATIONALIZATION
= centralized disposition manifest + fail-closed package discovery + exact-head CI runner
```

## 2. Allowed dispositions

Every discovered `pyproject.toml` below the configured active Python roots must have exactly one repository policy entry.

```text
MYPY_REQUIRED_STRICT
= package must provide [tool.mypy] with strict = true and the CI runner executes mypy

MYPY_REQUIRED_CONFIGURED
= package must provide [tool.mypy] and the CI runner executes the package-specific configuration

EXEMPT_WITH_EXPLICIT_REASON
= package is not counted as a mypy pass; the reason must be explicit and visible
```

An exemption is a governed limitation, not success evidence.

```text
EXEMPT_WITH_EXPLICIT_REASON != MYPY_PASS
EXPLICIT_DISPOSITION != STATIC_TYPE_CORRECTNESS
POLICY_COVERAGE != TYPE_COVERAGE
```

## 3. Fail-closed discovery

The policy runner discovers Python package roots from:

```text
components/**/pyproject.toml
examples/**/pyproject.toml
experiments/**/pyproject.toml
research-labs/**/pyproject.toml
```

The discovered package-root set must exactly equal the package-root set in `.github/ci/mypy-policy.json`.

Therefore a new Python package cannot silently bypass static-type governance:

```text
NEW_PYPROJECT
+ NO_MYPY_DISPOSITION
= QUALITY_FAIL
```

A stale policy entry whose package no longer exists also fails closed.

## 4. Toolchain integrity

The policy names `mypy==2.3.1` as the current direct tool pin. Both the general Quality toolchain and Runtime Strong QA toolchain must contain that exact direct pin.

The runner also checks the executable version before running package checks.

```text
POLICY_VERSION
= INSTALLED_VERSION
= DIRECT_QA_PIN
= DIRECT_RUNTIME_STRONG_QA_PIN
```

A version mismatch is treated as a governance failure rather than silently accepting different checker semantics across QA lanes.

## 5. Package-local configuration

Required packages use their own `pyproject.toml` `[tool.mypy]` configuration. The central policy does not replace local typing contracts.

For packages with repository-owned cross-package imports, the policy may provide an explicit `mypy_path` source-root list. This preserves the existing Runtime Strong QA pattern where checked-out repository source is treated as typed local source rather than accidentally downgraded to an untyped third-party distribution merely because a PEP 561 marker is absent.

```text
CENTRAL_POLICY
= scope + disposition + execution binding

PACKAGE_PYPROJECT
= package typing semantics
```

## 6. Exact-head evidence

During Quality, the runner records the exact GitHub commit SHA and evaluates every required package. It can emit a machine-readable JSON record containing:

```text
target_head
mypy_version
package_count
required_check_count
exempt_count
all_required_checks_passed
repository_wide_mypy_pass
per-package results
```

The repository-wide pass field is intentionally conservative:

```text
ALL_REQUIRED_CHECKS_PASS
+ EXEMPT_COUNT > 0
= REPOSITORY_WIDE_MYPY_PASS = false
```

This prevents a successful bounded mypy run from being narrated as complete repository typing coverage.

## 7. Baseline migration state

At the 2026-09-17 baseline, packages that already contain strict local mypy configuration are promoted into executable `MYPY_REQUIRED_STRICT` checks. Pre-existing Python packages without local mypy configuration are recorded as `EXEMPT_WITH_EXPLICIT_REASON` rather than being silently ignored or being forced into an untested synthetic configuration.

This is a migration baseline, not the final desired coverage state.

The intended direction is monotonic reduction of justified exemptions where package semantics and dependency typing support it.

```text
BASELINE_EXEMPTION
!= PERMANENT_EXEMPTION

MYPY_REQUIRED_STRICT
SHOULD_NOT_REGRESS_TO_EXEMPT
WITHOUT_EXPLICIT_REVIEWED_REASON
```

## 8. QC / QA role

### QC — Quality Control

The executable checker inspects typed source and rejects incompatible type relationships for packages whose disposition requires checking.

### QA — Quality Assurance

The repository policy controls whether active packages are in scope, whether their disposition is explicit, whether required configuration exists, whether version pins remain aligned, and whether new packages can silently escape the control.

Thus mypy participates in both layers:

```text
MYPY_EXECUTION = QC_CONTROL
MYPY_SCOPE_AND_DISPOSITION_GOVERNANCE = QA_CONTROL
```

## 9. Boundaries

```text
MYPY_PASS != PROGRAM_CORRECTNESS
MYPY_PASS != TEST_PASS
MYPY_PASS != SECURITY_VALIDATION
MYPY_PASS != SCIENTIFIC_VALIDATION
MYPY_PASS != COMPLETE_RUNTIME_PATH_COVERAGE

PYTEST_PASS != MYPY_PASS
RUFF_PASS != MYPY_PASS
COMPILEALL_PASS != MYPY_PASS

EXEMPTION_RECORDED != EXEMPTION_JUSTIFIED_FOREVER
QUALITY_SUCCESS != REPOSITORY_WIDE_MYPY_PASS
```

The purpose of this control is not to inflate a QA score. It is to make static-type-analysis scope explicit, executable, traceable, and fail-closed against future silent drift.
