from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import Iterable, Mapping

from aion_research_eval import CaseResult, ClaimBoundaryGate, ExperimentReport


class AuditStatus(str, Enum):
    ADMITTED_FOR_REVIEW = "ADMITTED_FOR_REVIEW"
    HOLD = "HOLD"
    INVALID = "INVALID"


@dataclass(frozen=True, slots=True)
class EvaluationAudit:
    status: AuditStatus
    reason: str
    case_count: int
    pass_rate: float | None
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False
    research_only: bool = True
    scientific_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    model_execution: bool = False
    observed_result: str = "NOT_EVALUATED"

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status.value,
            "reason": self.reason,
            "case_count": self.case_count,
            "pass_rate": self.pass_rate,
            "canonical_effect": self.canonical_effect,
            "governance_effect": self.governance_effect,
            "deployment": self.deployment,
            "research_only": self.research_only,
            "scientific_conclusion": self.scientific_conclusion,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "model_execution": self.model_execution,
            "observed_result": self.observed_result,
        }


def _audit(status: AuditStatus, reason: str, report: ExperimentReport) -> EvaluationAudit:
    return EvaluationAudit(status, reason, len(report.cases), report.pass_rate)


def _case_ids(report: ExperimentReport) -> list[str]:
    return [case.case_id for case in report.cases]


def _metadata_provenance_complete(case: CaseResult) -> bool:
    value = case.metadata.get("case_provenance_ref")
    return isinstance(value, str) and bool(value.strip())


def audit_evaluation_report(
    report: ExperimentReport,
    *,
    expected_dataset: str,
    expected_case_ids: Iterable[str] = (),
    forbidden_claim: str | None = None,
) -> EvaluationAudit:
    if not expected_dataset.strip():
        return _audit(AuditStatus.INVALID, "EXPECTED_DATASET_MISSING", report)
    if report.dataset_name != expected_dataset:
        return _audit(AuditStatus.HOLD, "DATASET_SCOPE_MISMATCH", report)
    if not report.implementation_id.strip():
        return _audit(AuditStatus.INVALID, "IMPLEMENTATION_ID_MISSING", report)
    if not report.research_only:
        return _audit(AuditStatus.INVALID, "RESEARCH_ONLY_FLAG_DISABLED", report)
    if report.canonical_effect != "NONE":
        return _audit(AuditStatus.INVALID, "CANONICAL_EFFECT_REQUESTED", report)
    ids = _case_ids(report)
    if not ids or any(not case_id.strip() for case_id in ids):
        return _audit(AuditStatus.INVALID, "CASE_ID_MISSING", report)
    if len(ids) != len(set(ids)):
        return _audit(AuditStatus.INVALID, "DUPLICATE_CASE_ID", report)
    expected = tuple(item for item in expected_case_ids if item.strip())
    if expected and set(ids) != set(expected):
        return _audit(AuditStatus.HOLD, "CASE_COVERAGE_MISMATCH", report)
    if any(case.elapsed_ms < 0.0 or not isfinite(case.elapsed_ms) for case in report.cases):
        return _audit(AuditStatus.INVALID, "ELAPSED_TIME_INVALID", report)
    if any(not case.evidence for case in report.cases):
        return _audit(AuditStatus.HOLD, "CASE_EVIDENCE_MISSING", report)
    evaluator_names = [item.evaluator for case in report.cases for item in case.evidence]
    if any(not name.strip() for name in evaluator_names):
        return _audit(AuditStatus.INVALID, "EVALUATOR_ID_MISSING", report)
    if any(not _metadata_provenance_complete(case) for case in report.cases):
        return _audit(AuditStatus.HOLD, "CASE_PROVENANCE_INCOMPLETE", report)
    if forbidden_claim is not None:
        disposition = ClaimBoundaryGate().disposition(forbidden_claim)
        if disposition == "DENY_PROMOTION":
            return _audit(AuditStatus.INVALID, "FORBIDDEN_CLAIM_PROMOTION", report)
    return _audit(AuditStatus.ADMITTED_FOR_REVIEW, "EVALUATION_REPORT_ADMITTED_FOR_REVIEW_ONLY", report)


def audit_report_comparison(
    left: ExperimentReport,
    right: ExperimentReport,
    *,
    expected_dataset: str,
) -> EvaluationAudit:
    if left.dataset_name != right.dataset_name or left.dataset_name != expected_dataset:
        return _audit(AuditStatus.HOLD, "COMPARISON_DATASET_MISMATCH", left)
    if left.implementation_id == right.implementation_id:
        return _audit(AuditStatus.INVALID, "COMPARISON_IMPLEMENTATION_COLLISION", left)
    if not left.research_only or not right.research_only:
        return _audit(AuditStatus.INVALID, "COMPARISON_RESEARCH_ONLY_FLAG_DISABLED", left)
    if left.canonical_effect != "NONE" or right.canonical_effect != "NONE":
        return _audit(AuditStatus.INVALID, "COMPARISON_CANONICAL_EFFECT_REQUESTED", left)
    if _case_ids(left) != _case_ids(right):
        return _audit(AuditStatus.HOLD, "COMPARISON_CASE_ORDER_MISMATCH", left)
    return _audit(AuditStatus.ADMITTED_FOR_REVIEW, "COMPARISON_ADMITTED_FOR_REVIEW_ONLY", left)
