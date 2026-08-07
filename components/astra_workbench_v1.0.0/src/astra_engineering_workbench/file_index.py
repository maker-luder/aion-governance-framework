"""Deterministic workspace file index and hash-tree functions."""

from __future__ import annotations

import hashlib
from pathlib import Path


EXCLUDED_PARTS = {
    ".astra_meta",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "build",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def index_workspace(root: Path) -> tuple[tuple[str, int, str], ...]:
    records: list[tuple[str, int, str]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().lower()):
        relative = path.relative_to(root)
        if (
            not path.is_file()
            or any(part in EXCLUDED_PARTS or part.endswith(".egg-info") for part in relative.parts)
            or path.suffix.lower() in {".pyc", ".pyo"}
        ):
            continue
        records.append((relative.as_posix(), path.stat().st_size, sha256_file(path)))
    return tuple(records)


def workspace_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, size, file_hash in index_workspace(root):
        digest.update(f"{relative}\0{size}\0{file_hash}\n".encode("utf-8"))
    return digest.hexdigest()
