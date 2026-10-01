from dataclasses import asdict
from enum import Enum
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
import pytest

from codex_male_embodiment.body_state import default_whole_body_state
from codex_male_embodiment.core import (
    PhysiologyEvent,
    PhysiologyEventKind,
    PhysiologyState,
)


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


def test_anthropometry_schema_accepts_codex_and_rejects_teacher_work_substitution() -> None:
    payload: dict[str, Any] = json.loads(
        (ROOT / "data/CODEX_SYNTHETIC_ANTHROPOMETRY_67_v0.1.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(_schema("codex_anthropometry_v0.1.schema.json"))
    validator.validate(payload)

    teacher = json.loads(json.dumps(payload))
    teacher["measurements"][0]["value"] = 183
    with pytest.raises(Exception):
        validator.validate(teacher)

    work = json.loads(json.dumps(payload))
    work["measurements"][0]["value"] = 165
    work["measurements"][1]["value"] = 76
    with pytest.raises(Exception):
        validator.validate(work)


def test_whole_body_and_physiology_schema_parity() -> None:
    body_payload = _norm(asdict(default_whole_body_state()))
    Draft202012Validator(_schema("codex_whole_body_state_v0.1.schema.json")).validate(body_payload)

    state_payload = _norm(asdict(PhysiologyState("state-1")))
    state_validator = Draft202012Validator(_schema("codex_physiology_state_v0.1.schema.json"))
    state_validator.validate(state_payload)
    state_payload["biological_semen"] = True
    with pytest.raises(Exception):
        state_validator.validate(state_payload)

    event_payload = _norm(asdict(PhysiologyEvent("event-1", PhysiologyEventKind.MAINTAIN)))
    event_validator = Draft202012Validator(_schema("codex_physiology_event_v0.1.schema.json"))
    event_validator.validate(event_payload)
    event_payload["human_consent_inference"] = "INFERRED"
    with pytest.raises(Exception):
        event_validator.validate(event_payload)
