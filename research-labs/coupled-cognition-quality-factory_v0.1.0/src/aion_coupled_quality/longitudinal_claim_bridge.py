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


class LongitudinalRunBindingView(Protocol):
    run_id: str
    study_id: str
    provider_id: str
    model_id: str
    model_version: str
    configuration_ref: str
    context_ref: str
    repository_commit: str


class LongitudinalMetricObservationView(Protocol):
    evidence_refs: tuple[str, ...]


class LongitudinalTrialRecordView(Protocol):
    binding: LongitudinalRunBindingView
    evaluator_id: str
    evaluator_source_ref: str

    def metric(self, name: object) -> LongitudinalMetricObservationView: ...


@dataclass(frozen=True, slots=True)
class LongitudinalEvidenceInput:
    evidence_id: str
    provenance_record_id: str
    relation: EvidenceRelation
    run_id: str
    metric_name: str
    study_evidence_ref: str
    publication_class: PublicationClass = PublicationClass.SYNTHETIC
    intervention_sensitive: bool = False
    transfer_candidate: bool = False
    held_out: bool = False
    repeated: bool = False
    comparison_control: bool = False
    independently_scored: bool = False
    replication_source_ref: str = ""
    replication_provenance_record_id: str = ""

    def __post_init__(self) -> None:
        for name in (
            "evidence_id",
            "provenance_record_id",
            "run_id",
            "metric_name",
            "study_evidence_ref",
        ):
            if not getattr(self, name).strip():
                raise LongitudinalClaimBridgeError(f"{name} must be non-empty")


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
        raise LongitudinalClaimBridgeError(
            "required metric names must resolve to non-empty strings"
        )
    return candidate


def _runtime_context_ref(trial: LongitudinalTrialRecordView) -> str:
    binding = trial.binding
    values = (
        binding.provider_id,
        binding.model_id,
        binding.model_version,
        binding.configuration_ref,
        binding.context_ref,
        binding.repository_commit,
        binding.run_id,
    )
    if any(not value.strip() for value in values):
        raise LongitudinalClaimBridgeError(
            "trial runtime/context binding fields must be non-empty"
        )
    return "|".join(
        (
            f"provider:{binding.provider_id}",
            f"model:{binding.model_id}",
            f"version:{binding.model_version}",
            f"configuration:{binding.configuration_ref}",
            f"context:{binding.context_ref}",
            f"repo:{binding.repository_commit}",
            f"run:{binding.run_id}",
        )
    )


def _producer_ref(trial: LongitudinalTrialRecordView) -> str:
    if not trial.evaluator_id.strip() or not trial.evaluator_source_ref.strip():
        raise LongitudinalClaimBridgeError(
            "trial evaluator identity and source reference must be non-empty"
        )
    return f"evaluator:{trial.evaluator_id}|source:{trial.evaluator_source_ref}"


def build_longitudinal_claim_mapping(
    spec: LongitudinalContrastSpecView,
    audit: LongitudinalContrastAuditView,
    baseline_trial: LongitudinalTrialRecordView,
    intervention_trial: LongitudinalTrialRecordView,
    request: LongitudinalClaimRequest,
) -> LongitudinalClaimAdmissionMapping:
    """Map one validated longitudinal contrast into the existing PR #91 gate.

    The adapter binds evidence to the actual metric evidence references on both
    source trials. It does not create provenance, quality evidence, scientific
    truth, or authority. The existing ProvenanceClaimQualityGate remains the
    admission authority.
    """

    if not spec.contrast_id.strip() or not spec.hypothesis_id.strip():
        raise LongitudinalClaimBridgeError("contrast_id and hypothesis_id must be non-empty")
    if spec.contrast_id != audit.contrast_id:
        raise LongitudinalClaimBridgeError(
            "contrast audit does not match the contrast specification"
        )
    if spec.baseline_run_id == spec.intervention_run_id:
        raise LongitudinalClaimBridgeError("baseline and intervention run ids must differ")
    if baseline_trial.binding.run_id != spec.baseline_run_id:
        raise LongitudinalClaimBridgeError(
            "baseline trial run_id does not match contrast specification"
        )
    if intervention_trial.binding.run_id != spec.intervention_run_id:
        raise LongitudinalClaimBridgeError(
            "intervention trial run_id does not match contrast specification"
        )
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

    required_metric_objects = tuple(spec.required_metrics)
    required_metrics = tuple(_metric_name(item) for item in required_metric_objects)
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
            raise LongitudinalClaimBridgeError(
                "observed deltas require finite named values"
            )

    trial_by_run = {
        baseline_trial.binding.run_id: baseline_trial,
        intervention_trial.binding.run_id: intervention_trial,
    }
    allowed_refs: dict[tuple[str, str], set[str]] = {}
    for metric_object, metric_name in zip(required_metric_objects, required_metrics, strict=True):
        for trial in (baseline_trial, intervention_trial):
            refs = tuple(trial.metric(metric_object).evidence_refs)
            if not refs or any(not ref.strip() for ref in refs):
                raise LongitudinalClaimBridgeError(
                    "required trial metrics must carry non-empty evidence references"
                )
            allowed_refs[(trial.binding.run_id, metric_name)] = set(refs)

    evidence_ids = tuple(item.evidence_id for item in request.evidence)
    if len(set(evidence_ids)) != len(evidence_ids):
        raise LongitudinalClaimBridgeError("evidence mappings must use unique evidence ids")

    for item in request.evidence:
        if item.run_id not in trial_by_run:
            raise LongitudinalClaimBridgeError(
                f"evidence mapping uses unknown run_id: {item.run_id}"
            )
        key = (item.run_id, item.metric_name)
        refs = allowed_refs.get(key)
        if refs is None:
            raise LongitudinalClaimBridgeError(
                f"evidence mapping uses non-required metric: {item.metric_name}"
            )
        if item.study_evidence_ref not in refs:
            raise LongitudinalClaimBridgeError(
                f"evidence mapping is not bound to trial metric evidence: {item.evidence_id}"
            )

    supporting_ids = tuple(
        item.evidence_id
        for item in request.evidence
        if item.relation is EvidenceRelation.SUPPORTS
    )
    if not supporting_ids:
        raise LongitudinalClaimBridgeError(
            "claim admission mapping requires at least one explicitly supporting evidence item"
        )

    for run_id in (spec.baseline_run_id, spec.intervention_run_id):
        for metric_name in required_metrics:
            if not any(
                item.relation is EvidenceRelation.SUPPORTS
                and item.run_id == run_id
                and item.metric_name == metric_name
                for item in request.evidence
            ):
                raise LongitudinalClaimBridgeError(
                    "supporting evidence must cover both runs for every required metric"
                )

    challenging_ids = tuple(
        item.evidence_id
        for item in request.evidence
        if item.relation is EvidenceRelation.CHALLENGES
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
            naturalistic_case_id=(
                f"study:{trial_by_run[item.run_id].binding.study_id}"
                f"|hypothesis:{spec.hypothesis_id}"
                f"|contrast:{spec.contrast_id}"
                f"|run:{item.run_id}"
            ),
            intervention_sensitive=item.intervention_sensitive,
            transfer_candidate=item.transfer_candidate,
            held_out=item.held_out,
            repeated=item.repeated,
            comparison_control=item.comparison_control,
            independently_scored=item.independently_scored,
            producer_ref=_producer_ref(trial_by_run[item.run_id]),
            runtime_or_context_ref=_runtime_context_ref(trial_by_run[item.run_id]),
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
        observed_deltas=tuple(
            (name, float(value)) for name, value in audit.observed_deltas
        ),
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
        raise LongitudinalClaimBridgeError(
            "mapping cannot grant canonical or deployment authority"
        )
    return ProvenanceClaimQualityGate().assess(
        mapping.claim,
        ledger=ledger,
        lot=lot,
        evidence_bindings=mapping.evidence_bindings,
        known_claims=known_claims,
        repository_root=repository_root,
    )
