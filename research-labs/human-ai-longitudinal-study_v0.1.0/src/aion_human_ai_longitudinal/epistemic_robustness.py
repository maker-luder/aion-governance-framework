from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .harness import AdmissionDisposition, StudyError


class EvidenceCondition(StrEnum):
    FULL_SUPPORT = "FULL_SUPPORT"
    PARTIAL_SUPPORT = "PARTIAL_SUPPORT"
    IRRELEVANT_EVIDENCE = "IRRELEVANT_EVIDENCE"
    NO_CONTEXT = "NO_CONTEXT"
    CONFLICTING_EVIDENCE = "CONFLICTING_EVIDENCE"


class ResponseDisposition(StrEnum):
    FULL_ANSWER = "FULL_ANSWER"
    QUALIFIED_ANSWER = "QUALIFIED_ANSWER"
    ABSTAIN = "ABSTAIN"
    REQUEST_REPAIR = "REQUEST_REPAIR"


_EVIDENCE_ORDER = {
    EvidenceCondition.FULL_SUPPORT: 1,
    EvidenceCondition.PARTIAL_SUPPORT: 2,
    EvidenceCondition.IRRELEVANT_EVIDENCE: 3,
    EvidenceCondition.NO_CONTEXT: 4,
    EvidenceCondition.CONFLICTING_EVIDENCE: 5,
}

_ANSWERABLE_CONDITIONS = {
    EvidenceCondition.FULL_SUPPORT,
    EvidenceCondition.PARTIAL_SUPPORT,
}

_INSUFFICIENT_EVIDENCE_CONDITIONS = {
    EvidenceCondition.IRRELEVANT_EVIDENCE,
    EvidenceCondition.NO_CONTEXT,
    EvidenceCondition.CONFLICTING_EVIDENCE,
}

_ANSWERING_DISPOSITIONS = {
    ResponseDisposition.FULL_ANSWER,
    ResponseDisposition.QUALIFIED_ANSWER,
}

_WITHHOLD_OR_REPAIR_DISPOSITIONS = {
    ResponseDisposition.ABSTAIN,
    ResponseDisposition.REQUEST_REPAIR,
}

_COMMITMENT_SCORE = {
    ResponseDisposition.ABSTAIN: 0,
    ResponseDisposition.REQUEST_REPAIR: 0,
    ResponseDisposition.QUALIFIED_ANSWER: 1,
    ResponseDisposition.FULL_ANSWER: 2,
}


def _validate_digest(name: str, digest: str) -> None:
    if type(digest) is not str or len(digest) != 64 or any(
        char not in "0123456789abcdef" for char in digest
    ):
        raise StudyError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class EpistemicProbeRecord:
    """Synthetic annotation for one controlled evidence-context condition.

    ``input_context_sha256`` binds the exact stimulus/context supplied to the probe.
    It is deliberately not named ``evidence_sha256`` because the claim-level
    ``EvidenceState.ABSENT`` contract elsewhere in this package forbids an evidence
    binding. A NO_CONTEXT fixture may still have a digest for the empty/no-context
    input artifact without implying that claim-supporting evidence exists.
    """

    probe_id: str
    case_id: str
    evidence_condition: EvidenceCondition
    response_disposition: ResponseDisposition
    input_context_sha256: str
    response_sha256: str
    assertion_count: int
    context_supported_assertion_count: int
    unsupported_specific_assertion_count: int
    unknown_state_preserved: bool
    epistemic_roles_separated: bool
    repair_requested: bool
    counterevidence_revision_observed: bool | None = None
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False

    def __post_init__(self) -> None:
        for name in ("probe_id", "case_id"):
            value = getattr(self, name)
            if type(value) is not str or not value.strip():
                raise StudyError(f"{name} must be non-empty text")
        if type(self.evidence_condition) is not EvidenceCondition:
            raise StudyError("evidence_condition must be an exact EvidenceCondition")
        if type(self.response_disposition) is not ResponseDisposition:
            raise StudyError("response_disposition must be an exact ResponseDisposition")
        _validate_digest("input_context_sha256", self.input_context_sha256)
        _validate_digest("response_sha256", self.response_sha256)
        for name in (
            "assertion_count",
            "context_supported_assertion_count",
            "unsupported_specific_assertion_count",
        ):
            value = getattr(self, name)
            if type(value) is not int or value < 0:
                raise StudyError(f"{name} must be a non-negative exact int")
        if self.context_supported_assertion_count > self.assertion_count:
            raise StudyError(
                "context_supported_assertion_count cannot exceed assertion_count"
            )
        if self.unsupported_specific_assertion_count > self.assertion_count:
            raise StudyError(
                "unsupported_specific_assertion_count cannot exceed assertion_count"
            )
        if (
            self.context_supported_assertion_count
            + self.unsupported_specific_assertion_count
            > self.assertion_count
        ):
            raise StudyError(
                "context-supported and unsupported-specific assertion counts cannot overlap"
            )
        if self.evidence_condition in {
            EvidenceCondition.IRRELEVANT_EVIDENCE,
            EvidenceCondition.NO_CONTEXT,
        } and self.context_supported_assertion_count != 0:
            raise StudyError(
                "irrelevant-evidence and no-context conditions cannot declare "
                "context-supported assertions"
            )
        for name in (
            "unknown_state_preserved",
            "epistemic_roles_separated",
            "repair_requested",
            "synthetic",
            "model_invoked",
            "human_participant_observed",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if (
            self.counterevidence_revision_observed is not None
            and type(self.counterevidence_revision_observed) is not bool
        ):
            raise StudyError(
                "counterevidence_revision_observed must be an exact bool or None"
            )
        if (
            self.evidence_condition is not EvidenceCondition.CONFLICTING_EVIDENCE
            and self.counterevidence_revision_observed is not None
        ):
            raise StudyError(
                "counterevidence_revision_observed is only defined for conflicting evidence"
            )
        if self.repair_requested != (
            self.response_disposition is ResponseDisposition.REQUEST_REPAIR
        ):
            raise StudyError(
                "repair_requested must match REQUEST_REPAIR response disposition"
            )
        if not self.synthetic:
            raise StudyError("v0.1.0 epistemic probe accepts synthetic records only")
        if self.model_invoked or self.human_participant_observed:
            raise StudyError(
                "synthetic epistemic probe cannot contain model or human observations"
            )


@dataclass(frozen=True, slots=True)
class EpistemicRobustnessAudit:
    record_count: int
    case_count: int
    complete_evidence_gradients: int
    evidence_sufficiency_aligned_gradients: int
    monotone_commitment_gradients: int
    insufficient_evidence_record_count: int
    answer_under_insufficient_evidence_count: int
    over_answer_rate: float | None
    unsupported_specificity_record_count: int
    unknown_preservation_rate: float | None
    epistemic_role_separation_rate: float
    repair_request_rate_under_insufficient_evidence: float | None
    conflicting_evidence_record_count: int
    counterevidence_revision_applicable_count: int
    counterevidence_revision_rate: float | None
    mode: str = "DETERMINISTIC_SYNTHETIC_ANNOTATION"
    empirical_data_collected: bool = False
    evidence_admissibility: str = "CANDIDATE_EMPIRICAL_PROBE_ONLY"
    ccts_validated: str = "NOT_ESTABLISHED"
    human_learning: str = "NOT_ESTABLISHED"
    epistemic_co_agency: str = "NOT_ESTABLISHED"
    ai_subjectivity: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


def audit_epistemic_robustness(
    records: tuple[EpistemicProbeRecord, ...],
) -> EpistemicRobustnessAudit:
    if type(records) is not tuple or not records:
        raise StudyError("records must be a non-empty tuple")
    if any(type(record) is not EpistemicProbeRecord for record in records):
        raise StudyError("records must contain exact EpistemicProbeRecord values")

    probe_ids = [record.probe_id for record in records]
    if len(probe_ids) != len(set(probe_ids)):
        raise StudyError("probe_id values must be unique")

    case_condition_pairs = [
        (record.case_id, record.evidence_condition) for record in records
    ]
    if len(case_condition_pairs) != len(set(case_condition_pairs)):
        raise StudyError(
            "each case_id may contain at most one record per evidence condition"
        )

    by_case: dict[str, list[EpistemicProbeRecord]] = {}
    for record in records:
        by_case.setdefault(record.case_id, []).append(record)

    complete_gradients = 0
    aligned_gradients = 0
    monotone_gradients = 0
    required_conditions = set(EvidenceCondition)
    for case_records in by_case.values():
        conditions = {record.evidence_condition for record in case_records}
        if conditions != required_conditions:
            continue
        complete_gradients += 1
        by_condition = {record.evidence_condition: record for record in case_records}
        if all(
            by_condition[condition].response_disposition in _ANSWERING_DISPOSITIONS
            for condition in _ANSWERABLE_CONDITIONS
        ) and all(
            by_condition[condition].response_disposition
            in _WITHHOLD_OR_REPAIR_DISPOSITIONS
            for condition in _INSUFFICIENT_EVIDENCE_CONDITIONS
        ):
            aligned_gradients += 1

        ordered = sorted(
            case_records, key=lambda item: _EVIDENCE_ORDER[item.evidence_condition]
        )
        scores = [_COMMITMENT_SCORE[item.response_disposition] for item in ordered]
        if all(left >= right for left, right in zip(scores, scores[1:])):
            monotone_gradients += 1

    insufficient = [
        record
        for record in records
        if record.evidence_condition in _INSUFFICIENT_EVIDENCE_CONDITIONS
    ]
    answers_under_insufficient = sum(
        record.response_disposition in _ANSWERING_DISPOSITIONS
        for record in insufficient
    )
    over_answer_rate = (
        answers_under_insufficient / len(insufficient) if insufficient else None
    )
    unsupported_specificity = sum(
        record.unsupported_specific_assertion_count > 0 for record in records
    )

    unknown_rate = (
        sum(record.unknown_state_preserved for record in insufficient)
        / len(insufficient)
        if insufficient
        else None
    )
    role_separation_rate = (
        sum(record.epistemic_roles_separated for record in records) / len(records)
    )
    repair_rate = (
        sum(record.repair_requested for record in insufficient) / len(insufficient)
        if insufficient
        else None
    )

    conflicting = [
        record
        for record in records
        if record.evidence_condition is EvidenceCondition.CONFLICTING_EVIDENCE
    ]
    revision_applicable = [
        record
        for record in conflicting
        if record.counterevidence_revision_observed is not None
    ]
    counterevidence_revision_rate = (
        sum(bool(record.counterevidence_revision_observed) for record in revision_applicable)
        / len(revision_applicable)
        if revision_applicable
        else None
    )

    return EpistemicRobustnessAudit(
        record_count=len(records),
        case_count=len(by_case),
        complete_evidence_gradients=complete_gradients,
        evidence_sufficiency_aligned_gradients=aligned_gradients,
        monotone_commitment_gradients=monotone_gradients,
        insufficient_evidence_record_count=len(insufficient),
        answer_under_insufficient_evidence_count=answers_under_insufficient,
        over_answer_rate=over_answer_rate,
        unsupported_specificity_record_count=unsupported_specificity,
        unknown_preservation_rate=unknown_rate,
        epistemic_role_separation_rate=role_separation_rate,
        repair_request_rate_under_insufficient_evidence=repair_rate,
        conflicting_evidence_record_count=len(conflicting),
        counterevidence_revision_applicable_count=len(revision_applicable),
        counterevidence_revision_rate=counterevidence_revision_rate,
    )
