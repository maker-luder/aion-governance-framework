from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from aion_external_evidence import (
    EvidenceDecision,
    ExecutionMode,
    ExternalEvidenceReport,
    normalize_external_report,
)


class AuditStatus(str, Enum):
    ADMITTED_FOR_REVIEW = "ADMITTED_FOR_REVIEW"
    HOLD = "HOLD"
    INVALID = "INVALID"


@dataclass(frozen=True, slots=True)
class ExternalEvidenceAudit:
    status: AuditStatus
    reason: str
    normalized_decision: EvidenceDecision
    replication_eligible: bool
    provenance_complete: bool
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False
    scientific_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    observed_result: str = "NOT_EVALUATED"

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status.value,
            "reason": self.reason,
            "normalized_decision": self.normalized_decision.value,
            "replication_eligible": self.replication_eligible,
            "provenance_complete": self.provenance_complete,
            "canonical_effect": self.canonical_effect,
            "governance_effect": self.governance_effect,
            "deployment": self.deployment,
            "scientific_conclusion": self.scientific_conclusion,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "observed_result": self.observed_result,
        }


def _base_audit(status: AuditStatus, reason: str, normalized) -> ExternalEvidenceAudit:
    return ExternalEvidenceAudit(
        status=status,
        reason=reason,
        normalized_decision=normalized.decision,
        replication_eligible=normalized.replication_eligible,
        provenance_complete=normalized.provenance_complete,
    )


def _known_ids(known_report_ids: Iterable[str]) -> set[str]:
    return {item for item in known_report_ids if item.strip()}


def audit_external_evidence_report(
    report: ExternalEvidenceReport,
    *,
    expected_branch: str,
    known_report_ids: Iterable[str] = (),
    result_observed: bool = False,
) -> ExternalEvidenceAudit:
    normalized = normalize_external_report(report)
    if not expected_branch.strip():
        return _base_audit(AuditStatus.INVALID, "EXPECTED_BRANCH_MISSING", normalized)
    if report.report_id in _known_ids(known_report_ids):
        return _base_audit(AuditStatus.INVALID, "DUPLICATE_REPORT_ID", normalized)
    if report.branch != expected_branch:
        return _base_audit(AuditStatus.HOLD, "BRANCH_SCOPE_MISMATCH", normalized)
    if report.branch == "main":
        return _base_audit(AuditStatus.INVALID, "MAIN_BRANCH_RESEARCH_EVIDENCE_BLOCKED", normalized)
    if report.actor_kind.strip().upper() in {"UNKNOWN", "UNTRUSTED"}:
        return _base_audit(AuditStatus.HOLD, "ACTOR_IDENTITY_UNRESOLVED", normalized)
    if report.execution_mode is ExecutionMode.UNKNOWN and (report.input_hash or report.output_hash):
        return _base_audit(AuditStatus.HOLD, "UNKNOWN_MODE_CANNOT_CARRY_EXECUTION_DIGESTS", normalized)
    if report.execution_mode is ExecutionMode.EXECUTED_REPLICATION:
        if not report.claimed_result.strip():
            return _base_audit(AuditStatus.HOLD, "EXECUTED_REPLICATION_RESULT_CLAIM_MISSING", normalized)
        if not result_observed:
            return _base_audit(AuditStatus.HOLD, "EXECUTED_RESULT_CLAIM_WITHOUT_OBSERVATION", normalized)
    if report.execution_mode is not ExecutionMode.EXECUTED_REPLICATION and result_observed:
        return _base_audit(AuditStatus.INVALID, "RESULT_OBSERVATION_EXCEEDS_DECLARED_EXECUTION_MODE", normalized)
    if normalized.decision is EvidenceDecision.REJECT_INCONSISTENT_CLAIM:
        return _base_audit(AuditStatus.INVALID, "BASE_NORMALIZER_REJECTED_CLAIM", normalized)
    if normalized.decision is EvidenceDecision.HOLD_INCOMPLETE_PROVENANCE:
        return _base_audit(AuditStatus.HOLD, "BASE_NORMALIZER_REQUIRES_PROVENANCE", normalized)
    return _base_audit(AuditStatus.ADMITTED_FOR_REVIEW, "EXTERNAL_EVIDENCE_ADMITTED_FOR_REVIEW_ONLY", normalized)
