import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from aion_astra_runtime.models import IndividualRuntimeContext
from aion_astra_runtime.errors import PolicyDenied


ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = ROOT / "schemas" / "individual_runtime_context_v0.1.0.schema.json"
FIXTURE_PATH = ROOT / "conformance" / "individual_runtime_context_v0.1.0.json"


def _inputs() -> list[dict[str, object]]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert fixture["schema_version"] == "0.1.0"
    assert fixture["contract"] == schema["$id"]
    return fixture["vectors"]


def test_context_vectors_have_equivalent_schema_and_reference_parser_outcomes() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    for vector in _inputs():
        vector_id = vector["id"]
        context = vector["context"]
        expected = vector["expected"]
        schema_valid = not list(validator.iter_errors(context))

        if expected == "ACCEPT":
            assert schema_valid, vector_id
            assert isinstance(context, dict)
            parsed = IndividualRuntimeContext.from_dict(context)
            assert parsed.to_dict() == context, vector_id
        else:
            assert not schema_valid, vector_id
            with pytest.raises(PolicyDenied):
                IndividualRuntimeContext.from_dict(context)  # type: ignore[arg-type]


def test_conformance_fixture_contains_only_explicit_accept_or_reject_vectors() -> None:
    assert {vector["expected"] for vector in _inputs()} == {"ACCEPT", "REJECT"}
