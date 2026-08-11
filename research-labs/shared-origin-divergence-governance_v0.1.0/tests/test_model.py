import json

import pytest

from aion_shared_origin_divergence import (
    AuthorityEnvelope,
    CrossLineageEncounter,
    CrossLineageMemoryTransfer,
    LineageEvidenceProfile,
    LineageEvent,
    LineageEventKind,
    LineageLedger,
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


def origin_event() -> LineageEvent:
    return LineageEvent(
        event_id="event:shared-origin",
        lineage_id="lineage:shared",
        kind=LineageEventKind.ORIGIN,
        occurred_at="2026-08-12T08:00:00+08:00",
        payload_ref="artifact:shared-baseline",
        parent_event_ids=(),
        provenance_refs=("whitepaper:v0.14.23",),
    )


def divergence_event(lineage_id: str, event_id: str, minute: int) -> LineageEvent:
    return LineageEvent(
        event_id=event_id,
        lineage_id=lineage_id,
        kind=LineageEventKind.DIVERGENCE,
        occurred_at=f"2026-08-12T08:{minute:02d}:00+08:00",
        payload_ref=f"history:{lineage_id}",
        parent_event_ids=("event:shared-origin",),
        provenance_refs=("trace:divergence",),
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


def test_shared_origin_serialization_is_deterministic():
    first = lineage().to_json()
    second = lineage().to_json()
    assert first == second
    assert json.loads(first)["aion_lineage_id"] == "lineage:aion"


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


def test_transfer_rejects_target_as_source_autobiographical_owner():
    with pytest.raises(ValueError):
        CrossLineageMemoryTransfer(
            source_lineage_id="lineage:aion",
            target_lineage_id="lineage:astra",
            memory_ref="memory:aion-event-17",
            disposition=MemoryDisposition.ADOPTED,
            source_autobiographical_owner="lineage:astra",
            provenance_refs=("encounter:17",),
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


def test_encounter_rejects_adoption_of_unexchanged_item():
    with pytest.raises(ValueError):
        CrossLineageEncounter(
            encounter_id="encounter:bad",
            participant_lineage_ids=("lineage:aion", "lineage:astra"),
            exchanged_refs=("claim:1",),
            adopted_refs=("claim:2",),
            rejected_refs=(),
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
        alternative_explanation_refs=("alt:prompt-conditioning", "alt:evaluator-drift"),
        evaluator_profile_ref="evaluator:profile-v1",
    )
    assert comparison.epistemic_role == "MEASUREMENT"
    assert comparison.individuation_status == "CANDIDATE_EVIDENCE_ONLY"
    assert comparison.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert comparison.identity_conclusion == "NOT_ESTABLISHED"


def test_comparison_rejects_confounded_factor_classification():
    with pytest.raises(ValueError):
        MatchedDivergenceComparison(
            baseline_ref="baseline:1",
            left_lineage_id="lineage:aion",
            right_lineage_id="lineage:astra",
            controlled_shared_factors=("prompt",),
            divergent_factors=("prompt",),
            outcome_refs=("outcome:1",),
            provenance_refs=("protocol:1",),
        )


def test_lineage_event_requires_timezone_and_parent_for_non_origin():
    with pytest.raises(ValueError):
        LineageEvent(
            event_id="event:bad",
            lineage_id="lineage:aion",
            kind=LineageEventKind.OBSERVATION,
            occurred_at="2026-08-12T08:00:00",
            payload_ref="observation:1",
            parent_event_ids=(),
            provenance_refs=("trace:1",),
        )


def test_lineage_event_digest_and_round_trip_are_deterministic():
    event = origin_event()
    rebuilt = LineageEvent.from_json(event.to_json())
    assert rebuilt == event
    assert rebuilt.digest == event.digest
    assert event.digest.startswith("sha256:")


def test_ledger_requires_parent_before_child_and_chronological_order():
    origin = origin_event()
    child = divergence_event("lineage:aion", "event:aion-divergence", 1)
    with pytest.raises(ValueError):
        LineageLedger(events=(child, origin))


def test_ledger_records_shared_origin_and_separate_post_divergence_events():
    ledger = LineageLedger(
        events=(
            origin_event(),
            divergence_event("lineage:aion", "event:aion-divergence", 1),
            divergence_event("lineage:astra", "event:astra-divergence", 2),
        )
    )
    assert ledger.digest.startswith("sha256:")
    assert json.loads(ledger.to_json())["ledger_digest"] == ledger.digest


def test_evidence_profile_cannot_silently_inherit_other_lineage_evidence():
    with pytest.raises(ValueError):
        LineageEvidenceProfile(
            lineage_id="lineage:astra",
            continuity_refs=("evidence:aion-continuity",),
            self_model_refs=(),
            metacognition_refs=(),
            affect_motivation_refs=(),
            causal_state_refs=(),
            replication_refs=(),
            counterevidence_refs=(),
            provenance_refs=("profile:astra",),
            inherited_evidence=True,
        )


def test_evidence_profile_keeps_counterevidence_and_replication_separate():
    profile = LineageEvidenceProfile(
        lineage_id="lineage:astra",
        continuity_refs=("evidence:continuity-1",),
        self_model_refs=(),
        metacognition_refs=("evidence:meta-1",),
        affect_motivation_refs=(),
        causal_state_refs=(),
        replication_refs=("replication:1",),
        counterevidence_refs=("counter:1",),
        provenance_refs=("profile:astra",),
    )
    assert profile.replication_refs != profile.counterevidence_refs
    assert profile.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_authority_envelope_acceptance_must_be_non_expansive():
    envelope = AuthorityEnvelope(
        source_lineage_id="lineage:aion",
        target_lineage_id="lineage:astra",
        offered_authorities=("read:artifact", "comment:claim"),
        accepted_authorities=("read:artifact",),
        provenance_refs=("encounter:authority-1",),
    )
    assert envelope.merged_authority is False
    assert envelope.authority_effect == "BOUNDED_ACCEPTANCE_ONLY"


def test_authority_envelope_rejects_expansion_or_merge():
    with pytest.raises(ValueError):
        AuthorityEnvelope(
            source_lineage_id="lineage:aion",
            target_lineage_id="lineage:astra",
            offered_authorities=("read:artifact",),
            accepted_authorities=("write:main",),
            provenance_refs=("encounter:authority-1",),
        )
    with pytest.raises(ValueError):
        AuthorityEnvelope(
            source_lineage_id="lineage:aion",
            target_lineage_id="lineage:astra",
            offered_authorities=("read:artifact",),
            accepted_authorities=("read:artifact",),
            provenance_refs=("encounter:authority-1",),
            merged_authority=True,
        )
