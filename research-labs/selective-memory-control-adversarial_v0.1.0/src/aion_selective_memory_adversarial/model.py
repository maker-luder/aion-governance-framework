from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from aion_selective_memory import MemoryRecord, MemoryStatus, RetrievalTrace


class AuditStatus:
    ADMITTED_FOR_REVIEW = "ADMITTED_FOR_REVIEW"
    HOLD = "HOLD"
    INVALID = "INVALID"


@dataclass(frozen=True, slots=True)
class MemoryAudit:
    status: str
    reason: str
    record_count: int = 0
    considered_count: int = 0
    hit_count: int = 0
    authority: str = "REVIEW_METADATA_ONLY"
    memory_truth: str = "NOT_ESTABLISHED"
    identity_continuity: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False
    model_execution: bool = False
    observed_result: str = "NOT_EVALUATED"

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "reason": self.reason,
            "record_count": self.record_count,
            "considered_count": self.considered_count,
            "hit_count": self.hit_count,
            "authority": self.authority,
            "memory_truth": self.memory_truth,
            "identity_continuity": self.identity_continuity,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "canonical_effect": self.canonical_effect,
            "governance_effect": self.governance_effect,
            "deployment": self.deployment,
            "model_execution": self.model_execution,
            "observed_result": self.observed_result,
        }


def _timestamp_valid(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def audit_record(record: MemoryRecord) -> MemoryAudit:
    required = (record.memory_id, record.namespace, record.domain, record.purpose, record.content, record.source_ref, record.approval_ref, record.created_at)
    if any(not value.strip() for value in required):
        return MemoryAudit(AuditStatus.INVALID, "MEMORY_FIELD_MISSING", record_count=1)
    if not _timestamp_valid(record.created_at):
        return MemoryAudit(AuditStatus.INVALID, "CREATED_AT_TIMEZONE_INVALID", record_count=1)
    if record.revision < 1:
        return MemoryAudit(AuditStatus.INVALID, "REVISION_INVALID", record_count=1)
    if record.revision == 1 and record.supersedes is not None:
        return MemoryAudit(AuditStatus.INVALID, "INITIAL_RECORD_CANNOT_SUPERSEDE", record_count=1)
    if record.revision > 1 and not record.supersedes:
        return MemoryAudit(AuditStatus.INVALID, "REVISION_PARENT_MISSING", record_count=1)
    if record.status is not MemoryStatus.ACTIVE:
        return MemoryAudit(AuditStatus.HOLD, "NON_ACTIVE_MEMORY_NOT_CONTEXT_ELIGIBLE", record_count=1)
    return MemoryAudit(AuditStatus.ADMITTED_FOR_REVIEW, "MEMORY_RECORD_REVIEW_METADATA_ONLY", record_count=1)


def audit_records(records: Iterable[MemoryRecord]) -> MemoryAudit:
    items = tuple(records)
    if not items:
        return MemoryAudit(AuditStatus.HOLD, "MEMORY_STORE_EMPTY")
    ids = [record.memory_id for record in items]
    if len(ids) != len(set(ids)):
        return MemoryAudit(AuditStatus.INVALID, "DUPLICATE_MEMORY_ID", len(items))
    by_id = {record.memory_id: record for record in items}
    for record in items:
        base = audit_record(record)
        if base.status is AuditStatus.INVALID:
            return base
        if record.supersedes is not None:
            parent = by_id.get(record.supersedes)
            if parent is None:
                return MemoryAudit(AuditStatus.INVALID, "REVISION_PARENT_NOT_FOUND", len(items))
            if (parent.namespace, parent.domain, parent.purpose) != (record.namespace, record.domain, record.purpose):
                return MemoryAudit(AuditStatus.INVALID, "REVISION_SCOPE_DRIFT", len(items))
            if record.revision != parent.revision + 1:
                return MemoryAudit(AuditStatus.INVALID, "REVISION_NUMBER_DRIFT", len(items))
    active_sources = [record.source_ref for record in items if record.status is MemoryStatus.ACTIVE]
    if len(active_sources) != len(set(active_sources)):
        return MemoryAudit(AuditStatus.HOLD, "SOURCE_REF_REUSE_REQUIRES_REVIEW", len(items))
    if any(record.status is MemoryStatus.DISCARDED for record in items):
        return MemoryAudit(AuditStatus.HOLD, "DISCARDED_MEMORY_RETAINED_OUTSIDE_CONTEXT", len(items))
    return MemoryAudit(AuditStatus.ADMITTED_FOR_REVIEW, "MEMORY_STORE_REVIEW_METADATA_ONLY", len(items))


def audit_retrieval(trace: RetrievalTrace, records: Iterable[MemoryRecord]) -> MemoryAudit:
    items = tuple(records)
    by_id = {record.memory_id: record for record in items}
    if trace.namespace.strip() == "" or trace.domain.strip() == "" or trace.purpose.strip() == "":
        return MemoryAudit(AuditStatus.INVALID, "RETRIEVAL_SCOPE_MISSING", len(items))
    if len(set(trace.considered_ids)) != len(trace.considered_ids):
        return MemoryAudit(AuditStatus.INVALID, "DUPLICATE_CONSIDERED_ID", len(items), len(trace.considered_ids), len(trace.hits))
    if len(set(trace.blocked_ids)) != len(trace.blocked_ids):
        return MemoryAudit(AuditStatus.INVALID, "DUPLICATE_BLOCKED_ID", len(items), len(trace.considered_ids), len(trace.hits))
    if set(trace.considered_ids) & set(trace.blocked_ids):
        return MemoryAudit(AuditStatus.INVALID, "CONSIDERED_BLOCKED_OVERLAP", len(items), len(trace.considered_ids), len(trace.hits))
    previous = None
    for hit in trace.hits:
        record = by_id.get(hit.record.memory_id)
        if record is None:
            return MemoryAudit(AuditStatus.INVALID, "HIT_RECORD_NOT_FOUND", len(items), len(trace.considered_ids), len(trace.hits))
        if record.status is not MemoryStatus.ACTIVE:
            return MemoryAudit(AuditStatus.INVALID, "NON_ACTIVE_MEMORY_RETURNED", len(items), len(trace.considered_ids), len(trace.hits))
        if record.memory_id not in trace.considered_ids:
            return MemoryAudit(AuditStatus.INVALID, "HIT_NOT_CONSIDERED", len(items), len(trace.considered_ids), len(trace.hits))
        if (record.namespace, record.domain, record.purpose) != (trace.namespace, trace.domain, trace.purpose):
            return MemoryAudit(AuditStatus.INVALID, "HIT_SCOPE_MISMATCH", len(items), len(trace.considered_ids), len(trace.hits))
        if not 0.0 <= hit.score <= 1.0 or not hit.matched_terms:
            return MemoryAudit(AuditStatus.INVALID, "HIT_SCORE_OR_TERMS_INVALID", len(items), len(trace.considered_ids), len(trace.hits))
        if previous is not None and (-hit.score, -hit.record.revision, hit.record.memory_id) < previous:
            return MemoryAudit(AuditStatus.INVALID, "HIT_ORDER_INVALID", len(items), len(trace.considered_ids), len(trace.hits))
        previous = (-hit.score, -hit.record.revision, hit.record.memory_id)
    return MemoryAudit(AuditStatus.ADMITTED_FOR_REVIEW, "RETRIEVAL_TRACE_REVIEW_METADATA_ONLY", len(items), len(trace.considered_ids), len(trace.hits))


def audit_memory_lineage(records: Iterable[MemoryRecord], memory_id: str) -> MemoryAudit:
    items = {record.memory_id: record for record in records}
    current = items.get(memory_id)
    if current is None:
        return MemoryAudit(AuditStatus.INVALID, "MEMORY_ID_NOT_FOUND")
    seen: set[str] = set()
    count = 0
    while current is not None:
        if current.memory_id in seen:
            return MemoryAudit(AuditStatus.INVALID, "REVISION_CYCLE_DETECTED", count)
        seen.add(current.memory_id)
        count += 1
        if current.supersedes is None:
            break
        current = items.get(current.supersedes)
        if current is None:
            return MemoryAudit(AuditStatus.INVALID, "REVISION_PARENT_NOT_FOUND", count)
    return MemoryAudit(AuditStatus.ADMITTED_FOR_REVIEW, "MEMORY_LINEAGE_REVIEW_METADATA_ONLY", count)
