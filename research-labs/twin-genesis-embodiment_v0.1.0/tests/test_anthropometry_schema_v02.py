import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
import pytest

ROOT = Path(__file__).resolve().parents[1]


def _schema() -> dict[str, Any]:
    payload: dict[str, Any] = json.loads(
        (ROOT / "schemas/AION_ASTRA_ANTHROPOMETRY_V02_SCHEMA.json").read_text(encoding="utf-8")
    )
    Draft202012Validator.check_schema(payload)
    return payload


@pytest.mark.parametrize(
    "name",
    ["AION_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json", "ASTRA_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json"],
)
def test_profiles_match_schema(name: str) -> None:
    payload = json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))
    Draft202012Validator(_schema()).validate(payload)


def test_aion_archive_height_substitution_is_rejected() -> None:
    payload = json.loads(
        (ROOT / "data/AION_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json").read_text(encoding="utf-8")
    )
    payload["measurements"][0]["value"] = 180
    with pytest.raises(Exception):
        Draft202012Validator(_schema()).validate(payload)
