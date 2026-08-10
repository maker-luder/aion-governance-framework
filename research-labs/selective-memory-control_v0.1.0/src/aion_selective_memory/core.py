from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from enum import Enum
import re


class MemoryStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    DISCARDED = "DISCARDED"


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    memory_id: str
    namespace: str
    domain: str
    purpose: str
    content: str
    source_ref: str
    approval_ref: str
    created_at: str
    revision: int = 1
    supersedes: str | None = None
    status: MemoryStatus = MemoryStatus.ACTIVE


@dataclass(frozen=True, slots=True)
class RetrievalHit:
    record: MemoryRecord
    score: float
    matched_terms: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RetrievalTrace:
    query: str
    namespace: str
    domain: str
    purpose: str
    considered_ids: tuple[str, ...]
    blocked_ids: tuple[str, ...]
    hits: tuple[RetrievalHit, ...]


_LATIN_RE = re.compile(r"[A-Za-z0-9_]+")
_CJK_RUN_RE = re.compile(r"[\u4e00-\u9fff]+")


def _tokens(text: str) -> set[str]:
    """Deterministic lightweight tokenizer for research fixtures.

    Latin/alphanumeric tokens are word-based. CJK runs contribute single characters
    and adjacent bigrams so Chinese queries do not collapse into one giant token.
    """
    tokens = {token.casefold() for token in _LATIN_RE.findall(text)}
    for run in _CJK_RUN_RE.findall(text):
        tokens.update(run)
        tokens.update(run[index : index + 2] for index in range(len(run) - 1))
    return {token for token in tokens if token}


class SelectiveMemoryStore:
    """Deterministic selective-recall control layer for AION research.

    This is intentionally not an embedding model or autonomous write authority.
    It exposes the governance-relevant mechanics needed for controlled experiments:
    explicit write approval, namespace/domain/purpose gates, revision precedence,
    provenance preservation, and auditable retrieval traces.
    """

    def __init__(self) -> None:
        self._records: dict[str, MemoryRecord] = {}

    def add(
        self,
        *,
        memory_id: str,
        namespace: str,
        domain: str,
        purpose: str,
        content: str,
        source_ref: str,
        approval_ref: str,
        created_at: str | None = None,
    ) -> MemoryRecord:
        if memory_id in self._records:
            raise ValueError(f"memory_id already exists: {memory_id}")
        if not all(
            (memory_id, namespace, domain, purpose, content, source_ref, approval_ref)
        ):
            raise ValueError("all memory fields, including approval_ref, are required")
        record = MemoryRecord(
            memory_id=memory_id,
            namespace=namespace,
            domain=domain,
            purpose=purpose,
            content=content,
            source_ref=source_ref,
            approval_ref=approval_ref,
            created_at=created_at or datetime.now(timezone.utc).isoformat(),
        )
        self._records[memory_id] = record
        return record

    def revise(
        self,
        *,
        memory_id: str,
        new_memory_id: str,
        content: str,
        source_ref: str,
        approval_ref: str,
        created_at: str | None = None,
    ) -> MemoryRecord:
        old = self._records.get(memory_id)
        if old is None:
            raise KeyError(memory_id)
        if old.status is not MemoryStatus.ACTIVE:
            raise ValueError("only ACTIVE memories can be revised")
        if new_memory_id in self._records:
            raise ValueError(f"memory_id already exists: {new_memory_id}")
        if not approval_ref:
            raise ValueError("approval_ref is required")

        self._records[memory_id] = replace(old, status=MemoryStatus.SUPERSEDED)
        new = MemoryRecord(
            memory_id=new_memory_id,
            namespace=old.namespace,
            domain=old.domain,
            purpose=old.purpose,
            content=content,
            source_ref=source_ref,
            approval_ref=approval_ref,
            created_at=created_at or datetime.now(timezone.utc).isoformat(),
            revision=old.revision + 1,
            supersedes=old.memory_id,
        )
        self._records[new_memory_id] = new
        return new

    def discard(self, memory_id: str, *, approval_ref: str) -> MemoryRecord:
        old = self._records.get(memory_id)
        if old is None:
            raise KeyError(memory_id)
        if not approval_ref:
            raise ValueError("approval_ref is required")
        updated = replace(
            old,
            status=MemoryStatus.DISCARDED,
            approval_ref=approval_ref,
        )
        self._records[memory_id] = updated
        return updated

    def get(self, memory_id: str) -> MemoryRecord:
        return self._records[memory_id]

    def records(self) -> tuple[MemoryRecord, ...]:
        return tuple(self._records.values())

    def retrieve(
        self,
        query: str,
        *,
        namespace: str,
        domain: str,
        purpose: str,
        limit: int = 5,
    ) -> RetrievalTrace:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        query_terms = _tokens(query)
        considered: list[str] = []
        blocked: list[str] = []
        hits: list[RetrievalHit] = []

        for record in self._records.values():
            if record.status is not MemoryStatus.ACTIVE:
                blocked.append(record.memory_id)
                continue
            if (
                record.namespace != namespace
                or record.domain != domain
                or record.purpose != purpose
            ):
                blocked.append(record.memory_id)
                continue

            considered.append(record.memory_id)
            record_terms = _tokens(record.content)
            matched = tuple(sorted(query_terms & record_terms))
            if not matched:
                continue

            denom = max(1, len(query_terms | record_terms))
            score = len(matched) / denom
            hits.append(RetrievalHit(record=record, score=score, matched_terms=matched))

        hits.sort(key=lambda hit: (-hit.score, -hit.record.revision, hit.record.memory_id))
        return RetrievalTrace(
            query=query,
            namespace=namespace,
            domain=domain,
            purpose=purpose,
            considered_ids=tuple(considered),
            blocked_ids=tuple(blocked),
            hits=tuple(hits[:limit]),
        )

    def active_chain(self, memory_id: str) -> tuple[MemoryRecord, ...]:
        """Return lineage ending at memory_id by following ``supersedes`` backwards."""
        current = self._records[memory_id]
        chain = [current]
        while current.supersedes is not None:
            current = self._records[current.supersedes]
            chain.append(current)
        chain.reverse()
        return tuple(chain)
