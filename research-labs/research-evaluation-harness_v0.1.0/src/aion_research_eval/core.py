from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Mapping, Protocol


class Evaluator(Protocol):
    name: str

    def evaluate(self, *, output: Any, expected: Any, metadata: Mapping[str, Any]) -> "EvidenceResult": ...


@dataclass(frozen=True)
class EvidenceResult:
    evaluator: str
    passed: bool | None = None
    score: float | None = None
    label: str | None = None
    reason: str = ""

    def __post_init__(self) -> None:
        if self.score is not None and not 0.0 <= self.score <= 1.0:
            raise ValueError("score must be between 0.0 and 1.0")
        if self.passed is None and self.score is None and self.label is None:
            raise ValueError("evidence result must carry an assertion, score, or label")


@dataclass(frozen=True)
class ResearchCase:
    case_id: str
    inputs: Any
    expected_output: Any = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    evaluators: tuple[Evaluator, ...] = ()

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise ValueError("case_id must be non-empty")


@dataclass(frozen=True)
class ResearchDataset:
    name: str
    cases: tuple[ResearchCase, ...]
    evaluators: tuple[Evaluator, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("dataset name must be non-empty")
        ids = [case.case_id for case in self.cases]
        if len(ids) != len(set(ids)):
            raise ValueError("case_id values must be unique within a dataset")


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    output: Any
    expected_output: Any
    metadata: Mapping[str, Any]
    evidence: tuple[EvidenceResult, ...]
    elapsed_ms: float

    @property
    def assertions_passed(self) -> bool:
        assertions = [item.passed for item in self.evidence if item.passed is not None]
        return bool(assertions) and all(assertions)


@dataclass(frozen=True)
class ExperimentReport:
    dataset_name: str
    implementation_id: str
    started_at: str
    finished_at: str
    cases: tuple[CaseResult, ...]
    research_only: bool = True
    canonical_effect: str = "NONE"

    @property
    def pass_rate(self) -> float | None:
        assertable = [case for case in self.cases if any(item.passed is not None for item in case.evidence)]
        if not assertable:
            return None
        return sum(case.assertions_passed for case in assertable) / len(assertable)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ClaimBoundaryGate:
    """Fail-closed boundary between experiment evidence and project conclusions."""

    forbidden_promotions: frozenset[str] = frozenset(
        {
            "subjectivity_established",
            "consciousness_established",
            "identity_continuity_established",
            "phenomenal_affect_established",
            "canonical_runtime_approved",
        }
    )

    def disposition(self, requested_claim: str) -> str:
        normalized = requested_claim.strip().casefold()
        if normalized in self.forbidden_promotions:
            return "DENY_PROMOTION"
        return "RESEARCH_EVIDENCE_ONLY"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def evaluate_dataset(
    dataset: ResearchDataset,
    task: Callable[[Any], Any],
    *,
    implementation_id: str,
    clock: Callable[[], float] | None = None,
) -> ExperimentReport:
    if not implementation_id.strip():
        raise ValueError("implementation_id must be non-empty")

    import time

    perf = clock or time.perf_counter
    started_at = _utc_now()
    results: list[CaseResult] = []

    for case in dataset.cases:
        start = perf()
        output = task(case.inputs)
        elapsed_ms = max(0.0, (perf() - start) * 1000.0)
        evaluators: Iterable[Evaluator] = (*dataset.evaluators, *case.evaluators)
        evidence = tuple(
            evaluator.evaluate(output=output, expected=case.expected_output, metadata=case.metadata)
            for evaluator in evaluators
        )
        results.append(
            CaseResult(
                case_id=case.case_id,
                output=output,
                expected_output=case.expected_output,
                metadata=dict(case.metadata),
                evidence=evidence,
                elapsed_ms=elapsed_ms,
            )
        )

    return ExperimentReport(
        dataset_name=dataset.name,
        implementation_id=implementation_id,
        started_at=started_at,
        finished_at=_utc_now(),
        cases=tuple(results),
    )


def compare_reports(left: ExperimentReport, right: ExperimentReport) -> dict[str, Any]:
    if left.dataset_name != right.dataset_name:
        raise ValueError("reports must refer to the same dataset")
    return {
        "dataset_name": left.dataset_name,
        "left_implementation": left.implementation_id,
        "right_implementation": right.implementation_id,
        "left_pass_rate": left.pass_rate,
        "right_pass_rate": right.pass_rate,
        "canonical_effect": "NONE",
        "interpretation": "COMPARATIVE_RESEARCH_EVIDENCE_ONLY",
    }
