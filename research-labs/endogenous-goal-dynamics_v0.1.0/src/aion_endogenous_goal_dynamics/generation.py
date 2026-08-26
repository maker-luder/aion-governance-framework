from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Protocol

from .models import (
    CandidateOrigin,
    EndogenousState,
    ExternalFrame,
    GoalCandidate,
    GoalCandidateSet,
    canonical_hash,
)


@dataclass(frozen=True, slots=True)
class ModelGenerationRequest:
    external_frame_fingerprint: str
    bounded_state_projection: tuple[tuple[str, int], ...]
    candidate_universe: tuple[GoalCandidate, ...]
    parameters: tuple[tuple[str, str], ...] = ()

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)


@dataclass(frozen=True, slots=True)
class ModelGenerationResponse:
    candidates: tuple[GoalCandidate, ...]
    request_fingerprint: str
    response_fingerprint: str
    provider_id: str
    model_id: str
    deterministic: bool
    replay: bool
    provenance_refs: tuple[str, ...]


class ModelProvider(Protocol):
    provider_id: str
    model_id: str
    deterministic: bool
    replay: bool

    def generate_goal_candidates(self, request: ModelGenerationRequest) -> ModelGenerationResponse: ...


class CandidateGenerator(Protocol):
    generator_id: str
    version: str

    def generate(self, frame: ExternalFrame, state: EndogenousState | None = None) -> GoalCandidateSet: ...


def bounded_state_projection(state: EndogenousState | None) -> tuple[tuple[str, int], ...]:
    if state is None:
        return ()
    totals: dict[str, int] = {}
    for signal in state.signals:
        totals[signal.channel.value] = totals.get(signal.channel.value, 0) + signal.value_bp
    return tuple(sorted(totals.items()))


class DeterministicCandidateGenerator:
    generator_id = "DETERMINISTIC_CANDIDATE_GENERATOR"
    version = "0.1.0"

    def generate(self, frame: ExternalFrame, state: EndogenousState | None = None) -> GoalCandidateSet:
        projection = bounded_state_projection(state)
        request = canonical_hash((frame.fingerprint, projection, frame.candidate_universe_fingerprint))
        candidates = tuple(sorted(frame.candidate_universe, key=lambda candidate: candidate.goal_id))
        response = canonical_hash(candidates)
        return GoalCandidateSet(
            set_id=f"candidate-set:{response[:16]}",
            external_frame_fingerprint=frame.fingerprint,
            generator_id=self.generator_id,
            generator_version=self.version,
            candidates=candidates,
            request_fingerprint=request,
            response_fingerprint=response,
            provenance_refs=("local:deterministic-candidate-generator",),
        )


@dataclass(frozen=True, slots=True)
class ReplayFixture:
    fixture_id: str
    request_fingerprint: str
    candidates: tuple[GoalCandidate, ...]
    provider_id: str
    model_id: str
    response_fingerprint: str
    provenance_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        expected = canonical_hash(self.candidates)
        if self.response_fingerprint != expected:
            raise ValueError("replay response fingerprint does not match candidates")
        if not self.provenance_refs:
            raise ValueError("replay fixture requires provenance")


class ReplayCandidateGenerator:
    generator_id = "REPLAY_CANDIDATE_GENERATOR"
    version = "0.1.0"

    def __init__(self, fixture: ReplayFixture) -> None:
        self.fixture = fixture

    def generate(self, frame: ExternalFrame, state: EndogenousState | None = None) -> GoalCandidateSet:
        request = ModelGenerationRequest(
            external_frame_fingerprint=frame.fingerprint,
            bounded_state_projection=bounded_state_projection(state),
            candidate_universe=frame.candidate_universe,
        )
        if request.fingerprint != self.fixture.request_fingerprint:
            raise ValueError("replay request fingerprint mismatch")
        return GoalCandidateSet(
            set_id=f"replay:{self.fixture.fixture_id}",
            external_frame_fingerprint=frame.fingerprint,
            generator_id=self.generator_id,
            generator_version=self.version,
            candidates=tuple(sorted(self.fixture.candidates, key=lambda candidate: candidate.goal_id)),
            request_fingerprint=request.fingerprint,
            response_fingerprint=self.fixture.response_fingerprint,
            provider_id=self.fixture.provider_id,
            model_id=self.fixture.model_id,
            deterministic=True,
            replay=True,
            provenance_refs=self.fixture.provenance_refs,
        )


class DeterministicStubProvider:
    provider_id = "LOCAL_DETERMINISTIC_STUB"
    model_id = "stub-v0.1.0"
    deterministic = True
    replay = False

    def generate_goal_candidates(self, request: ModelGenerationRequest) -> ModelGenerationResponse:
        candidates = tuple(
            replace(candidate, origin=CandidateOrigin.MODEL, generation_evidence_refs=("stub:response",))
            for candidate in sorted(request.candidate_universe, key=lambda candidate: candidate.goal_id)
        )
        return ModelGenerationResponse(
            candidates=candidates,
            request_fingerprint=request.fingerprint,
            response_fingerprint=canonical_hash(candidates),
            provider_id=self.provider_id,
            model_id=self.model_id,
            deterministic=True,
            replay=False,
            provenance_refs=("local:deterministic-stub-provider",),
        )


class ReplayModelProvider:
    deterministic = True
    replay = True

    def __init__(self, fixture: ReplayFixture) -> None:
        self.fixture = fixture
        self.provider_id = fixture.provider_id
        self.model_id = fixture.model_id

    def generate_goal_candidates(self, request: ModelGenerationRequest) -> ModelGenerationResponse:
        if request.fingerprint != self.fixture.request_fingerprint:
            raise ValueError("replay provider request fingerprint mismatch")
        return ModelGenerationResponse(
            candidates=self.fixture.candidates,
            request_fingerprint=request.fingerprint,
            response_fingerprint=self.fixture.response_fingerprint,
            provider_id=self.provider_id,
            model_id=self.model_id,
            deterministic=True,
            replay=True,
            provenance_refs=self.fixture.provenance_refs,
        )


class ModelCandidateGenerator:
    generator_id = "MODEL_CANDIDATE_GENERATOR"
    version = "0.1.0"

    def __init__(self, provider: ModelProvider) -> None:
        self.provider = provider

    def generate(self, frame: ExternalFrame, state: EndogenousState | None = None) -> GoalCandidateSet:
        request = ModelGenerationRequest(
            external_frame_fingerprint=frame.fingerprint,
            bounded_state_projection=bounded_state_projection(state),
            candidate_universe=frame.candidate_universe,
        )
        response = self.provider.generate_goal_candidates(request)
        if response.request_fingerprint != request.fingerprint:
            raise ValueError("provider response is not bound to the request")
        if response.response_fingerprint != canonical_hash(response.candidates):
            raise ValueError("provider response fingerprint mismatch")
        return GoalCandidateSet(
            set_id=f"model-set:{response.response_fingerprint[:16]}",
            external_frame_fingerprint=frame.fingerprint,
            generator_id=self.generator_id,
            generator_version=self.version,
            candidates=tuple(response.candidates),
            request_fingerprint=request.fingerprint,
            response_fingerprint=response.response_fingerprint,
            provider_id=response.provider_id,
            model_id=response.model_id,
            deterministic=response.deterministic,
            replay=response.replay,
            provenance_refs=response.provenance_refs,
        )
