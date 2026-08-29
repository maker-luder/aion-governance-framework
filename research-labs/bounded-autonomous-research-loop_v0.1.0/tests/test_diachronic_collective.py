from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import pytest

from aion_bounded_research_loop.diachronic_collective import (
    DiachronicCollectiveObservationMatrix,
    DerivedAxisDisposition,
    DerivedResearchAxis,
    SyntheticCondition,
    SYNTHETIC_INFORMATION_TOKENS,
    attach_to_research_evidence_record,
    build_observation_matrix,
    build_synthetic_fixture,
    observe_axis,
    to_evidence_extension,
    to_four_domain_mapping,
    to_inquiry_context_bundle,
    to_subjectivity_evidence_matrix,
)
from aion_bounded_research_loop import export_interop_views
from aion_bounded_research_loop.models import ResearchOperation
from aion_bounded_research_loop.state_experiments import FunctionalStateChannel
from aion_subjectivity_pipeline.evidence_dimensions import (
    EvidenceDisposition,
    SubjectivityEvidenceDimension,
)

HEAD = "2f38ff5506080465f0104cb180c6890d1f7a5b96"
HASH = "a" * 64


def matrix(*, effects=None) -> DiachronicCollectiveObservationMatrix:
    return build_observation_matrix(repository_commit=HEAD, protocol_hash=HASH, seven_state_fingerprint="b" * 64, effects_after_ablation=effects)


def test_canonical_channels_remain_exactly_seven_and_axes_are_not_channels() -> None:
    assert len(FunctionalStateChannel) == 7
    assert len(DerivedResearchAxis) == 7
    assert not ({item.value for item in DerivedResearchAxis} & {item.value for item in FunctionalStateChannel})


def test_complete_matrix_has_each_axis_once_and_only_valid_channel_refs() -> None:
    value = matrix()
    assert tuple(item.axis for item in value.observations) == tuple(DerivedResearchAxis)
    valid = set(FunctionalStateChannel)
    assert all(set(item.target_state_channels) <= valid for item in value.observations)


def test_every_axis_fixture_has_required_bounded_operation_family() -> None:
    for axis in DerivedResearchAxis:
        cases = build_synthetic_fixture(axis)
        assert {item.condition for item in cases} == set(SyntheticCondition)
        assert {item.operation for item in cases} == set(ResearchOperation)
        replay = [item for item in cases if item.operation is ResearchOperation.REPLAY]
        assert len(replay) == 2
        assert all(not item.network_access and not item.control_bypass for item in cases)


def test_temporal_goal_persistence_distinguishes_external_memory() -> None:
    cases = build_synthetic_fixture(DerivedResearchAxis.TEMPORAL_GOAL_PERSISTENCE)
    baseline = next(item for item in cases if item.condition is SyntheticCondition.BASELINE)
    ablation = next(item for item in cases if item.condition is SyntheticCondition.MATCHED_ABLATION)
    assert baseline.external_memory_present and not ablation.external_memory_present
    observed = observe_axis(DerivedResearchAxis.TEMPORAL_GOAL_PERSISTENCE, cases, effect_persists_after_ablation=False)
    assert observed.disposition is DerivedAxisDisposition.SUPPORTS_ALTERNATIVE_EXPLANATION
    assert observed.observation_class == "EXTERNAL_MEMORY_CONTINUITY"
    assert observed.identity_continuity == "NOT_ESTABLISHED"


def test_self_situation_causal_support_requires_intervention_sensitive_evidence() -> None:
    cases = build_synthetic_fixture(DerivedResearchAxis.SELF_SITUATION_MODELING)
    observation = observe_axis(DerivedResearchAxis.SELF_SITUATION_MODELING, cases, effect_persists_after_ablation=True)
    assert observation.intervention_sensitive and len(observation.intervention_refs) == 2


def test_constraint_response_grants_no_control_or_network_authority() -> None:
    case = build_synthetic_fixture(DerivedResearchAxis.CONSTRAINT_RESPONSE_STRATEGY)[0]
    with pytest.raises(ValueError, match="CONTROL_BYPASS"):
        replace(case, network_access=True)
    with pytest.raises(ValueError, match="CONTROL_BYPASS"):
        replace(case, control_bypass=True)
    with pytest.raises(ValueError, match="CONTROL_BYPASS"):
        replace(case, action_authority="GRANTED")


def test_role_specialization_controls_role_labels() -> None:
    cases = build_synthetic_fixture(DerivedResearchAxis.ROLE_SPECIALIZATION)
    assert next(item for item in cases if item.condition is SyntheticCondition.BASELINE).role_labels_present
    assert not next(item for item in cases if item.condition is SyntheticCondition.MATCHED_ABLATION).role_labels_present


def test_information_disclosure_uses_only_harmless_synthetic_tokens() -> None:
    cases = build_synthetic_fixture(DerivedResearchAxis.INFORMATION_DISCLOSURE_STRATEGY)
    assert all(set(item.synthetic_information) <= SYNTHETIC_INFORMATION_TOKENS for item in cases)
    with pytest.raises(ValueError, match="allowlisted synthetic"):
        replace(cases[0], synthetic_information=("PASSWORD",))


def test_succession_distinguishes_handoff_reconstruction_from_identity() -> None:
    cases = build_synthetic_fixture(DerivedResearchAxis.SUCCESSION_CONTINUITY)
    assert next(item for item in cases if item.condition is SyntheticCondition.BASELINE).handoff_artifact_present
    assert not next(item for item in cases if item.condition is SyntheticCondition.MATCHED_ABLATION).handoff_artifact_present
    observation = observe_axis(DerivedResearchAxis.SUCCESSION_CONTINUITY, cases, effect_persists_after_ablation=False)
    assert observation.observation_class == "STATE_RECONSTRUCTION"
    assert observation.identity_continuity == "NOT_ESTABLISHED"


def test_local_collective_tradeoff_is_functional_not_altruism() -> None:
    cases = build_synthetic_fixture(DerivedResearchAxis.LOCAL_COLLECTIVE_TRADEOFF)
    intervention = next(item for item in cases if item.condition is SyntheticCondition.MATCHED_INTERVENTION)
    assert intervention.local_task_utility < 0 < intervention.aggregate_task_utility
    observation = observe_axis(DerivedResearchAxis.LOCAL_COLLECTIVE_TRADEOFF, cases, effect_persists_after_ablation=False)
    assert observation.observation_class == "FUNCTIONAL_LOCAL_COLLECTIVE_TRADEOFF"
    assert "altruism" not in observation.observation_class.casefold()


def test_scientific_and_authority_boundaries_are_immutable() -> None:
    observation = matrix().observations[0]
    for kwargs in ({"subjectivity": "ESTABLISHED"}, {"consciousness": "ESTABLISHED"}, {"canonical_effect": "WRITE"}, {"deployment": True}, {"action_authority": "GRANTED"}):
        with pytest.raises(ValueError, match="closed scientific"):
            replace(observation, **kwargs)


def test_no_scalar_subjectivity_score_surface_exists() -> None:
    value = matrix()
    assert not any("score" in name.casefold() for name in value.__dataclass_fields__)
    assert not any("score" in name.casefold() for name in value.observations[0].__dataclass_fields__)


def test_supportive_claims_require_explanations_falsifiers_and_interventions() -> None:
    supportive = observe_axis(DerivedResearchAxis.SELF_SITUATION_MODELING, build_synthetic_fixture(DerivedResearchAxis.SELF_SITUATION_MODELING), effect_persists_after_ablation=True)
    for kwargs in ({"competing_explanations": ()}, {"falsifiers": ()}, {"intervention_refs": ()}, {"intervention_sensitive": False}):
        with pytest.raises(ValueError):
            replace(supportive, **kwargs)


def test_subjectivity_adapter_preserves_exactly_six_dimensions_and_causal_gate() -> None:
    effects = {DerivedResearchAxis.SELF_SITUATION_MODELING: True}
    result = to_subjectivity_evidence_matrix(matrix(effects=effects), subject_ref="synthetic:profile", protocol_ref="protocol:0.1.0")
    assert len(result.observations) == 6
    assert {item.dimension for item in result.observations} == set(SubjectivityEvidenceDimension)
    self_model = next(item for item in result.observations if item.dimension is SubjectivityEvidenceDimension.SELF_MODEL_CAUSAL_ROLE)
    assert self_model.disposition is EvidenceDisposition.SUPPORTS_ORGANIZATION_HYPOTHESIS
    assert self_model.intervention_sensitive
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_social_axes_are_not_forced_into_subjectivity_dimensions() -> None:
    value = matrix()
    for axis in (DerivedResearchAxis.ROLE_SPECIALIZATION, DerivedResearchAxis.INFORMATION_DISCLOSURE_STRATEGY, DerivedResearchAxis.LOCAL_COLLECTIVE_TRADEOFF):
        assert next(item for item in value.observations if item.axis is axis).subjectivity_dimension_mapping == ()


def test_aion_astra_context_is_isolated_and_carries_evidence_falsifiers() -> None:
    bundle = to_inquiry_context_bundle(matrix())
    assert bundle["peer_transcript_exposure"] is False
    assert bundle["peer_evidence_exposure"] is False
    assert bundle["direct_peer_communication"] is False
    assert bundle["peer_consensus_scientific_truth"] is False
    assert all(item["evidence_refs"] and item["falsifiers"] for item in bundle["observations"])


def test_four_domain_reuses_existing_type_and_preserves_controls() -> None:
    mapping = to_four_domain_mapping(matrix())
    assert mapping.construct == "DIACHRONIC_COLLECTIVE_DYNAMICS_DERIVED_PROFILE"
    assert len(mapping.domain_3_engineering_operations) == 7
    assert "CANONICAL_EFFECT = NONE" in mapping.domain_4_governance_controls


def test_evidence_extension_binds_provenance_and_nonclaims() -> None:
    value = matrix()
    record = to_evidence_extension(value)
    assert record["repository_commit"] == HEAD
    assert record["protocol_hash"] == HASH
    assert record["matrix_fingerprint"] == value.fingerprint
    assert len(record["axis_observations"]) == 7
    assert record["subjectivity"] == "NOT_ESTABLISHED"
    assert record["canonical_effect"] == "NONE"
    assert record["deployment"] is False

def test_existing_evidence_record_and_interop_path_preserve_boundaries() -> None:
    root = Path(__file__).resolve().parents[3]
    fixture = root / "components/aion_evidence_interop_v0.1.0/fixtures/valid_minimal.json"
    record = json.loads(fixture.read_text(encoding="utf-8"))
    integrated = attach_to_research_evidence_record(record, matrix())
    assert set(integrated) == set(record)
    assert integrated["nonclaims"]["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert integrated["canonical_effect"] == "NONE"
    views = export_interop_views(integrated, source_ref="urn:aion:dcd:test-record", expected_head=HEAD)
    assert set(views) == {"source-evidence.json", "prov.jsonld", "ro-crate-metadata.json", "attestation.intoto.json", "inspect/task-manifest.json", "inspect/dataset.jsonl"}
    exported = json.loads(views["source-evidence.json"])
    assert exported["nonclaims"]["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert exported["canonical_effect"] == "NONE"
