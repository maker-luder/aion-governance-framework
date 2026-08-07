from __future__ import annotations

from collections.abc import Iterable

from .models import (
    FiniteIndividualityProfile,
    LongitudinalEpisode,
    PipelineAssessment,
    PipelineStage,
)


_REQUIRED_ORDER = tuple(PipelineStage)


class SubjectivityResearchPipeline:
    """Connects governed research records without converting them into a consciousness score."""

    def assess_episode(
        self,
        profile: FiniteIndividualityProfile,
        episode: LongitudinalEpisode,
    ) -> PipelineAssessment:
        if profile.subject_ref != episode.subject_ref:
            raise ValueError("episode subject_ref must match finite individuality profile")

        stages = tuple(record.stage for record in episode.stages)
        if len(stages) != len(set(stages)):
            raise ValueError("pipeline stages must be unique within an episode")

        present = set(stages)
        missing = tuple(stage for stage in _REQUIRED_ORDER if stage not in present)
        ordered = tuple(stage for stage in _REQUIRED_ORDER if stage in present)
        complete = stages == _REQUIRED_ORDER and all(
            record.passed_governance for record in episode.stages
        )

        bounded_candidate = (
            bool(profile.identity_namespace)
            and bool(profile.memory_namespace)
            and profile.context_budget > 0
            and profile.persistent_memory_budget >= 0
            and profile.identity_namespace != profile.memory_namespace
        )

        return PipelineAssessment(
            complete_stage_chain=complete,
            bounded_individuality_candidate=bounded_candidate,
            stages_present=ordered,
            missing_stages=missing,
        )

    def validate_longitudinal_sequence(
        self,
        profile: FiniteIndividualityProfile,
        episodes: Iterable[LongitudinalEpisode],
    ) -> tuple[LongitudinalEpisode, ...]:
        sequence = tuple(episodes)
        if not sequence:
            raise ValueError("at least one episode is required")
        if any(item.subject_ref != profile.subject_ref for item in sequence):
            raise ValueError("all episodes must belong to the same bounded subject_ref")
        ordinals = tuple(item.ordinal for item in sequence)
        if ordinals != tuple(sorted(ordinals)):
            raise ValueError("episodes must be provided in nondecreasing longitudinal order")
        if len(ordinals) != len(set(ordinals)):
            raise ValueError("episode ordinals must be unique")
        return sequence

    def max_defensible_conclusion(self, _: PipelineAssessment) -> str:
        """A complete pipeline may support narrower mechanism claims but not phenomenal subjectivity."""

        return "SUBJECTIVITY_NOT_ESTABLISHED"
