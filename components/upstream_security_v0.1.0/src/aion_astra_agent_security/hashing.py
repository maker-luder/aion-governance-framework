from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any


def _default(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    raise TypeError(type(value).__name__)


def hash_record(value: Any) -> str:
    if is_dataclass(value) and not isinstance(value, type):
        value = asdict(value)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=_default)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
