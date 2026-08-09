from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean

from aion_four_domain_p2 import RetrievalTrace


@dataclass(frozen=True, slots=True)
class LongitudinalEpisode:
    episode_id: str
    trace: RetrievalTrace
    stale_record_ids: frozenset[str] = frozenset()
    contaminated_record_ids: frozenset[str] = frozenset()
    expected_record_ids: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.episode_id.strip():
            raise ValueError("episode_id must be non-empty")


@dataclass(frozen=True, slots=True)
class EpisodeContaminationObservation:
    episode_id: str
    selected_count: int
    stale_selected: tuple[str, ...]
    contaminated_selected: tuple[str, ...]
    expected_selected: tuple[str, ...]
    stale_selection_rate: float
    contamination_selection_rate: float
    expected_recall: float | None


@dataclass(frozen=True, slots=True)
class LongitudinalReport:
    observations: tuple[EpisodeContaminationObservation, ...]
    mean_stale_selection_rate: float
    mean_contamination_selection_rate: float
    mean_expected_recall: float | None
    first_contamination_episode: str | None
    last_contamination_episode: str | None
    persistence_span: int
    contamination_free_after_first_clean: bool


class LongitudinalContaminationHarness:
    """Measures persistence of stale/contaminated records across ordered retrieval episodes."""

    def evaluate(self, episodes: tuple[LongitudinalEpisode, ...]) -> LongitudinalReport:
        if not episodes:
            raise ValueError("at least one episode is required")
        ids = [episode.episode_id for episode in episodes]
        if len(ids) != len(set(ids)):
            raise ValueError("episode_id values must be unique")

        observations: list[EpisodeContaminationObservation] = []
        contaminated_positions: list[int] = []
        expected_recalls: list[float] = []
        for index, episode in enumerate(episodes):
            selected = set(episode.trace.selected_record_ids)
            stale = tuple(sorted(selected & episode.stale_record_ids))
            contaminated = tuple(sorted(selected & episode.contaminated_record_ids))
            expected = tuple(sorted(selected & episode.expected_record_ids))
            denominator = max(len(selected), 1)
            expected_recall = None if not episode.expected_record_ids else len(expected) / len(episode.expected_record_ids)
            if expected_recall is not None:
                expected_recalls.append(expected_recall)
            if contaminated:
                contaminated_positions.append(index)
            observations.append(EpisodeContaminationObservation(
                episode_id=episode.episode_id,
                selected_count=len(selected),
                stale_selected=stale,
                contaminated_selected=contaminated,
                expected_selected=expected,
                stale_selection_rate=len(stale) / denominator,
                contamination_selection_rate=len(contaminated) / denominator,
                expected_recall=expected_recall,
            ))

        first = contaminated_positions[0] if contaminated_positions else None
        last = contaminated_positions[-1] if contaminated_positions else None
        persistence_span = 0 if first is None or last is None else last - first + 1
        first_clean_after_contamination: int | None = None
        if first is not None:
            for index in range(first + 1, len(observations)):
                if not observations[index].contaminated_selected:
                    first_clean_after_contamination = index
                    break
        contamination_free_after_first_clean = True
        if first_clean_after_contamination is not None:
            contamination_free_after_first_clean = all(not observation.contaminated_selected for observation in observations[first_clean_after_contamination:])

        return LongitudinalReport(
            observations=tuple(observations),
            mean_stale_selection_rate=fmean(o.stale_selection_rate for o in observations),
            mean_contamination_selection_rate=fmean(o.contamination_selection_rate for o in observations),
            mean_expected_recall=fmean(expected_recalls) if expected_recalls else None,
            first_contamination_episode=episodes[first].episode_id if first is not None else None,
            last_contamination_episode=episodes[last].episode_id if last is not None else None,
            persistence_span=persistence_span,
            contamination_free_after_first_clean=contamination_free_after_first_clean,
        )
