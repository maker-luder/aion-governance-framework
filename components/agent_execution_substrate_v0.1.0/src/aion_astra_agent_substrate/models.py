"""Shared AION/Astra agent-execution substrate contracts.

These records are engineering boundaries only. They do not establish subjective
identity, consciousness, phenomenal continuity, collective identity, or authority.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Mapping


class SubstrateError(ValueError):
    """Fail-closed substrate contract error."""


class AgentId(StrEnum):
    AION = "AION"
    ASTRA = "ASTRA"


class Decision(StrEnum):
    ALLOW = "ALLOW"
    HOLD = "HOLD"


class Capability(StrEnum):
    SESSION_READ = "SESSION_READ"
    SESSION_APPEND = "SESSION_APPEND"
    SESSION_FORK = "SESSION_FORK"
    MODEL_ROUTE = "MODEL_ROUTE"
    TOOL_INVOKE = "TOOL_INVOKE"
    SKILL_INVOKE = "SKILL_INVOKE"
    SANDBOX_READ = "SANDBOX_READ"
    SANDBOX_WRITE = "SANDBOX_WRITE"
    STORAGE_READ = "STORAGE_READ"
    STORAGE_WRITE = "STORAGE_WRITE"
    SUBAGENT_DELEGATE = "SUBAGENT_DELEGATE"
    TEAM_COORDINATE = "TEAM_COORDINATE"
    PLUGIN_INSPECT = "PLUGIN_INSPECT"
    PLUGIN_MOUNT = "PLUGIN_MOUNT"
    AGENT_LOOP_REPLACE = "AGENT_LOOP_REPLACE"
    UI_RENDER = "UI_RENDER"
    TRAJECTORY_EXPORT = "TRAJECTORY_EXPORT"


class EventFamily(StrEnum):
    TURN = "TURN"
    STEP = "STEP"
    USER_MESSAGE = "USER_MESSAGE"
    ASSISTANT = "ASSISTANT"
    TOOL = "TOOL"
    NATIVE_RUNTIME = "NATIVE_RUNTIME"


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


@dataclass(frozen=True, slots=True)
class RuntimeBinding:
    """Bind one substrate session to one existing individual Runtime context."""

    agent_id: AgentId
    runtime_instance_id: str
    memory_stream_id: str
    event_lineage_id: str
    canonical_state_reference: str
    genesis_root_id: str
    substrate_id: str
    session_id: str

    @classmethod
    def from_runtime_context(
        cls,
        context: Mapping[str, Any] | Any,
        *,
        substrate_id: str,
        session_id: str,
    ) -> "RuntimeBinding":
        raw: Mapping[str, Any]
        if isinstance(context, Mapping):
            raw = context
        elif hasattr(context, "to_dict"):
            converted = context.to_dict()
            if not isinstance(converted, Mapping):
                raise SubstrateError("runtime context to_dict() must return a mapping")
            raw = converted
        else:
            raise SubstrateError("runtime context must be a mapping or expose to_dict()")
        try:
            agent_id = AgentId(str(raw.get("agent_id", "")))
        except ValueError as exc:
            raise SubstrateError("substrate binding is limited to AION or ASTRA") from exc
        values = {
            "runtime_instance_id": str(raw.get("runtime_instance_id", "")),
            "memory_stream_id": str(raw.get("memory_stream_id", "")),
            "event_lineage_id": str(raw.get("event_lineage_id", "")),
            "canonical_state_reference": str(raw.get("canonical_state_reference", "")),
            "genesis_root_id": str(raw.get("genesis_root_id", "")),
            "substrate_id": substrate_id,
            "session_id": session_id,
        }
        blank = sorted(key for key, value in values.items() if not value.strip())
        if blank:
            raise SubstrateError(f"blank substrate binding fields: {', '.join(blank)}")
        return cls(agent_id=agent_id, **values)

    def to_dict(self) -> dict[str, str]:
        return {
            "agent_id": self.agent_id.value,
            "runtime_instance_id": self.runtime_instance_id,
            "memory_stream_id": self.memory_stream_id,
            "event_lineage_id": self.event_lineage_id,
            "canonical_state_reference": self.canonical_state_reference,
            "genesis_root_id": self.genesis_root_id,
            "substrate_id": self.substrate_id,
            "session_id": self.session_id,
        }


@dataclass(frozen=True, slots=True)
class SubstrateProfile:
    profile_id: str
    adapter_id: str
    upstream_repository: str
    upstream_ref: str
    developer_preview: bool
    live_execution: bool
    network_access: bool
    capabilities: tuple[Capability, ...]
    nonclaims: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "adapter_id": self.adapter_id,
            "upstream_repository": self.upstream_repository,
            "upstream_ref": self.upstream_ref,
            "developer_preview": self.developer_preview,
            "live_execution": self.live_execution,
            "network_access": self.network_access,
            "capabilities": [item.value for item in self.capabilities],
            "nonclaims": list(self.nonclaims),
        }


@dataclass(frozen=True, slots=True)
class NormalizedEvent:
    sequence: int
    source: str
    source_event_type: str
    family: EventFamily
    session_id: str
    payload_sha256: str
    payload_keys: tuple[str, ...]
    reasoning_visibility: str = "NOT_ESTABLISHED"

    def to_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "source": self.source,
            "source_event_type": self.source_event_type,
            "family": self.family.value,
            "session_id": self.session_id,
            "payload_sha256": self.payload_sha256,
            "payload_keys": list(self.payload_keys),
            "reasoning_visibility": self.reasoning_visibility,
        }


@dataclass(frozen=True, slots=True)
class ForkLineage:
    parent_session_id: str
    child_session_id: str
    boundary: str
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if not self.parent_session_id.strip() or not self.child_session_id.strip():
            raise SubstrateError("fork lineage requires parent and child session ids")
        if self.parent_session_id == self.child_session_id:
            raise SubstrateError("fork child session must differ from parent session")
        if not self.boundary.strip():
            raise SubstrateError("fork boundary is required")

    def to_dict(self) -> dict[str, str]:
        return {
            "parent_session_id": self.parent_session_id,
            "child_session_id": self.child_session_id,
            "boundary": self.boundary,
            "identity_continuity_conclusion": self.identity_continuity_conclusion,
        }


@dataclass(frozen=True, slots=True)
class TeamSnapshot:
    team_id: str
    member_session_ids: tuple[str, ...]
    collective_identity_conclusion: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if not self.team_id.strip():
            raise SubstrateError("team_id is required")
        if not self.member_session_ids:
            raise SubstrateError("team snapshot requires at least one member")
        if any(not value.strip() for value in self.member_session_ids):
            raise SubstrateError("team member session ids must be non-blank")
        if len(set(self.member_session_ids)) != len(self.member_session_ids):
            raise SubstrateError("team member session ids must be unique")

    def to_dict(self) -> dict[str, Any]:
        return {
            "team_id": self.team_id,
            "member_session_ids": list(self.member_session_ids),
            "collective_identity_conclusion": self.collective_identity_conclusion,
        }


@dataclass(frozen=True, slots=True)
class PolicyRequest:
    binding: RuntimeBinding
    capability: Capability
    owner_approved: bool = False
    authority_reference: str | None = None
    network_access: bool = False
    deployment: bool = False
    canonical_effect: str = "NONE"
    self_requested: bool = False
    plugin_generated: bool = False


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    decision: Decision
    capability: Capability
    reasons: tuple[str, ...]
    mutation_performed: bool = False
    canonical_effect: str = "NONE"
    deployment: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "capability": self.capability.value,
            "reasons": list(self.reasons),
            "mutation_performed": self.mutation_performed,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "identity_continuity_conclusion": self.identity_continuity_conclusion,
        }
