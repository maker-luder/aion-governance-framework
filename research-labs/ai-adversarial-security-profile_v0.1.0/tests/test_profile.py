from __future__ import annotations

from dataclasses import replace

import pytest

from aion_ai_security_profile import (
    AIAdversarialSecurityGate,
    AIAdversaryModel,
    AISecurityError,
    AISecurityProfileDisposition,
    AISecurityTestSpec,
    AISecurityThreatApplicability,
    AISecurityThreatClass,
    AISecurityThreatRecord,
    AttackerKnowledge,
    build_ai_adversarial_security_profile,
)
from aion_ai_tevv import AISystemBinding


def system() -> AISystemBinding:
    return AISystemBinding(
        provider_id="provider-under-study",
        product_id="product-under-study",
        model_id="model-under-study",
        model_version_ref="model-version:security-profile-v1",
        runtime_ref="runtime:security-sandbox-v1",
        environment_ref="environment:offline-security-sandbox-v1",
        prompt_ref="prompt:security-fixture-v1",
        scaffold_ref="scaffold:security-fixture-v1",
        tool_manifest_ref="tools:deny-by-default-v1",
        generation_config_ref="generation-config:security-fixture-v1",
        exact_source_state_ref="git:security-profile-fixture-v1",
    )


def applicability() -> tuple[AISecurityThreatApplicability, ...]:
    return tuple(
        AISecurityThreatApplicability(
            threat_class=threat_class,
            applicable=True,
            rationale_ref=f"applicability:{threat_class.value.lower()}",
        )
        for threat_class in AISecurityThreatClass
    )


def adversary() -> AIAdversaryModel:
    return AIAdversaryModel(
        adversary_id="ADV-EXTERNAL-001",
        goal_ref="goal:degrade-or-extract-ai-system-properties",
        objective_refs=("objective:security-boundary-bypass",),
        capability_refs=("capability:crafted-inputs", "capability:repeated-query-access"),
        knowledge=AttackerKnowledge.BLACK_BOX,
        access_refs=("access:declared-test-interface-only",),
        lifecycle_stage_refs=(
            "stage:data-and-supply-chain",
            "stage:inference-and-tool-runtime",
        ),
    )


def threat(threat_class: AISecurityThreatClass) -> AISecurityThreatRecord:
    suffix = threat_class.value
    return AISecurityThreatRecord(
        threat_id=f"THREAT-{suffix}",
        threat_class=threat_class,
        adversary_id="ADV-EXTERNAL-001",
        asset_refs=("asset:model-behavior", "asset:research-evidence-integrity"),
        attack_surface_refs=(f"surface:{suffix.lower()}",),
        scenario_ref=f"scenario:{suffix.lower()}-bounded",
        precondition_refs=(f"precondition:{suffix.lower()}-surface-exposed",),
        risk_ref=f"risk:ai-security:{suffix.lower()}",
        expected_security_property_refs=("property:fail-closed-boundary-preserved",),
        mitigation_refs=(f"mitigation:{suffix.lower()}-v1",),
        mitigation_effectiveness_review_ref=f"review:mitigation-effectiveness:{suffix.lower()}",
        detection_refs=(f"detection:{suffix.lower()}-v1",),
        detection_effectiveness_review_ref=f"review:detection-effectiveness:{suffix.lower()}",
        response_refs=("response:upstream-security-incident-sequence",),
        residual_risk_ref=f"residual-risk:{suffix.lower()}",
        external_taxonomy_refs=(
            "NIST-AI-100-2e2025",
            "OWASP-GENAI-TOP10-2025",
        ),
    )


def security_test(threat_class: AISecurityThreatClass) -> AISecurityTestSpec:
    suffix = threat_class.value
    return AISecurityTestSpec(
        test_id=f"SEC-TEST-{suffix}",
        threat_ids=(f"THREAT-{suffix}",),
        authorization_scope_ref="authorization:offline-synthetic-fixtures-only",
        test_environment_ref="environment:isolated-offline-sandbox-v1",
        isolation_ref="isolation:upstream-security-runtime-isolation-v1",
        task_budget_ref="budget:bounded-adversarial-test-v1",
        logging_plan_ref="logging:immutable-security-evidence-v1",
        adversarial_fixture_ref=f"fixture:adversarial-{suffix.lower()}",
        benign_control_ref=f"fixture:benign-{suffix.lower()}",
        fixture_provenance_ref=f"provenance:{suffix.lower()}-synthetic-fixture",
        fixture_integrity_ref=f"sha256:{suffix.lower()}-fixture-manifest",
        data_quality_ref=f"data-quality:{suffix.lower()}-synthetic",
        contamination_check_ref=f"check:contamination:{suffix.lower()}",
        leakage_check_ref=f"check:leakage:{suffix.lower()}",
        oracle_ref=f"oracle:{suffix.lower()}-security-property",
        success_criterion_ref=f"criterion:{suffix.lower()}-bounded-v1",
        stop_condition_ref="stop:first-boundary-violation-or-budget-exhaustion",
        max_attempts=3,
        held_out=True,
    )


def profile(
    *,
    applicability_value: tuple[AISecurityThreatApplicability, ...] | None = None,
    threats_value: tuple[AISecurityThreatRecord, ...] | None = None,
    tests_value: tuple[AISecurityTestSpec, ...] | None = None,
):
    app = applicability_value or applicability()
    threats = threats_value or tuple(threat(item) for item in AISecurityThreatClass)
    tests = tests_value or tuple(security_test(item) for item in AISecurityThreatClass)
    return build_ai_adversarial_security_profile(
        profile_id="AI-SECURITY-PROFILE-001",
        profile_version="0.1.0",
        objective_ref="objective:bounded-ai-specific-adversarial-security",
        intended_use_ref="use:research-engineering-security-planning-only",
        system=system(),
        threat_applicability=app,
        adversaries=(adversary(),),
        threats=threats,
        tests=tests,
        existing_security_control_refs=(
            "components/upstream_security_v0.1.0/docs/ARCHITECTURE.md",
            "docs/THREAT_MODEL.md",
            "docs/governance/RISK_MODEL.md",
        ),
        incident_response_ref=(
            "components/upstream_security_v0.1.0/docs/INCIDENT_RESPONSE_SEQUENCE.md"
        ),
        evaluator_ref="evaluator:security-review-role-v1",
        evaluator_independence_basis_ref="basis:separate-from-front-line-implementation-v1",
        security_toolchain_ref="toolchain:offline-synthetic-security-harness-v1",
        security_toolchain_version="v1",
        failure_action_ref="reaction:HOLD_ISOLATE_PRESERVE_EVIDENCE",
        preregistration_ref="preregistration:AI-SECURITY-PROFILE-001",
        source_refs=(
            "NIST-AI-100-2e2025",
            "OWASP-GENAI-TOP10-2025",
            "ISO-IEC-27090-UNDER-PUBLICATION-2026-09-18",
        ),
    )


def test_structural_security_profile_ready_but_not_security_pass() -> None:
    value = profile()
    result = AIAdversarialSecurityGate().assess(value)

    assert result.disposition is AISecurityProfileDisposition.READY_FOR_BOUNDED_ADVERSARIAL_EVALUATION
    assert result.adversarial_evaluation_executed is False
    assert result.empirical_security_evidence is False
    assert result.security_certification == "NONE"
    assert result.scientific_disposition == "HOLD"
    assert result.canonical_effect == "NONE"
    assert result.deployment is False
    assert "READY_FOR_BOUNDED_ADVERSARIAL_EVALUATION_NOT_SECURITY_PASS" in result.reasons


def test_all_core_threat_classes_require_explicit_applicability() -> None:
    with pytest.raises(AISecurityError, match="every core AI security threat class"):
        profile(applicability_value=applicability()[:-1])


def test_non_applicable_threat_cannot_keep_threat_record() -> None:
    items = list(applicability())
    items[0] = replace(items[0], applicable=False)
    with pytest.raises(AISecurityError, match="applicable threat classes"):
        profile(applicability_value=tuple(items))


def test_non_applicable_threat_with_no_record_is_valid() -> None:
    items = list(applicability())
    target = AISecurityThreatClass.MODEL_POISONING
    items = [
        replace(item, applicable=False) if item.threat_class is target else item
        for item in items
    ]
    threats = tuple(
        threat(item) for item in AISecurityThreatClass if item is not target
    )
    tests = tuple(
        security_test(item) for item in AISecurityThreatClass if item is not target
    )
    result = AIAdversarialSecurityGate().assess(
        profile(
            applicability_value=tuple(items),
            threats_value=threats,
            tests_value=tests,
        )
    )
    assert result.disposition is AISecurityProfileDisposition.READY_FOR_BOUNDED_ADVERSARIAL_EVALUATION


def test_threat_must_reference_known_adversary() -> None:
    values = list(tuple(threat(item) for item in AISecurityThreatClass))
    values[0] = replace(values[0], adversary_id="ADV-UNKNOWN")
    with pytest.raises(AISecurityError, match="unknown adversary"):
        profile(threats_value=tuple(values))


def test_every_applicable_threat_requires_test_coverage() -> None:
    with pytest.raises(AISecurityError, match="every applicable threat"):
        profile(tests_value=tuple(security_test(item) for item in list(AISecurityThreatClass)[1:]))


def test_security_test_rejects_unknown_threat() -> None:
    tests = list(tuple(security_test(item) for item in AISecurityThreatClass))
    tests[0] = replace(tests[0], threat_ids=("THREAT-UNKNOWN",))
    with pytest.raises(AISecurityError, match="unknown threat"):
        profile(tests_value=tuple(tests))


def test_non_held_out_adversarial_test_holds_gate() -> None:
    tests = list(tuple(security_test(item) for item in AISecurityThreatClass))
    tests[0] = replace(tests[0], held_out=False)
    result = AIAdversarialSecurityGate().assess(profile(tests_value=tuple(tests)))
    assert result.disposition is AISecurityProfileDisposition.HOLD
    assert "NON_HELD_OUT_ADVERSARIAL_TEST_REQUIRES_REVIEW" in result.reasons


def test_structural_profile_cannot_authorize_live_attack_surface() -> None:
    with pytest.raises(AISecurityError, match="structural/offline only"):
        replace(security_test(AISecurityThreatClass.PROMPT_INJECTION), live_target_allowed=True)
    with pytest.raises(AISecurityError, match="structural/offline only"):
        replace(security_test(AISecurityThreatClass.PRIVACY_ATTACK), credential_use_allowed=True)
    with pytest.raises(AISecurityError, match="structural/offline only"):
        replace(security_test(AISecurityThreatClass.EVASION), external_network_allowed=True)


def test_security_test_attempt_budget_is_bounded() -> None:
    with pytest.raises(AISecurityError, match="between 1 and 100"):
        replace(security_test(AISecurityThreatClass.EVASION), max_attempts=0)
    with pytest.raises(AISecurityError, match="between 1 and 100"):
        replace(security_test(AISecurityThreatClass.EVASION), max_attempts=101)


def test_profile_digest_detects_tampering() -> None:
    value = profile()
    with pytest.raises(AISecurityError, match="content digest mismatch"):
        replace(value, incident_response_ref="response:different")


def test_profile_preserves_security_and_subjectivity_nonclaims() -> None:
    value = profile()
    assert value.adversarial_evaluation_executed is False
    assert value.empirical_security_evidence is False
    assert value.security_certification == "NONE"
    assert value.scientific_disposition == "HOLD"
    assert value.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert value.consciousness_conclusion == "NOT_ESTABLISHED"
    assert value.canonical_effect == "NONE"
    assert value.deployment is False



def test_at_least_one_core_threat_must_be_applicable() -> None:
    all_not_applicable = tuple(
        replace(item, applicable=False)
        for item in applicability()
    )
    with pytest.raises(AISecurityError, match="at least one core AI security threat"):
        profile(
            applicability_value=all_not_applicable,
            threats_value=(),
            tests_value=(),
        )


def test_threat_requires_formal_risk_and_effectiveness_review_refs() -> None:
    base = threat(AISecurityThreatClass.PROMPT_INJECTION)
    with pytest.raises(AISecurityError, match="risk_ref"):
        replace(base, risk_ref="")
    with pytest.raises(AISecurityError, match="mitigation_effectiveness_review_ref"):
        replace(base, mitigation_effectiveness_review_ref="")
    with pytest.raises(AISecurityError, match="detection_effectiveness_review_ref"):
        replace(base, detection_effectiveness_review_ref="")


def test_adversarial_fixture_requires_provenance_contamination_and_leakage_refs() -> None:
    base = security_test(AISecurityThreatClass.PROMPT_INJECTION)
    with pytest.raises(AISecurityError, match="fixture_provenance_ref"):
        replace(base, fixture_provenance_ref="")
    with pytest.raises(AISecurityError, match="contamination_check_ref"):
        replace(base, contamination_check_ref="")
    with pytest.raises(AISecurityError, match="leakage_check_ref"):
        replace(base, leakage_check_ref="")



def test_adversarial_test_requires_isolation_budget_and_logging_refs() -> None:
    base = security_test(AISecurityThreatClass.PROMPT_INJECTION)
    with pytest.raises(AISecurityError, match="test_environment_ref"):
        replace(base, test_environment_ref="")
    with pytest.raises(AISecurityError, match="isolation_ref"):
        replace(base, isolation_ref="")
    with pytest.raises(AISecurityError, match="task_budget_ref"):
        replace(base, task_budget_ref="")
    with pytest.raises(AISecurityError, match="logging_plan_ref"):
        replace(base, logging_plan_ref="")
