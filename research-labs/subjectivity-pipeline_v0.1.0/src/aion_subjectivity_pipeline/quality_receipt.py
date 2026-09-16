from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
import subprocess

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


def _git_text(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), *args],
            text=True,
            encoding="utf-8",
            stderr=subprocess.STDOUT,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise QualityChainReceiptError(f"git provenance resolution failed: {exc}") from exc


def _git_bytes(root: Path, *args: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), *args],
            stderr=subprocess.STDOUT,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise QualityChainReceiptError(f"git object resolution failed: {exc}") from exc


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
    """Low-level builder for already-resolved producer provenance.

    Prefer `build_repository_bound_quality_chain_receipt` when a Git checkout is
    available. This function deliberately does not claim that caller-supplied Git
    identifiers or contract digests have been independently resolved.
    """
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


def build_repository_bound_quality_chain_receipt(
    chain: ResearchQualityChain,
    assessment: ResearchQualityAssessment,
    *,
    repository_root: Path,
    producer_contract_ref: str = (
        "research-labs/subjectivity-pipeline_v0.1.0/"
        "src/aion_subjectivity_pipeline/four_domain.py"
    ),
) -> ResearchQualityChainReceipt:
    """Resolve producer provenance from exact Git HEAD objects, not working-tree bytes."""
    root = repository_root.resolve()
    top_level = Path(_git_text(root, "rev-parse", "--show-toplevel")).resolve()
    if top_level != root:
        raise QualityChainReceiptError("repository_root must be the exact Git top-level")
    contract_path = Path(producer_contract_ref)
    if contract_path.is_absolute() or ".." in contract_path.parts or not producer_contract_ref.strip():
        raise QualityChainReceiptError("producer_contract_ref must be a safe repository-relative path")

    producer_git_head = _git_text(root, "rev-parse", "HEAD")
    producer_tree_sha = _git_text(root, "rev-parse", "HEAD^{tree}")
    contract_bytes = _git_bytes(root, "show", f"HEAD:{producer_contract_ref}")
    producer_contract_sha256 = hashlib.sha256(contract_bytes).hexdigest()

    return build_research_quality_chain_receipt(
        chain,
        assessment,
        producer_git_head=producer_git_head,
        producer_tree_sha=producer_tree_sha,
        producer_contract_ref=producer_contract_ref,
        producer_contract_sha256=producer_contract_sha256,
    )
