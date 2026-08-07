from __future__ import annotations

import pytest

from aion_memory_recall.models import RecallRequest
from aion_memory_recall.store import MemoryWriteDenied, SQLiteMemoryStore


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


def test_unverified_conflicted_or_tombstoned_memory_is_not_recalled(tmp_path):
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
    store.set_conflict("conflict")
    store.tombstone("tombstone")

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
