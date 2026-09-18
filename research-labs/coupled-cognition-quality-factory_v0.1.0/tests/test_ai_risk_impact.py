from __future__ import annotations

from dataclasses import replace
import hashlib
from pathlib import Path
import subprocess

import pytest

from aion_coupled_quality import QualityError, Severity
from aion_coupled_quality.ai_risk_impact import (
    AIImpactAssessmentRecord,
    AIImpactDisposition,
    AILifecycleStage,
    AIRiskDisposition,
    AIRiskImpactDisposition,
    AIRiskImpactGate,
    AIRiskImpactReceipt,
    AIRiskRecord,
    RiskLikelihood,
    build_repository_bound_risk_impact_receipt,
    build_risk_impact_receipt,
)


def risk(**changes: object) -> AIRiskRecord:
    values: dict[str, object] = {
        "risk_id": "RISK-OVERCLAIM-001",
        "risk_version": "0.1.0",
        "exact_source_state_ref": "git:d9155e9fd6908b2880adc43e160ece70a1036cc7",
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


def test_risk_version_and_source_state_are_mandatory() -> None:
    with pytest.raises(QualityError, match="risk_version"):
        risk(risk_version="")
    with pytest.raises(QualityError, match="exact_source_state_ref"):
        risk(exact_source_state_ref="")


def _receipt(**changes: object) -> AIRiskImpactReceipt:
    risks = changes.pop("risks", (risk(),))
    impacts = changes.pop("impacts", (impact(),))
    assert isinstance(risks, tuple)
    assert isinstance(impacts, tuple)
    assessment = AIRiskImpactGate().assess(risks=risks, impacts=impacts)
    values: dict[str, object] = {
        "receipt_id": "RISK-IMPACT-RECEIPT-001",
        "risks": risks,
        "impacts": impacts,
        "assessment": assessment,
        "exact_source_state_ref": "git:d9155e9fd6908b2880adc43e160ece70a1036cc7",
        "exact_runtime_ref": "runtime:receipt-builder-v1",
        "producer_git_head": "1" * 40,
        "producer_tree_sha": "2" * 40,
        "producer_contract_ref": "contract:ai-risk-impact-v0.1.0",
        "producer_contract_sha256": "3" * 64,
    }
    values.update(changes)
    return build_risk_impact_receipt(**values)


def test_risk_impact_receipt_is_content_addressed_and_non_authoritative() -> None:
    receipt = _receipt()

    assert receipt.risk_ids == ("RISK-OVERCLAIM-001",)
    assert receipt.impact_assessment_ids == ("IMPACT-RESEARCH-001",)
    assert len(receipt.risk_set_sha256) == 64
    assert len(receipt.impact_set_sha256) == 64
    assert len(receipt.assessment_sha256) == 64
    assert len(receipt.receipt_sha256) == 64
    assert receipt.iso_conformance_claim == "NONE"
    assert receipt.certification_claim == "NONE"
    assert receipt.scientific_disposition == "HOLD"
    assert receipt.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert receipt.disposition is AIRiskImpactDisposition.READY_FOR_HUMAN_REVIEW
    assert receipt.canonical_effect == "NONE"
    assert receipt.deployment_authority == "NONE"


def test_receipt_rejects_risk_source_state_drift() -> None:
    with pytest.raises(QualityError, match="risk record source state"):
        _receipt(risks=(risk(exact_source_state_ref="git:other-head"),))


def test_receipt_rejects_impact_source_state_drift() -> None:
    with pytest.raises(QualityError, match="impact assessment source state"):
        _receipt(impacts=(impact(exact_source_state_ref="git:other-head"),))


def test_receipt_digest_detects_tampering() -> None:
    receipt = _receipt()
    with pytest.raises(QualityError, match="content digest mismatch"):
        replace(receipt, receipt_sha256="0" * 64)


def test_receipt_changes_when_bound_risk_content_changes() -> None:
    first = _receipt()
    changed_risk = risk(
        risk_version="0.1.1",
        residual_risk_basis_ref="assessment:overclaim-residual-v2",
    )
    second = _receipt(risks=(changed_risk,))

    assert first.risk_set_sha256 != second.risk_set_sha256
    assert first.receipt_sha256 != second.receipt_sha256


def test_receipt_rejects_assessment_from_different_inputs() -> None:
    risks = (risk(),)
    impacts = (impact(),)
    wrong_assessment = AIRiskImpactGate().assess(
        risks=(risk(risk_id="RISK-OTHER"),),
        impacts=(impact(linked_risk_ids=("RISK-OTHER",)),),
    )
    with pytest.raises(QualityError, match="recomputed gate assessment"):
        build_risk_impact_receipt(
            receipt_id="RISK-IMPACT-RECEIPT-002",
            risks=risks,
            impacts=impacts,
            assessment=wrong_assessment,
            exact_source_state_ref="git:d9155e9fd6908b2880adc43e160ece70a1036cc7",
            exact_runtime_ref="runtime:receipt-builder-v1",
            producer_git_head="1" * 40,
            producer_tree_sha="2" * 40,
            producer_contract_ref="contract:ai-risk-impact-v0.1.0",
            producer_contract_sha256="3" * 64,
        )


def test_receipt_runtime_binding_is_mandatory() -> None:
    with pytest.raises(QualityError, match="exact_runtime_ref"):
        _receipt(exact_runtime_ref="")



def test_receipt_recomputes_gate_assessment_before_emission() -> None:
    risks = (risk(),)
    impacts = (impact(),)
    forged = replace(
        AIRiskImpactGate().assess(risks=risks, impacts=impacts),
        disposition=AIRiskImpactDisposition.HOLD,
    )
    with pytest.raises(QualityError, match="recomputed gate assessment"):
        build_risk_impact_receipt(
            receipt_id="RISK-IMPACT-RECEIPT-FORGED",
            risks=risks,
            impacts=impacts,
            assessment=forged,
            exact_source_state_ref="git:d9155e9fd6908b2880adc43e160ece70a1036cc7",
            exact_runtime_ref="runtime:receipt-builder-v1",
            producer_git_head="1" * 40,
            producer_tree_sha="2" * 40,
            producer_contract_ref="contract:ai-risk-impact-v0.1.0",
            producer_contract_sha256="3" * 64,
        )


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args],
        text=True,
        encoding="utf-8",
    ).strip()


def _repository_fixture(tmp_path: Path) -> tuple[Path, str, bytes]:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.name", "Risk Impact Receipt Fixture")
    _git(root, "config", "user.email", "fixture@example.invalid")
    contract_ref = "contracts/ai_risk_impact.py"
    contract_path = root / contract_ref
    contract_path.parent.mkdir(parents=True)
    committed_bytes = b"RISK_IMPACT_CONTRACT = True\n"
    contract_path.write_bytes(committed_bytes)
    _git(root, "add", contract_ref)
    _git(root, "commit", "-qm", "fixture risk impact contract")
    return root, contract_ref, committed_bytes


def test_repository_bound_receipt_uses_committed_git_objects(tmp_path: Path) -> None:
    root, contract_ref, committed_bytes = _repository_fixture(tmp_path)
    risks = (risk(),)
    impacts = (impact(),)
    assessment = AIRiskImpactGate().assess(risks=risks, impacts=impacts)

    receipt = build_repository_bound_risk_impact_receipt(
        receipt_id="RISK-IMPACT-RECEIPT-GIT",
        risks=risks,
        impacts=impacts,
        assessment=assessment,
        exact_source_state_ref="git:d9155e9fd6908b2880adc43e160ece70a1036cc7",
        exact_runtime_ref="runtime:receipt-builder-v1",
        repository_root=root,
        producer_contract_ref=contract_ref,
    )
    assert receipt.producer_git_head == _git(root, "rev-parse", "HEAD")
    assert receipt.producer_tree_sha == _git(root, "rev-parse", "HEAD^{tree}")
    assert receipt.producer_contract_sha256 == hashlib.sha256(committed_bytes).hexdigest()

    (root / contract_ref).write_text("RISK_IMPACT_CONTRACT = False\n", encoding="utf-8")
    dirty_receipt = build_repository_bound_risk_impact_receipt(
        receipt_id="RISK-IMPACT-RECEIPT-GIT-DIRTY",
        risks=risks,
        impacts=impacts,
        assessment=assessment,
        exact_source_state_ref="git:d9155e9fd6908b2880adc43e160ece70a1036cc7",
        exact_runtime_ref="runtime:receipt-builder-v1",
        repository_root=root,
        producer_contract_ref=contract_ref,
    )
    assert dirty_receipt.producer_contract_sha256 == hashlib.sha256(committed_bytes).hexdigest()
    assert dirty_receipt.producer_tree_sha == receipt.producer_tree_sha


def test_repository_bound_receipt_rejects_unsafe_producer_paths(tmp_path: Path) -> None:
    root, contract_ref, _ = _repository_fixture(tmp_path)
    nested = root / "nested"
    nested.mkdir()
    risks = (risk(),)
    impacts = (impact(),)
    assessment = AIRiskImpactGate().assess(risks=risks, impacts=impacts)

    with pytest.raises(QualityError, match="exact Git top-level"):
        build_repository_bound_risk_impact_receipt(
            receipt_id="RISK-IMPACT-RECEIPT-NESTED",
            risks=risks,
            impacts=impacts,
            assessment=assessment,
            exact_source_state_ref="git:d9155e9fd6908b2880adc43e160ece70a1036cc7",
            exact_runtime_ref="runtime:receipt-builder-v1",
            repository_root=nested,
            producer_contract_ref=contract_ref,
        )

    with pytest.raises(QualityError, match="safe repository-relative"):
        build_repository_bound_risk_impact_receipt(
            receipt_id="RISK-IMPACT-RECEIPT-UNSAFE",
            risks=risks,
            impacts=impacts,
            assessment=assessment,
            exact_source_state_ref="git:d9155e9fd6908b2880adc43e160ece70a1036cc7",
            exact_runtime_ref="runtime:receipt-builder-v1",
            repository_root=root,
            producer_contract_ref="../outside.py",
        )
