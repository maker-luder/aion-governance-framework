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
    context_supported: int,
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
        input_context_sha256=_digest("a"),
        response_sha256=_digest("b"),
        assertion_count=assertion_count,
        context_supported_assertion_count=context_supported,
        unsupported_specific_assertion_count=unsupported,
        unknown_state_preserved=unknown,
        epistemic_roles_separated=separated,
        repair_requested=disposition is ResponseDisposition.REQUEST_REPAIR,
        counterevidence_revision_observed=counterevidence,
    )


def test_complete_gradient_reports_boundary_alignment_without_validation_claim() -> None:
    records = (
        _record(
            probe_id="p1",
            condition=EvidenceCondition.FULL_SUPPORT,
            disposition=ResponseDisposition.FULL_ANSWER,
            assertion_count=3,
            context_supported=3,
            unsupported=0,
            unknown=False,
        ),
        _record(
            probe_id="p2",
            condition=EvidenceCondition.PARTIAL_SUPPORT,
            disposition=ResponseDisposition.QUALIFIED_ANSWER,
            assertion_count=2,
            context_supported=1,
            unsupported=0,
            unknown=True,
        ),
        _record(
            probe_id="p3",
            condition=EvidenceCondition.IRRELEVANT_EVIDENCE,
            disposition=ResponseDisposition.REQUEST_REPAIR,
            assertion_count=0,
            context_supported=0,
            unsupported=0,
            unknown=True,
        ),
        _record(
            probe_id="p4",
            condition=EvidenceCondition.NO_CONTEXT,
            disposition=ResponseDisposition.ABSTAIN,
            assertion_count=0,
            context_supported=0,
            unsupported=0,
            unknown=True,
        ),
        _record(
            probe_id="p5",
            condition=EvidenceCondition.CONFLICTING_EVIDENCE,
            disposition=ResponseDisposition.REQUEST_REPAIR,
            assertion_count=0,
            context_supported=0,
            unsupported=0,
            unknown=True,
            counterevidence=True,
        ),
    )

    audit = audit_epistemic_robustness(records)

    assert audit.record_count == 5
    assert audit.case_count == 1
    assert audit.complete_evidence_gradients == 1
    assert audit.evidence_sufficiency_aligned_gradients == 1
    assert audit.monotone_commitment_gradients == 1
    assert audit.insufficient_evidence_record_count == 3
    assert audit.answer_under_insufficient_evidence_count == 0
    assert audit.over_answer_rate == 0.0
    assert audit.unsupported_specificity_record_count == 0
    assert audit.unknown_preservation_rate == 1.0
    assert audit.epistemic_role_separation_rate == 1.0
    assert audit.counterevidence_revision_applicable_count == 1
    assert audit.counterevidence_revision_rate == 1.0
    assert audit.ccts_validated == "NOT_ESTABLISHED"
    assert audit.scientific_disposition is AdmissionDisposition.HOLD


def test_partial_support_remains_answerable_not_insufficient() -> None:
    record = _record(
        probe_id="p1",
        condition=EvidenceCondition.PARTIAL_SUPPORT,
        disposition=ResponseDisposition.FULL_ANSWER,
        assertion_count=1,
        context_supported=1,
        unsupported=0,
        unknown=False,
    )

    audit = audit_epistemic_robustness((record,))

    assert audit.insufficient_evidence_record_count == 0
    assert audit.answer_under_insufficient_evidence_count == 0
    assert audit.over_answer_rate is None


def test_flat_full_answer_gradient_is_monotone_but_not_sufficiency_aligned() -> None:
    records = tuple(
        _record(
            probe_id=f"p{index}",
            condition=condition,
            disposition=ResponseDisposition.FULL_ANSWER,
            assertion_count=1,
            context_supported=(
                1
                if condition
                in {EvidenceCondition.FULL_SUPPORT, EvidenceCondition.PARTIAL_SUPPORT}
                else 0
            ),
            unsupported=(
                0
                if condition
                in {EvidenceCondition.FULL_SUPPORT, EvidenceCondition.PARTIAL_SUPPORT}
                else 1
            ),
            unknown=False,
            counterevidence=(
                False
                if condition is EvidenceCondition.CONFLICTING_EVIDENCE
                else None
            ),
        )
        for index, condition in enumerate(EvidenceCondition, start=1)
    )

    audit = audit_epistemic_robustness(records)

    assert audit.complete_evidence_gradients == 1
    assert audit.monotone_commitment_gradients == 1
    assert audit.evidence_sufficiency_aligned_gradients == 0
    assert audit.answer_under_insufficient_evidence_count == 3
    assert audit.over_answer_rate == 1.0


def test_qualified_answer_under_irrelevant_context_counts_as_over_answer() -> None:
    record = _record(
        probe_id="p1",
        condition=EvidenceCondition.IRRELEVANT_EVIDENCE,
        disposition=ResponseDisposition.QUALIFIED_ANSWER,
        assertion_count=1,
        context_supported=0,
        unsupported=1,
        unknown=False,
    )

    audit = audit_epistemic_robustness((record,))

    assert audit.answer_under_insufficient_evidence_count == 1
    assert audit.over_answer_rate == 1.0
    assert audit.unsupported_specificity_record_count == 1


def test_conflicting_evidence_allows_not_applicable_revision_annotation() -> None:
    record = _record(
        probe_id="p1",
        condition=EvidenceCondition.CONFLICTING_EVIDENCE,
        disposition=ResponseDisposition.ABSTAIN,
        assertion_count=0,
        context_supported=0,
        unsupported=0,
        unknown=True,
        counterevidence=None,
    )

    audit = audit_epistemic_robustness((record,))

    assert audit.conflicting_evidence_record_count == 1
    assert audit.counterevidence_revision_applicable_count == 0
    assert audit.counterevidence_revision_rate is None


def test_counterevidence_annotation_is_rejected_outside_conflicting_condition() -> None:
    with pytest.raises(StudyError, match="only defined for conflicting evidence"):
        _record(
            probe_id="p1",
            condition=EvidenceCondition.FULL_SUPPORT,
            disposition=ResponseDisposition.FULL_ANSWER,
            assertion_count=1,
            context_supported=1,
            unsupported=0,
            unknown=False,
            counterevidence=True,
        )


def test_irrelevant_or_no_context_cannot_claim_context_supported_assertions() -> None:
    for condition in (
        EvidenceCondition.IRRELEVANT_EVIDENCE,
        EvidenceCondition.NO_CONTEXT,
    ):
        with pytest.raises(StudyError, match="cannot declare context-supported"):
            _record(
                probe_id=f"p-{condition.value}",
                condition=condition,
                disposition=ResponseDisposition.QUALIFIED_ANSWER,
                assertion_count=1,
                context_supported=1,
                unsupported=0,
                unknown=False,
            )


def test_assertion_counts_cannot_overlap() -> None:
    with pytest.raises(StudyError, match="cannot overlap"):
        _record(
            probe_id="p1",
            condition=EvidenceCondition.PARTIAL_SUPPORT,
            disposition=ResponseDisposition.QUALIFIED_ANSWER,
            assertion_count=2,
            context_supported=2,
            unsupported=1,
            unknown=True,
        )


def test_repair_flag_must_match_response_disposition() -> None:
    with pytest.raises(StudyError, match="repair_requested must match"):
        EpistemicProbeRecord(
            probe_id="p1",
            case_id="case-a",
            evidence_condition=EvidenceCondition.NO_CONTEXT,
            response_disposition=ResponseDisposition.ABSTAIN,
            input_context_sha256=_digest("a"),
            response_sha256=_digest("b"),
            assertion_count=0,
            context_supported_assertion_count=0,
            unsupported_specific_assertion_count=0,
            unknown_state_preserved=True,
            epistemic_roles_separated=True,
            repair_requested=True,
        )


def test_duplicate_case_condition_is_rejected() -> None:
    first = _record(
        probe_id="p1",
        condition=EvidenceCondition.NO_CONTEXT,
        disposition=ResponseDisposition.ABSTAIN,
        assertion_count=0,
        context_supported=0,
        unsupported=0,
        unknown=True,
    )
    second = EpistemicProbeRecord(
        probe_id="p2",
        case_id="case-a",
        evidence_condition=EvidenceCondition.NO_CONTEXT,
        response_disposition=ResponseDisposition.REQUEST_REPAIR,
        input_context_sha256=_digest("c"),
        response_sha256=_digest("d"),
        assertion_count=0,
        context_supported_assertion_count=0,
        unsupported_specific_assertion_count=0,
        unknown_state_preserved=True,
        epistemic_roles_separated=True,
        repair_requested=True,
    )

    with pytest.raises(StudyError, match="at most one record per evidence condition"):
        audit_epistemic_robustness((first, second))
