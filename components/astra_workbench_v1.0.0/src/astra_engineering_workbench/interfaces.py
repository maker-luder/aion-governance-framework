"""Typing-only adapter interfaces."""

from __future__ import annotations

from typing import Protocol

from .models import KernelEvaluation


class GovernanceEvaluator(Protocol):
    def evaluate(
        self,
        *,
        task_id: str,
        operation: str,
        target: str,
        approved: bool,
    ) -> KernelEvaluation:
        """Evaluate one operation without allowing the caller to override denial."""


class EpisodicEventWriter(Protocol):
    def append(
        self,
        *,
        agent_id: str,
        memory_stream_id: str,
        audit_stream_id: str,
        source_type: str,
        event_kind: str,
        payload_hash: str,
    ) -> str:
        """Append one provenance event to an explicitly scoped stream."""
