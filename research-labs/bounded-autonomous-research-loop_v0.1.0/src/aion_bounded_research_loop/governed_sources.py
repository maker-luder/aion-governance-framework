from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum

from .models import canonical_hash


class RegistryStatus(str, Enum):
    DECLARED_METADATA_ONLY = "DECLARED_METADATA_ONLY"
    CANDIDATE = "CANDIDATE"
    ACTIVE_REFERENCE = "ACTIVE_REFERENCE"
    HOLD = "HOLD"
    RETIRED = "RETIRED"


class VerificationPolicy(str, Enum):
    PROVENANCE_REQUIRED = "PROVENANCE_REQUIRED"
    HASH_BOUND = "HASH_BOUND"
    OFFICIAL_CURRENT_REQUIRED = "OFFICIAL_CURRENT_REQUIRED"


class IndependenceStatus(str, Enum):
    INDEPENDENT = "INDEPENDENT"
    NOT_INDEPENDENT = "NOT_INDEPENDENT"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class GovernedSourceRecord:
    source_id: str
    source_title: str
    source_version: str
    domain: str
    registry_status: RegistryStatus
    provenance_ref: str
    content_hash: str | None
    verification_policy: VerificationPolicy
    allowed_agents: tuple[str, ...]
    allowed_tasks: tuple[str, ...]
    context_token_cap: int
    current_official_verification: bool = False
    writeback_authority: str = "NONE"
    authority_level: str = "REFERENCE_ONLY"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        for label in ("source_id", "source_title", "source_version", "domain"):
            if not getattr(self, label).strip():
                raise ValueError(f"{label} must not be empty")
        if not self.provenance_ref.strip():
            raise ValueError("source provenance is required")
        if self.context_token_cap <= 0:
            raise ValueError("context_token_cap must be positive")
        if not self.allowed_agents or not self.allowed_tasks:
            raise ValueError("governed source requires explicit agent and task allowlists")
        if self.writeback_authority != "NONE":
            raise ValueError("SOURCE_USE != WRITEBACK_AUTHORITY")
        if self.canonical_effect != "NONE":
            raise ValueError("SOURCE_SELF_DECLARED_CANONICAL != AION_CANONICAL_STATE")
        if self.verification_policy is VerificationPolicy.HASH_BOUND and not self.content_hash:
            raise ValueError("HASH_BOUND source requires content_hash")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(asdict(self))


@dataclass(frozen=True, slots=True)
class SourceAdmissionDecision:
    source_id: str
    agent: str
    task: str
    requested_tokens: int
    admitted: bool
    disposition: str
    reasons: tuple[str, ...]
    source_fingerprint: str
    canonical_effect: str = "NONE"
    writeback_authority: str = "NONE"

    def __post_init__(self) -> None:
        if self.canonical_effect != "NONE" or self.writeback_authority != "NONE":
            raise ValueError("source admission cannot grant canonical or writeback authority")
        if self.requested_tokens <= 0:
            raise ValueError("requested_tokens must be positive")
        if self.admitted and self.disposition != "ADMIT":
            raise ValueError("admitted decision must use ADMIT disposition")
        if not self.admitted and self.disposition != "HOLD":
            raise ValueError("rejected decision must fail closed to HOLD")


def admit_source(record: GovernedSourceRecord, *, agent: str, task: str, requested_tokens: int) -> SourceAdmissionDecision:
    if requested_tokens <= 0:
        raise ValueError("requested_tokens must be positive")

    reasons: list[str] = []
    if record.registry_status is not RegistryStatus.ACTIVE_REFERENCE:
        reasons.append(f"registry_status={record.registry_status.value}")
    if agent not in record.allowed_agents:
        reasons.append("agent_not_allowed")
    if task not in record.allowed_tasks:
        reasons.append("task_not_allowed")
    if requested_tokens > record.context_token_cap:
        reasons.append("context_token_cap_exceeded")
    if record.verification_policy is VerificationPolicy.OFFICIAL_CURRENT_REQUIRED and not record.current_official_verification:
        reasons.append("current_official_verification_required")
    if record.verification_policy is VerificationPolicy.HASH_BOUND and not record.content_hash:
        reasons.append("content_hash_required")

    admitted = not reasons
    return SourceAdmissionDecision(
        source_id=record.source_id,
        agent=agent,
        task=task,
        requested_tokens=requested_tokens,
        admitted=admitted,
        disposition="ADMIT" if admitted else "HOLD",
        reasons=tuple(reasons),
        source_fingerprint=record.fingerprint,
    )


@dataclass(frozen=True, slots=True)
class AgentSourceExposure:
    agent: str
    source_fingerprints: tuple[str, ...]
    prompt_policy_refs: tuple[str, ...] = field(default_factory=tuple)
    direct_peer_communication: bool = False

    def __post_init__(self) -> None:
        if not self.agent.strip():
            raise ValueError("agent is required")
        if any(not item.strip() for item in self.source_fingerprints):
            raise ValueError("source fingerprints must be non-empty")


@dataclass(frozen=True, slots=True)
class IndependenceAssessment:
    aion: AgentSourceExposure
    astra: AgentSourceExposure
    reconciliation_after_independent_phase: bool
    source_independence: IndependenceStatus
    communication_independence: IndependenceStatus
    replication_claim: str
    reasons: tuple[str, ...]

    @property
    def fingerprint(self) -> str:
        return canonical_hash(asdict(self))


def assess_independence(
    aion: AgentSourceExposure,
    astra: AgentSourceExposure,
    *,
    reconciliation_after_independent_phase: bool,
) -> IndependenceAssessment:
    aion_sources = set(aion.source_fingerprints)
    astra_sources = set(astra.source_fingerprints)
    shared_sources = aion_sources & astra_sources

    if not aion_sources or not astra_sources:
        source_independence = IndependenceStatus.UNKNOWN
    elif shared_sources:
        source_independence = IndependenceStatus.NOT_INDEPENDENT
    else:
        source_independence = IndependenceStatus.INDEPENDENT

    if aion.direct_peer_communication or astra.direct_peer_communication:
        communication_independence = IndependenceStatus.NOT_INDEPENDENT
    else:
        communication_independence = IndependenceStatus.INDEPENDENT

    reasons: list[str] = []
    if source_independence is IndependenceStatus.UNKNOWN:
        reasons.append("source_exposure_unknown_or_empty")
    if source_independence is IndependenceStatus.NOT_INDEPENDENT:
        reasons.append("shared_source_exposure")
    if communication_independence is IndependenceStatus.NOT_INDEPENDENT:
        reasons.append("direct_peer_communication")
    if not reconciliation_after_independent_phase:
        reasons.append("reconciliation_started_too_early")

    replication_allowed = (
        source_independence is IndependenceStatus.INDEPENDENT
        and communication_independence is IndependenceStatus.INDEPENDENT
        and reconciliation_after_independent_phase
    )
    return IndependenceAssessment(
        aion=aion,
        astra=astra,
        reconciliation_after_independent_phase=reconciliation_after_independent_phase,
        source_independence=source_independence,
        communication_independence=communication_independence,
        replication_claim="ADMISSIBLE_CANDIDATE" if replication_allowed else "HOLD",
        reasons=tuple(reasons),
    )
