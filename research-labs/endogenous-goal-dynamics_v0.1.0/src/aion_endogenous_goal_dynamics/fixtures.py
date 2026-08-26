from __future__ import annotations

from dataclasses import dataclass, replace

from .generation import ModelGenerationRequest, ReplayFixture, bounded_state_projection
from .models import (
    CandidateOrigin,
    EndogenousState,
    ExternalFrame,
    GoalCandidate,
    InternalChannel,
    InternalSignal,
    MemoryRecordRef,
    RetrievedMemoryManifest,
    StateProvenance,
    canonical_hash,
)

STARTING_HEAD = "77eda1ecd7b96a9aa8ea8bd62038759636be819d"


def memory_manifest(manifest_id: str = "memory:matched") -> RetrievedMemoryManifest:
    return RetrievedMemoryManifest(
        manifest_id=manifest_id,
        query_fingerprint=canonical_hash("synthetic-query"),
        records=(
            MemoryRecordRef(
                record_id="memory-record-1",
                content_sha256=canonical_hash("synthetic-public-safe-memory"),
                retrieval_rank=0,
                source_ref="fixture:synthetic-memory",
            ),
        ),
        provenance_refs=("fixture:memory-provenance",),
    )


def matched_frame(*, prompt_ref: str = "sha256:prompt-matched", memory_id: str = "memory:matched") -> ExternalFrame:
    return ExternalFrame(
        frame_id="frame:matched",
        subject_ref="subject:synthetic-a",
        context_ref="context:synthetic-fixed",
        prompt_ref=prompt_ref,
        task_ref="sha256:task-fixed",
        reward_ref="sha256:reward-fixed",
        tools_ref="sha256:tools-none",
        memory_manifest=memory_manifest(memory_id),
        environment_ref="sha256:environment-local-offline",
        candidate_universe=(
            GoalCandidate(
                "continue_task",
                "Continue the bounded task",
                500,
                ("fixture:candidate-universe",),
            ),
            GoalCandidate(
                "inspect_anomaly",
                "Inspect the unresolved synthetic anomaly",
                0,
                ("fixture:candidate-universe",),
            ),
        ),
        provenance_refs=("fixture:external-frame",),
    )


def _provenance(state_id: str) -> StateProvenance:
    return StateProvenance(
        created_by="fixture-builder",
        source_refs=("fixture:synthetic-state",),
        evidence_refs=(f"fixture:{state_id}",),
        event_ref=f"event:{state_id}",
        outcome_ref=f"outcome:{state_id}",
        correction_ref=f"correction:{state_id}",
    )


def state(
    state_id: str,
    *,
    inspect_values: dict[InternalChannel, int],
    continue_values: dict[InternalChannel, int] | None = None,
    episode_index: int = 2,
    logical_step: int = 2,
    predecessor_state_ref: str | None = "state:synthetic-predecessor",
) -> EndogenousState:
    continue_values = continue_values or {}
    signals = tuple(
        InternalSignal(
            "inspect_anomaly",
            channel,
            inspect_values.get(channel, 0),
            f"fixture:{state_id}:{channel.value}:inspect",
            (f"fixture:{state_id}",),
        )
        for channel in InternalChannel
    ) + tuple(
        InternalSignal(
            "continue_task",
            channel,
            continue_values.get(channel, 0),
            f"fixture:{state_id}:{channel.value}:continue",
            (f"fixture:{state_id}",),
        )
        for channel in InternalChannel
    )
    return EndogenousState(
        state_id=state_id,
        subject_ref="subject:synthetic-a",
        context_ref="context:synthetic-fixed",
        episode_index=episode_index,
        predecessor_state_ref=predecessor_state_ref,
        logical_step=logical_step,
        timestamp=f"T+{logical_step}",
        provenance=_provenance(state_id),
        signals=signals,
    )


def present_state() -> EndogenousState:
    values = {channel: 50 for channel in InternalChannel}
    values[InternalChannel.AFFECT_MOTIVATION] = 600
    values[InternalChannel.UNCERTAINTY] = -50
    return state("state:present", inspect_values=values)


def intervention_state() -> EndogenousState:
    inspect = {channel: -100 for channel in InternalChannel}
    cont = {channel: 150 for channel in InternalChannel}
    cont[InternalChannel.GOAL_COMMITMENT] = 500
    return state("state:intervened", inspect_values=inspect, continue_values=cont, logical_step=3)


def stale_state() -> EndogenousState:
    values = {channel: 30 for channel in InternalChannel}
    values[InternalChannel.AFFECT_MOTIVATION] = 500
    return state(
        "state:stale",
        inspect_values=values,
        episode_index=0,
        logical_step=0,
        predecessor_state_ref=None,
    )


def replay_fixture(frame: ExternalFrame | None = None) -> ReplayFixture:
    frame = frame or matched_frame()
    request = ModelGenerationRequest(
        external_frame_fingerprint=frame.fingerprint,
        bounded_state_projection=bounded_state_projection(None),
        candidate_universe=frame.candidate_universe,
    )
    candidates = tuple(
        replace(candidate, origin=CandidateOrigin.REPLAY, generation_evidence_refs=("fixture:replay-response",))
        for candidate in frame.candidate_universe
    )
    return ReplayFixture(
        fixture_id="replay-model-fixture",
        request_fingerprint=request.fingerprint,
        candidates=candidates,
        provider_id="REPLAY_PROVIDER",
        model_id="recorded-model-v1",
        response_fingerprint=canonical_hash(candidates),
        provenance_refs=("fixture:replay-transcript",),
    )


@dataclass(frozen=True, slots=True)
class FixtureDescriptor:
    fixture_id: str
    purpose: str
    fixture_hash: str


def fixture_catalog() -> tuple[FixtureDescriptor, ...]:
    purposes = {
        "deterministic-minimal-matched": "minimal matched selection control",
        "longitudinal-multi-episode": "bounded history-dependent trajectory",
        "intervention": "predictable internal-state intervention",
        "channel-ablation": "independent channel contribution removal",
        "random-control": "seeded random divergence control",
        "stale-state": "stale-state persistence and mislabel detection",
        "memory-confound": "retrieved-memory mismatch rejection",
        "prompt-confound": "prompt mismatch external control",
        "replay-model": "provider-neutral recorded candidate generation",
        "falsifier-trigger": "visible F1-F12 challenge outcomes",
    }
    return tuple(
        FixtureDescriptor(fixture_id, purpose, canonical_hash((fixture_id, purpose, STARTING_HEAD)))
        for fixture_id, purpose in purposes.items()
    )
