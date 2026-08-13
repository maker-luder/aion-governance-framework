"""Design-only preregistration and intervention-integrity audit contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class AuditStatus(StrEnum):
    VALID = "VALID"
    INDETERMINATE = "INDETERMINATE"
    INVALID = "INVALID"


class Disposition(StrEnum):
    CONFIRMATORY_REVIEW = "CONFIRMATORY_REVIEW"
    EXPLORATORY_REVIEW = "EXPLORATORY_REVIEW"
    HOLD = "HOLD"


class AnalysisClass(StrEnum):
    CONFIRMATORY = "CONFIRMATORY"
    EXPLORATORY = "EXPLORATORY"


@dataclass(frozen=True, slots=True)
class PlannedOutcome:
    outcome_id: str
    label: str
    primary: bool
    direction: str | None
    measure_ref: str | None


@dataclass(frozen=True, slots=True)
class PlannedAnalysis:
    analysis_id: str
    outcome_id: str
    analysis_class: AnalysisClass
    method_ref: str | None
    estimand_ref: str | None
    decision_rule_ref: str | None


@dataclass(frozen=True, slots=True)
class Deviation:
    deviation_id: str
    description: str
    disclosed_at: int | None
    rationale: str | None
    impact_assessment: str | None


@dataclass(frozen=True, slots=True)
class InterventionPlan:
    plan_id: str
    plan_version: str
    registered_at: int | None
    intervention_start: int | None
    immutable_digest: str | None
    protocol_ref: str | None
    outcomes: tuple[PlannedOutcome, ...]
    analyses: tuple[PlannedAnalysis, ...]
    deviations: tuple[Deviation, ...]
    report_outcome_ids: frozenset[str]
    report_analysis_ids: frozenset[str]
    exploratory_analysis_ids: frozenset[str]
    all_results_reported: bool


@dataclass(frozen=True, slots=True)
class IntegrityDecision:
    status: AuditStatus
    disposition: Disposition
    reason: str
    plan_id: str
    confirmatory_analysis_ids: tuple[str, ...] = ()
    exploratory_analysis_ids: tuple[str, ...] = ()
    undisclosed_deviation_ids: tuple[str, ...] = ()
    unreported_outcome_ids: tuple[str, ...] = ()
    unreported_analysis_ids: tuple[str, ...] = ()
    scientific_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False
    intervention_executed: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        payload["disposition"] = self.disposition.value
        return payload


def audit_plan(plan: InterventionPlan) -> IntegrityDecision:
    """Audit metadata only; this function does not run an intervention or analysis."""

    if not plan.plan_id or not plan.plan_version:
        return IntegrityDecision(AuditStatus.INVALID, Disposition.HOLD, "MISSING_PLAN_ID_OR_VERSION", plan.plan_id)
    if plan.registered_at is None or plan.intervention_start is None:
        return IntegrityDecision(AuditStatus.INDETERMINATE, Disposition.HOLD, "MISSING_TEMPORAL_ORDERING", plan.plan_id)
    if plan.registered_at > plan.intervention_start:
        return IntegrityDecision(AuditStatus.INVALID, Disposition.HOLD, "REGISTRATION_AFTER_INTERVENTION_START", plan.plan_id)
    if not plan.immutable_digest or not plan.protocol_ref:
        return IntegrityDecision(AuditStatus.INDETERMINATE, Disposition.HOLD, "MISSING_PLAN_IMMUTABILITY_OR_PROTOCOL", plan.plan_id)
    if not plan.outcomes or not plan.analyses:
        return IntegrityDecision(AuditStatus.INVALID, Disposition.HOLD, "MISSING_OUTCOME_OR_ANALYSIS_DECLARATION", plan.plan_id)

    outcome_ids = {outcome.outcome_id for outcome in plan.outcomes}
    if len(outcome_ids) != len(plan.outcomes):
        return IntegrityDecision(AuditStatus.INVALID, Disposition.HOLD, "DUPLICATE_OUTCOME_ID", plan.plan_id)
    analysis_ids = {analysis.analysis_id for analysis in plan.analyses}
    if len(analysis_ids) != len(plan.analyses):
        return IntegrityDecision(AuditStatus.INVALID, Disposition.HOLD, "DUPLICATE_ANALYSIS_ID", plan.plan_id)
    primary_count = sum(1 for outcome in plan.outcomes if outcome.primary)
    if primary_count != 1:
        return IntegrityDecision(AuditStatus.INVALID, Disposition.HOLD, "PRIMARY_OUTCOME_CARDINALITY_INVALID", plan.plan_id)

    for outcome in plan.outcomes:
        if not outcome.measure_ref or not outcome.direction:
            return IntegrityDecision(AuditStatus.INDETERMINATE, Disposition.HOLD, "OUTCOME_MEASURE_OR_DIRECTION_MISSING", plan.plan_id)
    for analysis in plan.analyses:
        if analysis.outcome_id not in outcome_ids:
            return IntegrityDecision(AuditStatus.INVALID, Disposition.HOLD, "ANALYSIS_REFERENCES_UNKNOWN_OUTCOME", plan.plan_id)
        if not analysis.method_ref or not analysis.estimand_ref or not analysis.decision_rule_ref:
            return IntegrityDecision(AuditStatus.INDETERMINATE, Disposition.HOLD, "ANALYSIS_SPECIFICATION_INCOMPLETE", plan.plan_id)

    confirmatory = tuple(sorted(analysis.analysis_id for analysis in plan.analyses if analysis.analysis_class is AnalysisClass.CONFIRMATORY))
    exploratory = tuple(sorted(analysis.analysis_id for analysis in plan.analyses if analysis.analysis_class is AnalysisClass.EXPLORATORY))
    declared_exploratory = set(plan.exploratory_analysis_ids)
    if set(exploratory) != declared_exploratory:
        return IntegrityDecision(
            AuditStatus.INVALID,
            Disposition.HOLD,
            "EXPLORATORY_LABEL_MISMATCH",
            plan.plan_id,
            confirmatory,
            exploratory,
        )

    undisclosed = tuple(sorted(deviation.deviation_id for deviation in plan.deviations if deviation.disclosed_at is None or not deviation.rationale or not deviation.impact_assessment))
    if undisclosed:
        return IntegrityDecision(
            AuditStatus.INDETERMINATE,
            Disposition.HOLD,
            "DEVIATION_DISCLOSURE_INCOMPLETE",
            plan.plan_id,
            confirmatory,
            exploratory,
            undisclosed_deviation_ids=undisclosed,
        )

    unreported_outcomes = tuple(sorted(outcome_ids - set(plan.report_outcome_ids)))
    unreported_analyses = tuple(sorted(analysis_ids - set(plan.report_analysis_ids)))
    if unreported_outcomes or unreported_analyses or not plan.all_results_reported:
        return IntegrityDecision(
            AuditStatus.INDETERMINATE,
            Disposition.HOLD,
            "ALL_PREREGISTERED_RESULTS_NOT_REPORTED",
            plan.plan_id,
            confirmatory,
            exploratory,
            unreported_outcome_ids=unreported_outcomes,
            unreported_analysis_ids=unreported_analyses,
        )

    if exploratory:
        return IntegrityDecision(
            AuditStatus.VALID,
            Disposition.EXPLORATORY_REVIEW,
            "VALID_WITH_EXPLORATORY_ANALYSES_SEPARATED",
            plan.plan_id,
            confirmatory,
            exploratory,
        )
    return IntegrityDecision(
        AuditStatus.VALID,
        Disposition.CONFIRMATORY_REVIEW,
        "VALID_CONFIRMATORY_PLAN_AND_REPORT",
        plan.plan_id,
        confirmatory,
        exploratory,
    )
