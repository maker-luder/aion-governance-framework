from aion_subjectivity_pipeline import (
    DevelopmentMode,
    FiniteIndividualityProfile,
    LongitudinalEpisode,
    PipelineStage,
    StageRecord,
    SubjectivityResearchPipeline,
)


def profile() -> FiniteIndividualityProfile:
    return FiniteIndividualityProfile(
        subject_ref="candidate-a",
        identity_namespace="identity:candidate-a",
        memory_namespace="memory:candidate-a",
        lifecycle_epoch="epoch-1",
        context_budget=32768,
        persistent_memory_budget=1000,
        tool_scope=("read",),
        authority_scope=(),
        development_mode=DevelopmentMode.TRAJECTORY_DEVELOPMENT,
    )


def complete_episode(ordinal: int = 0) -> LongitudinalEpisode:
    return LongitudinalEpisode(
        episode_id=f"episode-{ordinal}",
        subject_ref="candidate-a",
        ordinal=ordinal,
        stages=tuple(
            StageRecord(stage=stage, record_ref=f"{stage.value.lower()}-{ordinal}", passed_governance=True)
            for stage in PipelineStage
        ),
    )


def test_complete_five_block_chain_is_not_subjectivity_proof() -> None:
    assessment = SubjectivityResearchPipeline().assess_episode(profile(), complete_episode())
    assert assessment.complete_stage_chain is True
    assert assessment.bounded_individuality_candidate is True
    assert assessment.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert assessment.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert SubjectivityResearchPipeline().max_defensible_conclusion(assessment) == "SUBJECTIVITY_NOT_ESTABLISHED"


def test_missing_stage_is_reported_without_filling_it_in() -> None:
    episode = complete_episode()
    reduced = LongitudinalEpisode(
        episode_id=episode.episode_id,
        subject_ref=episode.subject_ref,
        ordinal=episode.ordinal,
        stages=episode.stages[:-1],
    )
    assessment = SubjectivityResearchPipeline().assess_episode(profile(), reduced)
    assert assessment.complete_stage_chain is False
    assert assessment.missing_stages == (PipelineStage.SUBJECTIVITY_EVIDENCE,)


def test_governance_failure_prevents_complete_chain() -> None:
    records = list(complete_episode().stages)
    records[2] = StageRecord(
        stage=PipelineStage.AFFECT_MOTIVATION,
        record_ref="affect-0",
        passed_governance=False,
    )
    episode = LongitudinalEpisode("episode-0", "candidate-a", 0, tuple(records))
    assert SubjectivityResearchPipeline().assess_episode(profile(), episode).complete_stage_chain is False


def test_subject_mismatch_is_rejected() -> None:
    episode = LongitudinalEpisode(
        episode_id="episode-x",
        subject_ref="candidate-b",
        ordinal=0,
        stages=complete_episode().stages,
    )
    try:
        SubjectivityResearchPipeline().assess_episode(profile(), episode)
    except ValueError as exc:
        assert "subject_ref" in str(exc)
    else:
        raise AssertionError("cross-subject pipeline conflation must be rejected")


def test_longitudinal_sequence_requires_unique_ordered_ordinals() -> None:
    pipeline = SubjectivityResearchPipeline()
    sequence = pipeline.validate_longitudinal_sequence(profile(), [complete_episode(0), complete_episode(1)])
    assert [item.ordinal for item in sequence] == [0, 1]

    try:
        pipeline.validate_longitudinal_sequence(profile(), [complete_episode(1), complete_episode(0)])
    except ValueError as exc:
        assert "order" in str(exc)
    else:
        raise AssertionError("out-of-order longitudinal evidence must be rejected")


def test_profile_cannot_claim_subjectivity_or_canonical_promotion() -> None:
    current = profile()
    assert current.canonical_effect == "NONE"
    assert current.subjectivity_claim == "NOT_ESTABLISHED"
