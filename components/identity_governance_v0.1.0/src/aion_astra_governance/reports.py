from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .errors import ConflictError


def public_value(value: Any, workspace: Path | None = None) -> Any:
    if isinstance(value, dict):
        return {key: public_value(item, workspace) for key, item in value.items()}
    if isinstance(value, list):
        return [public_value(item, workspace) for item in value]
    if isinstance(value, str) and workspace is not None:
        return value.replace(str(workspace.resolve()), "<WORKSPACE>")
    return value


def write_json_report(path: Path, data: dict[str, Any], workspace: Path | None = None) -> Path:
    if path.exists():
        raise ConflictError(f"report already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(public_value(data, workspace), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_markdown_report(path: Path, title: str, rows: list[tuple[str, str]]) -> Path:
    if path.exists():
        raise ConflictError(f"report already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", "", "| Field | Value |", "|---|---|"]
    lines.extend(f"| {field} | {value} |" for field, value in rows)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
