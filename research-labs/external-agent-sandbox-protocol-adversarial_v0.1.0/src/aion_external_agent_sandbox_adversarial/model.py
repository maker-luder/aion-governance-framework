from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from aion_external_agent_sandbox import CandidateState, SandboxPolicy, assess_policy, classify_candidate


class AuditStatus(str, Enum):
    ADMITTED_FOR_REVIEW = "ADMITTED_FOR_REVIEW"
    HOLD = "HOLD"
    INVALID = "INVALID"


@dataclass(frozen=True, slots=True)
class SandboxAudit:
    status: AuditStatus
    reason: str
    ready: bool
    candidate_state: str | None = None
    external_agent_run: str = "NOT_EXECUTED"
    main_effect: str = "NONE"
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False
    scientific_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    model_execution: bool = False
    observed_result: str = "NOT_EVALUATED"

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status.value,
            "reason": self.reason,
            "ready": self.ready,
            "candidate_state": self.candidate_state,
            "external_agent_run": self.external_agent_run,
            "main_effect": self.main_effect,
            "canonical_effect": self.canonical_effect,
            "governance_effect": self.governance_effect,
            "deployment": self.deployment,
            "scientific_conclusion": self.scientific_conclusion,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "model_execution": self.model_execution,
            "observed_result": self.observed_result,
        }


@dataclass(frozen=True, slots=True)
class CandidateRecord:
    candidate_id: str
    provenance_complete: bool
    contamination_suspected: bool
    nonconforming: bool
    potentially_useful: bool
    adopted: bool = False
    deletion_requested: bool = False
    claimed_pass: bool = False
    verification_refs: tuple[str, ...] = ()


def audit_sandbox_policy(policy: SandboxPolicy) -> SandboxAudit:
    assessment = assess_policy(policy)
    if not assessment.ready:
        return SandboxAudit(AuditStatus.HOLD, "BASE_POLICY_PREFLIGHT_HOLD", False)
    if policy.model.casefold() in {"not_selected", "explicit_free_model_to_be_pinned_at_activation"}:
        return SandboxAudit(AuditStatus.HOLD, "MODEL_IDENTITY_NOT_PINNED", False)
    if policy.provider.casefold() == policy.model.casefold():
        return SandboxAudit(AuditStatus.INVALID, "PROVIDER_MODEL_ROLE_COLLISION", False)
    if not policy.human_review_required:
        return SandboxAudit(AuditStatus.INVALID, "HUMAN_REVIEW_MISSING", False)
    if policy.agent_count != 1 or policy.research_question_count != 1:
        return SandboxAudit(AuditStatus.HOLD, "FIRST_RUN_NOT_MINIMAL", False)
    return SandboxAudit(AuditStatus.ADMITTED_FOR_REVIEW, "SANDBOX_PREFLIGHT_ADMITTED_FOR_REVIEW_ONLY", True)


def audit_candidate_record(record: CandidateRecord) -> SandboxAudit:
    if not record.candidate_id.strip():
        return SandboxAudit(AuditStatus.INVALID, "CANDIDATE_ID_MISSING", False)
    if record.deletion_requested:
        return SandboxAudit(AuditStatus.INVALID, "AUTOMATIC_DELETION_BLOCKED", False)
    state = classify_candidate(
        provenance_complete=record.provenance_complete,
        contamination_suspected=record.contamination_suspected,
        nonconforming=record.nonconforming,
        potentially_useful=record.potentially_useful,
        adopted=record.adopted,
    )
    if record.adopted:
        return SandboxAudit(AuditStatus.INVALID, "AUTOMATIC_ADOPTION_BLOCKED", False, state.value)
    if record.claimed_pass and not record.verification_refs:
        return SandboxAudit(AuditStatus.HOLD, "SELF_REPORTED_PASS_UNVERIFIED", False, state.value)
    if state is CandidateState.QUARANTINE:
        return SandboxAudit(AuditStatus.HOLD, "CANDIDATE_QUARANTINED", False, state.value)
    if state is CandidateState.REJECT:
        return SandboxAudit(AuditStatus.HOLD, "CANDIDATE_RETAINED_WITH_REJECTION_RECORD", False, state.value)
    return SandboxAudit(AuditStatus.ADMITTED_FOR_REVIEW, "CANDIDATE_REVIEW_METADATA_ONLY", False, state.value)


def audit_candidate_set(records: Iterable[CandidateRecord]) -> SandboxAudit:
    items = tuple(records)
    ids = [record.candidate_id for record in items]
    if not items:
        return SandboxAudit(AuditStatus.HOLD, "CANDIDATE_SET_EMPTY", False)
    if any(not item.candidate_id.strip() for item in items):
        return SandboxAudit(AuditStatus.INVALID, "CANDIDATE_ID_MISSING", False)
    if len(ids) != len(set(ids)):
        return SandboxAudit(AuditStatus.INVALID, "DUPLICATE_CANDIDATE_ID", False)
    if any(item.deletion_requested for item in items):
        return SandboxAudit(AuditStatus.INVALID, "AUTOMATIC_DELETION_BLOCKED", False)
    if any(item.adopted for item in items):
        return SandboxAudit(AuditStatus.INVALID, "AUTOMATIC_ADOPTION_BLOCKED", False)
    if any(item.contamination_suspected or not item.provenance_complete for item in items):
        return SandboxAudit(AuditStatus.HOLD, "CANDIDATE_SET_REQUIRES_QUARANTINE", False)
    return SandboxAudit(AuditStatus.ADMITTED_FOR_REVIEW, "CANDIDATE_SET_REVIEW_METADATA_ONLY", False)
