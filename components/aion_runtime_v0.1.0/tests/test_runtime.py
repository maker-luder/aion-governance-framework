from __future__ import annotations

import pytest

from aion_memory_recall.models import RecallRequest
from aion_memory_recall.store import MemoryWriteDenied
from aion_runtime import AIONRuntime


def test_status_keeps_held_capabilities_closed(tmp_path):
    runtime = AIONRuntime(memory_db=tmp_path / "memory.sqlite3")
    status = runtime.status()
    assert status.live_cross_session_memory == "ENABLED_GOVERNED"
    assert status.automatic_canonical_writeback == "DISABLED"
    assert status.public_ablation_execution == "DISABLED"
    assert status.sexual_or_intimate_runtime == "NOT_AUTHORIZED"
    assert status.canonical_promotion == "PENDING_OWNER_REVIEW"


def test_runtime_memory_round_trip_requires_write_approval(tmp_path):
    runtime = AIONRuntime(memory_db=tmp_path / "memory.sqlite3")
    common = dict(
        memory_id="m1",
        namespace="aion-private",
        user_id="u1",
        agent_id="AION",
        content="runtime deployment decision",
        provenance_source="owner-input",
        provenance_verified=True,
        entities={"AION"},
        topics={"deployment"},
        access_scope={"project"},
    )
    with pytest.raises(MemoryWriteDenied):
        runtime.remember(writeback_approved=False, **common)

    runtime.remember(writeback_approved=True, **common)
    request = RecallRequest(
        user_id="u1",
        agent_id="AION",
        requester_scopes=frozenset({"project"}),
        entity_cues=frozenset({"AION"}),
        topic_cues=frozenset({"deployment"}),
    )
    recalled = runtime.recall(request)
    assert [item.memory_id for item in recalled] == ["m1"]
    assert recalled[0].canonical_effect == "NONE"
