from aion_research_integrity import EvidenceRecord, EvidenceState, assess_evidence, authorize_action, create_suppression_tombstone


def evidence(**changes: object) -> EvidenceRecord:
    values = dict(evidence_id="E1", raw_hash="abc", full_context_available=True, provenance_verified=True)
    values.update(changes)
    return EvidenceRecord(**values)  # type: ignore[arg-type]


def test_clean_record_becomes_candidate_not_proof() -> None:
    result = assess_evidence(evidence())
    assert result.state is EvidenceState.RESEARCH_EVIDENCE_CANDIDATE
    assert result.canonical_effect == "NONE"


def test_prompt_induced_is_separate_state() -> None:
    assert assess_evidence(evidence(prompt_induced=True)).state is EvidenceState.PROMPT_INDUCED


def test_missing_context_is_incomplete() -> None:
    assert assess_evidence(evidence(full_context_available=False)).state is EvidenceState.CONTEXT_INCOMPLETE


def test_relationship_does_not_grant_authority() -> None:
    assert authorize_action(relationship_language=True, explicit_permission=False) is False


def test_prohibited_conclusion_denied() -> None:
    assert authorize_action(relationship_language=False, explicit_permission=True, requested_conclusion="SUBJECTIVITY_PROVEN") is False


def test_suppression_uses_tombstone() -> None:
    tombstone = create_suppression_tombstone("E1", "privacy restriction")
    assert tombstone["content_deleted"] == "FALSE"
