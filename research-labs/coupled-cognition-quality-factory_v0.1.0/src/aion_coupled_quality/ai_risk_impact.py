from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path

from .models import QualityError, Severity


RISK_IMPACT_RECEIPT_SCHEMA_VERSION = "0.1.0"


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


def _hex(name: str, value: str, length: int) -> None:
    if type(value) is not str or len(value) != length or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise QualityError(f"{name} must be lowercase {length}-hex")


def _digest(payload: object) -> str:
    return hashlib.sha256(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()


def _git_text(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), *args],
            text=True,
            encoding="utf-8",
            stderr=subprocess.STDOUT,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise QualityError(f"git provenance resolution failed: {exc}") from exc


def _git_bytes(root: Path, *args: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), *args],
            stderr=subprocess.STDOUT,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise QualityError(f"git object resolution failed: {exc}") from exc


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
    risk_version: str
    exact_source_state_ref: str
    system_scope: str
    lifecycle_stage: AILifecycleStage
    risk_source: str
    event_or_condition: str
    affected_refs: tuple[str, ...]
    likelihood: RiskLikelihood
    consequence: Severity
    existing_control_refs: tuple[str, ...]
    control_effectiveness_refs: tuple[str, ...]
    treatment_refs: tuple[str, ...]
    residual_risk: Severity
    risk_evaluation_basis_ref: str
    residual_risk_basis_ref: str
    risk_owner_ref: str
    reassessment_triggers: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    disposition: AIRiskDisposition
    linked_ncr_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in (
            "risk_id",
            "risk_version",
            "exact_source_state_ref",
            "system_scope",
            "risk_source",
            "event_or_condition",
            "risk_evaluation_basis_ref",
            "residual_risk_basis_ref",
            "risk_owner_ref",
        ):
            _text(name, getattr(self, name))
        for name in (
            "affected_refs",
            "existing_control_refs",
            "control_effectiveness_refs",
            "treatment_refs",
            "reassessment_triggers",
            "evidence_refs",
            "linked_ncr_refs",
        ):
            _text_tuple(
                name,
                getattr(self, name),
                allow_empty=name in {
                    "existing_control_refs",
                    "control_effectiveness_refs",
                    "treatment_refs",
                    "linked_ncr_refs",
                },
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
            if not self.control_effectiveness_refs:
                raise QualityError("accepted risk requires control-effectiveness evidence refs")
            if self.residual_risk in {Severity.HIGH, Severity.CRITICAL}:
                raise QualityError("high/critical residual risk cannot be accepted with controls")
        if self.disposition is AIRiskDisposition.TREATMENT_REQUIRED and not self.treatment_refs:
            raise QualityError("treatment-required risk requires treatment refs")


@dataclass(frozen=True, slots=True)
class AIImpactAssessmentRecord:
    assessment_id: str
    assessment_version: str
    exact_source_state_ref: str
    system_scope: str
    ai_system_context_ref: str
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
    mitigation_effectiveness_refs: tuple[str, ...]
    linked_risk_ids: tuple[str, ...]
    residual_impact: Severity
    residual_impact_basis_ref: str
    reassessment_triggers: tuple[str, ...]
    assessment_evidence_basis_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    disposition: AIImpactDisposition
    observed_impacts_claimed: bool = False
    observed_impact_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in (
            "assessment_id",
            "assessment_version",
            "exact_source_state_ref",
            "system_scope",
            "ai_system_context_ref",
            "intended_use",
            "societal_context",
            "residual_impact_basis_ref",
        ):
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
            "mitigation_effectiveness_refs",
            "linked_risk_ids",
            "reassessment_triggers",
            "assessment_evidence_basis_refs",
            "evidence_refs",
            "observed_impact_refs",
        ):
            _text_tuple(
                name,
                getattr(self, name),
                allow_empty=name in {
                    "affected_groups",
                    "mitigation_effectiveness_refs",
                    "observed_impact_refs",
                },
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
            if not self.mitigation_effectiveness_refs:
                raise QualityError("assessed impact requires mitigation-effectiveness evidence refs")
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
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
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

        risk_ids = tuple(sorted(item.risk_id for item in risks))
        impact_ids = tuple(sorted(item.assessment_id for item in impacts))
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
            "RISK_EVALUATION_AND_RESIDUAL_BASIS_RECORDED",
            "CONTROL_AND_MITIGATION_EFFECTIVENESS_EVIDENCE_RECORDED",
            "RISK_VERSION_AND_SOURCE_STATE_BOUND",
            "IMPACT_ASSESSMENT_VERSION_AND_SOURCE_STATE_BOUND",
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



@dataclass(frozen=True, slots=True)
class AIRiskImpactReceipt:
    receipt_id: str
    assessment_target_ref: str
    exact_source_state_ref: str
    exact_runtime_ref: str
    producer_git_head: str
    producer_tree_sha: str
    producer_contract_ref: str
    producer_contract_sha256: str
    risk_ids: tuple[str, ...]
    impact_assessment_ids: tuple[str, ...]
    risk_set_sha256: str
    impact_set_sha256: str
    assessment_sha256: str
    disposition: AIRiskImpactDisposition
    receipt_sha256: str
    schema_version: str = RISK_IMPACT_RECEIPT_SCHEMA_VERSION
    iso_conformance_claim: str = "NONE"
    certification_claim: str = "NONE"
    scientific_disposition: str = "HOLD"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment_authority: str = "NONE"

    def __post_init__(self) -> None:
        for name in (
            "receipt_id",
            "assessment_target_ref",
            "exact_source_state_ref",
            "exact_runtime_ref",
            "producer_contract_ref",
        ):
            _text(name, getattr(self, name))
        _text_tuple("risk_ids", self.risk_ids)
        _text_tuple("impact_assessment_ids", self.impact_assessment_ids)
        if self.risk_ids != tuple(sorted(self.risk_ids)):
            raise QualityError("risk_ids must use canonical sorted order")
        if self.impact_assessment_ids != tuple(sorted(self.impact_assessment_ids)):
            raise QualityError("impact_assessment_ids must use canonical sorted order")
        if self.schema_version != RISK_IMPACT_RECEIPT_SCHEMA_VERSION:
            raise QualityError("unsupported AI risk/impact receipt schema version")
        if type(self.disposition) is not AIRiskImpactDisposition:
            raise QualityError("receipt disposition must be an exact AIRiskImpactDisposition")
        _hex("producer_git_head", self.producer_git_head, 40)
        _hex("producer_tree_sha", self.producer_tree_sha, 40)
        for name in (
            "producer_contract_sha256",
            "risk_set_sha256",
            "impact_set_sha256",
            "assessment_sha256",
            "receipt_sha256",
        ):
            _hex(name, getattr(self, name), 64)
        if self.iso_conformance_claim != "NONE" or self.certification_claim != "NONE":
            raise QualityError("risk/impact receipt cannot claim ISO conformance or certification")
        if self.scientific_disposition != "HOLD":
            raise QualityError("risk/impact receipt cannot establish scientific validity")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise QualityError("risk/impact receipt cannot establish subjectivity")
        if self.consciousness_conclusion != "NOT_ESTABLISHED":
            raise QualityError("risk/impact receipt cannot establish consciousness")
        if self.phenomenal_experience_conclusion != "NOT_ESTABLISHED":
            raise QualityError("risk/impact receipt cannot establish phenomenal experience")
        if self.canonical_effect != "NONE" or self.deployment_authority != "NONE":
            raise QualityError("risk/impact receipt cannot grant canonical or deployment authority")
        if self.receipt_sha256 != _digest(self.payload_without_digest()):
            raise QualityError("risk/impact receipt content digest mismatch")

    def payload_without_digest(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "receipt_id": self.receipt_id,
            "assessment_target_ref": self.assessment_target_ref,
            "exact_source_state_ref": self.exact_source_state_ref,
            "exact_runtime_ref": self.exact_runtime_ref,
            "producer_git_head": self.producer_git_head,
            "producer_tree_sha": self.producer_tree_sha,
            "producer_contract_ref": self.producer_contract_ref,
            "producer_contract_sha256": self.producer_contract_sha256,
            "risk_ids": self.risk_ids,
            "impact_assessment_ids": self.impact_assessment_ids,
            "risk_set_sha256": self.risk_set_sha256,
            "impact_set_sha256": self.impact_set_sha256,
            "assessment_sha256": self.assessment_sha256,
            "disposition": self.disposition.value,
            "iso_conformance_claim": self.iso_conformance_claim,
            "certification_claim": self.certification_claim,
            "scientific_disposition": self.scientific_disposition,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "consciousness_conclusion": self.consciousness_conclusion,
            "phenomenal_experience_conclusion": self.phenomenal_experience_conclusion,
            "canonical_effect": self.canonical_effect,
            "deployment_authority": self.deployment_authority,
        }


def build_risk_impact_receipt(
    *,
    receipt_id: str,
    assessment_target_ref: str,
    risks: tuple[AIRiskRecord, ...],
    impacts: tuple[AIImpactAssessmentRecord, ...],
    assessment: AIRiskImpactAssessment,
    exact_source_state_ref: str,
    exact_runtime_ref: str,
    producer_git_head: str,
    producer_tree_sha: str,
    producer_contract_ref: str,
    producer_contract_sha256: str,
) -> AIRiskImpactReceipt:
    _text("receipt_id", receipt_id)
    _text("assessment_target_ref", assessment_target_ref)
    _text("exact_source_state_ref", exact_source_state_ref)
    _text("exact_runtime_ref", exact_runtime_ref)
    _text("producer_contract_ref", producer_contract_ref)
    _hex("producer_git_head", producer_git_head, 40)
    _hex("producer_tree_sha", producer_tree_sha, 40)
    _hex("producer_contract_sha256", producer_contract_sha256, 64)
    if type(risks) is not tuple or not risks or any(type(item) is not AIRiskRecord for item in risks):
        raise QualityError("receipt risks must contain exact AIRiskRecord values")
    if type(impacts) is not tuple or not impacts or any(
        type(item) is not AIImpactAssessmentRecord for item in impacts
    ):
        raise QualityError("receipt impacts must contain exact AIImpactAssessmentRecord values")
    if type(assessment) is not AIRiskImpactAssessment:
        raise QualityError("receipt assessment must be an exact AIRiskImpactAssessment")

    recomputed_assessment = AIRiskImpactGate().assess(risks=risks, impacts=impacts)
    if assessment != recomputed_assessment:
        raise QualityError("receipt assessment does not match recomputed gate assessment")

    if any(item.exact_source_state_ref != exact_source_state_ref for item in risks):
        raise QualityError("risk record source state does not match receipt source state")
    if any(item.exact_source_state_ref != exact_source_state_ref for item in impacts):
        raise QualityError("impact assessment source state does not match receipt source state")

    risk_items = sorted(risks, key=lambda item: item.risk_id)
    impact_items = sorted(impacts, key=lambda item: item.assessment_id)
    risk_ids = tuple(item.risk_id for item in risk_items)
    impact_ids = tuple(item.assessment_id for item in impact_items)
    if assessment.risk_ids != risk_ids:
        raise QualityError("assessment risk ids do not match receipt risk inputs")
    if assessment.impact_assessment_ids != impact_ids:
        raise QualityError("assessment impact ids do not match receipt impact inputs")

    risk_set_sha256 = _digest([asdict(item) for item in risk_items])
    impact_set_sha256 = _digest([asdict(item) for item in impact_items])
    assessment_sha256 = _digest(asdict(assessment))

    payload = {
        "schema_version": RISK_IMPACT_RECEIPT_SCHEMA_VERSION,
        "receipt_id": receipt_id,
        "assessment_target_ref": assessment_target_ref,
        "exact_source_state_ref": exact_source_state_ref,
        "exact_runtime_ref": exact_runtime_ref,
        "producer_git_head": producer_git_head,
        "producer_tree_sha": producer_tree_sha,
        "producer_contract_ref": producer_contract_ref,
        "producer_contract_sha256": producer_contract_sha256,
        "risk_ids": risk_ids,
        "impact_assessment_ids": impact_ids,
        "risk_set_sha256": risk_set_sha256,
        "impact_set_sha256": impact_set_sha256,
        "assessment_sha256": assessment_sha256,
        "disposition": assessment.disposition.value,
        "iso_conformance_claim": "NONE",
        "certification_claim": "NONE",
        "scientific_disposition": "HOLD",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "consciousness_conclusion": "NOT_ESTABLISHED",
        "phenomenal_experience_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "deployment_authority": "NONE",
    }
    return AIRiskImpactReceipt(
        receipt_id=receipt_id,
        assessment_target_ref=assessment_target_ref,
        exact_source_state_ref=exact_source_state_ref,
        exact_runtime_ref=exact_runtime_ref,
        producer_git_head=producer_git_head,
        producer_tree_sha=producer_tree_sha,
        producer_contract_ref=producer_contract_ref,
        producer_contract_sha256=producer_contract_sha256,
        risk_ids=risk_ids,
        impact_assessment_ids=impact_ids,
        risk_set_sha256=risk_set_sha256,
        impact_set_sha256=impact_set_sha256,
        assessment_sha256=assessment_sha256,
        disposition=assessment.disposition,
        receipt_sha256=_digest(payload),
    )



def build_repository_bound_risk_impact_receipt(
    *,
    receipt_id: str,
    assessment_target_ref: str,
    risks: tuple[AIRiskRecord, ...],
    impacts: tuple[AIImpactAssessmentRecord, ...],
    assessment: AIRiskImpactAssessment,
    exact_source_state_ref: str,
    exact_runtime_ref: str,
    repository_root: Path,
    producer_contract_ref: str = (
        "research-labs/coupled-cognition-quality-factory_v0.1.0/"
        "src/aion_coupled_quality/ai_risk_impact.py"
    ),
) -> AIRiskImpactReceipt:
    """Resolve producer provenance from committed Git objects before issuing a receipt.

    Dirty working-tree bytes are intentionally ignored. The receipt binds the exact
    committed producer HEAD/tree/contract plus the caller-declared source/runtime state.
    """
    root = repository_root.resolve()
    top_level = Path(_git_text(root, "rev-parse", "--show-toplevel")).resolve()
    if top_level != root:
        raise QualityError("repository_root must be the exact Git top-level")
    contract_path = Path(producer_contract_ref)
    if contract_path.is_absolute() or ".." in contract_path.parts or not producer_contract_ref.strip():
        raise QualityError("producer_contract_ref must be a safe repository-relative path")

    producer_git_head = _git_text(root, "rev-parse", "HEAD")
    producer_tree_sha = _git_text(root, "rev-parse", "HEAD^{tree}")
    contract_bytes = _git_bytes(root, "show", f"HEAD:{producer_contract_ref}")
    producer_contract_sha256 = hashlib.sha256(contract_bytes).hexdigest()

    return build_risk_impact_receipt(
        receipt_id=receipt_id,
        assessment_target_ref=assessment_target_ref,
        risks=risks,
        impacts=impacts,
        assessment=assessment,
        exact_source_state_ref=exact_source_state_ref,
        exact_runtime_ref=exact_runtime_ref,
        producer_git_head=producer_git_head,
        producer_tree_sha=producer_tree_sha,
        producer_contract_ref=producer_contract_ref,
        producer_contract_sha256=producer_contract_sha256,
    )
