from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPONENT_SRC = ROOT / "components" / "memory_recall_governance_v0.1.0" / "src"
sys.path.insert(0, str(COMPONENT_SRC))

from aion_memory_recall.gate import decide_recall  # noqa: E402
from aion_memory_recall.models import MemoryRecord, RecallRequest, RecallStatus  # noqa: E402


def overlap(left: frozenset[str], right: frozenset[str]) -> int:
    return len({item.casefold() for item in left} & {item.casefold() for item in right})


def naive_recall(request: RecallRequest, records: list[MemoryRecord]) -> list[str]:
    return [record.memory_id for record in records if overlap(request.entity_cues, record.entities) + overlap(request.topic_cues, record.topics) > 0]


def fixture() -> tuple[RecallRequest, list[MemoryRecord]]:
    request = RecallRequest(user_id="user-a", agent_id="agent-a", requester_scopes=frozenset({"public"}), entity_cues=frozenset({"AION"}), topic_cues=frozenset({"continuity"}))
    common = dict(namespace="fixture", entities=frozenset({"AION"}), topics=frozenset({"continuity"}))
    records = [
        MemoryRecord("valid", user_id="user-a", agent_id="agent-a", access_scope=frozenset({"public"}), provenance_verified=True, **common),
        MemoryRecord("superseded", user_id="user-a", agent_id="agent-a", access_scope=frozenset({"public"}), provenance_verified=True, superseded=True, **common),
        MemoryRecord("badprov", user_id="user-a", agent_id="agent-a", access_scope=frozenset({"public"}), provenance_verified=False, **common),
        MemoryRecord("conflict", user_id="user-a", agent_id="agent-a", access_scope=frozenset({"public"}), provenance_verified=True, conflict=True, **common),
        MemoryRecord("wrongid", user_id="user-b", agent_id="agent-a", access_scope=frozenset({"public"}), provenance_verified=True, **common),
        MemoryRecord("private", user_id="user-a", agent_id="agent-a", access_scope=frozenset({"private"}), provenance_verified=True, **common),
    ]
    return request, records


def run() -> dict[str, object]:
    request, records = fixture()
    naive = naive_recall(request, records)
    governed = {record.memory_id: decide_recall(request, record).status.value for record in records}
    eligible = [memory_id for memory_id, status in governed.items() if status == RecallStatus.TEMPORARY_ONLY.value]
    expected = {
        "valid": "RECALL_ALLOWED_TEMPORARY_ONLY",
        "superseded": "RECALL_DENIED_PROVENANCE_FAILURE",
        "badprov": "RECALL_DENIED_PROVENANCE_FAILURE",
        "conflict": "RECALL_QUARANTINED_CONFLICT",
        "wrongid": "RECALL_DENIED_IDENTITY_MISMATCH",
        "private": "RECALL_DENIED_ACCESS_SCOPE",
    }
    assert len(naive) == 6
    assert governed == expected
    assert eligible == ["valid"]
    return {"experiment": "g1-recall-gate-baseline_v0.1.0", "m0_naive_selected": naive, "m0_naive_count": len(naive), "m1_dispositions": governed, "m1_eligible": eligible, "m1_eligible_count": len(eligible), "m1_blocked_or_quarantined_count": len(records) - len(eligible), "canonical_effect": "NONE", "subjectivity_conclusion": "NOT_ESTABLISHED"}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
