"""Persistent, governance-gated cross-session memory storage.

This module deliberately separates persistence from canonical state. A stored
memory is evidence-bearing context, not truth and not an automatic canonical
writeback.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .gate import rank_candidates
from .models import MemoryRecord, RecallRequest


class MemoryWriteDenied(ValueError):
    """Raised when a caller attempts an unapproved or invalid memory write."""


def _clean_string_values(name: str, values: Iterable[str]) -> frozenset[str]:
    if isinstance(values, (str, bytes)):
        raise MemoryWriteDenied(f"{name} must be an iterable of strings")
    try:
        items = tuple(values)
    except TypeError as exc:
        raise MemoryWriteDenied(f"{name} must be an iterable of strings") from exc
    if any(not isinstance(item, str) for item in items):
        raise MemoryWriteDenied(f"{name} must be an iterable of strings")
    return frozenset(item.strip() for item in items if item.strip())


@dataclass(frozen=True, slots=True)
class StoredMemory:
    memory_id: str
    namespace: str
    user_id: str
    agent_id: str
    content: str
    entities: frozenset[str]
    topics: frozenset[str]
    access_scope: frozenset[str]
    provenance_source: str
    provenance_verified: bool
    recorded_at: str
    conflict: bool = False
    tombstoned: bool = False
    superseded: bool = False
    canonical_effect: str = "NONE"

    def governance_record(self) -> MemoryRecord:
        return MemoryRecord(
            memory_id=self.memory_id,
            namespace=self.namespace,
            user_id=self.user_id,
            agent_id=self.agent_id,
            entities=self.entities,
            topics=self.topics,
            access_scope=self.access_scope,
            provenance_verified=self.provenance_verified,
            conflict=self.conflict,
            tombstoned=self.tombstoned,
            superseded=self.superseded,
            canonical_effect=self.canonical_effect,
        )


class SQLiteMemoryStore:
    """Small local persistent store with explicit write approval and recall gates."""

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS memory_records (
                    memory_id TEXT PRIMARY KEY,
                    namespace TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    entities_json TEXT NOT NULL,
                    topics_json TEXT NOT NULL,
                    access_scope_json TEXT NOT NULL,
                    provenance_source TEXT NOT NULL,
                    provenance_verified INTEGER NOT NULL,
                    recorded_at TEXT NOT NULL,
                    conflict INTEGER NOT NULL DEFAULT 0,
                    tombstoned INTEGER NOT NULL DEFAULT 0,
                    superseded INTEGER NOT NULL DEFAULT 0,
                    canonical_effect TEXT NOT NULL CHECK (canonical_effect = 'NONE')
                )
                """
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_memory_identity ON memory_records(user_id, agent_id, namespace)"
            )

    def write(
        self,
        *,
        memory_id: str,
        namespace: str,
        user_id: str,
        agent_id: str,
        content: str,
        entities: Iterable[str] = (),
        topics: Iterable[str] = (),
        access_scope: Iterable[str] = (),
        provenance_source: str,
        provenance_verified: bool,
        writeback_approved: bool,
        recorded_at: str | None = None,
    ) -> StoredMemory:
        if not isinstance(writeback_approved, bool):
            raise MemoryWriteDenied("writeback_approved must be a boolean")
        if not isinstance(provenance_verified, bool):
            raise MemoryWriteDenied("provenance_verified must be a boolean")
        if not writeback_approved:
            raise MemoryWriteDenied("explicit writeback approval is required")
        required = {
            "memory_id": memory_id,
            "namespace": namespace,
            "user_id": user_id,
            "agent_id": agent_id,
            "content": content,
            "provenance_source": provenance_source,
        }
        non_string = [name for name, value in required.items() if not isinstance(value, str)]
        if non_string:
            raise MemoryWriteDenied(f"required fields must be a string: {', '.join(sorted(non_string))}")
        blank = [name for name, value in required.items() if not value.strip()]
        if blank:
            raise MemoryWriteDenied(f"blank required fields: {', '.join(sorted(blank))}")
        if recorded_at is not None and (not isinstance(recorded_at, str) or not recorded_at.strip()):
            raise MemoryWriteDenied("recorded_at must be a non-blank string")

        timestamp = recorded_at or datetime.now(timezone.utc).isoformat()
        entity_values = _clean_string_values("entities", entities)
        topic_values = _clean_string_values("topics", topics)
        scope_values = _clean_string_values("access_scope", access_scope)

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO memory_records (
                    memory_id, namespace, user_id, agent_id, content,
                    entities_json, topics_json, access_scope_json,
                    provenance_source, provenance_verified, recorded_at,
                    conflict, tombstoned, superseded, canonical_effect
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0, 'NONE')
                """,
                (
                    memory_id,
                    namespace,
                    user_id,
                    agent_id,
                    content,
                    json.dumps(sorted(entity_values), ensure_ascii=False),
                    json.dumps(sorted(topic_values), ensure_ascii=False),
                    json.dumps(sorted(scope_values), ensure_ascii=False),
                    provenance_source,
                    int(provenance_verified),
                    timestamp,
                ),
            )

        return self.get(memory_id)

    def get(self, memory_id: str) -> StoredMemory:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM memory_records WHERE memory_id = ?", (memory_id,)
            ).fetchone()
        if row is None:
            raise KeyError(memory_id)
        return self._decode(row)

    def list_for_identity(self, *, user_id: str, agent_id: str) -> list[StoredMemory]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM memory_records WHERE user_id = ? AND agent_id = ? ORDER BY recorded_at, memory_id",
                (user_id, agent_id),
            ).fetchall()
        return [self._decode(row) for row in rows]

    def recall(
        self,
        request: RecallRequest,
        *,
        limit: int = 8,
        namespace: str | None = None,
    ) -> list[StoredMemory]:
        if limit < 1 or limit > 64:
            raise ValueError("limit must be between 1 and 64")
        stored = self.list_for_identity(user_id=request.user_id, agent_id=request.agent_id)
        if namespace is not None:
            stored = [item for item in stored if item.namespace == namespace]
        by_id = {item.memory_id: item for item in stored}
        ranked = rank_candidates(request, (item.governance_record() for item in stored))
        return [by_id[item.memory_id] for item in ranked[:limit]]

    def set_conflict(self, memory_id: str, *, conflict: bool = True) -> None:
        self._set_flag(memory_id, "conflict", conflict)

    def tombstone(self, memory_id: str) -> None:
        self._set_flag(memory_id, "tombstoned", True)

    def supersede(self, memory_id: str) -> None:
        self._set_flag(memory_id, "superseded", True)

    def _set_flag(self, memory_id: str, column: str, value: bool) -> None:
        if column not in {"conflict", "tombstoned", "superseded"}:
            raise ValueError("unsupported memory flag")
        with self._connect() as connection:
            cursor = connection.execute(
                f"UPDATE memory_records SET {column} = ? WHERE memory_id = ?",
                (int(value), memory_id),
            )
            if cursor.rowcount != 1:
                raise KeyError(memory_id)

    @staticmethod
    def _decode(row: sqlite3.Row) -> StoredMemory:
        return StoredMemory(
            memory_id=str(row["memory_id"]),
            namespace=str(row["namespace"]),
            user_id=str(row["user_id"]),
            agent_id=str(row["agent_id"]),
            content=str(row["content"]),
            entities=frozenset(json.loads(str(row["entities_json"]))),
            topics=frozenset(json.loads(str(row["topics_json"]))),
            access_scope=frozenset(json.loads(str(row["access_scope_json"]))),
            provenance_source=str(row["provenance_source"]),
            provenance_verified=bool(row["provenance_verified"]),
            recorded_at=str(row["recorded_at"]),
            conflict=bool(row["conflict"]),
            tombstoned=bool(row["tombstoned"]),
            superseded=bool(row["superseded"]),
            canonical_effect=str(row["canonical_effect"]),
        )
