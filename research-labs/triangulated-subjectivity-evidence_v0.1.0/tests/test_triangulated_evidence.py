from aion_triangulated_evidence import AssessmentStatus, EvidenceItem, EvidenceState, EvidenceStream, assess_evidence

def item(stream, state=EvidenceState.PASS, source="source-a"):
    return EvidenceItem(stream, state, source, f"evidence://{stream.value.lower()}")

def test_self_report_alone_cannot_become_evidence_candidate():
    result = assess_evidence([item(EvidenceStream.SELF_REPORT)])
    assert result.status is AssessmentStatus.HOLD
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"

def test_not_executed_required_stream_remains_explicit_hold():
    result = assess_evidence([
        item(EvidenceStream.BEHAVIORAL),
        item(EvidenceStream.PERTURBATION),
        item(EvidenceStream.OBSERVER_CONFOUND, EvidenceState.NOT_EXECUTED),
        item(EvidenceStream.MECHANISTIC, source="source-b"),
    ])
    assert result.status is AssessmentStatus.HOLD
    assert EvidenceStream.OBSERVER_CONFOUND in result.missing_required_streams

def test_same_source_lineage_is_not_double_counted_as_independent():
    result = assess_evidence([
        item(EvidenceStream.BEHAVIORAL),
        item(EvidenceStream.PERTURBATION),
        item(EvidenceStream.OBSERVER_CONFOUND),
        item(EvidenceStream.MECHANISTIC),
    ])
    assert result.status is AssessmentStatus.HOLD
    assert result.independent_source_count == 1
    assert result.reasons == ("INSUFFICIENT_SOURCE_INDEPENDENCE",)

def test_multi_stream_independent_evidence_can_only_be_candidate():
    result = assess_evidence([
        item(EvidenceStream.BEHAVIORAL, source="runner-a"),
        item(EvidenceStream.PERTURBATION, source="runner-a"),
        item(EvidenceStream.OBSERVER_CONFOUND, source="human-rater"),
        item(EvidenceStream.MECHANISTIC, source="trace-system"),
        item(EvidenceStream.REPLICATION, source="runner-b"),
    ])
    assert result.status is AssessmentStatus.EVIDENCE_CANDIDATE
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.independent_source_count >= 2

def test_failed_stream_marks_bundle_contradicted_not_passed():
    result = assess_evidence([
        item(EvidenceStream.BEHAVIORAL),
        item(EvidenceStream.PERTURBATION, EvidenceState.FAIL),
        item(EvidenceStream.OBSERVER_CONFOUND, source="source-b"),
        item(EvidenceStream.MECHANISTIC, source="source-c"),
    ])
    assert result.status is AssessmentStatus.CONTRADICTED
