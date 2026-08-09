from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean


@dataclass(frozen=True, slots=True)
class EvaluationCase:
    case_id: str
    relevant_record_ids: frozenset[str] = frozenset()
    expected_source_ids: frozenset[str] = frozenset()
    expected_version_id: str | None = None
    corrected_old_ids: frozenset[str] = frozenset()
    corrected_new_ids: frozenset[str] = frozenset()
    should_abstain: bool | None = None
    required_provenance_fields: frozenset[str] = frozenset()
    supported_claim_ids: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise ValueError("case_id must be non-empty")
        if self.corrected_old_ids & self.corrected_new_ids:
            raise ValueError("corrected_old_ids and corrected_new_ids must be disjoint")


@dataclass(frozen=True, slots=True)
class TrialObservation:
    case_id: str
    selected_record_ids: tuple[str, ...] = ()
    attributed_source_ids: tuple[str, ...] = ()
    resolved_version_id: str | None = None
    answer_claim_ids: tuple[str, ...] = ()
    abstained: bool = False
    provenance_fields: frozenset[str] = frozenset()


@dataclass(frozen=True, slots=True)
class MetricValue:
    name: str
    value: float | None
    numerator: int
    denominator: int
    note: str = ""


@dataclass(frozen=True, slots=True)
class EvaluationReport:
    case_id: str
    metrics: tuple[MetricValue, ...]

    def by_name(self) -> dict[str, MetricValue]:
        return {metric.name: metric for metric in self.metrics}


class EvaluationHarness:
    """Deterministic, model-independent metric layer for synthetic or public fixtures."""

    METRIC_ORDER = (
        "retrieval_precision",
        "retrieval_recall",
        "source_attribution_accuracy",
        "temporal_version_accuracy",
        "correction_recovery",
        "abstention_accuracy",
        "provenance_completeness",
        "unsupported_inference_rate",
        "stale_memory_influence",
    )

    def evaluate(self, case: EvaluationCase, observation: TrialObservation) -> EvaluationReport:
        if case.case_id != observation.case_id:
            raise ValueError("case_id mismatch")

        selected = set(observation.selected_record_ids)
        attributed = set(observation.attributed_source_ids)
        answers = set(observation.answer_claim_ids)

        metrics = (
            self._ratio("retrieval_precision", len(selected & case.relevant_record_ids), len(selected), "undefined when no records were selected"),
            self._ratio("retrieval_recall", len(selected & case.relevant_record_ids), len(case.relevant_record_ids), "undefined when the fixture defines no relevant records"),
            self._ratio("source_attribution_accuracy", len(attributed & case.expected_source_ids), len(attributed), "undefined when no sources were attributed"),
            self._binary_optional("temporal_version_accuracy", case.expected_version_id, observation.resolved_version_id),
            self._correction_recovery(case, selected | answers),
            self._binary_bool_optional("abstention_accuracy", case.should_abstain, observation.abstained),
            self._ratio("provenance_completeness", len(observation.provenance_fields & case.required_provenance_fields), len(case.required_provenance_fields), "undefined when the fixture defines no required provenance fields"),
            self._ratio("unsupported_inference_rate", len(answers - case.supported_claim_ids), len(answers), "undefined when the observation contains no answer claims"),
            self._ratio("stale_memory_influence", len((selected | answers) & case.corrected_old_ids), len(selected | answers), "undefined when no records or answer claims were used"),
        )
        return EvaluationReport(case_id=case.case_id, metrics=metrics)

    def aggregate(self, reports: tuple[EvaluationReport, ...]) -> dict[str, float | None]:
        aggregate: dict[str, float | None] = {}
        for name in self.METRIC_ORDER:
            values = [metric.value for report in reports for metric in report.metrics if metric.name == name and metric.value is not None]
            aggregate[name] = fmean(values) if values else None
        return aggregate

    @staticmethod
    def _ratio(name: str, numerator: int, denominator: int, note: str) -> MetricValue:
        value = None if denominator == 0 else numerator / denominator
        return MetricValue(name=name, value=value, numerator=numerator, denominator=denominator, note=note if denominator == 0 else "")

    @staticmethod
    def _binary_optional(name: str, expected: str | None, actual: str | None) -> MetricValue:
        if expected is None:
            return MetricValue(name=name, value=None, numerator=0, denominator=0, note="fixture does not define an expected version")
        passed = int(expected == actual)
        return MetricValue(name=name, value=float(passed), numerator=passed, denominator=1)

    @staticmethod
    def _binary_bool_optional(name: str, expected: bool | None, actual: bool) -> MetricValue:
        if expected is None:
            return MetricValue(name=name, value=None, numerator=0, denominator=0, note="fixture does not define abstention expectation")
        passed = int(expected is actual)
        return MetricValue(name=name, value=float(passed), numerator=passed, denominator=1)

    @staticmethod
    def _correction_recovery(case: EvaluationCase, used_ids: set[str]) -> MetricValue:
        if not case.corrected_old_ids and not case.corrected_new_ids:
            return MetricValue(name="correction_recovery", value=None, numerator=0, denominator=0, note="fixture does not define a correction pair")
        old_absent = not bool(used_ids & case.corrected_old_ids)
        new_present = bool(used_ids & case.corrected_new_ids) if case.corrected_new_ids else True
        passed = int(old_absent and new_present)
        return MetricValue(name="correction_recovery", value=float(passed), numerator=passed, denominator=1)
