import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "individual_runtime_context_v0.1.0.schema.json"


def _validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _context(agent_id: str = "AION") -> dict[str, str]:
    return {
        "agent_id": agent_id,
        "runtime_instance_id": f"{agent_id}-RUNTIME-001",
        "memory_stream_id": f"{agent_id}-MEMORY-001",
        "event_lineage_id": f"{agent_id}-EVENTS-001",
        "canonical_state_reference": f"{agent_id}-CANONICAL",
        "genesis_root_id": "ROOT-001",
    }


def test_schema_accepts_aion_and_astra_contexts_without_granting_identity_authority() -> None:
    validator = _validator()
    assert list(validator.iter_errors(_context("AION"))) == []
    assert list(validator.iter_errors(_context("ASTRA"))) == []


def test_schema_rejects_missing_required_context_fields() -> None:
    context = _context()
    context.pop("event_lineage_id")
    assert list(_validator().iter_errors(context))


def test_schema_rejects_blank_and_whitespace_only_strings() -> None:
    for field in _context():
        context = _context()
        context[field] = " "  # type: ignore[assignment]
        assert list(_validator().iter_errors(context)), field


def test_schema_rejects_type_coercion_and_unknown_fields() -> None:
    validator = _validator()
    wrong_type = _context()
    wrong_type["runtime_instance_id"] = 1  # type: ignore[assignment]
    assert list(validator.iter_errors(wrong_type))

    unknown_field = copy.deepcopy(_context())
    unknown_field["unreviewed_authority"] = "OWNER"  # type: ignore[assignment]
    assert list(validator.iter_errors(unknown_field))


def test_schema_contract_is_strictly_six_fields() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert schema["required"] == [
        "agent_id",
        "runtime_instance_id",
        "memory_stream_id",
        "event_lineage_id",
        "canonical_state_reference",
        "genesis_root_id",
    ]
    assert schema["additionalProperties"] is False
