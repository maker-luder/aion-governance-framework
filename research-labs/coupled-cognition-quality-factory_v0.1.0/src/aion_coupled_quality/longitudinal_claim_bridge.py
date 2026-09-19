from __future__ import annotations

from dataclasses import dataclass, field
import math
from pathlib import Path
from typing import Protocol

from .claim_quality import (
    ChallengeResolution,
    ClaimDependency,
    ClaimLevel,
    ClaimQualityAssessment,
    ClaimRevision,
    ClaimStatus,
    EvidenceBinding,
    EvidenceRelation,
    ProvenanceClaimQualityGate,
    PublicationClass,
    ResearchClaimRecord,
)
from .models import ResearchLot
from .provenance import EpistemicProvenanceLedger


class LongitudinalClaimBridgeError(ValueError):
    pass


class LongitudinalContrastSpecView(Protocol):
    contrast_id: str
    hypothesis_id: str
    baseline_run_id: str
    intervention_run_id: str
    manipulated_fields: tuple[str, ...]
    required_metrics: tuple[object, ...]
    falsifier: str
    alternative_explanations: tuple[str, ...]


class LongitudinalContrastAuditView(Protocol):
    contrast_id: str
    structurally_admissible: bool
    observed_deltas: tuple[tuple[str, float], ...]
    reasons: tuple[str, ...]
    canonical_effect: str
    deployment: bool


@dataclass(frozen=True, slots=True)
class LongitudinalEvidenceInput:
    evidence_id: str
    provenance_record_id: str
    relation: EvidenceRelation
    publication_class: PublicationClass = PublicationClass.SYNTHETIC
    naturalistic_case_id: str = ""
    intervention_sensitive: bool = False
    transfer_candidate: bool = False
    held_out: bool = False
    repeated: bool = False
    comparison_control: bool = False
    independently_scored: bool = False
    producer_ref: str = ""
    runtime_or_context_ref: str = ""
    replication_source_ref: str = ""
    replication_provenance_record_id: str = ""

    def __post_init__(self) -> None:
        if not self.evidence_id.strip() or not self.provenance_record_id.strip():
            raise LongitudinalClaimBridgeError(
                "evidence_id and provenance_record_id must be non-empty"
            )
        if self.relation is EvidenceRelation.SUPPORTS:
            if not self.producer_ref.strip() or not self.runtime_or_context_ref.strip():
                raise LongitudinalClaimBridgeError(
                    "supporting longitudinal evidence requires producer_ref and runtime_or_context_ref"
                )


@dataclass(frozen=True, slots=True)
class LongitudinalClaimRequest:
    claim_id: str
    version: int
    statement: str
    provenance_record_id: str
    claim_level: ClaimLevel
    evidence: tuple[LongitudinalEvidenceInput, ...]
    inferred_statements: tuple[str, ...] = field(default_factory=tuple)
    publication_class: PublicationClass = PublicationClass.SYNTHETIC
    resolved_challenge_ids: tuple[str, ...] = field(default_factory=tuple)
    challenge_resolutions: tuple[ChallengeResolution, ...] = field(default_factory=tuple)
    dependencies: tuple[ClaimDependency, ...] = field(default_factory=tuple)
    revision: ClaimRevision | None = None
    population_scope: bool = False
    causal_learning_effect: bool = False

    def __post_init__(self) -> None:
        if not self.claim_id.strip() or not self.statement.strip():
            raise LongitudinalClaimBridgeError("claim_id and statement must be non-empty")
        if not self.provenance_record_id.strip():
            raise LongitudinalClaimBridgeError("provenance_record_id must be non-empty")
        if self.version < 1:
            raise LongitudinalClaimBridgeError("claim version must be positive")
        if not self.evidence:
            raise LongitudinalClaimBridgeError("at least one evidence mapping is required")
        if any(not item.strip() for item in self.inferred_statements):
            raise LongitudinalClaimBridgeError("inferred_statements cannot contain empty values")


@dataclass(frozen=True, slots=True)
class LongitudinalClaimAdmissionMapping:
    hypothesis_id: str
    contrast_id: str
    baseline_run_id: str
    intervention_run_id: str
    manipulated_fields: tuple[str, ...]
    required_metrics: tuple[str, ...]
    observed_deltas: tuple[tuple[str, float], ...]
    claim: ResearchClaimRecord
    evidence_bindings: tuple[EvidenceBinding, ...]
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False


def _metric_name(value: object) -> str:
    candidate = getattr(value, "value", value)
    if not isinstance(candidate, str) or not candidate.strip():
        raise LongitudinalClaimBridgeError("required metric names must resolve to non-empty strings")
    return candidate


def build_longitudinal_claim_mapping(
    spec: LongitudinalContrastSpecView,
    audit: LongitudinalContrastAuditView,
    request: LongitudinalClaimRequest,
) -> LongitudinalClaimAdmissionMapping:
    """Map one structurally admissible longitudinal contrast into the existing PR #91 gate.

    The function does not create provenance, quality evidence, scientific truth, or
    authority. Callers must supply those independently and the existing
    ProvenanceClaimQualityGate remains the admission authority.
    """

    if not spec.contrast_id.strip() or not spec.hypothesis_id.strip():
        raise LongitudinalClaimBridgeError("contrast_id and hypothesis_id must be non-empty")
    if spec.contrast_id != audit.contrast_id:
        raise LongitudinalClaimBridgeError("contrast audit does not match the contrast specification")
    if spec.baseline_run_id == spec.intervention_run_id:
        raise LongitudinalClaimBridgeError("baseline and intervention run ids must differ")
    if not audit.structurally_admissible:
        raise LongitudinalClaimBridgeError(
            "structurally inadmissible contrast cannot enter claim admission mapping"
        )
    if audit.canonical_effect != "NONE" or audit.deployment:
        raise LongitudinalClaimBridgeError(
            "longitudinal contrast cannot carry canonical or deployment authority"
        )
    if not spec.manipulated_fields or any(not item.strip() for item in spec.manipulated_fields):
        raise LongitudinalClaimBridgeError("manipulated_fields must be non-empty")
    if len(set(spec.manipulated_fields)) != len(spec.manipulated_fields):
        raise LongitudinalClaimBridgeError("manipulated_fields must be unique")
    if not spec.falsifier.strip():
        raise LongitudinalClaimBridgeError("contrast falsifier must be non-empty")
    if not spec.alternative_explanations or any(
        not item.strip() for item in spec.alternative_explanations
    ):
        raise LongitudinalClaimBridgeError("alternative_explanations must be non-empty")

    required_metrics = tuple(_metric_name(item) for item in spec.required_metrics)
    if not required_metrics or len(set(required_metrics)) != len(required_metrics):
        raise LongitudinalClaimBridgeError("required_metrics must be non-empty and unique")

    observed_metric_names = tuple(name for name, _ in audit.observed_deltas)
    if len(set(observed_metric_names)) != len(observed_metric_names):
        raise LongitudinalClaimBridgeError("observed delta metric names must be unique")
    if set(observed_metric_names) != set(required_metrics):
        raise LongitudinalClaimBridgeError(
            "observed delta metrics must exactly match the preregistered required metrics"
        )
    for name, value in audit.observed_deltas:
        if not name.strip() or not math.isfinite(float(value)):
            raise LongitudinalClaimBridgeError("observed deltas require finite named values")

    evidence_ids = tuple(item.evidence_id for item in request.evidence)
    if len(set(evidence_ids)) != len(evidence_ids):
        raise LongitudinalClaimBridgeError("evidence mappings must use unique evidence ids")

    supporting_ids = tuple(
        item.evidence_id for item in request.evidence if item.relation is EvidenceRelation.SUPPORTS
    )
    if not supporting_ids:
        raise LongitudinalClaimBridgeError(
            "claim admission mapping requires at least one explicitly supporting evidence item"
        )
    challenging_ids = tuple(
        item.evidence_id for item in request.evidence if item.relation is EvidenceRelation.CHALLENGES
    )
    observed_ids = tuple(
        item.evidence_id
        for item in request.evidence
        if item.relation
        in {
            EvidenceRelation.OBSERVES,
            EvidenceRelation.SUPPORTS,
            EvidenceRelation.NEUTRAL,
            EvidenceRelation.UNRESOLVED,
        }
    )
    if not observed_ids:
        raise LongitudinalClaimBridgeError(
            "claim admission mapping requires at least one observed/non-challenge evidence item"
        )

    bindings = tuple(
        EvidenceBinding(
            evidence_id=item.evidence_id,
            provenance_record_id=item.provenance_record_id,
            relation=item.relation,
            publication_class=item.publication_class,
            naturalistic_case_id=item.naturalistic_case_id,
            intervention_sensitive=item.intervention_sensitive,
            transfer_candidate=item.transfer_candidate,
            held_out=item.held_out,
            repeated=item.repeated,
            comparison_control=item.comparison_control,
            independently_scored=item.independently_scored,
            producer_ref=item.producer_ref,
            runtime_or_context_ref=item.runtime_or_context_ref,
            replication_source_ref=item.replication_source_ref,
            replication_provenance_record_id=item.replication_provenance_record_id,
        )
        for item in request.evidence
    )

    claim = ResearchClaimRecord(
        claim_id=request.claim_id,
        version=request.version,
        statement=request.statement,
        provenance_record_id=request.provenance_record_id,
        claim_level=request.claim_level,
        status=ClaimStatus.OBSERVED,
        observed_evidence_ids=observed_ids,
        inferred_statements=request.inferred_statements,
        competing_explanations=spec.alternative_explanations,
        falsifier=spec.falsifier,
        supporting_evidence_ids=supporting_ids,
        publication_class=request.publication_class,
        challenging_evidence_ids=challenging_ids,
        resolved_challenge_ids=request.resolved_challenge_ids,
        challenge_resolutions=request.challenge_resolutions,
        dependencies=request.dependencies,
        revision=request.revision,
        population_scope=request.population_scope,
        causal_learning_effect=request.causal_learning_effect,
        subjectivity_claim=False,
        consciousness_claim=False,
        phenomenal_experience_claim=False,
        moral_agency_claim=False,
        moral_status_claim=False,
        canonical_effect="NONE",
    )

    return LongitudinalClaimAdmissionMapping(
        hypothesis_id=spec.hypothesis_id,
        contrast_id=spec.contrast_id,
        baseline_run_id=spec.baseline_run_id,
        intervention_run_id=spec.intervention_run_id,
        manipulated_fields=tuple(spec.manipulated_fields),
        required_metrics=required_metrics,
        observed_deltas=tuple((name, float(value)) for name, value in audit.observed_deltas),
        claim=claim,
        evidence_bindings=bindings,
    )


def assess_longitudinal_claim_mapping(
    mapping: LongitudinalClaimAdmissionMapping,
    *,
    ledger: EpistemicProvenanceLedger,
    lot: ResearchLot,
    repository_root: Path,
    known_claims: tuple[ResearchClaimRecord, ...] = (),
) -> ClaimQualityAssessment:
    """Submit a mapped longitudinal claim to the existing provenance quality gate."""

    if mapping.canonical_effect != "NONE" or mapping.deployment:
        raise LongitudinalClaimBridgeError("mapping cannot grant canonical or deployment authority")
    return ProvenanceClaimQualityGate().assess(
        mapping.claim,
        ledger=ledger,
        lot=lot,
        evidence_bindings=mapping.evidence_bindings,
        known_claims=known_claims,
        repository_root=repository_root,
    )
