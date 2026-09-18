from __future__ import annotations

from dataclasses import replace

import pytest

from aion_coupled_quality import QualityError, Severity
from aion_coupled_quality.ai_risk_impact import (
    AIImpactAssessmentRecord,
    AIImpactDisposition,
    AILifecycleStage,
    AIRiskDisposition,
    AIRiskImpactDisposition,
    AIRiskImpactGate,
    AIRiskRecord,
    RiskLikelihood,
)


def risk(**changes: object) -> AIRiskRecord:
    values: dict[str, object] = {
        "risk_id": "RISK-OVERCLAIM-001",
        "system_scope": "public research-engineering repository",
        "lifecycle_stage": AILifecycleStage.RESEARCH,
        "risk_source": "evidence-to-claim promotion",
        "event_or_condition": "engineering or model output is promoted beyond its evidential ceiling",
        "affected_refs": ("research:subjectivity-core", "public:reader"),
        "likelihood": RiskLikelihood.POSSIBLE,
        "consequence": Severity.HIGH,
        "existing_control_refs": (
            "docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md",
            "docs/RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md",
        ),
        "control_effectiveness_refs": (
            "test:claim-ceiling-negative-paths",
            "ci:research-evidence-admission",
        ),
        "treatment_refs": ("control:claim-ceiling-review",),
        "residual_risk": Severity.MEDIUM,
        "risk_evaluation_basis_ref": "method:repository-native-qualitative-risk-v1",
        "residual_risk_basis_ref": "assessment:overclaim-residual-v1",
        "risk_owner_ref": "role:HUMAN_REVIEW_BOUNDARY",
        "reassessment_triggers": (
            "new model or provider",
            "claim-ceiling policy change",
            "new empirical evidence",
        ),
        "evidence_refs": ("repo:quality-chain",),
        "disposition": AIRiskDisposition.ACCEPTED_WITH_CONTROLS,
    }
    values.update(changes)
    return AIRiskRecord(**values)


def impact(**changes: object) -> AIImpactAssessmentRecord:
    values: dict[str, object] = {
        "assessment_id": "IMPACT-RESEARCH-001",
        "assessment_version": "0.1.0",
        "exact_source_state_ref": "git:d9155e9fd6908b2880adc43e160ece70a1036cc7",
        "system_scope": "AI-assisted research-engineering workflow and its repository control surface",
        "ai_system_context_ref": "context:human-ai-research-engineering-workflow-v1",
        "lifecycle_stage": AILifecycleStage.RESEARCH,
        "intended_use": "bounded research engineering and evidence-quality management",
        "foreseeable_uses": (
            "maintainer review",
            "public inspection of research methods",
        ),
        "foreseeable_misuses": (
            "treating engineering pass as scientific proof",
            "treating a research hypothesis as an established property of AI",
        ),
        "affected_individuals": ("maintainers", "external readers"),
        "affected_groups": ("research collaborators",),
        "societal_context": "public AI research communication under scientific uncertainty",
        "potential_benefit_refs": ("benefit:traceability", "benefit:false-positive-reduction"),
        "potential_harm_refs": ("harm:misinterpretation", "harm:false-confidence"),
        "human_oversight_refs": ("control:HUMAN_REVIEW_BOUNDARY",),
        "mitigation_refs": (
            "control:mandatory-nonclaims",
            "control:claim-ceiling-review",
        ),
        "mitigation_effectiveness_refs": (
            "test:mandatory-nonclaim-enforcement",
            "test:claim-ceiling-negative-paths",
        ),
        "linked_risk_ids": ("RISK-OVERCLAIM-001",),
        "residual_impact": Severity.MEDIUM,
        "residual_impact_basis_ref": "assessment:research-workflow-impact-residual-v1",
        "reassessment_triggers": (
            "deployment status changes",
            "intended-use changes",
            "new affected stakeholder group identified",
        ),
        "assessment_evidence_basis_refs": (
            "git:d9155e9fd6908b2880adc43e160ece70a1036cc7",
            "repo:quality-chain",
            "repo:subjectivity-protocol",
        ),
        "evidence_refs": ("repo:public-readme", "repo:subjectivity-protocol"),
        "disposition": AIImpactDisposition.ASSESSED_WITH_CONTROLS,
        "observed_impacts_claimed": False,
        "observed_impact_refs": (),
    }
    values.update(changes)
    return AIImpactAssessmentRecord(**values)


def test_bounded_risk_and_impact_records_reach_human_review_only() -> None:
    assessment = AIRiskImpactGate().assess(risks=(risk(),), impacts=(impact(),))

    assert assessment.disposition is AIRiskImpactDisposition.READY_FOR_HUMAN_REVIEW
    assert assessment.iso_conformance_claim == "NONE"
    assert assessment.certification_claim == "NONE"
    assert assessment.scientific_disposition == "HOLD"
    assert assessment.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert assessment.canonical_effect == "NONE"
    assert assessment.deployment_authority == "NONE"


def test_open_treatment_prevents_ready_disposition() -> None:
    open_risk = risk(
        disposition=AIRiskDisposition.TREATMENT_REQUIRED,
        residual_risk=Severity.HIGH,
        treatment_refs=("plan:add-independent-impact-review",),
    )

    assessment = AIRiskImpactGate().assess(risks=(open_risk,), impacts=(impact(),))

    assert assessment.disposition is AIRiskImpactDisposition.TREATMENT_OR_MITIGATION_REQUIRED
    assert "OPEN_RISK_TREATMENT_OR_IMPACT_MITIGATION" in assessment.reasons


def test_high_residual_risk_cannot_be_accepted() -> None:
    with pytest.raises(QualityError, match="high/critical residual risk"):
        risk(residual_risk=Severity.HIGH)


def test_high_residual_impact_cannot_be_assessed_as_controlled() -> None:
    with pytest.raises(QualityError, match="high/critical residual impact"):
        impact(residual_impact=Severity.CRITICAL)


def test_observed_impact_claim_requires_observation_references() -> None:
    with pytest.raises(QualityError, match="observed-impact claim flag"):
        impact(observed_impacts_claimed=True, observed_impact_refs=())


def test_observation_references_cannot_be_silently_added_to_potential_only_record() -> None:
    with pytest.raises(QualityError, match="observed-impact claim flag"):
        impact(observed_impacts_claimed=False, observed_impact_refs=("field:observation-1",))


def test_impact_must_link_only_to_registered_risks() -> None:
    with pytest.raises(QualityError, match="unknown risk identifiers"):
        AIRiskImpactGate().assess(
            risks=(risk(),),
            impacts=(impact(linked_risk_ids=("RISK-UNKNOWN",)),),
        )


def test_hold_record_fails_closed() -> None:
    held = replace(risk(), disposition=AIRiskDisposition.HOLD)
    assessment = AIRiskImpactGate().assess(risks=(held,), impacts=(impact(),))

    assert assessment.disposition is AIRiskImpactDisposition.HOLD
    assert "STRUCTURAL_OR_GOVERNANCE_HOLD_PRESENT" in assessment.reasons


def test_accepted_risk_requires_control_effectiveness_evidence() -> None:
    with pytest.raises(QualityError, match="control-effectiveness evidence"):
        risk(control_effectiveness_refs=())


def test_risk_evaluation_basis_is_mandatory() -> None:
    with pytest.raises(QualityError, match="risk_evaluation_basis_ref"):
        risk(risk_evaluation_basis_ref="")


def test_residual_risk_basis_is_mandatory() -> None:
    with pytest.raises(QualityError, match="residual_risk_basis_ref"):
        risk(residual_risk_basis_ref="")


def test_controlled_impact_requires_mitigation_effectiveness_evidence() -> None:
    with pytest.raises(QualityError, match="mitigation-effectiveness evidence"):
        impact(mitigation_effectiveness_refs=())


@pytest.mark.parametrize(
    "field",
    ("assessment_version", "exact_source_state_ref", "ai_system_context_ref", "residual_impact_basis_ref"),
)
def test_impact_assessment_state_and_basis_fields_are_mandatory(field: str) -> None:
    with pytest.raises(QualityError, match=field):
        impact(**{field: ""})


def test_impact_assessment_requires_evidence_basis_refs() -> None:
    with pytest.raises(QualityError, match="assessment_evidence_basis_refs"):
        impact(assessment_evidence_basis_refs=())
