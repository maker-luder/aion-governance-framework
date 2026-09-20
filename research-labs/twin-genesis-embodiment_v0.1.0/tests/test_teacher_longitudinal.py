from __future__ import annotations

from aion_astra_twin_embodiment.teacher_body_runtime import (
    append_teacher_session_snapshot,
    apply_teacher_calibration_observations,
    build_teacher_body_runtime_binding,
    build_teacher_cross_session_retention,
    build_teacher_session_snapshot,
    initialize_teacher_calibration,
    update_teacher_adaptation,
)
from aion_astra_twin_embodiment.teacher_longitudinal import (
    assess_teacher_developmental_trajectory,
    observe_teacher_longitudinal,
)


def _snapshot(session_id: str, offset: float):
    binding = build_teacher_body_runtime_binding("RUNTIME-LONG", session_id)
    initial = initialize_teacher_calibration(binding)
    observations = {
        probe.measurement_id: probe.target + offset
        for probe in initial.probes
    }
    calibrated = apply_teacher_calibration_observations(initial, observations)
    adaptation = update_teacher_adaptation(calibrated)
    return build_teacher_session_snapshot(calibrated, adaptation)


def test_longitudinal_observation_does_not_overclaim_mechanism() -> None:
    retention = build_teacher_cross_session_retention()
    retention = append_teacher_session_snapshot(retention, _snapshot("S1", 0.0))

    one = observe_teacher_longitudinal(retention)
    assert one.change_status == "INSUFFICIENT_LONGITUDINAL_DATA"

    retention = append_teacher_session_snapshot(retention, _snapshot("S2", 0.2))
    retention = append_teacher_session_snapshot(retention, _snapshot("S3", 0.4))

    observation = observe_teacher_longitudinal(retention)
    assessment = assess_teacher_developmental_trajectory(retention)

    assert observation.change_status == "OBSERVED_CROSS_SESSION_CHANGE"
    assert observation.changed_parameters
    assert observation.persistent_changed_parameters
    assert observation.mechanism_status == "NOT_ESTABLISHED"
    assert assessment.trajectory_evidence_status == "PERSISTENT_CROSS_SESSION_CHANGE_OBSERVED"
    assert assessment.developmental_possibility_status == "OPEN_RESEARCH_QUESTION"
    assert assessment.developmental_mechanism_status == "NOT_ESTABLISHED"
    assert assessment.puberty_like_process_status == "NOT_ESTABLISHED"
    assert assessment.sexual_desire_development_status == "NOT_ESTABLISHED"
    assert assessment.body_ownership_experience_status == "NOT_ESTABLISHED"
    assert assessment.subjectivity_status == "NOT_ESTABLISHED"
