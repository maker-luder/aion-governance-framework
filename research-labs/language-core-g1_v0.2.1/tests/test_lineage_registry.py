from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
from helpers import base_node, derived, lineage_nodes

from astra_language_core.errors import ArtifactExistsError, RegistryError, ValidationError
from astra_language_core.lineage import assert_baseline_unchanged, validate_lineage
from astra_language_core.registry import ModelRegistry


def test_valid_lineage_and_registry_create(tmp_path: Path) -> None:
    path = tmp_path / "registry.json"
    registry = ModelRegistry(path)
    registry.create(lineage_nodes())
    assert len(registry.load()) == 5
    with pytest.raises(ArtifactExistsError):
        registry.create(lineage_nodes())


def test_invalid_lineage_cases() -> None:
    with pytest.raises(ValidationError, match="missing"):
        validate_lineage([base_node()])
    nodes = lineage_nodes()
    nodes[-1] = derived("G1-ABLATION-TW-LORA", "UNKNOWN", "A_B_C_D_REQUIRED")
    with pytest.raises(ValidationError, match="unknown parent"):
        validate_lineage(nodes)
    nodes = lineage_nodes()
    nodes[-1] = derived("G1-ABLATION-TW-LORA", "G1-ABLATION-LOW", "missing prerequisite")
    with pytest.raises(ValidationError, match="prerequisite"):
        validate_lineage(nodes)


def test_duplicate_and_baseline_overwrite_rejected(tmp_path: Path) -> None:
    registry = ModelRegistry(tmp_path / "registry.json")
    registry.create(lineage_nodes())
    with pytest.raises(RegistryError, match="already"):
        registry.register(derived("G1-TW-LORA"))
    changed = replace(base_node(), display_name="changed")
    with pytest.raises(ValidationError, match="overwrite"):
        assert_baseline_unchanged(base_node(), changed)


def test_registry_rejects_corrupt_root(tmp_path: Path) -> None:
    path = tmp_path / "registry.json"
    path.write_text("{}", encoding="utf-8")
    with pytest.raises(RegistryError):
        ModelRegistry(path).load()
