"""Recoverability hardening for the individual Runtime state candidate.

This layer deliberately strengthens integrity/atomicity without changing the
project's non-claims: recovery remains Owner-governed metadata/reference
recovery, not arbitrary physical database/file restoration and not autonomous
self-repair.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from aion_astra_runtime.models import IndividualRuntimeContext

from .store import (
    IndividualRuntimeStateStore as _BaseIndividualRuntimeStateStore,
    RecoveryState,
    RuntimeCheckpoint,
    RuntimeEvent,
    RuntimeStateError,
    _canonical,
    _hash,
    _now,
)


class IndividualRuntimeStateStore(_BaseIndividualRuntimeStateStore):
    """Fail-closed recoverability hardening over the base append-only store.

    Added controls:
    - checkpoint rows carry a content hash and are verified before use;
    - checkpoint metadata is bound back into the append-only event lineage;
    - migration ``migrating_out`` / ``migrated_in`` events are committed in one
      SQLite transaction so a failed second write cannot leave a half migration;
    - lineage verification treats an unpaired/mismatched migration transition as
      invalid.
    """

    def _initialize(self) -> None:
        super()._initialize()
        with self._connect() as connection:
            columns = {
                str(row["name"])
                for row in connection.execute("PRAGMA table_info(runtime_checkpoints)").fetchall()
            }
            if "checkpoint_hash" not in columns:
                connection.execute(
                    "ALTER TABLE runtime_checkpoints ADD COLUMN checkpoint_hash TEXT NOT NULL DEFAULT ''"
                )

    @staticmethod
    def _checkpoint_hash(
        *,
        checkpoint_id: str,
        event_lineage_id: str,
        sequence: int,
        agent_id: str,
        runtime_instance_id: str,
        memory_stream_id: str,
        canonical_state_reference: str,
        genesis_root_id: str,
        state_reference: str,
        memory_reference: str,
        created_at: str,
        canonical_effect: str,
    ) -> str:
        return _hash(
            {
                "checkpoint_id": checkpoint_id,
                "event_lineage_id": event_lineage_id,
                "sequence": sequence,
                "agent_id": agent_id,
                "runtime_instance_id": runtime_instance_id,
                "memory_stream_id": memory_stream_id,
                "canonical_state_reference": canonical_state_reference,
                "genesis_root_id": genesis_root_id,
                "state_reference": state_reference,
                "memory_reference": memory_reference,
                "created_at": created_at,
                "canonical_effect": canonical_effect,
            }
        )

    @classmethod
    def _decode_checkpoint(cls, row: sqlite3.Row) -> RuntimeCheckpoint:
        expected = cls._checkpoint_hash(
            checkpoint_id=str(row["checkpoint_id"]),
            event_lineage_id=str(row["event_lineage_id"]),
            sequence=int(row["sequence"]),
            agent_id=str(row["agent_id"]),
            runtime_instance_id=str(row["runtime_instance_id"]),
            memory_stream_id=str(row["memory_stream_id"]),
            canonical_state_reference=str(row["canonical_state_reference"]),
            genesis_root_id=str(row["genesis_root_id"]),
            state_reference=str(row["state_reference"]),
            memory_reference=str(row["memory_reference"]),
            created_at=str(row["created_at"]),
            canonical_effect=str(row["canonical_effect"]),
        )
        stored = str(row["checkpoint_hash"])
        if not stored or stored != expected:
            raise RuntimeStateError("checkpoint integrity verification failed; recovery/rollback denied")
        return super()._decode_checkpoint(row)

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
        checkpoint_hash = self._checkpoint_hash(
            checkpoint_id=checkpoint_id,
            event_lineage_id=self.context.event_lineage_id,
            sequence=sequence,
            agent_id=self.context.agent_id,
            runtime_instance_id=self.context.runtime_instance_id,
            memory_stream_id=self.context.memory_stream_id,
            canonical_state_reference=self.context.canonical_state_reference,
            genesis_root_id=self.context.genesis_root_id,
            state_reference=state_reference,
            memory_reference=memory_reference,
            created_at=created_at,
            canonical_effect="NONE",
        )

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO runtime_checkpoints (
                    checkpoint_id, event_lineage_id, sequence, agent_id,
                    runtime_instance_id, memory_stream_id,
                    canonical_state_reference, genesis_root_id,
                    state_reference, memory_reference, created_at, canonical_effect,
                    checkpoint_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'NONE', ?)
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
                    checkpoint_hash,
                ),
            )

        self.append_event(
            "runtime.checkpoint_created",
            {
                "checkpoint_id": checkpoint_id,
                "checkpoint_sequence": sequence,
                "checkpoint_hash": checkpoint_hash,
                "canonical_effect": "NONE",
            },
        )
        return RuntimeCheckpoint(
            checkpoint_id,
            sequence,
            self.context,
            state_reference,
            memory_reference,
            created_at,
        )

    def _require_checkpoint_lineage_binding(self, checkpoint: RuntimeCheckpoint) -> None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT checkpoint_hash FROM runtime_checkpoints WHERE checkpoint_id = ? AND event_lineage_id = ?",
                (checkpoint.checkpoint_id, self.context.event_lineage_id),
            ).fetchone()
        if row is None:
            raise RuntimeStateError("checkpoint disappeared during recovery verification")
        checkpoint_hash = str(row["checkpoint_hash"])
        matched = any(
            event.event_type == "runtime.checkpoint_created"
            and str(event.payload.get("checkpoint_id", "")) == checkpoint.checkpoint_id
            and str(event.payload.get("checkpoint_hash", "")) == checkpoint_hash
            for event in self.events()
        )
        if not matched:
            raise RuntimeStateError("checkpoint is not bound to the verified event lineage")

    def verify(self) -> bool:
        if not super().verify():
            return False

        events = self.events()
        index = 0
        while index < len(events):
            event = events[index]
            if event.event_type == "runtime.migrating_out":
                if index + 1 >= len(events):
                    return False
                migrated_in = events[index + 1]
                if migrated_in.event_type != "runtime.migrated_in":
                    return False
                if event.payload != migrated_in.payload:
                    return False
                if event.context.runtime_instance_id != str(
                    event.payload.get("from_runtime_instance_id", "")
                ):
                    return False
                if migrated_in.context.runtime_instance_id != str(
                    event.payload.get("to_runtime_instance_id", "")
                ):
                    return False
                index += 2
                continue
            if event.event_type == "runtime.migrated_in":
                return False
            index += 1
        return True

    def recover(self) -> RecoveryState:
        recovery = super().recover()
        if recovery.checkpoint is not None:
            self._require_checkpoint_lineage_binding(recovery.checkpoint)
        return recovery

    def rollback_to_checkpoint(self, checkpoint_id: str, *, owner_approved: bool) -> RuntimeCheckpoint:
        if not self.verify():
            raise RuntimeStateError("event lineage verification failed; rollback denied")
        checkpoint = self.get_checkpoint(checkpoint_id)
        self._require_checkpoint_lineage_binding(checkpoint)
        return super().rollback_to_checkpoint(checkpoint_id, owner_approved=owner_approved)

    @staticmethod
    def _append_event_with_connection(
        connection: sqlite3.Connection,
        *,
        context: IndividualRuntimeContext,
        event_type: str,
        payload: dict[str, Any],
    ) -> RuntimeEvent:
        if not event_type.strip():
            raise RuntimeStateError("event_type must be non-empty")
        occurred_at = _now()
        previous = connection.execute(
            "SELECT sequence, event_hash FROM runtime_events WHERE event_lineage_id = ? ORDER BY sequence DESC LIMIT 1",
            (context.event_lineage_id,),
        ).fetchone()
        sequence = 1 if previous is None else int(previous["sequence"]) + 1
        previous_hash = "GENESIS" if previous is None else str(previous["event_hash"])
        body = {
            "event_lineage_id": context.event_lineage_id,
            "sequence": sequence,
            "event_type": event_type,
            "occurred_at": occurred_at,
            "context": context.to_dict(),
            "payload": payload,
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
                context.event_lineage_id,
                sequence,
                event_type,
                occurred_at,
                context.agent_id,
                context.runtime_instance_id,
                context.memory_stream_id,
                context.canonical_state_reference,
                context.genesis_root_id,
                _canonical(payload),
                previous_hash,
                event_hash,
            ),
        )
        return RuntimeEvent(
            sequence,
            event_type,
            occurred_at,
            context,
            payload,
            previous_hash,
            event_hash,
        )

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

        try:
            with self._connect() as connection:
                self._append_event_with_connection(
                    connection,
                    context=self.context,
                    event_type="runtime.migrating_out",
                    payload=reference_payload,
                )
                self._append_event_with_connection(
                    connection,
                    context=new_context,
                    event_type="runtime.migrated_in",
                    payload=reference_payload,
                )
        except sqlite3.DatabaseError as exc:
            raise RuntimeStateError("atomic migration persistence failed; migration denied") from exc

        migrated = self.__class__(self.path, new_context)
        if not migrated.verify():
            raise RuntimeStateError("post-migration lineage verification failed")
        return migrated
