"""Evidence cache reuse and explicit invalidation."""

from __future__ import annotations

from dataclasses import replace

from .enums import EvidenceValidity
from .models import EvidenceReference


def classify_evidence(
    evidence: EvidenceReference,
    *,
    current_source_hash: str,
    current_environment_fingerprint: str,
    changed_dependencies: tuple[str, ...] = (),
) -> EvidenceReference:
    if evidence.validity_status is EvidenceValidity.NON_REUSABLE_EVIDENCE:
        return evidence
    if evidence.source_commit_or_hash != current_source_hash:
        return replace(evidence, validity_status=EvidenceValidity.INVALIDATED_EVIDENCE)
    if evidence.environment_fingerprint != current_environment_fingerprint:
        return replace(evidence, validity_status=EvidenceValidity.STALE_EVIDENCE)
    if set(evidence.dependency_scope) & set(changed_dependencies):
        return replace(evidence, validity_status=EvidenceValidity.INVALIDATED_EVIDENCE)
    return replace(evidence, validity_status=EvidenceValidity.REUSABLE_EVIDENCE)
