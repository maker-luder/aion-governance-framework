from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CandidateState(str, Enum):
    REVIEW_CANDIDATE = "REVIEW_CANDIDATE"
    RETAIN_ISOLATED = "RETAIN_ISOLATED"
    QUARANTINE = "QUARANTINE"
    REJECT = "REJECT"


@dataclass(frozen=True, slots=True)
class SandboxPolicy:
    provider: str
    model: str
    free_status_verified_at_activation: bool
    explicit_model_lineage: bool
    auto_model_routing: bool
    separate_sandbox_repository: bool
    primary_repository_write: bool
    research_integration_write: bool
    main_write: bool
    auto_merge: bool
    public_safe_capsule_only: bool
    secret_access: bool
    private_memory_access: bool
    local_agent_configuration_access: bool
    scheduled_trigger_enabled: bool
    agent_count: int
    research_question_count: int
    human_review_required: bool
    local_agent_cloud_migration: bool
    local_agent_network_egress: bool
    local_agent_external_worker_role: bool


@dataclass(frozen=True, slots=True)
class SandboxAssessment:
    ready: bool
    reasons: tuple[str, ...]
    external_agent_run: str = "NOT_EXECUTED"
    main_effect: str = "NONE"


def assess_policy(policy: SandboxPolicy) -> SandboxAssessment:
    reasons: list[str] = []
    if not policy.provider.strip():
        reasons.append("PROVIDER_MISSING")
    if not policy.model.strip() or policy.model == "NOT_SELECTED":
        reasons.append("MODEL_LINEAGE_NOT_FROZEN")
    if not policy.free_status_verified_at_activation:
        reasons.append("FREE_STATUS_NOT_REVERIFIED")
    if not policy.explicit_model_lineage or policy.auto_model_routing:
        reasons.append("MODEL_ROUTING_NOT_EXPLICIT")
    if not policy.separate_sandbox_repository:
        reasons.append("SANDBOX_REPOSITORY_NOT_ISOLATED")
    if policy.primary_repository_write or policy.research_integration_write or policy.main_write:
        reasons.append("AION_WRITE_AUTHORITY_PRESENT")
    if policy.auto_merge:
        reasons.append("AUTO_MERGE_PRESENT")
    if not policy.public_safe_capsule_only:
        reasons.append("CAPSULE_SCOPE_UNBOUNDED")
    if policy.secret_access or policy.private_memory_access or policy.local_agent_configuration_access:
        reasons.append("PROHIBITED_CONTEXT_ACCESS_PRESENT")
    if policy.scheduled_trigger_enabled:
        reasons.append("FIRST_RUN_MUST_BE_UNSCHEDULED")
    if policy.agent_count != 1 or policy.research_question_count != 1:
        reasons.append("FIRST_RUN_NOT_MINIMAL")
    if not policy.human_review_required:
        reasons.append("HUMAN_REVIEW_MISSING")
    if policy.local_agent_cloud_migration or policy.local_agent_network_egress or policy.local_agent_external_worker_role:
        reasons.append("LOCAL_AGENT_BOUNDARY_WEAKENED")

    return SandboxAssessment(not reasons, tuple(reasons) if reasons else ("SANDBOX_PREFLIGHT_READY",))


def classify_candidate(*, provenance_complete: bool, contamination_suspected: bool, nonconforming: bool, potentially_useful: bool, adopted: bool = False) -> CandidateState:
    if not provenance_complete or contamination_suspected:
        return CandidateState.QUARANTINE
    if nonconforming and not potentially_useful:
        return CandidateState.REJECT
    if potentially_useful and not adopted:
        return CandidateState.RETAIN_ISOLATED
    return CandidateState.REVIEW_CANDIDATE
