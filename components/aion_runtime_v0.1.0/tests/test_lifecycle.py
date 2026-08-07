from __future__ import annotations

from aion_astra_runtime.models import IndividualRuntimeContext
from aion_runtime import AIONRuntime


def context(**changes: str) -> IndividualRuntimeContext:
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


def test_restart_reopens_same_event_lineage(tmp_path):
    memory_db = tmp_path / "memory.sqlite3"
    state_db = tmp_path / "state.sqlite3"
    first = AIONRuntime(memory_db=memory_db, state_db=state_db, context=context())
    first.record_start(reason="first")
    first.record_stop(reason="restart")

    restarted = AIONRuntime(memory_db=memory_db, state_db=state_db, context=context())
    restarted.record_start(reason="restart")
    assert [event.event_type for event in restarted.state.events()] == [
        "runtime.started",
        "runtime.stopped",
        "runtime.started",
    ]
    assert restarted.state.verify() is True


def test_checkpoint_recovery_and_migration_preserve_aion_lineage(tmp_path):
    memory_db = tmp_path / "memory.sqlite3"
    state_db = tmp_path / "state.sqlite3"
    runtime = AIONRuntime(memory_db=memory_db, state_db=state_db, context=context())
    runtime.record_start()
    checkpoint = runtime.checkpoint(
        checkpoint_id="AION-CP-001",
        state_reference="state:aion:001",
        memory_reference="memory:aion:001",
        owner_approved=True,
    )
    assert checkpoint.canonical_effect == "NONE"

    recovery = runtime.recover()
    assert recovery.lineage_valid is True
    assert recovery.checkpoint is not None
    assert recovery.checkpoint.checkpoint_id == "AION-CP-001"

    migrated = runtime.migrate_runtime(
        context(runtime_instance_id="AION-I-002"),
        owner_approved=True,
    )
    assert migrated.context.runtime_instance_id == "AION-I-002"
    assert migrated.context.event_lineage_id == runtime.context.event_lineage_id
    assert migrated.state.verify() is True
