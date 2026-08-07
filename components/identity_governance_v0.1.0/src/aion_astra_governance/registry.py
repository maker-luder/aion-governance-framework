from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import ConflictError, ValidationError
from .models import CapabilityArtifactRecord, ProjectIdentityRecord
from .storage import load_json, write_new_json


class ProjectIdentityRegistry:
    def __init__(self, root: Path) -> None:
        self.root = root

    def register(self, record: ProjectIdentityRecord) -> Path:
        return write_new_json(self.root / f"{record.project_id}.json", record)

    def load(self, project_id: str) -> dict[str, Any]:
        return dict(load_json(self.root / f"{project_id}.json"))


class CapabilityRegistry:
    """Single capability registry; Language Core model nodes enter through the adapter below."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def register(self, record: CapabilityArtifactRecord) -> Path:
        return write_new_json(self.root / f"{record.artifact_id}.json", record)

    def ids(self) -> set[str]:
        if not self.root.exists():
            return set()
        return {path.stem for path in self.root.glob("*.json")}

    def verify(self, artifact_id: str) -> bool:
        path = self.root / f"{artifact_id}.json"
        if not path.is_file():
            return False
        data = load_json(path)
        return isinstance(data, dict) and data.get("artifact_id") == artifact_id

    @staticmethod
    def from_language_core_node(node: dict[str, Any]) -> CapabilityArtifactRecord:
        model_id = node.get("model_id")
        if not isinstance(model_id, str):
            raise ValidationError("Language Core node lacks model_id")
        mapping = {
            "G1-BASE": "LANGUAGE_MODEL_BASELINE",
            "G1-TW-LORA": "LANGUAGE_ADAPTER",
            "G1-ABLATION-LOW": "MODIFIED_MODEL",
            "G1-RANDOM-CONTROL": "RESEARCH_CONTROL",
            "G1-ABLATION-TW-LORA": "MODIFIED_MODEL",
        }
        return CapabilityArtifactRecord(
            artifact_id=model_id,
            capability_type=mapping.get(model_id, "LANGUAGE_MODEL_CANDIDATE"),
            display_name=str(node.get("display_name", model_id)),
            revision=str(node.get("family_generation", "UNKNOWN")),
            upstream_source=str(node.get("upstream_model_name", "UNKNOWN")),
            upstream_developer=str(node.get("upstream_developer", "UNKNOWN")),
            upstream_license=str(node.get("upstream_license", "NOT_VERIFIED")),
            model_family=str(node.get("family_generation", "UNKNOWN")),
            base_model=str(node.get("parent_model_id", "UNKNOWN")),
            modification_type=str(node.get("modification_type", "UNKNOWN")),
            file_format=str(node.get("source_format", "UNKNOWN")),
            quantization=str(node.get("quantization", "UNKNOWN")),
            local_path=node.get("source_path") if isinstance(node.get("source_path"), str) else None,
            sha256=str(node.get("sha256") or "UNKNOWN"),
            status="EXPERIMENTAL",
            notes="Imported through Language Core adapter; project identity inheritance denied.",
        )

    def export(self, artifact_id: str) -> dict[str, Any]:
        path = self.root / f"{artifact_id}.json"
        if not path.exists():
            raise ConflictError(f"unknown artifact: {artifact_id}")
        return dict(load_json(path))
