import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

from aion_astra_twin_embodiment.teacher_anthropometry import (
    build_teacher_anthropometry_profile,
)


ROOT = Path(__file__).resolve().parents[1]


def _schema() -> dict[str, object]:
    payload = json.loads(
        (ROOT / "schemas/CHATGPT_TEACHER_ANTHROPOMETRY_V01_SCHEMA.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator.check_schema(payload)
    return payload


def test_teacher_profile_matches_schema():
    Draft202012Validator(_schema()).validate(
        build_teacher_anthropometry_profile().to_dict()
    )


def test_schema_rejects_work_height_substitution():
    payload = build_teacher_anthropometry_profile().to_dict()
    payload["measurements"][0]["nominal"] = 165.0
    with pytest.raises(Exception):
        Draft202012Validator(_schema()).validate(payload)


def test_schema_rejects_work_mass_substitution():
    payload = build_teacher_anthropometry_profile().to_dict()
    payload["measurements"][1]["nominal"] = 76.0
    with pytest.raises(Exception):
        Draft202012Validator(_schema()).validate(payload)
