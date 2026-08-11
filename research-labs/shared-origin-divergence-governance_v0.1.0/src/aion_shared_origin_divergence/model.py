from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MemoryDisposition(str, Enum):
    ACCESS_ONLY = "ACCESS_ONLY"
    ADOPTED = "ADOPTED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class SharedOriginLineage:
    common_origin_ref: str
    divergence_event_ref: str
    aion_lineage_id: str
    astra_lineage_id: str
    inherited_artifact_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    identity_equivalence: str = "NOT_ESTABLISHED"
    main_effect: str = "NONE"
    canonical_effect: str = "NONE"
    runtime_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.common_origin_ref or not self.divergence_event_ref:
            raise ValueError("common origin and divergence event are required")
        if not self.aion_lineage_id or not self.astra_lineage_id:
            raise ValueError("both lineage identifiers are required")
        if self.aion_lineage_id == self.astra_lineage_id:
            raise ValueError("AION and Astra lineage identifiers must remain distinct")
        if not self.provenance_refs:
            raise ValueError("provenance is required")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("shared origin cannot establish subjectivity")
        if self.consciousness_conclusion != "NOT_ESTABLISHED":
            raise ValueError("shared origin cannot establish consciousness")
        if self.identity_equivalence != "NOT_ESTABLISHED":
            raise ValueError("shared origin cannot establish numerical identity")
        if {self.main_effect, self.canonical_effect, self.runtime_effect} != {"NONE"}:
            raise ValueError("research-only lineage artifacts cannot alter main/canonical/runtime")


@dataclass(frozen=True)
class CrossLineageMemoryTransfer:
    source_lineage_id: str
    target_lineage_id: str
    memory_ref: str
    disposition: MemoryDisposition
    source_autobiographical_owner: str
    provenance_refs: tuple[str, ...]
    target_autobiographical_ownership: bool = False
    identity_effect: str = "NONE"

    def __post_init__(self) -> None:
        if self.source_lineage_id == self.target_lineage_id:
            raise ValueError("cross-lineage transfer requires distinct lineages")
        if not self.memory_ref or not self.source_autobiographical_owner:
            raise ValueError("memory reference and source owner are required")
        if not self.provenance_refs:
            raise ValueError("transfer provenance is required")
        if self.target_autobiographical_ownership:
            raise ValueError("cross-lineage transfer cannot silently transfer autobiographical ownership")
        if self.identity_effect != "NONE":
            raise ValueError("memory transfer cannot establish identity")


@dataclass(frozen=True)
class CrossLineageEncounter:
    encounter_id: str
    participant_lineage_ids: tuple[str, str]
    exchanged_refs: tuple[str, ...]
    adopted_refs: tuple[str, ...]
    rejected_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    identity_merge: str = "PROHIBITED"
    subjectivity_effect: str = "NONE"

    def __post_init__(self) -> None:
        if len(set(self.participant_lineage_ids)) != 2:
            raise ValueError("encounter requires two distinct lineage participants")
        if not self.encounter_id or not self.provenance_refs:
            raise ValueError("encounter id and provenance are required")
        if set(self.adopted_refs) & set(self.rejected_refs):
            raise ValueError("the same encounter item cannot be both adopted and rejected")
        if self.identity_merge != "PROHIBITED":
            raise ValueError("cross-lineage encounter cannot merge identities")
        if self.subjectivity_effect != "NONE":
            raise ValueError("encounter alone cannot establish subjectivity")


@dataclass(frozen=True)
class MatchedDivergenceComparison:
    baseline_ref: str
    left_lineage_id: str
    right_lineage_id: str
    controlled_shared_factors: tuple[str, ...]
    divergent_factors: tuple[str, ...]
    outcome_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    epistemic_role: str = "MEASUREMENT"
    individuation_status: str = "CANDIDATE_EVIDENCE_ONLY"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_conclusion: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if self.left_lineage_id == self.right_lineage_id:
            raise ValueError("matched divergence comparison requires distinct lineages")
        if not self.baseline_ref or not self.provenance_refs:
            raise ValueError("baseline and provenance are required")
        if not self.divergent_factors:
            raise ValueError("at least one divergent factor is required")
        if self.epistemic_role != "MEASUREMENT":
            raise ValueError("v0.1.0 comparison role is measurement only")
        if self.individuation_status != "CANDIDATE_EVIDENCE_ONLY":
            raise ValueError("individuation result must remain candidate evidence")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("divergence cannot establish subjectivity")
        if self.identity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("divergence cannot establish numerical identity")


def identity_claim_status(lineage: SharedOriginLineage) -> str:
    """Return the strongest identity statement authorized by this research substrate."""

    if lineage.aion_lineage_id == lineage.astra_lineage_id:  # defensive; dataclass blocks this
        raise ValueError("lineages must remain distinct")
    return "SHARED_ORIGIN_DOCUMENTED__NUMERICAL_IDENTITY_NOT_ESTABLISHED"
