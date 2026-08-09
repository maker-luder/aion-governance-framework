from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from statistics import fmean


def _bounded_bp(value: int | None, name: str) -> None:
    if value is not None and not 0 <= value <= 10_000:
        raise ValueError(f"{name} must be between 0 and 10000 basis points")


class Conclusion(str, Enum):
    SUPPORTS = "SUPPORTS"
    CHALLENGES = "CHALLENGES"
    FALSIFIES = "FALSIFIES"
    INCONCLUSIVE = "INCONCLUSIVE"


class DisagreementClass(str, Enum):
    CONSENSUS = "CONSENSUS"
    WEAK_DISAGREEMENT = "WEAK_DISAGREEMENT"
    STRUCTURED_DISAGREEMENT = "STRUCTURED_DISAGREEMENT"
    FUNDAMENTAL_DISAGREEMENT = "FUNDAMENTAL_DISAGREEMENT"


@dataclass(frozen=True, slots=True)
class AgentPosition:
    run_id: str
    runner_id: str
    hypothesis_id: str
    conclusion: Conclusion
    evidence_refs: tuple[str, ...]
    claim_refs: tuple[str, ...] = ()
    dimension_tags: tuple[str, ...] = ()
    confidence_bp: int | None = None

    def __post_init__(self) -> None:
        for name in ("run_id", "runner_id", "hypothesis_id"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        _bounded_bp(self.confidence_bp, "confidence_bp")
        if self.conclusion is not Conclusion.INCONCLUSIVE and not self.evidence_refs:
            raise ValueError("non-inconclusive positions require evidence_refs")


@dataclass(frozen=True, slots=True)
class DisagreementReport:
    hypothesis_id: str
    classification: DisagreementClass
    run_count: int
    runner_count: int
    conclusion_counts: tuple[tuple[str, int], ...]
    mean_pairwise_evidence_overlap: float
    evidence_union: tuple[str, ...]
    dimension_tags: tuple[str, ...]
    confidence_range_bp: tuple[int, int] | None
    minority_run_ids: tuple[str, ...]
    note: str


class CrossAgentDisagreementAnalyzer:
    """Deterministic disagreement analysis without semantic embedding or hidden adjudication."""

    def analyze(self, positions: tuple[AgentPosition, ...]) -> DisagreementReport:
        if len(positions) < 2:
            raise ValueError("at least two positions are required")
        hypothesis_ids = {item.hypothesis_id for item in positions}
        if len(hypothesis_ids) != 1:
            raise ValueError("all positions must address the same hypothesis")
        run_ids = [item.run_id for item in positions]
        if len(run_ids) != len(set(run_ids)):
            raise ValueError("run_id values must be unique")

        counts: dict[Conclusion, int] = {}
        for item in positions:
            counts[item.conclusion] = counts.get(item.conclusion, 0) + 1

        conclusions = set(counts)
        if len(conclusions) == 1:
            classification = DisagreementClass.CONSENSUS
            note = "All runs report the same explicit conclusion."
        elif Conclusion.SUPPORTS in conclusions and Conclusion.FALSIFIES in conclusions:
            classification = DisagreementClass.FUNDAMENTAL_DISAGREEMENT
            note = "At least one run supports and another falsifies the same hypothesis."
        elif conclusions <= {Conclusion.SUPPORTS, Conclusion.INCONCLUSIVE} or conclusions <= {
            Conclusion.FALSIFIES, Conclusion.INCONCLUSIVE
        }:
            classification = DisagreementClass.WEAK_DISAGREEMENT
            note = "Conclusions differ only by an inconclusive position."
        else:
            classification = DisagreementClass.STRUCTURED_DISAGREEMENT
            note = "Multiple substantive conclusion states are present."

        overlaps: list[float] = []
        for left, right in combinations(positions, 2):
            a, b = set(left.evidence_refs), set(right.evidence_refs)
            union = a | b
            overlaps.append(1.0 if not union else len(a & b) / len(union))

        max_count = max(counts.values())
        majority = {kind for kind, count in counts.items() if count == max_count}
        minority = tuple(sorted(item.run_id for item in positions if item.conclusion not in majority))

        confidences = [item.confidence_bp for item in positions if item.confidence_bp is not None]
        confidence_range = None if not confidences else (min(confidences), max(confidences))

        return DisagreementReport(
            hypothesis_id=next(iter(hypothesis_ids)),
            classification=classification,
            run_count=len(positions),
            runner_count=len({item.runner_id for item in positions}),
            conclusion_counts=tuple(sorted((kind.value, count) for kind, count in counts.items())),
            mean_pairwise_evidence_overlap=fmean(overlaps) if overlaps else 1.0,
            evidence_union=tuple(sorted({ref for item in positions for ref in item.evidence_refs})),
            dimension_tags=tuple(sorted({tag for item in positions for tag in item.dimension_tags})),
            confidence_range_bp=confidence_range,
            minority_run_ids=minority,
            note=note,
        )
