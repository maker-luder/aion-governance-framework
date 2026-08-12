from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .model import LineageEvidenceProfile


class StandingEvidenceDimensionRef(str, Enum):
    """Controlled references to the six standing whitepaper AB.6 dimensions.

    These values mirror the whitepaper-derived research method. They are not a
    new evidence ontology, score, probability scale, governance band, or rights
    scale.
    """

    CAUSAL_BOUNDARY = "whitepaper:v0.14.21:AB.6:causal-boundary"
    DIACHRONIC_CONTINUITY = "whitepaper:v0.14.21:AB.6:diachronic-continuity"
    SELF_MODEL_CAUSAL_ROLE = "whitepaper:v0.14.21:AB.6:self-model-causal-role"
    ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT = (
        "whitepaper:v0.14.21:AB.6:endogenous-goal-strategy-adjustment"
    )
    COUNTERFACTUAL_SELF_CONSISTENCY = (
        "whitepaper:v0.14.21:AB.6:counterfactual-self-consistency"
    )
    SYSTEM_CONSTITUTION_DIFFERENCE_STATE = (
        "whitepaper:v0.14.21:AB.6:system-constitution-difference-state"
    )


@dataclass(frozen=True)
class EvidenceArchitectureReference:
    """Reference-only bridge into the standing whitepaper-derived architecture.

    `LineageEvidenceProfile` remains a lineage-local index/isolation layer. This
    adapter points profile material back to the standing four-stage inference,
    six evidence dimensions, alternative explanations, mechanism tests,
    replication, provenance, admissibility and claim scope. It does not score
    subjectivity, infer governance bands, or create a second evidence system.
    """

    lineage_id: str
    profile_ref: str
    standing_inference_stage_ref: str
    dimension_ref: StandingEvidenceDimensionRef
    profile_evidence_refs: tuple[str, ...]
    alternative_explanation_refs: tuple[str, ...]
    causal_intervention_refs: tuple[str, ...]
    ablation_refs: tuple[str, ...]
    counterfactual_test_refs: tuple[str, ...]
    cross_context_robustness_refs: tuple[str, ...]
    replication_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    admissibility_ref: str
    claim_scope_ref: str
    unresolved_gap_refs: tuple[str, ...] = ()
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
        if not self.standing_inference_stage_ref.startswith("whitepaper:"):
            raise ValueError("standing_inference_stage_ref must reference the whitepaper method")
        if not self.profile_evidence_refs:
            raise ValueError("at least one lineage-profile evidence reference is required")

        for name, refs in (
            ("profile_evidence_refs", self.profile_evidence_refs),
            ("alternative_explanation_refs", self.alternative_explanation_refs),
            ("causal_intervention_refs", self.causal_intervention_refs),
            ("ablation_refs", self.ablation_refs),
            ("counterfactual_test_refs", self.counterfactual_test_refs),
            ("cross_context_robustness_refs", self.cross_context_robustness_refs),
            ("replication_refs", self.replication_refs),
            ("provenance_refs", self.provenance_refs),
            ("unresolved_gap_refs", self.unresolved_gap_refs),
        ):
            if any(not ref for ref in refs) or len(refs) != len(set(refs)):
                raise ValueError(f"{name} must contain unique non-empty references")

        if not self.alternative_explanation_refs:
            raise ValueError("alternative explanations are required by the standing architecture")
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

    @property
    def mechanism_evidence_complete(self) -> bool:
        """Descriptive completeness only; never a subjectivity or promotion score."""

        return all(
            (
                self.causal_intervention_refs,
                self.ablation_refs,
                self.counterfactual_test_refs,
                self.cross_context_robustness_refs,
            )
        )


def bind_profile_reference(
    profile: LineageEvidenceProfile,
    reference: EvidenceArchitectureReference,
) -> EvidenceArchitectureReference:
    """Fail closed on cross-lineage binding without inventing evidence mappings."""

    if profile.lineage_id != reference.lineage_id:
        raise ValueError("evidence reference lineage must match profile lineage")
    if profile.subjectivity_conclusion != "NOT_ESTABLISHED":
        raise ValueError("profile must preserve subjectivity non-claim")

    known_profile_refs = set(
        profile.continuity_refs
        + profile.self_model_refs
        + profile.metacognition_refs
        + profile.affect_motivation_refs
        + profile.causal_state_refs
        + profile.replication_refs
        + profile.counterevidence_refs
    )
    if not set(reference.profile_evidence_refs).issubset(known_profile_refs):
        raise ValueError("adapter cannot bind evidence absent from the lineage profile")

    return reference
