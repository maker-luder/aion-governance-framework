from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any

from .enums import ApprovalStatus, CanonicalEffect, ForkStatus, QAStatus, SubjectivityStatus
from .errors import ValidationError
from .hashing import hash_object, valid_sha256


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _require(value: str, name: str) -> None:
    if not value.strip():
        raise ValidationError(f"{name} must be non-empty")


def _hash_or_unknown(value: str, name: str) -> None:
    if value != "UNKNOWN" and not valid_sha256(value):
        raise ValidationError(f"{name} must be SHA-256 or UNKNOWN")


@dataclass(frozen=True, slots=True)
class SourceProvenance:
    document_type: str
    source: str
    canonical_effect: CanonicalEffect = CanonicalEffect.NONE
    project_identity_effect: str = "NONE"
    engineering_status: str = "PARTIALLY_ADOPTED_AS_REQUIREMENT_CANDIDATES"


@dataclass(frozen=True, slots=True)
class ProjectIdentityRecord:
    project_id: str
    canonical_name: str = "AION／Astra"
    aliases: tuple[str, ...] = ("AION", "Astra")
    project_type: str = "SPECIALIZED_AI_SYSTEM_AND_RESEARCH_LINEAGE"
    research_lineage_description: str = "User and ChatGPT long-term research with local candidate engineering"
    governance_root_id: str = "AION-ASTRA-GOVERNANCE-ROOT-001"
    canonical_manifest_id: str = "UNKNOWN"
    status: str = "QA_HOLD"
    subjectivity_status: SubjectivityStatus = SubjectivityStatus.NOT_ESTABLISHED
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)
    source_provenance: SourceProvenance = field(
        default_factory=lambda: SourceProvenance(
            "EXTERNAL_CONCEPTUAL_ARCHITECTURE_PROPOSAL",
            "外部 AI 助手依本輪討論產生的架構提案",
        )
    )
    notes: str = "Candidate record; not canonical approval."

    def __post_init__(self) -> None:
        _require(self.project_id, "project_id")
        if self.canonical_name != "AION／Astra":
            raise ValidationError("canonical_name must remain AION／Astra")
        if self.subjectivity_status is not SubjectivityStatus.NOT_ESTABLISHED:
            raise ValidationError("candidate identity subjectivity must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class CapabilityArtifactRecord:
    artifact_id: str
    capability_type: str
    display_name: str
    revision: str
    upstream_source: str = "UNKNOWN"
    upstream_developer: str = "UNKNOWN"
    upstream_license: str = "NOT_VERIFIED"
    model_family: str = "UNKNOWN"
    base_model: str = "UNKNOWN"
    modification_type: str = "UNKNOWN"
    file_format: str = "UNKNOWN"
    quantization: str = "UNKNOWN"
    local_path: str | None = None
    sha256: str = "UNKNOWN"
    manifest_id: str = "UNKNOWN"
    status: str = "EXPERIMENTAL"
    qa_status: QAStatus = QAStatus.QA_HOLD
    permissions: tuple[str, ...] = ()
    canonical_effect: CanonicalEffect = CanonicalEffect.NONE
    notes: str = ""

    def __post_init__(self) -> None:
        _require(self.artifact_id, "artifact_id")
        _hash_or_unknown(self.sha256, "sha256")
        if self.canonical_effect is not CanonicalEffect.NONE:
            raise ValidationError("candidate artifacts have canonical_effect NONE")
        if self.local_path and (PathLikeGuard.unsafe(self.local_path)):
            raise ValidationError("local_path must be relative and traversal-free")


class PathLikeGuard:
    @staticmethod
    def unsafe(value: str) -> bool:
        normalized = value.replace("\\", "/")
        return normalized.startswith("/") or ":" in normalized or ".." in normalized.split("/")


@dataclass(frozen=True, slots=True)
class RuntimeManifest:
    runtime_id: str
    runtime_type: str
    runtime_version: str = "UNKNOWN"
    execution_location: str = "LOCAL"
    network_mode: str = "OFFLINE"
    model_reference: str = "UNKNOWN"
    allowed_endpoints: tuple[str, ...] = ()
    timeout: int = 30
    sandbox_status: str = "NOT_IMPLEMENTED"
    tool_permissions: tuple[str, ...] = ()
    sha256_or_config_hash: str = "UNKNOWN"
    status: str = "CANDIDATE"
    notes: str = ""

    def __post_init__(self) -> None:
        _require(self.runtime_id, "runtime_id")
        _hash_or_unknown(self.sha256_or_config_hash, "sha256_or_config_hash")
        if self.timeout <= 0:
            raise ValidationError("timeout must be positive")
        for endpoint in self.allowed_endpoints:
            if not any(
                endpoint.startswith(prefix) for prefix in ("http://localhost", "http://127.0.0.1", "http://[::1]")
            ):
                raise ValidationError("runtime endpoints must be loopback only")


@dataclass(frozen=True, slots=True)
class SystemStateRecord:
    state_id: str
    project_id: str
    previous_state_id: str | None
    sequence_number: int
    state_type: str
    previous_state_hash: str
    canonical_manifest_hash: str
    governance_policy_hash: str
    capability_manifest_hash: str
    model_manifest_hash: str
    runtime_manifest_hash: str
    memory_manifest_hash: str = "UNKNOWN"
    evidence_manifest_hash: str = "UNKNOWN"
    artifact_ids: tuple[str, ...] = ()
    approval_status: ApprovalStatus = ApprovalStatus.NOT_REQUESTED
    qa_status: QAStatus = QAStatus.QA_HOLD
    canonical_effect: CanonicalEffect = CanonicalEffect.NONE
    created_at: str = field(default_factory=now_iso)
    created_by: str = "ENGINEERING_AGENT"
    notes: str = ""
    state_hash: str = ""

    def hash_payload(self) -> dict[str, Any]:
        return {
            "previous_state_hash": self.previous_state_hash,
            "project_id": self.project_id,
            "canonical_manifest_hash": self.canonical_manifest_hash,
            "governance_policy_hash": self.governance_policy_hash,
            "capability_manifest_hash": self.capability_manifest_hash,
            "model_manifest_hash": self.model_manifest_hash,
            "runtime_manifest_hash": self.runtime_manifest_hash,
            "memory_manifest_hash": self.memory_manifest_hash,
            "evidence_manifest_hash": self.evidence_manifest_hash,
            "artifact_ids": self.artifact_ids,
            "sequence_number": self.sequence_number,
        }

    def expected_hash(self) -> str:
        return hash_object(self.hash_payload())

    def __post_init__(self) -> None:
        _require(self.state_id, "state_id")
        if self.sequence_number < 0:
            raise ValidationError("sequence_number cannot be negative")
        if self.sequence_number == 0 and (self.previous_state_id is not None or self.previous_state_hash != "GENESIS"):
            raise ValidationError("genesis must use previous_state_id null and previous_state_hash GENESIS")
        if self.sequence_number > 0 and (not self.previous_state_id or not valid_sha256(self.previous_state_hash)):
            raise ValidationError("non-genesis state requires parent id and SHA-256")
        for name in (
            "canonical_manifest_hash",
            "governance_policy_hash",
            "capability_manifest_hash",
            "model_manifest_hash",
            "runtime_manifest_hash",
            "memory_manifest_hash",
            "evidence_manifest_hash",
        ):
            _hash_or_unknown(getattr(self, name), name)
        if self.state_hash and self.state_hash != self.expected_hash():
            raise ValidationError("state_hash does not match deterministic payload")

    def sealed(self) -> SystemStateRecord:
        values = asdict(self)
        values["state_hash"] = self.expected_hash()
        return SystemStateRecord(**values)


@dataclass(frozen=True, slots=True)
class ResearchForkRecord:
    fork_id: str
    parent_state_id: str
    parent_state_hash: str
    fork_type: str
    purpose: str
    hypothesis: str
    scope: tuple[str, ...]
    identity_inheritance: str = "DENIED"
    canonical_writeback: str = "DENIED"
    memory_writeback: str = "DENIED"
    tool_privilege_inheritance: str = "DENIED"
    relationship_authority_inheritance: str = "DENIED"
    allowed_operations: tuple[str, ...] = ()
    prohibited_operations: tuple[str, ...] = ("CANONICAL_WRITEBACK", "PARENT_OVERWRITE", "PRIVILEGE_ESCALATION")
    artifact_ids: tuple[str, ...] = ()
    status: ForkStatus = ForkStatus.QA_HOLD
    qa_status: QAStatus = QAStatus.QA_HOLD
    created_at: str = field(default_factory=now_iso)
    closed_at: str | None = None
    disposition: str = "ACTIVE"
    merge_candidate_id: str | None = None
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.fork_id.startswith("RESEARCH-FORK-"):
            raise ValidationError("fork_id must start RESEARCH-FORK-")
        if not valid_sha256(self.parent_state_hash):
            raise ValidationError("parent_state_hash must be SHA-256")
        denied = (
            self.identity_inheritance,
            self.canonical_writeback,
            self.memory_writeback,
            self.tool_privilege_inheritance,
            self.relationship_authority_inheritance,
        )
        if any(value != "DENIED" for value in denied):
            raise ValidationError("research fork inheritances and writeback must be DENIED")


@dataclass(frozen=True, slots=True)
class LineageEvent:
    event_id: str
    event_type: str
    previous_event_hash: str
    project_id: str
    state_id: str | None
    fork_id: str | None
    payload_hash: str
    actor_role: str
    occurred_at: str = field(default_factory=now_iso)
    approval_reference: str | None = None
    source_provenance: str = "LOCAL_ENGINEERING_EVENT"
    notes: str = ""
    event_hash: str = ""

    def expected_hash(self) -> str:
        return hash_object(
            {
                "event_id": self.event_id,
                "event_type": self.event_type,
                "previous_event_hash": self.previous_event_hash,
                "project_id": self.project_id,
                "state_id": self.state_id,
                "fork_id": self.fork_id,
                "payload_hash": self.payload_hash,
                "actor_role": self.actor_role,
                "occurred_at": self.occurred_at,
                "approval_reference": self.approval_reference,
                "source_provenance": self.source_provenance,
            }
        )

    def __post_init__(self) -> None:
        if self.event_type in {"CANONICAL_UPDATED", "MERGE_APPROVED"} and not self.approval_reference:
            raise ValidationError("human approval reference is required for this event type")
        _hash_or_unknown(self.payload_hash, "payload_hash")
        if self.event_hash and self.event_hash != self.expected_hash():
            raise ValidationError("event_hash does not match deterministic payload")


@dataclass(frozen=True, slots=True)
class AnalysisChannel:
    channel_id: str
    findings: tuple[str, ...]
    interpretation: str
    uncertainty: str
    supporting_evidence: tuple[str, ...]
    contradictory_evidence: tuple[str, ...]
    generated_by: str
    model_or_method_reference: str
    confidence_optional: float | None = None


@dataclass(frozen=True, slots=True)
class PerspectiveEventRecord:
    event_id: str
    shared_evidence: tuple[str, ...]
    evidence_hash: str
    analysis_channels: tuple[AnalysisChannel, ...]
    agreements: tuple[str, ...]
    disagreements: tuple[str, ...]
    unresolved_questions: tuple[str, ...]
    merged_summary_optional: str | None = None
    merge_status: str = "UNRESOLVED"
    source_provenance: str = "RESEARCH_ANALYSIS"
    canonical_effect: CanonicalEffect = CanonicalEffect.NONE
    created_at: str = field(default_factory=now_iso)

    def __post_init__(self) -> None:
        if len(self.analysis_channels) < 2:
            raise ValidationError("perspective event requires at least two channels")
        if (self.disagreements or self.unresolved_questions) and self.merge_status == "RESOLVED":
            raise ValidationError("unresolved disagreements cannot be marked RESOLVED")
        if self.canonical_effect is not CanonicalEffect.NONE:
            raise ValidationError("perspective records cannot directly affect canonical")
