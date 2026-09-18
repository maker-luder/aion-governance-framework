from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field
from enum import StrEnum

from aion_ai_tevv import TEVVProfileDisposition, TEVVProfileReceipt

from .ai_risk_impact import AIRiskImpactDisposition, AIRiskImpactReceipt
from .end_to_end import (
    EndToEndDisposition,
    EndToEndQualityAssessment,
    EndToEndQualitySystemEngine,
    ExistingChainDisposition,
    ExistingQualityChainBinding,
    FieldQualitySignal,
    ManagementReviewRecord,
    MeasurementAssuranceRecord,
    QualityAuditRecord,
    ResearchQualityPlan,
)
from .models import QualityError, Severity


RECEIPT_SCHEMA_VERSION = "0.1.0"


def _text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise QualityError(f"{name} must be non-empty text")


def _text_tuple(name: str, values: tuple[str, ...], *, allow_empty: bool = False) -> None:
    if type(values) is not tuple:
        raise QualityError(f"{name} must be a tuple")
    if not allow_empty and not values:
        raise QualityError(f"{name} must not be empty")
    if any(type(value) is not str or not value.strip() for value in values):
        raise QualityError(f"{name} must contain non-empty text")
    if len(values) != len(set(values)):
        raise QualityError(f"{name} must be unique")


def _hex(name: str, value: str, length: int) -> None:
    if type(value) is not str or len(value) != length or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise QualityError(f"{name} must be lowercase {length}-hex")


def _digest(payload: object) -> str:
    return hashlib.sha256(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()


class DataRole(StrEnum):
    SOURCE = "SOURCE"
    EXPERIMENT_INPUT = "EXPERIMENT_INPUT"
    FIXTURE = "FIXTURE"
    EVALUATION_LABELS = "EVALUATION_LABELS"
    RUNTIME_RECORD = "RUNTIME_RECORD"
    COUNTEREVIDENCE = "COUNTEREVIDENCE"


class DataQualityDisposition(StrEnum):
    FIT_FOR_DECLARED_USE = "FIT_FOR_DECLARED_USE"
    REQUALIFICATION_REQUIRED = "REQUALIFICATION_REQUIRED"
    HOLD = "HOLD"


class SupplierQualityDisposition(StrEnum):
    CONDITIONAL = "CONDITIONAL"
    ENHANCED_REVIEW = "ENHANCED_REVIEW"
    SCOPE_RESTRICTED = "SCOPE_RESTRICTED"
    QUARANTINED = "QUARANTINED"
    DENIED = "DENIED"


class ClaimImpactDisposition(StrEnum):
    RESOLVED = "RESOLVED"
    HOLD = "HOLD"
    REQUALIFICATION_REQUIRED = "REQUALIFICATION_REQUIRED"
    REVISION_REQUIRED = "REVISION_REQUIRED"
    WITHDRAWAL_REQUIRED = "WITHDRAWAL_REQUIRED"


class SamplingRiskClass(StrEnum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH_CRITICAL = "HIGH_CRITICAL"


class SamplingDisposition(StrEnum):
    BOUNDED_CONFIDENCE_ONLY = "BOUNDED_CONFIDENCE_ONLY"
    HOLD = "HOLD"
    FULL_INSPECTION_REQUIRED = "FULL_INSPECTION_REQUIRED"


class ProcessStabilityDisposition(StrEnum):
    BOUNDED_STABLE_SIGNAL = "BOUNDED_STABLE_SIGNAL"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


@dataclass(frozen=True, slots=True)
class QualityChainReceiptBinding:
    chain_id: str
    candidate_id: str
    candidate_fingerprint: str
    disposition: ExistingChainDisposition
    exact_source_state_ref: str
    exact_runtime_ref: str
    producer_git_head: str
    producer_tree_sha: str
    checkpoint_set_sha256: str
    capa_set_sha256: str
    assessment_sha256: str
    producer_contract_ref: str
    producer_contract_sha256: str
    receipt_sha256: str
    schema_version: str = RECEIPT_SCHEMA_VERSION
    release_authority: str = "NONE"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        for name in (
            "chain_id",
            "candidate_id",
            "candidate_fingerprint",
            "exact_source_state_ref",
            "exact_runtime_ref",
            "producer_contract_ref",
        ):
            _text(name, getattr(self, name))
        if type(self.disposition) is not ExistingChainDisposition:
            raise QualityError("disposition must be an exact ExistingChainDisposition")
        if self.schema_version != RECEIPT_SCHEMA_VERSION:
            raise QualityError("unsupported quality-chain receipt schema version")
        _hex("candidate_fingerprint", self.candidate_fingerprint, 64)
        _hex("producer_git_head", self.producer_git_head, 40)
        _hex("producer_tree_sha", self.producer_tree_sha, 40)
        for name in (
            "checkpoint_set_sha256",
            "capa_set_sha256",
            "assessment_sha256",
            "producer_contract_sha256",
            "receipt_sha256",
        ):
            _hex(name, getattr(self, name), 64)
        if self.release_authority != "NONE":
            raise QualityError("quality-chain receipt cannot grant release authority")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise QualityError("quality-chain receipt cannot establish subjectivity")
        if self.phenomenal_experience_conclusion != "NOT_ESTABLISHED":
            raise QualityError("quality-chain receipt cannot establish phenomenal experience")
        if self.scientific_disposition != "HOLD":
            raise QualityError("quality-chain receipt cannot establish scientific validity")
        if self.canonical_effect != "NONE" or self.deployment:
            raise QualityError("quality-chain receipt cannot create canonical or deployment effect")
        if self.receipt_sha256 != _digest(self.payload_without_digest()):
            raise QualityError("quality-chain receipt content digest mismatch")

    def payload_without_digest(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "chain_id": self.chain_id,
            "candidate_id": self.candidate_id,
            "candidate_fingerprint": self.candidate_fingerprint,
            "disposition": self.disposition.value,
            "exact_source_state_ref": self.exact_source_state_ref,
            "exact_runtime_ref": self.exact_runtime_ref,
            "producer_git_head": self.producer_git_head,
            "producer_tree_sha": self.producer_tree_sha,
            "checkpoint_set_sha256": self.checkpoint_set_sha256,
            "capa_set_sha256": self.capa_set_sha256,
            "assessment_sha256": self.assessment_sha256,
            "producer_contract_ref": self.producer_contract_ref,
            "producer_contract_sha256": self.producer_contract_sha256,
            "release_authority": self.release_authority,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "phenomenal_experience_conclusion": self.phenomenal_experience_conclusion,
            "scientific_disposition": self.scientific_disposition,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
        }

    def to_existing_binding(self) -> ExistingQualityChainBinding:
        return ExistingQualityChainBinding(
            chain_id=self.chain_id,
            four_domain_candidate_fingerprint=self.candidate_fingerprint,
            disposition=self.disposition,
        )


@dataclass(frozen=True, slots=True)
class DataQualityRecord:
    data_id: str
    role: DataRole
    provenance_ref: str
    exact_source_state_ref: str
    selection_rule: str
    completeness_ref: str
    consistency_ref: str
    duplicate_check_ref: str
    representativeness_scope: str
    privacy_status: str
    license_status: str
    known_limitations: tuple[str, ...]
    contamination_risk: Severity
    leakage_risk: Severity
    synthetic: bool
    empirical_population: bool
    fitness_for_declared_use: bool
    disposition: DataQualityDisposition
    label_provenance_ref: str = "NOT_APPLICABLE"

    def __post_init__(self) -> None:
        for name in (
            "data_id",
            "provenance_ref",
            "exact_source_state_ref",
            "selection_rule",
            "completeness_ref",
            "consistency_ref",
            "duplicate_check_ref",
            "representativeness_scope",
            "privacy_status",
            "license_status",
            "label_provenance_ref",
        ):
            _text(name, getattr(self, name))
        _text_tuple("known_limitations", self.known_limitations, allow_empty=True)
        if type(self.role) is not DataRole:
            raise QualityError("role must be an exact DataRole")
        if type(self.contamination_risk) is not Severity or type(self.leakage_risk) is not Severity:
            raise QualityError("data risks must use exact Severity values")
        for name in ("synthetic", "empirical_population", "fitness_for_declared_use"):
            if type(getattr(self, name)) is not bool:
                raise QualityError(f"{name} must be an exact bool")
        if type(self.disposition) is not DataQualityDisposition:
            raise QualityError("disposition must be an exact DataQualityDisposition")
        if self.synthetic and self.empirical_population:
            raise QualityError("synthetic data cannot be declared an empirical population")
        if self.role is DataRole.EVALUATION_LABELS and self.label_provenance_ref == "NOT_APPLICABLE":
            raise QualityError("evaluation labels require label provenance")
        severe_risk = self.contamination_risk in {Severity.HIGH, Severity.CRITICAL} or self.leakage_risk in {
            Severity.HIGH,
            Severity.CRITICAL,
        }
        if severe_risk and self.disposition is DataQualityDisposition.FIT_FOR_DECLARED_USE:
            raise QualityError("high/critical contamination or leakage cannot be fit for declared use")
        if self.fitness_for_declared_use != (
            self.disposition is DataQualityDisposition.FIT_FOR_DECLARED_USE
        ):
            raise QualityError("fitness flag must agree with data-quality disposition")


@dataclass(frozen=True, slots=True)
class UpstreamQualityRecord:
    supplier_object_id: str
    scope: str
    version_ref: str
    provenance_refs: tuple[str, ...]
    assessment_refs: tuple[str, ...]
    dependency_role: str
    criticality: Severity
    replaceability: str
    exposure: str
    methodological_confounds: tuple[str, ...]
    disposition: SupplierQualityDisposition
    requalification_triggers: tuple[str, ...]
    approved_scope_refs: tuple[str, ...] = field(default_factory=tuple)
    restricted_scope_refs: tuple[str, ...] = field(default_factory=tuple)
    incident_refs: tuple[str, ...] = field(default_factory=tuple)
    local_ncr_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in (
            "supplier_object_id",
            "scope",
            "version_ref",
            "dependency_role",
            "replaceability",
            "exposure",
        ):
            _text(name, getattr(self, name))
        for name in (
            "provenance_refs",
            "assessment_refs",
            "methodological_confounds",
            "requalification_triggers",
            "approved_scope_refs",
            "restricted_scope_refs",
            "incident_refs",
            "local_ncr_refs",
        ):
            _text_tuple(
                name,
                getattr(self, name),
                allow_empty=name not in {"provenance_refs", "assessment_refs", "requalification_triggers"},
            )
        if type(self.criticality) is not Severity:
            raise QualityError("criticality must be an exact Severity")
        if type(self.disposition) is not SupplierQualityDisposition:
            raise QualityError("disposition must be an exact SupplierQualityDisposition")
        if self.disposition is SupplierQualityDisposition.CONDITIONAL and not self.approved_scope_refs:
            raise QualityError("conditional supplier state must identify approved scope refs")
        if self.disposition in {SupplierQualityDisposition.QUARANTINED, SupplierQualityDisposition.DENIED} and not (
            self.incident_refs or self.assessment_refs
        ):
            raise QualityError("quarantined/denied supplier state requires evidence references")


@dataclass(frozen=True, slots=True)
class ClaimWithdrawalPropagationRecord:
    propagation_id: str
    trigger_ref: str
    invalidated_evidence_refs: tuple[str, ...]
    directly_affected_claim_refs: tuple[str, ...]
    dependent_claim_refs: tuple[str, ...]
    disposition: ClaimImpactDisposition
    history_preserved: bool = True
    deletion_requested: bool = False
    local_ncr_refs: tuple[str, ...] = field(default_factory=tuple)
    resolution_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        _text("propagation_id", self.propagation_id)
        _text("trigger_ref", self.trigger_ref)
        for name in (
            "invalidated_evidence_refs",
            "directly_affected_claim_refs",
            "dependent_claim_refs",
            "local_ncr_refs",
            "resolution_refs",
        ):
            _text_tuple(
                name,
                getattr(self, name),
                allow_empty=name in {"dependent_claim_refs", "local_ncr_refs", "resolution_refs"},
            )
        if type(self.disposition) is not ClaimImpactDisposition:
            raise QualityError("disposition must be an exact ClaimImpactDisposition")
        if type(self.history_preserved) is not bool or type(self.deletion_requested) is not bool:
            raise QualityError("claim withdrawal flags must be exact bools")
        if not self.history_preserved or self.deletion_requested:
            raise QualityError("claim withdrawal must preserve history and cannot request deletion")
        if self.disposition is ClaimImpactDisposition.RESOLVED and not self.resolution_refs:
            raise QualityError("resolved claim propagation requires resolution refs")
        if self.disposition is ClaimImpactDisposition.WITHDRAWAL_REQUIRED and not self.invalidated_evidence_refs:
            raise QualityError("claim withdrawal requires invalidated evidence refs")


@dataclass(frozen=True, slots=True)
class SamplingRound:
    round_index: int
    sample_ref: str
    randomization_ref: str
    inspected_count: int
    defect_count: int

    def __post_init__(self) -> None:
        if type(self.round_index) is not int or self.round_index < 1:
            raise QualityError("round_index must be a positive exact int")
        _text("sample_ref", self.sample_ref)
        _text("randomization_ref", self.randomization_ref)
        if type(self.inspected_count) is not int or self.inspected_count < 1:
            raise QualityError("inspected_count must be a positive exact int")
        if type(self.defect_count) is not int or self.defect_count < 0 or self.defect_count > self.inspected_count:
            raise QualityError("defect_count must be between zero and inspected_count")


@dataclass(frozen=True, slots=True)
class RepeatedRandomSpotCheckPlan:
    sampling_plan_id: str
    lot_or_process_id: str
    population_definition: str
    population_size: int
    risk_class: SamplingRiskClass
    round_count: int
    sample_size_per_round: int
    acceptance_number_per_round: int
    rounds: tuple[SamplingRound, ...]
    reinspection_trigger_refs: tuple[str, ...]
    full_inspection_trigger: str
    irregular_reinspection_required: bool = True
    selection_method: str = "RANDOM"
    subjectivity_critical: bool = False

    def __post_init__(self) -> None:
        for name in (
            "sampling_plan_id",
            "lot_or_process_id",
            "population_definition",
            "full_inspection_trigger",
        ):
            _text(name, getattr(self, name))
        if type(self.risk_class) is not SamplingRiskClass:
            raise QualityError("risk_class must be an exact SamplingRiskClass")
        if type(self.round_count) is not int or not 3 <= self.round_count <= 10:
            raise QualityError("round_count must be preregistered between 3 and 10")
        if type(self.population_size) is not int or self.population_size < 1:
            raise QualityError("population_size must be a positive exact int")
        if type(self.sample_size_per_round) is not int or not 1 <= self.sample_size_per_round <= self.population_size:
            raise QualityError("sample_size_per_round must fit the declared population")
        if type(self.acceptance_number_per_round) is not int or not 0 <= self.acceptance_number_per_round <= self.sample_size_per_round:
            raise QualityError("acceptance_number_per_round must fit the sample size")
        if type(self.rounds) is not tuple or len(self.rounds) != self.round_count:
            raise QualityError("rounds must exactly match preregistered round_count")
        if [item.round_index for item in self.rounds] != list(range(1, self.round_count + 1)):
            raise QualityError("sampling rounds must be complete and sequential")
        if any(item.inspected_count != self.sample_size_per_round for item in self.rounds):
            raise QualityError("each sampling round must use the preregistered sample size")
        randomization_refs = [item.randomization_ref for item in self.rounds]
        if len(randomization_refs) != len(set(randomization_refs)):
            raise QualityError("each sampling round requires a distinct randomization reference")
        _text_tuple("reinspection_trigger_refs", self.reinspection_trigger_refs)
        if type(self.irregular_reinspection_required) is not bool or type(self.subjectivity_critical) is not bool:
            raise QualityError("sampling policy flags must be exact bools")
        if not self.irregular_reinspection_required:
            raise QualityError("repeated spot-check control requires irregular reinspection")
        if self.selection_method != "RANDOM":
            raise QualityError("repeated spot-check control requires random selection")
        if self.subjectivity_critical:
            raise QualityError("subjectivity-critical admission cannot use sampling as a substitute for full review")


@dataclass(frozen=True, slots=True)
class SamplingAssessment:
    sampling_plan_id: str
    disposition: SamplingDisposition
    reasons: tuple[str, ...]
    population_verified: bool = False
    zero_defect_claim: bool = False


def assess_repeated_random_sampling(plan: RepeatedRandomSpotCheckPlan) -> SamplingAssessment:
    reasons = [
        "RANDOM_SELECTION_PER_ROUND_BOUND",
        "ROUND_COUNT_PREREGISTERED_3_TO_10",
        "IRREGULAR_REINSPECTION_REQUIRED",
        "SAMPLE_PASS_IS_NOT_FULL_POPULATION_VERIFICATION",
    ]
    if plan.risk_class is SamplingRiskClass.HIGH_CRITICAL:
        reasons.append("HIGH_CRITICAL_RISK_REQUIRES_FULL_INSPECTION")
        return SamplingAssessment(
            plan.sampling_plan_id,
            SamplingDisposition.FULL_INSPECTION_REQUIRED,
            tuple(reasons),
        )
    failing_rounds = tuple(
        item.round_index
        for item in plan.rounds
        if item.defect_count > plan.acceptance_number_per_round
    )
    if failing_rounds:
        reasons.append("SAMPLING_ROUND_EXCEEDED_ACCEPTANCE_NUMBER:" + ",".join(map(str, failing_rounds)))
        reasons.append("ESCALATE_TO_FULL_INSPECTION")
        return SamplingAssessment(
            plan.sampling_plan_id,
            SamplingDisposition.FULL_INSPECTION_REQUIRED,
            tuple(reasons),
        )
    reasons.append("MULTI_ROUND_SAMPLE_SUPPORTS_BOUNDED_CONFIDENCE_ONLY")
    return SamplingAssessment(
        plan.sampling_plan_id,
        SamplingDisposition.BOUNDED_CONFIDENCE_ONLY,
        tuple(reasons),
    )


@dataclass(frozen=True, slots=True)
class ProcessMetricSeries:
    series_id: str
    process_signature: str
    measurement_ref: str
    metric_name: str
    observation_refs: tuple[str, ...]
    values: tuple[float, ...]
    declared_window: str
    lower_control_limit: float
    center_line: float
    upper_control_limit: float
    homogeneous_process: bool = True

    def __post_init__(self) -> None:
        for name in (
            "series_id",
            "process_signature",
            "measurement_ref",
            "metric_name",
            "declared_window",
        ):
            _text(name, getattr(self, name))
        _text_tuple("observation_refs", self.observation_refs)
        if type(self.values) is not tuple or len(self.values) != len(self.observation_refs) or len(self.values) < 3:
            raise QualityError("process metric series requires at least three trace-bound observations")
        if any(type(value) is not float or not math.isfinite(value) for value in self.values):
            raise QualityError("process metric values must be finite exact floats")
        if not all(
            type(value) is float and math.isfinite(value)
            for value in (self.lower_control_limit, self.center_line, self.upper_control_limit)
        ):
            raise QualityError("process control limits must be finite exact floats")
        if not self.lower_control_limit < self.center_line < self.upper_control_limit:
            raise QualityError("process control limits must satisfy lower < center < upper")
        if type(self.homogeneous_process) is not bool or not self.homogeneous_process:
            raise QualityError("SPC-style monitoring requires a homogeneous declared process")


@dataclass(frozen=True, slots=True)
class ProcessStabilityAssessment:
    series_id: str
    disposition: ProcessStabilityDisposition
    out_of_control_indices: tuple[int, ...]
    reasons: tuple[str, ...]
    subjectivity_conclusion: str = "NOT_ESTABLISHED"


def assess_process_stability(series: ProcessMetricSeries) -> ProcessStabilityAssessment:
    outliers = tuple(
        index
        for index, value in enumerate(series.values, start=1)
        if value < series.lower_control_limit or value > series.upper_control_limit
    )
    reasons = [
        "PROCESS_SIGNATURE_BOUND",
        "DECLARED_LIMITS_USED_NOT_REESTIMATED_POST_HOC",
        "PROCESS_STABILITY_SIGNAL_IS_NOT_SUBJECTIVITY_EVIDENCE",
    ]
    if outliers:
        reasons.append("OUT_OF_CONTROL_OBSERVATIONS:" + ",".join(map(str, outliers)))
        return ProcessStabilityAssessment(
            series.series_id,
            ProcessStabilityDisposition.REVIEW_REQUIRED,
            outliers,
            tuple(reasons),
        )
    reasons.append("NO_DECLARED_LIMIT_BREACH_OBSERVED")
    return ProcessStabilityAssessment(
        series.series_id,
        ProcessStabilityDisposition.BOUNDED_STABLE_SIGNAL,
        (),
        tuple(reasons),
    )


@dataclass(frozen=True, slots=True)
class ExtendedQualityControls:
    data_quality: tuple[DataQualityRecord, ...] = field(default_factory=tuple)
    supplier_quality: tuple[UpstreamQualityRecord, ...] = field(default_factory=tuple)
    sampling: tuple[SamplingAssessment, ...] = field(default_factory=tuple)
    process_stability: tuple[ProcessStabilityAssessment, ...] = field(default_factory=tuple)
    claim_withdrawal: tuple[ClaimWithdrawalPropagationRecord, ...] = field(default_factory=tuple)

    def trace_refs(self) -> tuple[str, ...]:
        if not self.data_quality:
            raise QualityError("full QMS requires at least one data-quality record")
        if not self.supplier_quality:
            raise QualityError("full QMS requires at least one upstream supplier-quality record")
        refs = [item.data_id for item in self.data_quality]
        refs.extend(item.supplier_object_id for item in self.supplier_quality)
        refs.extend(item.sampling_plan_id for item in self.sampling)
        refs.extend(item.series_id for item in self.process_stability)
        refs.extend(item.propagation_id for item in self.claim_withdrawal)
        if len(refs) != len(set(refs)):
            raise QualityError("extended quality control identifiers must be unique")
        return tuple(refs)


@dataclass(frozen=True, slots=True)
class FullQualitySystemAssessment:
    plan_id: str
    disposition: EndToEndDisposition
    reasons: tuple[str, ...]
    base_assessment: EndToEndQualityAssessment
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    scientific_disposition: str = "HOLD"
    merge_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False


class FullQualitySystemEngine:
    """Adds bounded supplier/data/sampling/process/withdrawal controls around the existing QMS.

    It consumes content-addressed producer receipts from the canonical
    ResearchQualityChain, AI risk/impact control, and standalone structural TEVV
    profile rather than re-running those producer semantics. It does not establish
    model quality, empirical TEVV evidence, subjectivity, scientific validity,
    release authority, or merge authority.
    """

    def assess(
        self,
        *,
        plan: ResearchQualityPlan,
        measurements: tuple[MeasurementAssuranceRecord, ...],
        chain_receipt: QualityChainReceiptBinding,
        risk_impact_receipt: AIRiskImpactReceipt,
        tevv_receipt: TEVVProfileReceipt,
        field_signals: tuple[FieldQualitySignal, ...],
        audits: tuple[QualityAuditRecord, ...],
        management_review: ManagementReviewRecord,
        controls: ExtendedQualityControls,
    ) -> FullQualitySystemAssessment:
        reasons: list[str] = ["FULL_RESEARCH_QMS_EXTENSION_EVALUATED"]

        required_configuration_refs = {
            f"git:{chain_receipt.producer_git_head}",
            f"tree:{chain_receipt.producer_tree_sha}",
            f"contract-sha256:{chain_receipt.producer_contract_sha256}",
            f"quality-chain-receipt:{chain_receipt.receipt_sha256}",
            chain_receipt.exact_source_state_ref,
            chain_receipt.exact_runtime_ref,
            f"git:{risk_impact_receipt.producer_git_head}",
            f"tree:{risk_impact_receipt.producer_tree_sha}",
            f"contract-sha256:{risk_impact_receipt.producer_contract_sha256}",
            f"risk-impact-receipt:{risk_impact_receipt.receipt_sha256}",
            risk_impact_receipt.exact_source_state_ref,
            risk_impact_receipt.exact_runtime_ref,
            f"git:{tevv_receipt.producer_git_head}",
            f"tree:{tevv_receipt.producer_tree_sha}",
            f"contract-sha256:{tevv_receipt.producer_contract_sha256}",
            f"tevv-profile-receipt:{tevv_receipt.receipt_sha256}",
            f"tevv-profile:{tevv_receipt.profile_id}:{tevv_receipt.profile_sha256}",
            f"tevv-vocabulary-sha256:{tevv_receipt.tevv_vocabulary_sha256}",
            tevv_receipt.exact_source_state_ref,
            tevv_receipt.exact_runtime_ref,
        }
        if not required_configuration_refs <= set(plan.configuration_refs):
            reasons.append("QUALITY_RECEIPTS_NOT_BOUND_TO_QUALITY_PLAN_CONFIGURATION")

        if risk_impact_receipt.assessment_target_ref != f"quality-plan:{plan.plan_id}":
            reasons.append("AI_RISK_IMPACT_RECEIPT_TARGET_MISMATCH")

        if risk_impact_receipt.assessment_target_sha256 != plan.assessment_target_sha256():
            reasons.append("AI_RISK_IMPACT_RECEIPT_TARGET_DIGEST_MISMATCH")

        if not set(risk_impact_receipt.risk_ids) <= set(plan.risk_refs):
            reasons.append("AI_RISK_REGISTER_NOT_BOUND_TO_QUALITY_PLAN_RISK_REFS")

        if tevv_receipt.assessment_target_ref != f"quality-plan:{plan.plan_id}":
            reasons.append("TEVV_RECEIPT_TARGET_MISMATCH")

        if tevv_receipt.assessment_target_sha256 != plan.assessment_target_sha256():
            reasons.append("TEVV_RECEIPT_TARGET_DIGEST_MISMATCH")

        if not set(tevv_receipt.risk_refs) <= set(plan.risk_refs):
            reasons.append("TEVV_RISKS_NOT_BOUND_TO_QUALITY_PLAN_RISK_REFS")

        tevv_measurement_ids = {
            item.measurement_id for item in tevv_receipt.measurement_bindings
        }
        supplied_measurement_ids = {item.measurement_id for item in measurements}
        if not tevv_measurement_ids <= set(plan.measurement_ids):
            reasons.append("TEVV_MEASUREMENTS_NOT_BOUND_TO_QUALITY_PLAN")
        if not tevv_measurement_ids <= supplied_measurement_ids:
            reasons.append("TEVV_MEASUREMENT_ASSURANCE_RECORDS_MISSING")

        control_data_ids = {item.data_id for item in controls.data_quality}
        if not set(tevv_receipt.data_quality_refs) <= control_data_ids:
            reasons.append("TEVV_DATA_QUALITY_RECORDS_MISSING")

        required_risk_review_refs = {
            risk_impact_receipt.receipt_id,
            *risk_impact_receipt.risk_ids,
            *risk_impact_receipt.impact_assessment_ids,
        }
        if not required_risk_review_refs <= set(management_review.input_refs):
            reasons.append("MANAGEMENT_REVIEW_AI_RISK_IMPACT_INPUTS_INCOMPLETE")

        required_tevv_review_refs = {
            tevv_receipt.receipt_id,
            tevv_receipt.profile_id,
            f"tevv-profile-receipt:{tevv_receipt.receipt_sha256}",
            *tevv_receipt.risk_refs,
            *tevv_measurement_ids,
            *tevv_receipt.data_quality_refs,
        }
        if not required_tevv_review_refs <= set(management_review.input_refs):
            reasons.append("MANAGEMENT_REVIEW_TEVV_INPUTS_INCOMPLETE")

        extended_refs = controls.trace_refs()
        if not set(extended_refs) <= set(management_review.input_refs):
            reasons.append("MANAGEMENT_REVIEW_EXTENDED_CONTROL_INPUTS_INCOMPLETE")

        base = EndToEndQualitySystemEngine().assess(
            plan=plan,
            measurements=measurements,
            chain=chain_receipt.to_existing_binding(),
            field_signals=field_signals,
            audits=audits,
            management_review=management_review,
        )

        data_hold = any(item.disposition is DataQualityDisposition.HOLD for item in controls.data_quality)
        data_requal = any(
            item.disposition is DataQualityDisposition.REQUALIFICATION_REQUIRED
            for item in controls.data_quality
        )
        if data_hold:
            reasons.append("DATA_QUALITY_HOLD")
        if data_requal:
            reasons.append("DATA_QUALITY_REQUALIFICATION_REQUIRED")

        supplier_hold = any(
            item.disposition
            in {
                SupplierQualityDisposition.ENHANCED_REVIEW,
                SupplierQualityDisposition.SCOPE_RESTRICTED,
                SupplierQualityDisposition.QUARANTINED,
                SupplierQualityDisposition.DENIED,
            }
            for item in controls.supplier_quality
        )
        if supplier_hold:
            reasons.append("UPSTREAM_SUPPLIER_QUALITY_REVIEW_REQUIRED")

        sampling_escalation = any(
            item.disposition is SamplingDisposition.FULL_INSPECTION_REQUIRED
            for item in controls.sampling
        )
        sampling_hold = any(item.disposition is SamplingDisposition.HOLD for item in controls.sampling)
        if sampling_escalation:
            reasons.append("SAMPLING_ESCALATED_TO_FULL_INSPECTION")
        if sampling_hold:
            reasons.append("SAMPLING_CONTROL_HOLD")

        process_review = any(
            item.disposition is ProcessStabilityDisposition.REVIEW_REQUIRED
            for item in controls.process_stability
        )
        if process_review:
            reasons.append("PROCESS_STABILITY_REVIEW_REQUIRED")

        claim_impact = any(
            item.disposition is not ClaimImpactDisposition.RESOLVED
            for item in controls.claim_withdrawal
        )
        if claim_impact:
            reasons.append("CLAIM_WITHDRAWAL_OR_REQUALIFICATION_PROPAGATION_OPEN")

        if risk_impact_receipt.disposition is AIRiskImpactDisposition.HOLD:
            reasons.append("AI_RISK_IMPACT_RECEIPT_HOLD")
        elif (
            risk_impact_receipt.disposition
            is AIRiskImpactDisposition.TREATMENT_OR_MITIGATION_REQUIRED
        ):
            reasons.append("AI_RISK_IMPACT_TREATMENT_OR_MITIGATION_REQUIRED")

        if tevv_receipt.disposition is TEVVProfileDisposition.HOLD:
            reasons.append("TEVV_PROFILE_RECEIPT_HOLD")

        hard_hold = any(
            reason in {
                "QUALITY_RECEIPTS_NOT_BOUND_TO_QUALITY_PLAN_CONFIGURATION",
                "AI_RISK_IMPACT_RECEIPT_TARGET_MISMATCH",
                "AI_RISK_IMPACT_RECEIPT_TARGET_DIGEST_MISMATCH",
                "AI_RISK_REGISTER_NOT_BOUND_TO_QUALITY_PLAN_RISK_REFS",
                "TEVV_RECEIPT_TARGET_MISMATCH",
                "TEVV_RECEIPT_TARGET_DIGEST_MISMATCH",
                "TEVV_RISKS_NOT_BOUND_TO_QUALITY_PLAN_RISK_REFS",
                "TEVV_MEASUREMENTS_NOT_BOUND_TO_QUALITY_PLAN",
                "TEVV_MEASUREMENT_ASSURANCE_RECORDS_MISSING",
                "TEVV_DATA_QUALITY_RECORDS_MISSING",
                "MANAGEMENT_REVIEW_AI_RISK_IMPACT_INPUTS_INCOMPLETE",
                "MANAGEMENT_REVIEW_TEVV_INPUTS_INCOMPLETE",
                "MANAGEMENT_REVIEW_EXTENDED_CONTROL_INPUTS_INCOMPLETE",
                "DATA_QUALITY_HOLD",
                "UPSTREAM_SUPPLIER_QUALITY_REVIEW_REQUIRED",
                "SAMPLING_ESCALATED_TO_FULL_INSPECTION",
                "SAMPLING_CONTROL_HOLD",
                "PROCESS_STABILITY_REVIEW_REQUIRED",
                "CLAIM_WITHDRAWAL_OR_REQUALIFICATION_PROPAGATION_OPEN",
                "AI_RISK_IMPACT_RECEIPT_HOLD",
                "AI_RISK_IMPACT_TREATMENT_OR_MITIGATION_REQUIRED",
                "TEVV_PROFILE_RECEIPT_HOLD",
            }
            for reason in reasons
        )
        if base.disposition is EndToEndDisposition.HOLD or hard_hold:
            disposition = EndToEndDisposition.HOLD
        elif base.disposition is EndToEndDisposition.CAPA_REQUIRED or data_requal:
            disposition = EndToEndDisposition.CAPA_REQUIRED
        else:
            disposition = EndToEndDisposition.READY_FOR_HUMAN_REVIEW
            reasons.extend(
                (
                    "CONTENT_ADDRESSED_QUALITY_CHAIN_RECEIPT_BOUND",
                    "CONTENT_ADDRESSED_AI_RISK_IMPACT_RECEIPT_BOUND",
                    "AI_RISK_IMPACT_RECEIPT_TARGET_SEMANTICS_BOUND",
                    "AI_RISK_IMPACT_READY_FOR_HUMAN_REVIEW",
                    "CONTENT_ADDRESSED_TEVV_PROFILE_RECEIPT_BOUND",
                    "TEVV_RECEIPT_TARGET_SEMANTICS_BOUND",
                    "TEVV_RISK_COVERAGE_BOUND_TO_QUALITY_PLAN",
                    "TEVV_MEASUREMENT_ASSURANCE_BINDINGS_COMPLETE",
                    "TEVV_DATA_QUALITY_BINDINGS_COMPLETE",
                    "TEVV_PROFILE_READY_FOR_BOUNDED_EXECUTION_ONLY",
                    "DATA_QUALITY_BOUND_TO_DECLARED_USE",
                    "SUPPLIER_QUALITY_BOUND_TO_DECLARED_SCOPE",
                    "SAMPLING_RESULTS_REMAIN_BOUNDED_CONFIDENCE_ONLY",
                    "PROCESS_MONITORING_IS_PROCESS_HEALTH_NOT_SUBJECTIVITY_EVIDENCE",
                    "CLAIM_INVALIDATION_PRESERVES_HISTORY",
                    "FULL_QMS_PASS_IS_NOT_SUBJECTIVITY_EVIDENCE",
                )
            )
        return FullQualitySystemAssessment(
            plan_id=plan.plan_id,
            disposition=disposition,
            reasons=tuple((*base.reasons, *reasons)),
            base_assessment=base,
        )
