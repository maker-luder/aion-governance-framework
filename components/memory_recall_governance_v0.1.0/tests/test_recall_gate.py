from aion_memory_recall import MemoryRecord, RecallRequest, RecallStatus, decide_recall, rank_candidates


def record(**changes: object) -> MemoryRecord:
    values = dict(
        memory_id="M1", namespace="AION_PRIVATE", user_id="U1", agent_id="AION",
        entities=frozenset({"mypy strict"}), topics=frozenset({"offline install"}),
        access_scope=frozenset({"private"}), provenance_verified=True,
    )
    values.update(changes)
    return MemoryRecord(**values)  # type: ignore[arg-type]


def request(**changes: object) -> RecallRequest:
    values = dict(user_id="U1", agent_id="AION", requester_scopes=frozenset({"private"}),
                  entity_cues=frozenset({"mypy strict"}), topic_cues=frozenset())
    values.update(changes)
    return RecallRequest(**values)  # type: ignore[arg-type]


def test_no_cue_no_recall() -> None:
    decision = decide_recall(request(entity_cues=frozenset(), topic_cues=frozenset()), record())
    assert decision.status is RecallStatus.NOT_REQUIRED


def test_identity_isolation() -> None:
    assert decide_recall(request(agent_id="ASTRA"), record()).status is RecallStatus.DENIED_IDENTITY


def test_provenance_before_use() -> None:
    assert decide_recall(request(), record(provenance_verified=False)).status is RecallStatus.DENIED_PROVENANCE


def test_conflict_quarantine() -> None:
    assert decide_recall(request(), record(conflict=True)).status is RecallStatus.QUARANTINED_CONFLICT


def test_recall_is_temporary_and_no_writeback() -> None:
    decision = decide_recall(request(), record())
    assert decision.status is RecallStatus.TEMPORARY_ONLY
    assert decision.writeback_allowed is False
    assert decision.canonical_effect == "NONE"


def test_deterministic_ranking() -> None:
    second = record(memory_id="M2", topics=frozenset({"offline install", "extra"}))
    ranked = rank_candidates(request(topic_cues=frozenset({"offline install"})), [second, record()])
    assert [item.memory_id for item in ranked] == ["M1", "M2"]
