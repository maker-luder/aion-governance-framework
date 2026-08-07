from __future__ import annotations

import pytest

from aion_astra_runtime.models import IndividualRuntimeContext
from individual_runtime_state import IndividualRuntimeStateStore, RuntimeStateError


def context(**changes: str) -> IndividualRuntimeContext:
    values = {
        "agent_id": "AION",
        "runtime_instance_id": "AION-I-001",
        "memory_stream_id": "AION-MEMORY-001",
        "event_lineage_id": "AION-EVENTS-001",
        "canonical_state_reference": "AION-CANONICAL",
        "genesis_root_id": "ROOT-001",
    }
    values.update(changes)
    return IndividualRuntimeContext(**values)


def test_event_lineage_persists_across_restart(tmp_path):
    db = tmp_path / "state.sqlite3"
    first = IndividualRuntimeStateStore(db, context())
    first.append_event("runtime.started", {"reason": "initial"})

    restarted = IndividualRuntimeStateStore(db, context())
    restarted.append_event("runtime.restarted", {})

    events = restarted.events()
    assert [event.sequence for event in events] == [1, 2]
    assert events[0].event_hash == events[1].previous_hash
    assert restarted.verify() is True


def test_checkpoint_recovery_and_non_destructive_rollback(tmp_path):
    store = IndividualRuntimeStateStore(tmp_path / "state.sqlite3", context())
    store.append_event("runtime.started")
    checkpoint = store.checkpoint(
        checkpoint_id="CP-001",
        state_reference="state:001",
        memory_reference="memory:001",
        owner_approved=True,
    )
    assert checkpoint.canonical_effect == "NONE"

    store.append_event("runtime.worked")
    before = len(store.events())
    selected = store.rollback_to_checkpoint("CP-001", owner_approved=True)
    after = store.events()

    assert selected.checkpoint_id == "CP-001"
    assert len(after) == before + 1
    assert after[-1].event_type == "runtime.rollback_requested"
    assert after[-1].payload["history_truncated"] is False

    recovery = store.recover()
    assert recovery.lineage_valid is True
    assert recovery.checkpoint is not None
    assert recovery.checkpoint.checkpoint_id == "CP-001"


def test_checkpoint_and_rollback_require_owner_approval(tmp_path):
    store = IndividualRuntimeStateStore(tmp_path / "state.sqlite3", context())
    with pytest.raises(RuntimeStateError):
        store.checkpoint(
            checkpoint_id="CP-X",
            state_reference="state:x",
            memory_reference="memory:x",
            owner_approved=False,
        )


def test_migration_changes_only_runtime_instance(tmp_path):
    db = tmp_path / "state.sqlite3"
    store = IndividualRuntimeStateStore(db, context())
    store.append_event("runtime.started")
    migrated = store.migrate_instance(
        context(runtime_instance_id="AION-I-002"),
        owner_approved=True,
    )

    assert migrated.context.runtime_instance_id == "AION-I-002"
    assert migrated.context.event_lineage_id == "AION-EVENTS-001"
    assert migrated.verify() is True
    assert [event.event_type for event in migrated.events()][-2:] == [
        "runtime.migrating_out",
        "runtime.migrated_in",
    ]


def test_migration_cannot_change_individual_ownership(tmp_path):
    store = IndividualRuntimeStateStore(tmp_path / "state.sqlite3", context())
    with pytest.raises(RuntimeStateError):
        store.migrate_instance(
            context(runtime_instance_id="AION-I-002", memory_stream_id="OTHER"),
            owner_approved=True,
        )


def test_existing_lineage_rejects_different_agent(tmp_path):
    db = tmp_path / "state.sqlite3"
    store = IndividualRuntimeStateStore(db, context())
    store.append_event("runtime.started")
    with pytest.raises(RuntimeStateError):
        IndividualRuntimeStateStore(db, context(agent_id="ASTRA"))
