"""Integrated AION runtime implementation candidate.

The runtime composes the existing bounded execution engine with the persistent
cross-session memory store. It deliberately does not self-promote to canonical
state and does not infer subjectivity or identity continuity from persistence.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from aion_astra_runtime.engine import AstraRuntime
from aion_astra_runtime.models import RunResult, TaskSpec
from aion_memory_recall.models import RecallRequest
from aion_memory_recall.store import SQLiteMemoryStore, StoredMemory


@dataclass(frozen=True, slots=True)
class RuntimeStatus:
    runtime: str = "AION_RUNTIME_IMPLEMENTATION_CANDIDATE"
    version: str = "0.1.0"
    bounded_execution: str = "ENABLED"
    live_cross_session_memory: str = "ENABLED_GOVERNED"
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
            "automatic_canonical_writeback": self.automatic_canonical_writeback,
            "public_ablation_execution": self.public_ablation_execution,
            "sexual_or_intimate_runtime": self.sexual_or_intimate_runtime,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "independent_ivv": self.independent_ivv,
            "canonical_promotion": self.canonical_promotion,
        }


class AIONRuntime:
    """Governed composition root for bounded execution and persistent recall."""

    def __init__(self, *, memory_db: str | Path, execution: AstraRuntime | None = None) -> None:
        self.memory = SQLiteMemoryStore(memory_db)
        self.execution = execution or AstraRuntime()

    @staticmethod
    def status() -> RuntimeStatus:
        return RuntimeStatus()

    def run_task(
        self,
        task: TaskSpec,
        *,
        baseline_root: Path,
        sessions_root: Path,
        kill_switch: Path | None = None,
    ) -> RunResult:
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
        namespace: str,
        user_id: str,
        agent_id: str,
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
            namespace=namespace,
            user_id=user_id,
            agent_id=agent_id,
            content=content,
            entities=entities,
            topics=topics,
            access_scope=access_scope,
            provenance_source=provenance_source,
            provenance_verified=provenance_verified,
            writeback_approved=writeback_approved,
        )

    def recall(self, request: RecallRequest, *, limit: int = 8) -> list[StoredMemory]:
        return self.memory.recall(request, limit=limit)
