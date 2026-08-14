import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from aion_astra_runtime.models import IndividualRuntimeContext
from individual_runtime_state import IndividualRuntimeStateStore, RuntimeStateError


ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = ROOT / "schemas" / "individual_runtime_lifecycle_transition_v0.1.0.schema.json"
FIXTURE_PATH = ROOT / "conformance" / "individual_runtime_lifecycle_transition_v0.1.0.json"


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


def test_lifecycle_vectors_match_schema_and_atomic_state_behavior(tmp_path) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    for vector in _vectors():
        vector_id = vector["id"]
        transition = vector["transition"]
        expected = vector["expected"]
        assert isinstance(transition, dict)
        schema_valid = not list(validator.iter_errors(transition))
        store = IndividualRuntimeStateStore(tmp_path / f"{vector_id}.sqlite3", _context())
        initial_events = vector["initial_events"]
        assert isinstance(initial_events, list)
        _seed(store, initial_events)
        before = [(event.sequence, event.event_type, event.event_hash) for event in store.events()]

        if expected == "ACCEPT":
            assert schema_valid, vector_id
            event = store.transition_lifecycle(str(transition["event_type"]))
            assert event.event_type == transition["event_type"]
            assert store.lifecycle_state() == transition["to_state"]
            assert store.verify() is True
            assert len(store.events()) == len(before) + 1
        else:
            assert not schema_valid, vector_id
            lifecycle_rejected = (
                transition["event_type"] == "runtime.started" and transition["from_state"] == "RUNNING"
            ) or (
                transition["event_type"] == "runtime.stopped"
                and transition["from_state"] in {"INITIALIZED", "STOPPED"}
            )
            if lifecycle_rejected:
                with pytest.raises(RuntimeStateError):
                    store.transition_lifecycle(str(transition["event_type"]))
            assert [(event.sequence, event.event_type, event.event_hash) for event in store.events()] == before
            assert store.lifecycle_state() == transition["from_state"]
            assert store.verify() is True


def test_lifecycle_fixture_contains_both_accepted_and_rejected_vectors() -> None:
    assert {vector["expected"] for vector in _vectors()} == {"ACCEPT", "REJECT"}
