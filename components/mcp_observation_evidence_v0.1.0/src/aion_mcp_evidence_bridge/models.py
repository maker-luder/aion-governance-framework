from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

RECALL_SOURCES = (
    "INTERNAL_CONTEXT",
    "CHAT_HISTORY_REFERENCE",
    "SAVED_MEMORY",
    "MCP_EXTERNAL_RETRIEVAL",
    "USER_PROMPT",
    "UNKNOWN",
)

Authority = Literal["NONE", "PROPOSE", "IMPLEMENT", "REVIEW", "APPROVE", "RELEASE"]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class EvidenceProvenance:
    source_type: str
    source_id: str
    source_timestamp: str
    retrieval_timestamp: str
    tool_name: str
    tool_call_id: str
    authority: Authority
    canonical_effect: Literal["NONE"] = "NONE"

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_type": self.source_type,
            "source_id": self.source_id,
            "source_timestamp": self.source_timestamp,
            "retrieval_timestamp": self.retrieval_timestamp,
            "tool_name": self.tool_name,
            "tool_call_id": self.tool_call_id,
            "authority": self.authority,
            "canonical_effect": self.canonical_effect,
        }


@dataclass(frozen=True, slots=True)
class EvidenceEnvelope:
    subject: str
    found: bool
    data: dict[str, Any]
    provenance: EvidenceProvenance
    mcp_role: Literal["READ_ONLY_EVIDENCE_BRIDGE"] = "READ_ONLY_EVIDENCE_BRIDGE"
    accepted_as_fact: Literal[False] = False
    canonical_effect: Literal["NONE"] = "NONE"
    memory_write: Literal["NONE"] = "NONE"
    identity_authority: Literal["NONE"] = "NONE"
    recall_source: Literal[
        "INTERNAL_CONTEXT",
        "CHAT_HISTORY_REFERENCE",
        "SAVED_MEMORY",
        "MCP_EXTERNAL_RETRIEVAL",
        "USER_PROMPT",
        "UNKNOWN",
    ] = "MCP_EXTERNAL_RETRIEVAL"

    def to_dict(self) -> dict[str, Any]:
        return {
            "mcp_role": self.mcp_role,
            "accepted_as_fact": self.accepted_as_fact,
            "canonical_effect": self.canonical_effect,
            "memory_write": self.memory_write,
            "identity_authority": self.identity_authority,
            "recall_source": self.recall_source,
            "subject": self.subject,
            "found": self.found,
            "data": self.data,
            "provenance": self.provenance.to_dict(),
        }


def make_tool_call_id() -> str:
    return f"mcp-phase1-{uuid4()}"
