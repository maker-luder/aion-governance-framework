from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum


class StandardsCrosswalkError(ValueError):
    pass


class StandardContributionRole(StrEnum):
    VOCABULARY = "VOCABULARY"
    PROCESS_CONTROL = "PROCESS_CONTROL"
    EVIDENCE_QUALITY = "EVIDENCE_QUALITY"
    TECHNICAL_METHOD = "TECHNICAL_METHOD"
    CLAIM_LIMIT = "CLAIM_LIMIT"


class TevvTerm(StrEnum):
    TEST = "TEST"
    EVALUATION = "EVALUATION"
    VERIFICATION = "VERIFICATION"
    VALIDATION = "VALIDATION"


@dataclass(frozen=True, slots=True)
class ExternalStandardSource:
    standard_id: str
    title: str
    issuing_body: str
    version_or_date: str
    locator: str
    accessed_on: str
    contribution_roles: tuple[StandardContributionRole, ...]
    content_sha256: str

    def __post_init__(self) -> None:
        for name in ("standard_id", "title", "issuing_body", "version_or_date", "locator", "accessed_on"):
            if not getattr(self, name).strip():
                raise StandardsCrosswalkError(f"{name} is required")
        if not self.contribution_roles or len(set(self.contribution_roles)) != len(self.contribution_roles):
            raise StandardsCrosswalkError("contribution_roles must be non-empty and unique")
        if any(type(role) is not StandardContributionRole for role in self.contribution_roles):
            raise StandardsCrosswalkError("contribution_roles require exact enum values")
        if len(self.content_sha256) != 64 or any(c not in "0123456789abcdef" for c in self.content_sha256):
            raise StandardsCrosswalkError("content_sha256 must be lowercase 64-hex")


@dataclass(frozen=True, slots=True)
class FourDomainStandardBinding:
    binding_id: str
    standard_id: str
    human_construct_use: str
    machine_question_use: str
    engineering_operation_use: str
    governance_interpretation_use: str
    permitted_claim: str
    prohibited_promotion: str

    def __post_init__(self) -> None:
        for name in self.__dataclass_fields__:
            value = getattr(self, name)
            if not value.strip():
                raise StandardsCrosswalkError(f"{name} is required")


@dataclass(frozen=True, slots=True)
class SubjectivityConfoundRecord:
    confound_id: str
    human_construct: str
    machine_operationalization: str
    competing_explanations: tuple[str, ...]
    machine_equivalence: bool = False
    subjectivity_proxy: bool = False

    def __post_init__(self) -> None:
        if not self.confound_id.strip() or not self.human_construct.strip():
            raise StandardsCrosswalkError("confound id and human construct are required")
        if not self.machine_operationalization.strip():
            raise StandardsCrosswalkError("machine operationalization is required")
        if not self.competing_explanations or any(not item.strip() for item in self.competing_explanations):
            raise StandardsCrosswalkError("competing explanations are required")
        if type(self.machine_equivalence) is not bool or type(self.subjectivity_proxy) is not bool:
            raise StandardsCrosswalkError("confound flags must be exact bools")
        if self.machine_equivalence or self.subjectivity_proxy:
            raise StandardsCrosswalkError("human constructs cannot become machine equivalence or subjectivity proxies")


@dataclass(frozen=True, slots=True)
class TevvDefinition:
    term: TevvTerm
    question: str
    pass_criterion: str

    def __post_init__(self) -> None:
        if type(self.term) is not TevvTerm:
            raise StandardsCrosswalkError("TEVV term must be exact")
        if not self.question.strip() or not self.pass_criterion.strip():
            raise StandardsCrosswalkError("TEVV question and criterion are required")


@dataclass(frozen=True, slots=True)
class StandardsCrosswalkAudit:
    structurally_admissible: bool
    source_count: int
    binding_count: int
    confound_count: int
    tev_vocabulary_complete: bool
    reasons: tuple[str, ...]
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    moral_status_conclusion: str = "NOT_ESTABLISHED"
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False


class FourDomainStandardsRegistry:
    def audit(
        self,
        *,
        sources: tuple[ExternalStandardSource, ...],
        bindings: tuple[FourDomainStandardBinding, ...],
        confounds: tuple[SubjectivityConfoundRecord, ...],
        tev_vocabulary: tuple[TevvDefinition, ...],
    ) -> StandardsCrosswalkAudit:
        source_ids = [source.standard_id for source in sources]
        if not sources or len(source_ids) != len(set(source_ids)):
            raise StandardsCrosswalkError("standard sources must be non-empty and unique")
        binding_ids = [binding.binding_id for binding in bindings]
        if not bindings or len(binding_ids) != len(set(binding_ids)):
            raise StandardsCrosswalkError("bindings must be non-empty and unique")
        unknown = {binding.standard_id for binding in bindings} - set(source_ids)
        if unknown:
            raise StandardsCrosswalkError(f"unknown standard bindings: {sorted(unknown)}")
        if {item.term for item in tev_vocabulary} != set(TevvTerm):
            raise StandardsCrosswalkError("TEST EVALUATION VERIFICATION VALIDATION must remain distinct and complete")
        if len(tev_vocabulary) != len(TevvTerm):
            raise StandardsCrosswalkError("TEVV terms must occur exactly once")
        if not confounds:
            raise StandardsCrosswalkError("subjectivity confound register is required")
        roles = {role for source in sources for role in source.contribution_roles}
        if not {StandardContributionRole.PROCESS_CONTROL, StandardContributionRole.EVIDENCE_QUALITY}.issubset(roles):
            raise StandardsCrosswalkError("process-control and evidence-quality roles are required")
        return StandardsCrosswalkAudit(
            structurally_admissible=True,
            source_count=len(sources),
            binding_count=len(bindings),
            confound_count=len(confounds),
            tev_vocabulary_complete=True,
            reasons=(
                "EXTERNAL_STANDARD_ROLE_IS_EXPLICIT",
                "FOUR_DOMAIN_TRANSLATION_IS_COMPLETE",
                "TEVV_TERMS_REMAIN_DISTINCT",
                "HUMAN_CONSTRUCT_IS_NOT_A_MACHINE_ONTOLOGY_PROXY",
                "STANDARD_CONFORMANCE_DOES_NOT_ESTABLISH_SUBJECTIVITY",
            ),
        )


def payload_sha256(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def audit_fingerprint(audit: StandardsCrosswalkAudit) -> str:
    return hashlib.sha256(
        json.dumps(
            {
                "structurally_admissible": audit.structurally_admissible,
                "source_count": audit.source_count,
                "binding_count": audit.binding_count,
                "confound_count": audit.confound_count,
                "tev_vocabulary_complete": audit.tev_vocabulary_complete,
                "reasons": audit.reasons,
                "subjectivity_conclusion": audit.subjectivity_conclusion,
                "canonical_effect": audit.canonical_effect,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
