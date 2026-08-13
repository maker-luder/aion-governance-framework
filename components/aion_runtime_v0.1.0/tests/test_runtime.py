from __future__ import annotations

from unittest.mock import Mock

import pytest

from aion_astra_runtime.models import IndividualRuntimeContext, TaskSpec
from aion_memory_recall.store import MemoryWriteDenied
from aion_runtime import AIONRuntime, RuntimeIdentityMismatch


def aion_context(**changes: str) -> IndividualRuntimeContext:
    values = {
        "agent_id": "AION",
        "runtime_instance_id": "AION-I-001",
        "memory_stream_id": "AION_PRIVATE_EPISODIC_MEMORY",
        "event_lineage_id": "AION-EVENT-LINEAGE-001",
        "canonical_state_reference": "AION_CANONICAL",
        "genesis_root_id": "ROOT-001",
    }
    values.update(changes)
    return IndividualRuntimeContext(**values)


def test_runtime_rejects_non_aion_context(tmp_path):
    with pytest.raises(RuntimeIdentityMismatch):
        AIONRuntime(
            memory_db=tmp_path / "memory.sqlite3",
            context=aion_context(agent_id="ASTRA"),
        )


def test_status_keeps_held_capabilities_closed(tmp_path):
    runtime = AIONRuntime(memory_db=tmp_path / "memory.sqlite3", context=aion_context())
    status = runtime.status()
    assert status.live_cross_session_memory == "ENABLED_GOVERNED"
    assert status.individual_runtime_binding == "ENFORCED_CANDIDATE"
    assert status.automatic_canonical_writeback == "DISABLED"
    assert status.canonical_promotion == "PENDING_OWNER_REVIEW"


def test_runtime_memory_round_trip_is_bound_to_aion_stream(tmp_path):
    runtime = AIONRuntime(memory_db=tmp_path / "memory.sqlite3", context=aion_context())
    common = dict(
        memory_id="m1",
        user_id="u1",
        content="runtime deployment decision",
        provenance_source="owner-input",
        provenance_verified=True,
        entities={"AION"},
        topics={"deployment"},
        access_scope={"project"},
    )
    with pytest.raises(MemoryWriteDenied):
        runtime.remember(writeback_approved=False, **common)

    stored = runtime.remember(writeback_approved=True, **common)
    assert stored.agent_id == "AION"
    assert stored.namespace == "AION_PRIVATE_EPISODIC_MEMORY"
    assert stored.canonical_effect == "NONE"

    recalled = runtime.recall(
        user_id="u1",
        requester_scopes={"project"},
        entity_cues={"AION"},
        topic_cues={"deployment"},
    )
    assert [item.memory_id for item in recalled] == ["m1"]


def test_task_context_must_match_bound_runtime_instance(tmp_path):
    runtime = AIONRuntime(memory_db=tmp_path / "memory.sqlite3", context=aion_context())
    task = TaskSpec.from_dict(
        {
            "task_id": "AION-MISMATCH-001",
            "objective": "Inventory and summarize",
            "profile": "INVENTORY_SUMMARIZE",
            "input_paths": ["input.txt"],
            "output_path": "out.txt",
            "owner_approved": True,
            "approved_by": "OWNER",
            "runtime_context": aion_context(runtime_instance_id="AION-I-OTHER").to_dict(),
        }
    )
    with pytest.raises(RuntimeIdentityMismatch):
        runtime.run_task(
            task,
            baseline_root=tmp_path,
            sessions_root=tmp_path,
        )


def test_recall_applies_bound_namespace_before_limit(tmp_path):
    runtime = AIONRuntime(memory_db=tmp_path / "memory.sqlite3", context=aion_context())
    common = dict(
        user_id="u1",
        content="candidate",
        provenance_source="owner-input",
        provenance_verified=True,
        entities={"AION"},
        topics={"deployment"},
        access_scope={"project"},
        writeback_approved=True,
    )
    runtime.memory.write(
        memory_id="a-foreign",
        namespace="ASTRA_PRIVATE_EPISODIC_MEMORY",
        agent_id="AION",
        **common,
    )
    runtime.remember(memory_id="z-bound", **common)

    recalled = runtime.recall(
        user_id="u1",
        requester_scopes={"project"},
        entity_cues={"AION"},
        topic_cues={"deployment"},
        limit=1,
    )

    assert [item.memory_id for item in recalled] == ["z-bound"]


def test_task_exception_is_recorded_before_propagation(tmp_path):
    execution = Mock()
    execution.run.side_effect = RuntimeError("planner failure")
    runtime = AIONRuntime(
        memory_db=tmp_path / "memory.sqlite3",
        context=aion_context(),
        execution=execution,
    )
    task = TaskSpec.from_dict(
        {
            "task_id": "AION-FAIL-001",
            "objective": "Inventory and summarize",
            "profile": "INVENTORY_SUMMARIZE",
            "input_paths": ["input.txt"],
            "output_path": "out.txt",
            "owner_approved": True,
            "approved_by": "OWNER",
            "runtime_context": aion_context().to_dict(),
        }
    )

    with pytest.raises(RuntimeError, match="planner failure"):
        runtime.run_task(task, baseline_root=tmp_path, sessions_root=tmp_path)

    assert [event.event_type for event in runtime.state.events()] == [
        "task.started",
        "task.failed",
    ]
