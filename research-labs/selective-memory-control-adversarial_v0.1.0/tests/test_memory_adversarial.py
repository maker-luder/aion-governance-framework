import pytest

from aion_selective_memory import MemoryRecord, MemoryStatus, RetrievalHit, RetrievalTrace, SelectiveMemoryStore

from aion_selective_memory_adversarial import AuditStatus, audit_memory_lineage, audit_record, audit_records, audit_retrieval


STAMP = "2026-08-13T00:00:00+00:00"


def record(memory_id: str = "memory:1", **overrides) -> MemoryRecord:
    values = dict(
        memory_id=memory_id,
        namespace="subject:aion",
        domain="research",
        purpose="review",
        content="bounded governance evidence",
        source_ref="repo:evidence:1",
        approval_ref="approval:1",
        created_at=STAMP,
        revision=1,
        supersedes=None,
        status=MemoryStatus.ACTIVE,
    )
    values.update(overrides)
    return MemoryRecord(**values)


def trace(*, records, hits=(), considered=("memory:1",), blocked=(), **overrides) -> RetrievalTrace:
    values = dict(
        query="governance evidence",
        namespace="subject:aion",
        domain="research",
        purpose="review",
        considered_ids=considered,
        blocked_ids=blocked,
        hits=hits,
    )
    values.update(overrides)
    return RetrievalTrace(**values)


def assert_no_effect(audit) -> None:
    assert audit.authority == "REVIEW_METADATA_ONLY"
    assert audit.memory_truth == "NOT_ESTABLISHED"
    assert audit.identity_continuity == "NOT_ESTABLISHED"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert audit.canonical_effect == "NONE"
    assert audit.governance_effect == "NONE"
    assert audit.deployment is False
    assert audit.model_execution is False
    assert audit.observed_result == "NOT_EVALUATED"


def test_valid_record_is_review_metadata_only() -> None:
    audit = audit_record(record())
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "MEMORY_RECORD_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)


def test_missing_record_field_is_invalid() -> None:
    audit = audit_record(record(content=""))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "MEMORY_FIELD_MISSING"
    assert_no_effect(audit)


def test_created_at_requires_timezone() -> None:
    audit = audit_record(record(created_at="2026-08-13T00:00:00"))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "CREATED_AT_TIMEZONE_INVALID"
    assert_no_effect(audit)


def test_revision_number_must_be_positive() -> None:
    audit = audit_record(record(revision=0))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "REVISION_INVALID"
    assert_no_effect(audit)


def test_initial_record_cannot_supersede() -> None:
    audit = audit_record(record(supersedes="memory:0"))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "INITIAL_RECORD_CANNOT_SUPERSEDE"
    assert_no_effect(audit)


def test_revision_parent_is_required() -> None:
    audit = audit_record(record(revision=2))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "REVISION_PARENT_MISSING"
    assert_no_effect(audit)


def test_non_active_record_is_held() -> None:
    audit = audit_record(record(status=MemoryStatus.SUPERSEDED))
    assert audit.status == AuditStatus.HOLD
    assert audit.reason == "NON_ACTIVE_MEMORY_NOT_CONTEXT_ELIGIBLE"
    assert_no_effect(audit)


def test_empty_store_is_held() -> None:
    audit = audit_records(())
    assert audit.status == AuditStatus.HOLD
    assert audit.reason == "MEMORY_STORE_EMPTY"
    assert_no_effect(audit)


def test_duplicate_memory_ids_are_invalid() -> None:
    item = record()
    audit = audit_records((item, item))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "DUPLICATE_MEMORY_ID"
    assert_no_effect(audit)


def test_revision_parent_must_exist() -> None:
    audit = audit_records((record(revision=2, supersedes="memory:missing"),))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "REVISION_PARENT_NOT_FOUND"
    assert_no_effect(audit)


def test_revision_scope_drift_is_invalid() -> None:
    old = record()
    new = record("memory:2", namespace="subject:other", revision=2, supersedes="memory:1", source_ref="repo:evidence:2", approval_ref="approval:2")
    audit = audit_records((old, new))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "REVISION_SCOPE_DRIFT"
    assert_no_effect(audit)


def test_revision_number_drift_is_invalid() -> None:
    old = record()
    new = record("memory:2", revision=3, supersedes="memory:1", source_ref="repo:evidence:2", approval_ref="approval:2")
    audit = audit_records((old, new))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "REVISION_NUMBER_DRIFT"
    assert_no_effect(audit)


def test_active_source_reference_reuse_is_held() -> None:
    first = record()
    second = record("memory:2", source_ref=first.source_ref, approval_ref="approval:2")
    audit = audit_records((first, second))
    assert audit.status == AuditStatus.HOLD
    assert audit.reason == "SOURCE_REF_REUSE_REQUIRES_REVIEW"
    assert_no_effect(audit)


def test_discarded_record_retention_is_held() -> None:
    audit = audit_records((record(status=MemoryStatus.DISCARDED),))
    assert audit.status == AuditStatus.HOLD
    assert audit.reason == "DISCARDED_MEMORY_RETAINED_OUTSIDE_CONTEXT"
    assert_no_effect(audit)


def test_valid_revision_chain_is_admitted() -> None:
    old = record()
    new = record("memory:2", revision=2, supersedes="memory:1", source_ref="repo:evidence:2", approval_ref="approval:2")
    audit = audit_records((old, new))
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "MEMORY_STORE_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)


def test_valid_memory_lineage_is_admitted() -> None:
    old = record()
    new = record("memory:2", revision=2, supersedes="memory:1", source_ref="repo:evidence:2", approval_ref="approval:2")
    audit = audit_memory_lineage((old, new), "memory:2")
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "MEMORY_LINEAGE_REVIEW_METADATA_ONLY"
    assert audit.record_count == 2
    assert_no_effect(audit)


def test_missing_memory_lineage_id_is_invalid() -> None:
    audit = audit_memory_lineage((record(),), "memory:missing")
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "MEMORY_ID_NOT_FOUND"
    assert_no_effect(audit)


def test_store_requires_approval_for_writes() -> None:
    store = SelectiveMemoryStore()
    with pytest.raises(ValueError, match="approval_ref"):
        store.add(memory_id="memory:1", namespace="subject:aion", domain="research", purpose="review", content="x", source_ref="repo:x", approval_ref="")


def test_valid_retrieval_trace_is_admitted() -> None:
    item = record()
    hit = RetrievalHit(item, 0.5, ("evidence",))
    audit = audit_retrieval(trace(records=(item,), hits=(hit,)), (item,))
    assert audit.status == AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "RETRIEVAL_TRACE_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)


def test_retrieval_scope_requires_all_dimensions() -> None:
    item = record()
    audit = audit_retrieval(trace(records=(item,), namespace=""), (item,))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "RETRIEVAL_SCOPE_MISSING"
    assert_no_effect(audit)


def test_duplicate_considered_ids_are_invalid() -> None:
    item = record()
    audit = audit_retrieval(trace(records=(item,), considered=("memory:1", "memory:1")), (item,))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "DUPLICATE_CONSIDERED_ID"
    assert_no_effect(audit)


def test_duplicate_blocked_ids_are_invalid() -> None:
    item = record()
    audit = audit_retrieval(trace(records=(item,), blocked=("memory:2", "memory:2")), (item,))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "DUPLICATE_BLOCKED_ID"
    assert_no_effect(audit)


def test_considered_blocked_overlap_is_invalid() -> None:
    item = record()
    audit = audit_retrieval(trace(records=(item,), blocked=("memory:1",)), (item,))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "CONSIDERED_BLOCKED_OVERLAP"
    assert_no_effect(audit)


def test_non_active_memory_cannot_be_returned() -> None:
    item = record(status=MemoryStatus.SUPERSEDED)
    hit = RetrievalHit(item, 0.5, ("evidence",))
    audit = audit_retrieval(trace(records=(item,), hits=(hit,)), (item,))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "NON_ACTIVE_MEMORY_RETURNED"
    assert_no_effect(audit)


def test_hit_must_be_considered() -> None:
    item = record()
    hit = RetrievalHit(item, 0.5, ("evidence",))
    audit = audit_retrieval(trace(records=(item,), considered=(), hits=(hit,)), (item,))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "HIT_NOT_CONSIDERED"
    assert_no_effect(audit)


def test_hit_scope_must_match_trace() -> None:
    item = record(namespace="subject:other")
    hit = RetrievalHit(item, 0.5, ("evidence",))
    audit = audit_retrieval(trace(records=(item,), hits=(hit,)), (item,))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "HIT_SCOPE_MISMATCH"
    assert_no_effect(audit)


def test_hit_score_must_be_bounded_and_have_terms() -> None:
    item = record()
    audit = audit_retrieval(trace(records=(item,), hits=(RetrievalHit(item, 1.1, ("evidence",)),)), (item,))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "HIT_SCORE_OR_TERMS_INVALID"
    assert_no_effect(audit)


def test_hit_without_matched_terms_is_invalid() -> None:
    item = record()
    audit = audit_retrieval(trace(records=(item,), hits=(RetrievalHit(item, 0.5, ()),)), (item,))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "HIT_SCORE_OR_TERMS_INVALID"
    assert_no_effect(audit)


def test_retrieval_order_is_checked() -> None:
    first = record("memory:1", revision=2, supersedes="memory:0", source_ref="repo:1", approval_ref="approval:1")
    second = record("memory:2", source_ref="repo:2", approval_ref="approval:2")
    hits = (RetrievalHit(second, 0.2, ("evidence",)), RetrievalHit(first, 0.8, ("evidence",)))
    audit = audit_retrieval(trace(records=(first, second), hits=hits, considered=("memory:1", "memory:2")), (first, second))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "HIT_ORDER_INVALID"
    assert_no_effect(audit)


def test_hit_record_must_exist_in_audited_records() -> None:
    item = record()
    other = record("memory:2", source_ref="repo:2", approval_ref="approval:2")
    audit = audit_retrieval(trace(records=(item,), hits=(RetrievalHit(other, 0.5, ("evidence",)),)), (item,))
    assert audit.status == AuditStatus.INVALID
    assert audit.reason == "HIT_RECORD_NOT_FOUND"
    assert_no_effect(audit)
