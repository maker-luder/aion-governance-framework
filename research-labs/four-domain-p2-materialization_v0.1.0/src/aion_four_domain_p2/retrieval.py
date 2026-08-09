from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import hashlib
import json


def _require_aware(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")


def _bounded_basis_points(value: int, field_name: str) -> None:
    if not 0 <= value <= 10_000:
        raise ValueError(f"{field_name} must be between 0 and 10000 basis points")


class ExclusionReason(str, Enum):
    SUBJECT_MISMATCH = "SUBJECT_MISMATCH"
    NAMESPACE_MISMATCH = "NAMESPACE_MISMATCH"
    FUTURE_RECORD = "FUTURE_RECORD"
    TOMBSTONED = "TOMBSTONED"
    SUPERSEDED = "SUPERSEDED"
    WITHDRAWN = "WITHDRAWN"
    CONFLICT = "CONFLICT"
    PROVENANCE_GATE_FAILED = "PROVENANCE_GATE_FAILED"
    MAX_RECORDS_REACHED = "MAX_RECORDS_REACHED"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"


@dataclass(frozen=True, slots=True)
class RankingWeights:
    relevance: int = 60
    temporal: int = 25
    priority: int = 15

    def __post_init__(self) -> None:
        if min(self.relevance, self.temporal, self.priority) < 0:
            raise ValueError("ranking weights must be non-negative")
        if self.relevance + self.temporal + self.priority <= 0:
            raise ValueError("at least one ranking weight must be positive")

    def as_tuple(self) -> tuple[int, int, int]:
        return (self.relevance, self.temporal, self.priority)


@dataclass(frozen=True, slots=True)
class RetrievalCandidate:
    record_id: str
    subject_id: str
    namespace: str
    content_ref: str
    source_refs: tuple[str, ...]
    recorded_at: datetime
    cost_units: int
    relevance_bp: int
    temporal_bp: int = 0
    priority_bp: int = 0
    score_basis_refs: tuple[str, ...] = ()
    tombstoned: bool = False
    superseded: bool = False
    withdrawn: bool = False
    conflict: bool = False
    provenance_gate_passed: bool = True

    def __post_init__(self) -> None:
        for field_name in ("record_id", "subject_id", "namespace", "content_ref"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be non-empty")
        _require_aware(self.recorded_at, "recorded_at")
        if self.cost_units <= 0:
            raise ValueError("cost_units must be positive")
        _bounded_basis_points(self.relevance_bp, "relevance_bp")
        _bounded_basis_points(self.temporal_bp, "temporal_bp")
        _bounded_basis_points(self.priority_bp, "priority_bp")
        if not self.score_basis_refs:
            raise ValueError("score_basis_refs must explain supplied ranking signals")

    def deterministic_score(self, weights: RankingWeights) -> int:
        return (
            self.relevance_bp * weights.relevance
            + self.temporal_bp * weights.temporal
            + self.priority_bp * weights.priority
        )


@dataclass(frozen=True, slots=True)
class RetrievalRequest:
    query_id: str
    subject_id: str
    namespace: str
    cue_ref: str
    as_of: datetime
    budget_units: int
    max_records: int
    weights: RankingWeights = RankingWeights()

    def __post_init__(self) -> None:
        for field_name in ("query_id", "subject_id", "namespace", "cue_ref"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be non-empty")
        _require_aware(self.as_of, "as_of")
        if self.budget_units < 0:
            raise ValueError("budget_units must be non-negative")
        if self.max_records < 0:
            raise ValueError("max_records must be non-negative")


@dataclass(frozen=True, slots=True)
class CandidateDecision:
    record_id: str
    eligible: bool
    selected: bool
    score: int
    cost_units: int
    reasons: tuple[ExclusionReason, ...]


@dataclass(frozen=True, slots=True)
class RetrievalTrace:
    query_id: str
    selected_record_ids: tuple[str, ...]
    selected_content_refs: tuple[str, ...]
    total_cost_units: int
    budget_units: int
    max_records: int
    weights: RankingWeights
    decisions: tuple[CandidateDecision, ...]
    candidate_universe_hash: str
    manifest_hash: str

    def decision_for(self, record_id: str) -> CandidateDecision:
        for decision in self.decisions:
            if decision.record_id == record_id:
                return decision
        raise KeyError(record_id)


class DeterministicContextAssembler:
    """Transparent candidate gating and context selection.

    All semantic/ranking signals are caller-supplied and basis-attributed. The assembler
    performs no embedding call, model inference, hidden relevance extraction, or writeback.
    """

    def assemble(
        self,
        request: RetrievalRequest,
        candidates: tuple[RetrievalCandidate, ...],
    ) -> RetrievalTrace:
        ids = [item.record_id for item in candidates]
        if len(ids) != len(set(ids)):
            raise ValueError("candidate record_id values must be unique")

        gated: dict[str, tuple[ExclusionReason, ...]] = {}
        scores = {item.record_id: item.deterministic_score(request.weights) for item in candidates}
        for candidate in candidates:
            reasons: list[ExclusionReason] = []
            if candidate.subject_id != request.subject_id:
                reasons.append(ExclusionReason.SUBJECT_MISMATCH)
            if candidate.namespace != request.namespace:
                reasons.append(ExclusionReason.NAMESPACE_MISMATCH)
            if candidate.recorded_at > request.as_of:
                reasons.append(ExclusionReason.FUTURE_RECORD)
            if candidate.tombstoned:
                reasons.append(ExclusionReason.TOMBSTONED)
            if candidate.superseded:
                reasons.append(ExclusionReason.SUPERSEDED)
            if candidate.withdrawn:
                reasons.append(ExclusionReason.WITHDRAWN)
            if candidate.conflict:
                reasons.append(ExclusionReason.CONFLICT)
            if not candidate.provenance_gate_passed:
                reasons.append(ExclusionReason.PROVENANCE_GATE_FAILED)
            gated[candidate.record_id] = tuple(reasons)

        eligible = sorted(
            (item for item in candidates if not gated[item.record_id]),
            key=lambda item: (-scores[item.record_id], item.record_id),
        )

        selected: list[RetrievalCandidate] = []
        post_reasons: dict[str, tuple[ExclusionReason, ...]] = {}
        used = 0
        for candidate in eligible:
            if len(selected) >= request.max_records:
                post_reasons[candidate.record_id] = (ExclusionReason.MAX_RECORDS_REACHED,)
                continue
            if used + candidate.cost_units > request.budget_units:
                post_reasons[candidate.record_id] = (ExclusionReason.BUDGET_EXCEEDED,)
                continue
            selected.append(candidate)
            used += candidate.cost_units

        selected_ids = {item.record_id for item in selected}
        decisions = tuple(
            CandidateDecision(
                record_id=item.record_id,
                eligible=not gated[item.record_id],
                selected=item.record_id in selected_ids,
                score=scores[item.record_id],
                cost_units=item.cost_units,
                reasons=gated[item.record_id] or post_reasons.get(item.record_id, ()),
            )
            for item in sorted(candidates, key=lambda value: value.record_id)
        )

        universe_payload = [
            {
                "record_id": item.record_id,
                "recorded_at": item.recorded_at.isoformat(),
                "cost_units": item.cost_units,
                "relevance_bp": item.relevance_bp,
                "temporal_bp": item.temporal_bp,
                "priority_bp": item.priority_bp,
                "score_basis_refs": list(item.score_basis_refs),
                "source_refs": list(item.source_refs),
                "flags": {
                    "tombstoned": item.tombstoned,
                    "superseded": item.superseded,
                    "withdrawn": item.withdrawn,
                    "conflict": item.conflict,
                    "provenance_gate_passed": item.provenance_gate_passed,
                },
            }
            for item in sorted(candidates, key=lambda value: value.record_id)
        ]
        candidate_universe_hash = hashlib.sha256(
            json.dumps(universe_payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

        manifest_payload = {
            "query_id": request.query_id,
            "subject_id": request.subject_id,
            "namespace": request.namespace,
            "cue_ref": request.cue_ref,
            "as_of": request.as_of.isoformat(),
            "budget_units": request.budget_units,
            "max_records": request.max_records,
            "weights": request.weights.as_tuple(),
            "candidate_universe_hash": candidate_universe_hash,
            "selected_record_ids": [item.record_id for item in selected],
            "decisions": [
                {
                    "record_id": item.record_id,
                    "eligible": item.eligible,
                    "selected": item.selected,
                    "score": item.score,
                    "cost_units": item.cost_units,
                    "reasons": [reason.value for reason in item.reasons],
                }
                for item in decisions
            ],
        }
        manifest_hash = hashlib.sha256(
            json.dumps(manifest_payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

        return RetrievalTrace(
            query_id=request.query_id,
            selected_record_ids=tuple(item.record_id for item in selected),
            selected_content_refs=tuple(item.content_ref for item in selected),
            total_cost_units=used,
            budget_units=request.budget_units,
            max_records=request.max_records,
            weights=request.weights,
            decisions=decisions,
            candidate_universe_hash=candidate_universe_hash,
            manifest_hash=manifest_hash,
        )
