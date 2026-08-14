from __future__ import annotations

import sqlite3

import pytest

from aion_memory_recall.models import RecallRequest
from aion_memory_recall.store import MemoryRecordCorruption, MemoryWriteDenied, SQLiteMemoryStore


def request() -> RecallRequest:
    return RecallRequest(
        user_id="user-1",
        agent_id="AION",
        requester_scopes=frozenset({"project"}),
        entity_cues=frozenset({"Astra"}),
        topic_cues=frozenset({"runtime"}),
    )


def test_write_requires_explicit_approval(tmp_path):
    store = SQLiteMemoryStore(tmp_path / "memory.sqlite3")
    with pytest.raises(MemoryWriteDenied):
        store.write(
            memory_id="m1",
            namespace="private",
            user_id="user-1",
            agent_id="AION",
            content="candidate memory",
            entities={"Astra"},
            topics={"runtime"},
            access_scope={"project"},
            provenance_source="owner-input",
            provenance_verified=True,
            writeback_approved=False,
        )


def test_verified_memory_persists_and_recalls(tmp_path):
    path = tmp_path / "memory.sqlite3"
    store = SQLiteMemoryStore(path)
    stored = store.write(
        memory_id="m1",
        namespace="private",
        user_id="user-1",
        agent_id="AION",
        content="Astra runtime decision",
        entities={"Astra"},
        topics={"runtime"},
        access_scope={"project"},
        provenance_source="owner-input",
        provenance_verified=True,
        writeback_approved=True,
        recorded_at="2026-08-07T00:00:00+00:00",
    )
    assert stored.canonical_effect == "NONE"

    reopened = SQLiteMemoryStore(path)
    recalled = reopened.recall(request())
    assert [item.memory_id for item in recalled] == ["m1"]
    assert recalled[0].content == "Astra runtime decision"


@pytest.mark.parametrize(
    ("column", "value", "message"),
    [
        ("entities_json", "not-json", "JSON"),
        ("provenance_verified", 2, "flag"),
        ("canonical_effect", "PROMOTED", "canonical_effect"),
    ],
)
def test_malformed_persisted_memory_fails_closed(tmp_path, column, value, message):
    path = tmp_path / "memory.sqlite3"
    store = SQLiteMemoryStore(path)
    store.write(
        memory_id="m1",
        namespace="private",
        user_id="user-1",
        agent_id="AION",
        content="candidate",
        entities={"Astra"},
        topics={"runtime"},
        access_scope={"project"},
        provenance_source="test",
        provenance_verified=True,
        writeback_approved=True,
    )
    with sqlite3.connect(path) as connection:
        connection.execute("PRAGMA ignore_check_constraints = ON")
        connection.execute(
            f"UPDATE memory_records SET {column} = ? WHERE memory_id = ?",
            (value, "m1"),
        )

    with pytest.raises(MemoryRecordCorruption, match=message):
        store.get("m1")
    with pytest.raises(MemoryRecordCorruption, match=message):
        store.recall(request())


def test_unverified_conflicted_tombstoned_or_superseded_memory_is_not_recalled(tmp_path):
    store = SQLiteMemoryStore(tmp_path / "memory.sqlite3")
    common = dict(
        namespace="private",
        user_id="user-1",
        agent_id="AION",
        content="candidate",
        entities={"Astra"},
        topics={"runtime"},
        access_scope={"project"},
        provenance_source="test",
        writeback_approved=True,
    )
    store.write(memory_id="unverified", provenance_verified=False, **common)
    store.write(memory_id="conflict", provenance_verified=True, **common)
    store.write(memory_id="tombstone", provenance_verified=True, **common)
    store.write(memory_id="superseded", provenance_verified=True, **common)
    store.set_conflict("conflict")
    store.tombstone("tombstone")
    store.supersede("superseded")

    assert store.recall(request()) == []


def test_identity_and_scope_isolation_remain_enforced(tmp_path):
    store = SQLiteMemoryStore(tmp_path / "memory.sqlite3")
    store.write(
        memory_id="m1",
        namespace="private",
        user_id="user-1",
        agent_id="AION",
        content="candidate",
        entities={"Astra"},
        topics={"runtime"},
        access_scope={"private"},
        provenance_source="test",
        provenance_verified=True,
        writeback_approved=True,
    )
    assert store.recall(request()) == []


def _write_kwargs() -> dict[str, object]:
    return {
        "memory_id": "m1",
        "namespace": "private",
        "user_id": "user-1",
        "agent_id": "AION",
        "content": "candidate",
        "entities": {"Astra"},
        "topics": {"runtime"},
        "access_scope": {"project"},
        "provenance_source": "test",
        "provenance_verified": True,
        "writeback_approved": True,
    }


@pytest.mark.parametrize("field", ["memory_id", "namespace", "user_id", "agent_id", "content", "provenance_source"])
def test_write_rejects_non_string_required_fields(tmp_path, field: str) -> None:
    store = SQLiteMemoryStore(tmp_path / "memory.sqlite3")
    values = _write_kwargs()
    values[field] = 1
    with pytest.raises(MemoryWriteDenied, match="must be a string"):
        store.write(**values)


@pytest.mark.parametrize("field", ["writeback_approved", "provenance_verified"])
def test_write_rejects_non_boolean_governance_flags(tmp_path, field: str) -> None:
    store = SQLiteMemoryStore(tmp_path / "memory.sqlite3")
    values = _write_kwargs()
    values[field] = 1
    with pytest.raises(MemoryWriteDenied, match="must be a boolean"):
        store.write(**values)


@pytest.mark.parametrize("method", ["set_conflict", "tombstone", "supersede"])
def test_flag_mutation_rejects_invalid_memory_ids(tmp_path, method):
    store = SQLiteMemoryStore(tmp_path / "memory.sqlite3")
    with pytest.raises(MemoryWriteDenied, match="memory_id"):
        if method == "set_conflict":
            store.set_conflict("", conflict=True)
        elif method == "tombstone":
            store.tombstone("")
        else:
            store.supersede("")


def test_set_conflict_rejects_non_boolean_flag(tmp_path):
    store = SQLiteMemoryStore(tmp_path / "memory.sqlite3")
    store.write(**_write_kwargs())
    with pytest.raises(MemoryWriteDenied, match="conflict must be a boolean"):
        store.set_conflict("m1", conflict=1)


def test_write_rejects_scalar_iterable_and_blank_recorded_at(tmp_path) -> None:
    store = SQLiteMemoryStore(tmp_path / "memory.sqlite3")
    values = _write_kwargs()
    values["entities"] = "Astra"
    with pytest.raises(MemoryWriteDenied, match="entities must be an iterable of strings"):
        store.write(**values)

    values = _write_kwargs()
    values["topics"] = ["runtime", 1]
    with pytest.raises(MemoryWriteDenied, match="topics must be an iterable of strings"):
        store.write(**values)

    values = _write_kwargs()
    values["recorded_at"] = "   "
    with pytest.raises(MemoryWriteDenied, match="recorded_at"):
        store.write(**values)
