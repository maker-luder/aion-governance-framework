from aion_selective_memory import MemoryStatus, SelectiveMemoryStore


def _store() -> SelectiveMemoryStore:
    store = SelectiveMemoryStore()
    store.add(
        memory_id="m1",
        namespace="teacher",
        domain="project",
        purpose="research",
        content="AION uses correction-aware provenance for memory recall",
        source_ref="owner:2026-08-11",
        approval_ref="write-gate:approved:m1",
        created_at="2026-08-11T00:00:00+00:00",
    )
    return store


def test_revision_supersedes_old_memory_and_preserves_lineage() -> None:
    store = _store()
    revised = store.revise(
        memory_id="m1",
        new_memory_id="m2",
        content="AION uses selective recall with correction-aware provenance",
        source_ref="joint-review:2026-08-11",
        approval_ref="write-gate:approved:m2",
        created_at="2026-08-11T00:01:00+00:00",
    )
    assert store.get("m1").status is MemoryStatus.SUPERSEDED
    assert revised.revision == 2
    assert revised.supersedes == "m1"
    assert [r.memory_id for r in store.active_chain("m2")] == ["m1", "m2"]


def test_retrieval_blocks_superseded_memory() -> None:
    store = _store()
    store.revise(
        memory_id="m1",
        new_memory_id="m2",
        content="AION selective recall correction provenance",
        source_ref="joint-review:2026-08-11",
        approval_ref="write-gate:approved:m2",
    )
    trace = store.retrieve(
        "selective recall provenance",
        namespace="teacher",
        domain="project",
        purpose="research",
    )
    assert [hit.record.memory_id for hit in trace.hits] == ["m2"]
    assert "m1" in trace.blocked_ids


def test_namespace_isolation() -> None:
    store = _store()
    trace = store.retrieve(
        "AION provenance",
        namespace="other-agent",
        domain="project",
        purpose="research",
    )
    assert trace.hits == ()
    assert "m1" in trace.blocked_ids


def test_domain_and_purpose_isolation() -> None:
    store = _store()
    wrong_domain = store.retrieve(
        "AION provenance",
        namespace="teacher",
        domain="personal",
        purpose="research",
    )
    wrong_purpose = store.retrieve(
        "AION provenance",
        namespace="teacher",
        domain="project",
        purpose="casual",
    )
    assert wrong_domain.hits == ()
    assert wrong_purpose.hits == ()


def test_provenance_and_approval_are_returned_with_hit() -> None:
    store = _store()
    trace = store.retrieve(
        "AION provenance",
        namespace="teacher",
        domain="project",
        purpose="research",
    )
    assert trace.hits[0].record.source_ref == "owner:2026-08-11"
    assert trace.hits[0].record.approval_ref == "write-gate:approved:m1"


def test_discarded_memory_is_not_context_eligible() -> None:
    store = _store()
    store.discard("m1", approval_ref="write-gate:discard:m1")
    trace = store.retrieve(
        "AION provenance",
        namespace="teacher",
        domain="project",
        purpose="research",
    )
    assert trace.hits == ()
    assert "m1" in trace.blocked_ids


def test_chinese_retrieval_does_not_collapse_to_single_token() -> None:
    store = SelectiveMemoryStore()
    store.add(
        memory_id="zh1",
        namespace="teacher",
        domain="project",
        purpose="research",
        content="研究分支測試選擇性記憶與修訂優先",
        source_ref="synthetic:zh",
        approval_ref="write-gate:approved:zh1",
    )
    trace = store.retrieve(
        "選擇性記憶 修訂",
        namespace="teacher",
        domain="project",
        purpose="research",
    )
    assert [hit.record.memory_id for hit in trace.hits] == ["zh1"]
    assert len(trace.hits[0].matched_terms) >= 2


def test_write_requires_approval_reference() -> None:
    store = SelectiveMemoryStore()
    try:
        store.add(
            memory_id="bad",
            namespace="teacher",
            domain="project",
            purpose="research",
            content="unapproved write",
            source_ref="synthetic",
            approval_ref="",
        )
    except ValueError as exc:
        assert "approval_ref" in str(exc)
    else:
        raise AssertionError("unapproved write should fail")
