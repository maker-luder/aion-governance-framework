from __future__ import annotations

from dataclasses import replace

import pytest

from aion_human_ai_longitudinal.empirical_gate import (
    ConstructFalsifier,
    ControlCondition,
    EmpiricalProtocol,
    InterCoderAgreementMethod,
    audit_empirical_protocol,
)
from aion_human_ai_longitudinal.harness import AdmissionDisposition, StudyError


def digest(char: str) -> str:
    return char * 64


def protocol(**overrides: object) -> EmpiricalProtocol:
    values: dict[str, object] = {
        "protocol_id": "ccts-htecr:synthetic:001",
        "protocol_sha256": digest("1"),
        "corpus_manifest_sha256": digest("2"),
        "coding_manual_sha256": digest("3"),
        "analysis_plan_sha256": digest("4"),
        "primary_contrast": "HTECR indicators across the full eligible corpus",
        "pilot_unit_ids": ("pilot-001",),
        "confirmatory_unit_ids": ("confirm-001",),
        "controls": tuple(ControlCondition),
        "falsifiers": tuple(ConstructFalsifier),
        "minimum_independent_coders": 2,
        "agreement_method": InterCoderAgreementMethod.KRIPPENDORFF_ALPHA,
        "agreement_acceptance_rule": "Use the prospectively frozen rule bound by this artifact digest.",
        "agreement_rule_sha256": digest("5"),
        "preregistration_ref": "synthetic/preregistration-v0.1.md",
        "preregistration_sha256": digest("6"),
        "protocol_freeze_receipt_sha256": digest("7"),
        "consent_route": "",
        "ethics_route": "",
        "preregistered": True,
        "protocol_frozen": True,
    }
    values.update(overrides)
    return EmpiricalProtocol(**values)


def test_complete_synthetic_protocol_opens_method_gate_without_claim_promotion() -> None:
    audit = audit_empirical_protocol(protocol())
    assert audit.pilot_gate_ready is True
    assert audit.confirmatory_gate_ready is True
    assert audit.htecr_measurement_independent_of_ccts_admission is True
    assert audit.complete_negative_controls is True
    assert audit.complete_falsifier_set is True
    assert audit.independent_coder_plan_present is True
    assert audit.agreement_rule_predeclared is True
    assert audit.preregistration_binding_present is True
    assert audit.protocol_freeze_binding_present is True
    assert audit.empirical_data_collected is False
    assert audit.ccts_empirical_validation == "NOT_ESTABLISHED"
    assert audit.htecr_validation == "NOT_ESTABLISHED"
    assert audit.subjectivity == "NOT_ESTABLISHED"
    assert audit.scientific_disposition is AdmissionDisposition.HOLD
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False


def test_ccts_status_cannot_be_used_as_htecr_eligibility_gate() -> None:
    with pytest.raises(StudyError, match="cannot gate HTECR"):
        protocol(ccts_status_is_htecr_eligibility_gate=True)


def test_pilot_and_confirmatory_material_must_be_disjoint() -> None:
    with pytest.raises(StudyError, match="must be disjoint"):
        protocol(confirmatory_unit_ids=("pilot-001",))


def test_complete_a_to_d_controls_are_required() -> None:
    with pytest.raises(StudyError, match="complete A-D"):
        protocol(controls=tuple(ControlCondition)[:-1])


def test_complete_f1_to_f10_falsifiers_are_required() -> None:
    with pytest.raises(StudyError, match="F1-F10"):
        protocol(falsifiers=tuple(ConstructFalsifier)[:-1])


def test_two_independent_coders_are_a_design_minimum() -> None:
    with pytest.raises(StudyError, match="two independent coders"):
        protocol(minimum_independent_coders=1)


def test_agreement_method_is_not_a_free_text_placeholder() -> None:
    with pytest.raises(StudyError, match="exact InterCoderAgreementMethod"):
        protocol(agreement_method="PROSPECTIVELY_SELECTED")  # type: ignore[arg-type]


def test_preregistration_and_freeze_require_bound_evidence() -> None:
    with pytest.raises(StudyError, match="preregistration_ref"):
        protocol(preregistration_ref="")
    with pytest.raises(StudyError, match="protocol_freeze_receipt_sha256"):
        protocol(protocol_freeze_receipt_sha256="")


def test_confirmatory_gate_requires_preregistration_binding() -> None:
    item = protocol(
        preregistered=False,
        preregistration_ref="",
        preregistration_sha256="",
    )
    audit = audit_empirical_protocol(item)
    assert audit.pilot_gate_ready is True
    assert audit.confirmatory_gate_ready is False
    assert audit.preregistration_binding_present is False


def test_real_participant_material_requires_consent_and_ethics_routes() -> None:
    with pytest.raises(StudyError, match="consent_route"):
        protocol(contains_real_participant_data=True)

    item = protocol(
        contains_real_participant_data=True,
        consent_route="APPROVED_CONSENT_ROUTE",
        ethics_route="APPLICABLE_REVIEW_ROUTE",
    )
    assert audit_empirical_protocol(item).confirmatory_gate_ready is True


@pytest.mark.parametrize(
    "field",
    [
        "claims_ccts_empirical_validation",
        "claims_htecr_validation",
        "claims_human_learning_effect",
        "claims_subjectivity",
        "claims_consciousness",
        "claims_phenomenal_experience",
        "claims_moral_agency",
        "claims_moral_status",
    ],
)
def test_infrastructure_cannot_promote_scientific_or_ontological_claims(field: str) -> None:
    with pytest.raises(StudyError):
        protocol(**{field: True})


def test_raw_strings_do_not_bypass_exact_control_types() -> None:
    with pytest.raises(StudyError, match="exact ControlCondition"):
        replace(protocol(), controls=("A_FAST_WEAK_COORDINATION",))  # type: ignore[arg-type]
