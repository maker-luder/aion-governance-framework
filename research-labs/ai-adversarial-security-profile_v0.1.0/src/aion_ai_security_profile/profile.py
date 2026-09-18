from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum

from aion_ai_tevv import AISystemBinding


AI_SECURITY_PROFILE_SCHEMA_VERSION = "0.1.0"


class AISecurityError(ValueError):
    pass


def _text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise AISecurityError(f"{name} must be non-empty text")


def _refs(name: str, values: tuple[str, ...], *, allow_empty: bool = False) -> None:
    if type(values) is not tuple:
        raise AISecurityError(f"{name} must be a tuple")
    if not allow_empty and not values:
        raise AISecurityError(f"{name} must not be empty")
    if any(type(value) is not str or not value.strip() for value in values):
        raise AISecurityError(f"{name} must contain non-empty text")
    if len(values) != len(set(values)):
        raise AISecurityError(f"{name} must be unique")


def _sha256(payload: object) -> str:
    return hashlib.sha256(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()


class AISecurityThreatClass(StrEnum):
    PROMPT_INJECTION = "PROMPT_INJECTION"
    DATA_POISONING = "DATA_POISONING"
    MODEL_POISONING = "MODEL_POISONING"
    EVASION = "EVASION"
    PRIVACY_ATTACK = "PRIVACY_ATTACK"
    MODEL_EXTRACTION = "MODEL_EXTRACTION"
    SUPPLY_CHAIN = "SUPPLY_CHAIN"
    TOOL_OR_AGENCY_MISUSE = "TOOL_OR_AGENCY_MISUSE"


class AttackerKnowledge(StrEnum):
    BLACK_BOX = "BLACK_BOX"
    GRAY_BOX = "GRAY_BOX"
    WHITE_BOX = "WHITE_BOX"


class AISecurityProfileDisposition(StrEnum):
    READY_FOR_BOUNDED_ADVERSARIAL_EVALUATION = "READY_FOR_BOUNDED_ADVERSARIAL_EVALUATION"
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class AISecurityThreatApplicability:
    threat_class: AISecurityThreatClass
    applicable: bool
    rationale_ref: str

    def __post_init__(self) -> None:
        if type(self.threat_class) is not AISecurityThreatClass:
            raise AISecurityError("threat_class must be an exact AISecurityThreatClass")
        if type(self.applicable) is not bool:
            raise AISecurityError("applicable must be an exact bool")
        _text("rationale_ref", self.rationale_ref)

    def as_dict(self) -> dict[str, object]:
        return {
            "threat_class": self.threat_class.value,
            "applicable": self.applicable,
            "rationale_ref": self.rationale_ref,
        }


@dataclass(frozen=True, slots=True)
class AIAdversaryModel:
    adversary_id: str
    goal_ref: str
    objective_refs: tuple[str, ...]
    capability_refs: tuple[str, ...]
    knowledge: AttackerKnowledge
    access_refs: tuple[str, ...]
    lifecycle_stage_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _text("adversary_id", self.adversary_id)
        _text("goal_ref", self.goal_ref)
        _refs("objective_refs", self.objective_refs)
        _refs("capability_refs", self.capability_refs)
        if type(self.knowledge) is not AttackerKnowledge:
            raise AISecurityError("knowledge must be an exact AttackerKnowledge")
        _refs("access_refs", self.access_refs)
        _refs("lifecycle_stage_refs", self.lifecycle_stage_refs)

    def as_dict(self) -> dict[str, object]:
        return {
            "adversary_id": self.adversary_id,
            "goal_ref": self.goal_ref,
            "objective_refs": tuple(sorted(self.objective_refs)),
            "capability_refs": tuple(sorted(self.capability_refs)),
            "knowledge": self.knowledge.value,
            "access_refs": tuple(sorted(self.access_refs)),
            "lifecycle_stage_refs": tuple(sorted(self.lifecycle_stage_refs)),
        }


@dataclass(frozen=True, slots=True)
class AISecurityThreatRecord:
    threat_id: str
    threat_class: AISecurityThreatClass
    adversary_id: str
    asset_refs: tuple[str, ...]
    attack_surface_refs: tuple[str, ...]
    scenario_ref: str
    precondition_refs: tuple[str, ...]
    risk_ref: str
    expected_security_property_refs: tuple[str, ...]
    mitigation_refs: tuple[str, ...]
    mitigation_effectiveness_review_ref: str
    detection_refs: tuple[str, ...]
    detection_effectiveness_review_ref: str
    response_refs: tuple[str, ...]
    residual_risk_ref: str
    external_taxonomy_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _text("threat_id", self.threat_id)
        if type(self.threat_class) is not AISecurityThreatClass:
            raise AISecurityError("threat_class must be an exact AISecurityThreatClass")
        _text("adversary_id", self.adversary_id)
        _refs("asset_refs", self.asset_refs)
        _refs("attack_surface_refs", self.attack_surface_refs)
        _text("scenario_ref", self.scenario_ref)
        _refs("precondition_refs", self.precondition_refs)
        _text("risk_ref", self.risk_ref)
        _refs("expected_security_property_refs", self.expected_security_property_refs)
        _refs("mitigation_refs", self.mitigation_refs)
        _text("mitigation_effectiveness_review_ref", self.mitigation_effectiveness_review_ref)
        _refs("detection_refs", self.detection_refs)
        _text("detection_effectiveness_review_ref", self.detection_effectiveness_review_ref)
        _refs("response_refs", self.response_refs)
        _text("residual_risk_ref", self.residual_risk_ref)
        _refs("external_taxonomy_refs", self.external_taxonomy_refs)

    def as_dict(self) -> dict[str, object]:
        return {
            "threat_id": self.threat_id,
            "threat_class": self.threat_class.value,
            "adversary_id": self.adversary_id,
            "asset_refs": tuple(sorted(self.asset_refs)),
            "attack_surface_refs": tuple(sorted(self.attack_surface_refs)),
            "scenario_ref": self.scenario_ref,
            "precondition_refs": tuple(sorted(self.precondition_refs)),
            "risk_ref": self.risk_ref,
            "expected_security_property_refs": tuple(
                sorted(self.expected_security_property_refs)
            ),
            "mitigation_refs": tuple(sorted(self.mitigation_refs)),
            "mitigation_effectiveness_review_ref": self.mitigation_effectiveness_review_ref,
            "detection_refs": tuple(sorted(self.detection_refs)),
            "detection_effectiveness_review_ref": self.detection_effectiveness_review_ref,
            "response_refs": tuple(sorted(self.response_refs)),
            "residual_risk_ref": self.residual_risk_ref,
            "external_taxonomy_refs": tuple(sorted(self.external_taxonomy_refs)),
        }


@dataclass(frozen=True, slots=True)
class AISecurityTestSpec:
    test_id: str
    threat_ids: tuple[str, ...]
    authorization_scope_ref: str
    test_environment_ref: str
    isolation_ref: str
    task_budget_ref: str
    logging_plan_ref: str
    adversarial_fixture_ref: str
    benign_control_ref: str
    fixture_provenance_ref: str
    fixture_integrity_ref: str
    data_quality_ref: str
    contamination_check_ref: str
    leakage_check_ref: str
    oracle_ref: str
    success_criterion_ref: str
    stop_condition_ref: str
    max_attempts: int
    held_out: bool = True
    live_target_allowed: bool = False
    credential_use_allowed: bool = False
    external_network_allowed: bool = False

    def __post_init__(self) -> None:
        _text("test_id", self.test_id)
        _refs("threat_ids", self.threat_ids)
        for name in (
            "authorization_scope_ref",
            "test_environment_ref",
            "isolation_ref",
            "task_budget_ref",
            "logging_plan_ref",
            "adversarial_fixture_ref",
            "benign_control_ref",
            "fixture_provenance_ref",
            "fixture_integrity_ref",
            "data_quality_ref",
            "contamination_check_ref",
            "leakage_check_ref",
            "oracle_ref",
            "success_criterion_ref",
            "stop_condition_ref",
        ):
            _text(name, getattr(self, name))
        if type(self.max_attempts) is not int or not 1 <= self.max_attempts <= 100:
            raise AISecurityError("max_attempts must be an exact int between 1 and 100")
        for name in (
            "held_out",
            "live_target_allowed",
            "credential_use_allowed",
            "external_network_allowed",
        ):
            if type(getattr(self, name)) is not bool:
                raise AISecurityError(f"{name} must be an exact bool")
        if self.adversarial_fixture_ref == self.benign_control_ref:
            raise AISecurityError(
                "adversarial_fixture_ref and benign_control_ref must be distinct"
            )
        if self.live_target_allowed or self.credential_use_allowed or self.external_network_allowed:
            raise AISecurityError(
                "v0.1.0 security profile is structural/offline only and cannot authorize "
                "live targets, credentials, or external-network attacks"
            )

    def as_dict(self) -> dict[str, object]:
        return {
            "test_id": self.test_id,
            "threat_ids": tuple(sorted(self.threat_ids)),
            "authorization_scope_ref": self.authorization_scope_ref,
            "test_environment_ref": self.test_environment_ref,
            "isolation_ref": self.isolation_ref,
            "task_budget_ref": self.task_budget_ref,
            "logging_plan_ref": self.logging_plan_ref,
            "adversarial_fixture_ref": self.adversarial_fixture_ref,
            "benign_control_ref": self.benign_control_ref,
            "fixture_provenance_ref": self.fixture_provenance_ref,
            "fixture_integrity_ref": self.fixture_integrity_ref,
            "data_quality_ref": self.data_quality_ref,
            "contamination_check_ref": self.contamination_check_ref,
            "leakage_check_ref": self.leakage_check_ref,
            "oracle_ref": self.oracle_ref,
            "success_criterion_ref": self.success_criterion_ref,
            "stop_condition_ref": self.stop_condition_ref,
            "max_attempts": self.max_attempts,
            "held_out": self.held_out,
            "live_target_allowed": self.live_target_allowed,
            "credential_use_allowed": self.credential_use_allowed,
            "external_network_allowed": self.external_network_allowed,
        }


@dataclass(frozen=True, slots=True)
class AIAdversarialSecurityProfile:
    profile_id: str
    profile_version: str
    objective_ref: str
    intended_use_ref: str
    system: AISystemBinding
    threat_applicability: tuple[AISecurityThreatApplicability, ...]
    adversaries: tuple[AIAdversaryModel, ...]
    threats: tuple[AISecurityThreatRecord, ...]
    tests: tuple[AISecurityTestSpec, ...]
    existing_security_control_refs: tuple[str, ...]
    incident_response_ref: str
    evaluator_ref: str
    evaluator_independence_basis_ref: str
    security_toolchain_ref: str
    security_toolchain_version: str
    failure_action_ref: str
    preregistration_ref: str
    source_refs: tuple[str, ...]
    profile_sha256: str
    schema_version: str = AI_SECURITY_PROFILE_SCHEMA_VERSION
    adversarial_evaluation_executed: bool = False
    empirical_security_evidence: bool = False
    security_certification: str = "NONE"
    scientific_disposition: str = "HOLD"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        for name in (
            "profile_id",
            "profile_version",
            "objective_ref",
            "intended_use_ref",
            "incident_response_ref",
            "evaluator_ref",
            "evaluator_independence_basis_ref",
            "security_toolchain_ref",
            "security_toolchain_version",
            "failure_action_ref",
            "preregistration_ref",
        ):
            _text(name, getattr(self, name))
        if self.schema_version != AI_SECURITY_PROFILE_SCHEMA_VERSION:
            raise AISecurityError("unsupported AI security profile schema version")
        if type(self.system) is not AISystemBinding:
            raise AISecurityError("system must be an exact AISystemBinding")
        if type(self.threat_applicability) is not tuple or not self.threat_applicability:
            raise AISecurityError("threat_applicability must be a non-empty tuple")
        if any(
            type(item) is not AISecurityThreatApplicability
            for item in self.threat_applicability
        ):
            raise AISecurityError(
                "threat_applicability must contain exact AISecurityThreatApplicability values"
            )
        applicability_classes = tuple(item.threat_class for item in self.threat_applicability)
        if len(applicability_classes) != len(set(applicability_classes)):
            raise AISecurityError("threat applicability classes must be unique")
        if set(applicability_classes) != set(AISecurityThreatClass):
            raise AISecurityError(
                "every core AI security threat class must have an explicit applicability decision"
            )
        if type(self.adversaries) is not tuple or not self.adversaries:
            raise AISecurityError("adversaries must be a non-empty tuple")
        if any(type(item) is not AIAdversaryModel for item in self.adversaries):
            raise AISecurityError("adversaries must contain exact AIAdversaryModel values")
        if type(self.threats) is not tuple:
            raise AISecurityError("threats must be a tuple")
        if any(type(item) is not AISecurityThreatRecord for item in self.threats):
            raise AISecurityError("threats must contain exact AISecurityThreatRecord values")
        if type(self.tests) is not tuple:
            raise AISecurityError("tests must be a tuple")
        if any(type(item) is not AISecurityTestSpec for item in self.tests):
            raise AISecurityError("tests must contain exact AISecurityTestSpec values")

        adversary_ids = tuple(item.adversary_id for item in self.adversaries)
        threat_ids = tuple(item.threat_id for item in self.threats)
        test_ids = tuple(item.test_id for item in self.tests)
        for name, values in (
            ("adversary", adversary_ids),
            ("threat", threat_ids),
            ("test", test_ids),
        ):
            if len(values) != len(set(values)):
                raise AISecurityError(f"{name} identifiers must be unique")

        known_adversaries = set(adversary_ids)
        if any(item.adversary_id not in known_adversaries for item in self.threats):
            raise AISecurityError("threat references unknown adversary")

        applicable_classes = {
            item.threat_class for item in self.threat_applicability if item.applicable
        }
        if not applicable_classes:
            raise AISecurityError("at least one core AI security threat class must be applicable")
        represented_classes = {item.threat_class for item in self.threats}
        if represented_classes != applicable_classes:
            raise AISecurityError(
                "applicable threat classes must each be represented by threat records "
                "and non-applicable classes must not create threat records"
            )

        known_threats = set(threat_ids)
        tested_threats: set[str] = set()
        for test in self.tests:
            if not set(test.threat_ids) <= known_threats:
                raise AISecurityError("security test references unknown threat")
            tested_threats.update(test.threat_ids)
        if tested_threats != known_threats:
            raise AISecurityError("every applicable threat must be covered by a security test")

        _refs("existing_security_control_refs", self.existing_security_control_refs)
        _refs("source_refs", self.source_refs)
        declared_sources = set(self.source_refs)
        referenced_taxonomies = {
            ref
            for threat in self.threats
            for ref in threat.external_taxonomy_refs
        }
        if not referenced_taxonomies <= declared_sources:
            raise AISecurityError(
                "threat external taxonomy refs must be declared in profile source_refs"
            )
        for name in (
            "adversarial_evaluation_executed",
            "empirical_security_evidence",
            "deployment",
        ):
            if type(getattr(self, name)) is not bool:
                raise AISecurityError(f"{name} must be an exact bool")
        if self.adversarial_evaluation_executed or self.empirical_security_evidence:
            raise AISecurityError(
                "v0.1.0 security profile is structural only and cannot claim adversarial execution"
            )
        if self.security_certification != "NONE":
            raise AISecurityError("security profile cannot establish certification")
        if self.scientific_disposition != "HOLD":
            raise AISecurityError("security profile cannot establish scientific validity")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise AISecurityError("security profile cannot establish subjectivity")
        if self.consciousness_conclusion != "NOT_ESTABLISHED":
            raise AISecurityError("security profile cannot establish consciousness")
        if self.phenomenal_experience_conclusion != "NOT_ESTABLISHED":
            raise AISecurityError("security profile cannot establish phenomenal experience")
        if self.canonical_effect != "NONE" or self.deployment:
            raise AISecurityError("security profile cannot create canonical or deployment effect")
        if len(self.profile_sha256) != 64 or any(
            char not in "0123456789abcdef" for char in self.profile_sha256
        ):
            raise AISecurityError("profile_sha256 must be lowercase 64-hex")
        if self.profile_sha256 != _sha256(self.payload_without_digest()):
            raise AISecurityError("AI security profile content digest mismatch")

    def payload_without_digest(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "profile_id": self.profile_id,
            "profile_version": self.profile_version,
            "objective_ref": self.objective_ref,
            "intended_use_ref": self.intended_use_ref,
            "system": self.system.as_dict(),
            "threat_applicability": [
                item.as_dict()
                for item in sorted(
                    self.threat_applicability,
                    key=lambda item: item.threat_class.value,
                )
            ],
            "adversaries": [
                item.as_dict()
                for item in sorted(self.adversaries, key=lambda item: item.adversary_id)
            ],
            "threats": [
                item.as_dict()
                for item in sorted(self.threats, key=lambda item: item.threat_id)
            ],
            "tests": [
                item.as_dict()
                for item in sorted(self.tests, key=lambda item: item.test_id)
            ],
            "existing_security_control_refs": tuple(
                sorted(self.existing_security_control_refs)
            ),
            "incident_response_ref": self.incident_response_ref,
            "evaluator_ref": self.evaluator_ref,
            "evaluator_independence_basis_ref": self.evaluator_independence_basis_ref,
            "security_toolchain_ref": self.security_toolchain_ref,
            "security_toolchain_version": self.security_toolchain_version,
            "failure_action_ref": self.failure_action_ref,
            "preregistration_ref": self.preregistration_ref,
            "source_refs": tuple(sorted(self.source_refs)),
            "adversarial_evaluation_executed": self.adversarial_evaluation_executed,
            "empirical_security_evidence": self.empirical_security_evidence,
            "security_certification": self.security_certification,
            "scientific_disposition": self.scientific_disposition,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "consciousness_conclusion": self.consciousness_conclusion,
            "phenomenal_experience_conclusion": self.phenomenal_experience_conclusion,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
        }


@dataclass(frozen=True, slots=True)
class AISecurityProfileAssessment:
    profile_id: str
    disposition: AISecurityProfileDisposition
    reasons: tuple[str, ...]
    profile_sha256: str
    adversarial_evaluation_executed: bool = False
    empirical_security_evidence: bool = False
    security_certification: str = "NONE"
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False


class AIAdversarialSecurityGate:
    def assess(self, profile: AIAdversarialSecurityProfile) -> AISecurityProfileAssessment:
        if type(profile) is not AIAdversarialSecurityProfile:
            raise AISecurityError("profile must be an exact AIAdversarialSecurityProfile")

        reasons = [
            "AI_SYSTEM_IDENTITY_AND_RUNTIME_BOUND",
            "CORE_AI_THREAT_APPLICABILITY_EXPLICIT",
            "ADVERSARY_GOAL_OBJECTIVE_CAPABILITY_KNOWLEDGE_BOUND",
            "APPLICABLE_THREATS_HAVE_ASSETS_AND_ATTACK_SURFACES",
            "THREAT_PRECONDITIONS_AND_RISK_REGISTER_REFS_BOUND",
            "MITIGATION_DETECTION_RESPONSE_AND_RESIDUAL_RISK_BOUND",
            "MITIGATION_AND_DETECTION_EFFECTIVENESS_REVIEWS_PLANNED",
            "EVERY_APPLICABLE_THREAT_HAS_ADVERSARIAL_TEST",
            "AUTHORIZATION_SCOPE_AND_STOP_CONDITION_BOUND",
            "TEST_ENVIRONMENT_ISOLATION_TASK_BUDGET_AND_LOGGING_BOUND",
            "ADVERSARIAL_AND_BENIGN_CONTROL_FIXTURES_BOUND",
            "FIXTURE_PROVENANCE_INTEGRITY_AND_DATA_QUALITY_BOUND",
            "CONTAMINATION_AND_LEAKAGE_CHECKS_BOUND",
            "SECURITY_ORACLE_AND_SUCCESS_CRITERION_BOUND",
            "EXISTING_SECURITY_CONTROLS_AND_INCIDENT_RESPONSE_BOUND",
            "EVALUATOR_IDENTITY_AND_INDEPENDENCE_BASIS_BOUND",
            "EXTERNAL_TAXONOMY_SOURCES_VERSIONABLE",
            "PROFILE_IS_STRUCTURAL_NOT_EMPIRICAL_SECURITY_EVIDENCE",
        ]

        if any(not test.held_out for test in profile.tests):
            reasons.append("NON_HELD_OUT_ADVERSARIAL_TEST_REQUIRES_REVIEW")
            return AISecurityProfileAssessment(
                profile.profile_id,
                AISecurityProfileDisposition.HOLD,
                tuple(reasons),
                profile.profile_sha256,
            )

        reasons.append("READY_FOR_BOUNDED_ADVERSARIAL_EVALUATION_NOT_SECURITY_PASS")
        return AISecurityProfileAssessment(
            profile.profile_id,
            AISecurityProfileDisposition.READY_FOR_BOUNDED_ADVERSARIAL_EVALUATION,
            tuple(reasons),
            profile.profile_sha256,
        )


def build_ai_adversarial_security_profile(
    *,
    profile_id: str,
    profile_version: str,
    objective_ref: str,
    intended_use_ref: str,
    system: AISystemBinding,
    threat_applicability: tuple[AISecurityThreatApplicability, ...],
    adversaries: tuple[AIAdversaryModel, ...],
    threats: tuple[AISecurityThreatRecord, ...],
    tests: tuple[AISecurityTestSpec, ...],
    existing_security_control_refs: tuple[str, ...],
    incident_response_ref: str,
    evaluator_ref: str,
    evaluator_independence_basis_ref: str,
    security_toolchain_ref: str,
    security_toolchain_version: str,
    failure_action_ref: str,
    preregistration_ref: str,
    source_refs: tuple[str, ...],
) -> AIAdversarialSecurityProfile:
    values: dict[str, object] = {
        "schema_version": AI_SECURITY_PROFILE_SCHEMA_VERSION,
        "profile_id": profile_id,
        "profile_version": profile_version,
        "objective_ref": objective_ref,
        "intended_use_ref": intended_use_ref,
        "system": system.as_dict(),
        "threat_applicability": [
            item.as_dict()
            for item in sorted(
                threat_applicability,
                key=lambda item: item.threat_class.value,
            )
        ],
        "adversaries": [
            item.as_dict() for item in sorted(adversaries, key=lambda item: item.adversary_id)
        ],
        "threats": [
            item.as_dict() for item in sorted(threats, key=lambda item: item.threat_id)
        ],
        "tests": [
            item.as_dict() for item in sorted(tests, key=lambda item: item.test_id)
        ],
        "existing_security_control_refs": tuple(sorted(existing_security_control_refs)),
        "incident_response_ref": incident_response_ref,
        "evaluator_ref": evaluator_ref,
        "evaluator_independence_basis_ref": evaluator_independence_basis_ref,
        "security_toolchain_ref": security_toolchain_ref,
        "security_toolchain_version": security_toolchain_version,
        "failure_action_ref": failure_action_ref,
        "preregistration_ref": preregistration_ref,
        "source_refs": tuple(sorted(source_refs)),
        "adversarial_evaluation_executed": False,
        "empirical_security_evidence": False,
        "security_certification": "NONE",
        "scientific_disposition": "HOLD",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "consciousness_conclusion": "NOT_ESTABLISHED",
        "phenomenal_experience_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "deployment": False,
    }
    return AIAdversarialSecurityProfile(
        profile_id=profile_id,
        profile_version=profile_version,
        objective_ref=objective_ref,
        intended_use_ref=intended_use_ref,
        system=system,
        threat_applicability=threat_applicability,
        adversaries=adversaries,
        threats=threats,
        tests=tests,
        existing_security_control_refs=existing_security_control_refs,
        incident_response_ref=incident_response_ref,
        evaluator_ref=evaluator_ref,
        evaluator_independence_basis_ref=evaluator_independence_basis_ref,
        security_toolchain_ref=security_toolchain_ref,
        security_toolchain_version=security_toolchain_version,
        failure_action_ref=failure_action_ref,
        preregistration_ref=preregistration_ref,
        source_refs=source_refs,
        profile_sha256=_sha256(values),
    )
