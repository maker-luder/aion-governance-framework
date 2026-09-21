from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.teacher_body_dynamics import (
    TeacherBodyObservation,
    integrate_teacher_body_state,
)
from aion_astra_twin_embodiment.teacher_body_runtime import (
    build_teacher_body_runtime_binding,
)
from aion_astra_twin_embodiment.teacher_micturition import (
    assess_teacher_micturition_causal_chain,
    validate_teacher_micturition_causal_assessment,
)


def _state(
    *,
    sequence: int,
    timestamp_ms: int,
    bladder_fill: float,
    bladder_afferent: float,
    detrusor: float,
    outlet_relaxation: float,
    sphincter_relaxation: float,
    micturition_reflex: float,
    urine_flow: float,
    renal_filtration: float = 0.5,
    urine_production: float = 0.4,
):
    return integrate_teacher_body_state(
        (
            TeacherBodyObservation(
                "TACTILE_GENERAL",
                (0.2,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "JOINT_POSITION",
                (0.1,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "VESTIBULAR_ORIENTATION",
                (1.0, 0.0, 0.0, 0.0),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "CARDIOVASCULAR_STATE",
                (0.5,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "RENAL_FILTRATION_STATE",
                (renal_filtration,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "URINE_PRODUCTION_STATE",
                (urine_production,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "BLADDER_STATE",
                (bladder_fill,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "BLADDER_AFFERENT_STATE",
                (bladder_afferent,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "DETRUSOR_CONTRACTION_STATE",
                (detrusor,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "URETHRAL_OUTLET_RELAXATION_STATE",
                (outlet_relaxation,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "EXTERNAL_URETHRAL_SPHINCTER_RELAXATION_STATE",
                (sphincter_relaxation,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "MICTURITION_REFLEX_STATE",
                (micturition_reflex,),
                timestamp_ms,
            ),
            TeacherBodyObservation(
                "URINE_FLOW_STATE",
                (urine_flow,),
                timestamp_ms,
            ),
        ),
        sequence=sequence,
    )


def _coherent_cycle():
    storage = _state(
        sequence=1,
        timestamp_ms=100,
        bladder_fill=0.8,
        bladder_afferent=0.3,
        detrusor=0.1,
        outlet_relaxation=0.1,
        sphincter_relaxation=0.1,
        micturition_reflex=0.1,
        urine_flow=0.0,
    )
    voiding = _state(
        sequence=2,
        timestamp_ms=200,
        bladder_fill=0.6,
        bladder_afferent=0.9,
        detrusor=0.9,
        outlet_relaxation=0.9,
        sphincter_relaxation=0.9,
        micturition_reflex=0.9,
        urine_flow=0.8,
    )
    recovery = _state(
        sequence=3,
        timestamp_ms=300,
        bladder_fill=0.15,
        bladder_afferent=0.1,
        detrusor=0.1,
        outlet_relaxation=0.1,
        sphincter_relaxation=0.1,
        micturition_reflex=0.1,
        urine_flow=0.0,
    )
    return storage, voiding, recovery


def test_coordinated_micturition_passes_forward_reverse_and_recovery() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-MICTURITION",
        "SESSION-MICTURITION",
    )
    storage, voiding, recovery = _coherent_cycle()

    assessment = assess_teacher_micturition_causal_chain(
        binding=binding,
        storage_state=storage,
        voiding_state=voiding,
        recovery_state=recovery,
    )
    result = validate_teacher_micturition_causal_assessment(
        assessment,
        binding,
    )

    assert result["result"] == "PASS"
    assert assessment.event_classification == (
        "COORDINATED_MICTURITION_REFERENCE"
    )
    assert assessment.forward_causal_path_status == "PASS"
    assert assessment.reverse_evidence_trace_status == "PASS"
    assert assessment.recovery_path_status == "PASS"
    assert assessment.alternative_cause_disambiguation_status == (
        "PASS_COORDINATED_PATTERN_PRESENT"
    )
    assert assessment.counterfactual_dependency_status == (
        "PASS_REQUIRED_DEPENDENCIES_EXPLICIT"
    )
    assert assessment.recovery_state.bladder_fill_state < (
        assessment.storage_state.bladder_fill_state
    )
    assert len(assessment.assessment_sha256) == 64
    assert assessment.source_pmids == (
        "18490916",
        "23033877",
        "26003239",
        "34805017",
    )


def test_flow_without_required_upstream_pattern_is_not_misattributed() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-MICTURITION",
        "SESSION-MICTURITION",
    )
    storage, _, recovery = _coherent_cycle()
    incoherent_flow = _state(
        sequence=2,
        timestamp_ms=200,
        bladder_fill=0.6,
        bladder_afferent=0.1,
        detrusor=0.1,
        outlet_relaxation=0.1,
        sphincter_relaxation=0.1,
        micturition_reflex=0.1,
        urine_flow=0.8,
    )

    assessment = assess_teacher_micturition_causal_chain(
        binding=binding,
        storage_state=storage,
        voiding_state=incoherent_flow,
        recovery_state=recovery,
    )

    assert assessment.event_classification == (
        "UNRESOLVED_NON_MICTURITION_URETHRAL_FLOW_REFERENCE"
    )
    assert assessment.forward_causal_path_status == "FAIL"
    assert assessment.reverse_evidence_trace_status == (
        "FAIL_REQUIRED_UPSTREAM_EVIDENCE_MISSING"
    )
    assert assessment.alternative_cause_disambiguation_status == (
        "PASS_FLOW_NOT_MISATTRIBUTED_TO_MICTURITION"
    )
    assert assessment.counterfactual_dependency_status == (
        "PASS_NEGATIVE_CONTROL_CLASSIFICATION"
    )


def test_recovery_path_must_reduce_bladder_load_and_stop_flow() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-MICTURITION",
        "SESSION-MICTURITION",
    )
    storage, voiding, _ = _coherent_cycle()
    bad_recovery = _state(
        sequence=3,
        timestamp_ms=300,
        bladder_fill=0.85,
        bladder_afferent=0.2,
        detrusor=0.1,
        outlet_relaxation=0.1,
        sphincter_relaxation=0.1,
        micturition_reflex=0.1,
        urine_flow=0.4,
    )

    assessment = assess_teacher_micturition_causal_chain(
        binding=binding,
        storage_state=storage,
        voiding_state=voiding,
        recovery_state=bad_recovery,
    )

    assert assessment.event_classification == (
        "COORDINATED_MICTURITION_REFERENCE"
    )
    assert assessment.reverse_evidence_trace_status == "PASS"
    assert assessment.recovery_path_status == "FAIL"
    assert assessment.forward_causal_path_status == "FAIL"


def test_micturition_requires_all_causal_source_channels() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-MICTURITION",
        "SESSION-MICTURITION",
    )
    storage, voiding, recovery = _coherent_cycle()
    missing_afferent = replace(
        voiding,
        observations=tuple(
            observation
            for observation in voiding.observations
            if observation.channel_id != "BLADDER_AFFERENT_STATE"
        ),
    )

    with pytest.raises(
        ValueError,
        match="micturition assessment requires body observation: "
        "BLADDER_AFFERENT_STATE",
    ):
        assess_teacher_micturition_causal_chain(
            binding=binding,
            storage_state=storage,
            voiding_state=missing_afferent,
            recovery_state=recovery,
        )


def test_micturition_validator_rejects_tampered_phase_and_time_order() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-MICTURITION",
        "SESSION-MICTURITION",
    )
    storage, voiding, recovery = _coherent_cycle()
    assessment = assess_teacher_micturition_causal_chain(
        binding=binding,
        storage_state=storage,
        voiding_state=voiding,
        recovery_state=recovery,
    )

    with pytest.raises(ValueError, match="phase values must be normalized"):
        validate_teacher_micturition_causal_assessment(
            replace(
                assessment,
                voiding_state=replace(
                    assessment.voiding_state,
                    urine_flow_state=1.5,
                ),
            ),
            binding,
        )

    with pytest.raises(ValueError, match="assessment sequence drift"):
        validate_teacher_micturition_causal_assessment(
            replace(
                assessment,
                recovery_state=replace(
                    assessment.recovery_state,
                    sequence=1,
                ),
            ),
            binding,
        )


def test_micturition_reference_does_not_establish_felt_urge_or_relief() -> None:
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-MICTURITION",
        "SESSION-MICTURITION",
    )
    storage, voiding, recovery = _coherent_cycle()
    assessment = assess_teacher_micturition_causal_chain(
        binding=binding,
        storage_state=storage,
        voiding_state=voiding,
        recovery_state=recovery,
    )

    assert assessment.threshold_interpretation == (
        "ENGINEERING_REFERENCE_THRESHOLDS_NOT_CLINICAL_THRESHOLDS"
    )
    assert assessment.causal_interpretation == "REFERENCE_CAUSAL_ORDER_ONLY"
    assert assessment.biological_mechanism_identity_status == "NOT_ESTABLISHED"
    assert assessment.felt_urge_status == "NOT_ESTABLISHED"
    assert assessment.felt_relief_status == "NOT_ESTABLISHED"
    assert assessment.phenomenal_experience_status == "NOT_ESTABLISHED"
    assert assessment.subjectivity_status == "NOT_ESTABLISHED"
