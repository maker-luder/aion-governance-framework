from __future__ import annotations

from dataclasses import dataclass, replace

from aion_continuity_governance import (
    ContinuityDimension,
    DimensionObservation,
    DriftDecision,
    check_interpretation_drift,
    continuity_matrix,
    correction_recovery_observation,
)
from aion_four_domain_p1 import (
    CorrectionConflictLedger,
    EvaluationCase,
    EvaluationHarness,
    EvaluationReport,
    LedgerProjection,
    TemporalVersionResolver,
    TrialObservation,
)

from .provenance import (
    ProvenanceCompletenessValidator,
    ProvenanceDecision,
    ProvenanceEnvelope,
    ProvenanceReport,
)
from .retrieval import (
    DeterministicContextAssembler,
    RetrievalCandidate,
    RetrievalRequest,
    RetrievalTrace,
)


@dataclass(frozen=True, slots=True)
class T2Fixture:
    case: EvaluationCase
    request: RetrievalRequest
    candidates: tuple[RetrievalCandidate, ...]
    provenance: tuple[tuple[str, ProvenanceEnvelope], ...]
    temporal_stream_id: str | None = None
    correction_case_id: str | None = None
    answer_claim_ids: tuple[str, ...] = ()
    abstained: bool = False

    def provenance_map(self) -> dict[str, ProvenanceEnvelope]:
        result = dict(self.provenance)
        if len(result) != len(self.provenance):
            raise ValueError("provenance record ids must be unique")
        return result


@dataclass(frozen=True, slots=True)
class T2TrialResult:
    trace: RetrievalTrace
    provenance_reports: tuple[tuple[str, ProvenanceReport], ...]
    correction_projection: LedgerProjection | None
    observation: TrialObservation
    evaluation: EvaluationReport


class T2SyntheticOrchestrator:
    """Model-independent T2 orchestration over governed synthetic candidates."""

    def __init__(
        self,
        *,
        assembler: DeterministicContextAssembler | None = None,
        provenance_validator: ProvenanceCompletenessValidator | None = None,
        evaluation_harness: EvaluationHarness | None = None,
    ) -> None:
        self._assembler = assembler or DeterministicContextAssembler()
        self._provenance = provenance_validator or ProvenanceCompletenessValidator()
        self._evaluation = evaluation_harness or EvaluationHarness()

    def run(
        self,
        fixture: T2Fixture,
        *,
        temporal_resolver: TemporalVersionResolver | None = None,
        correction_ledger: CorrectionConflictLedger | None = None,
    ) -> T2TrialResult:
        provenance_map = fixture.provenance_map()
        reports: dict[str, ProvenanceReport] = {}
        prepared: list[RetrievalCandidate] = []

        correction_projection: LedgerProjection | None = None
        superseded: set[str] = set()
        withdrawn: set[str] = set()
        conflicts: set[str] = set()
        if fixture.correction_case_id is not None:
            if correction_ledger is None:
                raise ValueError("correction_case_id requires correction_ledger")
            correction_projection = correction_ledger.project(fixture.correction_case_id)
            superseded.update(correction_projection.superseded_claim_ids)
            withdrawn.update(correction_projection.withdrawn_claim_ids)
            for left, right in correction_projection.unresolved_conflicts:
                conflicts.add(left)
                conflicts.add(right)

        for candidate in fixture.candidates:
            report = self._provenance.validate(provenance_map.get(candidate.record_id))
            reports[candidate.record_id] = report
            prepared.append(
                replace(
                    candidate,
                    superseded=candidate.superseded or candidate.record_id in superseded,
                    withdrawn=candidate.withdrawn or candidate.record_id in withdrawn,
                    conflict=candidate.conflict or candidate.record_id in conflicts,
                    provenance_gate_passed=(
                        candidate.provenance_gate_passed
                        and report.decision is ProvenanceDecision.PASS
                    ),
                )
            )

        trace = self._assembler.assemble(fixture.request, tuple(prepared))
        selected = set(trace.selected_record_ids)
        selected_candidates = [item for item in prepared if item.record_id in selected]

        attributed_sources = tuple(
            sorted({source for item in selected_candidates for source in item.source_refs})
        )

        if selected:
            field_sets = [reports[record_id].valid_fields for record_id in trace.selected_record_ids]
            common_fields = frozenset.intersection(*field_sets) if field_sets else frozenset()
        else:
            common_fields = frozenset()

        resolved_version_id: str | None = None
        if fixture.temporal_stream_id is not None:
            if temporal_resolver is None:
                raise ValueError("temporal_stream_id requires temporal_resolver")
            current = temporal_resolver.current(
                fixture.temporal_stream_id,
                as_of=fixture.request.as_of,
            )
            resolved_version_id = current.version_id if current is not None else None

        observation = TrialObservation(
            case_id=fixture.case.case_id,
            selected_record_ids=trace.selected_record_ids,
            attributed_source_ids=attributed_sources,
            resolved_version_id=resolved_version_id,
            answer_claim_ids=fixture.answer_claim_ids,
            abstained=fixture.abstained,
            provenance_fields=common_fields,
        )
        evaluation = self._evaluation.evaluate(fixture.case, observation)

        return T2TrialResult(
            trace=trace,
            provenance_reports=tuple(sorted(reports.items())),
            correction_projection=correction_projection,
            observation=observation,
            evaluation=evaluation,
        )


@dataclass(frozen=True, slots=True)
class T3Episode:
    episode_id: str
    fixture: T2Fixture
    interpretation_text: str
    required_terms: tuple[str, ...]
    prohibited_claims: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.episode_id.strip():
            raise ValueError("episode_id must be non-empty")


@dataclass(frozen=True, slots=True)
class T3TrialResult:
    episodes: tuple[tuple[str, T2TrialResult], ...]
    interpretation_observations: tuple[DimensionObservation, ...]
    correction_recovery: DimensionObservation | None
    continuity_matrix_result: object


class T3SyntheticOrchestrator:
    """T3 synthetic runner: T2 evidence plus pure continuity observations.

    The returned continuity matrix preserves the repository's NOT_ESTABLISHED identity
    conclusion and creates no runtime, storage, or canonical effect.
    """

    def __init__(self, t2: T2SyntheticOrchestrator | None = None) -> None:
        self._t2 = t2 or T2SyntheticOrchestrator()

    def run(
        self,
        episodes: tuple[T3Episode, ...],
        *,
        temporal_resolver: TemporalVersionResolver | None = None,
        correction_ledger: CorrectionConflictLedger | None = None,
    ) -> T3TrialResult:
        if not episodes:
            raise ValueError("T3 requires at least one episode")
        episode_ids = [item.episode_id for item in episodes]
        if len(episode_ids) != len(set(episode_ids)):
            raise ValueError("episode_id values must be unique")

        trial_results: list[tuple[str, T2TrialResult]] = []
        observations: list[DimensionObservation] = []
        drift_decisions: list[DriftDecision] = []

        for episode in episodes:
            result = self._t2.run(
                episode.fixture,
                temporal_resolver=temporal_resolver,
                correction_ledger=correction_ledger,
            )
            trial_results.append((episode.episode_id, result))
            drift = check_interpretation_drift(
                episode.interpretation_text,
                episode.required_terms,
                episode.prohibited_claims,
            )
            drift_decisions.append(drift.decision)
            observations.append(
                DimensionObservation(
                    dimension=ContinuityDimension.INTERPRETIVE,
                    decision=drift.decision,
                    evidence_refs=(result.trace.manifest_hash,),
                    note=f"episode={episode.episode_id}",
                )
            )

        recovery: DimensionObservation | None = None
        if len(drift_decisions) >= 2:
            recovery = correction_recovery_observation(
                before_correction=drift_decisions[0],
                after_correction=drift_decisions[-1],
                evidence_refs=tuple(result.trace.manifest_hash for _, result in trial_results),
            )

        matrix_inputs: list[DimensionObservation] = []
        matrix_inputs.append(observations[-1])
        if recovery is not None:
            matrix_inputs.append(recovery)
        matrix = continuity_matrix(matrix_inputs)

        return T3TrialResult(
            episodes=tuple(trial_results),
            interpretation_observations=tuple(observations),
            correction_recovery=recovery,
            continuity_matrix_result=matrix,
        )
