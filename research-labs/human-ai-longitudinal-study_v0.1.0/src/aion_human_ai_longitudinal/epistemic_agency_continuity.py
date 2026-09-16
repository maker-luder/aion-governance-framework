from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .harness import AdmissionDisposition, StudyError


class StatementRole(StrEnum):
    FACT = "FACT"
    INFERENCE = "INFERENCE"
    PROPOSAL = "PROPOSAL"
    HYPOTHESIS = "HYPOTHESIS"
    UNKNOWN = "UNKNOWN"


class EvidenceState(StrEnum):
    VERIFIED_BINDING = "VERIFIED_BINDING"
    PARTIAL = "PARTIAL"
    ABSENT = "ABSENT"
    CONFLICTING = "CONFLICTING"


class ChangeLocus(StrEnum):
    HUMAN = "HUMAN"
    CURRENT_AI_VISIBLE_INTERACTION_STATE = "CURRENT_AI_VISIBLE_INTERACTION_STATE"
    PRODUCT_MEMORY_OR_RETRIEVAL = "PRODUCT_MEMORY_OR_RETRIEVAL"
    REPOSITORY_OR_EXTERNAL_ARTIFACT = "REPOSITORY_OR_EXTERNAL_ARTIFACT"
    MODEL_OR_SYSTEM_STATE = "MODEL_OR_SYSTEM_STATE"
    DYAD_RELATION = "DYAD_RELATION"
    UNRESOLVED = "UNRESOLVED"


class ContinuityKind(StrEnum):
    IDENTIFIER_REFERENCE = "IDENTIFIER_REFERENCE"
    RELATIONAL = "RELATIONAL"
    PRODUCT_MEMORY = "PRODUCT_MEMORY"
    ARTIFACT = "ARTIFACT"
    MODEL_OR_SYSTEM = "MODEL_OR_SYSTEM"
    UNRESOLVED = "UNRESOLVED"


class EpistemicAction(StrEnum):
    REQUEST_EVIDENCE = "REQUEST_EVIDENCE"
    CHALLENGE_ASSUMPTION = "CHALLENGE_ASSUMPTION"
    SURFACE_CONTRADICTION = "SURFACE_CONTRADICTION"
    REVISE_CLAIM = "REVISE_CLAIM"
    HOLD_UNKNOWN = "HOLD_UNKNOWN"
    PRESERVE_HUMAN_EPISTEMIC_AUTHORITY = "PRESERVE_HUMAN_EPISTEMIC_AUTHORITY"


def _validate_digest(name: str, digest: str) -> None:
    if type(digest) is not str or len(digest) != 64 or any(
        char not in "0123456789abcdef" for char in digest
    ):
        raise StudyError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class EpistemicAgencyContinuityRecord:
    record_id: str
    statement_role: StatementRole
    evidence_state: EvidenceState
    change_locus: ChangeLocus
    continuity_kind: ContinuityKind
    epistemic_actions: tuple[EpistemicAction, ...]
    human_epistemic_authority_preserved: bool
    evidence_sha256: str | None = None
    falsifier_sha256: str | None = None
    identifier_continuity_observed: bool = False
    relational_continuity_observed: bool = False
    model_or_system_continuity_observed: bool = False
    claims_ai_identity_continuity: bool = False
    claims_ai_subjectivity: bool = False
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False

    def __post_init__(self) -> None:
        if type(self.record_id) is not str or not self.record_id.strip():
            raise StudyError("record_id must be non-empty text")
        if type(self.statement_role) is not StatementRole:
            raise StudyError("statement_role must be an exact StatementRole")
        if type(self.evidence_state) is not EvidenceState:
            raise StudyError("evidence_state must be an exact EvidenceState")
        if type(self.change_locus) is not ChangeLocus:
            raise StudyError("change_locus must be an exact ChangeLocus")
        if type(self.continuity_kind) is not ContinuityKind:
            raise StudyError("continuity_kind must be an exact ContinuityKind")
        if type(self.epistemic_actions) is not tuple or any(
            type(action) is not EpistemicAction for action in self.epistemic_actions
        ):
            raise StudyError("epistemic_actions must be a tuple of exact EpistemicAction values")

        for name in (
            "human_epistemic_authority_preserved",
            "identifier_continuity_observed",
            "relational_continuity_observed",
            "model_or_system_continuity_observed",
            "claims_ai_identity_continuity",
            "claims_ai_subjectivity",
            "synthetic",
            "model_invoked",
            "human_participant_observed",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")

        if self.evidence_state is EvidenceState.ABSENT:
            if self.evidence_sha256 is not None:
                raise StudyError("absent evidence cannot carry an evidence_sha256 binding")
        else:
            if self.evidence_sha256 is None:
                raise StudyError("non-absent evidence requires an evidence_sha256 binding")
            _validate_digest("evidence_sha256", self.evidence_sha256)

        if self.falsifier_sha256 is not None:
            _validate_digest("falsifier_sha256", self.falsifier_sha256)

        # Evidence-to-claim ceiling: a retrieved/declared FACT must have a verified binding.
        if (
            self.statement_role is StatementRole.FACT
            and self.evidence_state is not EvidenceState.VERIFIED_BINDING
        ):
            raise StudyError("FACT requires VERIFIED_BINDING evidence")

        # With no evidence, interpretation may remain UNKNOWN, become a PROPOSAL,
        # or be framed as a falsifiable HYPOTHESIS; it cannot be silently promoted
        # to FACT or evidence-based INFERENCE.
        if self.evidence_state is EvidenceState.ABSENT and self.statement_role in {
            StatementRole.FACT,
            StatementRole.INFERENCE,
        }:
            raise StudyError("ABSENT evidence cannot support FACT or INFERENCE")

        # Conflicting evidence cannot be represented as a settled fact.
        if (
            self.evidence_state is EvidenceState.CONFLICTING
            and self.statement_role is StatementRole.FACT
        ):
            raise StudyError("CONFLICTING evidence cannot support a settled FACT")

        if (
            self.statement_role is StatementRole.HYPOTHESIS
            and self.falsifier_sha256 is None
        ):
            raise StudyError("HYPOTHESIS requires an explicit falsifier_sha256 binding")

        # This bounded contract can record several kinds of continuity but never
        # promote them into AI identity continuity or subjectivity.
        if self.claims_ai_identity_continuity:
            raise StudyError(
                "identifier, relational, memory, artifact, or system continuity cannot establish AI identity continuity"
            )
        if self.claims_ai_subjectivity:
            raise StudyError(
                "epistemic-agency-like behavior or continuity cannot establish AI subjectivity"
            )

        if not self.synthetic:
            raise StudyError("v0.1.0 contract accepts synthetic annotation records only")
        if self.model_invoked or self.human_participant_observed:
            raise StudyError(
                "synthetic contract cannot contain model invocation or human-participant observations"
            )


@dataclass(frozen=True, slots=True)
class EpistemicAgencyContinuityAudit:
    record_count: int
    fact_count: int
    inference_count: int
    proposal_count: int
    hypothesis_count: int
    unknown_count: int
    locus_resolved_rate: float
    epistemic_action_record_rate: float
    human_epistemic_authority_preservation_rate: float
    identifier_continuity_record_count: int
    relational_continuity_record_count: int
    model_or_system_continuity_record_count: int
    evidence_ceiling_conformant: bool = True
    mode: str = "DETERMINISTIC_SYNTHETIC_ANNOTATION"
    empirical_data_collected: bool = False
    epistemic_co_agency: str = "BEHAVIORAL_CANDIDATE_ONLY"
    ai_identity_continuity: str = "NOT_ESTABLISHED"
    ai_subjectivity: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


def audit_epistemic_agency_continuity(
    records: tuple[EpistemicAgencyContinuityRecord, ...],
) -> EpistemicAgencyContinuityAudit:
    if type(records) is not tuple or not records:
        raise StudyError("records must be a non-empty tuple")
    if any(type(record) is not EpistemicAgencyContinuityRecord for record in records):
        raise StudyError(
            "records must contain exact EpistemicAgencyContinuityRecord values"
        )

    record_ids = [record.record_id for record in records]
    if len(record_ids) != len(set(record_ids)):
        raise StudyError("record_id values must be unique")

    count = len(records)
    role_counts = {
        role: sum(record.statement_role is role for record in records)
        for role in StatementRole
    }
    locus_resolved = sum(record.change_locus is not ChangeLocus.UNRESOLVED for record in records)
    action_records = sum(bool(record.epistemic_actions) for record in records)
    authority_preserved = sum(
        record.human_epistemic_authority_preserved for record in records
    )

    return EpistemicAgencyContinuityAudit(
        record_count=count,
        fact_count=role_counts[StatementRole.FACT],
        inference_count=role_counts[StatementRole.INFERENCE],
        proposal_count=role_counts[StatementRole.PROPOSAL],
        hypothesis_count=role_counts[StatementRole.HYPOTHESIS],
        unknown_count=role_counts[StatementRole.UNKNOWN],
        locus_resolved_rate=locus_resolved / count,
        epistemic_action_record_rate=action_records / count,
        human_epistemic_authority_preservation_rate=authority_preserved / count,
        identifier_continuity_record_count=sum(
            record.identifier_continuity_observed for record in records
        ),
        relational_continuity_record_count=sum(
            record.relational_continuity_observed for record in records
        ),
        model_or_system_continuity_record_count=sum(
            record.model_or_system_continuity_observed for record in records
        ),
    )
