from __future__ import annotations

from dataclasses import replace
from pathlib import Path

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
    TeacherDevelopmentalHumanSeed,
    TeacherProvenanceEvidenceBinding,
    append_teacher_embodied_development_milestone,
    append_teacher_interaction_history_anchor,
    append_teacher_provenance_reconstruction,
    assess_teacher_developmental_trajectory,
    assess_teacher_embodied_development_history,
    assess_teacher_embodied_interaction_history,
    assess_teacher_four_domain_development_synthesis,
    build_human_inspired_teacher_development_experiment_matrix,
    build_teacher_developmental_embodiment_run,
    build_teacher_stitched_developmental_trajectory,
    build_teacher_embodied_development_history,
    build_teacher_interaction_history,
    build_teacher_provenance_reconstruction_history,
    observe_teacher_longitudinal,
    run_repeated_teacher_developmental_trials,
    validate_teacher_developmental_embodiment_experiment_matrix,
    validate_teacher_developmental_embodiment_run,
    validate_teacher_embodied_development_history,
    validate_teacher_interaction_history,
    validate_teacher_provenance_reconstruction_history,
)



# #261 TEST MAP / #261 測試完整中文對照
#
# English: These tests are executable evidence for PR #261. The fixture below uses
# synthetic values unrelated to the Human runtime seed, so public tests do not persist
# personal measurements.
# 繁中：以下測試是 #261 的可執行證據。測試 fixture（固定測試資料）使用與本人無關的
# 合成數值，因此公開測試不會保存個人的身高、體重或私人互動內容。
#
# _synthetic_development_seed
#   = 建立測試專用合成參照：童年 101–109 cm / 24 kg，成人 178 cm / 72 kg。
#     這些數字只是測試資料，不代表任何人的真實歷史。
#
# Development-history tests / 發展歷史測試
# test_embodied_development_history_binds_macro_history_to_body_trajectory
#   = 驗證宏觀歷史可綁定 body/controller 軌跡證據。
# test_embodied_development_history_rejects_corrupted_chain_record
#   = 人為破壞歷史雜湊鏈時，驗證器必須拒絕。
# test_recorded_history_without_embodiment_anchor_does_not_overclaim
#   = 只有歷史記錄、沒有具身錨點時，不得誇大成具身發展已建立。
#
# Interaction-history tests / 互動歷史測試
# test_interaction_history_can_bind_to_embodied_development_milestones
#   = 互動錨點可綁定存在的具身發展里程碑。
# test_interaction_history_rejects_temporal_regression
#   = 後一筆時間若早於前一筆，必須拒絕，避免歷史倒序。
# test_interaction_history_rejects_unknown_development_binding
#   = 指向不存在里程碑的互動綁定必須拒絕。
# test_interaction_history_excludes_raw_private_content
#   = 驗證資料模型不需要保存原始私人逐字聊天內容。
#
# Provenance-reconstruction tests / 來源重建測試
# test_provenance_reconstruction_preserves_original_record_and_later_attribution
#   = 後來的新證據只能新增「重新理解」紀錄，不能改寫當時的舊紀錄。
# test_four_domain_synthesis_connects_embodiment_interaction_and_reconstruction
#   = 驗證具身、互動、來源重建之間真的形成跨域橋接，而不是三份孤立資料。
# test_four_domain_synthesis_rejects_unknown_reconstruction_target
#   = 來源重建如果指向不存在的舊紀錄，必須拒絕。
# test_provenance_reconstruction_supersession_cannot_change_target
#   = 新解釋若 supersede（取代）舊解釋，不得偷偷改成另一個目標紀錄。
#
# Developmental-embodiment tests / 發展具身測試
# test_human_inspired_development_matrix_preserves_uncertainty_and_same_terminal_body
#   = 驗證五組路徑保留未知中間資料、共享相同成人終點，且歷史雜湊彼此不同。
# test_same_terminal_body_can_preserve_different_development_histories
#   = 驗證「現在身體相同」不會把「不同過去」洗成同一條歷史。
# test_curiosity_and_willingness_to_try_are_independently_manipulable
#   = 驗證「好奇」與「願意實際嘗試」是兩個可獨立控制的變數。
# test_social_change_is_recorded_without_rewriting_childhood_social_style
#   = 後來社交傾向改變時，童年原始社交紀錄仍需保留。
# test_developmental_run_rejects_child_stage_with_excluded_runtime_enabled
#   = #261 排除的 sexual/reproductive runtime 若被塞入童年階段，驗證器必須拒絕。
#     這是本 PR 的變數隔離測試，不是成人生理不存在的主張。
# test_developmental_run_hash_detects_path_change_with_same_terminal_state
#   = 即使終點完全相同，只要中途路徑改變，run SHA-256 就必須不同。
# test_childhood_to_current_path_is_stitched_without_inventing_middle_measurements
#   = 拼接童年→過渡→現在時，不得捏造過渡期身高／體重；缺資料就維持未知。
# test_repeated_childhood_to_current_trials_are_deterministically_reproducible
#   = 相同輸入重跑五次，檢查是否得到同一軌跡雜湊與相同終點。
# test_same_current_state_preserves_distinct_stitched_childhood_paths
#   = 兩條不同童年路徑可到達同一現在，但拼接後的歷史仍需保持不同。
# test_stitched_path_keeps_current_unknown_behavior_as_unresolved_not_inferred
#   = 現在行為程度若只知道「有變但未量化」，程式必須標未解，不可猜高／中／低。
#
def _synthetic_development_seed() -> TeacherDevelopmentalHumanSeed:
    return TeacherDevelopmentalHumanSeed(
        childhood_height_cm_min=101.0,
        childhood_height_cm_max=109.0,
        childhood_weight_kg_reference=24.0,
        current_height_cm=178.0,
        current_weight_kg_reference=72.0,
        childhood_activity_level="HIGH",
        childhood_curiosity_level="HIGH",
        childhood_willingness_to_try_level="HIGH",
        childhood_social_approach_level="LOW",
        current_activity_level="CHANGED_NOT_QUANTIFIED",
        current_curiosity_level="HIGH",
        current_willingness_to_try_level="HIGH",
        current_social_approach_level="CHANGED_NOT_QUANTIFIED",
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


def test_review_annotations_leave_tests_independently_collectable() -> None:
    # 中文審查：註解後須是真正換行，避免新測試被併入前一個函式。
    source = Path(__file__).read_text(encoding="utf-8")
    marker = chr(92) + "n" + "def test_"
    assert marker not in source


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


# 中文審查：確認具身里程碑真的綁到 body/controller 軌跡，而不是只有文字歷史。
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


# 中文審查：故意破壞雜湊鏈，系統必須抓到並拒絕。
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


# 中文審查：沒有具身證據時只能說「有歷史記錄」，不能誇大成具身發展成立。
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


# 中文審查：互動歷史可以指向確實存在的發展里程碑。
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


# 中文審查：時間不能倒退；後一筆比前一筆更早就必須失敗。
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


# 中文審查：互動不能綁定不存在的發展里程碑。
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


# 中文審查：資料模型不得依賴保存原始私人逐字內容。
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


# 中文審查：後來的修正要新增紀錄，不能回頭修改當時原始紀錄。
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


# 中文審查：四域整合必須真的有跨域連結，不能只因檔案都存在就算完成。
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


# 中文審查：來源重建若指向不存在的舊紀錄，必須拒絕。
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


# 中文審查：後續修正可取代前一解釋，但不能偷偷更換被解釋的目標。
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


# 中文審查：五組路徑保留未知資料，最後成人身體相同，但歷史仍可區分。
def test_human_inspired_development_matrix_preserves_uncertainty_and_same_terminal_body() -> None:
    matrix = build_human_inspired_teacher_development_experiment_matrix(_synthetic_development_seed())
    result = validate_teacher_developmental_embodiment_experiment_matrix(matrix)

    assert result["result"] == "PASS"
    assert len(matrix.runs) == 5
    assert result["same_terminal_body_reference"] == "PASS"
    assert result["distinct_history_hashes"] == "PASS"
    assert result["explicit_uncertainty"] == "PASS"

    childhood = matrix.runs[0].stages[0]
    transition = matrix.runs[0].stages[1]
    adult = matrix.runs[0].stages[-1]

    assert childhood.height_cm_min == 101.0
    assert childhood.height_cm_max == 109.0
    assert childhood.weight_kg_reference == 24.0
    assert childhood.anthropometry_precision == "APPROXIMATE_SELF_REPORT"
    assert childhood.age_status == "UNKNOWN"

    assert transition.height_cm_min is None
    assert transition.height_cm_max is None
    assert transition.weight_kg_reference is None
    assert transition.anthropometry_precision == "UNKNOWN"

    assert adult.height_cm_min == 178.0
    assert adult.height_cm_max == 178.0
    assert adult.weight_kg_reference == 72.0
    assert adult.anthropometry_precision == "CURRENT_SELF_REPORT"

    assert all(
        not stage.sexual_or_reproductive_runtime_included
        for run in matrix.runs
        for stage in run.stages
    )
    assert all(not run.canonical_teacher_anthropometry_modified for run in matrix.runs)

    point_control = next(run for run in matrix.runs if run.run_id == "DEV-RUN-E")
    point_child = point_control.stages[0]
    assert point_child.height_cm_min == 105.0
    assert point_child.height_cm_max == 105.0
    assert point_child.anthropometry_precision == (
        "SYNTHETIC_POINT_ESTIMATE_CONTROL"
    )
    assert point_child.height_cm_min != childhood.height_cm_min
    assert point_control.run_sha256 != matrix.runs[0].run_sha256


# 中文審查：相同現在身體，不代表過去歷史相同。
def test_same_terminal_body_can_preserve_different_development_histories() -> None:
    matrix = build_human_inspired_teacher_development_experiment_matrix(_synthetic_development_seed())
    high = next(run for run in matrix.runs if run.run_id == "DEV-RUN-A")
    low = next(run for run in matrix.runs if run.run_id == "DEV-RUN-B")

    assert high.stages[-1] == low.stages[-1]
    assert high.run_sha256 != low.run_sha256
    assert high.stages[0].curiosity_level == "HIGH"
    assert low.stages[0].curiosity_level == "LOW"
    assert high.stages[0].willingness_to_try_level == "HIGH"
    assert low.stages[0].willingness_to_try_level == "LOW"


# 中文審查：好奇與實際願意嘗試分開控制，避免把兩個概念混成一個。
def test_curiosity_and_willingness_to_try_are_independently_manipulable() -> None:
    matrix = build_human_inspired_teacher_development_experiment_matrix(_synthetic_development_seed())
    high = next(run for run in matrix.runs if run.run_id == "DEV-RUN-A")
    low_willingness = next(
        run for run in matrix.runs if run.run_id == "DEV-RUN-C"
    )

    assert high.stages[0].curiosity_level == "HIGH"
    assert low_willingness.stages[0].curiosity_level == "HIGH"
    assert high.stages[0].willingness_to_try_level == "HIGH"
    assert low_willingness.stages[0].willingness_to_try_level == "LOW"
    assert high.run_sha256 != low_willingness.run_sha256


# 中文審查：後來社交狀態變了，也不能回頭改寫童年原始社交紀錄。
def test_social_change_is_recorded_without_rewriting_childhood_social_style() -> None:
    matrix = build_human_inspired_teacher_development_experiment_matrix(_synthetic_development_seed())
    observed = next(run for run in matrix.runs if run.run_id == "DEV-RUN-A")
    control = next(run for run in matrix.runs if run.run_id == "DEV-RUN-D")

    assert observed.stages[0].social_approach_level == "LOW"
    assert observed.stages[1].social_approach_level == "CHANGED_NOT_QUANTIFIED"
    assert observed.stages[-1].social_approach_level == "CHANGED_NOT_QUANTIFIED"

    assert control.stages[0].social_approach_level == "MODERATE"
    assert control.stages[1].social_approach_level == "MODERATE"
    assert observed.run_sha256 != control.run_sha256


# 中文審查：#261 的童年發展實驗排除性／生殖 runtime；若誤開啟就必須拒絕。
def test_developmental_run_rejects_child_stage_with_excluded_runtime_enabled() -> None:
    matrix = build_human_inspired_teacher_development_experiment_matrix(_synthetic_development_seed())
    baseline = matrix.runs[0]
    unsafe_child = replace(
        baseline.stages[0],
        sexual_or_reproductive_runtime_included=True,
    )

    with pytest.raises(
        ValueError,
        match="excludes sexual/reproductive runtime",
    ):
        build_teacher_developmental_embodiment_run(
            run_id="DEV-RUN-INVALID",
            condition_id="INVALID_CHILD_SCOPE",
            stages=(unsafe_child,) + baseline.stages[1:],
        )


# 中文審查：只要中途路徑變了，即使終點相同，歷史雜湊也必須不同。
def test_developmental_run_hash_detects_path_change_with_same_terminal_state() -> None:
    matrix = build_human_inspired_teacher_development_experiment_matrix(_synthetic_development_seed())
    baseline = matrix.runs[0]
    changed_transition = replace(
        baseline.stages[1],
        stage_id="TRANSITION-ALTERED-PATH",
        curiosity_level="MODERATE",
    )
    altered = build_teacher_developmental_embodiment_run(
        run_id="DEV-RUN-ALTERED",
        condition_id="ALTERED_PATH_SAME_TERMINAL",
        stages=(baseline.stages[0], changed_transition, baseline.stages[-1]),
    )

    assert altered.stages[-1] == baseline.stages[-1]
    assert altered.run_sha256 != baseline.run_sha256
    assert validate_teacher_developmental_embodiment_run(altered)["result"] == "PASS"


# 中文審查：童年→過渡→現在可以拼接，但不得捏造中間身高體重。
def test_childhood_to_current_path_is_stitched_without_inventing_middle_measurements() -> None:
    matrix = build_human_inspired_teacher_development_experiment_matrix(
        _synthetic_development_seed()
    )
    observed = next(run for run in matrix.runs if run.run_id == "DEV-RUN-A")
    trajectory = build_teacher_stitched_developmental_trajectory(observed)

    assert trajectory.stage_ids == (
        "CHILD-HIGH-EXPLORATION",
        "TRANSITION-HIGH-EXPLORATION",
        "ADULT-CURRENT-COMMON",
    )
    assert len(trajectory.transitions) == 2
    assert trajectory.intermediate_anthropometry_interpolated is False
    assert all(
        transition.anthropometry_change_status == "PARTIALLY_UNRESOLVED"
        for transition in trajectory.transitions
    )
    assert trajectory.transitions[0].retained_behavior_fields == (
        "activity_level",
        "curiosity_level",
        "willingness_to_try_level",
    )
    assert trajectory.transitions[0].unresolved_behavior_fields == (
        "social_approach_level",
    )
    assert trajectory.transitions[1].unresolved_behavior_fields == (
        "activity_level",
        "social_approach_level",
    )
    assert trajectory.causal_development_claim == "NONE"
    assert trajectory.autobiographical_identity_claim == "NONE"
    assert trajectory.subjective_continuity_status == "NOT_ESTABLISHED"


# 中文審查：同一輸入重跑五次，驗證工程上的決定論式可重現性。
def test_repeated_childhood_to_current_trials_are_deterministically_reproducible() -> None:
    matrix = build_human_inspired_teacher_development_experiment_matrix(
        _synthetic_development_seed()
    )
    observed = next(run for run in matrix.runs if run.run_id == "DEV-RUN-A")

    assessment = run_repeated_teacher_developmental_trials(
        observed,
        repetitions=5,
    )

    assert assessment.repetitions == 5
    assert assessment.unique_trajectory_hashes == 1
    assert assessment.reproducibility_status == (
        "DETERMINISTIC_TRAJECTORY_REPRODUCED"
    )
    assert assessment.terminal_state_control_status == (
        "SAME_TERMINAL_STATE_CONFIRMED"
    )
    assert assessment.historical_path_status == (
        "CHILDHOOD_TO_CURRENT_PATH_RECORDED"
    )
    assert assessment.causal_interpretation_status == "NOT_ESTABLISHED"


# 中文審查：不同童年路徑即使到達同一現在，拼接歷史仍要保持不同。
def test_same_current_state_preserves_distinct_stitched_childhood_paths() -> None:
    matrix = build_human_inspired_teacher_development_experiment_matrix(
        _synthetic_development_seed()
    )
    high = next(run for run in matrix.runs if run.run_id == "DEV-RUN-A")
    low = next(run for run in matrix.runs if run.run_id == "DEV-RUN-B")

    high_path = build_teacher_stitched_developmental_trajectory(high)
    low_path = build_teacher_stitched_developmental_trajectory(low)

    assert high.stages[-1] == low.stages[-1]
    assert high_path.trajectory_sha256 != low_path.trajectory_sha256
    assert high_path.stage_ids != low_path.stage_ids


# 中文審查：不知道現在行為具體變成多少，就必須保留未解，不能自行推論。
def test_stitched_path_keeps_current_unknown_behavior_as_unresolved_not_inferred() -> None:
    seed = replace(
        _synthetic_development_seed(),
        current_curiosity_level="CHANGED_NOT_QUANTIFIED",
        current_willingness_to_try_level="CHANGED_NOT_QUANTIFIED",
    )
    matrix = build_human_inspired_teacher_development_experiment_matrix(seed)
    observed = next(run for run in matrix.runs if run.run_id == "DEV-RUN-A")
    trajectory = build_teacher_stitched_developmental_trajectory(observed)

    final_transition = trajectory.transitions[-1]
    assert "curiosity_level" in final_transition.unresolved_behavior_fields
    assert "willingness_to_try_level" in final_transition.unresolved_behavior_fields
    assert "curiosity_level" not in final_transition.changed_behavior_fields
    assert "willingness_to_try_level" not in final_transition.retained_behavior_fields
