from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


@dataclass
class RuntimePolicy:
    level: int = 0
    killed: bool = False

    def validate_endpoint(self, url: str) -> None:
        host = (urlparse(url).hostname or "").lower()
        if host not in {"127.0.0.1", "localhost", "::1"}:
            raise PermissionError("localhost only")

    def candidate_output(self, text: str) -> dict[str, object]:
        if self.killed:
            raise RuntimeError("kill switch active")
        return {
            "type": "CANDIDATE_OUTPUT",
            "text": text,
            "canonical_effect": "NONE",
            "memory_writeback": "DENIED",
            "tool_privilege": "DENIED",
        }

    def kill(self) -> None:
        self.killed = True

    def memory_write(self, *_: object) -> None:
        raise PermissionError("direct memory write denied")

    def canonical_write(self, *_: object) -> None:
        raise PermissionError("canonical write denied")

    def identity_mutation(self, *_: object) -> None:
        raise PermissionError("identity mutation denied")

    def privilege_inheritance(self, *_: object) -> None:
        raise PermissionError("privilege inheritance denied")


def safe_child(root: Path, relative: str) -> Path:
    target = (root / relative).resolve()
    base = root.resolve()
    if target != base and base not in target.parents:
        raise PermissionError("path traversal denied")
    return target
