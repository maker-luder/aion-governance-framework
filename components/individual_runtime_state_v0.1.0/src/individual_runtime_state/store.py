"""Persistent individual runtime event lineage, checkpoints, recovery and migration."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from aion_astra_runtime.models import IndividualRuntimeContext


class RuntimeStateError(ValueError):
    """Raised when individual runtime state invariants are violated."""


@dataclass(frozen=True, slots=True)
class RuntimeEvent:
    sequence: int
    event_type: str
    occurred_at: str
    context: IndividualRuntimeContext
    payload: dict[str, Any]
    previous_hash: str
    event_hash: str


@dataclass(frozen=True, slots=True)
class RuntimeCheckpoint:
    checkpoint_id: str
    sequence: int
    context: IndividualRuntimeContext
    state_reference: str
    memory_reference: str
    created_at: str
    canonical_effect: str = "NONE"


@dataclass(frozen=True, slots=True)
class RecoveryState:
    context: IndividualRuntimeContext
    last_sequence: int
    last_event_hash: str
    checkpoint: RuntimeCheckpoint | None
    lineage_valid: bool


@dataclass(frozen=True, slots=True)
class EnvironmentEvidence:
    evidence_id: str
    device_id: str
    fingerprint: str
    hardware_profile_hash: str
    runtime_environment_hash: str
    policy_config_hash: str
    verification_reference: str
    verification_status: str
    verified_at: str


@dataclass(frozen=True, slots=True)
class MigrationSummary:
    source_evidence_id: str
    target_evidence_id: str
    migration_count: int
    first_sequence: int
    last_sequence: int


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _hash(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _row_text(row: sqlite3.Row, column: str) -> str:
    value = row[column]
    if not isinstance(value, str) or not value.strip():
        raise RuntimeStateError(f"malformed runtime event column: {column}")
    return value


def _row_int(row: sqlite3.Row, column: str) -> int:
    value = row[column]
    if type(value) is not int or value < 0:
        raise RuntimeStateError(f"malformed runtime event column: {column}")
    return value


def _decode_payload(raw: object) -> dict[str, Any]:
    if not isinstance(raw, str):
        raise RuntimeStateError("malformed runtime event payload encoding")
    try:
        payload = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc:
        raise RuntimeStateError("malformed runtime event payload JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeStateError("runtime event payload must be a JSON object")
    return payload


class IndividualRuntimeStateStore:
    """Append-only state store bound to one individual runtime context.

    A lineage may continue across runtime-instance migration, but agent identity,
    memory stream, event lineage, canonical-state reference and genesis root are
    immutable within that lineage. Device/environment evidence is content-addressed
    and reusable; migration events remain unique and append-only.
    """

    def __init__(self, path: str | Path, context: IndividualRuntimeContext) -> None:
        context.validate()
        self.path = str(path)
        self.context = context
        self._initialize()
        self._validate_existing_lineage_binding()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS runtime_events (
                    event_lineage_id TEXT NOT NULL,
                    sequence INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    runtime_instance_id TEXT NOT NULL,
                    memory_stream_id TEXT NOT NULL,
                    canonical_state_reference TEXT NOT NULL,
                    genesis_root_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    previous_hash TEXT NOT NULL,
                    event_hash TEXT NOT NULL,
                    PRIMARY KEY (event_lineage_id, sequence),
                    UNIQUE (event_hash)
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS runtime_checkpoints (
                    checkpoint_id TEXT PRIMARY KEY,
                    event_lineage_id TEXT NOT NULL,
                    sequence INTEGER NOT NULL,
                    agent_id TEXT NOT NULL,
                    runtime_instance_id TEXT NOT NULL,
                    memory_stream_id TEXT NOT NULL,
                    canonical_state_reference TEXT NOT NULL,
                    genesis_root_id TEXT NOT NULL,
                    state_reference TEXT NOT NULL,
                    memory_reference TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    canonical_effect TEXT NOT NULL CHECK (canonical_effect = 'NONE')
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS runtime_environment_evidence (
                    evidence_id TEXT PRIMARY KEY,
                    device_id TEXT NOT NULL,
                    fingerprint TEXT NOT NULL UNIQUE,
                    hardware_profile_hash TEXT NOT NULL,
                    runtime_environment_hash TEXT NOT NULL,
                    policy_config_hash TEXT NOT NULL,
                    verification_reference TEXT NOT NULL,
                    verification_status TEXT NOT NULL,
                    verified_at TEXT NOT NULL
                )
                """
            )

    @staticmethod
    def _stable_identity(context: IndividualRuntimeContext) -> tuple[str, str, str, str, str]:
        return (
            context.agent_id,
            context.memory_stream_id,
            context.event_lineage_id,
            context.canonical_state_reference,
            context.genesis_root_id,
        )

    def _validate_existing_lineage_binding(self) -> None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM runtime_events WHERE event_lineage_id = ? ORDER BY sequence LIMIT 1",
                (self.context.event_lineage_id,),
            ).fetchone()
        if row is None:
            return
        existing = IndividualRuntimeContext(
            agent_id=str(row["agent_id"]),
            runtime_instance_id=str(row["runtime_instance_id"]),
            memory_stream_id=str(row["memory_stream_id"]),
            event_lineage_id=self.context.event_lineage_id,
            canonical_state_reference=str(row["canonical_state_reference"]),
            genesis_root_id=str(row["genesis_root_id"]),
        )
        if self._stable_identity(existing) != self._stable_identity(self.context):
            raise RuntimeStateError("runtime context conflicts with the existing individual event lineage")

    def append_event(self, event_type: str, payload: dict[str, Any] | None = None) -> RuntimeEvent:
        if not event_type.strip():
            raise RuntimeStateError("event_type must be non-empty")
        clean_payload = dict(payload or {})
        occurred_at = _now()
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            previous = connection.execute(
                "SELECT sequence, event_hash FROM runtime_events WHERE event_lineage_id = ? ORDER BY sequence DESC LIMIT 1",
                (self.context.event_lineage_id,),
            ).fetchone()
            sequence = 1 if previous is None else int(previous["sequence"]) + 1
            previous_hash = "GENESIS" if previous is None else str(previous["event_hash"])
            body = {
                "event_lineage_id": self.context.event_lineage_id,
                "sequence": sequence,
                "event_type": event_type,
                "occurred_at": occurred_at,
                "context": self.context.to_dict(),
                "payload": clean_payload,
                "previous_hash": previous_hash,
            }
            event_hash = _hash(body)
            connection.execute(
                """
                INSERT INTO runtime_events (
                    event_lineage_id, sequence, event_type, occurred_at,
                    agent_id, runtime_instance_id, memory_stream_id,
                    canonical_state_reference, genesis_root_id, payload_json,
                    previous_hash, event_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.context.event_lineage_id,
                    sequence,
                    event_type,
                    occurred_at,
                    self.context.agent_id,
                    self.context.runtime_instance_id,
                    self.context.memory_stream_id,
                    self.context.canonical_state_reference,
                    self.context.genesis_root_id,
                    _canonical(clean_payload),
                    previous_hash,
                    event_hash,
                ),
            )
        return RuntimeEvent(sequence, event_type, occurred_at, self.context, clean_payload, previous_hash, event_hash)

    def events(self) -> list[RuntimeEvent]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM runtime_events WHERE event_lineage_id = ? ORDER BY sequence",
                (self.context.event_lineage_id,),
            ).fetchall()
        result: list[RuntimeEvent] = []
        for row in rows:
            try:
                context = IndividualRuntimeContext(
                    agent_id=_row_text(row, "agent_id"),
                    runtime_instance_id=_row_text(row, "runtime_instance_id"),
                    memory_stream_id=_row_text(row, "memory_stream_id"),
                    event_lineage_id=_row_text(row, "event_lineage_id"),
                    canonical_state_reference=_row_text(row, "canonical_state_reference"),
                    genesis_root_id=_row_text(row, "genesis_root_id"),
                )
                context.validate()
                event_lineage_id = _row_text(row, "event_lineage_id")
                if event_lineage_id != self.context.event_lineage_id:
                    raise RuntimeStateError("runtime event lineage does not match the bound context")
                result.append(
                    RuntimeEvent(
                        sequence=_row_int(row, "sequence"),
                        event_type=_row_text(row, "event_type"),
                        occurred_at=_row_text(row, "occurred_at"),
                        context=context,
                        payload=_decode_payload(row["payload_json"]),
                        previous_hash=_row_text(row, "previous_hash"),
                        event_hash=_row_text(row, "event_hash"),
                    )
                )
            except RuntimeStateError:
                raise
            except (KeyError, TypeError, ValueError) as exc:
                raise RuntimeStateError("malformed runtime event row") from exc
        return result

    def lifecycle_state(self) -> str:
        state = "INITIALIZED"
        for event in self.events():
            if event.event_type == "runtime.started":
                if state == "RUNNING":
                    raise RuntimeStateError("runtime lifecycle contains a duplicate start")
                state = "RUNNING"
            elif event.event_type == "runtime.stopped":
                if state != "RUNNING":
                    raise RuntimeStateError("runtime lifecycle contains a stop before start")
                state = "STOPPED"
        return state

    def verify(self) -> bool:
        try:
            events = self.events()
        except RuntimeStateError:
            return False
        previous_hash = "GENESIS"
        stable = self._stable_identity(self.context)
        for expected_sequence, event in enumerate(events, start=1):
            if event.sequence != expected_sequence or event.previous_hash != previous_hash:
                return False
            if self._stable_identity(event.context) != stable:
                return False
            body = {
                "event_lineage_id": event.context.event_lineage_id,
                "sequence": event.sequence,
                "event_type": event.event_type,
                "occurred_at": event.occurred_at,
                "context": event.context.to_dict(),
                "payload": event.payload,
                "previous_hash": event.previous_hash,
            }
            if _hash(body) != event.event_hash:
                return False
            previous_hash = event.event_hash
        return True

    def register_environment_evidence(
        self,
        *,
        device_id: str,
        hardware_profile_hash: str,
        runtime_environment_hash: str,
        policy_config_hash: str,
        verification_reference: str,
        verification_status: str = "PASS",
    ) -> EnvironmentEvidence:
        required = {
            "device_id": device_id,
            "hardware_profile_hash": hardware_profile_hash,
            "runtime_environment_hash": runtime_environment_hash,
            "policy_config_hash": policy_config_hash,
            "verification_reference": verification_reference,
            "verification_status": verification_status,
        }
        blank = [name for name, value in required.items() if not value.strip()]
        if blank:
            raise RuntimeStateError(f"blank environment evidence fields: {', '.join(sorted(blank))}")
        fingerprint = _hash(
            {
                "device_id": device_id,
                "hardware_profile_hash": hardware_profile_hash,
                "runtime_environment_hash": runtime_environment_hash,
                "policy_config_hash": policy_config_hash,
            }
        )
        with self._connect() as connection:
            existing = connection.execute(
                "SELECT * FROM runtime_environment_evidence WHERE fingerprint = ?",
                (fingerprint,),
            ).fetchone()
            if existing is not None:
                return self._decode_environment_evidence(existing)
            evidence_id = f"ENV-{fingerprint[:24].upper()}"
            verified_at = _now()
            connection.execute(
                """
                INSERT INTO runtime_environment_evidence (
                    evidence_id, device_id, fingerprint, hardware_profile_hash,
                    runtime_environment_hash, policy_config_hash,
                    verification_reference, verification_status, verified_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(fingerprint) DO NOTHING
                """,
                (
                    evidence_id,
                    device_id,
                    fingerprint,
                    hardware_profile_hash,
                    runtime_environment_hash,
                    policy_config_hash,
                    verification_reference,
                    verification_status,
                    verified_at,
                ),
            )
            stored = connection.execute(
                "SELECT * FROM runtime_environment_evidence WHERE fingerprint = ?",
                (fingerprint,),
            ).fetchone()
            if stored is None:
                raise RuntimeStateError("environment evidence upsert did not produce a stored artifact")
            return self._decode_environment_evidence(stored)

    def get_environment_evidence(self, evidence_id: str) -> EnvironmentEvidence:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM runtime_environment_evidence WHERE evidence_id = ?",
                (evidence_id,),
            ).fetchone()
        if row is None:
            raise KeyError(evidence_id)
        return self._decode_environment_evidence(row)

    def checkpoint(
        self,
        *,
        checkpoint_id: str,
        state_reference: str,
        memory_reference: str,
        owner_approved: bool,
    ) -> RuntimeCheckpoint:
        if not owner_approved:
            raise RuntimeStateError("explicit Owner approval is required for checkpoint creation")
        if not checkpoint_id.strip() or not state_reference.strip() or not memory_reference.strip():
            raise RuntimeStateError("checkpoint identifiers and references must be non-empty")
        events = self.events()
        sequence = 0 if not events else events[-1].sequence
        created_at = _now()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO runtime_checkpoints (
                    checkpoint_id, event_lineage_id, sequence, agent_id,
                    runtime_instance_id, memory_stream_id,
                    canonical_state_reference, genesis_root_id,
                    state_reference, memory_reference, created_at, canonical_effect
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'NONE')
                """,
                (
                    checkpoint_id,
                    self.context.event_lineage_id,
                    sequence,
                    self.context.agent_id,
                    self.context.runtime_instance_id,
                    self.context.memory_stream_id,
                    self.context.canonical_state_reference,
                    self.context.genesis_root_id,
                    state_reference,
                    memory_reference,
                    created_at,
                ),
            )
        self.append_event("runtime.checkpoint_created", {"checkpoint_id": checkpoint_id, "checkpoint_sequence": sequence})
        return RuntimeCheckpoint(checkpoint_id, sequence, self.context, state_reference, memory_reference, created_at)

    def latest_checkpoint(self) -> RuntimeCheckpoint | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM runtime_checkpoints WHERE event_lineage_id = ? ORDER BY sequence DESC, created_at DESC LIMIT 1",
                (self.context.event_lineage_id,),
            ).fetchone()
        return None if row is None else self._decode_checkpoint(row)

    def recover(self) -> RecoveryState:
        if not self.verify():
            raise RuntimeStateError("event lineage verification failed; recovery denied")
        events = self.events()
        last_sequence = 0 if not events else events[-1].sequence
        last_hash = "GENESIS" if not events else events[-1].event_hash
        return RecoveryState(self.context, last_sequence, last_hash, self.latest_checkpoint(), True)

    def rollback_to_checkpoint(self, checkpoint_id: str, *, owner_approved: bool) -> RuntimeCheckpoint:
        if not owner_approved:
            raise RuntimeStateError("explicit Owner approval is required for rollback")
        checkpoint = self.get_checkpoint(checkpoint_id)
        self.append_event(
            "runtime.rollback_requested",
            {
                "checkpoint_id": checkpoint.checkpoint_id,
                "state_reference": checkpoint.state_reference,
                "memory_reference": checkpoint.memory_reference,
                "history_truncated": False,
                "canonical_effect": "NONE",
            },
        )
        return checkpoint

    def migrate_instance(
        self,
        new_context: IndividualRuntimeContext,
        *,
        owner_approved: bool,
        source_evidence_id: str,
        target_evidence_id: str,
    ) -> "IndividualRuntimeStateStore":
        if not owner_approved:
            raise RuntimeStateError("explicit Owner approval is required for runtime migration")
        new_context.validate()
        if self._stable_identity(new_context) != self._stable_identity(self.context):
            raise RuntimeStateError("migration may not change individual lineage ownership")
        if new_context.runtime_instance_id == self.context.runtime_instance_id:
            raise RuntimeStateError("migration requires a new runtime_instance_id")
        source_evidence = self.get_environment_evidence(source_evidence_id)
        target_evidence = self.get_environment_evidence(target_evidence_id)
        if source_evidence.verification_status != "PASS" or target_evidence.verification_status != "PASS":
            raise RuntimeStateError("migration requires PASS environment evidence for source and target")
        reference_payload = {
            "from_runtime_instance_id": self.context.runtime_instance_id,
            "to_runtime_instance_id": new_context.runtime_instance_id,
            "source_evidence_id": source_evidence.evidence_id,
            "target_evidence_id": target_evidence.evidence_id,
            "canonical_effect": "NONE",
        }
        self.append_event("runtime.migrating_out", reference_payload)
        migrated = IndividualRuntimeStateStore(self.path, new_context)
        migrated.append_event("runtime.migrated_in", reference_payload)
        return migrated

    def migration_summary(self) -> list[MigrationSummary]:
        grouped: dict[tuple[str, str], list[int]] = {}
        for event in self.events():
            if event.event_type != "runtime.migrating_out":
                continue
            source = str(event.payload.get("source_evidence_id", ""))
            target = str(event.payload.get("target_evidence_id", ""))
            if not source or not target:
                continue
            grouped.setdefault((source, target), []).append(event.sequence)
        return [
            MigrationSummary(
                source_evidence_id=source,
                target_evidence_id=target,
                migration_count=len(sequences),
                first_sequence=min(sequences),
                last_sequence=max(sequences),
            )
            for (source, target), sequences in sorted(grouped.items())
        ]

    def get_checkpoint(self, checkpoint_id: str) -> RuntimeCheckpoint:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM runtime_checkpoints WHERE checkpoint_id = ? AND event_lineage_id = ?",
                (checkpoint_id, self.context.event_lineage_id),
            ).fetchone()
        if row is None:
            raise KeyError(checkpoint_id)
        return self._decode_checkpoint(row)

    @staticmethod
    def _decode_checkpoint(row: sqlite3.Row) -> RuntimeCheckpoint:
        context = IndividualRuntimeContext(
            agent_id=str(row["agent_id"]),
            runtime_instance_id=str(row["runtime_instance_id"]),
            memory_stream_id=str(row["memory_stream_id"]),
            event_lineage_id=str(row["event_lineage_id"]),
            canonical_state_reference=str(row["canonical_state_reference"]),
            genesis_root_id=str(row["genesis_root_id"]),
        )
        return RuntimeCheckpoint(
            checkpoint_id=str(row["checkpoint_id"]),
            sequence=int(row["sequence"]),
            context=context,
            state_reference=str(row["state_reference"]),
            memory_reference=str(row["memory_reference"]),
            created_at=str(row["created_at"]),
            canonical_effect=str(row["canonical_effect"]),
        )

    @staticmethod
    def _decode_environment_evidence(row: sqlite3.Row) -> EnvironmentEvidence:
        return EnvironmentEvidence(
            evidence_id=str(row["evidence_id"]),
            device_id=str(row["device_id"]),
            fingerprint=str(row["fingerprint"]),
            hardware_profile_hash=str(row["hardware_profile_hash"]),
            runtime_environment_hash=str(row["runtime_environment_hash"]),
            policy_config_hash=str(row["policy_config_hash"]),
            verification_reference=str(row["verification_reference"]),
            verification_status=str(row["verification_status"]),
            verified_at=str(row["verified_at"]),
        )
