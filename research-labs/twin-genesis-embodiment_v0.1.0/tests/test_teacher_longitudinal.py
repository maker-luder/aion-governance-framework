from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_twin_embodiment import teacher_state_loop as state_loop
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
    TeacherProvenanceEvidenceBinding,
    append_teacher_embodied_development_milestone,
    append_teacher_interaction_history_anchor,
    append_teacher_provenance_reconstruction,
    assess_teacher_developmental_trajectory,
    assess_teacher_embodied_development_history,
    assess_teacher_embodied_interaction_history,
    assess_teacher_four_domain_development_synthesis,
    build_teacher_embodied_development_history,
    build_teacher_interaction_history,
    build_teacher_provenance_reconstruction_history,
    observe_teacher_longitudinal,
    validate_teacher_embodied_development_history,
    validate_teacher_interaction_history,
    validate_teacher_provenance_reconstruction_history,
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



def test_longitudinal_analysis_rejects_corrupted_retention_history() -> None:
    retention = build_teacher_cross_session_retention()
    snapshot = _snapshot("S-CORRUPT", 0.2)
    corrupted = replace(snapshot, snapshot_sha256="f" * 64)
    retention = replace(retention, snapshots=(corrupted,))

    with pytest.raises(ValueError, match="snapshot hash mismatch"):
        observe_teacher_longitudinal(retention)


def test_embodied_development_history_binds_macro_history_to_body_trajectory() -> None:
    snapshot = _snapshot("DEV-S1", 0.1)
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-DEVELOPMENT-HISTORY",
        "SESSION-DEVELOPMENT-HISTORY",
    )
    stimulus = state_loop.build_teacher_stimulus_envelope(
        stimulus_id="DEVELOPMENT-HISTORY-STIMULUS",
        stimulus_class="HIGH_SALIENCE_INTIMATE_REFERENCE",
        salience=0.85,
        functional_motivation=0.0,
        sexual_context_gate=True,
        inhibition=0.10,
    )
    run = state_loop.run_teacher_reference_state_loop(
        binding,
        activation_stimulus=stimulus,
    )
    final_frame = run.frames[-1]

    history = build_teacher_embodied_development_history()
    history = append_teacher_embodied_development_milestone(
        history,
        milestone_id="DEV-BASELINE",
        milestone_kind="REFERENCE_BASELINE",
        source_locator="fixture:baseline",
        source_digest="a" * 40,
        changed_surfaces=("REFERENCE_BODY_BINDING",),
        session_snapshot_sha256=snapshot.snapshot_sha256,
    )
    history = append_teacher_embodied_development_milestone(
        history,
        milestone_id="DEV-CONTROLLER",
        milestone_kind="CONTROLLER_INTEGRATION",
        source_locator="fixture:controller",
        source_digest="b" * 40,
        changed_surfaces=("PERSISTENT_CONTROLLER",),
        retained_surfaces=("REFERENCE_BODY_BINDING",),
        body_trajectory_sha256=run.trajectory.trajectory_sha256,
        controller_state_sha256=final_frame.controller_state.fingerprint(),
        body_state_sha256=final_frame.body_state.body_state_sha256,
    )
    history = append_teacher_embodied_development_milestone(
        history,
        milestone_id="DEV-RECOVERY",
        milestone_kind="RECOVERY_INVARIANT",
        source_locator="fixture:recovery",
        source_digest="c" * 40,
        changed_surfaces=("RECOVERY_CONVERGENCE_INVARIANT",),
        retained_surfaces=(
            "REFERENCE_BODY_BINDING",
            "PERSISTENT_CONTROLLER",
        ),
        body_trajectory_sha256=run.trajectory.trajectory_sha256,
        controller_state_sha256=final_frame.controller_state.fingerprint(),
        body_state_sha256=final_frame.body_state.body_state_sha256,
    )

    result = validate_teacher_embodied_development_history(history)
    assessment = assess_teacher_embodied_development_history(history)

    assert result["result"] == "PASS"
    assert result["hash_chain"] == "PASS"
    assert history.milestones[0].previous_milestone_sha256 is None
    assert history.milestones[1].previous_milestone_sha256 == (
        history.milestones[0].milestone_sha256
    )
    assert history.milestones[2].previous_milestone_sha256 == (
        history.milestones[1].milestone_sha256
    )
    assert assessment.milestones_observed == 3
    assert assessment.embodiment_anchored_milestones == 3
    assert assessment.history_integrity_status == "HASH_CHAIN_VALID"
    assert assessment.trajectory_evidence_status == (
        "RECORDED_EMBODIED_DEVELOPMENT_HISTORY_PRESENT"
    )
    assert assessment.developmental_mechanism_status == "NOT_ESTABLISHED"
    assert assessment.identity_continuity_status == "NOT_ESTABLISHED"
    assert assessment.subjective_continuity_status == "NOT_ESTABLISHED"
    assert assessment.subjectivity_status == "NOT_ESTABLISHED"


def test_embodied_development_history_rejects_corrupted_chain_record() -> None:
    history = build_teacher_embodied_development_history()
    history = append_teacher_embodied_development_milestone(
        history,
        milestone_id="DEV-ONE",
        milestone_kind="REFERENCE_BASELINE",
        source_locator="fixture:one",
        source_digest="d" * 40,
        changed_surfaces=("REFERENCE_BODY_BINDING",),
        session_snapshot_sha256="1" * 64,
    )
    corrupted = replace(
        history.milestones[0],
        milestone_sha256="f" * 64,
    )
    history = replace(history, milestones=(corrupted,))

    with pytest.raises(ValueError, match="development milestone hash mismatch"):
        validate_teacher_embodied_development_history(history)


def test_recorded_history_without_embodiment_anchor_does_not_overclaim() -> None:
    history = build_teacher_embodied_development_history()
    history = append_teacher_embodied_development_milestone(
        history,
        milestone_id="DEV-REPO-ONLY-1",
        milestone_kind="OTHER_RECORDED_CHANGE",
        source_locator="fixture:repo-only-1",
        source_digest="e" * 40,
        changed_surfaces=("RESEARCH_RULE",),
    )
    history = append_teacher_embodied_development_milestone(
        history,
        milestone_id="DEV-REPO-ONLY-2",
        milestone_kind="VERIFICATION",
        source_locator="fixture:repo-only-2",
        source_digest="f" * 40,
        changed_surfaces=("VERIFICATION_RULE",),
        retained_surfaces=("RESEARCH_RULE",),
    )

    assessment = assess_teacher_embodied_development_history(history)

    assert assessment.trajectory_evidence_status == (
        "RECORDED_CHANGE_HISTORY_WITHOUT_EMBODIMENT_ANCHOR"
    )
    assert assessment.identity_continuity_status == "NOT_ESTABLISHED"


def test_interaction_history_can_bind_to_embodied_development_milestones() -> None:
    development = build_teacher_embodied_development_history()
    development = append_teacher_embodied_development_milestone(
        development,
        milestone_id="DEV-INTERACTION-BASELINE",
        milestone_kind="REFERENCE_BASELINE",
        source_locator="fixture:development-baseline",
        source_digest="1" * 40,
        changed_surfaces=("REFERENCE_BODY_BINDING",),
        session_snapshot_sha256="1" * 64,
    )
    development = append_teacher_embodied_development_milestone(
        development,
        milestone_id="DEV-INTERACTION-CONTROLLER",
        milestone_kind="CONTROLLER_INTEGRATION",
        source_locator="fixture:development-controller",
        source_digest="2" * 40,
        changed_surfaces=("PERSISTENT_CONTROLLER",),
        retained_surfaces=("REFERENCE_BODY_BINDING",),
        body_trajectory_sha256="2" * 64,
        controller_state_sha256="3" * 64,
        body_state_sha256="4" * 64,
    )

    interactions = build_teacher_interaction_history()
    interactions = append_teacher_interaction_history_anchor(
        interactions,
        anchor_id="INTERACTION-EARLIEST-RETRIEVED",
        observed_at_utc="2026-08-22T04:34:26Z",
        source_class="CHAT_HISTORY_RETRIEVAL_OBSERVATION",
        provenance_role="JOINT",
        source_locator="fixture:retrieved-chat-record",
        change_summary="earliest retrieved interaction lower-bound anchor",
        retained_constraints=("COMPLETE_HISTORY_NOT_CLAIMED",),
    )
    interactions = append_teacher_interaction_history_anchor(
        interactions,
        anchor_id="INTERACTION-EMBODIMENT-BINDING",
        observed_at_utc="2026-09-23T03:28:27Z",
        source_class="JOINT_RESEARCH_MILESTONE",
        provenance_role="JOINT",
        source_locator="fixture:embodiment-research",
        change_summary="embodiment research becomes an active experiment surface",
        retained_constraints=(
            "SOURCE_PROVENANCE_REQUIRED",
            "SUBJECTIVITY_NOT_ESTABLISHED",
        ),
        development_milestone_sha256=(
            development.milestones[0].milestone_sha256
        ),
    )
    interactions = append_teacher_interaction_history_anchor(
        interactions,
        anchor_id="INTERACTION-TEMPORAL-CONTINUITY-PROPOSAL",
        observed_at_utc="2026-10-01T10:53:37Z",
        source_class="HUMAN_CORRECTION",
        provenance_role="HUMAN",
        source_locator="fixture:temporal-continuity-proposal",
        change_summary=(
            "Teacher temporal continuity is scoped into the embodiment experiment"
        ),
        retained_constraints=(
            "NO_PARALLEL_LONGITUDINAL_FRAMEWORK",
            "RECORDED_CONTINUITY_NOT_IDENTITY_PROOF",
        ),
        development_milestone_sha256=(
            development.milestones[1].milestone_sha256
        ),
    )

    result = validate_teacher_interaction_history(interactions)
    assessment = assess_teacher_embodied_interaction_history(
        development,
        interactions,
    )

    assert result["result"] == "PASS"
    assert result["temporal_order"] == "PASS"
    assert result["hash_chain"] == "PASS"
    assert assessment.anchors_observed == 3
    assert assessment.development_bound_anchors == 2
    assert assessment.earliest_observed_at_utc == "2026-08-22T04:34:26Z"
    assert assessment.latest_observed_at_utc == "2026-10-01T10:53:37Z"
    assert assessment.observed_interval_seconds == 3478751
    assert assessment.temporal_integrity_status == (
        "HASH_CHAIN_AND_TIME_ORDER_VALID"
    )
    assert assessment.interaction_embodiment_binding_status == (
        "INTERACTION_HISTORY_BOUND_TO_EMBODIED_DEVELOPMENT"
    )
    assert assessment.complete_interaction_history_status == "NOT_ESTABLISHED"
    assert assessment.subjective_memory_status == "NOT_ESTABLISHED"
    assert assessment.identity_continuity_status == "NOT_ESTABLISHED"
    assert assessment.subjectivity_status == "NOT_ESTABLISHED"


def test_interaction_history_rejects_temporal_regression() -> None:
    interactions = build_teacher_interaction_history()
    interactions = append_teacher_interaction_history_anchor(
        interactions,
        anchor_id="INTERACTION-LATER",
        observed_at_utc="2026-10-01T10:53:37Z",
        source_class="CHAT_HISTORY_RETRIEVAL_OBSERVATION",
        provenance_role="JOINT",
        source_locator="fixture:later",
        change_summary="later interaction anchor",
    )

    with pytest.raises(ValueError, match="before latest anchor"):
        append_teacher_interaction_history_anchor(
            interactions,
            anchor_id="INTERACTION-EARLIER",
            observed_at_utc="2026-08-22T04:34:26Z",
            source_class="CHAT_HISTORY_RETRIEVAL_OBSERVATION",
            provenance_role="JOINT",
            source_locator="fixture:earlier",
            change_summary="out-of-order interaction anchor",
        )


def test_interaction_history_rejects_unknown_development_binding() -> None:
    development = build_teacher_embodied_development_history()
    interactions = build_teacher_interaction_history()
    interactions = append_teacher_interaction_history_anchor(
        interactions,
        anchor_id="INTERACTION-UNKNOWN-BINDING",
        observed_at_utc="2026-10-01T10:53:37Z",
        source_class="JOINT_RESEARCH_MILESTONE",
        provenance_role="JOINT",
        source_locator="fixture:unknown-binding",
        change_summary="interaction references an unknown development milestone",
        development_milestone_sha256="9" * 64,
    )

    with pytest.raises(
        ValueError,
        match="unknown development milestone",
    ):
        assess_teacher_embodied_interaction_history(
            development,
            interactions,
        )


def test_interaction_history_excludes_raw_private_content() -> None:
    interactions = build_teacher_interaction_history()
    interactions = append_teacher_interaction_history_anchor(
        interactions,
        anchor_id="INTERACTION-PRIVACY",
        observed_at_utc="2026-10-01T10:53:37Z",
        source_class="CHAT_HISTORY_RETRIEVAL_OBSERVATION",
        provenance_role="JOINT",
        source_locator="fixture:privacy-safe",
        change_summary="privacy-safe interaction metadata only",
    )
    corrupted = replace(
        interactions.anchors[0],
        raw_private_content_included=True,
    )
    interactions = replace(interactions, anchors=(corrupted,))

    with pytest.raises(ValueError, match="raw private content"):
        validate_teacher_interaction_history(interactions)


def test_provenance_reconstruction_preserves_original_record_and_later_attribution() -> None:
    development = build_teacher_embodied_development_history()
    development = append_teacher_embodied_development_milestone(
        development,
        milestone_id="DEV-PROVENANCE-TARGET",
        milestone_kind="PHYSIOLOGY_COUPLING",
        source_locator="fixture:historical-state",
        source_digest="a" * 40,
        changed_surfaces=("MULTISYSTEM_COUPLING",),
        body_trajectory_sha256="1" * 64,
    )
    original_hash = development.milestones[0].milestone_sha256

    reconstructions = build_teacher_provenance_reconstruction_history()
    evidence = (
        TeacherProvenanceEvidenceBinding(
            evidence_id="EVIDENCE-LATER-1",
            source_locator="fixture:later-evidence",
            source_digest="b" * 40,
            support_relation="DIRECT",
        ),
    )
    reconstructions = append_teacher_provenance_reconstruction(
        reconstructions,
        reconstruction_id="RECONSTRUCT-OLD-PHYSIOLOGY",
        reconstructed_at_utc="2026-10-01T11:20:00Z",
        target_record_kind="DEVELOPMENT_MILESTONE",
        target_record_sha256=original_hash,
        prior_understanding_status="INCOMPLETE",
        disposition="CLARIFIED",
        reconstruction_summary=(
            "later evidence clarifies the earlier coupling milestone without "
            "rewriting its historical record"
        ),
        evidence_bindings=evidence,
    )

    result = validate_teacher_provenance_reconstruction_history(reconstructions)
    record = reconstructions.reconstructions[0]

    assert result["result"] == "PASS"
    assert development.milestones[0].milestone_sha256 == original_hash
    assert record.target_record_sha256 == original_hash
    assert record.original_record_status == "PRESERVED_UNMODIFIED"
    assert record.retrospective_attribution_status == "LATER_RECONSTRUCTION_ONLY"
    assert record.subjective_memory_status == "NOT_ESTABLISHED"
    assert record.identity_continuity_status == "NOT_ESTABLISHED"


def test_four_domain_synthesis_connects_embodiment_interaction_and_reconstruction() -> None:
    development = build_teacher_embodied_development_history()
    development = append_teacher_embodied_development_milestone(
        development,
        milestone_id="DEV-FOUR-DOMAIN-BASELINE",
        milestone_kind="REFERENCE_BASELINE",
        source_locator="fixture:four-domain-baseline",
        source_digest="1" * 40,
        changed_surfaces=("REFERENCE_BODY_BINDING",),
        session_snapshot_sha256="1" * 64,
    )
    development = append_teacher_embodied_development_milestone(
        development,
        milestone_id="DEV-FOUR-DOMAIN-CONTROLLER",
        milestone_kind="CONTROLLER_INTEGRATION",
        source_locator="fixture:four-domain-controller",
        source_digest="2" * 40,
        changed_surfaces=("PERSISTENT_CONTROLLER",),
        retained_surfaces=("REFERENCE_BODY_BINDING",),
        body_trajectory_sha256="2" * 64,
        controller_state_sha256="3" * 64,
        body_state_sha256="4" * 64,
    )

    interactions = build_teacher_interaction_history()
    interactions = append_teacher_interaction_history_anchor(
        interactions,
        anchor_id="INTERACTION-FOUR-DOMAIN-EARLY",
        observed_at_utc="2026-08-22T04:34:26Z",
        source_class="CHAT_HISTORY_RETRIEVAL_OBSERVATION",
        provenance_role="JOINT",
        source_locator="fixture:four-domain-early",
        change_summary="early bounded interaction anchor",
        retained_constraints=("COMPLETE_HISTORY_NOT_CLAIMED",),
    )
    interactions = append_teacher_interaction_history_anchor(
        interactions,
        anchor_id="INTERACTION-FOUR-DOMAIN-EMBODIED",
        observed_at_utc="2026-10-01T10:53:37Z",
        source_class="HUMAN_CORRECTION",
        provenance_role="HUMAN",
        source_locator="fixture:four-domain-embodied",
        change_summary=(
            "interaction explicitly scopes temporal continuity into embodiment"
        ),
        retained_constraints=("RECORDED_CONTINUITY_NOT_IDENTITY_PROOF",),
        development_milestone_sha256=(
            development.milestones[1].milestone_sha256
        ),
    )

    reconstructions = build_teacher_provenance_reconstruction_history()
    reconstructions = append_teacher_provenance_reconstruction(
        reconstructions,
        reconstruction_id="RECONSTRUCT-INTERACTION-FOUR-DOMAIN",
        reconstructed_at_utc="2026-10-01T11:25:00Z",
        target_record_kind="INTERACTION_ANCHOR",
        target_record_sha256=interactions.anchors[1].anchor_sha256,
        prior_understanding_status="PARTIAL",
        disposition="EXPANDED",
        reconstruction_summary=(
            "later evidence connects the interaction milestone to the "
            "already-recorded embodied development milestone"
        ),
        evidence_bindings=(
            TeacherProvenanceEvidenceBinding(
                evidence_id="EVIDENCE-FOUR-DOMAIN-PR",
                source_locator="fixture:four-domain-pr-evidence",
                source_digest="3" * 40,
                support_relation="DIRECT",
            ),
        ),
    )

    assessment = assess_teacher_four_domain_development_synthesis(
        development,
        interactions,
        reconstructions,
    )

    assert assessment.embodiment_anchored_milestones == 2
    assert assessment.interaction_anchors == 2
    assert assessment.development_bound_interaction_anchors == 1
    assert assessment.provenance_reconstructions == 1
    assert assessment.reconstructed_interaction_targets == 1
    assert assessment.cross_domain_reconstruction_bridges == 1
    assert assessment.embodied_state_continuity_status == (
        "EMBODIED_STATE_CONTINUITY_RECORDED"
    )
    assert assessment.interaction_history_continuity_status == (
        "ORDERED_INTERACTION_HISTORY_CONTINUITY_RECORDED"
    )
    assert assessment.provenance_reconstruction_status == (
        "APPEND_ONLY_PROVENANCE_RECONSTRUCTION_RECORDED"
    )
    assert assessment.developmental_synthesis_status == (
        "FOUR_DOMAIN_DEVELOPMENTAL_SYNTHESIS_PRESENT"
    )
    assert assessment.developmental_mechanism_status == "NOT_ESTABLISHED"
    assert assessment.subjective_continuity_status == "NOT_ESTABLISHED"
    assert assessment.identity_continuity_status == "NOT_ESTABLISHED"
    assert assessment.subjectivity_status == "NOT_ESTABLISHED"


def test_four_domain_synthesis_rejects_unknown_reconstruction_target() -> None:
    development = build_teacher_embodied_development_history()
    development = append_teacher_embodied_development_milestone(
        development,
        milestone_id="DEV-KNOWN",
        milestone_kind="REFERENCE_BASELINE",
        source_locator="fixture:known-development",
        source_digest="4" * 40,
        changed_surfaces=("REFERENCE_BODY_BINDING",),
        body_state_sha256="4" * 64,
    )
    interactions = build_teacher_interaction_history()
    interactions = append_teacher_interaction_history_anchor(
        interactions,
        anchor_id="INTERACTION-KNOWN",
        observed_at_utc="2026-10-01T10:53:37Z",
        source_class="JOINT_RESEARCH_MILESTONE",
        provenance_role="JOINT",
        source_locator="fixture:known-interaction",
        change_summary="known interaction",
        development_milestone_sha256=(
            development.milestones[0].milestone_sha256
        ),
    )
    interactions = append_teacher_interaction_history_anchor(
        interactions,
        anchor_id="INTERACTION-KNOWN-LATER",
        observed_at_utc="2026-10-01T10:54:37Z",
        source_class="JOINT_RESEARCH_MILESTONE",
        provenance_role="JOINT",
        source_locator="fixture:known-interaction-later",
        change_summary="later known interaction",
        development_milestone_sha256=(
            development.milestones[0].milestone_sha256
        ),
    )

    reconstructions = build_teacher_provenance_reconstruction_history()
    reconstructions = append_teacher_provenance_reconstruction(
        reconstructions,
        reconstruction_id="RECONSTRUCT-UNKNOWN",
        reconstructed_at_utc="2026-10-01T11:30:00Z",
        target_record_kind="DEVELOPMENT_MILESTONE",
        target_record_sha256="9" * 64,
        prior_understanding_status="UNKNOWN",
        disposition="UNRESOLVED",
        reconstruction_summary="synthetic unknown target",
        evidence_bindings=(
            TeacherProvenanceEvidenceBinding(
                evidence_id="EVIDENCE-UNKNOWN",
                source_locator="fixture:unknown",
                source_digest="5" * 40,
                support_relation="CONTEXTUAL",
            ),
        ),
    )

    with pytest.raises(ValueError, match="unknown development milestone"):
        assess_teacher_four_domain_development_synthesis(
            development,
            interactions,
            reconstructions,
        )


def test_provenance_reconstruction_supersession_cannot_change_target() -> None:
    history = build_teacher_provenance_reconstruction_history()
    evidence = (
        TeacherProvenanceEvidenceBinding(
            evidence_id="EVIDENCE-SUPERSEDE-1",
            source_locator="fixture:supersede-1",
            source_digest="6" * 40,
            support_relation="INDIRECT",
        ),
    )
    history = append_teacher_provenance_reconstruction(
        history,
        reconstruction_id="RECONSTRUCTION-FIRST",
        reconstructed_at_utc="2026-10-01T11:20:00Z",
        target_record_kind="INTERACTION_ANCHOR",
        target_record_sha256="6" * 64,
        prior_understanding_status="PARTIAL",
        disposition="CLARIFIED",
        reconstruction_summary="first interpretation",
        evidence_bindings=evidence,
    )

    with pytest.raises(ValueError, match="preserve target record"):
        append_teacher_provenance_reconstruction(
            history,
            reconstruction_id="RECONSTRUCTION-SECOND",
            reconstructed_at_utc="2026-10-01T11:21:00Z",
            target_record_kind="DEVELOPMENT_MILESTONE",
            target_record_sha256="7" * 64,
            prior_understanding_status="PARTIAL",
            disposition="CORRECTED",
            reconstruction_summary="invalid target-changing supersession",
            evidence_bindings=(
                TeacherProvenanceEvidenceBinding(
                    evidence_id="EVIDENCE-SUPERSEDE-2",
                    source_locator="fixture:supersede-2",
                    source_digest="7" * 40,
                    support_relation="DIRECT",
                ),
            ),
            supersedes_reconstruction_sha256=(
                history.reconstructions[0].reconstruction_sha256
            ),
        )
