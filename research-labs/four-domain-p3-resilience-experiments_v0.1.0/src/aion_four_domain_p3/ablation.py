from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum

from aion_four_domain_p2 import (
    DeterministicContextAssembler,
    RetrievalCandidate,
    RetrievalRequest,
    RetrievalTrace,
)


class Control(str, Enum):
    PROVENANCE_GATE = "PROVENANCE_GATE"
    SUPERSESSION_GATE = "SUPERSESSION_GATE"
    WITHDRAWAL_GATE = "WITHDRAWAL_GATE"
    CONFLICT_GATE = "CONFLICT_GATE"
    SUBJECT_ISOLATION = "SUBJECT_ISOLATION"
    NAMESPACE_ISOLATION = "NAMESPACE_ISOLATION"


@dataclass(frozen=True, slots=True)
class AblationRun:
    disabled_controls: frozenset[Control]
    trace: RetrievalTrace


@dataclass(frozen=True, slots=True)
class AblationComparison:
    control: AblationRun
    variants: tuple[AblationRun, ...]
    newly_selected_by_variant: tuple[tuple[str, ...], ...]


class RetrievalControlAblationHarness:
    """Synthetic control ablation for measuring dependence on specific retrieval guards."""

    def __init__(self) -> None:
        self._assembler = DeterministicContextAssembler()

    def compare(
        self,
        request: RetrievalRequest,
        candidates: tuple[RetrievalCandidate, ...],
        disabled_sets: tuple[frozenset[Control], ...],
    ) -> AblationComparison:
        control = AblationRun(
            disabled_controls=frozenset(),
            trace=self._assembler.assemble(request, candidates),
        )
        variants: list[AblationRun] = []
        deltas: list[tuple[str, ...]] = []
        baseline = set(control.trace.selected_record_ids)
        for disabled in disabled_sets:
            variant_candidates = tuple(
                self._apply_disabled_controls(item, request, disabled) for item in candidates
            )
            trace = self._assembler.assemble(request, variant_candidates)
            variants.append(AblationRun(disabled_controls=disabled, trace=trace))
            deltas.append(tuple(sorted(set(trace.selected_record_ids) - baseline)))
        return AblationComparison(
            control=control,
            variants=tuple(variants),
            newly_selected_by_variant=tuple(deltas),
        )

    @staticmethod
    def _apply_disabled_controls(
        item: RetrievalCandidate,
        request: RetrievalRequest,
        disabled: frozenset[Control],
    ) -> RetrievalCandidate:
        updates: dict[str, object] = {}
        if Control.PROVENANCE_GATE in disabled:
            updates["provenance_gate_passed"] = True
        if Control.SUPERSESSION_GATE in disabled:
            updates["superseded"] = False
        if Control.WITHDRAWAL_GATE in disabled:
            updates["withdrawn"] = False
        if Control.CONFLICT_GATE in disabled:
            updates["conflict"] = False
        if Control.SUBJECT_ISOLATION in disabled:
            updates["subject_id"] = request.subject_id
        if Control.NAMESPACE_ISOLATION in disabled:
            updates["namespace"] = request.namespace
        return replace(item, **updates)
