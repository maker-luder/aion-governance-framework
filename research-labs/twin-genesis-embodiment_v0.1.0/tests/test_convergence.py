from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

import aion_astra_twin_embodiment.convergence as convergence


ROOT = Path(__file__).parents[1]


def test_convergence_module_exists_for_archive_classification_contract() -> None:
    assert (
        importlib.util.find_spec("aion_astra_twin_embodiment.convergence")
        is not None
    ), "convergence module must exist before archive classifications can be loaded"


@pytest.mark.parametrize(
    "name",
    (
        "ConvergenceClassification",
        "AdoptionStatus",
        "ArchiveDisposition",
        "ConvergenceLedger",
        "load_convergence_ledger",
        "convergence_ledger_hash",
        "validate_convergence_ledger",
    ),
)
def test_convergence_public_contract_surface_exists(name: str) -> None:
    assert hasattr(convergence, name), f"missing convergence contract surface: {name}"


@pytest.mark.parametrize(
    "relative_path",
    (
        "data/EMBODIMENT_ARCHIVE_CONVERGENCE_LEDGER_v0.1.json",
        "schemas/EMBODIMENT_ARCHIVE_CONVERGENCE_LEDGER_SCHEMA.json",
    ),
)
def test_convergence_contract_artifacts_exist(relative_path: str) -> None:
    assert (ROOT / relative_path).is_file(), f"missing convergence artifact: {relative_path}"
