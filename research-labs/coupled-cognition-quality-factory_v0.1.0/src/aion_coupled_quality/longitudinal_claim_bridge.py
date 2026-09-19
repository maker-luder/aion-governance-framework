from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import Protocol

from .claim_quality import (
    ClaimLevel,
    ClaimQualityAssessment,
    ClaimStatus,
    EvidenceBinding,
    EvidenceRelation,
    ProvenanceClaimQualityGate,
    PublicationClass,
    ResearchClaimRecord,
)
from .models import EvidenceKind, ResearchLot
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
    value: float | int
    unit: str
    evidence_refs: tuple[str, ...]
    held_out: bool


class LongitudinalTrialRecordView(Protocol):
    binding: LongitudinalRunBindingView
    evaluator_id: str
    evaluator_source_ref: str

    def metric(self, name: object) -> LongitudinalMetricObservationView: ...


@dataclass(frozen=True, slots=True)
class LongitudinalEvidenceInput:
    evidence_id: str
    provenance_record_id: str
    run_id: str
    metric_name: str
    study_evidence_ref: str

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
    provenance_record_id: str
    evidence: tuple[LongitudinalEvidenceInput, ...]

    def __post_init__(self) -> None:
        if not self.claim_id.strip():
            raise LongitudinalClaimBridgeError("claim_id must be non-empty")
        if not self.provenance_record_id.strip():
            raise LongitudinalClaimBridgeError("provenance_record_id must be non-empty")
        if self.version < 1:
            raise LongitudinalClaimBridgeError("claim version must be positive")
        if not self.evidence:
            raise LongitudinalClaimBridgeError("at least one evidence mapping is required")


@dataclass(frozen=True, slots=True)
class LongitudinalClaimAdmissionMapping:
    hypothesis_id: str
    contrast_id: str
    baseline_run_id: str
    intervention_run_id: str
    manipulated_fields: tuple[str, ...]
    required_metrics: tuple[str, ...]
    observed_deltas: tuple[tuple[str, float], ...]
    metric_units: tuple[tuple[str, str], ...]
    quality_evidence_refs: tuple[tuple[str, str], ...]
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


def _content_addressed_ref(kind: str, payload: dict[str, str]) -> str:
    if not kind.strip() or any(not key.strip() or not value.strip() for key, value in payload.items()):
        raise LongitudinalClaimBridgeError(
            "content-addressed reference requires non-empty kind, keys, and values"
        )
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return f"{kind}-sha256:{hashlib.sha256(canonical).hexdigest()}"


def _runtime_context_ref(trial: LongitudinalTrialRecordView) -> str:
    binding = trial.binding
    return _content_addressed_ref(
        "longitudinal-runtime",
        {
            "configuration_ref": binding.configuration_ref,
            "context_ref": binding.context_ref,
            "model_id": binding.model_id,
            "model_version": binding.model_version,
            "provider_id": binding.provider_id,
            "repository_commit": binding.repository_commit,
            "run_id": binding.run_id,
        },
    )


def _producer_ref(trial: LongitudinalTrialRecordView) -> str:
    return _content_addressed_ref(
        "longitudinal-producer",
        {
            "evaluator_id": trial.evaluator_id,
            "evaluator_source_ref": trial.evaluator_source_ref,
        },
    )


def _naturalistic_case_ref(
    trial: LongitudinalTrialRecordView,
    spec: LongitudinalContrastSpecView,
) -> str:
    return _content_addressed_ref(
        "longitudinal-case",
        {
            "contrast_id": spec.contrast_id,
            "hypothesis_id": spec.hypothesis_id,
            "run_id": trial.binding.run_id,
            "study_id": trial.binding.study_id,
        },
    )


def _bounded_observation_statement(
    spec: LongitudinalContrastSpecView,
    observed_deltas: tuple[tuple[str, float], ...],
    metric_units: tuple[tuple[str, str], ...],
) -> str:
    units = dict(metric_units)
    rendered = ", ".join(
        f"{name}={value:.12g} {units[name]}" for name, value in observed_deltas
    )
    return (
        f"Synthetic longitudinal contrast {spec.contrast_id} associated with "
        f"{spec.hypothesis_id} recorded bounded metric deltas: {rendered}. "
        "This observation does not establish the hypothesis, a mechanism, "
        "causal learning, subjectivity, or consciousness."
    )


def _recompute_and_validate_deltas(
    spec: LongitudinalContrastSpecView,
    audit: LongitudinalContrastAuditView,
    baseline_trial: LongitudinalTrialRecordView,
    intervention_trial: LongitudinalTrialRecordView,
) -> tuple[tuple[tuple[str, float], ...], tuple[tuple[str, str], ...]]:
    required_metric_objects = tuple(spec.required_metrics)
    required_metrics = tuple(_metric_name(item) for item in required_metric_objects)
    if not required_metrics or len(set(required_metrics)) != len(required_metrics):
        raise LongitudinalClaimBridgeError("required_metrics must be non-empty and unique")

    audit_delta_by_name = dict(audit.observed_deltas)
    if len(audit_delta_by_name) != len(audit.observed_deltas):
        raise LongitudinalClaimBridgeError("observed delta metric names must be unique")
    if set(audit_delta_by_name) != set(required_metrics):
        raise LongitudinalClaimBridgeError(
            "observed delta metrics must exactly match the preregistered required metrics"
        )

    recomputed: list[tuple[str, float]] = []
    units: list[tuple[str, str]] = []
    for metric_object, metric_name in zip(
        required_metric_objects, required_metrics, strict=True
    ):
        left = baseline_trial.metric(metric_object)
        right = intervention_trial.metric(metric_object)
        if not left.unit.strip() or not right.unit.strip():
            raise LongitudinalClaimBridgeError("required metric units must be non-empty")
        if left.unit != right.unit:
            raise LongitudinalClaimBridgeError(f"metric unit drift: {metric_name}")
        if left.held_out != right.held_out:
            raise LongitudinalClaimBridgeError(f"held_out status drift: {metric_name}")
        left_value = float(left.value)
        right_value = float(right.value)
        if not math.isfinite(left_value) or not math.isfinite(right_value):
            raise LongitudinalClaimBridgeError(
                f"required metric values must be finite: {metric_name}"
            )
        delta = right_value - left_value
        audit_delta = float(audit_delta_by_name[metric_name])
        if not math.isfinite(audit_delta):
            raise LongitudinalClaimBridgeError(
                f"audit delta must be finite: {metric_name}"
            )
        if delta != audit_delta:
            raise LongitudinalClaimBridgeError(
                f"audit delta does not match source trial values: {metric_name}"
            )
        recomputed.append((metric_name, delta))
        units.append((metric_name, left.unit))
    return tuple(recomputed), tuple(units)


def build_longitudinal_claim_mapping(
    spec: LongitudinalContrastSpecView,
    audit: LongitudinalContrastAuditView,
    baseline_trial: LongitudinalTrialRecordView,
    intervention_trial: LongitudinalTrialRecordView,
    request: LongitudinalClaimRequest,
) -> LongitudinalClaimAdmissionMapping:
    """Map one validated longitudinal contrast into the existing PR #91 gate.

    Version 0.1 is intentionally narrow. It emits only synthetic L0 observation
    records with a bridge-generated bounded statement. The bridge rebinds the
    audit delta to source trial metric values and source evidence references.
    Stronger intervention, replication, population, causal-learning, publication,
    challenge-resolution, or phenomenology semantics require separate typed
    verification and are outside this adapter.
    """

    if not spec.contrast_id.strip() or not spec.hypothesis_id.strip():
        raise LongitudinalClaimBridgeError(
            "contrast_id and hypothesis_id must be non-empty"
        )
    if spec.contrast_id != audit.contrast_id:
        raise LongitudinalClaimBridgeError(
            "contrast audit does not match the contrast specification"
        )
    if spec.baseline_run_id == spec.intervention_run_id:
        raise LongitudinalClaimBridgeError(
            "baseline and intervention run ids must differ"
        )
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
    if not spec.manipulated_fields or any(
        not item.strip() for item in spec.manipulated_fields
    ):
        raise LongitudinalClaimBridgeError("manipulated_fields must be non-empty")
    if len(set(spec.manipulated_fields)) != len(spec.manipulated_fields):
        raise LongitudinalClaimBridgeError("manipulated_fields must be unique")
    if not spec.falsifier.strip():
        raise LongitudinalClaimBridgeError("contrast falsifier must be non-empty")
    if not spec.alternative_explanations or any(
        not item.strip() for item in spec.alternative_explanations
    ):
        raise LongitudinalClaimBridgeError(
            "alternative_explanations must be non-empty"
        )

    observed_deltas, metric_units = _recompute_and_validate_deltas(
        spec,
        audit,
        baseline_trial,
        intervention_trial,
    )
    required_metrics = tuple(name for name, _ in observed_deltas)

    trial_by_run = {
        baseline_trial.binding.run_id: baseline_trial,
        intervention_trial.binding.run_id: intervention_trial,
    }
    allowed_refs: dict[tuple[str, str], set[str]] = {}
    for metric_object, metric_name in zip(
        tuple(spec.required_metrics), required_metrics, strict=True
    ):
        for trial in (baseline_trial, intervention_trial):
            refs = tuple(trial.metric(metric_object).evidence_refs)
            if not refs or any(not ref.strip() for ref in refs):
                raise LongitudinalClaimBridgeError(
                    "required trial metrics must carry non-empty evidence references"
                )
            allowed_refs[(trial.binding.run_id, metric_name)] = set(refs)

    evidence_ids = tuple(item.evidence_id for item in request.evidence)
    if len(set(evidence_ids)) != len(evidence_ids):
        raise LongitudinalClaimBridgeError(
            "evidence mappings must use unique evidence ids"
        )
    source_bindings = tuple(
        (item.run_id, item.metric_name, item.study_evidence_ref)
        for item in request.evidence
    )
    if len(set(source_bindings)) != len(source_bindings):
        raise LongitudinalClaimBridgeError(
            "trial metric evidence mapping cannot be duplicated under multiple evidence ids"
        )

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

    for run_id in (spec.baseline_run_id, spec.intervention_run_id):
        for metric_name in required_metrics:
            if not any(
                item.run_id == run_id and item.metric_name == metric_name
                for item in request.evidence
            ):
                raise LongitudinalClaimBridgeError(
                    "supporting evidence must cover both runs for every required metric"
                )

    bindings = tuple(
        EvidenceBinding(
            evidence_id=item.evidence_id,
            provenance_record_id=item.provenance_record_id,
            relation=EvidenceRelation.SUPPORTS,
            publication_class=PublicationClass.SYNTHETIC,
            naturalistic_case_id=_naturalistic_case_ref(
                trial_by_run[item.run_id],
                spec,
            ),
            intervention_sensitive=False,
            transfer_candidate=False,
            held_out=False,
            repeated=False,
            comparison_control=False,
            independently_scored=False,
            producer_ref=_producer_ref(trial_by_run[item.run_id]),
            runtime_or_context_ref=_runtime_context_ref(trial_by_run[item.run_id]),
            replication_source_ref="",
            replication_provenance_record_id="",
        )
        for item in request.evidence
    )

    evidence_ids = tuple(item.evidence_id for item in request.evidence)
    quality_evidence_refs = tuple(
        (item.evidence_id, item.study_evidence_ref) for item in request.evidence
    )
    claim = ResearchClaimRecord(
        claim_id=request.claim_id,
        version=request.version,
        statement=_bounded_observation_statement(
            spec,
            observed_deltas,
            metric_units,
        ),
        provenance_record_id=request.provenance_record_id,
        claim_level=ClaimLevel.L0_OBSERVATION,
        status=ClaimStatus.OBSERVED,
        observed_evidence_ids=evidence_ids,
        inferred_statements=(),
        competing_explanations=spec.alternative_explanations,
        falsifier=spec.falsifier,
        supporting_evidence_ids=evidence_ids,
        publication_class=PublicationClass.SYNTHETIC,
        challenging_evidence_ids=(),
        resolved_challenge_ids=(),
        challenge_resolutions=(),
        dependencies=(),
        revision=None,
        population_scope=False,
        causal_learning_effect=False,
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
        observed_deltas=observed_deltas,
        metric_units=metric_units,
        quality_evidence_refs=quality_evidence_refs,
        claim=claim,
        evidence_bindings=bindings,
    )


def _validate_quality_lot_evidence(
    mapping: LongitudinalClaimAdmissionMapping,
    lot: ResearchLot,
) -> None:
    by_id = {item.evidence_id: item for item in lot.evidence}
    if len(by_id) != len(lot.evidence):
        raise LongitudinalClaimBridgeError(
            "quality lot contains duplicate evidence ids"
        )
    for evidence_id, expected_ref in mapping.quality_evidence_refs:
        item = by_id.get(evidence_id)
        if item is None:
            raise LongitudinalClaimBridgeError(
                f"quality lot is missing mapped evidence: {evidence_id}"
            )
        if item.reference != expected_ref:
            raise LongitudinalClaimBridgeError(
                f"quality lot evidence reference mismatch: {evidence_id}"
            )
        if item.kind is not EvidenceKind.TEST_RESULT:
            raise LongitudinalClaimBridgeError(
                f"quality lot mapped evidence must be TEST_RESULT: {evidence_id}"
            )
        if not item.supports_claim:
            raise LongitudinalClaimBridgeError(
                f"quality lot mapped evidence must support the bounded observation: {evidence_id}"
            )


def assess_longitudinal_claim_mapping(
    mapping: LongitudinalClaimAdmissionMapping,
    *,
    ledger: EpistemicProvenanceLedger,
    lot: ResearchLot,
    repository_root: Path,
    known_claims: tuple[ResearchClaimRecord, ...] = (),
) -> ClaimQualityAssessment:
    """Submit a mapped L0 observation to the existing provenance quality gate."""

    if mapping.canonical_effect != "NONE" or mapping.deployment:
        raise LongitudinalClaimBridgeError(
            "mapping cannot grant canonical or deployment authority"
        )
    _validate_quality_lot_evidence(mapping, lot)
    return ProvenanceClaimQualityGate().assess(
        mapping.claim,
        ledger=ledger,
        lot=lot,
        evidence_bindings=mapping.evidence_bindings,
        known_claims=known_claims,
        repository_root=repository_root,
    )
