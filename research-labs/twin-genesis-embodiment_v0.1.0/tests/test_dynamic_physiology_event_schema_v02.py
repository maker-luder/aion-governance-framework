from dataclasses import asdict
from enum import Enum
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
import pytest

from aion_astra_twin_embodiment.dynamic_physiology import (
    PhysiologyEvent,
    PhysiologyEventKind,
)


ROOT = Path(__file__).resolve().parents[1]


def _norm(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {key: _norm(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_norm(item) for item in value]
    return value


def test_dynamic_physiology_event_schema_matches_runtime_guards() -> None:
    schema = json.loads(
        (ROOT / "schemas/AION_ASTRA_DYNAMIC_PHYSIOLOGY_EVENT_V02_SCHEMA.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    payload = _norm(asdict(PhysiologyEvent("init", PhysiologyEventKind.INITIATE, 0.5)))
    validator.validate(payload)
    payload["human_consent_inference"] = "INFERRED"
    with pytest.raises(Exception):
        validator.validate(payload)
