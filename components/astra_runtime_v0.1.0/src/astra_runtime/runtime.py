"""Integrated Astra individual runtime implementation candidate.

Astra uses the same bounded execution and governed-memory infrastructure as
AION, while keeping an independently bound runtime context and memory stream.
This engineering separation does not establish subjectivity or phenomenal
continuity.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from aion_astra_runtime.engine import BoundedExecutionEngine
from aion_astra_runtime.models import IndividualRuntimeContext, RunResult, TaskSpec
from aion_memory_recall.models import RecallRequest
from aion_memory_recall.store import SQLiteMemoryStore, StoredMemory


@dataclass(frozen=True, slots=True)
class RuntimeStatus:
    runtime: str = "ASTRA_RUNTIME_IMPLEMENTATION_CANDIDATE"
    version: str = "0.1.0"
    bounded_execution: str = "ENABLED"
    live_cross_session_memory: str = "ENABLED_GOVERNED"
    individual_runtime_binding: str = "ENFORCED_CANDIDATE"
    automatic_canonical_writeback: str = "DISABLED"
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
            "automatic_canonical_writeback": self.automatic_canonical_writeback,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "independent_ivv": self.independent_ivv,
            "canonical_promotion": self.canonical_promotion,
        }


class RuntimeIdentityMismatch(ValueError):
    """Raised when an operation crosses the bound Astra runtime context."""


class AstraRuntime:
    """Astra-specific composition root over shared execution/memory infrastructure."""

    AGENT_ID = "ASTRA"

    def __init__(
        self,
        *,
        memory_db: str | Path,
        context: IndividualRuntimeContext,
        execution: BoundedExecutionEngine | None = None,
    ) -> None:
        context.validate()
        if context.agent_id != self.AGENT_ID:
            raise RuntimeIdentityMismatch("AstraRuntime requires context.agent_id == 'ASTRA'")
        self.context = context
        self.memory = SQLiteMemoryStore(memory_db)
        self.execution = execution or BoundedExecutionEngine()

    @staticmethod
    def status() -> RuntimeStatus:
        return RuntimeStatus()

    def _require_context(self, context: IndividualRuntimeContext) -> None:
        if context != self.context:
            raise RuntimeIdentityMismatch("task runtime_context does not match the bound Astra runtime instance")

    def run_task(
        self,
        task: TaskSpec,
        *,
        baseline_root: Path,
        sessions_root: Path,
        kill_switch: Path | None = None,
    ) -> RunResult:
        self._require_context(task.runtime_context)
        return self.execution.run(
            task,
            baseline_root=baseline_root,
            sessions_root=sessions_root,
            kill_switch=kill_switch,
        )

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
        return self.memory.write(
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
        records = self.memory.recall(request, limit=limit)
        return [record for record in records if record.namespace == self.context.memory_stream_id]
