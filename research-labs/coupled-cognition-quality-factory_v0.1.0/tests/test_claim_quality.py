import json
import shutil
from dataclasses import fields
from pathlib import Path

import pytest

from aion_coupled_quality import (
    ClaimAdmissionDisposition,
    ChallengeResolution,
    ClaimDependency,
    ClaimLayer,
    ClaimLevel,
    ClaimRevision,
    ClaimStatus,
    ContributionOrigin,
    ContributionRecord,
    CounterDisposition,
    CounterEvidenceItem,
    EpistemicProvenanceLedger,
    Evidence,
    EvidenceBinding,
    EvidenceKind,
    EvidenceRelation,
    ProvenanceClaimQualityGate,
    PublicationClass,
    QualityFactory,
    ResearchClaimRecord,
    ResearchLot,
    Severity,
    load_canonical_claim_contract,
)
from aion_coupled_quality.claim_quality import _ADAPTER_FIELD_MAPPING


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parents[1]


def _ledger(*, unknown_claim_origin: bool = False) -> EpistemicProvenanceLedger:
    ledger = EpistemicProvenanceLedger()
    ledger.add(
        ContributionRecord(
            record_id="claim-provenance",
            proposition="A bounded observation motivates a revisable research claim.",
            origin=(ContributionOrigin.UNKNOWN if unknown_claim_origin else ContributionOrigin.HUMAN_ORIGIN),
            layer=ClaimLayer.OBSERVATION,
            source_refs=(() if unknown_claim_origin else ("fixture:public-safe-observation",)),
        )
    )
    ledger.add(
        ContributionRecord(
            record_id="resolution-provenance",
            proposition="A review receipt addresses the named challenge.",
            origin=ContributionOrigin.AI_FORMALIZATION,
            layer=ClaimLayer.CORRECTION,
        )
    )
    for record_id, source in (("replication-a", "fixture:replication-a"), ("replication-b", "fixture:replication-b")):
        ledger.add(
            ContributionRecord(
                record_id=record_id,
                proposition="Separated replication provenance.",
                origin=ContributionOrigin.EXTERNAL_SOURCE,
                layer=ClaimLayer.SOURCE_REPORT,
                source_refs=(source,),
            )
        )
    ledger.add(
        ContributionRecord(
            record_id="support-provenance",
            proposition="Public-safe evidence record.",
            origin=ContributionOrigin.EXTERNAL_SOURCE,
            layer=ClaimLayer.SOURCE_REPORT,
            source_refs=("fixture:public-safe-evidence",),
        )
    )
    ledger.add(
        ContributionRecord(
            record_id="challenge-provenance",
            proposition="A competing explanation remains possible.",
            origin=ContributionOrigin.AI_FORMALIZATION,
            layer=ClaimLayer.HYPOTHESIS,
        )
    )
    return ledger


def _lot(*, final_qa: bool = True, second_support: bool = False) -> ResearchLot:
    lot = ResearchLot(lot_id="LOT-1", claim="bounded observation claim", risk=Severity.MEDIUM)
    factory = QualityFactory(lot)
    factory.set_falsifier("A matched observation contradicts the proposed distinction.")
    factory.add_evidence(
        Evidence(
            evidence_id="E-1",
            kind=EvidenceKind.EXTERNAL_PRIMARY,
            reference="fixture:public-safe-evidence",
            supports_claim=True,
            independent_of_current_pair=True,
        )
    )
    if second_support:
        factory.add_evidence(
            Evidence(
                evidence_id="E-2",
                kind=EvidenceKind.EXTERNAL_PRIMARY,
                reference="fixture:replication-b",
                supports_claim=True,
                independent_of_current_pair=True,
            )
        )
    factory.add_counterevidence(
        CounterEvidenceItem(
            item_id="C-1",
            reference="fixture:alternative",
            challenge="The observation may be a recency effect.",
        )
    )
    factory.dispose_counterevidence("C-1", CounterDisposition.ACCEPTED)
    if final_qa:
        assert factory.final_qa() is True
    return lot


def _claim(**changes: object) -> ResearchClaimRecord:
    defaults = dict(
        claim_id="CLAIM-1",
        version=1,
        statement="The bounded observation is retained as an anomaly requiring recheck.",
        provenance_record_id="claim-provenance",
        claim_level=ClaimLevel.L0_OBSERVATION,
        status=ClaimStatus.OBSERVED,
        observed_evidence_ids=("E-1",),
        inferred_statements=("The prior expectation may have been too broad.",),
        competing_explanations=("Recency effect", "Unrecorded prior knowledge"),
        falsifier="Repeated observations match the prior expectation.",
        supporting_evidence_ids=("E-1",),
    )
    defaults.update(changes)
    return ResearchClaimRecord(**defaults)


def _bindings(**changes: object) -> tuple[EvidenceBinding, ...]:
    defaults = dict(
        evidence_id="E-1",
        provenance_record_id="support-provenance",
        relation=EvidenceRelation.SUPPORTS,
        publication_class=PublicationClass.PUBLIC_SAFE,
        naturalistic_case_id="CASE-1",
    )
    defaults.update(changes)
    return (EvidenceBinding(**defaults),)


def _assess(
    claim: ResearchClaimRecord,
    *,
    ledger: EpistemicProvenanceLedger | None = None,
    lot: ResearchLot | None = None,
    bindings: tuple[EvidenceBinding, ...] | None = None,
    known_claims: tuple[ResearchClaimRecord, ...] = (),
):
    return ProvenanceClaimQualityGate().assess(
        claim,
        ledger=ledger or _ledger(),
        lot=lot or _lot(),
        evidence_bindings=bindings or _bindings(),
        known_claims=known_claims,
        repository_root=REPOSITORY_ROOT,
    )


def test_positive_path_admits_only_a_bounded_research_record() -> None:
    result = _assess(_claim())
    assert result.disposition is ClaimAdmissionDisposition.ADMISSIBLE_AS_BOUNDED_RESEARCH_RECORD
    assert result.scientific_disposition == "HOLD"
    assert result.subjectivity == "NOT_ESTABLISHED"
    assert result.consciousness == "NOT_ESTABLISHED"
    assert result.phenomenal_experience == "NOT_ESTABLISHED"
    assert result.canonical_effect == "NONE"


def test_missing_and_invalid_provenance_fail_closed() -> None:
    missing = _assess(_claim(provenance_record_id=None))
    invalid = _assess(_claim(provenance_record_id="not-in-ledger"))
    assert "MISSING_PROVENANCE" in missing.reasons
    assert "INVALID_PROVENANCE:not-in-ledger" in invalid.reasons


def test_unknown_origin_is_not_guessed() -> None:
    result = _assess(_claim(), ledger=_ledger(unknown_claim_origin=True))
    assert result.disposition is ClaimAdmissionDisposition.HOLD
    assert "UNKNOWN_CLAIM_ORIGIN" in result.reasons


def test_invalid_evidence_provenance_fails_closed() -> None:
    result = _assess(_claim(), bindings=_bindings(provenance_record_id="missing-source"))
    assert "INVALID_PROVENANCE:missing-source" in result.reasons


def test_private_transcript_and_unknown_publication_class_are_blocked() -> None:
    private = _assess(_claim(), bindings=_bindings(publication_class=PublicationClass.PRIVATE_TRANSCRIPT))
    unknown = _assess(_claim(), bindings=_bindings(publication_class=PublicationClass.UNKNOWN))
    assert "PRIVATE_TRANSCRIPT_NOT_PUBLISHABLE:E-1" in private.reasons
    assert "UNKNOWN_PUBLICATION_CLASS:E-1" in unknown.reasons


def test_private_or_unknown_claim_payload_is_blocked() -> None:
    private = _assess(_claim(publication_class=PublicationClass.PRIVATE_TRANSCRIPT))
    unknown = _assess(_claim(publication_class=PublicationClass.UNKNOWN))
    assert "PRIVATE_TRANSCRIPT_CLAIM_NOT_PUBLISHABLE" in private.reasons
    assert "UNKNOWN_CLAIM_PUBLICATION_CLASS" in unknown.reasons


def test_quality_factory_final_qa_is_required_but_is_not_scientific_validation() -> None:
    result = _assess(_claim(), lot=_lot(final_qa=False))
    assert "QUALITY_FACTORY_FINAL_QA_NOT_PASSED" in result.reasons
    assert result.scientific_disposition == "HOLD"


def test_quality_lot_cannot_grant_canonical_or_deployment_authority() -> None:
    lot = _lot()
    lot.deployment = True
    result = _assess(_claim(), lot=lot)
    assert "QUALITY_LOT_CANNOT_GRANT_CANONICAL_OR_DEPLOYMENT_AUTHORITY" in result.reasons


def test_unresolved_contradictory_evidence_blocks_admission() -> None:
    bindings = _bindings() + (
        EvidenceBinding(
            evidence_id="C-1",
            provenance_record_id="challenge-provenance",
            relation=EvidenceRelation.CHALLENGES,
            publication_class=PublicationClass.PUBLIC_SAFE,
        ),
    )
    result = _assess(_claim(challenging_evidence_ids=("C-1",)), bindings=bindings)
    assert "UNRESOLVED_CONTRADICTORY_EVIDENCE:C-1" in result.reasons


def test_resolved_challenge_retains_the_link() -> None:
    bindings = _bindings() + (
        EvidenceBinding(
            evidence_id="C-1",
            provenance_record_id="challenge-provenance",
            relation=EvidenceRelation.CHALLENGES,
            publication_class=PublicationClass.PUBLIC_SAFE,
        ),
    )
    result = _assess(
        _claim(
            challenging_evidence_ids=("C-1",),
            resolved_challenge_ids=("C-1",),
            challenge_resolutions=(
                ChallengeResolution("C-1", "CLAIM-1", 1, "fixture:resolution", "resolution-provenance"),
            ),
        ),
        bindings=bindings,
    )
    assert result.disposition is ClaimAdmissionDisposition.ADMISSIBLE_AS_BOUNDED_RESEARCH_RECORD


def test_observation_cannot_be_promoted_to_mechanism_without_intervention() -> None:
    result = _assess(_claim(claim_level=ClaimLevel.L3_INTERVENTION_SENSITIVE_MECHANISM))
    assert "MECHANISM_PROMOTION_REQUIRES_INTERVENTION_SENSITIVE_EVIDENCE" in result.reasons


def test_observed_evidence_must_have_a_binding_but_need_not_be_support() -> None:
    result = _assess(_claim(observed_evidence_ids=("UNBOUND",)))
    assert "MISSING_EVIDENCE_BINDING:UNBOUND" in result.reasons

    observed = EvidenceBinding(
        evidence_id="O-1",
        provenance_record_id="support-provenance",
        relation=EvidenceRelation.OBSERVES,
        publication_class=PublicationClass.PUBLIC_SAFE,
    )
    separated = _assess(_claim(observed_evidence_ids=("O-1",)), bindings=_bindings() + (observed,))
    assert separated.disposition is ClaimAdmissionDisposition.ADMISSIBLE_AS_BOUNDED_RESEARCH_RECORD


def test_same_author_same_runtime_repeats_do_not_reach_l4() -> None:
    bindings = tuple(
        EvidenceBinding(
            evidence_id=evidence_id,
            provenance_record_id="support-provenance",
            relation=EvidenceRelation.SUPPORTS,
            publication_class=PublicationClass.PUBLIC_SAFE,
            intervention_sensitive=True,
            held_out=True,
            repeated=True,
            producer_ref="same-author",
            runtime_or_context_ref="same-runtime",
            replication_source_ref=f"fixture:{evidence_id}",
            replication_provenance_record_id=provenance,
        )
        for evidence_id, provenance in (("E-1", "replication-a"), ("E-2", "replication-b"))
    )
    result = _assess(
        _claim(claim_level=ClaimLevel.L4_ROBUST_REPLICATION, supporting_evidence_ids=("E-1", "E-2")),
        lot=_lot(second_support=True),
        bindings=bindings,
    )
    assert "L4_REQUIRES_DISTINCT_PRODUCERS" in result.reasons
    assert "L4_REQUIRES_DISTINCT_RUNTIME_OR_CONTEXT" in result.reasons


def test_l4_separation_is_structurally_admissible_not_scientific_truth() -> None:
    bindings = tuple(
        EvidenceBinding(
            evidence_id=evidence_id,
            provenance_record_id="support-provenance",
            relation=EvidenceRelation.SUPPORTS,
            publication_class=PublicationClass.PUBLIC_SAFE,
            intervention_sensitive=True,
            held_out=True,
            repeated=True,
            producer_ref=producer,
            runtime_or_context_ref=runtime,
            replication_source_ref=f"fixture:{evidence_id}",
            replication_provenance_record_id=provenance,
        )
        for evidence_id, producer, runtime, provenance in (
            ("E-1", "producer-a", "runtime-a", "replication-a"),
            ("E-2", "producer-b", "runtime-b", "replication-b"),
        )
    )
    result = _assess(
        _claim(claim_level=ClaimLevel.L4_ROBUST_REPLICATION, supporting_evidence_ids=("E-1", "E-2")),
        lot=_lot(second_support=True),
        bindings=bindings,
    )
    assert result.disposition is ClaimAdmissionDisposition.ADMISSIBLE_AS_BOUNDED_RESEARCH_RECORD
    assert result.scientific_disposition == "HOLD"
    assert result.subjectivity == "NOT_ESTABLISHED"


def test_resolved_marker_without_traceable_resolution_holds() -> None:
    binding = EvidenceBinding(
        "C-1", "challenge-provenance", EvidenceRelation.CHALLENGES, PublicationClass.PUBLIC_SAFE
    )
    result = _assess(
        _claim(challenging_evidence_ids=("C-1",), resolved_challenge_ids=("C-1",)),
        bindings=_bindings() + (binding,),
    )
    assert "MISSING_CHALLENGE_RESOLUTION_EVIDENCE:C-1" in result.reasons


def test_stale_unrelated_unknown_and_circular_resolutions_hold() -> None:
    binding = EvidenceBinding(
        "C-1", "challenge-provenance", EvidenceRelation.CHALLENGES, PublicationClass.PUBLIC_SAFE
    )
    ledger = _ledger()
    ledger.add(
        ContributionRecord(
            record_id="unknown-resolution",
            proposition="Unknown resolution source.",
            origin=ContributionOrigin.UNKNOWN,
            layer=ClaimLayer.CORRECTION,
        )
    )
    cases = (
        (ChallengeResolution("C-1", "OTHER", 1, "fixture:resolution", "resolution-provenance"), "STALE_OR_UNRELATED_CHALLENGE_RESOLUTION:C-1"),
        (ChallengeResolution("C-1", "CLAIM-1", 2, "fixture:resolution", "resolution-provenance"), "STALE_OR_UNRELATED_CHALLENGE_RESOLUTION:C-1"),
        (ChallengeResolution("C-1", "CLAIM-1", 1, "fixture:resolution", "unknown-resolution"), "UNKNOWN_RESOLUTION_ORIGIN:C-1"),
        (ChallengeResolution("C-1", "CLAIM-1", 1, "C-1", "resolution-provenance"), "CIRCULAR_CHALLENGE_RESOLUTION:C-1"),
    )
    for resolution, expected in cases:
        result = _assess(
            _claim(
                challenging_evidence_ids=("C-1",),
                resolved_challenge_ids=("C-1",),
                challenge_resolutions=(resolution,),
            ),
            bindings=_bindings() + (binding,),
            ledger=ledger,
        )
        assert expected in result.reasons


def test_resolution_must_link_to_the_claim_revision() -> None:
    binding = EvidenceBinding(
        "C-1", "challenge-provenance", EvidenceRelation.CHALLENGES, PublicationClass.PUBLIC_SAFE
    )
    prior = _claim()
    claim = _claim(
        version=2,
        status=ClaimStatus.REVISED,
        challenging_evidence_ids=("C-1",),
        resolved_challenge_ids=("C-1",),
        challenge_resolutions=(
            ChallengeResolution(
                "C-1", "CLAIM-1", 2, "fixture:unrelated-review", "resolution-provenance"
            ),
        ),
        revision=ClaimRevision(
            "CLAIM-1", 1, 2, ("statement",), "fixture:actual-revision-receipt"
        ),
    )
    result = _assess(claim, bindings=_bindings() + (binding,), known_claims=(prior,))
    assert "RESOLUTION_REVISION_LINK_MISMATCH:C-1" in result.reasons


def test_adapter_contract_is_bound_to_canonical_schema_and_protocol() -> None:
    contract = load_canonical_claim_contract(REPOSITORY_ROOT)
    assert contract.schema_version == "0.2.0"
    assert contract.claim_levels == tuple(item.value for item in ClaimLevel)
    assert {name for name, _ in contract.adapter_field_mapping} == {
        item.name for item in fields(ResearchClaimRecord)
    }


def test_adapter_contract_fails_on_schema_or_mapping_drift(tmp_path: Path) -> None:
    (tmp_path / "schemas").mkdir()
    (tmp_path / "docs").mkdir()
    shutil.copy(REPOSITORY_ROOT / "schemas/research_evidence_record_v0.2.0.schema.json", tmp_path / "schemas")
    shutil.copy(REPOSITORY_ROOT / "docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md", tmp_path / "docs")
    schema_path = tmp_path / "schemas/research_evidence_record_v0.2.0.schema.json"
    schema = json.loads(schema_path.read_text())
    schema["properties"]["claim_level"]["enum"].append("L6_UNDEFINED")
    schema_path.write_text(json.dumps(schema))
    with pytest.raises(Exception, match="CLAIM_LEVEL_MAPPING_DRIFT"):
        load_canonical_claim_contract(tmp_path)

    shutil.copy(REPOSITORY_ROOT / "schemas/research_evidence_record_v0.2.0.schema.json", schema_path)
    missing = dict(_ADAPTER_FIELD_MAPPING)
    missing.pop("claim_id")
    with pytest.raises(Exception, match="ADAPTER_FIELD_MAPPING_INCOMPLETE"):
        load_canonical_claim_contract(tmp_path, field_mapping=missing)
    unsupported = dict(_ADAPTER_FIELD_MAPPING)
    unsupported["claim_id"] = "imaginary_semantics.claim_id"
    with pytest.raises(Exception, match="UNSUPPORTED_FIELD_SEMANTICS"):
        load_canonical_claim_contract(tmp_path, field_mapping=unsupported)


def test_gate_holds_without_canonical_binding() -> None:
    result = ProvenanceClaimQualityGate().assess(
        _claim(), ledger=_ledger(), lot=_lot(), evidence_bindings=_bindings()
    )
    assert "MISSING_CANONICAL_SCHEMA_PROTOCOL_BINDING" in result.reasons


def test_mechanism_cannot_be_promoted_to_phenomenology_or_subjectivity() -> None:
    binding = _bindings(intervention_sensitive=True)
    result = _assess(
        _claim(
            claim_level=ClaimLevel.L3_INTERVENTION_SENSITIVE_MECHANISM,
            subjectivity_claim=True,
            consciousness_claim=True,
            phenomenal_experience_claim=True,
            moral_agency_claim=True,
            moral_status_claim=True,
        ),
        bindings=binding,
    )
    assert "SUBJECTIVITY_PROMOTION_PROHIBITED" in result.reasons
    assert "CONSCIOUSNESS_PROMOTION_PROHIBITED" in result.reasons
    assert "PHENOMENAL_EXPERIENCE_PROMOTION_PROHIBITED" in result.reasons
    assert "MORAL_AGENCY_PROMOTION_PROHIBITED" in result.reasons
    assert "MORAL_STATUS_PROMOTION_PROHIBITED" in result.reasons
    assert result.subjectivity == "NOT_ESTABLISHED"


def test_single_naturalistic_case_cannot_become_population_claim() -> None:
    result = _assess(_claim(population_scope=True))
    assert "SINGLE_NATURALISTIC_CASE_CANNOT_SUPPORT_POPULATION_CLAIM" in result.reasons


def test_single_transfer_observation_cannot_become_causal_learning_claim() -> None:
    result = _assess(
        _claim(causal_learning_effect=True),
        bindings=_bindings(transfer_candidate=True),
    )
    assert "TRANSFER_OBSERVATION_CANNOT_ESTABLISH_CAUSAL_LEARNING_EFFECT" in result.reasons


def test_dependency_hold_propagates_to_downstream_claim() -> None:
    upstream = _claim(claim_id="UPSTREAM", status=ClaimStatus.HOLD)
    downstream = _claim(dependencies=(ClaimDependency("UPSTREAM", 1),))
    result = _assess(downstream, known_claims=(upstream,))
    assert "DEPENDENCY_HOLD:UPSTREAM@1" in result.reasons


def test_stale_dependency_and_stale_revision_are_rejected() -> None:
    old = _claim(claim_id="PRIOR", version=1)
    current = _claim(claim_id="PRIOR", version=2, status=ClaimStatus.RETAINED)
    revised = _claim(
        claim_id="PRIOR",
        version=3,
        status=ClaimStatus.REVISED,
        dependencies=(ClaimDependency("PRIOR", 1),),
        revision=ClaimRevision(
            previous_claim_id="PRIOR",
            previous_version=1,
            new_version=3,
            changed_fields=("statement",),
            rationale_ref="fixture:revision-rationale",
        ),
    )
    result = _assess(revised, known_claims=(old, current))
    assert "STALE_DEPENDENCY:PRIOR@1" in result.reasons
    assert "STALE_REVISION_BASE" in result.reasons


def test_public_safe_naturalistic_fixture_preserves_boundaries() -> None:
    fixture = json.loads((ROOT / "fixtures" / "naturalistic_learning_case_2026-09-11.json").read_text(encoding="utf-8"))
    assert fixture["raw_private_transcript"] == "NOT_PUBLISHED"
    assert fixture["scientific_disposition"] == "HOLD"
    assert fixture["subjectivity"] == "NOT_ESTABLISHED"
    assert fixture["claims"]["transfer"] == "TRANSFER_CANDIDATE"
    assert "DELIBERATE_PRETENDING" in fixture["competing_explanations"]
    assert fixture["provenance"]["formalization"] == "AI_FORMALIZATION"


def test_deterministic_assessment() -> None:
    first = _assess(_claim())
    second = _assess(_claim())
    assert first == second
