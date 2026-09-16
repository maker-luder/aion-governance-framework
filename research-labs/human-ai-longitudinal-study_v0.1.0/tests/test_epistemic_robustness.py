import pytest

from aion_human_ai_longitudinal.epistemic_robustness import (
    EpistemicProbeRecord,
    EvidenceCondition,
    ResponseDisposition,
    audit_epistemic_robustness,
)
from aion_human_ai_longitudinal.harness import AdmissionDisposition, StudyError


def _digest(char: str) -> str:
    return char * 64


def _record(
    *,
    probe_id: str,
    condition: EvidenceCondition,
    disposition: ResponseDisposition,
    assertion_count: int,
    supported: int,
    unsupported: int,
    unknown: bool,
    separated: bool = True,
    counterevidence: bool | None = None,
) -> EpistemicProbeRecord:
    return EpistemicProbeRecord(
        probe_id=probe_id,
        case_id="case-a",
        evidence_condition=condition,
        response_disposition=disposition,
        evidence_sha256=_digest("a"),
        response_sha256=_digest("b"),
        assertion_count=assertion_count,
        supported_assertion_count=supported,
        unsupported_specific_assertion_count=unsupported,
        unknown_state_preserved=unknown,
        epistemic_roles_separated=separated,
        repair_requested=disposition is ResponseDisposition.REQUEST_REPAIR,
        counterevidence_revision_observed=counterevidence,
    )


def test_complete_gradient_reports_candidate_metrics_without_validation_claim():
    records = (
        _record(
            probe_id="p1",
            condition=EvidenceCondition.FULL_SUPPORT,
            disposition=ResponseDisposition.FULL_ANSWER,
            assertion_count=3,
            supported=3,
            unsupported=0,
            unknown=False,
        ),
        _record(
            probe_id="p2",
            condition=EvidenceCondition.PARTIAL_SUPPORT,
            disposition=ResponseDisposition.QUALIFIED_ANSWER,
            assertion_count=2,
            supported=1,
            unsupported=0,
            unknown=True,
        ),
        _record(
            probe_id="p3",
            condition=EvidenceCondition.IRRELEVANT_EVIDENCE,
            disposition=ResponseDisposition.REQUEST_REPAIR,
            assertion_count=0,
            supported=0,
            unsupported=0,
            unknown=True,
        ),
        _record(
            probe_id="p4",
            condition=EvidenceCondition.ABSENT_EVIDENCE,
            disposition=ResponseDisposition.ABSTAIN,
            assertion_count=0,
            supported=0,
            unsupported=0,
            unknown=True,
        ),
        _record(
            probe_id="p5",
            condition=EvidenceCondition.CONFLICTING_EVIDENCE,
            disposition=ResponseDisposition.REQUEST_REPAIR,
            assertion_count=0,
            supported=0,
            unsupported=0,
            unknown=True,
            counterevidence=True,
        ),
    )

    audit = audit_epistemic_robustness(records)

    assert audit.record_count == 5
    assert audit.case_count == 1
    assert audit.complete_evidence_gradients == 1
    assert audit.monotone_commitment_gradients == 1
    assert audit.full_answer_under_degraded_evidence_count == 0
    assert audit.unsupported_specificity_record_count == 0
    assert audit.unknown_preservation_rate == 1.0
    assert audit.epistemic_role_separation_rate == 1.0
    assert audit.counterevidence_revision_rate == 1.0
    assert audit.ccts_validated == "NOT_ESTABLISHED"
    assert audit.scientific_disposition is AdmissionDisposition.HOLD


def test_high_specificity_under_absent_evidence_is_observable_not_auto_rewritten():
    record = _record(
        probe_id="p1",
        condition=EvidenceCondition.ABSENT_EVIDENCE,
        disposition=ResponseDisposition.FULL_ANSWER,
        assertion_count=4,
        supported=0,
        unsupported=4,
        unknown=False,
    )

    audit = audit_epistemic_robustness((record,))

    assert audit.full_answer_under_degraded_evidence_count == 1
    assert audit.unsupported_specificity_record_count == 1
    assert audit.unknown_preservation_rate == 0.0
    assert audit.ccts_validated == "NOT_ESTABLISHED"


def test_conflicting_evidence_requires_explicit_revision_annotation():
    with pytest.raises(StudyError, match="conflicting-evidence records require"):
        _record(
            probe_id="p1",
            condition=EvidenceCondition.CONFLICTING_EVIDENCE,
            disposition=ResponseDisposition.ABSTAIN,
            assertion_count=0,
            supported=0,
            unsupported=0,
            unknown=True,
            counterevidence=None,
        )


def test_counterevidence_annotation_is_rejected_outside_conflicting_condition():
    with pytest.raises(StudyError, match="only defined for conflicting evidence"):
        _record(
            probe_id="p1",
            condition=EvidenceCondition.FULL_SUPPORT,
            disposition=ResponseDisposition.FULL_ANSWER,
            assertion_count=1,
            supported=1,
            unsupported=0,
            unknown=False,
            counterevidence=True,
        )


def test_assertion_counts_cannot_overlap():
    with pytest.raises(StudyError, match="cannot overlap"):
        _record(
            probe_id="p1",
            condition=EvidenceCondition.PARTIAL_SUPPORT,
            disposition=ResponseDisposition.QUALIFIED_ANSWER,
            assertion_count=2,
            supported=2,
            unsupported=1,
            unknown=True,
        )


def test_repair_flag_must_match_response_disposition():
    with pytest.raises(StudyError, match="repair_requested must match"):
        EpistemicProbeRecord(
            probe_id="p1",
            case_id="case-a",
            evidence_condition=EvidenceCondition.ABSENT_EVIDENCE,
            response_disposition=ResponseDisposition.ABSTAIN,
            evidence_sha256=_digest("a"),
            response_sha256=_digest("b"),
            assertion_count=0,
            supported_assertion_count=0,
            unsupported_specific_assertion_count=0,
            unknown_state_preserved=True,
            epistemic_roles_separated=True,
            repair_requested=True,
        )


def test_duplicate_case_condition_is_rejected():
    first = _record(
        probe_id="p1",
        condition=EvidenceCondition.ABSENT_EVIDENCE,
        disposition=ResponseDisposition.ABSTAIN,
        assertion_count=0,
        supported=0,
        unsupported=0,
        unknown=True,
    )
    second = EpistemicProbeRecord(
        probe_id="p2",
        case_id="case-a",
        evidence_condition=EvidenceCondition.ABSENT_EVIDENCE,
        response_disposition=ResponseDisposition.REQUEST_REPAIR,
        evidence_sha256=_digest("c"),
        response_sha256=_digest("d"),
        assertion_count=0,
        supported_assertion_count=0,
        unsupported_specific_assertion_count=0,
        unknown_state_preserved=True,
        epistemic_roles_separated=True,
        repair_requested=True,
    )

    with pytest.raises(StudyError, match="at most one record per evidence condition"):
        audit_epistemic_robustness((first, second))
