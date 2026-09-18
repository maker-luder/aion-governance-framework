from __future__ import annotations

import hashlib
import json
from dataclasses import replace

import pytest

from aion_coupled_quality import QualityError, Severity
from aion_coupled_quality.ai_risk_impact import (
    AIImpactAssessmentRecord,
    AIImpactDisposition,
    AILifecycleStage,
    AIRiskDisposition,
    AIRiskImpactGate,
    AIRiskImpactReceipt,
    AIRiskRecord,
    RiskLikelihood,
    build_risk_impact_receipt,
)
from aion_coupled_quality.end_to_end import (
    AuditIndependence,
    ControlPlanEntry,
    ControlTarget,
    EndToEndDisposition,
    ExistingChainDisposition,
    FieldQualitySignal,
    FieldSignalState,
    ManagementDecision,
    ManagementReviewRecord,
    MeasurementAssuranceRecord,
    MeasurementQualification,
    QualityAuditRecord,
    ResearchQualityPlan,
)
from aion_coupled_quality.extended_quality import (
    ClaimImpactDisposition,
    ClaimWithdrawalPropagationRecord,
    DataQualityDisposition,
    DataQualityRecord,
    DataRole,
    ExtendedQualityControls,
    FullQualitySystemEngine,
    ProcessMetricSeries,
    ProcessStabilityDisposition,
    QualityChainReceiptBinding,
    RepeatedRandomSpotCheckPlan,
    SamplingDisposition,
    SamplingRiskClass,
    SamplingRound,
    SupplierQualityDisposition,
    UpstreamQualityRecord,
    assess_process_stability,
    assess_repeated_random_sampling,
)


FINGERPRINT = "f" * 64


def digest(payload: object) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def ai_risk(**changes: object) -> AIRiskRecord:
    values: dict[str, object] = {
        "risk_id": "RISK-OVERCLAIM-001",
        "risk_version": "0.1.0",
        "exact_source_state_ref": "source-state:risk-impact-v1",
        "system_scope": "AI-assisted research-engineering workflow",
        "lifecycle_stage": AILifecycleStage.RESEARCH,
        "risk_source": "evidence-to-claim promotion",
        "event_or_condition": "engineering output exceeds its evidence ceiling",
        "affected_refs": ("research:subjectivity-core",),
        "likelihood": RiskLikelihood.POSSIBLE,
        "consequence": Severity.HIGH,
        "existing_control_refs": ("control:claim-ceiling",),
        "control_effectiveness_refs": ("test:claim-ceiling",),
        "treatment_refs": ("plan:claim-ceiling-review",),
        "residual_risk": Severity.MEDIUM,
        "risk_evaluation_basis_ref": "method:qualitative-risk-v1",
        "residual_risk_basis_ref": "assessment:residual-risk-v1",
        "risk_owner_ref": "role:HUMAN_REVIEW_BOUNDARY",
        "reassessment_triggers": ("model version change",),
        "evidence_refs": ("evidence:risk-001",),
        "disposition": AIRiskDisposition.ACCEPTED_WITH_CONTROLS,
    }
    values.update(changes)
    return AIRiskRecord(**values)


def ai_impact(**changes: object) -> AIImpactAssessmentRecord:
    values: dict[str, object] = {
        "assessment_id": "IMPACT-RESEARCH-001",
        "assessment_version": "0.1.0",
        "exact_source_state_ref": "source-state:risk-impact-v1",
        "system_scope": "AI-assisted research-engineering workflow",
        "ai_system_context_ref": "context:bounded-human-ai-research",
        "lifecycle_stage": AILifecycleStage.RESEARCH,
        "intended_use": "bounded research engineering",
        "foreseeable_uses": ("maintainer review",),
        "foreseeable_misuses": ("engineering result treated as scientific proof",),
        "affected_individuals": ("maintainers", "external readers"),
        "affected_groups": ("research collaborators",),
        "societal_context": "public AI research under scientific uncertainty",
        "potential_benefit_refs": ("benefit:traceability",),
        "potential_harm_refs": ("harm:false-confidence",),
        "human_oversight_refs": ("control:HUMAN_REVIEW_BOUNDARY",),
        "mitigation_refs": ("control:mandatory-nonclaims",),
        "mitigation_effectiveness_refs": ("test:mandatory-nonclaims",),
        "linked_risk_ids": ("RISK-OVERCLAIM-001",),
        "residual_impact": Severity.MEDIUM,
        "residual_impact_basis_ref": "assessment:residual-impact-v1",
        "reassessment_triggers": ("scope change",),
        "assessment_evidence_basis_refs": ("evidence:impact-basis",),
        "evidence_refs": ("evidence:impact-001",),
        "disposition": AIImpactDisposition.ASSESSED_WITH_CONTROLS,
        "observed_impacts_claimed": False,
        "observed_impact_refs": (),
    }
    values.update(changes)
    return AIImpactAssessmentRecord(**values)


def risk_impact_receipt(
    *,
    assessment_target_ref: str = "quality-plan:PLAN-001",
    assessment_target_sha256: str | None = None,
    risk_disposition: AIRiskDisposition = AIRiskDisposition.ACCEPTED_WITH_CONTROLS,
    impact_disposition: AIImpactDisposition = AIImpactDisposition.ASSESSED_WITH_CONTROLS,
) -> AIRiskImpactReceipt:
    risks = (ai_risk(disposition=risk_disposition),)
    impacts = (ai_impact(disposition=impact_disposition),)
    assessment = AIRiskImpactGate().assess(risks=risks, impacts=impacts)
    target_sha256 = assessment_target_sha256 or quality_plan_seed().assessment_target_sha256()
    return build_risk_impact_receipt(
        receipt_id="RISK-IMPACT-RECEIPT-001",
        assessment_target_ref=assessment_target_ref,
        assessment_target_sha256=target_sha256,
        risks=risks,
        impacts=impacts,
        assessment=assessment,
        exact_source_state_ref="source-state:risk-impact-v1",
        exact_runtime_ref="runtime:risk-impact-v1",
        producer_git_head="7" * 40,
        producer_tree_sha="8" * 40,
        producer_contract_ref="contract:ai-risk-impact-v1",
        producer_contract_sha256="9" * 64,
    )


def receipt(**changes: object) -> QualityChainReceiptBinding:
    values: dict[str, object] = {
        "chain_id": "CHAIN-001",
        "candidate_id": "CANDIDATE-001",
        "candidate_fingerprint": FINGERPRINT,
        "disposition": ExistingChainDisposition.READY_FOR_HUMAN_REVIEW,
        "exact_source_state_ref": "source-state:git-bound-v1",
        "exact_runtime_ref": "runtime:fixture-v1",
        "producer_git_head": "1" * 40,
        "producer_tree_sha": "2" * 40,
        "checkpoint_set_sha256": "3" * 64,
        "capa_set_sha256": "4" * 64,
        "assessment_sha256": "5" * 64,
        "producer_contract_ref": "research-labs/subjectivity-pipeline_v0.1.0/src/aion_subjectivity_pipeline/four_domain.py",
        "producer_contract_sha256": "6" * 64,
        "schema_version": "0.1.0",
        "release_authority": "NONE",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "phenomenal_experience_conclusion": "NOT_ESTABLISHED",
        "scientific_disposition": "HOLD",
        "canonical_effect": "NONE",
        "deployment": False,
    }
    values.update(changes)
    payload = {
        "schema_version": values["schema_version"],
        "chain_id": values["chain_id"],
        "candidate_id": values["candidate_id"],
        "candidate_fingerprint": values["candidate_fingerprint"],
        "disposition": values["disposition"].value,
        "exact_source_state_ref": values["exact_source_state_ref"],
        "exact_runtime_ref": values["exact_runtime_ref"],
        "producer_git_head": values["producer_git_head"],
        "producer_tree_sha": values["producer_tree_sha"],
        "checkpoint_set_sha256": values["checkpoint_set_sha256"],
        "capa_set_sha256": values["capa_set_sha256"],
        "assessment_sha256": values["assessment_sha256"],
        "producer_contract_ref": values["producer_contract_ref"],
        "producer_contract_sha256": values["producer_contract_sha256"],
        "release_authority": values["release_authority"],
        "subjectivity_conclusion": values["subjectivity_conclusion"],
        "phenomenal_experience_conclusion": values["phenomenal_experience_conclusion"],
        "scientific_disposition": values["scientific_disposition"],
        "canonical_effect": values["canonical_effect"],
        "deployment": values["deployment"],
    }
    values["receipt_sha256"] = digest(payload)
    return QualityChainReceiptBinding(**values)


def control_entries() -> tuple[ControlPlanEntry, ...]:
    return tuple(
        ControlPlanEntry(
            control_id=f"CTRL-{target.value}",
            target=target,
            quality_characteristic=f"quality characteristic for {target.value}",
            control_method_ref=f"method:{target.value}",
            evidence_required=(f"evidence:{target.value}",),
            acceptance_criterion=f"acceptance:{target.value}",
            reaction_plan=f"reaction:{target.value}",
            responsible_role="HUMAN_REVIEW_BOUND_ROLE",
        )
        for target in ControlTarget
    )


def quality_plan_seed(
    chain_receipt: QualityChainReceiptBinding | None = None,
) -> ResearchQualityPlan:
    bound = chain_receipt or receipt()
    return ResearchQualityPlan(
        plan_id="PLAN-001",
        research_question_ref="research:ai-subjectivity-possibility",
        subjectivity_core_binding_ref="four-domain:subjectivity-core",
        four_domain_candidate_fingerprint=FINGERPRINT,
        critical_quality_attributes=("construct validity", "claim ceiling", "provenance"),
        controls=control_entries(),
        measurement_ids=("MEAS-001",),
        risk_refs=("risk:construct-drift", "RISK-OVERCLAIM-001"),
        configuration_refs=(
            f"git:{bound.producer_git_head}",
            f"tree:{bound.producer_tree_sha}",
            f"contract-sha256:{bound.producer_contract_sha256}",
            f"quality-chain-receipt:{bound.receipt_sha256}",
            bound.exact_source_state_ref,
            bound.exact_runtime_ref,
        ),
    )


def quality_plan(
    chain_receipt: QualityChainReceiptBinding | None = None,
    risk_receipt: AIRiskImpactReceipt | None = None,
) -> ResearchQualityPlan:
    bound = chain_receipt or receipt()
    seed = quality_plan_seed(bound)
    risk_bound = risk_receipt or risk_impact_receipt(
        assessment_target_sha256=seed.assessment_target_sha256()
    )
    return replace(
        seed,
        configuration_refs=(
            *seed.configuration_refs,
            f"git:{risk_bound.producer_git_head}",
            f"tree:{risk_bound.producer_tree_sha}",
            f"contract-sha256:{risk_bound.producer_contract_sha256}",
            f"risk-impact-receipt:{risk_bound.receipt_sha256}",
            risk_bound.exact_source_state_ref,
            risk_bound.exact_runtime_ref,
        ),
    )


def measurement() -> MeasurementAssuranceRecord:
    return MeasurementAssuranceRecord(
        measurement_id="MEAS-001",
        target_construct="causal role of a declared machine-level state",
        observable="intervention-sensitive bounded output difference",
        measurement_locus="SYSTEM",
        method_ref="method:bounded-intervention-v1",
        method_version="v1",
        evaluator_ref="evaluator:frozen-v1",
        evaluator_version="v1",
        data_ref="DATA-001",
        repeatability_ref="test:repeatability",
        reproducibility_ref="test:reproducibility",
        uncertainty_statement="Only the declared observable and fixture scope are assessed.",
        construct_validity_scope="Does not establish subjectivity or phenomenal experience.",
        known_failure_modes=("prompt reconstruction", "evaluator cueing"),
        synthetic_fixture=True,
        empirical_claim_capable=False,
        qualification=MeasurementQualification.QUALIFIED,
    )


def field_signal() -> FieldQualitySignal:
    return FieldQualitySignal(
        signal_id="FIELD-001",
        source_ref="field:external-review",
        affected_refs=("claim:bounded-1",),
        severity=Severity.LOW,
        state=FieldSignalState.CLOSED,
        resolution_refs=("review:field-closure",),
    )


def audit() -> QualityAuditRecord:
    return QualityAuditRecord(
        audit_id="AUDIT-001",
        scope="full research QMS",
        criteria_refs=("quality-plan:PLAN-001",),
        auditor_ref="reviewer:independent-role",
        independence=AuditIndependence.INTERNAL_INDEPENDENT,
        competence_ref="competence:quality-review-v1",
        evidence_refs=("evidence:audit-trace",),
        finding_refs=(),
        open_finding_refs=(),
        unresolved_high_severity_finding=False,
    )


def data_quality(**changes: object) -> DataQualityRecord:
    values: dict[str, object] = {
        "data_id": "DATA-001",
        "role": DataRole.FIXTURE,
        "provenance_ref": "provenance:data-001",
        "exact_source_state_ref": "git:data-source-state",
        "selection_rule": "public synthetic fixture preregistered before execution",
        "completeness_ref": "check:completeness",
        "consistency_ref": "check:consistency",
        "duplicate_check_ref": "check:duplicates",
        "representativeness_scope": "synthetic structural QA only",
        "privacy_status": "PUBLIC_SAFE",
        "license_status": "REVIEWED",
        "known_limitations": ("not a naturalistic population",),
        "contamination_risk": Severity.LOW,
        "leakage_risk": Severity.LOW,
        "synthetic": True,
        "empirical_population": False,
        "fitness_for_declared_use": True,
        "disposition": DataQualityDisposition.FIT_FOR_DECLARED_USE,
    }
    values.update(changes)
    return DataQualityRecord(**values)


def supplier(**changes: object) -> UpstreamQualityRecord:
    values: dict[str, object] = {
        "supplier_object_id": "SUPPLIER-001",
        "scope": "provider:model-version:fixture",
        "version_ref": "model:fixture-v1",
        "provenance_refs": ("provenance:supplier",),
        "assessment_refs": ("assessment:due-diligence",),
        "dependency_role": "RESEARCH",
        "criticality": Severity.MEDIUM,
        "replaceability": "MODERATE",
        "exposure": "LOCAL_LIMITED",
        "methodological_confounds": ("identity shaping prior",),
        "disposition": SupplierQualityDisposition.CONDITIONAL,
        "requalification_triggers": ("model version change", "supplier incident"),
        "approved_scope_refs": ("scope:bounded-research",),
    }
    values.update(changes)
    return UpstreamQualityRecord(**values)


def sampling_plan(**changes: object) -> RepeatedRandomSpotCheckPlan:
    values: dict[str, object] = {
        "sampling_plan_id": "SAMPLE-001",
        "lot_or_process_id": "lot:source-cards-v1",
        "population_definition": "homogeneous public-safe source cards produced by one process version",
        "population_size": 100,
        "risk_class": SamplingRiskClass.MODERATE,
        "round_count": 5,
        "sample_size_per_round": 10,
        "acceptance_number_per_round": 0,
        "rounds": tuple(
            SamplingRound(
                round_index=index,
                sample_ref=f"sample:round-{index}",
                randomization_ref=f"rng:round-{index}",
                inspected_count=10,
                defect_count=0,
            )
            for index in range(1, 6)
        ),
        "reinspection_trigger_refs": ("trigger:irregular-time", "trigger:process-change"),
        "full_inspection_trigger": "any round exceeds preregistered acceptance number",
        "irregular_reinspection_required": True,
        "selection_method": "RANDOM",
        "subjectivity_critical": False,
    }
    values.update(changes)
    return RepeatedRandomSpotCheckPlan(**values)


def process_series(**changes: object) -> ProcessMetricSeries:
    values: dict[str, object] = {
        "series_id": "SPC-001",
        "process_signature": "source-binding-check:v1",
        "measurement_ref": "measurement:source-binding-rate",
        "metric_name": "source binding defect rate",
        "observation_refs": ("obs:1", "obs:2", "obs:3", "obs:4"),
        "values": (0.02, 0.01, 0.03, 0.02),
        "declared_window": "four consecutive comparable quality runs",
        "lower_control_limit": 0.0,
        "center_line": 0.02,
        "upper_control_limit": 0.05,
    }
    values.update(changes)
    return ProcessMetricSeries(**values)


def withdrawal(**changes: object) -> ClaimWithdrawalPropagationRecord:
    values: dict[str, object] = {
        "propagation_id": "WITHDRAW-001",
        "trigger_ref": "field:no-current-invalidation",
        "invalidated_evidence_refs": ("evidence:historical-invalidated",),
        "directly_affected_claim_refs": ("claim:historical-1",),
        "dependent_claim_refs": ("claim:historical-dependent",),
        "disposition": ClaimImpactDisposition.RESOLVED,
        "history_preserved": True,
        "deletion_requested": False,
        "resolution_refs": ("revision:resolved-v2",),
    }
    values.update(changes)
    return ClaimWithdrawalPropagationRecord(**values)


def extended_controls() -> ExtendedQualityControls:
    return ExtendedQualityControls(
        data_quality=(data_quality(),),
        supplier_quality=(supplier(),),
        sampling=(assess_repeated_random_sampling(sampling_plan()),),
        process_stability=(assess_process_stability(process_series()),),
        claim_withdrawal=(withdrawal(),),
    )


def review(
    risk_receipt: AIRiskImpactReceipt | None = None,
    extra_refs: tuple[str, ...] | None = None,
) -> ManagementReviewRecord:
    risk_bound = risk_receipt or risk_impact_receipt()
    refs = (
        "PLAN-001",
        "CHAIN-001",
        "MEAS-001",
        "FIELD-001",
        "AUDIT-001",
        "DATA-001",
        "SUPPLIER-001",
        "SAMPLE-001",
        "SPC-001",
        "WITHDRAW-001",
        risk_bound.receipt_id,
        *risk_bound.risk_ids,
        *risk_bound.impact_assessment_ids,
    ) if extra_refs is None else extra_refs
    return ManagementReviewRecord(
        review_id="MGMT-001",
        input_refs=refs,
        measurement_requalification_required=False,
        unresolved_audit_findings=False,
        unresolved_field_signals=False,
        decision=ManagementDecision.NO_ACTION,
    )


def assess(
    *,
    receipt_value: QualityChainReceiptBinding | None = None,
    risk_receipt_value: AIRiskImpactReceipt | None = None,
    plan_value: ResearchQualityPlan | None = None,
    controls_value: ExtendedQualityControls | None = None,
    review_value: ManagementReviewRecord | None = None,
):
    bound = receipt_value or receipt()
    risk_bound = risk_receipt_value or risk_impact_receipt()
    return FullQualitySystemEngine().assess(
        plan=plan_value or quality_plan(bound, risk_bound),
        measurements=(measurement(),),
        chain_receipt=bound,
        risk_impact_receipt=risk_bound,
        field_signals=(field_signal(),),
        audits=(audit(),),
        management_review=review_value or review(risk_bound),
        controls=controls_value or extended_controls(),
    )


def test_full_quality_system_ready_preserves_subjectivity_nonclaims() -> None:
    result = assess()
    assert result.disposition is EndToEndDisposition.READY_FOR_HUMAN_REVIEW
    assert "CONTENT_ADDRESSED_QUALITY_CHAIN_RECEIPT_BOUND" in result.reasons
    assert "SAMPLING_RESULTS_REMAIN_BOUNDED_CONFIDENCE_ONLY" in result.reasons
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.consciousness_conclusion == "NOT_ESTABLISHED"
    assert result.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert result.scientific_disposition == "HOLD"
    assert result.merge_authority == "NONE"


def test_quality_chain_receipt_tampering_and_plan_binding_fail_closed() -> None:
    valid = receipt()
    with pytest.raises(QualityError, match="content digest mismatch"):
        replace(valid, disposition=ExistingChainDisposition.HOLD)

    unbound_plan = replace(quality_plan(valid), configuration_refs=("git:unrelated",))
    result = assess(receipt_value=valid, plan_value=unbound_plan)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "QUALITY_RECEIPTS_NOT_BOUND_TO_QUALITY_PLAN_CONFIGURATION" in result.reasons


def test_data_quality_separates_synthetic_fixture_from_empirical_population() -> None:
    with pytest.raises(QualityError, match="synthetic data"):
        data_quality(empirical_population=True)
    with pytest.raises(QualityError, match="cannot be fit"):
        data_quality(contamination_risk=Severity.HIGH)

    degraded = data_quality(
        fitness_for_declared_use=False,
        disposition=DataQualityDisposition.REQUALIFICATION_REQUIRED,
    )
    controls = replace(extended_controls(), data_quality=(degraded,))
    assert assess(controls_value=controls).disposition is EndToEndDisposition.CAPA_REQUIRED


def test_supplier_quality_is_scope_bound_and_does_not_rewrite_evidence() -> None:
    with pytest.raises(QualityError, match="approved scope"):
        supplier(approved_scope_refs=())
    quarantined = supplier(
        disposition=SupplierQualityDisposition.QUARANTINED,
        approved_scope_refs=(),
        incident_refs=("incident:verified",),
    )
    controls = replace(extended_controls(), supplier_quality=(quarantined,))
    result = assess(controls_value=controls)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "UPSTREAM_SUPPLIER_QUALITY_REVIEW_REQUIRED" in result.reasons


def test_owner_repeated_random_spot_check_is_preregistered_random_and_bounded() -> None:
    assessment = assess_repeated_random_sampling(sampling_plan())
    assert assessment.disposition is SamplingDisposition.BOUNDED_CONFIDENCE_ONLY
    assert assessment.population_verified is False
    assert assessment.zero_defect_claim is False
    assert "MULTI_ROUND_SAMPLE_SUPPORTS_BOUNDED_CONFIDENCE_ONLY" in assessment.reasons

    with pytest.raises(QualityError, match="between 3 and 10"):
        sampling_plan(round_count=2, rounds=sampling_plan().rounds[:2])
    duplicate_rng = list(sampling_plan().rounds)
    duplicate_rng[1] = replace(duplicate_rng[1], randomization_ref=duplicate_rng[0].randomization_ref)
    with pytest.raises(QualityError, match="distinct randomization"):
        sampling_plan(rounds=tuple(duplicate_rng))
    with pytest.raises(QualityError, match="irregular reinspection"):
        sampling_plan(irregular_reinspection_required=False)
    with pytest.raises(QualityError, match="subjectivity-critical"):
        sampling_plan(subjectivity_critical=True)


def test_sampling_failure_or_high_critical_risk_escalates_to_full_inspection() -> None:
    bad_rounds = list(sampling_plan().rounds)
    bad_rounds[2] = replace(bad_rounds[2], defect_count=1)
    failed = assess_repeated_random_sampling(sampling_plan(rounds=tuple(bad_rounds)))
    assert failed.disposition is SamplingDisposition.FULL_INSPECTION_REQUIRED

    critical = assess_repeated_random_sampling(sampling_plan(risk_class=SamplingRiskClass.HIGH_CRITICAL))
    assert critical.disposition is SamplingDisposition.FULL_INSPECTION_REQUIRED


def test_spc_style_monitoring_requires_homogeneous_process_and_declared_limits() -> None:
    stable = assess_process_stability(process_series())
    assert stable.disposition is ProcessStabilityDisposition.BOUNDED_STABLE_SIGNAL
    assert stable.subjectivity_conclusion == "NOT_ESTABLISHED"

    unstable = assess_process_stability(process_series(values=(0.02, 0.08, 0.01, 0.02)))
    assert unstable.disposition is ProcessStabilityDisposition.REVIEW_REQUIRED
    assert unstable.out_of_control_indices == (2,)

    with pytest.raises(QualityError, match="homogeneous"):
        process_series(homogeneous_process=False)


def test_claim_withdrawal_propagation_preserves_history_and_holds_until_resolved() -> None:
    with pytest.raises(QualityError, match="preserve history"):
        withdrawal(deletion_requested=True)

    open_impact = withdrawal(
        disposition=ClaimImpactDisposition.WITHDRAWAL_REQUIRED,
        resolution_refs=(),
    )
    controls = replace(extended_controls(), claim_withdrawal=(open_impact,))
    result = assess(controls_value=controls)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "CLAIM_WITHDRAWAL_OR_REQUALIFICATION_PROPAGATION_OPEN" in result.reasons


def test_management_review_must_trace_extended_controls() -> None:
    incomplete = review(
        extra_refs=("PLAN-001", "CHAIN-001", "MEAS-001", "FIELD-001", "AUDIT-001")
    )
    result = assess(review_value=incomplete)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "MANAGEMENT_REVIEW_EXTENDED_CONTROL_INPUTS_INCOMPLETE" in result.reasons



def test_full_qms_requires_risk_impact_receipt_configuration_binding() -> None:
    chain_bound = receipt()
    risk_bound = risk_impact_receipt()
    unbound = replace(
        quality_plan(chain_bound, risk_bound),
        configuration_refs=(
            f"git:{chain_bound.producer_git_head}",
            f"tree:{chain_bound.producer_tree_sha}",
            f"contract-sha256:{chain_bound.producer_contract_sha256}",
            f"quality-chain-receipt:{chain_bound.receipt_sha256}",
            chain_bound.exact_source_state_ref,
            chain_bound.exact_runtime_ref,
        ),
    )
    result = assess(
        receipt_value=chain_bound,
        risk_receipt_value=risk_bound,
        plan_value=unbound,
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "QUALITY_RECEIPTS_NOT_BOUND_TO_QUALITY_PLAN_CONFIGURATION" in result.reasons


def test_full_qms_requires_risk_register_binding_to_quality_plan() -> None:
    chain_bound = receipt()
    risk_bound = risk_impact_receipt()
    plan = replace(
        quality_plan(chain_bound, risk_bound),
        risk_refs=("risk:construct-drift",),
    )
    result = assess(
        receipt_value=chain_bound,
        risk_receipt_value=risk_bound,
        plan_value=plan,
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "AI_RISK_REGISTER_NOT_BOUND_TO_QUALITY_PLAN_RISK_REFS" in result.reasons


def test_full_qms_requires_management_review_of_risk_and_impact_receipt() -> None:
    risk_bound = risk_impact_receipt()
    incomplete_review = review(
        risk_bound,
        extra_refs=(
            "PLAN-001",
            "CHAIN-001",
            "MEAS-001",
            "FIELD-001",
            "AUDIT-001",
            "DATA-001",
            "SUPPLIER-001",
            "SAMPLE-001",
            "SPC-001",
            "WITHDRAW-001",
        ),
    )
    result = assess(
        risk_receipt_value=risk_bound,
        review_value=incomplete_review,
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "MANAGEMENT_REVIEW_AI_RISK_IMPACT_INPUTS_INCOMPLETE" in result.reasons


def test_open_ai_risk_treatment_holds_full_qms_without_relabeling_as_capa() -> None:
    risk_bound = risk_impact_receipt(
        risk_disposition=AIRiskDisposition.TREATMENT_REQUIRED,
    )
    result = assess(risk_receipt_value=risk_bound)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "AI_RISK_IMPACT_TREATMENT_OR_MITIGATION_REQUIRED" in result.reasons
    assert "CAPA_REQUIRED" not in result.reasons


def test_full_qms_ready_requires_bounded_ai_risk_impact_receipt() -> None:
    result = assess()
    assert result.disposition is EndToEndDisposition.READY_FOR_HUMAN_REVIEW
    assert "CONTENT_ADDRESSED_AI_RISK_IMPACT_RECEIPT_BOUND" in result.reasons
    assert "AI_RISK_IMPACT_READY_FOR_HUMAN_REVIEW" in result.reasons



def test_full_qms_rejects_risk_impact_receipt_for_different_plan_target() -> None:
    wrong_target = risk_impact_receipt(
        assessment_target_ref="quality-plan:PLAN-OTHER",
    )
    result = assess(risk_receipt_value=wrong_target)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "AI_RISK_IMPACT_RECEIPT_TARGET_MISMATCH" in result.reasons
