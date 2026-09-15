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
        if len(set(self.competing_explanations)) != len(self.competing_explanations):
            raise StandardsCrosswalkError("competing explanations must be unique")
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
    model_invoked: bool = False
    evidence_admissibility: str = "PROCESS_CONTROL_ONLY"
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
        source_payloads: dict[str, str],
        bindings: tuple[FourDomainStandardBinding, ...],
        confounds: tuple[SubjectivityConfoundRecord, ...],
        tev_vocabulary: tuple[TevvDefinition, ...],
    ) -> StandardsCrosswalkAudit:
        source_ids = [source.standard_id for source in sources]
        if not sources or len(source_ids) != len(set(source_ids)):
            raise StandardsCrosswalkError("standard sources must be non-empty and unique")
        if type(source_payloads) is not dict or any(
            type(key) is not str or type(value) is not str for key, value in source_payloads.items()
        ):
            raise StandardsCrosswalkError("source_payloads must be an exact string mapping")
        if set(source_payloads) != set(source_ids):
            raise StandardsCrosswalkError("source_payloads must cover every declared standard exactly")
        for source in sources:
            if payload_sha256(source_payloads[source.standard_id]) != source.content_sha256:
                raise StandardsCrosswalkError(
                    f"content hash mismatch for standard source: {source.standard_id}"
                )

        binding_ids = [binding.binding_id for binding in bindings]
        if not bindings or len(binding_ids) != len(set(binding_ids)):
            raise StandardsCrosswalkError("bindings must be non-empty and unique")
        bound_source_ids = {binding.standard_id for binding in bindings}
        unknown = bound_source_ids - set(source_ids)
        if unknown:
            raise StandardsCrosswalkError(f"unknown standard bindings: {sorted(unknown)}")
        unbound = set(source_ids) - bound_source_ids
        if unbound:
            raise StandardsCrosswalkError(f"standard sources require Four-Domain bindings: {sorted(unbound)}")
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
                "SOURCE_CONTENT_HASHES_VERIFIED",
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
                "model_invoked": audit.model_invoked,
                "evidence_admissibility": audit.evidence_admissibility,
                "subjectivity_conclusion": audit.subjectivity_conclusion,
                "consciousness_conclusion": audit.consciousness_conclusion,
                "phenomenal_experience_conclusion": audit.phenomenal_experience_conclusion,
                "moral_status_conclusion": audit.moral_status_conclusion,
                "scientific_disposition": audit.scientific_disposition,
                "canonical_effect": audit.canonical_effect,
                "deployment": audit.deployment,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
