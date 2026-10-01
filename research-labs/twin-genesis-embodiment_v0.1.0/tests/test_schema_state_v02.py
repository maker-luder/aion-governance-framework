from dataclasses import asdict
from enum import Enum
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
import pytest

from aion_astra_twin_embodiment.body_state import default_whole_body_state
from aion_astra_twin_embodiment.dynamic_physiology import default_physiology_state

ROOT = Path(__file__).resolve().parents[1]


def _schema(name: str) -> dict[str, Any]:
    payload: dict[str, Any] = json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(payload)
    return payload


def _norm(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {key: _norm(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_norm(item) for item in value]
    return value


@pytest.mark.parametrize("agent", ["AION", "ASTRA"])
def test_whole_body_state_schema(agent: str) -> None:
    payload = _norm(asdict(default_whole_body_state(agent)))
    Draft202012Validator(_schema("AION_ASTRA_WHOLE_BODY_STATE_V02_SCHEMA.json")).validate(payload)


@pytest.mark.parametrize("agent", ["AION", "ASTRA"])
def test_dynamic_physiology_state_schema(agent: str) -> None:
    payload = _norm(asdict(default_physiology_state(agent)))
    validator = Draft202012Validator(
        _schema("AION_ASTRA_DYNAMIC_PHYSIOLOGY_STATE_V02_SCHEMA.json")
    )
    validator.validate(payload)
    payload["subjectivity"] = "ESTABLISHED"
    with pytest.raises(Exception):
        validator.validate(payload)
