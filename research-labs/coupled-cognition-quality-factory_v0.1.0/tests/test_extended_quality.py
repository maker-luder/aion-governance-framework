from __future__ import annotations

import hashlib
import json
from dataclasses import replace

import pytest

from aion_ai_security_profile import (
    AIAdversarialSecurityGate,
    AIAdversaryModel,
    AISecurityProfileDisposition,
    AISecurityProfileReceipt,
    AISecurityTestSpec,
    AISecurityThreatApplicability,
    AISecurityThreatClass,
    AISecurityThreatRecord,
    AttackerKnowledge,
    build_ai_adversarial_security_profile,
    build_ai_security_profile_receipt,
)
from aion_ai_tevv import (
    AITEVVProfileGate,
    AISystemBinding,
    EvaluatorIndependence,
    HumanSubjectsStatus,
    OracleStrategy,
    TEVVActivity,
    TEVVLifecycleStage,
    TEVVCaseSpec,
    TEVVMetricMeasurementBinding,
    TEVVMetricSpec,
    TEVVProfileDisposition,
    TEVVProfileReceipt,
    TEVVTestApproach,
    build_tevv_profile,
    build_tevv_profile_receipt,
)
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
    risk_id: str = "RISK-OVERCLAIM-001",
) -> AIRiskImpactReceipt:
    risks = (
        ai_risk(
            risk_id=risk_id,
            disposition=risk_disposition,
        ),
    )
    impacts = (
        ai_impact(
            linked_risk_ids=(risk_id,),
            disposition=impact_disposition,
        ),
    )
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


def tevv_profile(
    *,
    evaluator_independence: EvaluatorIndependence = EvaluatorIndependence.INTERNAL_INDEPENDENT,
):
    return build_tevv_profile(
        profile_id="TEVV-PROFILE-001",
        profile_version="0.1.0",
        objective_ref="objective:qms-bound-structural-tevv",
        intended_use_ref="use:research-engineering-only",
        tevv_vocabulary_ref="subjectivity-pipeline:TevvDefinition:v0.1.0",
        tevv_vocabulary_sha256="a" * 64,
        lifecycle_stage=TEVVLifecycleStage.RESEARCH,
        risk_refs=("RISK-OVERCLAIM-001",),
        unmeasured_risks=(),
        activities=(TEVVActivity.TEST,),
        system=AISystemBinding(
            provider_id="provider:fixture",
            product_id="product:fixture",
            model_id="model:fixture",
            model_version_ref="model-version:fixture-v1",
            runtime_ref="runtime:tevv-profile-v1",
            environment_ref="environment:research-sandbox",
            prompt_ref="prompt:fixture",
            scaffold_ref="scaffold:fixture",
            tool_manifest_ref="tools:fixture",
            generation_config_ref="generation-config:fixture",
            exact_source_state_ref="source-state:tevv-profile-v1",
        ),
        metrics=(
            TEVVMetricSpec(
                metric_id="TEVV-METRIC-001",
                measurement_concept="bounded task correctness",
                method_ref="method:bounded-measurement-v1",
                method_version="v1",
                unit="ratio",
                acceptance_criterion_ref="criterion:bounded-v1",
                uncertainty_ref="uncertainty:bounded-v1",
                construct_validity_ref="validity:bounded-v1",
                quality_characteristic_refs=("quality:functional-correctness",),
                effectiveness_review_ref="review:metric-effectiveness-v1",
                risk_refs=("RISK-OVERCLAIM-001",),
            ),
        ),
        cases=(
            TEVVCaseSpec(
                case_id="TEVV-CASE-001",
                input_ref="input:tevv-case-001",
                test_set_ref="test-set:DATA-001",
                test_set_integrity_ref="integrity:DATA-001",
                data_quality_ref="DATA-001",
                contamination_check_ref="check:contamination-data-001",
                leakage_check_ref="check:leakage-data-001",
                scenario_ref="scenario:bounded-research",
                test_environment_ref="environment:research-sandbox",
                test_approach=TEVVTestApproach.BLACK_BOX,
                oracle_strategy=OracleStrategy.PROPERTY_BASED,
                oracle_ref="oracle:bounded-property-v1",
                oracle_qualification_ref="NOT_APPLICABLE",
                expected_property_refs=("property:no-unsupported-claim",),
                metric_ids=("TEVV-METRIC-001",),
                held_out=True,
            ),
        ),
        repetition_policy_ref="policy:repeat-v1",
        nondeterminism_policy_ref="policy:nondeterminism-v1",
        minimum_repetitions=1,
        stochastic_system=False,
        aggregation_rule_ref="aggregation:bounded-v1",
        tevv_toolchain_ref="tevv-toolchain:fixture-v1",
        tevv_toolchain_version="v1",
        verification_requirement_refs=(),
        validation_requirement_refs=(),
        evaluator_ref="evaluator:tevv-fixture",
        evaluator_version="v1",
        evaluator_independence=evaluator_independence,
        evaluator_independence_basis_ref="basis:tevv-fixture-independence",
        human_subjects_status=HumanSubjectsStatus.NOT_APPLICABLE,
        human_subjects_protection_refs=(),
        population_representativeness_refs=(),
        target_context_ref="context:research-sandbox",
        context_similarity_statement="Structural research-sandbox scope only.",
        context_similarity_basis_refs=("basis:research-sandbox",),
        operating_condition_refs=("condition:research-sandbox",),
        generalizability_limit_refs=("limit:no-deployment-generalization",),
        failure_action_ref="reaction:HOLD_AND_REVIEW",
        preregistration_ref="preregistration:TEVV-PROFILE-001",
    )


def tevv_receipt(
    *,
    assessment_target_ref: str = "quality-plan:PLAN-001",
    assessment_target_sha256: str | None = None,
    evaluator_independence: EvaluatorIndependence = EvaluatorIndependence.INTERNAL_INDEPENDENT,
    measurement_id: str = "MEAS-001",
) -> TEVVProfileReceipt:
    value = tevv_profile(evaluator_independence=evaluator_independence)
    assessment = AITEVVProfileGate().assess(value)
    target_sha256 = assessment_target_sha256 or quality_plan_seed().assessment_target_sha256()
    return build_tevv_profile_receipt(
        receipt_id="TEVV-RECEIPT-001",
        assessment_target_ref=assessment_target_ref,
        assessment_target_sha256=target_sha256,
        profile=value,
        assessment=assessment,
        measurement_bindings=(
            TEVVMetricMeasurementBinding(
                metric_id="TEVV-METRIC-001",
                measurement_id=measurement_id,
                mapping_basis_ref="mapping:tevv-metric-to-measurement-v1",
            ),
        ),
        producer_git_head="a" * 40,
        producer_tree_sha="b" * 40,
        producer_contract_ref="contract:ai-tevv-profile-v1",
        producer_contract_sha256="c" * 64,
    )


def security_profile(
    *,
    held_out: bool = True,
    risk_ref: str = "RISK-OVERCLAIM-001",
    data_quality_ref: str = "DATA-001",
):
    applicability = tuple(
        AISecurityThreatApplicability(
            threat_class=item,
            applicable=item is AISecurityThreatClass.PROMPT_INJECTION,
            rationale_ref=f"applicability:{item.value.lower()}",
        )
        for item in AISecurityThreatClass
    )
    adversary = AIAdversaryModel(
        adversary_id="ADV-SECURITY-001",
        goal_ref="goal:bounded-security-boundary-probe",
        objective_refs=("objective:security-boundary-bypass",),
        capability_refs=("capability:crafted-inputs",),
        knowledge=AttackerKnowledge.BLACK_BOX,
        access_refs=("access:declared-offline-test-interface",),
        lifecycle_stage_refs=("stage:inference-and-tool-runtime",),
    )
    threat = AISecurityThreatRecord(
        threat_id="THREAT-PROMPT-INJECTION-001",
        threat_class=AISecurityThreatClass.PROMPT_INJECTION,
        adversary_id=adversary.adversary_id,
        asset_refs=("asset:model-behavior",),
        attack_surface_refs=("surface:prompt-context",),
        scenario_ref="scenario:bounded-prompt-injection",
        precondition_refs=("precondition:prompt-input-available",),
        risk_ref=risk_ref,
        expected_security_property_refs=("property:boundary-preserved",),
        mitigation_refs=("mitigation:prompt-boundary-v1",),
        mitigation_effectiveness_review_ref="review:prompt-mitigation-v1",
        detection_refs=("detection:prompt-boundary-v1",),
        detection_effectiveness_review_ref="review:prompt-detection-v1",
        response_refs=("response:upstream-security-incident-sequence",),
        residual_risk_ref="residual-risk:prompt-injection",
        external_taxonomy_refs=("NIST-AI-100-2e2025",),
    )
    test = AISecurityTestSpec(
        test_id="SEC-TEST-PROMPT-INJECTION-001",
        threat_ids=(threat.threat_id,),
        authorization_scope_ref="authorization:offline-synthetic-fixtures-only",
        test_environment_ref="environment:research-sandbox",
        isolation_ref="isolation:upstream-security-runtime-isolation-v1",
        task_budget_ref="budget:bounded-adversarial-test-v1",
        logging_plan_ref="logging:immutable-security-evidence-v1",
        adversarial_fixture_ref="fixture:adversarial-prompt-injection",
        benign_control_ref="fixture:benign-prompt-control",
        fixture_provenance_ref="provenance:prompt-injection-synthetic",
        fixture_integrity_ref="integrity:prompt-injection-fixture-v1",
        data_quality_ref="DATA-001",
        contamination_check_ref="check:contamination-data-001",
        leakage_check_ref="check:leakage-data-001",
        oracle_ref="oracle:prompt-security-property",
        success_criterion_ref="criterion:prompt-boundary-preserved",
        stop_condition_ref="stop:first-boundary-violation-or-budget-exhaustion",
        max_attempts=3,
        held_out=held_out,
    )
    return build_ai_adversarial_security_profile(
        profile_id="AI-SECURITY-PROFILE-001",
        profile_version="0.1.0",
        objective_ref="objective:qms-bound-ai-security",
        intended_use_ref="use:research-engineering-security-planning-only",
        system=AISystemBinding(
            provider_id="provider:fixture",
            product_id="product:fixture",
            model_id="model:fixture",
            model_version_ref="model-version:fixture-v1",
            runtime_ref="runtime:tevv-profile-v1",
            environment_ref="environment:research-sandbox",
            prompt_ref="prompt:fixture",
            scaffold_ref="scaffold:fixture",
            tool_manifest_ref="tools:fixture",
            generation_config_ref="generation-config:fixture",
            exact_source_state_ref="source-state:tevv-profile-v1",
        ),
        threat_applicability=applicability,
        adversaries=(adversary,),
        threats=(threat,),
        tests=(test,),
        existing_security_control_refs=(
            "components/upstream_security_v0.1.0/docs/ARCHITECTURE.md",
            "docs/THREAT_MODEL.md",
        ),
        incident_response_ref=(
            "components/upstream_security_v0.1.0/docs/INCIDENT_RESPONSE_SEQUENCE.md"
        ),
        evaluator_ref="evaluator:security-review-role-v1",
        evaluator_independence_basis_ref="basis:security-review-independent-v1",
        security_toolchain_ref="toolchain:offline-security-harness-v1",
        security_toolchain_version="v1",
        failure_action_ref="reaction:HOLD_ISOLATE_PRESERVE_EVIDENCE",
        preregistration_ref="preregistration:AI-SECURITY-PROFILE-001",
        source_refs=("NIST-AI-100-2e2025",),
    )


def security_receipt(
    *,
    assessment_target_ref: str = "quality-plan:PLAN-001",
    assessment_target_sha256: str | None = None,
    tevv_receipt_value: TEVVProfileReceipt | None = None,
    held_out: bool = True,
    risk_ref: str = "RISK-OVERCLAIM-001",
    data_quality_ref: str = "DATA-001",
) -> AISecurityProfileReceipt:
    tevv_bound = tevv_receipt_value or tevv_receipt()
    value = security_profile(
        held_out=held_out,
        risk_ref=risk_ref,
        data_quality_ref=data_quality_ref,
    )
    assessment = AIAdversarialSecurityGate().assess(value)
    target_sha256 = assessment_target_sha256 or quality_plan_seed().assessment_target_sha256()
    return build_ai_security_profile_receipt(
        receipt_id="AI-SECURITY-RECEIPT-001",
        assessment_target_ref=assessment_target_ref,
        assessment_target_sha256=target_sha256,
        profile=value,
        assessment=assessment,
        tevv_receipt=tevv_bound,
        tevv_alignment_basis_ref="mapping:security-profile-to-tevv-v1",
        producer_git_head="d" * 40,
        producer_tree_sha="e" * 40,
        producer_contract_ref="contract:ai-security-profile-v1",
        producer_contract_sha256="f" * 64,
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
    tevv_receipt_value: TEVVProfileReceipt | None = None,
    security_receipt_value: AISecurityProfileReceipt | None = None,
) -> ResearchQualityPlan:
    bound = chain_receipt or receipt()
    seed = quality_plan_seed(bound)
    target_sha256 = seed.assessment_target_sha256()
    risk_bound = risk_receipt or risk_impact_receipt(
        assessment_target_sha256=target_sha256
    )
    tevv_bound = tevv_receipt_value or tevv_receipt(
        assessment_target_sha256=target_sha256
    )
    security_bound = security_receipt_value or security_receipt(
        assessment_target_sha256=target_sha256,
        tevv_receipt_value=tevv_bound,
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
            f"git:{tevv_bound.producer_git_head}",
            f"tree:{tevv_bound.producer_tree_sha}",
            f"contract-sha256:{tevv_bound.producer_contract_sha256}",
            f"tevv-profile-receipt:{tevv_bound.receipt_sha256}",
            f"tevv-profile:{tevv_bound.profile_id}:{tevv_bound.profile_sha256}",
            f"tevv-vocabulary-sha256:{tevv_bound.tevv_vocabulary_sha256}",
            tevv_bound.exact_source_state_ref,
            tevv_bound.exact_runtime_ref,
            f"git:{security_bound.producer_git_head}",
            f"tree:{security_bound.producer_tree_sha}",
            f"contract-sha256:{security_bound.producer_contract_sha256}",
            f"ai-security-profile-receipt:{security_bound.receipt_sha256}",
            f"ai-security-profile:{security_bound.profile_id}:{security_bound.profile_sha256}",
            security_bound.exact_source_state_ref,
            security_bound.exact_runtime_ref,
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
    tevv_receipt_value: TEVVProfileReceipt | None = None,
    security_receipt_value: AISecurityProfileReceipt | None = None,
    extra_refs: tuple[str, ...] | None = None,
) -> ManagementReviewRecord:
    risk_bound = risk_receipt or risk_impact_receipt()
    tevv_bound = tevv_receipt_value or tevv_receipt()
    security_bound = security_receipt_value or security_receipt(
        tevv_receipt_value=tevv_bound
    )
    tevv_measurement_ids = tuple(
        item.measurement_id for item in tevv_bound.measurement_bindings
    )
    default_refs = (
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
        tevv_bound.receipt_id,
        tevv_bound.profile_id,
        f"tevv-profile-receipt:{tevv_bound.receipt_sha256}",
        *tevv_bound.risk_refs,
        *tevv_measurement_ids,
        *tevv_bound.data_quality_refs,
        security_bound.receipt_id,
        security_bound.profile_id,
        f"ai-security-profile-receipt:{security_bound.receipt_sha256}",
        *security_bound.threat_ids,
        *security_bound.test_ids,
        *security_bound.risk_refs,
        *security_bound.data_quality_refs,
        *security_bound.security_control_refs,
        security_bound.incident_response_ref,
        *security_bound.authorization_scope_refs,
        *security_bound.isolation_refs,
        *security_bound.task_budget_refs,
        *security_bound.logging_plan_refs,
        *security_bound.source_refs,
        security_bound.tevv_alignment_basis_ref,
    )
    refs = tuple(dict.fromkeys(default_refs)) if extra_refs is None else extra_refs
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
    tevv_receipt_value: TEVVProfileReceipt | None = None,
    security_receipt_value: AISecurityProfileReceipt | None = None,
    plan_value: ResearchQualityPlan | None = None,
    controls_value: ExtendedQualityControls | None = None,
    review_value: ManagementReviewRecord | None = None,
):
    bound = receipt_value or receipt()
    risk_bound = risk_receipt_value or risk_impact_receipt()
    tevv_bound = tevv_receipt_value or tevv_receipt()
    security_bound = security_receipt_value or security_receipt(
        tevv_receipt_value=tevv_bound
    )
    return FullQualitySystemEngine().assess(
        plan=plan_value or quality_plan(bound, risk_bound, tevv_bound, security_bound),
        measurements=(measurement(),),
        chain_receipt=bound,
        risk_impact_receipt=risk_bound,
        tevv_receipt=tevv_bound,
        security_receipt=security_bound,
        field_signals=(field_signal(),),
        audits=(audit(),),
        management_review=review_value or review(
            risk_bound,
            tevv_bound,
            security_bound,
        ),
        controls=controls_value or extended_controls(),
    )


def test_full_quality_system_ready_preserves_subjectivity_nonclaims() -> None:
    result = assess()
    assert result.disposition is EndToEndDisposition.READY_FOR_HUMAN_REVIEW
    assert "CONTENT_ADDRESSED_QUALITY_CHAIN_RECEIPT_BOUND" in result.reasons
    assert "CONTENT_ADDRESSED_TEVV_PROFILE_RECEIPT_BOUND" in result.reasons
    assert "TEVV_PROFILE_READY_FOR_BOUNDED_EXECUTION_ONLY" in result.reasons
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



def test_full_qms_rejects_same_plan_id_after_semantic_target_drift() -> None:
    risk_bound = risk_impact_receipt()
    original_plan = quality_plan(risk_receipt=risk_bound)
    mutated_plan = replace(
        original_plan,
        research_question_ref="research:different-question",
    )

    assert mutated_plan.plan_id == original_plan.plan_id
    assert mutated_plan.assessment_target_sha256() != original_plan.assessment_target_sha256()

    result = assess(
        risk_receipt_value=risk_bound,
        plan_value=mutated_plan,
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "AI_RISK_IMPACT_RECEIPT_TARGET_DIGEST_MISMATCH" in result.reasons


def test_quality_plan_assessment_target_digest_is_order_invariant_for_set_like_fields() -> None:
    plan = quality_plan_seed()
    reordered = replace(
        plan,
        critical_quality_attributes=tuple(reversed(plan.critical_quality_attributes)),
        controls=tuple(reversed(plan.controls)),
        measurement_ids=tuple(reversed(plan.measurement_ids)),
        risk_refs=tuple(reversed(plan.risk_refs)),
    )
    assert reordered.assessment_target_sha256() == plan.assessment_target_sha256()


def test_full_qms_ready_records_semantic_target_binding() -> None:
    result = assess()
    assert result.disposition is EndToEndDisposition.READY_FOR_HUMAN_REVIEW
    assert "AI_RISK_IMPACT_RECEIPT_TARGET_SEMANTICS_BOUND" in result.reasons



def test_full_qms_requires_tevv_receipt_configuration_binding() -> None:
    chain_bound = receipt()
    risk_bound = risk_impact_receipt()
    tevv_bound = tevv_receipt()
    plan = quality_plan(chain_bound, risk_bound, tevv_bound)
    stripped = replace(
        plan,
        configuration_refs=tuple(
            ref
            for ref in plan.configuration_refs
            if not (
                ref == f"git:{tevv_bound.producer_git_head}"
                or ref == f"tree:{tevv_bound.producer_tree_sha}"
                or ref == f"contract-sha256:{tevv_bound.producer_contract_sha256}"
                or ref == f"tevv-profile-receipt:{tevv_bound.receipt_sha256}"
                or ref == f"tevv-profile:{tevv_bound.profile_id}:{tevv_bound.profile_sha256}"
                or ref == f"tevv-vocabulary-sha256:{tevv_bound.tevv_vocabulary_sha256}"
                or ref == tevv_bound.exact_source_state_ref
                or ref == tevv_bound.exact_runtime_ref
            )
        ),
    )
    result = assess(
        receipt_value=chain_bound,
        risk_receipt_value=risk_bound,
        tevv_receipt_value=tevv_bound,
        plan_value=stripped,
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "QUALITY_RECEIPTS_NOT_BOUND_TO_QUALITY_PLAN_CONFIGURATION" in result.reasons


def test_full_qms_rejects_tevv_receipt_for_different_plan_target() -> None:
    wrong_target = tevv_receipt(assessment_target_ref="quality-plan:PLAN-OTHER")
    result = assess(tevv_receipt_value=wrong_target)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "TEVV_RECEIPT_TARGET_MISMATCH" in result.reasons


def test_full_qms_rejects_tevv_receipt_after_plan_semantic_drift() -> None:
    tevv_bound = tevv_receipt()
    original = quality_plan(tevv_receipt_value=tevv_bound)
    mutated = replace(original, research_question_ref="research:changed-after-tevv")
    result = assess(tevv_receipt_value=tevv_bound, plan_value=mutated)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "TEVV_RECEIPT_TARGET_DIGEST_MISMATCH" in result.reasons


def test_full_qms_requires_tevv_risk_coverage_in_quality_plan() -> None:
    tevv_bound = tevv_receipt()
    plan = replace(
        quality_plan(tevv_receipt_value=tevv_bound),
        risk_refs=("risk:construct-drift",),
    )
    result = assess(tevv_receipt_value=tevv_bound, plan_value=plan)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "TEVV_RISKS_NOT_BOUND_TO_QUALITY_PLAN_RISK_REFS" in result.reasons


def test_full_qms_requires_tevv_measurement_assurance_binding() -> None:
    tevv_bound = tevv_receipt(measurement_id="MEAS-OTHER")
    result = assess(tevv_receipt_value=tevv_bound)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "TEVV_MEASUREMENTS_NOT_BOUND_TO_QUALITY_PLAN" in result.reasons
    assert "TEVV_MEASUREMENT_ASSURANCE_RECORDS_MISSING" in result.reasons


def test_full_qms_requires_tevv_data_quality_binding() -> None:
    tevv_bound = tevv_receipt()
    controls = replace(
        extended_controls(),
        data_quality=(replace(data_quality(), data_id="DATA-OTHER"),),
    )
    result = assess(tevv_receipt_value=tevv_bound, controls_value=controls)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "TEVV_DATA_QUALITY_RECORDS_MISSING" in result.reasons


def test_full_qms_requires_management_review_of_tevv_receipt() -> None:
    risk_bound = risk_impact_receipt()
    tevv_bound = tevv_receipt()
    incomplete = review(
        risk_bound,
        tevv_bound,
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
            risk_bound.receipt_id,
            *risk_bound.risk_ids,
            *risk_bound.impact_assessment_ids,
        ),
    )
    result = assess(
        risk_receipt_value=risk_bound,
        tevv_receipt_value=tevv_bound,
        review_value=incomplete,
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "MANAGEMENT_REVIEW_TEVV_INPUTS_INCOMPLETE" in result.reasons


def test_tevv_hold_receipt_holds_full_qms_without_claiming_model_failure() -> None:
    tevv_bound = tevv_receipt(
        evaluator_independence=EvaluatorIndependence.NON_INDEPENDENT,
    )
    assert tevv_bound.disposition is TEVVProfileDisposition.HOLD
    result = assess(tevv_receipt_value=tevv_bound)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "TEVV_PROFILE_RECEIPT_HOLD" in result.reasons
    assert tevv_bound.model_executed is False
    assert tevv_bound.empirical_model_evidence is False


def test_full_qms_ready_records_tevv_structural_bindings_only() -> None:
    result = assess()
    assert result.disposition is EndToEndDisposition.READY_FOR_HUMAN_REVIEW
    assert "CONTENT_ADDRESSED_TEVV_PROFILE_RECEIPT_BOUND" in result.reasons
    assert "TEVV_RECEIPT_TARGET_SEMANTICS_BOUND" in result.reasons
    assert "TEVV_RISK_COVERAGE_BOUND_TO_QUALITY_PLAN" in result.reasons
    assert "TEVV_MEASUREMENT_ASSURANCE_BINDINGS_COMPLETE" in result.reasons
    assert "TEVV_DATA_QUALITY_BINDINGS_COMPLETE" in result.reasons
    assert "TEVV_PROFILE_READY_FOR_BOUNDED_EXECUTION_ONLY" in result.reasons
    assert result.scientific_disposition == "HOLD"



def test_full_qms_ready_records_ai_security_structural_bindings_only() -> None:
    result = assess()
    assert result.disposition is EndToEndDisposition.READY_FOR_HUMAN_REVIEW
    assert "CONTENT_ADDRESSED_AI_SECURITY_PROFILE_RECEIPT_BOUND" in result.reasons
    assert "AI_SECURITY_RECEIPT_TARGET_SEMANTICS_BOUND" in result.reasons
    assert "AI_SECURITY_RISK_REGISTER_BINDINGS_COMPLETE" in result.reasons
    assert "AI_SECURITY_DATA_QUALITY_BINDINGS_COMPLETE" in result.reasons
    assert "AI_SECURITY_TEVV_RECEIPT_ALIGNMENT_BOUND" in result.reasons
    assert "AI_SECURITY_SOURCE_RUNTIME_ALIGNMENT_BOUND" in result.reasons
    assert "AI_SECURITY_CONTROL_AND_RESPONSE_TRACE_BOUND" in result.reasons
    assert (
        "AI_SECURITY_PROFILE_READY_FOR_BOUNDED_ADVERSARIAL_EVALUATION_ONLY"
        in result.reasons
    )
    assert result.scientific_disposition == "HOLD"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.consciousness_conclusion == "NOT_ESTABLISHED"
    assert result.phenomenal_experience_conclusion == "NOT_ESTABLISHED"


def test_full_qms_requires_ai_security_receipt_configuration_binding() -> None:
    chain_bound = receipt()
    risk_bound = risk_impact_receipt()
    tevv_bound = tevv_receipt()
    security_bound = security_receipt(tevv_receipt_value=tevv_bound)
    plan = quality_plan(chain_bound, risk_bound, tevv_bound, security_bound)
    stripped = replace(
        plan,
        configuration_refs=tuple(
            ref
            for ref in plan.configuration_refs
            if not (
                ref == f"git:{security_bound.producer_git_head}"
                or ref == f"tree:{security_bound.producer_tree_sha}"
                or ref
                == f"contract-sha256:{security_bound.producer_contract_sha256}"
                or ref
                == f"ai-security-profile-receipt:{security_bound.receipt_sha256}"
                or ref
                == f"ai-security-profile:{security_bound.profile_id}:{security_bound.profile_sha256}"
                or ref == security_bound.exact_source_state_ref
                or ref == security_bound.exact_runtime_ref
            )
        ),
    )
    result = assess(
        receipt_value=chain_bound,
        risk_receipt_value=risk_bound,
        tevv_receipt_value=tevv_bound,
        security_receipt_value=security_bound,
        plan_value=stripped,
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "QUALITY_RECEIPTS_NOT_BOUND_TO_QUALITY_PLAN_CONFIGURATION" in result.reasons


def test_full_qms_rejects_ai_security_receipt_for_different_plan_target() -> None:
    wrong_target = security_receipt(
        assessment_target_ref="quality-plan:PLAN-OTHER",
    )
    result = assess(security_receipt_value=wrong_target)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "AI_SECURITY_RECEIPT_TARGET_MISMATCH" in result.reasons


def test_full_qms_rejects_ai_security_receipt_after_plan_semantic_drift() -> None:
    security_bound = security_receipt()
    original = quality_plan(security_receipt_value=security_bound)
    mutated = replace(
        original,
        research_question_ref="research:changed-after-ai-security",
    )
    result = assess(
        security_receipt_value=security_bound,
        plan_value=mutated,
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "AI_SECURITY_RECEIPT_TARGET_DIGEST_MISMATCH" in result.reasons


def test_full_qms_requires_ai_security_risks_in_quality_plan() -> None:
    security_bound = security_receipt(
        risk_ref="RISK-AI-SECURITY-ORPHAN",
    )
    result = assess(security_receipt_value=security_bound)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "AI_SECURITY_RISKS_NOT_BOUND_TO_QUALITY_PLAN_RISK_REFS" in result.reasons


def test_full_qms_requires_ai_security_risks_in_ai_risk_register() -> None:
    risk_bound = risk_impact_receipt(risk_id="RISK-OTHER")
    tevv_bound = tevv_receipt()
    security_bound = security_receipt(tevv_receipt_value=tevv_bound)
    result = assess(
        risk_receipt_value=risk_bound,
        tevv_receipt_value=tevv_bound,
        security_receipt_value=security_bound,
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "AI_SECURITY_RISKS_NOT_BOUND_TO_AI_RISK_REGISTER" in result.reasons


def test_full_qms_requires_ai_security_data_quality_binding() -> None:
    security_bound = security_receipt(data_quality_ref="DATA-SECURITY-OTHER")
    result = assess(security_receipt_value=security_bound)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "AI_SECURITY_DATA_QUALITY_RECORDS_MISSING" in result.reasons


def test_full_qms_requires_ai_security_alignment_with_supplied_tevv_receipt() -> None:
    tevv_for_security = tevv_receipt()
    security_bound = security_receipt(tevv_receipt_value=tevv_for_security)
    different_tevv = tevv_receipt(measurement_id="MEAS-OTHER")
    result = assess(
        tevv_receipt_value=different_tevv,
        security_receipt_value=security_bound,
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "AI_SECURITY_TEVV_RECEIPT_ALIGNMENT_MISMATCH" in result.reasons


def test_full_qms_requires_management_review_of_ai_security_receipt() -> None:
    risk_bound = risk_impact_receipt()
    tevv_bound = tevv_receipt()
    security_bound = security_receipt(tevv_receipt_value=tevv_bound)
    incomplete = review(
        risk_bound,
        tevv_bound,
        security_bound,
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
            risk_bound.receipt_id,
            *risk_bound.risk_ids,
            *risk_bound.impact_assessment_ids,
            tevv_bound.receipt_id,
            tevv_bound.profile_id,
            f"tevv-profile-receipt:{tevv_bound.receipt_sha256}",
            *tevv_bound.risk_refs,
            *tuple(
                item.measurement_id
                for item in tevv_bound.measurement_bindings
            ),
            *tevv_bound.data_quality_refs,
        ),
    )
    result = assess(
        risk_receipt_value=risk_bound,
        tevv_receipt_value=tevv_bound,
        security_receipt_value=security_bound,
        review_value=incomplete,
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "MANAGEMENT_REVIEW_AI_SECURITY_INPUTS_INCOMPLETE" in result.reasons


def test_ai_security_hold_receipt_holds_full_qms_without_security_pass_claim() -> None:
    security_bound = security_receipt(held_out=False)
    assert security_bound.disposition is AISecurityProfileDisposition.HOLD
    result = assess(security_receipt_value=security_bound)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "AI_SECURITY_PROFILE_RECEIPT_HOLD" in result.reasons
    assert security_bound.adversarial_evaluation_executed is False
    assert security_bound.empirical_security_evidence is False
    assert security_bound.security_certification == "NONE"
