from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from enum import StrEnum

from .harness import AdmissionDisposition, StudyError

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class ControlCondition(StrEnum):
    A_FAST_WEAK_COORDINATION = "A_FAST_WEAK_COORDINATION"
    B_SLOW_STRONG_COORDINATION = "B_SLOW_STRONG_COORDINATION"
    C_HIGH_THROUGHPUT_HIGH_COORDINATION = "C_HIGH_THROUGHPUT_HIGH_COORDINATION"
    D_HIGH_THROUGHPUT_QUALITY_COLLAPSE = "D_HIGH_THROUGHPUT_QUALITY_COLLAPSE"


class ConstructFalsifier(StrEnum):
    F1 = "F1"
    F2 = "F2"
    F3 = "F3"
    F4 = "F4"
    F5 = "F5"
    F6 = "F6"
    F7 = "F7"
    F8 = "F8"
    F9 = "F9"
    F10 = "F10"


class InterCoderAgreementMethod(StrEnum):
    KRIPPENDORFF_ALPHA = "KRIPPENDORFF_ALPHA"
    COHEN_KAPPA = "COHEN_KAPPA"
    FLEISS_KAPPA = "FLEISS_KAPPA"
    INTRACLASS_CORRELATION = "INTRACLASS_CORRELATION"


def _text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise StudyError(f"{name} must be non-empty text")


def _digest(name: str, value: str) -> None:
    if type(value) is not str or _SHA256.fullmatch(value) is None:
        raise StudyError(f"{name} must be a lowercase SHA-256 digest")


def _unique_non_empty(name: str, values: tuple[str, ...]) -> None:
    if type(values) is not tuple or not values:
        raise StudyError(f"{name} must be a non-empty tuple")
    if any(type(item) is not str or not item.strip() for item in values):
        raise StudyError(f"{name} must contain non-empty text")
    if len(values) != len(set(values)):
        raise StudyError(f"{name} must be unique")


@dataclass(frozen=True, slots=True)
class EmpiricalProtocol:
    protocol_id: str
    protocol_sha256: str
    corpus_manifest_sha256: str
    coding_manual_sha256: str
    analysis_plan_sha256: str
    primary_contrast: str
    pilot_unit_ids: tuple[str, ...]
    confirmatory_unit_ids: tuple[str, ...]
    controls: tuple[ControlCondition, ...]
    falsifiers: tuple[ConstructFalsifier, ...]
    minimum_independent_coders: int
    agreement_method: InterCoderAgreementMethod
    agreement_acceptance_rule: str
    agreement_rule_sha256: str
    preregistration_ref: str
    preregistration_sha256: str
    protocol_freeze_receipt_sha256: str
    consent_route: str
    ethics_route: str
    preregistered: bool
    protocol_frozen: bool
    ccts_status_is_htecr_eligibility_gate: bool = False
    contains_real_participant_data: bool = False
    claims_ccts_empirical_validation: bool = False
    claims_htecr_validation: bool = False
    claims_human_learning_effect: bool = False
    claims_subjectivity: bool = False
    claims_consciousness: bool = False
    claims_phenomenal_experience: bool = False
    claims_moral_agency: bool = False
    claims_moral_status: bool = False

    def __post_init__(self) -> None:
        _text("protocol_id", self.protocol_id)
        for name in (
            "protocol_sha256",
            "corpus_manifest_sha256",
            "coding_manual_sha256",
            "analysis_plan_sha256",
            "agreement_rule_sha256",
        ):
            _digest(name, getattr(self, name))

        _text("primary_contrast", self.primary_contrast)
        _unique_non_empty("pilot_unit_ids", self.pilot_unit_ids)
        _unique_non_empty("confirmatory_unit_ids", self.confirmatory_unit_ids)
        if set(self.pilot_unit_ids) & set(self.confirmatory_unit_ids):
            raise StudyError("pilot and confirmatory unit ids must be disjoint")

        if type(self.controls) is not tuple or any(type(item) is not ControlCondition for item in self.controls):
            raise StudyError("controls must be exact ControlCondition values")
        if set(self.controls) != set(ControlCondition):
            raise StudyError("controls must include the complete A-D negative-control set")

        if type(self.falsifiers) is not tuple or any(type(item) is not ConstructFalsifier for item in self.falsifiers):
            raise StudyError("falsifiers must be exact ConstructFalsifier values")
        if set(self.falsifiers) != set(ConstructFalsifier):
            raise StudyError("falsifiers must include F1-F10")

        if type(self.minimum_independent_coders) is not int or self.minimum_independent_coders < 2:
            raise StudyError("at least two independent coders must be planned")
        if type(self.agreement_method) is not InterCoderAgreementMethod:
            raise StudyError("agreement_method must be an exact InterCoderAgreementMethod")
        _text("agreement_acceptance_rule", self.agreement_acceptance_rule)

        for name in (
            "preregistered",
            "protocol_frozen",
            "ccts_status_is_htecr_eligibility_gate",
            "contains_real_participant_data",
            "claims_ccts_empirical_validation",
            "claims_htecr_validation",
            "claims_human_learning_effect",
            "claims_subjectivity",
            "claims_consciousness",
            "claims_phenomenal_experience",
            "claims_moral_agency",
            "claims_moral_status",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")

        if self.preregistered:
            _text("preregistration_ref", self.preregistration_ref)
            _digest("preregistration_sha256", self.preregistration_sha256)
        elif self.preregistration_ref or self.preregistration_sha256:
            raise StudyError("preregistration binding cannot be present when preregistered is false")

        if self.protocol_frozen:
            _digest(
                "protocol_freeze_receipt_sha256",
                self.protocol_freeze_receipt_sha256,
            )
        elif self.protocol_freeze_receipt_sha256:
            raise StudyError("protocol freeze receipt cannot be present when protocol_frozen is false")

        if self.ccts_status_is_htecr_eligibility_gate:
            raise StudyError("CCTS structural status cannot gate HTECR measurement eligibility")

        promoted = {
            "CCTS empirical validation": self.claims_ccts_empirical_validation,
            "HTECR validation": self.claims_htecr_validation,
            "Human learning effect": self.claims_human_learning_effect,
            "subjectivity": self.claims_subjectivity,
            "consciousness": self.claims_consciousness,
            "phenomenal experience": self.claims_phenomenal_experience,
            "moral agency": self.claims_moral_agency,
            "moral status": self.claims_moral_status,
        }
        for label, enabled in promoted.items():
            if enabled:
                raise StudyError(f"protocol infrastructure cannot establish {label}")

        if self.contains_real_participant_data:
            _text("consent_route", self.consent_route)
            _text("ethics_route", self.ethics_route)


@dataclass(frozen=True, slots=True)
class EmpiricalGateAudit:
    protocol_id: str
    pilot_gate_ready: bool
    confirmatory_gate_ready: bool
    htecr_measurement_independent_of_ccts_admission: bool
    complete_negative_controls: bool
    complete_falsifier_set: bool
    independent_coder_plan_present: bool
    agreement_rule_predeclared: bool
    preregistration_binding_present: bool
    protocol_freeze_binding_present: bool
    empirical_data_collected: bool = False
    ccts_empirical_validation: str = "NOT_ESTABLISHED"
    htecr_validation: str = "NOT_ESTABLISHED"
    human_learning_effect: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    moral_agency: str = "NOT_ESTABLISHED"
    moral_status: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


def audit_empirical_protocol(
    protocol: EmpiricalProtocol, *, evidence: dict[str, bytes] | None = None
) -> EmpiricalGateAudit:
    """Check supplied bytes; readiness is not authenticated Human approval.

    Evidence keys name digest fields. Protocol JSON is canonical UTF-8 JSON
    (sorted keys, compact separators, ensure_ascii=False), excluding its own
    digest and the freeze receipt digest to avoid a circular hash dependency.
    The freeze receipt must name this protocol ID and verified protocol digest.
    """
    if type(protocol) is not EmpiricalProtocol:
        raise StudyError("protocol must be an exact EmpiricalProtocol")

    if evidence is None:
        evidence = {}
    if type(evidence) is not dict:
        raise StudyError("evidence must be an exact dict of content bytes")
    fields = (
        "protocol_sha256",
        "corpus_manifest_sha256",
        "coding_manual_sha256",
        "analysis_plan_sha256",
        "agreement_rule_sha256",
        "preregistration_sha256",
        "protocol_freeze_receipt_sha256",
    )
    if any(type(key) is not str or key not in fields for key in evidence):
        raise StudyError("unknown evidence content field")
    verified: set[str] = set()
    for name, content in evidence.items():
        if type(content) is not bytes or not content:
            raise StudyError(f"{name} content must be non-empty bytes")
        if hashlib.sha256(content).hexdigest() != getattr(protocol, name):
            raise StudyError(f"{name} content digest mismatch")
        verified.add(name)

    if "protocol_sha256" in verified:
        payload = asdict(protocol)
        del payload["protocol_sha256"]
        del payload["protocol_freeze_receipt_sha256"]
        expected = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        if evidence["protocol_sha256"] != expected:
            raise StudyError("protocol content does not match current protocol fields")
    if "agreement_rule_sha256" in verified:
        if evidence["agreement_rule_sha256"] != protocol.agreement_acceptance_rule.encode("utf-8"):
            raise StudyError("agreement rule content does not match declared rule")
    if "protocol_freeze_receipt_sha256" in verified:
        try:
            receipt = json.loads(evidence["protocol_freeze_receipt_sha256"])
        except (ValueError, UnicodeError) as exc:
            raise StudyError("freeze receipt content must be JSON") from exc
        if type(receipt) is not dict or receipt != {
            "protocol_id": protocol.protocol_id,
            "protocol_sha256": protocol.protocol_sha256,
        }:
            raise StudyError("freeze receipt must bind the current protocol")

    core_bound = set(fields[:4]).issubset(verified)
    freeze_binding = protocol.protocol_frozen and core_bound and ("protocol_freeze_receipt_sha256" in verified)
    prereg_binding = protocol.preregistered and core_bound and ("preregistration_sha256" in verified)
    agreement_bound = core_bound and "agreement_rule_sha256" in verified

    pilot_ready = freeze_binding and agreement_bound
    confirmatory_ready = pilot_ready and prereg_binding
    if protocol.contains_real_participant_data:
        confirmatory_ready = confirmatory_ready and bool(
            protocol.consent_route.strip() and protocol.ethics_route.strip()
        )

    return EmpiricalGateAudit(
        protocol_id=protocol.protocol_id,
        pilot_gate_ready=pilot_ready,
        confirmatory_gate_ready=confirmatory_ready,
        htecr_measurement_independent_of_ccts_admission=True,
        complete_negative_controls=set(protocol.controls) == set(ControlCondition),
        complete_falsifier_set=set(protocol.falsifiers) == set(ConstructFalsifier),
        independent_coder_plan_present=protocol.minimum_independent_coders >= 2,
        agreement_rule_predeclared=agreement_bound,
        preregistration_binding_present=prereg_binding,
        protocol_freeze_binding_present=freeze_binding,
    )
