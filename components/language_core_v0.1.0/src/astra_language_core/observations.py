from __future__ import annotations

import json
from pathlib import Path

from .errors import ValidationError
from .json_types import JsonValue


def load_observations(path: Path) -> list[dict[str, JsonValue]]:
    value: JsonValue = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValidationError("observations root must be an array")
    records: list[dict[str, JsonValue]] = []
    for item in value:
        if not isinstance(item, dict) or not isinstance(item.get("observation_id"), str):
            raise ValidationError("invalid observation record")
        if item.get("canonical_effect") != "NONE":
            raise ValidationError("observation canonical_effect must be NONE")
        records.append(item)
    return records
