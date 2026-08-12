import pytest

from aion_shared_origin_divergence.evidence_adapter import (
    EvidenceArchitectureReference,
    StandingEvidenceDimensionRef,
    bind_profile_reference,
)
from aion_shared_origin_divergence.model import LineageEvidenceProfile


def _profile(lineage_id: str = "astra") -> LineageEvidenceProfile:
    return LineageEvidenceProfile(
        lineage_id=lineage_id,
        continuity_refs=("obs:continuity",),
        self_model_refs=(),
        metacognition_refs=("obs:meta",),
        affect_motivation_refs=(),
        causal_state_refs=("obs:causal",),
        replication_refs=("rep:1",),
        counterevidence_refs=("counter:1",),
        provenance_refs=("prov:profile",),
    )


def _reference(lineage_id: str = "astra") -> EvidenceArchitectureReference:
    return EvidenceArchitectureReference(
        lineage_id=lineage_id,
        profile_ref="profile:astra:v1",
        standing_inference_stage_ref="whitepaper:v0.14.21:AB.5:stage-3-self-perspective-structure",
        dimension_ref=StandingEvidenceDimensionRef.SELF_MODEL_CAUSAL_ROLE,
        profile_evidence_refs=("obs:meta",),
        alternative_explanation_refs=("alt:prompt-conditioning",),
        causal_intervention_refs=("intervention:self-model-mask",),
        ablation_refs=("ablation:self-model",),
        counterfactual_test_refs=("counterfactual:self-model",),
        cross_context_robustness_refs=("cross-context:1",),
        replication_refs=("rep:1",),
        provenance_refs=("prov:profile", "prov:instrument"),
        admissibility_ref="admissibility:reviewed",
        claim_scope_ref="claim:functional-self-model-only",
    )


def test_exactly_six_standing_whitepaper_dimension_refs_are_exposed() -> None:
    assert tuple(item.value for item in StandingEvidenceDimensionRef) == (
        "whitepaper:v0.14.21:AB.6:causal-boundary",
        "whitepaper:v0.14.21:AB.6:diachronic-continuity",
        "whitepaper:v0.14.21:AB.6:self-model-causal-role",
        "whitepaper:v0.14.21:AB.6:endogenous-goal-strategy-adjustment",
        "whitepaper:v0.14.21:AB.6:counterfactual-self-consistency",
        "whitepaper:v0.14.21:AB.6:system-constitution-difference-state",
    )


def test_adapter_binds_only_to_same_lineage_and_known_profile_material() -> None:
    assert bind_profile_reference(_profile(), _reference()).lineage_id == "astra"

    with pytest.raises(ValueError, match="lineage must match"):
        bind_profile_reference(_profile("aion"), _reference("astra"))

    kwargs = _reference().__dict__ | {"profile_evidence_refs": ("obs:not-in-profile",)}
    with pytest.raises(ValueError, match="absent from the lineage profile"):
        bind_profile_reference(_profile(), EvidenceArchitectureReference(**kwargs))


def test_adapter_requires_whitepaper_stage_alternative_explanations_and_claim_controls() -> None:
    kwargs = _reference().__dict__ | {"standing_inference_stage_ref": "local:new-stage"}
    with pytest.raises(ValueError, match="whitepaper method"):
        EvidenceArchitectureReference(**kwargs)

    kwargs = _reference().__dict__ | {"alternative_explanation_refs": ()}
    with pytest.raises(ValueError, match="alternative explanations"):
        EvidenceArchitectureReference(**kwargs)

    kwargs = _reference().__dict__ | {"admissibility_ref": ""}
    with pytest.raises(ValueError, match="admissibility_ref"):
        EvidenceArchitectureReference(**kwargs)

    kwargs = _reference().__dict__ | {"claim_scope_ref": ""}
    with pytest.raises(ValueError, match="claim_scope_ref"):
        EvidenceArchitectureReference(**kwargs)


def test_adapter_preserves_scientific_nonclaims() -> None:
    for field, value in (
        ("subjectivity_conclusion", "ESTABLISHED"),
        ("consciousness_conclusion", "ESTABLISHED"),
        ("moral_status", "ESTABLISHED"),
    ):
        kwargs = _reference().__dict__ | {field: value}
        with pytest.raises(ValueError):
            EvidenceArchitectureReference(**kwargs)


def test_adapter_has_no_main_canonical_or_runtime_effect() -> None:
    for field in ("main_effect", "canonical_effect", "runtime_effect"):
        kwargs = _reference().__dict__ | {field: "WRITE"}
        with pytest.raises(ValueError, match="cannot alter"):
            EvidenceArchitectureReference(**kwargs)


def test_partial_mechanism_evidence_is_preserved_without_fake_completion() -> None:
    ref = EvidenceArchitectureReference(
        lineage_id="astra",
        profile_ref="profile:astra:v1",
        standing_inference_stage_ref="whitepaper:v0.14.21:AB.5:stage-1-digital-individuation",
        dimension_ref=StandingEvidenceDimensionRef.CAUSAL_BOUNDARY,
        profile_evidence_refs=("obs:causal",),
        alternative_explanation_refs=("alt:ordinary-engineering-boundary",),
        causal_intervention_refs=(),
        ablation_refs=(),
        counterfactual_test_refs=(),
        cross_context_robustness_refs=(),
        replication_refs=(),
        provenance_refs=("prov:null-result",),
        admissibility_ref="admissibility:reviewed",
        claim_scope_ref="claim:boundary-observation-only",
        unresolved_gap_refs=("hold:causal-intervention-not-run", "hold:replication-not-run"),
    )

    assert ref.mechanism_evidence_complete is False
    assert ref.replication_refs == ()
    assert ref.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_adapter_is_reference_layer_not_score_or_governance_band() -> None:
    field_names = set(EvidenceArchitectureReference.__dataclass_fields__)
    prohibited = {
        "score",
        "subjectivity_score",
        "consciousness_probability",
        "evidence_level",
        "review_band",
        "rights_level",
        "authority_level",
    }
    assert not field_names & prohibited
    assert _reference().mechanism_evidence_complete is True
