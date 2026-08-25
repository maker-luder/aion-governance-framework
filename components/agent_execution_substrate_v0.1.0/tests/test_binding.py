from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from aion_astra_agent_substrate import RuntimeBinding, SubstrateError


COMPONENT = Path(__file__).resolve().parents[1]


def _context(agent_id: str) -> dict[str, str]:
    return {
        "agent_id": agent_id,
        "runtime_instance_id": f"{agent_id}-I-001",
        "memory_stream_id": f"{agent_id}-MEMORY-001",
        "event_lineage_id": f"{agent_id}-EVENTS-001",
        "canonical_state_reference": f"{agent_id}-CANONICAL",
        "genesis_root_id": "TWIN-GENESIS-001",
    }


def test_binding_accepts_existing_aion_and_astra_runtime_context_shapes() -> None:
    aion = RuntimeBinding.from_runtime_context(
        _context("AION"),
        substrate_id="dsh-pinned",
        session_id="aion-session",
    )
    astra = RuntimeBinding.from_runtime_context(
        _context("ASTRA"),
        substrate_id="dsh-pinned",
        session_id="astra-session",
    )
    assert aion.agent_id.value == "AION"
    assert astra.agent_id.value == "ASTRA"
    assert aion.genesis_root_id == astra.genesis_root_id
    assert aion.session_id != astra.session_id
    assert aion.memory_stream_id != astra.memory_stream_id
    assert aion.event_lineage_id != astra.event_lineage_id


def test_binding_rejects_unknown_agent() -> None:
    with pytest.raises(SubstrateError, match="limited to AION or ASTRA"):
        RuntimeBinding.from_runtime_context(
            _context("OTHER"),
            substrate_id="native",
            session_id="session",
        )


def test_binding_rejects_blank_existing_runtime_identifiers() -> None:
    raw = _context("AION")
    raw["event_lineage_id"] = ""
    with pytest.raises(SubstrateError, match="event_lineage_id"):
        RuntimeBinding.from_runtime_context(
            raw,
            substrate_id="native",
            session_id="session",
        )


def test_binding_json_schema_matches_runtime_binding_output() -> None:
    schema = json.loads((COMPONENT / "schemas/substrate_binding_v0.1.0.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    binding = RuntimeBinding.from_runtime_context(
        _context("AION"),
        substrate_id="native",
        session_id="session",
    )
    Draft202012Validator(schema).validate(binding.to_dict())
