from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import ConflictError
from .models import ResearchForkRecord
from .storage import load_json, write_new_json


class ResearchForkService:
    def __init__(self, root: Path) -> None:
        self.root = root

    def create(self, fork: ResearchForkRecord, parent: dict[str, Any], known_artifacts: set[str]) -> Path:
        if parent.get("state_id") != fork.parent_state_id or parent.get("state_hash") != fork.parent_state_hash:
            raise ConflictError("fork parent state or hash mismatch")
        if any(item not in known_artifacts for item in fork.artifact_ids):
            raise ConflictError("fork references an unknown artifact")
        target = self.root / fork.fork_id / "fork_record.json"
        return write_new_json(target, fork)

    def inspect(self, fork_id: str) -> dict[str, Any]:
        return dict(load_json(self.root / fork_id / "fork_record.json"))
