from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .errors import ValidationError
from .json_types import JsonValue


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def shard_manifest(root: Path, paths: list[Path]) -> dict[str, JsonValue]:
    resolved_root = root.resolve()
    records: list[JsonValue] = []
    seen: set[str] = set()
    for path in sorted(paths, key=lambda item: item.as_posix()):
        resolved = path.resolve()
        try:
            relative = resolved.relative_to(resolved_root).as_posix()
        except ValueError as exc:
            raise ValidationError(f"model shard escapes root: {path}") from exc
        if relative in seen or not resolved.is_file():
            raise ValidationError(f"duplicate or missing model shard: {relative}")
        seen.add(relative)
        records.append({"path": relative, "size": resolved.stat().st_size, "sha256": sha256_file(resolved)})
    canonical = json.dumps(records, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {
        "algorithm": "SHA-256",
        "record_count": len(records),
        "records": records,
        "manifest_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
    }
