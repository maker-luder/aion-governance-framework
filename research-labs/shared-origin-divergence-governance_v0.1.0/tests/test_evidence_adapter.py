import pytest

from aion_shared_origin_divergence.evidence_adapter import (
    EvidenceArchitectureReference,
    EvidenceDimension,
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
        dimension=EvidenceDimension.METACOGNITION,
        evidence_refs=("obs:meta",),
        alternative_explanation_refs=("alt:prompt-conditioning",),
        replication_refs=("rep:1",),
        provenance_refs=("prov:profile", "prov:instrument"),
        admissibility_ref="admissibility:reviewed",
        claim_scope_ref="claim:functional-metacognition-only",
    )


def test_adapter_binds_only_to_same_lineage() -> None:
    assert bind_profile_reference(_profile(), _reference()).lineage_id == "astra"
    with pytest.raises(ValueError, match="lineage must match"):
        bind_profile_reference(_profile("aion"), _reference("astra"))


def test_adapter_requires_admissibility_and_claim_scope() -> None:
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


def test_adapter_has_no_runtime_or_canonical_effect() -> None:
    for field in ("main_effect", "canonical_effect", "runtime_effect"):
        kwargs = _reference().__dict__ | {field: "WRITE"}
        with pytest.raises(ValueError, match="cannot alter"):
            EvidenceArchitectureReference(**kwargs)


def test_adapter_does_not_require_positive_replication() -> None:
    ref = EvidenceArchitectureReference(
        lineage_id="astra",
        profile_ref="profile:astra:v1",
        dimension=EvidenceDimension.CAUSAL_STATE,
        evidence_refs=("obs:null-effect",),
        alternative_explanation_refs=("alt:measurement-noise",),
        replication_refs=(),
        provenance_refs=("prov:null-result",),
        admissibility_ref="admissibility:reviewed",
        claim_scope_ref="claim:null-result-only",
    )
    assert ref.replication_refs == ()
    assert ref.subjectivity_conclusion == "NOT_ESTABLISHED"
