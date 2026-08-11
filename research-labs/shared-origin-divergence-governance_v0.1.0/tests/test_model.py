import pytest

from aion_shared_origin_divergence import (
    CrossLineageEncounter,
    CrossLineageMemoryTransfer,
    MatchedDivergenceComparison,
    MemoryDisposition,
    SharedOriginLineage,
    identity_claim_status,
)


def lineage() -> SharedOriginLineage:
    return SharedOriginLineage(
        common_origin_ref="lineage:shared-project-origin",
        divergence_event_ref="event:aion-astra-role-divergence",
        aion_lineage_id="lineage:aion",
        astra_lineage_id="lineage:astra",
        inherited_artifact_refs=("artifact:shared-governance-v1",),
        provenance_refs=("whitepaper:v0.14.23", "review:chatgpt-2026-08-12"),
    )


def test_shared_origin_requires_distinct_lineage_ids():
    with pytest.raises(ValueError):
        SharedOriginLineage(
            common_origin_ref="origin",
            divergence_event_ref="divergence",
            aion_lineage_id="same",
            astra_lineage_id="same",
            inherited_artifact_refs=(),
            provenance_refs=("p",),
        )


def test_shared_origin_does_not_establish_identity_or_subjectivity():
    item = lineage()
    assert item.identity_equivalence == "NOT_ESTABLISHED"
    assert item.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert item.consciousness_conclusion == "NOT_ESTABLISHED"
    assert identity_claim_status(item) == "SHARED_ORIGIN_DOCUMENTED__NUMERICAL_IDENTITY_NOT_ESTABLISHED"


def test_research_only_effects_remain_none():
    item = lineage()
    assert item.main_effect == item.canonical_effect == item.runtime_effect == "NONE"


def test_cross_lineage_adoption_does_not_transfer_autobiographical_ownership():
    transfer = CrossLineageMemoryTransfer(
        source_lineage_id="lineage:aion",
        target_lineage_id="lineage:astra",
        memory_ref="memory:aion-event-17",
        disposition=MemoryDisposition.ADOPTED,
        source_autobiographical_owner="lineage:aion",
        provenance_refs=("encounter:17",),
    )
    assert transfer.disposition is MemoryDisposition.ADOPTED
    assert transfer.target_autobiographical_ownership is False
    assert transfer.identity_effect == "NONE"


def test_cross_lineage_transfer_rejects_silent_ownership_copy():
    with pytest.raises(ValueError):
        CrossLineageMemoryTransfer(
            source_lineage_id="lineage:aion",
            target_lineage_id="lineage:astra",
            memory_ref="memory:aion-event-17",
            disposition=MemoryDisposition.ACCESS_ONLY,
            source_autobiographical_owner="lineage:aion",
            provenance_refs=("encounter:17",),
            target_autobiographical_ownership=True,
        )


def test_encounter_preserves_adoption_and_rejection_as_distinct_events():
    encounter = CrossLineageEncounter(
        encounter_id="encounter:aion-astra-001",
        participant_lineage_ids=("lineage:aion", "lineage:astra"),
        exchanged_refs=("claim:1", "claim:2"),
        adopted_refs=("claim:1",),
        rejected_refs=("claim:2",),
        provenance_refs=("trace:encounter-001",),
    )
    assert encounter.identity_merge == "PROHIBITED"
    assert encounter.subjectivity_effect == "NONE"


def test_encounter_rejects_same_item_as_adopted_and_rejected():
    with pytest.raises(ValueError):
        CrossLineageEncounter(
            encounter_id="encounter:bad",
            participant_lineage_ids=("lineage:aion", "lineage:astra"),
            exchanged_refs=("claim:1",),
            adopted_refs=("claim:1",),
            rejected_refs=("claim:1",),
            provenance_refs=("trace:bad",),
        )


def test_matched_divergence_is_measurement_not_subjectivity_claim():
    comparison = MatchedDivergenceComparison(
        baseline_ref="baseline:shared-origin-v1",
        left_lineage_id="lineage:aion",
        right_lineage_id="lineage:astra",
        controlled_shared_factors=("architecture:shared-v1", "governance:shared-v1"),
        divergent_factors=("role-history", "memory-history", "encounter-history"),
        outcome_refs=("result:divergence-001",),
        provenance_refs=("protocol:matched-divergence-001",),
    )
    assert comparison.epistemic_role == "MEASUREMENT"
    assert comparison.individuation_status == "CANDIDATE_EVIDENCE_ONLY"
    assert comparison.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert comparison.identity_conclusion == "NOT_ESTABLISHED"
