from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

from .models import RecoveryRecord, WholeSystemEvent, WholeSystemStage, WholeSystemStatus


class WholeSystemStorageError(RuntimeError):
    """Raised when append-only state storage detects corruption or invalid transitions."""


class SQLiteWholeSystemStore:
    """Persistent event/checkpoint store with a recoverable write-ahead intent."""

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=2.0)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS whole_system_events (
                    run_id TEXT NOT NULL,
                    sequence INTEGER NOT NULL,
                    event_id TEXT NOT NULL UNIQUE,
                    stage TEXT NOT NULL,
                    status TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    canonical_effect TEXT NOT NULL CHECK (canonical_effect = 'NONE'),
                    previous_hash TEXT NOT NULL,
                    event_hash TEXT NOT NULL,
                    PRIMARY KEY (run_id, sequence)
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS whole_system_checkpoints (
                    run_id TEXT NOT NULL,
                    checkpoint_id TEXT NOT NULL,
                    last_sequence INTEGER NOT NULL,
                    state_json TEXT NOT NULL,
                    state_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    canonical_effect TEXT NOT NULL CHECK (canonical_effect = 'NONE'),
                    PRIMARY KEY (run_id, checkpoint_id)
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS whole_system_writeback_intents (
                    transaction_id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    memory_id TEXT NOT NULL,
                    content_digest TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    canonical_effect TEXT NOT NULL CHECK (canonical_effect = 'NONE')
                )
                """
            )

    def next_sequence(self, run_id: str) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT COALESCE(MAX(sequence), 0) AS last_sequence FROM whole_system_events WHERE run_id = ?",
                (run_id,),
            ).fetchone()
        return int(row["last_sequence"]) + 1

    def append(self, event: WholeSystemEvent) -> WholeSystemEvent:
        with self._connect() as connection:
            return self._append_in_connection(connection, event)

    def _append_in_connection(self, connection: sqlite3.Connection, event: WholeSystemEvent) -> WholeSystemEvent:
        row = connection.execute(
            "SELECT COALESCE(MAX(sequence), 0) AS last_sequence FROM whole_system_events WHERE run_id = ?",
            (event.run_id,),
        ).fetchone()
        expected = int(row["last_sequence"]) + 1
        if event.sequence != expected:
            raise WholeSystemStorageError(
                f"event sequence gap for {event.run_id}: expected {expected}, got {event.sequence}"
            )
        previous_row = connection.execute(
            "SELECT event_hash FROM whole_system_events WHERE run_id = ? ORDER BY sequence DESC LIMIT 1",
            (event.run_id,),
        ).fetchone()
        previous_hash = str(previous_row["event_hash"]) if previous_row else ""
        payload = {
            "event_id": event.event_id,
            "run_id": event.run_id,
            "sequence": event.sequence,
            "stage": event.stage.value,
            "status": event.status.value if isinstance(event.status, WholeSystemStatus) else str(event.status),
            "payload": dict(event.payload),
            "occurred_at": event.occurred_at,
            "canonical_effect": event.canonical_effect,
            "previous_hash": previous_hash,
        }
        event_hash = hashlib.sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
        ).hexdigest()
        stored = WholeSystemEvent(
            event_id=event.event_id,
            run_id=event.run_id,
            sequence=event.sequence,
            stage=event.stage,
            status=event.status,
            payload=dict(event.payload),
            occurred_at=event.occurred_at,
            canonical_effect="NONE",
            event_hash=event_hash,
        )
        try:
            connection.execute(
                """
                INSERT INTO whole_system_events (
                    run_id, sequence, event_id, stage, status, payload_json,
                    occurred_at, canonical_effect, previous_hash, event_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'NONE', ?, ?)
                """,
                (
                    stored.run_id,
                    stored.sequence,
                    stored.event_id,
                    stored.stage.value,
                    stored.status.value if isinstance(stored.status, WholeSystemStatus) else str(stored.status),
                    json.dumps(dict(stored.payload), ensure_ascii=False, sort_keys=True, default=str),
                    stored.occurred_at,
                    previous_hash,
                    event_hash,
                ),
            )
        except sqlite3.IntegrityError as exc:
            raise WholeSystemStorageError("append-only event insertion failed") from exc
        return stored

    def save_checkpoint(self, *, run_id: str, checkpoint_id: str, state: Mapping[str, Any]) -> str:
        last_sequence = self.next_sequence(run_id) - 1
        state_json = json.dumps(dict(state), ensure_ascii=False, sort_keys=True, default=str)
        state_hash = hashlib.sha256(state_json.encode("utf-8")).hexdigest()
        created_at = datetime.now(UTC).isoformat()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO whole_system_checkpoints (
                    run_id, checkpoint_id, last_sequence, state_json, state_hash,
                    created_at, canonical_effect
                ) VALUES (?, ?, ?, ?, ?, ?, 'NONE')
                """,
                (run_id, checkpoint_id, last_sequence, state_json, state_hash, created_at),
            )
        return checkpoint_id

    def begin_writeback_intent(self, *, run_id: str, memory_id: str, content: str) -> str:
        transaction_id = f"{run_id}:writeback:{memory_id}"
        now = datetime.now(UTC).isoformat()
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO whole_system_writeback_intents (
                    transaction_id, run_id, memory_id, content_digest, status,
                    created_at, updated_at, reason, canonical_effect
                ) VALUES (?, ?, ?, ?, 'PENDING', ?, ?, 'memory write is awaiting durable governance commit', 'NONE')
                """,
                (transaction_id, run_id, memory_id, digest, now, now),
            )
        return transaction_id

    def mark_writeback_intent(self, transaction_id: str, *, status: str, reason: str) -> None:
        if status not in {"COMMITTED", "ABORTED", "RECONCILED_COMMITTED", "RECONCILED_ABORTED"}:
            raise WholeSystemStorageError(f"unsupported writeback intent status: {status}")
        now = datetime.now(UTC).isoformat()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE whole_system_writeback_intents
                SET status = ?, updated_at = ?, reason = ?
                WHERE transaction_id = ? AND status = 'PENDING'
                """,
                (status, now, reason, transaction_id),
            )
            if cursor.rowcount != 1:
                raise WholeSystemStorageError(f"writeback intent is missing or already resolved: {transaction_id}")

    def pending_intents(self, run_id: str | None = None) -> tuple[dict[str, Any], ...]:
        query = "SELECT * FROM whole_system_writeback_intents WHERE status = 'PENDING'"
        values: tuple[Any, ...] = ()
        if run_id is not None:
            query += " AND run_id = ?"
            values = (run_id,)
        query += " ORDER BY created_at, transaction_id"
        with self._connect() as connection:
            rows = connection.execute(query, values).fetchall()
        return tuple(dict(row) for row in rows)

    def latest_checkpoint(self, run_id: str) -> tuple[str, int, dict[str, Any]] | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT checkpoint_id, last_sequence, state_json, state_hash
                FROM whole_system_checkpoints
                WHERE run_id = ? ORDER BY created_at DESC, checkpoint_id DESC LIMIT 1
                """,
                (run_id,),
            ).fetchone()
        if row is None:
            return None
        state_json = str(row["state_json"])
        expected_hash = hashlib.sha256(state_json.encode("utf-8")).hexdigest()
        if expected_hash != str(row["state_hash"]):
            raise WholeSystemStorageError("checkpoint hash mismatch")
        return str(row["checkpoint_id"]), int(row["last_sequence"]), json.loads(state_json)

    def events(self, run_id: str) -> tuple[WholeSystemEvent, ...]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM whole_system_events WHERE run_id = ? ORDER BY sequence",
                (run_id,),
            ).fetchall()
        return tuple(self._decode(row) for row in rows)

    def verify_chain(self, run_id: str) -> bool:
        previous_hash = ""
        expected_sequence = 1
        for event in self.events(run_id):
            if event.sequence != expected_sequence:
                return False
            payload = {
                "event_id": event.event_id,
                "run_id": event.run_id,
                "sequence": event.sequence,
                "stage": event.stage.value,
                "status": event.status.value if isinstance(event.status, WholeSystemStatus) else str(event.status),
                "payload": dict(event.payload),
                "occurred_at": event.occurred_at,
                "canonical_effect": event.canonical_effect,
                "previous_hash": previous_hash,
            }
            expected_hash = hashlib.sha256(
                json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
            ).hexdigest()
            if event.event_hash != expected_hash:
                return False
            previous_hash = event.event_hash
            expected_sequence += 1
        return True

    def recover(self, run_id: str) -> RecoveryRecord:
        events = self.events(run_id)
        checkpoint = self.latest_checkpoint(run_id)
        checkpoint_id = checkpoint[0] if checkpoint else None
        state = checkpoint[2] if checkpoint else {}
        pending = self.pending_intents(run_id)
        if pending:
            state = {**state, "pending_transactions": [item["transaction_id"] for item in pending]}
        return RecoveryRecord(
            run_id=run_id,
            last_sequence=events[-1].sequence if events else 0,
            checkpoint_id=checkpoint_id,
            state=state,
            chain_valid=self.verify_chain(run_id),
            events=events,
        )

    def _decode(self, row: sqlite3.Row) -> WholeSystemEvent:
        status_raw = str(row["status"])
        try:
            status: WholeSystemStatus | str = WholeSystemStatus(status_raw)
        except ValueError:
            status = status_raw
        return WholeSystemEvent(
            event_id=str(row["event_id"]),
            run_id=str(row["run_id"]),
            sequence=int(row["sequence"]),
            stage=WholeSystemStage(str(row["stage"])),
            status=status,
            payload=json.loads(str(row["payload_json"])),
            occurred_at=str(row["occurred_at"]),
            canonical_effect=str(row["canonical_effect"]),
            event_hash=str(row["event_hash"]),
        )
