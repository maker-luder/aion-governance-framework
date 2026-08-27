# Installation

## Scope

AION is a multi-package research repository, not a single published PyPI distribution. Install the specific component you intend to inspect or run. The CI matrix covers Python 3.11 and 3.12; component metadata requires Python 3.11 or newer.

## Source checkout

```powershell
git clone https://github.com/maker-luder/aion-governance-framework.git
cd aion-governance-framework
```

## Development install: Evidence Interop

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".\components\aion_evidence_interop_v0.1.0[dev]"
```

This installs `aion-evidence-interop`, an inspection-only exporter. It performs no model execution or network access.

## Focused test execution

```powershell
python -m pytest -q .\components\aion_evidence_interop_v0.1.0\tests
```

For repository-wide checks, use the commands and evidence semantics in [`../BUILD_AND_VERIFY.md`](../BUILD_AND_VERIFY.md). A test pass is engineering evidence only; it does not establish a scientific conclusion, release readiness, or merge authority.

## Other components

Each component has its own `pyproject.toml` and local README. Install it explicitly with `python -m pip install -e .\components\<component>[dev]` only after reading its local requirements and boundaries.
