from __future__ import annotations

from dataclasses import dataclass

from aion_prereg_integrity import AnalysisClass, AuditStatus, Disposition, InterventionPlan, audit_plan


@dataclass(frozen=True, slots=True)
class PreregAudit:
    status: str
    disposition: str
    reason: str
    plan_id: str
    confirmatory_analysis_ids: tuple[str, ...] = ()
    exploratory_analysis_ids: tuple[str, ...] = ()
    scientific_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False
    intervention_executed: bool = False
    observed_outcomes: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "disposition": self.disposition,
            "reason": self.reason,
            "plan_id": self.plan_id,
            "confirmatory_analysis_ids": list(self.confirmatory_analysis_ids),
            "exploratory_analysis_ids": list(self.exploratory_analysis_ids),
            "scientific_conclusion": self.scientific_conclusion,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
            "intervention_executed": self.intervention_executed,
            "observed_outcomes": self.observed_outcomes,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "identity_continuity_conclusion": self.identity_continuity_conclusion,
        }


def _from_base(plan: InterventionPlan) -> PreregAudit:
    decision = audit_plan(plan)
    return PreregAudit(
        status=decision.status.value,
        disposition=decision.disposition.value,
        reason=decision.reason,
        plan_id=decision.plan_id,
        confirmatory_analysis_ids=decision.confirmatory_analysis_ids,
        exploratory_analysis_ids=decision.exploratory_analysis_ids,
    )


def audit_preregistration(plan: InterventionPlan) -> PreregAudit:
    if not plan.plan_id or not plan.plan_version:
        return PreregAudit(AuditStatus.INVALID.value, Disposition.HOLD.value, "MISSING_PLAN_ID_OR_VERSION", plan.plan_id)
    if not plan.immutable_digest or any(ch.isspace() for ch in plan.immutable_digest):
        return PreregAudit(AuditStatus.INVALID.value, Disposition.HOLD.value, "IMMUTABLE_DIGEST_FORMAT_INVALID", plan.plan_id)
    if any(not outcome.outcome_id.strip() for outcome in plan.outcomes):
        return PreregAudit(AuditStatus.INVALID.value, Disposition.HOLD.value, "OUTCOME_ID_MISSING", plan.plan_id)
    if any(not analysis.analysis_id.strip() for analysis in plan.analyses):
        return PreregAudit(AuditStatus.INVALID.value, Disposition.HOLD.value, "ANALYSIS_ID_MISSING", plan.plan_id)
    outcome_ids = {outcome.outcome_id for outcome in plan.outcomes}
    analysis_ids = {analysis.analysis_id for analysis in plan.analyses}
    if not set(plan.report_outcome_ids).issubset(outcome_ids):
        return PreregAudit(AuditStatus.INVALID.value, Disposition.HOLD.value, "REPORT_UNKNOWN_OUTCOME", plan.plan_id)
    if not set(plan.report_analysis_ids).issubset(analysis_ids):
        return PreregAudit(AuditStatus.INVALID.value, Disposition.HOLD.value, "REPORT_UNKNOWN_ANALYSIS", plan.plan_id)
    if not set(plan.exploratory_analysis_ids).issubset(analysis_ids):
        return PreregAudit(AuditStatus.INVALID.value, Disposition.HOLD.value, "EXPLORATORY_UNKNOWN_ANALYSIS", plan.plan_id)
    deviation_ids = [deviation.deviation_id for deviation in plan.deviations]
    if any(not deviation_id.strip() for deviation_id in deviation_ids):
        return PreregAudit(AuditStatus.INVALID.value, Disposition.HOLD.value, "DEVIATION_ID_MISSING", plan.plan_id)
    if len(deviation_ids) != len(set(deviation_ids)):
        return PreregAudit(AuditStatus.INVALID.value, Disposition.HOLD.value, "DUPLICATE_DEVIATION_ID", plan.plan_id)
    return _from_base(plan)


@dataclass(frozen=True, slots=True)
class OutcomeLockSnapshot:
    plan_id: str
    digest_before: str
    digest_after: str
    outcome_ids_before: frozenset[str]
    outcome_ids_after: frozenset[str]
    analysis_ids_before: frozenset[str]
    analysis_ids_after: frozenset[str]
    observed_outcome: bool


def audit_outcome_lock(snapshot: OutcomeLockSnapshot) -> PreregAudit:
    if not snapshot.plan_id:
        return PreregAudit(AuditStatus.INVALID.value, Disposition.HOLD.value, "LOCK_PLAN_ID_MISSING", snapshot.plan_id)
    if not snapshot.digest_before or not snapshot.digest_after:
        return PreregAudit(AuditStatus.INVALID.value, Disposition.HOLD.value, "LOCK_DIGEST_MISSING", snapshot.plan_id)
    added_outcomes = snapshot.outcome_ids_after - snapshot.outcome_ids_before
    added_analyses = snapshot.analysis_ids_after - snapshot.analysis_ids_before
    if snapshot.observed_outcome and (added_outcomes or added_analyses):
        return PreregAudit(AuditStatus.INVALID.value, Disposition.HOLD.value, "POST_OUTCOME_DECLARATION_MUTATION", snapshot.plan_id)
    if snapshot.observed_outcome and snapshot.digest_before != snapshot.digest_after:
        return PreregAudit(AuditStatus.INVALID.value, Disposition.HOLD.value, "PLAN_DIGEST_CHANGED_AFTER_OUTCOME", snapshot.plan_id)
    if not snapshot.observed_outcome and (added_outcomes or added_analyses or snapshot.digest_before != snapshot.digest_after):
        return PreregAudit(AuditStatus.INDETERMINATE.value, Disposition.HOLD.value, "PRE_OUTCOME_PLAN_CHANGE_REQUIRES_REVIEW", snapshot.plan_id)
    return PreregAudit(AuditStatus.VALID.value, Disposition.CONFIRMATORY_REVIEW.value, "OUTCOME_LOCK_UNCHANGED", snapshot.plan_id)


def audit_intervention_boundary(plan: InterventionPlan) -> PreregAudit:
    decision = audit_preregistration(plan)
    return PreregAudit(
        status=decision.status,
        disposition=decision.disposition,
        reason=decision.reason,
        plan_id=decision.plan_id,
        confirmatory_analysis_ids=decision.confirmatory_analysis_ids,
        exploratory_analysis_ids=decision.exploratory_analysis_ids,
    )
