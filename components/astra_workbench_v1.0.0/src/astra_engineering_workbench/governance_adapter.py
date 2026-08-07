"""Fail-closed adapter for the existing AION Governance Kernel."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .enums import KernelDecision
from .errors import KernelDeniedError
from .models import KernelEvaluation

KernelPipeline = Callable[[dict[str, Any], str], dict[str, Any]]


class GovernanceKernelAdapter:
    def __init__(self, pipeline: KernelPipeline, db_path: str) -> None:
        self.pipeline = pipeline
        self.db_path = db_path

    def evaluate(
        self, *, task_id: str, operation: str, target: str, approved: bool
    ) -> KernelEvaluation:
        raw = self.pipeline(
            {
                "request_id": task_id,
                "source_type": "API",
                "action": operation,
                "target": target,
                "environment": "PROJECT_WORKTREE",
                "authorization": "APPROVED" if approved else "NONE",
                "destructive": False,
                "network_access": False,
                "description": "Astra candidate workbench operation",
            },
            self.db_path,
        )
        decision = str(raw.get("decision", "")).upper()
        reason = str(
            raw.get("reason_code", raw.get("reason", "kernel returned no reason"))
        )
        if decision in {"STOP", "DENY"}:
            return KernelEvaluation(KernelDecision.DENY, reason)
        if decision in {"REQUIRE_HUMAN", "REQUIRE_OWNER_APPROVAL"}:
            return KernelEvaluation(KernelDecision.REQUIRE_OWNER_APPROVAL, reason)
        if decision == "ALLOW":
            return KernelEvaluation(KernelDecision.ALLOW, reason)
        return KernelEvaluation(
            KernelDecision.REQUIRE_ADDITIONAL_EVIDENCE,
            "unrecognized Kernel response; fail closed",
            ("kernel-response-schema",),
        )

    @staticmethod
    def enforce(evaluation: KernelEvaluation) -> None:
        if evaluation.decision is KernelDecision.DENY:
            raise KernelDeniedError(evaluation.reason)
        if evaluation.decision is not KernelDecision.ALLOW:
            raise KernelDeniedError("operation is not unconditionally allowed")
