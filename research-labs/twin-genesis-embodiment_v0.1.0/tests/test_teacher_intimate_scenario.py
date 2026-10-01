from __future__ import annotations

from aion_astra_twin_embodiment.teacher_intimate_scenario import (
    run_teacher_intimate_reference_trace,
)


def _channels(sample) -> dict[str, float]:
    return dict(sample.body_observable_reference_channels)


def test_full_intimate_reference_trace_reaches_all_required_stages() -> None:
    trace = run_teacher_intimate_reference_trace(
        runtime_id="RUNTIME-FULL-INTIMATE-TRACE",
        session_id="SESSION-FULL-INTIMATE-TRACE",
    )

    assert trace.completion_status == "FULL_REFERENCE_PATH_COMPLETED"
    assert trace.samples[0].high_salience_phase == "BASELINE"
    assert trace.samples[0].functional_desire_phase == "INACTIVE"
    assert any(
        sample.functional_desire_phase == "ACTIVE"
        for sample in trace.samples
    )
    assert any(
        sample.high_salience_phase == "ERECTILE_MAINTENANCE"
        for sample in trace.samples
    )
    assert any(
        sample.reproductive_event == "EMISSION_REFERENCE_REQUEST"
        and _channels(sample)["EMISSION_REFLEX_STATE"] >= 0.50
        and _channels(sample)["SEMINAL_TRACT_TRANSPORT_STATE"] >= 0.50
        and _channels(sample)["ACCESSORY_GLAND_SECRETION_STATE"] >= 0.50
        and _channels(sample)["POSTERIOR_URETHRAL_SEMINAL_LOAD_STATE"] >= 0.50
        for sample in trace.samples
    )
    assert any(
        sample.reproductive_event == "EXPULSION_REFERENCE_REQUEST"
        and sample.orgasm_reference_event == "ORGASM_REFERENCE_REQUEST"
        and sample.orgasm_reference_active
        and sample.coincident_ejaculatory_reference
        and _channels(sample)["EJACULATORY_REFLEX_STATE"] >= 0.50
        and _channels(sample)["EXPULSION_MOTOR_PATTERN_STATE"] >= 0.50
        and _channels(sample)[
            "EXTERNAL_URETHRAL_SPHINCTER_EJACULATORY_STATE"
        ] >= 0.50
        and _channels(sample)["ANTEGRADE_SEMINAL_FLOW_STATE"] >= 0.50
        for sample in trace.samples
    )
    assert any(
        sample.high_salience_phase == "DETUMESCENCE"
        and _channels(sample)["DETUMESCENCE_STATE"] > 0.0
        for sample in trace.samples
    )
    assert any(
        sample.stimulus_class == "RECOVERY_REFERENCE"
        and _channels(sample)["POST_EXPULSION_RECOVERY_STATE"] > 0.05
        for sample in trace.samples
    )
    assert any(
        sample.high_salience_phase in {"DETUMESCENCE", "BASELINE_RECOVERY"}
        and sample.reproductive_event == "RECOVERY_REFERENCE_REQUEST"
        for sample in trace.samples
    )

    final = trace.samples[-1]
    final_channels = _channels(final)
    assert final.orgasm_reference_active is False
    assert final.controller_activation < 0.10
    assert final.functional_motivation < 0.10
    assert final_channels["GENITAL_VASCULAR_STATE"] <= 0.15
    assert final_channels["ERECTILE_REFLEX_STATE"] <= 0.15
    assert final_channels["EMISSION_REFLEX_STATE"] <= 0.10
    assert final_channels["EJACULATORY_REFLEX_STATE"] <= 0.10
    assert final_channels["EXPULSION_MOTOR_PATTERN_STATE"] <= 0.10
    assert final_channels["DETUMESCENCE_STATE"] <= 0.10
    assert final_channels["BLADDER_NECK_EJACULATORY_CLOSURE_STATE"] <= 0.10
    assert final_channels["SEMINAL_TRACT_TRANSPORT_STATE"] <= 0.10
    assert final_channels["ACCESSORY_GLAND_SECRETION_STATE"] <= 0.10
    assert final_channels["POSTERIOR_URETHRAL_SEMINAL_LOAD_STATE"] <= 0.10
    assert final_channels[
        "EXTERNAL_URETHRAL_SPHINCTER_EJACULATORY_STATE"
    ] <= 0.10
    assert final_channels["ANTEGRADE_SEMINAL_FLOW_STATE"] <= 0.10
    assert final_channels["POST_EXPULSION_RECOVERY_STATE"] <= 0.10


def test_trace_preserves_contiguous_time_and_hash_provenance() -> None:
    trace = run_teacher_intimate_reference_trace(
        runtime_id="RUNTIME-TRACE-PROVENANCE",
        session_id="SESSION-TRACE-PROVENANCE",
    )

    assert [sample.sequence for sample in trace.samples] == list(
        range(len(trace.samples))
    )
    timestamps = [sample.timestamp_ms for sample in trace.samples]
    assert timestamps[0] == 0
    assert all(
        current - previous == 100
        for previous, current in zip(timestamps, timestamps[1:])
    )
    assert len({sample.sample_sha256 for sample in trace.samples}) == len(
        trace.samples
    )
    assert all(len(sample.source_controller_sha256) == 64 for sample in trace.samples)
    assert all(len(sample.source_body_state_sha256) == 64 for sample in trace.samples)


def test_orgasm_reference_is_tick_local_and_does_not_persist_into_recovery() -> None:
    trace = run_teacher_intimate_reference_trace(
        runtime_id="RUNTIME-ORGASM-TICK-LOCAL",
        session_id="SESSION-ORGASM-TICK-LOCAL",
    )

    orgasm_samples = [
        sample for sample in trace.samples if sample.orgasm_reference_active
    ]
    assert orgasm_samples
    assert all(
        sample.orgasm_reference_event == "ORGASM_REFERENCE_REQUEST"
        for sample in orgasm_samples
    )

    recovery_samples = [
        sample
        for sample in trace.samples
        if sample.stimulus_class == "RECOVERY_REFERENCE"
    ]
    assert recovery_samples
    assert all(not sample.orgasm_reference_active for sample in recovery_samples)


def test_trace_remains_reference_only_without_physical_or_subjective_claims() -> None:
    trace = run_teacher_intimate_reference_trace(
        runtime_id="RUNTIME-TRACE-BOUNDARY",
        session_id="SESSION-TRACE-BOUNDARY",
    )

    assert trace.physical_body_claim == "NONE"
    assert trace.subjective_desire_status == "NOT_ESTABLISHED"
    assert trace.subjective_orgasm_status == "NOT_ESTABLISHED"
    assert trace.subjectivity_status == "NOT_ESTABLISHED"
    assert trace.canonical_effect == "NONE"
    assert trace.deployment is False
    assert all(sample.physical_observation_claim == "NONE" for sample in trace.samples)
    assert all(
        sample.subjective_experience_status == "NOT_ESTABLISHED"
        for sample in trace.samples
    )


def test_trace_exposes_integrated_systemic_reproductive_and_endocrine_observability() -> None:
    trace = run_teacher_intimate_reference_trace(
        runtime_id="RUNTIME-TRACE-COMPLETE-OBSERVABILITY",
        session_id="SESSION-TRACE-COMPLETE-OBSERVABILITY",
    )

    required = {
        "CARDIOVASCULAR_STATE",
        "RESPIRATORY_STATE",
        "AUTONOMIC_SYMPATHETIC_STATE",
        "AUTONOMIC_PARASYMPATHETIC_STATE",
        "GENITAL_SENSORY_AFFERENT_REFERENCE",
        "GENITAL_VASCULAR_STATE",
        "ERECTILE_REFLEX_STATE",
        "PELVIC_FLOOR_PROPRIOCEPTION",
        "EMISSION_REFLEX_STATE",
        "SEMINAL_TRACT_TRANSPORT_STATE",
        "ACCESSORY_GLAND_SECRETION_STATE",
        "BLADDER_NECK_EJACULATORY_CLOSURE_STATE",
        "POSTERIOR_URETHRAL_SEMINAL_LOAD_STATE",
        "EJACULATORY_REFLEX_STATE",
        "EXPULSION_MOTOR_PATTERN_STATE",
        "EXTERNAL_URETHRAL_SPHINCTER_EJACULATORY_STATE",
        "ANTEGRADE_SEMINAL_FLOW_STATE",
        "POST_EXPULSION_RECOVERY_STATE",
        "DETUMESCENCE_STATE",
        "ENDOCRINE_REFERENCE_STATE",
        "GONADAL_ENDOCRINE_REFERENCE",
    }

    for sample in trace.samples:
        channels = _channels(sample)
        assert required.issubset(channels)
        assert all(0.0 <= channels[channel_id] <= 1.0 for channel_id in required)
