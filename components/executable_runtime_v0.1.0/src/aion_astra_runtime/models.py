"""Immutable runtime records and strict JSON task parsing."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .errors import PolicyDenied


class RunStatus(StrEnum):
    RECEIVED = "RECEIVED"
    RUNNING = "RUNNING"
    PASS_PENDING_OWNER_REVIEW = "PASS_PENDING_OWNER_REVIEW"
    HOLD = "HOLD"


class NetworkPolicy(StrEnum):
    OFFLINE = "OFFLINE"
    LOOPBACK_ONLY = "LOOPBACK_ONLY"


@dataclass(frozen=True, slots=True)
class IndividualRuntimeContext:
    """Required identity/lineage binding for one concrete individual runtime instance.

    This record is an engineering ownership boundary. It does not establish
    subjective identity, consciousness, or phenomenal continuity.
    """

    agent_id: str
    runtime_instance_id: str
    memory_stream_id: str
    event_lineage_id: str
    canonical_state_reference: str
    genesis_root_id: str

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "IndividualRuntimeContext":
        context = cls(
            agent_id=str(raw.get("agent_id", "")),
            runtime_instance_id=str(raw.get("runtime_instance_id", "")),
            memory_stream_id=str(raw.get("memory_stream_id", "")),
            event_lineage_id=str(raw.get("event_lineage_id", "")),
            canonical_state_reference=str(raw.get("canonical_state_reference", "")),
            genesis_root_id=str(raw.get("genesis_root_id", "")),
        )
        context.validate()
        return context

    def validate(self) -> None:
        values = {
            "agent_id": self.agent_id,
            "runtime_instance_id": self.runtime_instance_id,
            "memory_stream_id": self.memory_stream_id,
            "event_lineage_id": self.event_lineage_id,
            "canonical_state_reference": self.canonical_state_reference,
            "genesis_root_id": self.genesis_root_id,
        }
        blank = [name for name, value in values.items() if not value.strip()]
        if blank:
            raise PolicyDenied(f"blank individual runtime context fields: {', '.join(sorted(blank))}")

    def to_dict(self) -> dict[str, str]:
        return {
            "agent_id": self.agent_id,
            "runtime_instance_id": self.runtime_instance_id,
            "memory_stream_id": self.memory_stream_id,
            "event_lineage_id": self.event_lineage_id,
            "canonical_state_reference": self.canonical_state_reference,
            "genesis_root_id": self.genesis_root_id,
        }


@dataclass(frozen=True, slots=True)
class TaskSpec:
    task_id: str
    objective: str
    profile: str
    input_paths: tuple[str, ...]
    output_path: str
    owner_approved: bool
    approved_by: str
    runtime_context: IndividualRuntimeContext
    max_steps: int = 12
    network_policy: NetworkPolicy = NetworkPolicy.OFFLINE
    canonical_effect: str = "NONE"

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "TaskSpec":
        inputs = raw.get("input_paths")
        if not isinstance(inputs, list) or not inputs or not all(
            isinstance(item, str) and item.strip() for item in inputs
        ):
            raise PolicyDenied("input_paths must be a non-empty string array")
        raw_context = raw.get("runtime_context")
        if not isinstance(raw_context, dict):
            raise PolicyDenied("runtime_context is required and must be an object")
        try:
            network_policy = NetworkPolicy(str(raw.get("network_policy", "OFFLINE")))
        except ValueError as exc:
            raise PolicyDenied("network_policy is unsupported") from exc
        task = cls(
            task_id=str(raw.get("task_id", "")),
            objective=str(raw.get("objective", "")),
            profile=str(raw.get("profile", "")),
            input_paths=tuple(inputs),
            output_path=str(raw.get("output_path", "")),
            owner_approved=raw.get("owner_approved") is True,
            approved_by=str(raw.get("approved_by", "")),
            runtime_context=IndividualRuntimeContext.from_dict(raw_context),
            max_steps=int(raw.get("max_steps", 12)),
            network_policy=network_policy,
            canonical_effect=str(raw.get("canonical_effect", "NONE")),
        )
        task.validate()
        return task

    def validate(self) -> None:
        if not self.task_id or any(char in self.task_id for char in '\\/:*?"<>|'):
            raise PolicyDenied("task_id is blank or unsafe")
        if not self.objective.strip():
            raise PolicyDenied("objective is required")
        if self.profile != "INVENTORY_SUMMARIZE":
            raise PolicyDenied("only INVENTORY_SUMMARIZE is admitted in runtime v0.1.0")
        if not self.owner_approved or not self.approved_by.strip():
            raise PolicyDenied("explicit Owner approval is required")
        self.runtime_context.validate()
        if not 5 <= self.max_steps <= 64:
            raise PolicyDenied("max_steps must be between 5 and 64")
        if self.canonical_effect != "NONE":
            raise PolicyDenied("canonical effects are not admitted")


@dataclass(frozen=True, slots=True)
class Action:
    tool: str
    arguments: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Observation:
    tool: str
    status: str
    payload: dict[str, Any]


@dataclass(frozen=True, slots=True)
class RunResult:
    task_id: str
    runtime_context: IndividualRuntimeContext
    status: RunStatus
    steps_executed: int
    candidate_root: str
    output_root: str
    output_relative_path: str
    output_sha256: str | None
    audit_path: str
    audit_chain_valid: bool
    baseline_unchanged: bool
    canonical_effect: str = "NONE"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    deployment: bool = False
    failure_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "runtime_context": self.runtime_context.to_dict(),
            "status": self.status.value,
            "steps_executed": self.steps_executed,
            "candidate_root": self.candidate_root,
            "output_root": self.output_root,
            "output_relative_path": self.output_relative_path,
            "output_sha256": self.output_sha256,
            "audit_path": self.audit_path,
            "audit_chain_valid": self.audit_chain_valid,
            "baseline_unchanged": self.baseline_unchanged,
            "canonical_effect": self.canonical_effect,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "deployment": self.deployment,
            "failure_reason": self.failure_reason,
        }
