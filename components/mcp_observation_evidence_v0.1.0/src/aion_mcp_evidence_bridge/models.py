from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

RETRIEVAL_MECHANISMS = (
    "INTERNAL_CONTEXT",
    "CHAT_HISTORY_REFERENCE",
    "SAVED_MEMORY",
    "MCP_EXTERNAL_RETRIEVAL",
    "USER_PROMPT",
    "UNKNOWN",
)
# Backward-compatible name for existing callers; semantics are retrieval mechanisms.
RECALL_SOURCES = RETRIEVAL_MECHANISMS

EVIDENCE_SOURCE_CLASSES = (
    "SYNTHETIC_FIXTURE",
    "PUBLIC_REPOSITORY",
    "APPROVED_NOTION_OBSERVATION_METADATA",
    "OFFICIAL_EXTERNAL_DOCUMENTATION",
    "EXPLICIT_HUMAN_OWNER_RECORD",
    "CHATGPT_TEACHER_RECORD",
    "JOINTLY_CONVERGED_RECORD",
    "COMPOSITE_GOVERNANCE_RECORD",
    "TASK_EXECUTION_PROVENANCE",
    "UNKNOWN",
)

Authority = Literal[
    "NONE",
    "PROPOSE",
    "PROPOSE_REVIEW",
    "IMPLEMENT",
    "REVIEW",
    "APPROVE",
    "APPROVE_SCOPE",
    "RELEASE",
]
RetrievalMechanism = Literal[
    "INTERNAL_CONTEXT",
    "CHAT_HISTORY_REFERENCE",
    "SAVED_MEMORY",
    "MCP_EXTERNAL_RETRIEVAL",
    "USER_PROMPT",
    "UNKNOWN",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class EvidenceProvenance:
    evidence_source_class: str
    source_id: str
    source_timestamp: str
    retrieval_timestamp: str
    tool_name: str
    tool_call_id: str
    authority: Authority
    retrieval_mechanism: RetrievalMechanism = "MCP_EXTERNAL_RETRIEVAL"
    canonical_effect: Literal["NONE"] = "NONE"

    def to_dict(self) -> dict[str, Any]:
        return {
            # Compatibility alias only. The explicit dimensions are
            # evidence_source_class and retrieval_mechanism.
            "source_type": self.evidence_source_class,
            "evidence_source_class": self.evidence_source_class,
            "retrieval_mechanism": self.retrieval_mechanism,
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
    retrieval_mechanism: RetrievalMechanism = "MCP_EXTERNAL_RETRIEVAL"

    def to_dict(self) -> dict[str, Any]:
        return {
            "mcp_role": self.mcp_role,
            "accepted_as_fact": self.accepted_as_fact,
            "canonical_effect": self.canonical_effect,
            "memory_write": self.memory_write,
            "identity_authority": self.identity_authority,
            "retrieval_mechanism": self.retrieval_mechanism,
            # Compatibility alias only.
            "recall_source": self.retrieval_mechanism,
            "subject": self.subject,
            "found": self.found,
            "data": self.data,
            "provenance": self.provenance.to_dict(),
        }


def make_tool_call_id() -> str:
    return f"mcp-phase1-{uuid4()}"
