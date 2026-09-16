# Mypy QA coverage gap record — 2026-09-17

Status: `DOCUMENTATION_ONLY / NCR_SOURCE_RECORD / NO_IMPLEMENTATION_CHANGE`

## 1. Why this record exists

This record was opened after the Human Owner noticed that `mypy` had been omitted from a conversational summary of the repository's Python quality tooling. That omission triggered a repository inspection because `mypy` has historically been treated as a substantial QA control in several AION/Astra components.

This document records the observed coverage gap and the reason it matters. It does **not** implement a new repository-wide `mypy` policy. That implementation must be separately inspected, scoped, tested, and authorized.

```text
HUMAN_OWNER_ORIGINAL_OBSERVATION
= mypy is an important long-standing QC/QA pillar and must not silently disappear from quality governance

CHATGPT_TEACHER_ERROR
= conversationally summarized Python tooling without mentioning mypy, which prompted inspection

DOCUMENT_SCOPE
= RECORD_CURRENT_GAP_AND_ROOT_CAUSE_PATH

IMPLEMENTATION_CHANGE = NONE
```

## 2. Current repository facts

At the exact main state inspected before this record:

```text
MAIN_HEAD_AT_INSPECTION
= 143b9e1611b3c99ebc9f008eb92da2c5c14fd595
```

The general `.github/workflows/quality.yml` workflow installs the direct QA toolchain from `.github/ci/quality-toolchain.txt` and runs Ruff, pytest, compileall, component tests, coverage, source-state checks, evidence traceability, and IQC-related controls.

However, that general Quality workflow does **not** install or invoke `mypy`.

The general pinned toolchain currently contains:

```text
pytest==9.1.1
pytest-cov==7.1.0
jsonschema==4.26.0
ruff==0.16.4
```

A separate `Runtime Strong QA` workflow does install and invoke `mypy` through `.github/ci/runtime-strong-qa-toolchain.txt`, where the current direct pin is:

```text
mypy==2.3.1
```

The Runtime Strong QA script currently runs strict `mypy` for selected runtime packages, including:

```text
components/executable_runtime_v0.1.0
components/individual_runtime_state_v0.1.0
components/aion_runtime_v0.1.0
components/astra_runtime_v0.1.0
```

Multiple component `pyproject.toml` files also contain strict `mypy` configuration. This confirms that strict static typing is an established repository quality practice in several mature components.

At the same time, newer or differently scoped Python packages can exist without a component-local `[tool.mypy]` section. For example, at inspection time:

```text
research-labs/human-ai-longitudinal-study_v0.1.0/pyproject.toml
```

contained pytest configuration but no local mypy configuration.

Therefore:

```text
GENERAL_QUALITY_RUNS_MYPY = FALSE
RUNTIME_STRONG_QA_RUNS_MYPY = TRUE
RUNTIME_STRONG_QA_MYPY_SCOPE = SELECTED_RUNTIME_COMPONENTS
REPOSITORY_WIDE_CURRENT_MYPY_PASS = NOT_ESTABLISHED
QUALITY_SUCCESS != REPOSITORY_WIDE_MYPY_PASS
```

## 3. Why mypy is not interchangeable with pytest, Ruff, or compileall

`mypy` is a static type checker for Python. It analyzes annotated code without executing it and checks whether values, function arguments, return values, generics, unions, protocols, and other typed relationships are used consistently.

This gives it a different defect-detection surface from runtime tests and linting:

```text
pytest
= executes selected test cases and checks observed runtime behavior

Ruff
= lint/static source analysis for configured rule families

compileall
= verifies that Python source can compile to bytecode

mypy
= checks static type relationships across annotated code paths and interfaces
```

A test suite can pass while an untested call path still violates a declared type contract. Conversely, `mypy` can pass while the program still contains wrong business logic, security defects, incorrect scientific claims, or runtime behavior not represented by the type system.

Therefore:

```text
MYPY_PASS != PROGRAM_CORRECTNESS
MYPY_PASS != SECURITY_VALIDATION
MYPY_PASS != SCIENTIFIC_VALIDATION
PYTEST_PASS != STATIC_TYPE_CONSISTENCY_PROVEN
RUFF_PASS != MYPY_PASS
COMPILEALL_PASS != MYPY_PASS
```

Official mypy documentation describes mypy as a static type checker, emphasizes gradual typing, and notes that unannotated code may receive little or no checking unless stricter options are enabled. Strict mode enables additional checks such as disallowing untyped function definitions. This makes configuration and scope part of the quality evidence, not merely whether the `mypy` executable was invoked.

External references:

- https://mypy.readthedocs.io/en/latest/
- https://mypy.readthedocs.io/en/latest/getting_started.html
- https://mypy.readthedocs.io/en/latest/common_issues.html

## 4. Root-cause path observed in the repository

The current gap is not evidence that the repository intentionally abandoned `mypy`.

The observed path is instead:

```text
HISTORICAL_STRICT_MYPY_PRACTICE
-> strong typing adopted by multiple mature components
-> Runtime Strong QA retained a dedicated mypy lane
-> general Quality workflow evolved as a broader repository gate
-> general Quality toolchain did not absorb mypy
-> repository continued adding components / examples / research labs
-> not every new Python surface entered the Runtime Strong QA scope
-> a Quality SUCCESS could therefore exist without current mypy evidence for all changed Python code
```

This is a QA coverage/governance gap rather than a presently demonstrated code defect.

```text
KNOWN_TYPE_DEFECT = NOT_ESTABLISHED
QA_COVERAGE_GAP = OBSERVED
ROOT_CAUSE_CLASS
= STATIC_TYPE_ANALYSIS_SCOPE_DIVERGENCE_BETWEEN_QA_LANES
```

## 5. NCR-style interpretation

### Expected condition

For active Python code where static typing is part of the intended quality model, the repository should have an explicit and traceable mypy disposition.

### Observed condition

- General Quality does not install or run mypy.
- Runtime Strong QA does run strict mypy, but for a bounded subset of runtime packages.
- Some Python packages outside that lane can therefore be merged after Quality success without repository-wide current mypy evidence.

### Immediate containment

Until a repository-wide policy is explicitly established:

```text
DO_NOT_CLAIM_REPOSITORY_WIDE_MYPY_PASS
DO_NOT_INFER_MYPY_PASS_FROM_QUALITY_SUCCESS
HISTORICAL_MYPY_PASS != CURRENT_EXACT_HEAD_MYPY_PASS
```

### Corrective-action candidate

Determine the intended static-typing scope and make it executable rather than implicit.

Candidate explicit dispositions for each active Python package:

```text
MYPY_REQUIRED
MYPY_NOT_APPLICABLE_WITH_REASON
MYPY_DEFERRED_WITH_HOLD_OR_RECORDED_LIMITATION
```

### Preventive-action candidate

New Python packages should not silently fall outside the static-type-analysis policy. CI should be able to detect package-scope drift.

These are candidates only. This document does not authorize or implement them.

## 6. Can the repository use its existing mypy setup without a phone-local installation?

Yes, with an important distinction.

The repository does **not** currently contain a vendored `mypy` executable merely waiting to be copied out and run. Instead, it contains:

```text
1. a pinned dependency declaration (`mypy==2.3.1`) in the Runtime Strong QA toolchain;
2. GitHub Actions workflow logic that installs that toolchain on a GitHub-hosted runner;
3. a repository script that invokes strict mypy against selected source roots;
4. component-level mypy configurations in multiple packages.
```

Therefore a Human Owner using a phone does not need to install mypy locally in order for GitHub-hosted CI to run it. The current repository already demonstrates that pattern in Runtime Strong QA:

```text
GITHUB_HOSTED_RUNNER
-> pip install pinned QA toolchain
-> python -m mypy ...
-> CI result
```

What is **not yet established** is whether the same existing setup can be expanded safely to the entire active repository without configuration, typing, third-party-stub, performance, or scope problems.

That requires a separate inspection of:

```text
- all active Python source roots;
- existing [tool.mypy] configurations;
- packages with no mypy configuration;
- Any / untyped boundaries;
- missing third-party type information and PEP 561 behavior;
- Python 3.11 / 3.12 compatibility expectations;
- whether strict mode is appropriate everywhere;
- CI runtime and maintenance cost;
- whether generated/historical/vendor/example surfaces should be excluded.
```

So the current answer is:

```text
CAN_GITHUB_CI_RUN_MYPY_WITHOUT_PHONE_LOCAL_INSTALL = YES
REPOSITORY_ALREADY_DEMONSTRATES_THIS = YES
CAN_EXISTING_RUNTIME_MYPY_LANE_BE_BLINDLY_APPLIED_REPO_WIDE = NOT_ESTABLISHED
REPO_WIDE_MYPY_FEASIBILITY_REQUIRES_INSPECTION = YES
```

## 7. Quality-management standing

The Human Owner explicitly identifies mypy as a long-standing QC/QA pillar whose omission from quality governance should be treated seriously.

That owner position is recorded without converting it into an unreviewed technical mandate that every Python file must immediately use one identical strict configuration.

```text
HUMAN_OWNER_QUALITY_POSITION
= MYPY_MUST_NOT_SILENTLY_DISAPPEAR_FROM_QC_QA_GOVERNANCE

GPT_TEACHER_ANALYSIS
= the repository currently has a real static-type-analysis coverage gap between QA lanes

REPOSITORY_WIDE_POLICY
= TO_BE_DETERMINED_BY_FOLLOW_UP_INSPECTION
```

## 8. Boundaries

```text
DOCUMENT_RECORD != FIX
MYPY_EXISTS_IN_TOOLCHAIN != REPO_WIDE_MYPY_PASS
MYPY_STRICT_ON_SELECTED_COMPONENTS != STRICT_MYPY_ON_ALL_COMPONENTS
QUALITY_SUCCESS != ALL_POSSIBLE_QUALITY_CONTROLS_PASSED
STATIC_TYPE_ANALYSIS != TEST_EXECUTION
STATIC_TYPE_ANALYSIS != SCIENTIFIC_VALIDATION
```

Next action after this documentation-only record is merged: return to the current repository source, inventory the active Python surface, and determine whether the existing pinned mypy/GitHub Actions pattern can be extended repository-wide with bounded, evidence-backed changes.