from __future__ import annotations

from aion_astra_runtime.models import IndividualRuntimeContext
from astra_runtime import AstraRuntime


def context(**changes: str) -> IndividualRuntimeContext:
    values = {
        "agent_id": "ASTRA",
        "runtime_instance_id": "ASTRA-I-001",
        "memory_stream_id": "ASTRA_RESEARCH_EPISODIC_MEMORY",
        "event_lineage_id": "ASTRA-EVENT-LINEAGE-001",
        "canonical_state_reference": "ASTRA_CANONICAL",
        "genesis_root_id": "ROOT-001",
    }
    values.update(changes)
    return IndividualRuntimeContext(**values)


def test_restart_reopens_same_event_lineage(tmp_path):
    memory_db = tmp_path / "memory.sqlite3"
    state_db = tmp_path / "state.sqlite3"
    first = AstraRuntime(memory_db=memory_db, state_db=state_db, context=context())
    first.record_start(reason="first")
    first.record_stop(reason="restart")

    restarted = AstraRuntime(memory_db=memory_db, state_db=state_db, context=context())
    restarted.record_start(reason="restart")
    assert [event.event_type for event in restarted.state.events()] == [
        "runtime.started",
        "runtime.stopped",
        "runtime.started",
    ]
    assert restarted.state.verify() is True


def test_checkpoint_recovery_and_migration_preserve_astra_lineage(tmp_path):
    memory_db = tmp_path / "memory.sqlite3"
    state_db = tmp_path / "state.sqlite3"
    runtime = AstraRuntime(memory_db=memory_db, state_db=state_db, context=context())
    runtime.record_start()
    checkpoint = runtime.checkpoint(
        checkpoint_id="ASTRA-CP-001",
        state_reference="state:astra:001",
        memory_reference="memory:astra:001",
        owner_approved=True,
    )
    assert checkpoint.canonical_effect == "NONE"

    recovery = runtime.recover()
    assert recovery.lineage_valid is True
    assert recovery.checkpoint is not None
    assert recovery.checkpoint.checkpoint_id == "ASTRA-CP-001"

    source = runtime.register_environment_evidence(
        device_id="DEVICE-A",
        hardware_profile_hash="hardware-a",
        runtime_environment_hash="runtime-a",
        policy_config_hash="policy-v1",
        verification_reference="qa:a",
    )
    target = runtime.register_environment_evidence(
        device_id="DEVICE-B",
        hardware_profile_hash="hardware-b",
        runtime_environment_hash="runtime-b",
        policy_config_hash="policy-v1",
        verification_reference="qa:b",
    )
    migrated = runtime.migrate_runtime(
        context(runtime_instance_id="ASTRA-I-002"),
        owner_approved=True,
        source_evidence_id=source.evidence_id,
        target_evidence_id=target.evidence_id,
    )
    assert migrated.context.runtime_instance_id == "ASTRA-I-002"
    assert migrated.context.event_lineage_id == runtime.context.event_lineage_id
    assert migrated.state.verify() is True
    assert migrated.migration_summary()[0].migration_count == 1
