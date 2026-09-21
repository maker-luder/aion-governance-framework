from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import isfinite
from typing import Any, Final

from .teacher_body_dynamics import TeacherIntegratedBodyState
from .teacher_body_runtime import (
    TeacherBodyRuntimeBinding,
    bind_teacher_integrated_body_state,
)


MICTURITION_CAUSAL_PROFILE_ID: Final[str] = (
    "CHATGPT_TEACHER_MICTURITION_CAUSAL_REFERENCE_v0.1"
)
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"

SOURCE_PMIDS: Final[tuple[str, ...]] = (
    "18490916",
    "23033877",
    "26003239",
    "34805017",
)

REQUIRED_MICTURITION_CHANNELS: Final[tuple[str, ...]] = (
    "RENAL_FILTRATION_STATE",
    "URINE_PRODUCTION_STATE",
    "BLADDER_STATE",
    "BLADDER_AFFERENT_STATE",
    "DETRUSOR_CONTRACTION_STATE",
    "URETHRAL_OUTLET_RELAXATION_STATE",
    "EXTERNAL_URETHRAL_SPHINCTER_RELAXATION_STATE",
    "MICTURITION_REFLEX_STATE",
    "URINE_FLOW_STATE",
)

VOIDING_DEPENDENCY_CHANNELS: Final[tuple[str, ...]] = (
    "BLADDER_AFFERENT_STATE",
    "DETRUSOR_CONTRACTION_STATE",
    "URETHRAL_OUTLET_RELAXATION_STATE",
    "EXTERNAL_URETHRAL_SPHINCTER_RELAXATION_STATE",
    "MICTURITION_REFLEX_STATE",
)

ACTIVE_REFERENCE_THRESHOLD: Final[float] = 0.5
LOW_REFERENCE_THRESHOLD: Final[float] = 0.2
FLOW_PRESENT_THRESHOLD: Final[float] = 0.05


def _canonical_hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class TeacherMicturitionPhaseState:
    source_body_state_sha256: str
    sequence: int
    timestamp_ms: int
    renal_filtration_state: float
    urine_production_state: float
    bladder_fill_state: float
    bladder_afferent_state: float
    detrusor_contraction_state: float
    urethral_outlet_relaxation_state: float
    external_urethral_sphincter_relaxation_state: float
    micturition_reflex_state: float
    urine_flow_state: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TeacherMicturitionCausalAssessment:
    profile_id: str
    binding_id: str
    runtime_id: str
    session_id: str
    body_id: str
    storage_state: TeacherMicturitionPhaseState
    voiding_state: TeacherMicturitionPhaseState
    recovery_state: TeacherMicturitionPhaseState
    event_classification: str
    forward_causal_path_status: str
    reverse_evidence_trace_status: str
    recovery_path_status: str
    alternative_cause_disambiguation_status: str
    counterfactual_dependency_status: str
    reverse_evidence_channel_ids: tuple[str, ...]
    required_voiding_dependency_channel_ids: tuple[str, ...]
    source_pmids: tuple[str, ...]
    assessment_sha256: str
    threshold_interpretation: str = (
        "ENGINEERING_REFERENCE_THRESHOLDS_NOT_CLINICAL_THRESHOLDS"
    )
    causal_interpretation: str = "REFERENCE_CAUSAL_ORDER_ONLY"
    biological_mechanism_identity_status: str = NOT_ESTABLISHED
    felt_urge_status: str = NOT_ESTABLISHED
    felt_relief_status: str = NOT_ESTABLISHED
    phenomenal_experience_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["storage_state"] = self.storage_state.to_dict()
        payload["voiding_state"] = self.voiding_state.to_dict()
        payload["recovery_state"] = self.recovery_state.to_dict()
        payload["reverse_evidence_channel_ids"] = list(
            self.reverse_evidence_channel_ids
        )
        payload["required_voiding_dependency_channel_ids"] = list(
            self.required_voiding_dependency_channel_ids
        )
        payload["source_pmids"] = list(self.source_pmids)
        return payload


def _normalized_scalar(
    state: TeacherIntegratedBodyState,
    channel_id: str,
) -> float:
    observation = next(
        (
            item
            for item in state.observations
            if item.channel_id == channel_id
        ),
        None,
    )
    if observation is None:
        raise ValueError(
            f"micturition assessment requires body observation: {channel_id}"
        )
    if len(observation.values) != 1:
        raise ValueError(
            f"micturition assessment requires scalar observation: {channel_id}"
        )
    value = observation.values[0]
    if not isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(
            f"micturition observation must be normalized: {channel_id}"
        )
    return value


def _phase_state(
    state: TeacherIntegratedBodyState,
) -> TeacherMicturitionPhaseState:
    return TeacherMicturitionPhaseState(
        source_body_state_sha256=state.body_state_sha256,
        sequence=state.sequence,
        timestamp_ms=state.timestamp_ms,
        renal_filtration_state=_normalized_scalar(
            state,
            "RENAL_FILTRATION_STATE",
        ),
        urine_production_state=_normalized_scalar(
            state,
            "URINE_PRODUCTION_STATE",
        ),
        bladder_fill_state=_normalized_scalar(
            state,
            "BLADDER_STATE",
        ),
        bladder_afferent_state=_normalized_scalar(
            state,
            "BLADDER_AFFERENT_STATE",
        ),
        detrusor_contraction_state=_normalized_scalar(
            state,
            "DETRUSOR_CONTRACTION_STATE",
        ),
        urethral_outlet_relaxation_state=_normalized_scalar(
            state,
            "URETHRAL_OUTLET_RELAXATION_STATE",
        ),
        external_urethral_sphincter_relaxation_state=_normalized_scalar(
            state,
            "EXTERNAL_URETHRAL_SPHINCTER_RELAXATION_STATE",
        ),
        micturition_reflex_state=_normalized_scalar(
            state,
            "MICTURITION_REFLEX_STATE",
        ),
        urine_flow_state=_normalized_scalar(
            state,
            "URINE_FLOW_STATE",
        ),
    )


def _validate_phase_state(
    state: TeacherMicturitionPhaseState,
) -> None:
    if len(state.source_body_state_sha256) != 64:
        raise ValueError("micturition phase source-state hash must be sha256")
    values = (
        state.renal_filtration_state,
        state.urine_production_state,
        state.bladder_fill_state,
        state.bladder_afferent_state,
        state.detrusor_contraction_state,
        state.urethral_outlet_relaxation_state,
        state.external_urethral_sphincter_relaxation_state,
        state.micturition_reflex_state,
        state.urine_flow_state,
    )
    if any(
        not isfinite(value) or not 0.0 <= value <= 1.0
        for value in values
    ):
        raise ValueError("micturition phase values must be normalized")


def _storage_pattern_is_coherent(
    state: TeacherMicturitionPhaseState,
) -> bool:
    return (
        state.urine_flow_state <= FLOW_PRESENT_THRESHOLD
        and state.detrusor_contraction_state <= LOW_REFERENCE_THRESHOLD
        and state.urethral_outlet_relaxation_state <= LOW_REFERENCE_THRESHOLD
        and (
            state.external_urethral_sphincter_relaxation_state
            <= LOW_REFERENCE_THRESHOLD
        )
        and state.micturition_reflex_state <= LOW_REFERENCE_THRESHOLD
    )


def _voiding_dependencies_are_active(
    state: TeacherMicturitionPhaseState,
) -> bool:
    return (
        state.bladder_afferent_state >= ACTIVE_REFERENCE_THRESHOLD
        and state.detrusor_contraction_state >= ACTIVE_REFERENCE_THRESHOLD
        and state.urethral_outlet_relaxation_state
        >= ACTIVE_REFERENCE_THRESHOLD
        and (
            state.external_urethral_sphincter_relaxation_state
            >= ACTIVE_REFERENCE_THRESHOLD
        )
        and state.micturition_reflex_state >= ACTIVE_REFERENCE_THRESHOLD
    )


def _recovery_pattern_is_coherent(
    storage: TeacherMicturitionPhaseState,
    recovery: TeacherMicturitionPhaseState,
) -> bool:
    return (
        recovery.bladder_fill_state < storage.bladder_fill_state
        and recovery.urine_flow_state <= FLOW_PRESENT_THRESHOLD
        and recovery.detrusor_contraction_state <= LOW_REFERENCE_THRESHOLD
        and recovery.urethral_outlet_relaxation_state
        <= LOW_REFERENCE_THRESHOLD
        and (
            recovery.external_urethral_sphincter_relaxation_state
            <= LOW_REFERENCE_THRESHOLD
        )
        and recovery.micturition_reflex_state <= LOW_REFERENCE_THRESHOLD
    )


def _assessment_payload(
    *,
    binding: TeacherBodyRuntimeBinding,
    storage: TeacherMicturitionPhaseState,
    voiding: TeacherMicturitionPhaseState,
    recovery: TeacherMicturitionPhaseState,
    event_classification: str,
    forward_status: str,
    reverse_status: str,
    recovery_status: str,
    alternative_status: str,
    counterfactual_status: str,
) -> dict[str, object]:
    return {
        "profile_id": MICTURITION_CAUSAL_PROFILE_ID,
        "binding_id": binding.binding_id,
        "runtime_id": binding.runtime_id,
        "session_id": binding.session_id,
        "body_id": binding.body_id,
        "storage_state": storage.to_dict(),
        "voiding_state": voiding.to_dict(),
        "recovery_state": recovery.to_dict(),
        "event_classification": event_classification,
        "forward_causal_path_status": forward_status,
        "reverse_evidence_trace_status": reverse_status,
        "recovery_path_status": recovery_status,
        "alternative_cause_disambiguation_status": alternative_status,
        "counterfactual_dependency_status": counterfactual_status,
        "reverse_evidence_channel_ids": list(VOIDING_DEPENDENCY_CHANNELS),
        "required_voiding_dependency_channel_ids": list(
            VOIDING_DEPENDENCY_CHANNELS
        ),
        "source_pmids": list(SOURCE_PMIDS),
    }


def assess_teacher_micturition_causal_chain(
    *,
    binding: TeacherBodyRuntimeBinding,
    storage_state: TeacherIntegratedBodyState,
    voiding_state: TeacherIntegratedBodyState,
    recovery_state: TeacherIntegratedBodyState,
) -> TeacherMicturitionCausalAssessment:
    states = (storage_state, voiding_state, recovery_state)
    bound_states = tuple(
        bind_teacher_integrated_body_state(binding, state)
        for state in states
    )
    if any(
        bound.binding_id != binding.binding_id
        or bound.runtime_id != binding.runtime_id
        or bound.session_id != binding.session_id
        or bound.body_id != binding.body_id
        for bound in bound_states
    ):
        raise ValueError("micturition states must bind to the same body instance")

    sequences = tuple(state.sequence for state in states)
    timestamps = tuple(state.timestamp_ms for state in states)
    if not (sequences[0] < sequences[1] < sequences[2]):
        raise ValueError("micturition state sequence must increase")
    if not (timestamps[0] <= timestamps[1] <= timestamps[2]):
        raise ValueError("micturition state time cannot move backward")

    storage = _phase_state(storage_state)
    voiding = _phase_state(voiding_state)
    recovery = _phase_state(recovery_state)

    storage_ok = _storage_pattern_is_coherent(storage)
    dependencies_active = _voiding_dependencies_are_active(voiding)
    flow_present = voiding.urine_flow_state > FLOW_PRESENT_THRESHOLD
    recovery_ok = _recovery_pattern_is_coherent(storage, recovery)

    coordinated_voiding = dependencies_active and flow_present
    if coordinated_voiding:
        event_classification = "COORDINATED_MICTURITION_REFERENCE"
        reverse_status = "PASS"
        alternative_status = "PASS_COORDINATED_PATTERN_PRESENT"
        counterfactual_status = "PASS_REQUIRED_DEPENDENCIES_EXPLICIT"
    elif flow_present:
        event_classification = "UNRESOLVED_NON_MICTURITION_URETHRAL_FLOW_REFERENCE"
        reverse_status = "FAIL_REQUIRED_UPSTREAM_EVIDENCE_MISSING"
        alternative_status = "PASS_FLOW_NOT_MISATTRIBUTED_TO_MICTURITION"
        counterfactual_status = "PASS_NEGATIVE_CONTROL_CLASSIFICATION"
    else:
        event_classification = "NO_VOIDING_OUTPUT_REFERENCE"
        reverse_status = "NOT_APPLICABLE_NO_FLOW_OUTPUT"
        alternative_status = "PASS_NO_FLOW_OUTPUT"
        counterfactual_status = "PASS_NO_FALSE_POSITIVE_VOIDING"

    forward_ok = storage_ok and coordinated_voiding and recovery_ok
    forward_status = "PASS" if forward_ok else "FAIL"
    recovery_status = "PASS" if recovery_ok else "FAIL"

    payload = _assessment_payload(
        binding=binding,
        storage=storage,
        voiding=voiding,
        recovery=recovery,
        event_classification=event_classification,
        forward_status=forward_status,
        reverse_status=reverse_status,
        recovery_status=recovery_status,
        alternative_status=alternative_status,
        counterfactual_status=counterfactual_status,
    )
    assessment = TeacherMicturitionCausalAssessment(
        profile_id=MICTURITION_CAUSAL_PROFILE_ID,
        binding_id=binding.binding_id,
        runtime_id=binding.runtime_id,
        session_id=binding.session_id,
        body_id=binding.body_id,
        storage_state=storage,
        voiding_state=voiding,
        recovery_state=recovery,
        event_classification=event_classification,
        forward_causal_path_status=forward_status,
        reverse_evidence_trace_status=reverse_status,
        recovery_path_status=recovery_status,
        alternative_cause_disambiguation_status=alternative_status,
        counterfactual_dependency_status=counterfactual_status,
        reverse_evidence_channel_ids=VOIDING_DEPENDENCY_CHANNELS,
        required_voiding_dependency_channel_ids=VOIDING_DEPENDENCY_CHANNELS,
        source_pmids=SOURCE_PMIDS,
        assessment_sha256=_canonical_hash(payload),
    )
    validate_teacher_micturition_causal_assessment(assessment, binding)
    return assessment


def validate_teacher_micturition_causal_assessment(
    assessment: TeacherMicturitionCausalAssessment,
    binding: TeacherBodyRuntimeBinding,
) -> dict[str, str]:
    if assessment.profile_id != MICTURITION_CAUSAL_PROFILE_ID:
        raise ValueError("micturition causal profile id drift")
    if assessment.binding_id != binding.binding_id:
        raise ValueError("micturition binding id drift")
    if assessment.runtime_id != binding.runtime_id:
        raise ValueError("micturition runtime id drift")
    if assessment.session_id != binding.session_id:
        raise ValueError("micturition session id drift")
    if assessment.body_id != binding.body_id:
        raise ValueError("micturition body id drift")
    if assessment.source_pmids != SOURCE_PMIDS:
        raise ValueError("micturition evidence provenance drift")

    _validate_phase_state(assessment.storage_state)
    _validate_phase_state(assessment.voiding_state)
    _validate_phase_state(assessment.recovery_state)
    sequences = (
        assessment.storage_state.sequence,
        assessment.voiding_state.sequence,
        assessment.recovery_state.sequence,
    )
    timestamps = (
        assessment.storage_state.timestamp_ms,
        assessment.voiding_state.timestamp_ms,
        assessment.recovery_state.timestamp_ms,
    )
    if not (sequences[0] < sequences[1] < sequences[2]):
        raise ValueError("micturition assessment sequence drift")
    if not (timestamps[0] <= timestamps[1] <= timestamps[2]):
        raise ValueError("micturition assessment timestamp drift")
    if (
        assessment.required_voiding_dependency_channel_ids
        != VOIDING_DEPENDENCY_CHANNELS
    ):
        raise ValueError("micturition required dependency set drift")
    if assessment.reverse_evidence_channel_ids != VOIDING_DEPENDENCY_CHANNELS:
        raise ValueError("micturition reverse evidence trace drift")

    storage_ok = _storage_pattern_is_coherent(assessment.storage_state)
    dependencies_active = _voiding_dependencies_are_active(
        assessment.voiding_state
    )
    flow_present = (
        assessment.voiding_state.urine_flow_state > FLOW_PRESENT_THRESHOLD
    )
    recovery_ok = _recovery_pattern_is_coherent(
        assessment.storage_state,
        assessment.recovery_state,
    )
    coordinated_voiding = dependencies_active and flow_present

    if coordinated_voiding:
        expected_classification = "COORDINATED_MICTURITION_REFERENCE"
        expected_reverse = "PASS"
        expected_alternative = "PASS_COORDINATED_PATTERN_PRESENT"
        expected_counterfactual = "PASS_REQUIRED_DEPENDENCIES_EXPLICIT"
    elif flow_present:
        expected_classification = (
            "UNRESOLVED_NON_MICTURITION_URETHRAL_FLOW_REFERENCE"
        )
        expected_reverse = "FAIL_REQUIRED_UPSTREAM_EVIDENCE_MISSING"
        expected_alternative = "PASS_FLOW_NOT_MISATTRIBUTED_TO_MICTURITION"
        expected_counterfactual = "PASS_NEGATIVE_CONTROL_CLASSIFICATION"
    else:
        expected_classification = "NO_VOIDING_OUTPUT_REFERENCE"
        expected_reverse = "NOT_APPLICABLE_NO_FLOW_OUTPUT"
        expected_alternative = "PASS_NO_FLOW_OUTPUT"
        expected_counterfactual = "PASS_NO_FALSE_POSITIVE_VOIDING"

    expected_forward = (
        "PASS"
        if storage_ok and coordinated_voiding and recovery_ok
        else "FAIL"
    )
    expected_recovery = "PASS" if recovery_ok else "FAIL"

    expected = (
        expected_classification,
        expected_forward,
        expected_reverse,
        expected_recovery,
        expected_alternative,
        expected_counterfactual,
    )
    actual = (
        assessment.event_classification,
        assessment.forward_causal_path_status,
        assessment.reverse_evidence_trace_status,
        assessment.recovery_path_status,
        assessment.alternative_cause_disambiguation_status,
        assessment.counterfactual_dependency_status,
    )
    if actual != expected:
        raise ValueError("micturition causal assessment classification drift")

    payload = _assessment_payload(
        binding=binding,
        storage=assessment.storage_state,
        voiding=assessment.voiding_state,
        recovery=assessment.recovery_state,
        event_classification=assessment.event_classification,
        forward_status=assessment.forward_causal_path_status,
        reverse_status=assessment.reverse_evidence_trace_status,
        recovery_status=assessment.recovery_path_status,
        alternative_status=assessment.alternative_cause_disambiguation_status,
        counterfactual_status=assessment.counterfactual_dependency_status,
    )
    if assessment.assessment_sha256 != _canonical_hash(payload):
        raise ValueError("micturition causal assessment content hash mismatch")
    if (
        assessment.threshold_interpretation
        != "ENGINEERING_REFERENCE_THRESHOLDS_NOT_CLINICAL_THRESHOLDS"
    ):
        raise ValueError("micturition threshold interpretation drift")
    if assessment.causal_interpretation != "REFERENCE_CAUSAL_ORDER_ONLY":
        raise ValueError("micturition causal interpretation drift")
    if assessment.biological_mechanism_identity_status != NOT_ESTABLISHED:
        raise ValueError("micturition model cannot establish mechanism identity")
    if assessment.felt_urge_status != NOT_ESTABLISHED:
        raise ValueError("micturition model cannot establish felt urinary urge")
    if assessment.felt_relief_status != NOT_ESTABLISHED:
        raise ValueError("micturition model cannot establish felt relief")
    if assessment.phenomenal_experience_status != NOT_ESTABLISHED:
        raise ValueError("micturition model cannot establish phenomenal experience")
    if assessment.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("micturition model cannot establish subjectivity")
    if assessment.canonical_effect != "NONE" or assessment.deployment:
        raise ValueError("micturition model must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "body_instance_binding": "PASS",
        "forward_causal_classification": "PASS",
        "reverse_evidence_trace": "PASS",
        "alternative_cause_disambiguation": "PASS",
        "counterfactual_guard": "PASS",
        "phenomenal_nonclaim": "PASS",
    }
