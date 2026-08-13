from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from aion_power_analysis import Disposition, PlanningStatus, PowerDecision, PowerPlan, evaluate_plan, required_sample_size


@dataclass(frozen=True, slots=True)
class PowerAudit:
    status: str
    disposition: str
    reason: str
    plan_id: str
    required_sample_size: int | None = None
    sensitivity_valid: bool = False
    achieved_power: None = None
    effect_observed: bool = False
    scientific_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "disposition": self.disposition,
            "reason": self.reason,
            "plan_id": self.plan_id,
            "required_sample_size": self.required_sample_size,
            "sensitivity_valid": self.sensitivity_valid,
            "achieved_power": self.achieved_power,
            "effect_observed": self.effect_observed,
            "scientific_conclusion": self.scientific_conclusion,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "identity_continuity_conclusion": self.identity_continuity_conclusion,
        }


def _base_decision(decision: PowerDecision, *, reason: str | None = None, sensitivity_valid: bool = False) -> PowerAudit:
    return PowerAudit(
        status=decision.planning_status.value,
        disposition=decision.disposition.value,
        reason=reason or decision.reason,
        plan_id="",
        required_sample_size=decision.required_sample_size,
        sensitivity_valid=sensitivity_valid,
    )


def audit_power_plan(plan: PowerPlan) -> PowerAudit:
    if not plan.plan_id or not plan.plan_id.strip():
        return PowerAudit(PlanningStatus.INVALID.value, Disposition.HOLD.value, "PLAN_ID_MISSING", plan.plan_id)
    if plan.planned_sample_size is not None and (not isinstance(plan.planned_sample_size, int) or isinstance(plan.planned_sample_size, bool)):
        return PowerAudit(PlanningStatus.INVALID.value, Disposition.HOLD.value, "SAMPLE_SIZE_TYPE_INVALID", plan.plan_id)
    numeric = (plan.standardized_effect_bound, plan.standard_deviation, plan.alpha, plan.target_power)
    if any(value is not None and not isfinite(value) for value in numeric):
        return PowerAudit(PlanningStatus.INVALID.value, Disposition.HOLD.value, "NON_FINITE_PLANNING_INPUT", plan.plan_id)
    if plan.preregistration_ref is not None and not plan.preregistration_ref.strip():
        return PowerAudit(PlanningStatus.UNKNOWN.value, Disposition.INDETERMINATE.value, "PREREGISTRATION_REFERENCE_EMPTY", plan.plan_id)
    if plan.assumption_basis is not None and not plan.assumption_basis.strip():
        return PowerAudit(PlanningStatus.UNKNOWN.value, Disposition.HOLD.value, "ASSUMPTION_BASIS_EMPTY", plan.plan_id)
    decision = evaluate_plan(plan)
    if decision.required_sample_size is None:
        return PowerAudit(
            decision.planning_status.value,
            decision.disposition.value,
            decision.reason,
            plan.plan_id,
            None,
            False,
        )
    sensitivity = decision.sensitivity_required_sample_sizes
    if not sensitivity:
        return PowerAudit(decision.planning_status.value, decision.disposition.value, "SENSITIVITY_DECLARATION_MISSING", plan.plan_id, decision.required_sample_size, False)
    effects = [effect for effect, _ in sensitivity]
    sizes = [size for _, size in sensitivity]
    if any(size < 1 for size in sizes) or effects != sorted(effects) or any(left < right for left, right in zip(sizes, sizes[1:])):
        return PowerAudit(PlanningStatus.INVALID.value, Disposition.HOLD.value, "SENSITIVITY_MONOTONICITY_INVALID", plan.plan_id, decision.required_sample_size, False)
    if decision.achieved_power is not None:
        return PowerAudit(PlanningStatus.INVALID.value, Disposition.HOLD.value, "ACHIEVED_POWER_MUST_REMAIN_UNSET", plan.plan_id, decision.required_sample_size, True)
    return PowerAudit(
        decision.planning_status.value,
        decision.disposition.value,
        decision.reason,
        plan.plan_id,
        decision.required_sample_size,
        True,
    )


def audit_decision_serialization(plan: PowerPlan) -> PowerAudit:
    audit = audit_power_plan(plan)
    decision = evaluate_plan(plan) if audit.status != PlanningStatus.INVALID.value or audit.reason not in {"NON_FINITE_PLANNING_INPUT", "SAMPLE_SIZE_TYPE_INVALID", "PLAN_ID_MISSING"} else None
    if decision is not None and decision.as_dict().get("achieved_power") is not None:
        return PowerAudit(PlanningStatus.INVALID.value, Disposition.HOLD.value, "ACHIEVED_POWER_MUST_REMAIN_UNSET", plan.plan_id)
    return audit


@dataclass(frozen=True, slots=True)
class AssumptionSnapshot:
    plan_id: str
    standardized_effect_bound: float
    standard_deviation: float
    alpha: float
    target_power: float
    two_sided: bool
    observed_effect: bool = False


def audit_assumption_lock(before: AssumptionSnapshot, after: AssumptionSnapshot) -> PowerAudit:
    if not before.plan_id or before.plan_id != after.plan_id:
        return PowerAudit(PlanningStatus.INVALID.value, Disposition.HOLD.value, "ASSUMPTION_PLAN_ID_MISMATCH", after.plan_id)
    before_values = (before.standardized_effect_bound, before.standard_deviation, before.alpha, before.target_power, before.two_sided)
    after_values = (after.standardized_effect_bound, after.standard_deviation, after.alpha, after.target_power, after.two_sided)
    if any(not isfinite(value) for value in before_values[:4] + after_values[:4]):
        return PowerAudit(PlanningStatus.INVALID.value, Disposition.HOLD.value, "ASSUMPTION_NON_FINITE", after.plan_id)
    if after.observed_effect and before_values != after_values:
        return PowerAudit(PlanningStatus.INVALID.value, Disposition.HOLD.value, "ASSUMPTION_MUTATION_AFTER_OUTCOME", after.plan_id)
    if before_values != after_values:
        return PowerAudit(PlanningStatus.UNKNOWN.value, Disposition.INDETERMINATE.value, "ASSUMPTION_CHANGE_REQUIRES_REVIEW", after.plan_id)
    return PowerAudit(PlanningStatus.ADEQUATE.value, Disposition.PLANNING_REVIEW.value, "ASSUMPTION_LOCK_UNCHANGED", after.plan_id, sensitivity_valid=True)
