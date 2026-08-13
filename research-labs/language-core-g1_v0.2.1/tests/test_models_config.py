from __future__ import annotations

import json
from pathlib import Path

import pytest
from helpers import base_node

from astra_language_core.config import LabConfig, generation_settings, load_json_compatible_yaml
from astra_language_core.errors import ValidationError
from astra_language_core.models import ModelNode


def test_model_round_trip() -> None:
    original = base_node()
    assert ModelNode.from_dict(original.to_dict()) == original


@pytest.mark.parametrize("field,value", [("unknown", 1), ("parameter_count", "4B"), ("merged", "no")])
def test_model_rejects_unknown_or_wrong_type(field: str, value: object) -> None:
    data = base_node().to_dict()
    data[field] = value  # type: ignore[assignment]
    with pytest.raises(ValidationError):
        ModelNode.from_dict(data)


def test_root_and_hash_rules() -> None:
    with pytest.raises(ValidationError):
        ModelNode("X", "x", "G1", None)
    with pytest.raises(ValidationError):
        ModelNode("X", "x", "G1", "G1-BASE", sha256="bad")


def test_config_and_generation(tmp_path: Path) -> None:
    path = tmp_path / "lab.yaml"
    path.write_text(
        json.dumps(
            {
                "project_identity": "AION／Astra",
                "subsystem": "Lab",
                "model_family_status": "EXPERIMENTAL_RESEARCH_FAMILY",
                "artifact_root": "a",
                "registry_path": "r.json",
                "dataset_path": "d.jsonl",
            }
        ),
        encoding="utf-8",
    )
    cfg = LabConfig.from_dict(load_json_compatible_yaml(path), tmp_path)
    assert cfg.artifact_root == (tmp_path / "a").resolve()
    assert generation_settings({"seed": 2}).seed == 2
    with pytest.raises(ValidationError):
        generation_settings({"mystery": True})


def test_bad_config(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("not-json", encoding="utf-8")
    with pytest.raises(ValidationError):
        load_json_compatible_yaml(path)
