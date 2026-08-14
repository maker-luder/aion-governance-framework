from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import sqlite3
import threading

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


def evidence(store: IndividualRuntimeStateStore, device_id: str, suffix: str):
    return store.register_environment_evidence(
        device_id=device_id,
        hardware_profile_hash=f"hardware-{suffix}",
        runtime_environment_hash=f"runtime-{suffix}",
        policy_config_hash="policy-v1",
        verification_reference=f"qa:{suffix}",
    )


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


def test_concurrent_event_appends_are_serialized(tmp_path):
    db = tmp_path / "state.sqlite3"
    store = IndividualRuntimeStateStore(db, context())

    with ThreadPoolExecutor(max_workers=4) as executor:
        events = list(
            executor.map(
                lambda index: store.append_event("runtime.concurrent", {"index": index}),
                range(16),
            )
        )

    assert sorted(event.sequence for event in events) == list(range(1, 17))
    assert store.verify() is True
    assert len(store.events()) == 16


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


def test_recovery_denies_tampered_event_lineage(tmp_path):
    db = tmp_path / "state.sqlite3"
    store = IndividualRuntimeStateStore(db, context())
    store.append_event("runtime.started", {"reason": "initial"})
    with sqlite3.connect(db) as connection:
        connection.execute(
            "UPDATE runtime_events SET payload_json = ? WHERE event_lineage_id = ? AND sequence = 1",
            ('{"reason":"tampered"}', context().event_lineage_id),
        )
    assert store.verify() is False
    with pytest.raises(RuntimeStateError, match="recovery denied"):
        store.recover()


@pytest.mark.parametrize("payload_json", ["not-json", "[]"])
def test_malformed_event_payload_fails_closed(tmp_path, payload_json):
    db = tmp_path / "state.sqlite3"
    store = IndividualRuntimeStateStore(db, context())
    store.append_event("runtime.started", {"reason": "initial"})
    with sqlite3.connect(db) as connection:
        connection.execute(
            "UPDATE runtime_events SET payload_json = ? WHERE event_lineage_id = ? AND sequence = 1",
            (payload_json, context().event_lineage_id),
        )

    with pytest.raises(RuntimeStateError, match="runtime event payload"):
        store.events()
    assert store.verify() is False
    with pytest.raises(RuntimeStateError, match="recovery denied"):
        store.recover()


def test_malformed_event_text_column_fails_closed(tmp_path):
    db = tmp_path / "state.sqlite3"
    store = IndividualRuntimeStateStore(db, context())
    store.append_event("runtime.started")
    with sqlite3.connect(db) as connection:
        connection.execute(
            "UPDATE runtime_events SET event_hash = '' WHERE event_lineage_id = ? AND sequence = 1",
            (context().event_lineage_id,),
        )

    with pytest.raises(RuntimeStateError, match="event column: event_hash"):
        store.events()
    assert store.verify() is False
    with pytest.raises(RuntimeStateError, match="recovery denied"):
        store.recover()


def test_recovery_and_rollback_deny_tampered_checkpoint_reference(tmp_path):
    db = tmp_path / "state.sqlite3"
    store = IndividualRuntimeStateStore(db, context())
    store.append_event("runtime.started")
    store.checkpoint(
        checkpoint_id="CP-TAMPER",
        state_reference="state:trusted",
        memory_reference="memory:trusted",
        owner_approved=True,
    )
    with sqlite3.connect(db) as connection:
        connection.execute(
            "UPDATE runtime_checkpoints SET state_reference = ? WHERE checkpoint_id = ?",
            ("state:tampered", "CP-TAMPER"),
        )
    with pytest.raises(RuntimeStateError, match="checkpoint integrity"):
        store.recover()
    with pytest.raises(RuntimeStateError, match="checkpoint integrity"):
        store.rollback_to_checkpoint("CP-TAMPER", owner_approved=True)


def test_environment_evidence_is_reused_by_fingerprint(tmp_path):
    store = IndividualRuntimeStateStore(tmp_path / "state.sqlite3", context())
    first = evidence(store, "DEVICE-A", "a")
    reused = store.register_environment_evidence(
        device_id="DEVICE-A",
        hardware_profile_hash="hardware-a",
        runtime_environment_hash="runtime-a",
        policy_config_hash="policy-v1",
        verification_reference="qa:a-new-reference",
    )
    assert reused.evidence_id == first.evidence_id
    assert reused.fingerprint == first.fingerprint


def test_concurrent_registration_reuses_one_evidence_record(tmp_path, monkeypatch):
    barrier = threading.Barrier(2)
    select_lock = threading.Lock()
    select_count = 0
    original_connect = IndividualRuntimeStateStore._connect

    class BarrierConnection:
        def __init__(self, connection):
            self._connection = connection

        def __enter__(self):
            self._connection.__enter__()
            return self

        def __exit__(self, *args):
            return self._connection.__exit__(*args)

        def execute(self, sql, parameters=()):
            nonlocal select_count
            should_wait = False
            if "SELECT * FROM runtime_environment_evidence WHERE fingerprint = ?" in sql:
                with select_lock:
                    select_count += 1
                    should_wait = select_count <= 2
            if should_wait:
                barrier.wait(timeout=5)
            return self._connection.execute(sql, parameters)

        def __getattr__(self, name):
            return getattr(self._connection, name)

    def connect(self):
        return BarrierConnection(original_connect(self))

    monkeypatch.setattr(IndividualRuntimeStateStore, "_connect", connect)
    store = IndividualRuntimeStateStore(tmp_path / "state.sqlite3", context())

    def register():
        return evidence(store, "DEVICE-A", "same")

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _index: register(), range(2)))

    assert {item.evidence_id for item in results} == {results[0].evidence_id}
    with sqlite3.connect(tmp_path / "state.sqlite3") as connection:
        count = connection.execute("SELECT COUNT(*) FROM runtime_environment_evidence").fetchone()[0]
    assert count == 1


def test_changed_environment_requires_new_evidence(tmp_path):
    store = IndividualRuntimeStateStore(tmp_path / "state.sqlite3", context())
    first = evidence(store, "DEVICE-A", "a")
    changed = store.register_environment_evidence(
        device_id="DEVICE-A",
        hardware_profile_hash="hardware-a",
        runtime_environment_hash="runtime-a-v2",
        policy_config_hash="policy-v1",
        verification_reference="qa:a-v2",
    )
    assert changed.evidence_id != first.evidence_id
    assert changed.fingerprint != first.fingerprint


def test_migration_changes_only_runtime_instance_and_reuses_evidence(tmp_path):
    db = tmp_path / "state.sqlite3"
    store = IndividualRuntimeStateStore(db, context())
    source = evidence(store, "DEVICE-A", "a")
    target = evidence(store, "DEVICE-B", "b")
    store.append_event("runtime.started")

    migrated = store.migrate_instance(
        context(runtime_instance_id="AION-I-002"),
        owner_approved=True,
        source_evidence_id=source.evidence_id,
        target_evidence_id=target.evidence_id,
    )

    assert migrated.context.runtime_instance_id == "AION-I-002"
    assert migrated.context.event_lineage_id == "AION-EVENTS-001"
    assert migrated.verify() is True
    assert [event.event_type for event in migrated.events()][-2:] == [
        "runtime.migrating_out",
        "runtime.migrated_in",
    ]
    assert migrated.events()[-2].payload["source_evidence_id"] == source.evidence_id
    assert migrated.events()[-2].payload["target_evidence_id"] == target.evidence_id


def test_atomic_migration_rolls_back_if_second_transition_write_fails(tmp_path, monkeypatch):
    db = tmp_path / "state.sqlite3"
    store = IndividualRuntimeStateStore(db, context())
    source = evidence(store, "DEVICE-A", "a")
    target = evidence(store, "DEVICE-B", "b")
    store.append_event("runtime.started")
    original = IndividualRuntimeStateStore._append_event_with_connection

    def fail_on_migrated_in(connection, *, context, event_type, payload):
        if event_type == "runtime.migrated_in":
            raise sqlite3.DatabaseError("simulated migration interruption")
        return original(connection, context=context, event_type=event_type, payload=payload)

    monkeypatch.setattr(
        IndividualRuntimeStateStore,
        "_append_event_with_connection",
        staticmethod(fail_on_migrated_in),
    )
    before = [(event.sequence, event.event_type, event.event_hash) for event in store.events()]
    with pytest.raises(RuntimeStateError, match="atomic migration persistence failed"):
        store.migrate_instance(
            context(runtime_instance_id="AION-I-002"),
            owner_approved=True,
            source_evidence_id=source.evidence_id,
            target_evidence_id=target.evidence_id,
        )
    after = [(event.sequence, event.event_type, event.event_hash) for event in store.events()]
    assert after == before
    assert store.verify() is True


def test_unpaired_migration_transition_invalidates_lineage(tmp_path):
    store = IndividualRuntimeStateStore(tmp_path / "state.sqlite3", context())
    store.append_event(
        "runtime.migrating_out",
        {
            "from_runtime_instance_id": "AION-I-001",
            "to_runtime_instance_id": "AION-I-002",
            "source_evidence_id": "ENV-A",
            "target_evidence_id": "ENV-B",
            "canonical_effect": "NONE",
        },
    )
    assert store.verify() is False
    with pytest.raises(RuntimeStateError, match="recovery denied"):
        store.recover()


def test_round_trip_migrations_keep_unique_events_but_reuse_two_evidence_records(tmp_path):
    db = tmp_path / "state.sqlite3"
    first = IndividualRuntimeStateStore(db, context())
    device_a = evidence(first, "DEVICE-A", "a")
    device_b = evidence(first, "DEVICE-B", "b")

    on_b = first.migrate_instance(
        context(runtime_instance_id="AION-I-002"),
        owner_approved=True,
        source_evidence_id=device_a.evidence_id,
        target_evidence_id=device_b.evidence_id,
    )
    back_on_a = on_b.migrate_instance(
        context(runtime_instance_id="AION-I-003"),
        owner_approved=True,
        source_evidence_id=device_b.evidence_id,
        target_evidence_id=device_a.evidence_id,
    )

    migration_events = [
        event for event in back_on_a.events() if event.event_type == "runtime.migrating_out"
    ]
    assert len(migration_events) == 2
    assert migration_events[0].event_hash != migration_events[1].event_hash

    summaries = back_on_a.migration_summary()
    assert {(item.source_evidence_id, item.target_evidence_id, item.migration_count) for item in summaries} == {
        (device_a.evidence_id, device_b.evidence_id, 1),
        (device_b.evidence_id, device_a.evidence_id, 1),
    }

    assert back_on_a.get_environment_evidence(device_a.evidence_id).device_id == "DEVICE-A"
    assert back_on_a.get_environment_evidence(device_b.evidence_id).device_id == "DEVICE-B"


def test_migration_requires_pass_environment_evidence(tmp_path):
    store = IndividualRuntimeStateStore(tmp_path / "state.sqlite3", context())
    source = evidence(store, "DEVICE-A", "a")
    failed = store.register_environment_evidence(
        device_id="DEVICE-B",
        hardware_profile_hash="hardware-b",
        runtime_environment_hash="runtime-b",
        policy_config_hash="policy-v1",
        verification_reference="qa:b",
        verification_status="FAIL",
    )
    with pytest.raises(RuntimeStateError):
        store.migrate_instance(
            context(runtime_instance_id="AION-I-002"),
            owner_approved=True,
            source_evidence_id=source.evidence_id,
            target_evidence_id=failed.evidence_id,
        )


def test_migration_cannot_change_individual_ownership(tmp_path):
    store = IndividualRuntimeStateStore(tmp_path / "state.sqlite3", context())
    source = evidence(store, "DEVICE-A", "a")
    target = evidence(store, "DEVICE-B", "b")
    with pytest.raises(RuntimeStateError):
        store.migrate_instance(
            context(runtime_instance_id="AION-I-002", memory_stream_id="OTHER"),
            owner_approved=True,
            source_evidence_id=source.evidence_id,
            target_evidence_id=target.evidence_id,
        )


def test_existing_lineage_rejects_different_agent(tmp_path):
    db = tmp_path / "state.sqlite3"
    store = IndividualRuntimeStateStore(db, context())
    store.append_event("runtime.started")
    with pytest.raises(RuntimeStateError):
        IndividualRuntimeStateStore(db, context(agent_id="ASTRA"))
