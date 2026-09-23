from __future__ import annotations

import importlib
import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
SCHEMA_PATH = ROOT / "schemas" / "SHARED_EMBODIMENT_CORE_SCHEMA.json"

REQUIRED_SURFACE = (
    "ObservationDomain",
    "ObservabilityClass",
    "StaticBodyRegion",
    "ObservationInterface",
    "MotorInterface",
    "PhysiologySystemInterface",
    "SharedEmbodimentCore",
    "build_shared_embodiment_core",
    "shared_embodiment_core_hash",
    "validate_shared_embodiment_core",
)


def test_shared_core_module_and_public_surface_exist() -> None:
    spec = importlib.util.find_spec("aion_astra_twin_embodiment.shared_core")
    assert spec is not None, "shared_core module must exist"
    module = importlib.import_module("aion_astra_twin_embodiment.shared_core")
    missing = [name for name in REQUIRED_SURFACE if not hasattr(module, name)]
    assert missing == [], f"missing shared-core surface: {missing}"


def test_shared_core_schema_exists() -> None:
    assert SCHEMA_PATH.is_file(), "shared-core schema must exist"
