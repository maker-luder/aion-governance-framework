from __future__ import annotations

import pytest

from aion_astra_agent_substrate import RuntimeBinding, SubstrateError, normalize_native_trajectory


def _binding() -> RuntimeBinding:
    return RuntimeBinding.from_runtime_context(
        {
            "agent_id": "ASTRA",
            "runtime_instance_id": "ASTRA-I-001",
            "memory_stream_id": "ASTRA-MEM-001",
            "event_lineage_id": "ASTRA-EVT-001",
            "canonical_state_reference": "ASTRA-CANONICAL",
            "genesis_root_id": "GENESIS-001",
        },
        substrate_id="native-bounded-runtime",
        session_id="astra-native-001",
    )


def test_existing_bounded_runtime_audit_actions_normalize_to_same_contract() -> None:
    events = normalize_native_trajectory(
        [
            {"action": "runtime.started", "details": {"canonical_effect": "NONE"}},
            {"action": "planner.decision", "details": {"step": 1, "tool": "inventory"}},
            {"action": "tool.completed", "details": {"step": 1, "status": "PASS"}},
            {"action": "task.completed", "details": {"status": "PASS_PENDING_OWNER_REVIEW"}},
        ],
        binding=_binding(),
    )
    assert [event.sequence for event in events] == [1, 2, 3, 4]
    assert all(event.session_id == "astra-native-001" for event in events)
    assert all(event.family.value == "NATIVE_RUNTIME" for event in events)


def test_unknown_native_event_fails_closed() -> None:
    with pytest.raises(SubstrateError, match="unsupported"):
        normalize_native_trajectory(
            [{"action": "runtime.unbounded_magic", "details": {}}],
            binding=_binding(),
        )
