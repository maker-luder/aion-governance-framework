import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from aion_astra_runtime.models import IndividualRuntimeContext
from individual_runtime_state import IndividualRuntimeStateStore, RuntimeStateError


ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = ROOT / "schemas" / "individual_runtime_lifecycle_transition_request_v0.1.0.schema.json"
FIXTURE_PATH = ROOT / "conformance" / "individual_runtime_lifecycle_transition_request_v0.1.0.json"


def _context() -> IndividualRuntimeContext:
    return IndividualRuntimeContext(
        agent_id="AION",
        runtime_instance_id="AION-RUNTIME-001",
        memory_stream_id="AION-MEMORY-001",
        event_lineage_id="AION-EVENTS-001",
        canonical_state_reference="AION-CANONICAL",
        genesis_root_id="ROOT-001",
    )


def _vectors() -> list[dict[str, object]]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert fixture["schema_version"] == "0.1.0"
    assert fixture["contract"] == schema["$id"]
    Draft202012Validator.check_schema(schema)
    return fixture["vectors"]


def _seed(store: IndividualRuntimeStateStore, initial_events: list[str]) -> None:
    for event_type in initial_events:
        store.transition_lifecycle(event_type)


def test_lifecycle_requests_match_schema_and_admission_behavior(tmp_path) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    for vector in _vectors():
        vector_id = vector["id"]
        request = vector["request"]
        expected_result = vector["expected_result"]
        expected_final_state = vector["expected_final_state"]
        assert isinstance(request, (dict, list))
        schema_valid = not list(validator.iter_errors(request))
        assert schema_valid is (vector["request_schema"] == "VALID"), vector_id

        store = IndividualRuntimeStateStore(tmp_path / f"{vector_id}.sqlite3", _context())
        initial_events = vector["initial_events"]
        assert isinstance(initial_events, list)
        _seed(store, initial_events)
        before = [(event.sequence, event.event_type, event.event_hash) for event in store.events()]

        if expected_result == "ACCEPT":
            assert schema_valid, vector_id
            outcome = store.transition_lifecycle_request(request)
            assert outcome.from_state == vector["initial_state"], vector_id
            assert outcome.to_state == expected_final_state, vector_id
            assert outcome.event.event_type == request["event_type"]
            assert outcome.request.to_dict() == request
            assert store.lifecycle_state() == expected_final_state
            assert store.verify() is True
            assert len(store.events()) == len(before) + 1
        else:
            assert not (schema_valid and expected_result == "ACCEPT"), vector_id
            with pytest.raises(RuntimeStateError):
                store.transition_lifecycle_request(request)
            after = [(event.sequence, event.event_type, event.event_hash) for event in store.events()]
            assert after == before, vector_id
            assert store.lifecycle_state() == vector["expected_final_state"], vector_id
            assert store.verify() is True


def test_lifecycle_request_excludes_derived_state_and_implementation_claims() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert schema["required"] == ["event_type", "canonical_effect"]
    assert schema["additionalProperties"] is False
    assert set(schema["properties"]) == {"event_type", "canonical_effect"}


def test_lifecycle_fixture_contains_accepts_and_fail_closed_rejections() -> None:
    vectors = _vectors()
    assert {vector["expected_result"] for vector in vectors} == {"ACCEPT", "REJECT"}
    assert {vector["request_schema"] for vector in vectors} == {"VALID", "INVALID"}
