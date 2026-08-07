from __future__ import annotations

import json
import os
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from .errors import ConflictError, ValidationError
from .models import PathLikeGuard


def _default(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    raise TypeError(type(value).__name__)


def write_new_json(path: Path, value: Any) -> Path:
    if path.exists():
        raise ConflictError(f"output already exists: {path}")
    if PathLikeGuard.unsafe(path.as_posix()) and not path.is_absolute():
        raise ValidationError("unsafe output path")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = asdict(value) if is_dataclass(value) and not isinstance(value, type) else value
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    os.replace(temporary, path)
    return path


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))
