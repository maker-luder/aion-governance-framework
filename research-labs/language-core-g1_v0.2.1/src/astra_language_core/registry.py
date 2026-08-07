from __future__ import annotations

import json
import os
from pathlib import Path

from .errors import ArtifactExistsError, RegistryError, ValidationError
from .json_types import JsonValue
from .lineage import assert_baseline_unchanged, validate_lineage
from .models import ModelNode


class ModelRegistry:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> list[ModelNode]:
        if not self.path.exists():
            return []
        try:
            raw: JsonValue = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RegistryError(f"cannot load registry: {exc}") from exc
        if not isinstance(raw, list):
            raise RegistryError("registry root must be an array")
        nodes: list[ModelNode] = []
        for item in raw:
            if not isinstance(item, dict):
                raise RegistryError("registry entries must be objects")
            try:
                nodes.append(ModelNode.from_dict(item))
            except ValidationError as exc:
                raise RegistryError(str(exc)) from exc
        return nodes

    def create(self, nodes: list[ModelNode]) -> None:
        if self.path.exists():
            raise ArtifactExistsError(f"registry already exists: {self.path}")
        validate_lineage(nodes)
        self._write(nodes)

    def register(self, node: ModelNode) -> None:
        nodes = self.load()
        existing = next((item for item in nodes if item.model_id == node.model_id), None)
        if existing is not None:
            assert_baseline_unchanged(existing, node)
            raise RegistryError(f"model_id already registered: {node.model_id}")
        nodes.append(node)
        self._write(nodes)

    def _write(self, nodes: list[ModelNode]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps([node.to_dict() for node in nodes], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, self.path)
