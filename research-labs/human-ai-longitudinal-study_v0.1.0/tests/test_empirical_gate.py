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
    item, evidence = bound_protocol()
    audit = audit_empirical_protocol(item, evidence=evidence)
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
    item, evidence = bound_protocol(
        preregistered=False,
        preregistration_ref="",
        preregistration_sha256="",
    )
    audit = audit_empirical_protocol(item, evidence=evidence)
    assert audit.pilot_gate_ready is True
    assert audit.confirmatory_gate_ready is False
    assert audit.preregistration_binding_present is False


def test_real_participant_material_requires_consent_and_ethics_routes() -> None:
    with pytest.raises(StudyError, match="consent_route"):
        protocol(contains_real_participant_data=True)

    item, evidence = bound_protocol(
        contains_real_participant_data=True,
        consent_route="APPROVED_CONSENT_ROUTE",
        ethics_route="APPLICABLE_REVIEW_ROUTE",
    )
    assert audit_empirical_protocol(item, evidence=evidence).confirmatory_gate_ready is True


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


def test_digest_strings_without_content_do_not_open_gates() -> None:
    audit = audit_empirical_protocol(protocol())
    assert audit.pilot_gate_ready is False
    assert audit.confirmatory_gate_ready is False
    assert audit.agreement_rule_predeclared is False
    assert audit.preregistration_binding_present is False
    assert audit.protocol_freeze_binding_present is False


def bound_protocol(**overrides: object):
    import hashlib
    import json
    from dataclasses import asdict

    item = protocol(**overrides)
    evidence = {
        "corpus_manifest_sha256": b"synthetic corpus manifest",
        "coding_manual_sha256": b"synthetic coding manual",
        "analysis_plan_sha256": b"synthetic analysis plan",
        "agreement_rule_sha256": item.agreement_acceptance_rule.encode("utf-8"),
    }
    if item.preregistered:
        evidence["preregistration_sha256"] = b"synthetic preregistration; not external registration"
    item = replace(item, **{k: hashlib.sha256(v).hexdigest() for k, v in evidence.items()})
    payload = asdict(item)
    payload.pop("protocol_sha256")
    payload.pop("protocol_freeze_receipt_sha256")
    evidence["protocol_sha256"] = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    item = replace(item, protocol_sha256=hashlib.sha256(evidence["protocol_sha256"]).hexdigest())
    if item.protocol_frozen:
        evidence["protocol_freeze_receipt_sha256"] = json.dumps(
            {
                "protocol_id": item.protocol_id,
                "protocol_sha256": item.protocol_sha256,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        item = replace(
            item, protocol_freeze_receipt_sha256=hashlib.sha256(evidence["protocol_freeze_receipt_sha256"]).hexdigest()
        )
    return item, evidence


def test_matching_content_opens_only_technical_method_gates() -> None:
    item, evidence = bound_protocol()
    audit = audit_empirical_protocol(item, evidence=evidence)
    assert audit.pilot_gate_ready and audit.confirmatory_gate_ready
    assert audit.scientific_disposition is AdmissionDisposition.HOLD
    assert audit.ccts_empirical_validation == "NOT_ESTABLISHED"


@pytest.mark.parametrize(
    "field",
    [
        "protocol_sha256",
        "corpus_manifest_sha256",
        "coding_manual_sha256",
        "analysis_plan_sha256",
        "agreement_rule_sha256",
        "preregistration_sha256",
        "protocol_freeze_receipt_sha256",
    ],
)
def test_changed_or_missing_content_fails_closed(field: str) -> None:
    item, evidence = bound_protocol()
    evidence[field] += b"changed"
    with pytest.raises(StudyError, match="content"):
        audit_empirical_protocol(item, evidence=evidence)
    del evidence[field]
    audit = audit_empirical_protocol(item, evidence=evidence)
    assert audit.confirmatory_gate_ready is False


def test_changed_protocol_fields_cannot_reuse_old_evidence() -> None:
    item, evidence = bound_protocol()
    item = replace(item, primary_contrast="changed contrast")
    with pytest.raises(StudyError, match="protocol content"):
        audit_empirical_protocol(item, evidence=evidence)


def test_freeze_receipt_for_other_protocol_is_rejected() -> None:
    import hashlib

    item, evidence = bound_protocol()
    evidence["protocol_freeze_receipt_sha256"] = b'{"protocol_id":"other","protocol_sha256":"other"}'
    item = replace(
        item, protocol_freeze_receipt_sha256=hashlib.sha256(evidence["protocol_freeze_receipt_sha256"]).hexdigest()
    )
    with pytest.raises(StudyError, match="freeze receipt"):
        audit_empirical_protocol(item, evidence=evidence)


def test_pilot_content_without_preregistration_keeps_confirmatory_gate_closed() -> None:
    item, evidence = bound_protocol(preregistered=False, preregistration_ref="", preregistration_sha256="")
    audit = audit_empirical_protocol(item, evidence=evidence)
    assert audit.pilot_gate_ready is True
    assert audit.confirmatory_gate_ready is False


def test_rehashed_other_agreement_rule_is_rejected() -> None:
    import hashlib

    item, evidence = bound_protocol()
    evidence["agreement_rule_sha256"] = b"other rule"
    item = replace(item, agreement_rule_sha256=hashlib.sha256(b"other rule").hexdigest())
    del evidence["protocol_sha256"]
    with pytest.raises(StudyError, match="agreement rule content"):
        audit_empirical_protocol(item, evidence=evidence)


@pytest.mark.parametrize("bad", [b"", "text", bytearray(b"bytes"), None])
def test_evidence_requires_nonempty_immutable_bytes(bad: object) -> None:
    item, evidence = bound_protocol()
    evidence["coding_manual_sha256"] = bad
    with pytest.raises(StudyError, match="content"):
        audit_empirical_protocol(item, evidence=evidence)


@pytest.mark.parametrize("bad", [[], "evidence", 1])
def test_evidence_container_must_be_exact_dict(bad: object) -> None:
    with pytest.raises(StudyError, match="exact dict"):
        audit_empirical_protocol(protocol(), evidence=bad)


def test_unknown_evidence_key_is_rejected() -> None:
    with pytest.raises(StudyError, match="unknown evidence"):
        audit_empirical_protocol(protocol(), evidence={"unknown": b"content"})
