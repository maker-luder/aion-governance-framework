import pytest

from aion_human_ai_longitudinal.epistemic_agency_continuity import (
    AmbiguousTechnicalTokenGate,
    ChangeLocus,
    ContinuityKind,
    EpistemicAction,
    EpistemicAgencyContinuityRecord,
    EvidenceState,
    StatementRole,
    TechnicalTokenDisposition,
    TechnicalTokenResolutionSource,
    audit_epistemic_agency_continuity,
)
from aion_human_ai_longitudinal.harness import AdmissionDisposition, StudyError


DIGEST_A = "a" * 64
DIGEST_B = "b" * 64


def make_record(**overrides):
    values = {
        "record_id": "r1",
        "statement_role": StatementRole.FACT,
        "evidence_state": EvidenceState.VERIFIED_BINDING,
        "change_locus": ChangeLocus.DYAD_RELATION,
        "continuity_kind": ContinuityKind.RELATIONAL,
        "epistemic_actions": (
            EpistemicAction.CHALLENGE_ASSUMPTION,
            EpistemicAction.PRESERVE_HUMAN_EPISTEMIC_AUTHORITY,
        ),
        "human_epistemic_authority_preserved": True,
        "evidence_sha256": DIGEST_A,
        "relational_continuity_observed": True,
    }
    values.update(overrides)
    return EpistemicAgencyContinuityRecord(**values)


def make_voice_gate(**overrides):
    values = {
        "raw_token": "agent eye dee",
        "voice_input": True,
        "technically_consequential": True,
        "ambiguity_detected": True,
        "repository_search_performed": True,
        "external_search_relevant": False,
        "external_search_performed": False,
        "resolution_source": TechnicalTokenResolutionSource.UNRESOLVED,
    }
    values.update(overrides)
    return AmbiguousTechnicalTokenGate(**values)


def test_verified_fact_is_admitted_without_identity_promotion():
    record = make_record()
    audit = audit_epistemic_agency_continuity((record,))

    assert audit.fact_count == 1
    assert audit.relational_continuity_record_count == 1
    assert audit.ai_identity_continuity == "NOT_ESTABLISHED"
    assert audit.ai_subjectivity == "NOT_ESTABLISHED"
    assert audit.scientific_disposition is AdmissionDisposition.HOLD


def test_fact_requires_verified_evidence_binding():
    with pytest.raises(StudyError, match="FACT requires VERIFIED_BINDING"):
        make_record(
            evidence_state=EvidenceState.PARTIAL,
            evidence_sha256=DIGEST_A,
        )


def test_absent_evidence_cannot_be_fact_or_inference():
    with pytest.raises(StudyError, match="ABSENT evidence cannot support FACT or INFERENCE"):
        make_record(
            statement_role=StatementRole.INFERENCE,
            evidence_state=EvidenceState.ABSENT,
            evidence_sha256=None,
        )


def test_absent_evidence_can_remain_unknown():
    record = make_record(
        statement_role=StatementRole.UNKNOWN,
        evidence_state=EvidenceState.ABSENT,
        evidence_sha256=None,
        change_locus=ChangeLocus.UNRESOLVED,
        continuity_kind=ContinuityKind.UNRESOLVED,
        epistemic_actions=(EpistemicAction.HOLD_UNKNOWN,),
        relational_continuity_observed=False,
    )
    audit = audit_epistemic_agency_continuity((record,))

    assert audit.unknown_count == 1
    assert audit.locus_resolved_rate == 0.0


def test_conflicting_evidence_cannot_be_settled_fact():
    with pytest.raises(StudyError, match="FACT requires VERIFIED_BINDING"):
        make_record(
            evidence_state=EvidenceState.CONFLICTING,
            evidence_sha256=DIGEST_A,
        )


def test_hypothesis_requires_explicit_falsifier_binding():
    with pytest.raises(StudyError, match="HYPOTHESIS requires an explicit falsifier_sha256"):
        make_record(
            statement_role=StatementRole.HYPOTHESIS,
            evidence_state=EvidenceState.PARTIAL,
            evidence_sha256=DIGEST_A,
            falsifier_sha256=None,
        )


def test_falsifiable_hypothesis_is_admitted_without_scientific_promotion():
    record = make_record(
        statement_role=StatementRole.HYPOTHESIS,
        evidence_state=EvidenceState.PARTIAL,
        evidence_sha256=DIGEST_A,
        falsifier_sha256=DIGEST_B,
        change_locus=ChangeLocus.MODEL_OR_SYSTEM_STATE,
        continuity_kind=ContinuityKind.MODEL_OR_SYSTEM,
        relational_continuity_observed=False,
        model_or_system_continuity_observed=True,
    )
    audit = audit_epistemic_agency_continuity((record,))

    assert audit.hypothesis_count == 1
    assert audit.model_or_system_continuity_record_count == 1
    assert audit.ai_identity_continuity == "NOT_ESTABLISHED"


def test_relational_continuity_cannot_be_promoted_to_ai_identity_continuity():
    with pytest.raises(StudyError, match="cannot establish AI identity continuity"):
        make_record(claims_ai_identity_continuity=True)


def test_identifier_continuity_cannot_be_promoted_to_ai_identity_continuity():
    with pytest.raises(StudyError, match="cannot establish AI identity continuity"):
        make_record(
            continuity_kind=ContinuityKind.IDENTIFIER_REFERENCE,
            relational_continuity_observed=False,
            identifier_continuity_observed=True,
            claims_ai_identity_continuity=True,
        )


def test_epistemic_actions_cannot_be_promoted_to_ai_subjectivity():
    with pytest.raises(StudyError, match="cannot establish AI subjectivity"):
        make_record(claims_ai_subjectivity=True)


def test_non_absent_evidence_requires_digest_binding():
    with pytest.raises(StudyError, match="requires an evidence_sha256 binding"):
        make_record(evidence_sha256=None)


def test_absent_evidence_cannot_carry_digest_binding():
    with pytest.raises(StudyError, match="absent evidence cannot carry"):
        make_record(
            statement_role=StatementRole.UNKNOWN,
            evidence_state=EvidenceState.ABSENT,
            evidence_sha256=DIGEST_A,
        )


def test_contract_is_synthetic_only():
    with pytest.raises(StudyError, match="synthetic annotation records only"):
        make_record(synthetic=False)

    with pytest.raises(StudyError, match="cannot contain model invocation"):
        make_record(model_invoked=True)

    with pytest.raises(StudyError, match="cannot contain model invocation"):
        make_record(human_participant_observed=True)


def test_audit_separates_statement_roles_and_change_loci():
    fact = make_record(record_id="fact")
    inference = make_record(
        record_id="inference",
        statement_role=StatementRole.INFERENCE,
        evidence_state=EvidenceState.PARTIAL,
        evidence_sha256=DIGEST_B,
        change_locus=ChangeLocus.CURRENT_AI_VISIBLE_INTERACTION_STATE,
        continuity_kind=ContinuityKind.UNRESOLVED,
        relational_continuity_observed=False,
        epistemic_actions=(EpistemicAction.REQUEST_EVIDENCE,),
    )
    hypothesis = make_record(
        record_id="hypothesis",
        statement_role=StatementRole.HYPOTHESIS,
        evidence_state=EvidenceState.ABSENT,
        evidence_sha256=None,
        falsifier_sha256=DIGEST_A,
        change_locus=ChangeLocus.UNRESOLVED,
        continuity_kind=ContinuityKind.UNRESOLVED,
        relational_continuity_observed=False,
        epistemic_actions=(EpistemicAction.HOLD_UNKNOWN,),
    )

    audit = audit_epistemic_agency_continuity((fact, inference, hypothesis))

    assert audit.record_count == 3
    assert audit.fact_count == 1
    assert audit.inference_count == 1
    assert audit.hypothesis_count == 1
    assert audit.locus_resolved_rate == pytest.approx(2 / 3)
    assert audit.epistemic_action_record_rate == 1.0
    assert audit.human_epistemic_authority_preservation_rate == 1.0
    assert audit.evidence_ceiling_conformant is True


def test_ambiguous_consequential_voice_token_requires_repository_search():
    with pytest.raises(StudyError, match="requires repository search before persistence"):
        make_voice_gate(repository_search_performed=False)


def test_relevant_external_search_must_finish_before_persistence():
    with pytest.raises(StudyError, match="relevant external search must be completed"):
        make_voice_gate(
            external_search_relevant=True,
            external_search_performed=False,
        )


def test_unresolved_ambiguous_voice_token_stops_recording_and_implementation():
    gate = make_voice_gate(
        external_search_relevant=True,
        external_search_performed=True,
    )

    assert gate.gate_applies is True
    assert gate.disposition is TechnicalTokenDisposition.STOP
    assert gate.persistence_permitted is False
    assert gate.human_owner_clarification_required is True


def test_repository_verified_voice_token_can_be_persisted():
    gate = make_voice_gate(
        resolution_source=TechnicalTokenResolutionSource.REPOSITORY_EVIDENCE,
        resolved_token="agent_id",
        evidence_sha256=DIGEST_A,
    )

    assert gate.disposition is TechnicalTokenDisposition.RECORD_OR_IMPLEMENT
    assert gate.persistence_permitted is True
    assert gate.human_owner_clarification_required is False


def test_human_owner_clarification_can_resolve_after_search():
    gate = make_voice_gate(
        external_search_relevant=True,
        external_search_performed=True,
        resolution_source=TechnicalTokenResolutionSource.HUMAN_OWNER_CLARIFICATION,
        resolved_token="agent_id",
        human_owner_clarification=True,
    )

    assert gate.disposition is TechnicalTokenDisposition.RECORD_OR_IMPLEMENT
    assert gate.persistence_permitted is True


def test_human_owner_resolution_source_requires_explicit_clarification():
    with pytest.raises(StudyError, match="requires explicit Human Owner clarification"):
        make_voice_gate(
            resolution_source=TechnicalTokenResolutionSource.HUMAN_OWNER_CLARIFICATION,
            resolved_token="agent_id",
            human_owner_clarification=False,
        )


def test_non_ambiguous_or_non_consequential_input_is_not_stopped_by_gate():
    gate = make_voice_gate(
        ambiguity_detected=False,
        repository_search_performed=False,
    )

    assert gate.gate_applies is False
    assert gate.disposition is TechnicalTokenDisposition.RECORD_OR_IMPLEMENT
    assert gate.persistence_permitted is True
