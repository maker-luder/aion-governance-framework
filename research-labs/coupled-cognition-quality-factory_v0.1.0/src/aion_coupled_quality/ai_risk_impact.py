from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from .models import QualityError, Severity


def _text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise QualityError(f"{name} must be non-empty text")


def _text_tuple(name: str, values: tuple[str, ...], *, allow_empty: bool = False) -> None:
    if type(values) is not tuple:
        raise QualityError(f"{name} must be a tuple")
    if not allow_empty and not values:
        raise QualityError(f"{name} must not be empty")
    if any(type(value) is not str or not value.strip() for value in values):
        raise QualityError(f"{name} must contain non-empty text")
    if len(values) != len(set(values)):
        raise QualityError(f"{name} must be unique")


class AILifecycleStage(StrEnum):
    RESEARCH = "RESEARCH"
    DEVELOPMENT = "DEVELOPMENT"
    PRE_DEPLOYMENT = "PRE_DEPLOYMENT"
    DEPLOYMENT = "DEPLOYMENT"
    OPERATION = "OPERATION"
    RETIREMENT = "RETIREMENT"


class RiskLikelihood(StrEnum):
    RARE = "RARE"
    UNLIKELY = "UNLIKELY"
    POSSIBLE = "POSSIBLE"
    LIKELY = "LIKELY"
    ALMOST_CERTAIN = "ALMOST_CERTAIN"


class AIRiskDisposition(StrEnum):
    ACCEPTED_WITH_CONTROLS = "ACCEPTED_WITH_CONTROLS"
    TREATMENT_REQUIRED = "TREATMENT_REQUIRED"
    HOLD = "HOLD"


class AIImpactDisposition(StrEnum):
    ASSESSED_WITH_CONTROLS = "ASSESSED_WITH_CONTROLS"
    MITIGATION_REQUIRED = "MITIGATION_REQUIRED"
    HOLD = "HOLD"


class AIRiskImpactDisposition(StrEnum):
    READY_FOR_HUMAN_REVIEW = "READY_FOR_HUMAN_REVIEW"
    TREATMENT_OR_MITIGATION_REQUIRED = "TREATMENT_OR_MITIGATION_REQUIRED"
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class AIRiskRecord:
    risk_id: str
    system_scope: str
    lifecycle_stage: AILifecycleStage
    risk_source: str
    event_or_condition: str
    affected_refs: tuple[str, ...]
    likelihood: RiskLikelihood
    consequence: Severity
    existing_control_refs: tuple[str, ...]
    treatment_refs: tuple[str, ...]
    residual_risk: Severity
    risk_owner_ref: str
    reassessment_triggers: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    disposition: AIRiskDisposition
    linked_ncr_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in (
            "risk_id",
            "system_scope",
            "risk_source",
            "event_or_condition",
            "risk_owner_ref",
        ):
            _text(name, getattr(self, name))
        for name in (
            "affected_refs",
            "existing_control_refs",
            "treatment_refs",
            "reassessment_triggers",
            "evidence_refs",
            "linked_ncr_refs",
        ):
            _text_tuple(
                name,
                getattr(self, name),
                allow_empty=name in {"existing_control_refs", "treatment_refs", "linked_ncr_refs"},
            )
        if type(self.lifecycle_stage) is not AILifecycleStage:
            raise QualityError("lifecycle_stage must be an exact AILifecycleStage")
        if type(self.likelihood) is not RiskLikelihood:
            raise QualityError("likelihood must be an exact RiskLikelihood")
        if type(self.consequence) is not Severity or type(self.residual_risk) is not Severity:
            raise QualityError("risk consequence and residual risk must use exact Severity values")
        if type(self.disposition) is not AIRiskDisposition:
            raise QualityError("disposition must be an exact AIRiskDisposition")
        if self.disposition is AIRiskDisposition.ACCEPTED_WITH_CONTROLS:
            if not self.existing_control_refs:
                raise QualityError("accepted risk requires existing controls")
            if self.residual_risk in {Severity.HIGH, Severity.CRITICAL}:
                raise QualityError("high/critical residual risk cannot be accepted with controls")
        if self.disposition is AIRiskDisposition.TREATMENT_REQUIRED and not self.treatment_refs:
            raise QualityError("treatment-required risk requires treatment refs")


@dataclass(frozen=True, slots=True)
class AIImpactAssessmentRecord:
    assessment_id: str
    system_scope: str
    lifecycle_stage: AILifecycleStage
    intended_use: str
    foreseeable_uses: tuple[str, ...]
    foreseeable_misuses: tuple[str, ...]
    affected_individuals: tuple[str, ...]
    affected_groups: tuple[str, ...]
    societal_context: str
    potential_benefit_refs: tuple[str, ...]
    potential_harm_refs: tuple[str, ...]
    human_oversight_refs: tuple[str, ...]
    mitigation_refs: tuple[str, ...]
    linked_risk_ids: tuple[str, ...]
    residual_impact: Severity
    reassessment_triggers: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    disposition: AIImpactDisposition
    observed_impacts_claimed: bool = False
    observed_impact_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in ("assessment_id", "system_scope", "intended_use", "societal_context"):
            _text(name, getattr(self, name))
        for name in (
            "foreseeable_uses",
            "foreseeable_misuses",
            "affected_individuals",
            "affected_groups",
            "potential_benefit_refs",
            "potential_harm_refs",
            "human_oversight_refs",
            "mitigation_refs",
            "linked_risk_ids",
            "reassessment_triggers",
            "evidence_refs",
            "observed_impact_refs",
        ):
            _text_tuple(
                name,
                getattr(self, name),
                allow_empty=name in {"affected_groups", "observed_impact_refs"},
            )
        if type(self.lifecycle_stage) is not AILifecycleStage:
            raise QualityError("lifecycle_stage must be an exact AILifecycleStage")
        if type(self.residual_impact) is not Severity:
            raise QualityError("residual_impact must use an exact Severity")
        if type(self.disposition) is not AIImpactDisposition:
            raise QualityError("disposition must be an exact AIImpactDisposition")
        if type(self.observed_impacts_claimed) is not bool:
            raise QualityError("observed_impacts_claimed must be an exact bool")
        if self.observed_impacts_claimed != bool(self.observed_impact_refs):
            raise QualityError("observed-impact claim flag must agree with observed impact refs")
        if self.disposition is AIImpactDisposition.ASSESSED_WITH_CONTROLS:
            if not self.human_oversight_refs or not self.mitigation_refs:
                raise QualityError("assessed impact requires oversight and mitigation refs")
            if self.residual_impact in {Severity.HIGH, Severity.CRITICAL}:
                raise QualityError("high/critical residual impact cannot be assessed as controlled")
        if self.disposition is AIImpactDisposition.MITIGATION_REQUIRED and not self.mitigation_refs:
            raise QualityError("mitigation-required impact requires mitigation refs")


@dataclass(frozen=True, slots=True)
class AIRiskImpactAssessment:
    disposition: AIRiskImpactDisposition
    reasons: tuple[str, ...]
    risk_ids: tuple[str, ...]
    impact_assessment_ids: tuple[str, ...]
    iso_conformance_claim: str = "NONE"
    certification_claim: str = "NONE"
    scientific_disposition: str = "HOLD"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment_authority: str = "NONE"


class AIRiskImpactGate:
    """Fail-closed AI risk and impact gate for repository research-engineering use.

    This repository-native control is informed by public ISO/IEC 23894:2023 and
    ISO/IEC 42005:2025 descriptions. It is not an ISO conformance or certification
    mechanism and grants no deployment, merge, canonical, or scientific authority.
    """

    def assess(
        self,
        *,
        risks: tuple[AIRiskRecord, ...],
        impacts: tuple[AIImpactAssessmentRecord, ...],
    ) -> AIRiskImpactAssessment:
        if type(risks) is not tuple or not risks:
            raise QualityError("AI risk gate requires at least one risk record")
        if type(impacts) is not tuple or not impacts:
            raise QualityError("AI impact gate requires at least one impact assessment")
        if any(type(item) is not AIRiskRecord for item in risks):
            raise QualityError("risks must contain exact AIRiskRecord values")
        if any(type(item) is not AIImpactAssessmentRecord for item in impacts):
            raise QualityError("impacts must contain exact AIImpactAssessmentRecord values")

        risk_ids = tuple(item.risk_id for item in risks)
        impact_ids = tuple(item.assessment_id for item in impacts)
        if len(risk_ids) != len(set(risk_ids)):
            raise QualityError("risk identifiers must be unique")
        if len(impact_ids) != len(set(impact_ids)):
            raise QualityError("impact assessment identifiers must be unique")

        known_risks = set(risk_ids)
        for impact in impacts:
            if not set(impact.linked_risk_ids) <= known_risks:
                raise QualityError("impact assessment references unknown risk identifiers")

        reasons = [
            "AI_RISK_REGISTER_PRESENT",
            "AI_IMPACT_ASSESSMENT_PRESENT",
            "RESIDUAL_RISK_AND_IMPACT_RECORDED",
            "REASSESSMENT_TRIGGERS_RECORDED",
            "ISO_CONFORMANCE_NOT_CLAIMED",
            "CERTIFICATION_NOT_CLAIMED",
            "SCIENTIFIC_VALIDITY_NOT_GRANTED",
        ]

        if any(item.disposition is AIRiskDisposition.HOLD for item in risks) or any(
            item.disposition is AIImpactDisposition.HOLD for item in impacts
        ):
            reasons.append("STRUCTURAL_OR_GOVERNANCE_HOLD_PRESENT")
            return AIRiskImpactAssessment(
                AIRiskImpactDisposition.HOLD,
                tuple(reasons),
                risk_ids,
                impact_ids,
            )

        if any(item.disposition is AIRiskDisposition.TREATMENT_REQUIRED for item in risks) or any(
            item.disposition is AIImpactDisposition.MITIGATION_REQUIRED for item in impacts
        ):
            reasons.append("OPEN_RISK_TREATMENT_OR_IMPACT_MITIGATION")
            return AIRiskImpactAssessment(
                AIRiskImpactDisposition.TREATMENT_OR_MITIGATION_REQUIRED,
                tuple(reasons),
                risk_ids,
                impact_ids,
            )

        reasons.append("BOUNDED_RISK_AND_IMPACT_RECORDS_READY_FOR_HUMAN_REVIEW")
        return AIRiskImpactAssessment(
            AIRiskImpactDisposition.READY_FOR_HUMAN_REVIEW,
            tuple(reasons),
            risk_ids,
            impact_ids,
        )
