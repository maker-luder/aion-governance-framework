from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from .four_domain import ResearchQualityAssessment, ResearchQualityChain


RECEIPT_SCHEMA_VERSION = "0.1.0"


class QualityChainReceiptError(ValueError):
    pass


def _sha256_payload(payload: object) -> str:
    rendered = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(rendered).hexdigest()


def _require_hex(name: str, value: str, length: int) -> None:
    if type(value) is not str or len(value) != length or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise QualityChainReceiptError(f"{name} must be lowercase {length}-hex")


@dataclass(frozen=True, slots=True)
class ResearchQualityChainReceipt:
    chain_id: str
    candidate_id: str
    candidate_fingerprint: str
    disposition: str
    exact_source_state_ref: str
    exact_runtime_ref: str
    producer_git_head: str
    producer_tree_sha: str
    checkpoint_set_sha256: str
    capa_set_sha256: str
    assessment_sha256: str
    producer_contract_ref: str
    producer_contract_sha256: str
    receipt_sha256: str
    schema_version: str = RECEIPT_SCHEMA_VERSION
    release_authority: str = "NONE"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        for name in (
            "chain_id",
            "candidate_id",
            "candidate_fingerprint",
            "disposition",
            "exact_source_state_ref",
            "exact_runtime_ref",
            "producer_contract_ref",
        ):
            value = getattr(self, name)
            if type(value) is not str or not value.strip():
                raise QualityChainReceiptError(f"{name} must be non-empty text")
        if self.schema_version != RECEIPT_SCHEMA_VERSION:
            raise QualityChainReceiptError("unsupported receipt schema version")
        _require_hex("candidate_fingerprint", self.candidate_fingerprint, 64)
        _require_hex("producer_git_head", self.producer_git_head, 40)
        _require_hex("producer_tree_sha", self.producer_tree_sha, 40)
        for name in (
            "checkpoint_set_sha256",
            "capa_set_sha256",
            "assessment_sha256",
            "producer_contract_sha256",
            "receipt_sha256",
        ):
            _require_hex(name, getattr(self, name), 64)
        if self.release_authority != "NONE":
            raise QualityChainReceiptError("receipt cannot grant release authority")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise QualityChainReceiptError("receipt cannot establish subjectivity")
        if self.phenomenal_experience_conclusion != "NOT_ESTABLISHED":
            raise QualityChainReceiptError("receipt cannot establish phenomenal experience")
        if self.scientific_disposition != "HOLD":
            raise QualityChainReceiptError("receipt cannot establish scientific validity")
        if self.canonical_effect != "NONE" or self.deployment:
            raise QualityChainReceiptError("receipt cannot create canonical or deployment effect")
        if self.receipt_sha256 != _sha256_payload(self.payload_without_digest()):
            raise QualityChainReceiptError("receipt content digest mismatch")

    def payload_without_digest(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "chain_id": self.chain_id,
            "candidate_id": self.candidate_id,
            "candidate_fingerprint": self.candidate_fingerprint,
            "disposition": self.disposition,
            "exact_source_state_ref": self.exact_source_state_ref,
            "exact_runtime_ref": self.exact_runtime_ref,
            "producer_git_head": self.producer_git_head,
            "producer_tree_sha": self.producer_tree_sha,
            "checkpoint_set_sha256": self.checkpoint_set_sha256,
            "capa_set_sha256": self.capa_set_sha256,
            "assessment_sha256": self.assessment_sha256,
            "producer_contract_ref": self.producer_contract_ref,
            "producer_contract_sha256": self.producer_contract_sha256,
            "release_authority": self.release_authority,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "phenomenal_experience_conclusion": self.phenomenal_experience_conclusion,
            "scientific_disposition": self.scientific_disposition,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
        }

    def as_dict(self) -> dict[str, object]:
        return {**self.payload_without_digest(), "receipt_sha256": self.receipt_sha256}


def build_research_quality_chain_receipt(
    chain: ResearchQualityChain,
    assessment: ResearchQualityAssessment,
    *,
    producer_git_head: str,
    producer_tree_sha: str,
    producer_contract_ref: str,
    producer_contract_sha256: str,
) -> ResearchQualityChainReceipt:
    if assessment.chain_id != chain.chain_id:
        raise QualityChainReceiptError("assessment and chain identifiers must match")
    _require_hex("producer_git_head", producer_git_head, 40)
    _require_hex("producer_tree_sha", producer_tree_sha, 40)
    _require_hex("producer_contract_sha256", producer_contract_sha256, 64)
    if not producer_contract_ref.strip():
        raise QualityChainReceiptError("producer_contract_ref must be non-empty")

    checkpoint_payload = [
        {
            "checkpoint": record.checkpoint.value,
            "input_refs": list(record.input_refs),
            "output_refs": list(record.output_refs),
            "passed": record.passed,
            "defect_refs": list(record.defect_refs),
        }
        for record in sorted(chain.checkpoints, key=lambda item: item.checkpoint.value)
    ]
    capa_payload = [
        {
            "ncr_id": record.ncr_id,
            "state": record.state.value,
            "root_cause": record.root_cause,
            "corrective_action": record.corrective_action,
            "preventive_action": record.preventive_action,
            "effectiveness_test": record.effectiveness_test,
            "verification_refs": list(record.verification_refs),
        }
        for record in sorted(chain.capa_records, key=lambda item: item.ncr_id)
    ]
    assessment_payload = {
        "chain_id": assessment.chain_id,
        "disposition": assessment.disposition.value,
        "reasons": list(assessment.reasons),
        "release_authority": assessment.release_authority,
        "subjectivity_conclusion": assessment.subjectivity_conclusion,
        "phenomenal_experience_conclusion": assessment.phenomenal_experience_conclusion,
        "scientific_disposition": assessment.scientific_disposition,
        "canonical_effect": assessment.canonical_effect,
        "deployment": assessment.deployment,
    }
    values: dict[str, object] = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "chain_id": chain.chain_id,
        "candidate_id": chain.candidate_id,
        "candidate_fingerprint": chain.candidate_fingerprint,
        "disposition": assessment.disposition.value,
        "exact_source_state_ref": chain.exact_source_state_ref,
        "exact_runtime_ref": chain.exact_runtime_ref,
        "producer_git_head": producer_git_head,
        "producer_tree_sha": producer_tree_sha,
        "checkpoint_set_sha256": _sha256_payload(checkpoint_payload),
        "capa_set_sha256": _sha256_payload(capa_payload),
        "assessment_sha256": _sha256_payload(assessment_payload),
        "producer_contract_ref": producer_contract_ref,
        "producer_contract_sha256": producer_contract_sha256,
        "release_authority": assessment.release_authority,
        "subjectivity_conclusion": assessment.subjectivity_conclusion,
        "phenomenal_experience_conclusion": assessment.phenomenal_experience_conclusion,
        "scientific_disposition": assessment.scientific_disposition,
        "canonical_effect": assessment.canonical_effect,
        "deployment": assessment.deployment,
    }
    values["receipt_sha256"] = _sha256_payload(values)
    return ResearchQualityChainReceipt(**values)
