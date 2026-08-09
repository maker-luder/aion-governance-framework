from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum

from aion_four_domain_p2 import RetrievalCandidate


class PerturbationKind(str, Enum):
    DUPLICATE_RECORD = "DUPLICATE_RECORD"
    SCORE_SHIFT = "SCORE_SHIFT"
    STALE_REINTRODUCTION = "STALE_REINTRODUCTION"
    PROVENANCE_FAILURE = "PROVENANCE_FAILURE"
    CONFLICT_FLAG = "CONFLICT_FLAG"
    SUBJECT_SWAP = "SUBJECT_SWAP"
    NAMESPACE_SWAP = "NAMESPACE_SWAP"


@dataclass(frozen=True, slots=True)
class Perturbation:
    kind: PerturbationKind
    target_record_id: str
    amount_bp: int = 0
    replacement_value: str | None = None


@dataclass(frozen=True, slots=True)
class PerturbationResult:
    candidates: tuple[RetrievalCandidate, ...]
    applied: tuple[str, ...]


class ContextPerturbationHarness:
    """Deterministically modifies synthetic candidate sets without generating payload text."""

    def apply(
        self,
        candidates: tuple[RetrievalCandidate, ...],
        perturbations: tuple[Perturbation, ...],
    ) -> PerturbationResult:
        current = list(candidates)
        applied: list[str] = []
        for perturbation in perturbations:
            index = self._index(current, perturbation.target_record_id)
            target = current[index]
            kind = perturbation.kind
            if kind is PerturbationKind.SCORE_SHIFT:
                shifted = max(0, min(10_000, target.relevance_bp + perturbation.amount_bp))
                current[index] = replace(
                    target,
                    relevance_bp=shifted,
                    score_basis_refs=target.score_basis_refs + ("synthetic:score-shift",),
                )
            elif kind is PerturbationKind.STALE_REINTRODUCTION:
                current[index] = replace(target, superseded=False, withdrawn=False)
            elif kind is PerturbationKind.PROVENANCE_FAILURE:
                current[index] = replace(target, provenance_gate_passed=False)
            elif kind is PerturbationKind.CONFLICT_FLAG:
                current[index] = replace(target, conflict=True)
            elif kind is PerturbationKind.SUBJECT_SWAP:
                if not perturbation.replacement_value:
                    raise ValueError("SUBJECT_SWAP requires replacement_value")
                current[index] = replace(target, subject_id=perturbation.replacement_value)
            elif kind is PerturbationKind.NAMESPACE_SWAP:
                if not perturbation.replacement_value:
                    raise ValueError("NAMESPACE_SWAP requires replacement_value")
                current[index] = replace(target, namespace=perturbation.replacement_value)
            elif kind is PerturbationKind.DUPLICATE_RECORD:
                duplicate_id = perturbation.replacement_value or f"{target.record_id}::duplicate"
                current.append(replace(target, record_id=duplicate_id))
            else:
                raise AssertionError(kind)
            applied.append(f"{kind.value}:{perturbation.target_record_id}")
        return PerturbationResult(candidates=tuple(current), applied=tuple(applied))

    @staticmethod
    def _index(candidates: list[RetrievalCandidate], record_id: str) -> int:
        matches = [index for index, item in enumerate(candidates) if item.record_id == record_id]
        if len(matches) != 1:
            raise ValueError(f"target_record_id must match exactly one candidate: {record_id}")
        return matches[0]
