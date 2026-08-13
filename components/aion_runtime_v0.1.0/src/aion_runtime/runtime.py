"""Integrated AION individual runtime implementation candidate.

The runtime binds shared bounded execution, governed persistent memory, and an
append-only individual event lineage to one explicit AION runtime instance.
Persistence and execution do not establish subjectivity, consciousness, or
phenomenal continuity.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from aion_astra_runtime.engine import BoundedExecutionEngine
from aion_astra_runtime.models import IndividualRuntimeContext, RunResult, TaskSpec
from aion_memory_recall.models import RecallRequest
from aion_memory_recall.store import SQLiteMemoryStore, StoredMemory
from individual_runtime_state import (
    EnvironmentEvidence,
    IndividualRuntimeStateStore,
    MigrationSummary,
    RecoveryState,
    RuntimeCheckpoint,
)


@dataclass(frozen=True, slots=True)
class RuntimeStatus:
    runtime: str = "AION_RUNTIME_IMPLEMENTATION_CANDIDATE"
    version: str = "0.1.0"
    bounded_execution: str = "ENABLED"
    live_cross_session_memory: str = "ENABLED_GOVERNED"
    individual_runtime_binding: str = "ENFORCED_CANDIDATE"
    individual_event_lineage: str = "ENABLED_GOVERNED_CANDIDATE"
    checkpoint_recovery: str = "ENABLED_OWNER_GOVERNED_CANDIDATE"
    migration_evidence_reuse: str = "ENABLED_CONTENT_ADDRESSED_CANDIDATE"
    automatic_canonical_writeback: str = "DISABLED"
    public_ablation_execution: str = "DISABLED"
    sexual_or_intimate_runtime: str = "NOT_AUTHORIZED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    independent_ivv: str = "NOT_ACHIEVED"
    canonical_promotion: str = "PENDING_OWNER_REVIEW"

    def to_dict(self) -> dict[str, str]:
        return {
            "runtime": self.runtime,
            "version": self.version,
            "bounded_execution": self.bounded_execution,
            "live_cross_session_memory": self.live_cross_session_memory,
            "individual_runtime_binding": self.individual_runtime_binding,
            "individual_event_lineage": self.individual_event_lineage,
            "checkpoint_recovery": self.checkpoint_recovery,
            "migration_evidence_reuse": self.migration_evidence_reuse,
            "automatic_canonical_writeback": self.automatic_canonical_writeback,
            "public_ablation_execution": self.public_ablation_execution,
            "sexual_or_intimate_runtime": self.sexual_or_intimate_runtime,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "independent_ivv": self.independent_ivv,
            "canonical_promotion": self.canonical_promotion,
        }


class RuntimeIdentityMismatch(ValueError):
    """Raised when an operation attempts to cross the bound individual runtime."""


class AIONRuntime:
    """AION-specific composition root over shared governed infrastructure."""

    AGENT_ID = "AION"

    def __init__(
        self,
        *,
        memory_db: str | Path,
        context: IndividualRuntimeContext,
        state_db: str | Path | None = None,
        execution: BoundedExecutionEngine | None = None,
    ) -> None:
        context.validate()
        if context.agent_id != self.AGENT_ID:
            raise RuntimeIdentityMismatch("AIONRuntime requires context.agent_id == 'AION'")
        self.context = context
        self.memory = SQLiteMemoryStore(memory_db)
        self.state = IndividualRuntimeStateStore(state_db or f"{memory_db}.state.sqlite3", context)
        self.execution = execution or BoundedExecutionEngine()

    @staticmethod
    def status() -> RuntimeStatus:
        return RuntimeStatus()

    def _require_context(self, context: IndividualRuntimeContext) -> None:
        if context != self.context:
            raise RuntimeIdentityMismatch("task runtime_context does not match the bound AION runtime instance")

    def record_start(self, *, reason: str = "operator_start") -> None:
        self.state.append_event("runtime.started", {"reason": reason, "canonical_effect": "NONE"})

    def record_stop(self, *, reason: str = "operator_stop") -> None:
        self.state.append_event("runtime.stopped", {"reason": reason, "canonical_effect": "NONE"})

    def run_task(
        self,
        task: TaskSpec,
        *,
        baseline_root: Path,
        sessions_root: Path,
        kill_switch: Path | None = None,
    ) -> RunResult:
        self._require_context(task.runtime_context)
        self.state.append_event("task.started", {"task_id": task.task_id})
        try:
            result = self.execution.run(
                task,
                baseline_root=baseline_root,
                sessions_root=sessions_root,
                kill_switch=kill_switch,
            )
        except Exception as exc:
            self.state.append_event(
                "task.failed",
                {
                    "task_id": task.task_id,
                    "error_type": type(exc).__name__,
                    "reason": str(exc),
                    "canonical_effect": "NONE",
                },
            )
            raise
        self.state.append_event(
            "task.completed",
            {"task_id": task.task_id, "status": result.status.value, "canonical_effect": result.canonical_effect},
        )
        return result

    def remember(
        self,
        *,
        memory_id: str,
        user_id: str,
        content: str,
        provenance_source: str,
        provenance_verified: bool,
        writeback_approved: bool,
        entities: Iterable[str] = (),
        topics: Iterable[str] = (),
        access_scope: Iterable[str] = (),
    ) -> StoredMemory:
        stored = self.memory.write(
            memory_id=memory_id,
            namespace=self.context.memory_stream_id,
            user_id=user_id,
            agent_id=self.context.agent_id,
            content=content,
            entities=entities,
            topics=topics,
            access_scope=access_scope,
            provenance_source=provenance_source,
            provenance_verified=provenance_verified,
            writeback_approved=writeback_approved,
        )
        self.state.append_event(
            "memory.written",
            {"memory_id": memory_id, "provenance_source": provenance_source, "canonical_effect": "NONE"},
        )
        return stored

    def recall(
        self,
        *,
        user_id: str,
        requester_scopes: Iterable[str],
        entity_cues: Iterable[str] = (),
        topic_cues: Iterable[str] = (),
        limit: int = 8,
    ) -> list[StoredMemory]:
        request = RecallRequest(
            user_id=user_id,
            agent_id=self.context.agent_id,
            requester_scopes=frozenset(requester_scopes),
            entity_cues=frozenset(entity_cues),
            topic_cues=frozenset(topic_cues),
        )
        records = [
            record
            for record in self.memory.recall(
                request,
                limit=limit,
                namespace=self.context.memory_stream_id,
            )
        ]
        self.state.append_event("memory.recalled", {"result_count": len(records)})
        return records

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
        return self.state.register_environment_evidence(
            device_id=device_id,
            hardware_profile_hash=hardware_profile_hash,
            runtime_environment_hash=runtime_environment_hash,
            policy_config_hash=policy_config_hash,
            verification_reference=verification_reference,
            verification_status=verification_status,
        )

    def migration_summary(self) -> list[MigrationSummary]:
        return self.state.migration_summary()

    def checkpoint(
        self,
        *,
        checkpoint_id: str,
        state_reference: str,
        memory_reference: str,
        owner_approved: bool,
    ) -> RuntimeCheckpoint:
        return self.state.checkpoint(
            checkpoint_id=checkpoint_id,
            state_reference=state_reference,
            memory_reference=memory_reference,
            owner_approved=owner_approved,
        )

    def recover(self) -> RecoveryState:
        recovery = self.state.recover()
        self.state.append_event(
            "runtime.recovered",
            {"from_sequence": recovery.last_sequence, "checkpoint_id": recovery.checkpoint.checkpoint_id if recovery.checkpoint else None},
        )
        return recovery

    def rollback_to_checkpoint(self, checkpoint_id: str, *, owner_approved: bool) -> RuntimeCheckpoint:
        return self.state.rollback_to_checkpoint(checkpoint_id, owner_approved=owner_approved)

    def migrate_runtime(
        self,
        new_context: IndividualRuntimeContext,
        *,
        owner_approved: bool,
        source_evidence_id: str,
        target_evidence_id: str,
    ) -> "AIONRuntime":
        if new_context.agent_id != self.AGENT_ID:
            raise RuntimeIdentityMismatch("AION migration must remain bound to AION")
        migrated_state = self.state.migrate_instance(
            new_context,
            owner_approved=owner_approved,
            source_evidence_id=source_evidence_id,
            target_evidence_id=target_evidence_id,
        )
        return AIONRuntime(
            memory_db=self.memory.path,
            context=new_context,
            state_db=migrated_state.path,
            execution=self.execution,
        )
