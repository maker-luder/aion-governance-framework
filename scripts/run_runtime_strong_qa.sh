#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

WHEELHOUSE="${RUNNER_TEMP:-/tmp}/aion-runtime-wheelhouse"
COLD_VENV="${RUNNER_TEMP:-/tmp}/aion-runtime-cold-venv"
rm -rf "$WHEELHOUSE" "$COLD_VENV"
mkdir -p "$WHEELHOUSE"

LOCAL_PACKAGES=(
  "components/governance_kernel_v0.4.0"
  "components/astra_workbench_v1.0.0"
  "research-labs/language-core-g1_v0.2.1"
  "components/executable_runtime_v0.1.0"
  "components/memory_recall_governance_v0.1.0"
  "components/individual_runtime_state_v0.1.0"
  "components/aion_runtime_v0.1.0"
  "components/astra_runtime_v0.1.0"
)

printf '\n== Editable local dependency chain ==\n'
for package in "${LOCAL_PACKAGES[@]}"; do
  python -m pip install --no-deps -e "$package"
done

printf '\n== mypy strict ==\n'
python -m mypy --config-file components/executable_runtime_v0.1.0/pyproject.toml components/executable_runtime_v0.1.0/src/aion_astra_runtime
python -m mypy --config-file components/individual_runtime_state_v0.1.0/pyproject.toml components/individual_runtime_state_v0.1.0/src/individual_runtime_state
python -m mypy --config-file components/aion_runtime_v0.1.0/pyproject.toml components/aion_runtime_v0.1.0/src/aion_runtime
python -m mypy --config-file components/astra_runtime_v0.1.0/pyproject.toml components/astra_runtime_v0.1.0/src/astra_runtime

printf '\n== Branch-aware coverage (minimum 80%% per changed Runtime component) ==\n'
python -m pytest -q components/executable_runtime_v0.1.0/tests \
  --cov=aion_astra_runtime --cov-branch --cov-report=term-missing --cov-fail-under=80
python -m pytest -q components/individual_runtime_state_v0.1.0/tests \
  --cov=individual_runtime_state --cov-branch --cov-report=term-missing --cov-fail-under=80
python -m pytest -q components/aion_runtime_v0.1.0/tests \
  --cov=aion_runtime --cov-branch --cov-report=term-missing --cov-fail-under=80
python -m pytest -q components/astra_runtime_v0.1.0/tests \
  --cov=astra_runtime --cov-branch --cov-report=term-missing --cov-fail-under=80

printf '\n== Wheel build ==\n'
for package in "${LOCAL_PACKAGES[@]}"; do
  python -m build --wheel --no-isolation --outdir "$WHEELHOUSE" "$package"
done
ls -1 "$WHEELHOUSE"

printf '\n== Cold offline installation from local wheelhouse ==\n'
python -m venv "$COLD_VENV"
"$COLD_VENV/bin/python" -m pip install \
  --no-index \
  --find-links "$WHEELHOUSE" \
  "aion-runtime==0.1.0" \
  "astra-runtime==0.1.0"

printf '\n== Cold import smoke ==\n'
"$COLD_VENV/bin/python" - <<'PY'
import aion_astra_runtime
import aion_governance_kernel
import aion_memory_recall
import aion_runtime
import astra_engineering_workbench
import astra_language_core
import astra_runtime
import individual_runtime_state

print("RUNTIME_STRONG_QA_IMPORT_SMOKE=PASS")
PY

printf '\nRUNTIME_STRONG_QA=PASS\n'
