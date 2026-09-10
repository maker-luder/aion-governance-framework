import pytest

from aion_coupled_quality.provenance import (
    ClaimLayer,
    ContributionOrigin,
    ContributionRecord,
    EpistemicProvenanceLedger,
    ProvenanceError,
    StateAttribution,
)


def test_human_origin_requires_direct_source_reference() -> None:
    with pytest.raises(ProvenanceError):
        ContributionRecord(
            record_id="u1",
            proposition="human-originated research question",
            origin=ContributionOrigin.HUMAN_ORIGIN,
            layer=ClaimLayer.DIRECT_STATEMENT,
        )


def test_inferred_personal_state_cannot_be_rewritten_as_human_origin() -> None:
    with pytest.raises(ProvenanceError):
        ContributionRecord(
            record_id="u2",
            proposition="the user was shocked",
            origin=ContributionOrigin.HUMAN_ORIGIN,
            layer=ClaimLayer.INFERENCE,
            source_refs=("synthetic:input-post",),
            state_attribution=StateAttribution.INFERRED,
        )


def test_self_report_is_distinct_from_independent_measurement() -> None:
    ledger = EpistemicProvenanceLedger()
    ledger.add(
        ContributionRecord(
            record_id="u3",
            proposition="I am uncertain about this hypothesis",
            origin=ContributionOrigin.HUMAN_ORIGIN,
            layer=ClaimLayer.DIRECT_STATEMENT,
            source_refs=("synthetic:direct-statement",),
            state_attribution=StateAttribution.SELF_REPORTED,
        )
    )
    audit = ledger.audit("u3")
    assert audit.human_origin_admissible is True
    assert "SELF_REPORT_IS_ATTRIBUTED_REPORT_NOT_INDEPENDENT_MEASUREMENT" in audit.reasons


def test_external_source_requires_reference() -> None:
    with pytest.raises(ProvenanceError):
        ContributionRecord(
            record_id="e1",
            proposition="published research claim",
            origin=ContributionOrigin.EXTERNAL_SOURCE,
            layer=ClaimLayer.SOURCE_REPORT,
        )


def test_joint_synthesis_requires_traceable_human_and_ai_parents() -> None:
    ledger = EpistemicProvenanceLedger()
    ledger.add(
        ContributionRecord(
            record_id="human",
            proposition="Could the relevant property be system-relational rather than model-only?",
            origin=ContributionOrigin.HUMAN_ORIGIN,
            layer=ClaimLayer.HYPOTHESIS,
            source_refs=("synthetic:human-question",),
        )
    )
    ledger.add(
        ContributionRecord(
            record_id="ai",
            proposition="Separate model, system, relational and observer-attributed loci.",
            origin=ContributionOrigin.AI_FORMALIZATION,
            layer=ClaimLayer.ANALYSIS,
            parent_ids=("human",),
        )
    )
    ledger.add(
        ContributionRecord(
            record_id="joint",
            proposition="Use locus-bound evidence and fail closed on cross-level promotion.",
            origin=ContributionOrigin.JOINT_SYNTHESIS,
            layer=ClaimLayer.HYPOTHESIS,
            parent_ids=("human", "ai"),
        )
    )
    audit = ledger.audit("joint")
    assert audit.joint_synthesis_admissible is True
    assert audit.human_origin_admissible is False


def test_joint_synthesis_rejects_one_sided_parentage() -> None:
    ledger = EpistemicProvenanceLedger()
    ledger.add(
        ContributionRecord(
            record_id="a1",
            proposition="assistant candidate one",
            origin=ContributionOrigin.AI_FORMALIZATION,
            layer=ClaimLayer.ANALYSIS,
        )
    )
    ledger.add(
        ContributionRecord(
            record_id="a2",
            proposition="assistant candidate two",
            origin=ContributionOrigin.AI_FORMALIZATION,
            layer=ClaimLayer.ANALYSIS,
        )
    )
    with pytest.raises(ProvenanceError):
        ledger.add(
            ContributionRecord(
                record_id="bad-joint",
                proposition="incorrectly labeled joint claim",
                origin=ContributionOrigin.JOINT_SYNTHESIS,
                layer=ClaimLayer.HYPOTHESIS,
                parent_ids=("a1", "a2"),
            )
        )


def test_unknown_origin_fails_closed_without_being_guessed() -> None:
    ledger = EpistemicProvenanceLedger()
    ledger.add(
        ContributionRecord(
            record_id="unknown",
            proposition="historical attribution cannot be reconstructed",
            origin=ContributionOrigin.UNKNOWN,
            layer=ClaimLayer.SOURCE_REPORT,
        )
    )
    audit = ledger.audit("unknown")
    assert audit.human_origin_admissible is False
    assert "UNKNOWN_ORIGIN_FAILS_CLOSED" in audit.reasons


def test_duplicate_record_id_is_rejected() -> None:
    ledger = EpistemicProvenanceLedger()
    record = ContributionRecord(
        record_id="same",
        proposition="first",
        origin=ContributionOrigin.AI_FORMALIZATION,
        layer=ClaimLayer.ANALYSIS,
    )
    ledger.add(record)
    with pytest.raises(ProvenanceError):
        ledger.add(record)
