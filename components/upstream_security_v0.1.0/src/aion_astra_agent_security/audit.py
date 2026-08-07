from __future__ import annotations

import json
import os
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from .errors import ValidationError


def _default(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    raise TypeError(type(value).__name__)


def append_immutable_record(path: Path, record: Any) -> Path:
    if path.exists():
        raise ValidationError("audit records are immutable and cannot be overwritten")
    path.parent.mkdir(parents=True, exist_ok=True)
    value = asdict(record) if is_dataclass(record) and not isinstance(record, type) else record
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    os.replace(temporary, path)
    return path
