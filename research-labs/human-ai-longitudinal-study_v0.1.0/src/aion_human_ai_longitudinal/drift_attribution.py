from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .harness import AdmissionDisposition, StudyError
from .transition_continuity import TransitionChangeLocus


def _require_text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise StudyError(f"{name} must be non-empty text")


def _require_unique_refs(name: str, value: tuple[str, ...]) -> None:
    if type(value) is not tuple or not value or any(
        type(ref) is not str or not ref.strip() for ref in value
    ):
        raise StudyError(f"{name} must be a non-empty tuple of references")
    if len(set(value)) != len(value):
        raise StudyError(f"{name} must be unique")


class DriftKind(StrEnum):
    CONTEXT_OMISSION = "CONTEXT_OMISSION"
    CONTEXT_OVERREACH = "CONTEXT_OVERREACH"
    FOCUS_OMISSION = "FOCUS_OMISSION"
    FOCUS_OVERREACH = "FOCUS_OVERREACH"
    LOCAL_SUBGOAL_TAKEOVER = "LOCAL_SUBGOAL_TAKEOVER"
    NEXT_STEP_DRIFT = "NEXT_STEP_DRIFT"
    AUTHORITY_DRIFT = "AUTHORITY_DRIFT"
    PROVENANCE_DRIFT = "PROVENANCE_DRIFT"
    UNCERTAINTY_UPGRADE = "UNCERTAINTY_UPGRADE"
    INTERPRETIVE_DRIFT = "INTERPRETIVE_DRIFT"
    RELATIONAL_ROLE_DRIFT = "RELATIONAL_ROLE_DRIFT"


@dataclass(frozen=True, slots=True)
class DriftAttributionRecord:
    drift_id: str
    source_checkpoint_id: str
    target_checkpoint_id: str
    kind: DriftKind
    candidate_loci: tuple[TransitionChangeLocus, ...]
    evidence_refs: tuple[str, ...]
    direct_intervention_evidence: bool = False
    provider_disclosure_evidence: bool = False
    reproducible_binding_evidence: bool = False
    claims_causal_identification: bool = False
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False

    def __post_init__(self) -> None:
        for name in ("drift_id", "source_checkpoint_id", "target_checkpoint_id"):
            _require_text(name, getattr(self, name))
        if self.source_checkpoint_id == self.target_checkpoint_id:
            raise StudyError("drift attribution requires distinct checkpoints")
        if type(self.kind) is not DriftKind:
            raise StudyError("kind must be an exact DriftKind")
        if type(self.candidate_loci) is not tuple or not self.candidate_loci:
            raise StudyError("candidate_loci must be a non-empty tuple")
        if any(type(item) is not TransitionChangeLocus for item in self.candidate_loci):
            raise StudyError(
                "candidate_loci must contain exact TransitionChangeLocus values"
            )
        if len(set(self.candidate_loci)) != len(self.candidate_loci):
            raise StudyError("candidate_loci must be unique")
        if TransitionChangeLocus.UNKNOWN in self.candidate_loci and len(self.candidate_loci) != 1:
            raise StudyError("UNKNOWN locus must be the sole candidate locus")
        _require_unique_refs("evidence_refs", self.evidence_refs)
        for name in (
            "direct_intervention_evidence",
            "provider_disclosure_evidence",
            "reproducible_binding_evidence",
            "claims_causal_identification",
            "synthetic",
            "model_invoked",
            "human_participant_observed",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if self.claims_causal_identification:
            raise StudyError(
                "v0.1.0 structural attribution records cannot claim causal identification"
            )
        if not self.synthetic or self.model_invoked or self.human_participant_observed:
            raise StudyError(
                "v0.1.0 drift-attribution records are synthetic and no-model only"
            )


@dataclass(frozen=True, slots=True)
class DriftAttributionAudit:
    record_count: int
    unknown_locus_record_ids: tuple[str, ...]
    single_candidate_locus_record_ids: tuple[str, ...]
    multi_candidate_locus_record_ids: tuple[str, ...]
    intervention_evidence_record_ids: tuple[str, ...]
    provider_disclosure_record_ids: tuple[str, ...]
    reproducible_binding_record_ids: tuple[str, ...]
    mode: str = "DETERMINISTIC_SYNTHETIC_DRIFT_ATTRIBUTION"
    empirical_data_collected: bool = False
    causal_identification: str = "NOT_ESTABLISHED"
    upstream_cause: str = "NOT_ESTABLISHED"
    model_capability_ordering: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


def audit_drift_attribution(
    records: tuple[DriftAttributionRecord, ...],
) -> DriftAttributionAudit:
    if type(records) is not tuple or not records:
        raise StudyError("records must be a non-empty tuple")
    if any(type(item) is not DriftAttributionRecord for item in records):
        raise StudyError("records must contain exact DriftAttributionRecord values")
    drift_ids = [item.drift_id for item in records]
    if len(drift_ids) != len(set(drift_ids)):
        raise StudyError("drift_id values must be unique")

    unknown = tuple(
        item.drift_id
        for item in records
        if item.candidate_loci == (TransitionChangeLocus.UNKNOWN,)
    )
    single = tuple(
        item.drift_id
        for item in records
        if len(item.candidate_loci) == 1
        and item.candidate_loci != (TransitionChangeLocus.UNKNOWN,)
    )
    multi = tuple(item.drift_id for item in records if len(item.candidate_loci) > 1)
    intervention = tuple(
        item.drift_id for item in records if item.direct_intervention_evidence
    )
    disclosure = tuple(
        item.drift_id for item in records if item.provider_disclosure_evidence
    )
    reproducible = tuple(
        item.drift_id for item in records if item.reproducible_binding_evidence
    )
    return DriftAttributionAudit(
        record_count=len(records),
        unknown_locus_record_ids=unknown,
        single_candidate_locus_record_ids=single,
        multi_candidate_locus_record_ids=multi,
        intervention_evidence_record_ids=intervention,
        provider_disclosure_record_ids=disclosure,
        reproducible_binding_record_ids=reproducible,
    )
