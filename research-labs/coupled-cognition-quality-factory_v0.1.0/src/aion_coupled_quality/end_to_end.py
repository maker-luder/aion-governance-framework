from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import StrEnum

from .models import QualityError, Severity


class ControlTarget(StrEnum):
    PRE_EXECUTION = "PRE_EXECUTION"
    MEASUREMENT_ASSURANCE = "MEASUREMENT_ASSURANCE"
    EXISTING_RESEARCH_QUALITY_CHAIN = "EXISTING_RESEARCH_QUALITY_CHAIN"
    POST_RELEASE_MONITORING = "POST_RELEASE_MONITORING"
    AUDIT_PROGRAMME = "AUDIT_PROGRAMME"
    MANAGEMENT_REVIEW = "MANAGEMENT_REVIEW"


class MeasurementQualification(StrEnum):
    QUALIFIED = "QUALIFIED"
    REQUALIFICATION_REQUIRED = "REQUALIFICATION_REQUIRED"


class ExistingChainDisposition(StrEnum):
    READY_FOR_HUMAN_REVIEW = "READY_FOR_HUMAN_REVIEW"
    CAPA_REQUIRED = "CAPA_REQUIRED"
    HOLD = "HOLD"


class FieldSignalState(StrEnum):
    OPEN = "OPEN"
    TRIAGED = "TRIAGED"
    LINKED_TO_NCR = "LINKED_TO_NCR"
    CLOSED = "CLOSED"


class AuditIndependence(StrEnum):
    INTERNAL_INDEPENDENT = "INTERNAL_INDEPENDENT"
    EXTERNAL_INDEPENDENT = "EXTERNAL_INDEPENDENT"
    NON_INDEPENDENT = "NON_INDEPENDENT"


class ManagementDecision(StrEnum):
    NO_ACTION = "NO_ACTION"
    QUALITY_PLAN_REVISION_REQUIRED = "QUALITY_PLAN_REVISION_REQUIRED"
    MEASUREMENT_REQUALIFICATION_REQUIRED = "MEASUREMENT_REQUALIFICATION_REQUIRED"
    AUDIT_REQUIRED = "AUDIT_REQUIRED"
    CAPA_REQUIRED = "CAPA_REQUIRED"
    HOLD = "HOLD"


class EndToEndDisposition(StrEnum):
    READY_FOR_HUMAN_REVIEW = "READY_FOR_HUMAN_REVIEW"
    CAPA_REQUIRED = "CAPA_REQUIRED"
    HOLD = "HOLD"


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


def _sha256_payload(payload: object) -> str:
    rendered = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(rendered).hexdigest()


@dataclass(frozen=True, slots=True)
class ControlPlanEntry:
    control_id: str
    target: ControlTarget
    quality_characteristic: str
    control_method_ref: str
    evidence_required: tuple[str, ...]
    acceptance_criterion: str
    reaction_plan: str
    responsible_role: str

    def __post_init__(self) -> None:
        for name in (
            "control_id",
            "quality_characteristic",
            "control_method_ref",
            "acceptance_criterion",
            "reaction_plan",
            "responsible_role",
        ):
            _text(name, getattr(self, name))
        if type(self.target) is not ControlTarget:
            raise QualityError("target must be an exact ControlTarget")
        _text_tuple("evidence_required", self.evidence_required)


@dataclass(frozen=True, slots=True)
class ResearchQualityPlan:
    plan_id: str
    research_question_ref: str
    subjectivity_core_binding_ref: str
    four_domain_candidate_fingerprint: str
    critical_quality_attributes: tuple[str, ...]
    controls: tuple[ControlPlanEntry, ...]
    measurement_ids: tuple[str, ...]
    risk_refs: tuple[str, ...]
    configuration_refs: tuple[str, ...]
    post_release_monitoring_required: bool = True
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        for name in (
            "plan_id",
            "research_question_ref",
            "subjectivity_core_binding_ref",
            "four_domain_candidate_fingerprint",
        ):
            _text(name, getattr(self, name))
        for name in (
            "critical_quality_attributes",
            "measurement_ids",
            "risk_refs",
            "configuration_refs",
        ):
            _text_tuple(name, getattr(self, name))
        if type(self.controls) is not tuple or not self.controls:
            raise QualityError("controls must be a non-empty tuple")
        if any(type(control) is not ControlPlanEntry for control in self.controls):
            raise QualityError("controls must contain exact ControlPlanEntry values")
        control_ids = [control.control_id for control in self.controls]
        if len(control_ids) != len(set(control_ids)):
            raise QualityError("control ids must be unique")
        targets = {control.target for control in self.controls}
        missing_targets = set(ControlTarget) - targets
        if missing_targets:
            missing = ",".join(sorted(target.value for target in missing_targets))
            raise QualityError(f"quality plan missing end-to-end control targets: {missing}")
        if type(self.post_release_monitoring_required) is not bool:
            raise QualityError("post_release_monitoring_required must be an exact bool")
        if self.canonical_effect != "NONE" or self.deployment:
            raise QualityError("quality plan cannot create canonical or deployment effect")

    def assessment_target_payload(self) -> dict[str, object]:
        """Canonical semantic target for AI risk/impact assessment.

        Configuration refs are intentionally excluded because the final plan pre-binds
        the risk/impact receipt digest, which would create a self-referential hash.
        Producer/source/runtime identities remain separately enforced by the full QMS.
        """
        control_payload = [
            {
                "control_id": control.control_id,
                "target": control.target.value,
                "quality_characteristic": control.quality_characteristic,
                "control_method_ref": control.control_method_ref,
                "evidence_required": sorted(control.evidence_required),
                "acceptance_criterion": control.acceptance_criterion,
                "reaction_plan": control.reaction_plan,
                "responsible_role": control.responsible_role,
            }
            for control in sorted(self.controls, key=lambda item: item.control_id)
        ]
        return {
            "plan_id": self.plan_id,
            "research_question_ref": self.research_question_ref,
            "subjectivity_core_binding_ref": self.subjectivity_core_binding_ref,
            "four_domain_candidate_fingerprint": self.four_domain_candidate_fingerprint,
            "critical_quality_attributes": sorted(self.critical_quality_attributes),
            "controls": control_payload,
            "measurement_ids": sorted(self.measurement_ids),
            "risk_refs": sorted(self.risk_refs),
            "post_release_monitoring_required": self.post_release_monitoring_required,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
        }

    def assessment_target_sha256(self) -> str:
        return _sha256_payload(self.assessment_target_payload())


@dataclass(frozen=True, slots=True)
class MeasurementAssuranceRecord:
    measurement_id: str
    target_construct: str
    observable: str
    measurement_locus: str
    method_ref: str
    method_version: str
    evaluator_ref: str
    evaluator_version: str
    data_ref: str
    repeatability_ref: str
    reproducibility_ref: str
    uncertainty_statement: str
    construct_validity_scope: str
    known_failure_modes: tuple[str, ...]
    synthetic_fixture: bool
    empirical_claim_capable: bool
    qualification: MeasurementQualification

    def __post_init__(self) -> None:
        for name in (
            "measurement_id",
            "target_construct",
            "observable",
            "measurement_locus",
            "method_ref",
            "method_version",
            "evaluator_ref",
            "evaluator_version",
            "data_ref",
            "repeatability_ref",
            "reproducibility_ref",
            "uncertainty_statement",
            "construct_validity_scope",
        ):
            _text(name, getattr(self, name))
        _text_tuple("known_failure_modes", self.known_failure_modes)
        if type(self.synthetic_fixture) is not bool or type(self.empirical_claim_capable) is not bool:
            raise QualityError("measurement fixture/claim flags must be exact bools")
        if type(self.qualification) is not MeasurementQualification:
            raise QualityError("qualification must be an exact MeasurementQualification")
        if self.synthetic_fixture and self.empirical_claim_capable:
            raise QualityError(
                "deterministic/synthetic fixtures cannot be declared empirical-claim capable"
            )

    def semantic_payload(self) -> dict[str, object]:
        return {
            "measurement_id": self.measurement_id,
            "target_construct": self.target_construct,
            "observable": self.observable,
            "measurement_locus": self.measurement_locus,
            "method_ref": self.method_ref,
            "method_version": self.method_version,
            "evaluator_ref": self.evaluator_ref,
            "evaluator_version": self.evaluator_version,
            "data_ref": self.data_ref,
            "repeatability_ref": self.repeatability_ref,
            "reproducibility_ref": self.reproducibility_ref,
            "uncertainty_statement": self.uncertainty_statement,
            "construct_validity_scope": self.construct_validity_scope,
            "known_failure_modes": sorted(self.known_failure_modes),
            "synthetic_fixture": self.synthetic_fixture,
            "empirical_claim_capable": self.empirical_claim_capable,
            "qualification": self.qualification.value,
        }

    def semantic_sha256(self) -> str:
        return _sha256_payload(self.semantic_payload())


@dataclass(frozen=True, slots=True)
class ExistingQualityChainBinding:
    chain_id: str
    four_domain_candidate_fingerprint: str
    disposition: ExistingChainDisposition

    def __post_init__(self) -> None:
        _text("chain_id", self.chain_id)
        _text("four_domain_candidate_fingerprint", self.four_domain_candidate_fingerprint)
        if type(self.disposition) is not ExistingChainDisposition:
            raise QualityError("disposition must be an exact ExistingChainDisposition")


@dataclass(frozen=True, slots=True)
class FieldQualitySignal:
    signal_id: str
    source_ref: str
    affected_refs: tuple[str, ...]
    severity: Severity
    state: FieldSignalState
    ncr_ref: str = ""
    resolution_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        _text("signal_id", self.signal_id)
        _text("source_ref", self.source_ref)
        _text_tuple("affected_refs", self.affected_refs)
        if type(self.severity) is not Severity:
            raise QualityError("severity must be an exact Severity")
        if type(self.state) is not FieldSignalState:
            raise QualityError("state must be an exact FieldSignalState")
        if self.state is FieldSignalState.LINKED_TO_NCR:
            _text("ncr_ref", self.ncr_ref)
        if self.state is FieldSignalState.CLOSED:
            _text_tuple("resolution_refs", self.resolution_refs)


@dataclass(frozen=True, slots=True)
class QualityAuditRecord:
    audit_id: str
    scope: str
    criteria_refs: tuple[str, ...]
    auditor_ref: str
    independence: AuditIndependence
    competence_ref: str
    evidence_refs: tuple[str, ...]
    finding_refs: tuple[str, ...]
    open_finding_refs: tuple[str, ...]
    unresolved_high_severity_finding: bool
    ncr_refs: tuple[str, ...] = field(default_factory=tuple)
    complete: bool = True

    def __post_init__(self) -> None:
        for name in ("audit_id", "scope", "auditor_ref", "competence_ref"):
            _text(name, getattr(self, name))
        _text_tuple("criteria_refs", self.criteria_refs)
        _text_tuple("evidence_refs", self.evidence_refs)
        _text_tuple("finding_refs", self.finding_refs, allow_empty=True)
        _text_tuple("open_finding_refs", self.open_finding_refs, allow_empty=True)
        _text_tuple("ncr_refs", self.ncr_refs, allow_empty=True)
        if not set(self.open_finding_refs) <= set(self.finding_refs):
            raise QualityError("open_finding_refs must be a subset of finding_refs")
        if type(self.independence) is not AuditIndependence:
            raise QualityError("independence must be an exact AuditIndependence")
        if type(self.unresolved_high_severity_finding) is not bool or type(self.complete) is not bool:
            raise QualityError("audit flags must be exact bools")
        if self.unresolved_high_severity_finding and not self.ncr_refs:
            raise QualityError("high-severity audit findings require an NCR reference")


@dataclass(frozen=True, slots=True)
class ManagementReviewRecord:
    review_id: str
    input_refs: tuple[str, ...]
    measurement_requalification_required: bool
    unresolved_audit_findings: bool
    unresolved_field_signals: bool
    decision: ManagementDecision
    merge_authority: bool = False
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        _text("review_id", self.review_id)
        _text_tuple("input_refs", self.input_refs)
        for name in (
            "measurement_requalification_required",
            "unresolved_audit_findings",
            "unresolved_field_signals",
            "merge_authority",
        ):
            if type(getattr(self, name)) is not bool:
                raise QualityError(f"{name} must be an exact bool")
        if type(self.decision) is not ManagementDecision:
            raise QualityError("decision must be an exact ManagementDecision")
        if self.merge_authority:
            raise QualityError("management review cannot grant merge authority")
        if self.scientific_disposition != "HOLD":
            raise QualityError("management review cannot establish scientific validity")
        if self.canonical_effect != "NONE" or self.deployment:
            raise QualityError("management review cannot create canonical or deployment effect")


@dataclass(frozen=True, slots=True)
class EndToEndQualityAssessment:
    plan_id: str
    disposition: EndToEndDisposition
    reasons: tuple[str, ...]
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    scientific_disposition: str = "HOLD"
    merge_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False


class EndToEndQualitySystemEngine:
    """Binds missing QMS front/back controls around the existing research quality chain.

    This adapter does not replace Four-Domain admission, ResearchQualityChain,
    QualityFactory NCR/CAPA, Human review, or merge authority.
    """

    def assess(
        self,
        *,
        plan: ResearchQualityPlan,
        measurements: tuple[MeasurementAssuranceRecord, ...],
        chain: ExistingQualityChainBinding,
        field_signals: tuple[FieldQualitySignal, ...],
        audits: tuple[QualityAuditRecord, ...],
        management_review: ManagementReviewRecord,
    ) -> EndToEndQualityAssessment:
        reasons: list[str] = ["END_TO_END_QMS_ENVELOPE_EVALUATED"]

        if plan.four_domain_candidate_fingerprint != chain.four_domain_candidate_fingerprint:
            reasons.append("FOUR_DOMAIN_FINGERPRINT_MISMATCH")

        measurement_ids = [record.measurement_id for record in measurements]
        if len(measurement_ids) != len(set(measurement_ids)):
            reasons.append("DUPLICATE_MEASUREMENT_ID")
        if set(measurement_ids) != set(plan.measurement_ids):
            reasons.append("QUALITY_PLAN_MEASUREMENT_BINDING_MISMATCH")

        measurement_requalification = any(
            record.qualification is MeasurementQualification.REQUALIFICATION_REQUIRED
            for record in measurements
        )
        if measurement_requalification:
            reasons.append("MEASUREMENT_REQUALIFICATION_REQUIRED")

        if chain.disposition is ExistingChainDisposition.HOLD:
            reasons.append("EXISTING_RESEARCH_QUALITY_CHAIN_HOLD")
        elif chain.disposition is ExistingChainDisposition.CAPA_REQUIRED:
            reasons.append("EXISTING_RESEARCH_QUALITY_CHAIN_CAPA_REQUIRED")

        signal_ids = [signal.signal_id for signal in field_signals]
        if len(signal_ids) != len(set(signal_ids)):
            reasons.append("DUPLICATE_FIELD_SIGNAL_ID")
        unresolved_field = any(signal.state is not FieldSignalState.CLOSED for signal in field_signals)
        severe_uncontained = any(
            signal.severity in {Severity.HIGH, Severity.CRITICAL}
            and signal.state in {FieldSignalState.OPEN, FieldSignalState.TRIAGED}
            for signal in field_signals
        )
        if unresolved_field:
            reasons.append("OPEN_FIELD_SIGNAL_REVIEW_REQUIRED")
        if severe_uncontained:
            reasons.append("HIGH_OR_CRITICAL_FIELD_SIGNAL_REQUIRES_NCR_CAPA")

        audit_ids = [audit.audit_id for audit in audits]
        if len(audit_ids) != len(set(audit_ids)):
            reasons.append("DUPLICATE_AUDIT_ID")
        if not audits:
            reasons.append("AUDIT_PROGRAMME_EXECUTION_REQUIRED")
        incomplete_audit = any(not audit.complete for audit in audits)
        unresolved_audit = any(audit.open_finding_refs for audit in audits)
        unresolved_high_audit = any(audit.unresolved_high_severity_finding for audit in audits)
        if incomplete_audit:
            reasons.append("INCOMPLETE_AUDIT_RECORD")
        if unresolved_audit:
            reasons.append("OPEN_AUDIT_FINDING_REVIEW_REQUIRED")
        if unresolved_high_audit:
            reasons.append("HIGH_SEVERITY_AUDIT_FINDING_REQUIRES_NCR_CAPA")

        expected_review_flags = (
            measurement_requalification,
            unresolved_audit,
            unresolved_field,
        )
        actual_review_flags = (
            management_review.measurement_requalification_required,
            management_review.unresolved_audit_findings,
            management_review.unresolved_field_signals,
        )
        if actual_review_flags != expected_review_flags:
            reasons.append("MANAGEMENT_REVIEW_INPUT_SUMMARY_MISMATCH")

        expected_review_refs = {
            plan.plan_id,
            chain.chain_id,
            *measurement_ids,
            *signal_ids,
            *audit_ids,
        }
        if not expected_review_refs <= set(management_review.input_refs):
            reasons.append("MANAGEMENT_REVIEW_TRACE_INPUTS_INCOMPLETE")

        issues_present = any(expected_review_flags) or severe_uncontained or unresolved_high_audit
        if issues_present and management_review.decision is ManagementDecision.NO_ACTION:
            reasons.append("MANAGEMENT_REVIEW_NO_ACTION_WITH_OPEN_QUALITY_ISSUES")

        structural_hold = any(
            reason in {
                "FOUR_DOMAIN_FINGERPRINT_MISMATCH",
                "DUPLICATE_MEASUREMENT_ID",
                "QUALITY_PLAN_MEASUREMENT_BINDING_MISMATCH",
                "DUPLICATE_FIELD_SIGNAL_ID",
                "DUPLICATE_AUDIT_ID",
                "AUDIT_PROGRAMME_EXECUTION_REQUIRED",
                "INCOMPLETE_AUDIT_RECORD",
                "MANAGEMENT_REVIEW_INPUT_SUMMARY_MISMATCH",
                "MANAGEMENT_REVIEW_TRACE_INPUTS_INCOMPLETE",
                "EXISTING_RESEARCH_QUALITY_CHAIN_HOLD",
                "OPEN_FIELD_SIGNAL_REVIEW_REQUIRED",
                "OPEN_AUDIT_FINDING_REVIEW_REQUIRED",
            }
            for reason in reasons
        )
        if structural_hold:
            return self._result(plan, EndToEndDisposition.HOLD, reasons)

        capa_required = any(
            reason in {
                "MEASUREMENT_REQUALIFICATION_REQUIRED",
                "EXISTING_RESEARCH_QUALITY_CHAIN_CAPA_REQUIRED",
                "HIGH_OR_CRITICAL_FIELD_SIGNAL_REQUIRES_NCR_CAPA",
                "HIGH_SEVERITY_AUDIT_FINDING_REQUIRES_NCR_CAPA",
                "MANAGEMENT_REVIEW_NO_ACTION_WITH_OPEN_QUALITY_ISSUES",
            }
            for reason in reasons
        )
        if capa_required:
            return self._result(plan, EndToEndDisposition.CAPA_REQUIRED, reasons)

        reasons.extend(
            (
                "QUALITY_PLAN_BOUND_TO_FULL_CONTROL_SURFACE",
                "MEASUREMENT_SYSTEMS_QUALIFIED_FOR_DECLARED_SCOPE",
                "EXISTING_RESEARCH_QUALITY_CHAIN_REUSED_NOT_DUPLICATED",
                "POST_RELEASE_FIELD_FEEDBACK_BOUND",
                "AUDIT_PROGRAMME_EXECUTION_BOUND",
                "MANAGEMENT_REVIEW_BOUND_WITHOUT_MERGE_AUTHORITY",
                "QMS_PASS_IS_NOT_SUBJECTIVITY_EVIDENCE",
            )
        )
        return self._result(plan, EndToEndDisposition.READY_FOR_HUMAN_REVIEW, reasons)

    @staticmethod
    def _result(
        plan: ResearchQualityPlan,
        disposition: EndToEndDisposition,
        reasons: list[str],
    ) -> EndToEndQualityAssessment:
        return EndToEndQualityAssessment(
            plan_id=plan.plan_id,
            disposition=disposition,
            reasons=tuple(reasons),
        )
