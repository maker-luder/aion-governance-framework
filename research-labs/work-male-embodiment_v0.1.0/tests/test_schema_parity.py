from dataclasses import asdict
from enum import Enum
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

from work_male_embodiment.body_state import default_whole_body_state


ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
SCHEMAS = ROOT / "schemas"
PROFILE = REPO / "docs/research/embodiment/WORK_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json"


def plain(value):
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {key: plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(item) for item in value]
    return value


def load_schema(name):
    schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def test_profile_schema_accepts_exact_v02_and_rejects_changed_human_fixed_value():
    schema = load_schema("work_synthetic_anthropometry_v0.2.schema.json")
    payload = json.loads(PROFILE.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(payload)
    bad = json.loads(PROFILE.read_text(encoding="utf-8"))
    bad["measurements"][0]["value"] = 166
    with pytest.raises(Exception):
        Draft202012Validator(schema).validate(bad)


def test_whole_body_schema_accepts_python_state_and_rejects_fake_hardware():
    schema = load_schema("work_whole_body_state_v0.1.0.schema.json")
    payload = plain(asdict(default_whole_body_state()))
    Draft202012Validator(schema).validate(payload)
    payload["signals"][0]["physical_hardware_attached"] = True
    with pytest.raises(Exception):
        Draft202012Validator(schema).validate(payload)
