from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_public_registry_does_not_fabricate_checkpoint_presence() -> None:
    registry = load("MODEL_REGISTRY_PUBLIC.json")
    assert registry["canonical_effect"] == "NONE"
    assert registry["deployment"] is False
    assert registry["independent_ivv"] == "NOT_ACHIEVED"
    assert len(registry["models"]) == 9
    assert all(item["repository_checkpoint_present"] is False for item in registry["models"])
    assert any(item["training_status"] == "RESOURCE_BLOCKED" for item in registry["models"])


def test_public_dataset_registry_preserves_no_private_material_boundary() -> None:
    registry = load("DATASET_REGISTRY_PUBLIC.json")
    assert len(registry["datasets"]) == 7
    assert all(item["repository_artifact_present"] is False for item in registry["datasets"])
    assert all(item["private_material_assessment"] == "NO_PRIVATE_MATERIAL" for item in registry["datasets"])


def test_local_evidence_files_are_present_without_production_claims() -> None:
    evidence = ROOT / "evidence"
    files = sorted(evidence.glob("LOCAL_*.json"))
    assert len(files) == 5
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        text = json.dumps(payload)
        assert "DEPLOYED" not in text or "NOT_DEPLOYED" in text
