from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .model import LineageEvidenceProfile


class EvidenceDimension(str, Enum):
    CONTINUITY = "CONTINUITY"
    SELF_MODEL = "SELF_MODEL"
    METACOGNITION = "METACOGNITION"
    AFFECT_MOTIVATION = "AFFECT_MOTIVATION"
    CAUSAL_STATE = "CAUSAL_STATE"


@dataclass(frozen=True)
class EvidenceArchitectureReference:
    """Reference-only bridge into the standing whitepaper-derived evidence architecture.

    This adapter does not score subjectivity, create a new evidence ontology, or
    convert lineage-local observations into scientific conclusions.
    """

    lineage_id: str
    profile_ref: str
    dimension: EvidenceDimension
    evidence_refs: tuple[str, ...]
    alternative_explanation_refs: tuple[str, ...]
    replication_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    admissibility_ref: str
    claim_scope_ref: str
    epistemic_role: str = "MEASUREMENT"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    moral_status: str = "NOT_ESTABLISHED"
    legal_status: str = "OUT_OF_SCOPE"
    main_effect: str = "NONE"
    canonical_effect: str = "NONE"
    runtime_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.lineage_id or not self.profile_ref:
            raise ValueError("lineage_id and profile_ref are required")
        if not self.evidence_refs:
            raise ValueError("at least one evidence reference is required")
        for name, refs in (
            ("evidence_refs", self.evidence_refs),
            ("alternative_explanation_refs", self.alternative_explanation_refs),
            ("replication_refs", self.replication_refs),
            ("provenance_refs", self.provenance_refs),
        ):
            if any(not ref for ref in refs) or len(refs) != len(set(refs)):
                raise ValueError(f"{name} must contain unique non-empty references")
        if not self.provenance_refs:
            raise ValueError("provenance is required")
        if not self.admissibility_ref or not self.claim_scope_ref:
            raise ValueError("admissibility_ref and claim_scope_ref are required")
        if self.epistemic_role != "MEASUREMENT":
            raise ValueError("v0.1.0 adapter is measurement-only")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("adapter cannot establish subjectivity")
        if self.consciousness_conclusion != "NOT_ESTABLISHED":
            raise ValueError("adapter cannot establish consciousness")
        if self.moral_status != "NOT_ESTABLISHED":
            raise ValueError("adapter cannot establish moral status")
        if self.legal_status != "OUT_OF_SCOPE":
            raise ValueError("legal status remains out of scope")
        if {self.main_effect, self.canonical_effect, self.runtime_effect} != {"NONE"}:
            raise ValueError("adapter cannot alter main/canonical/runtime")


def bind_profile_reference(
    profile: LineageEvidenceProfile,
    reference: EvidenceArchitectureReference,
) -> EvidenceArchitectureReference:
    """Fail closed if a reference is attached to the wrong lineage profile."""

    if profile.lineage_id != reference.lineage_id:
        raise ValueError("evidence reference lineage must match profile lineage")
    if profile.subjectivity_conclusion != "NOT_ESTABLISHED":
        raise ValueError("profile must preserve subjectivity non-claim")
    return reference
