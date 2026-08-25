"""Pinned DeepSeek Harness profile and offline durable-event adapter.

The adapter intentionally does not import, execute, install, or contact DSH.
It accepts already-captured durable session-event objects and turns them into
content-minimized AION/Astra substrate evidence.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .models import (
    Capability,
    EventFamily,
    ForkLineage,
    NormalizedEvent,
    RuntimeBinding,
    SubstrateError,
    SubstrateProfile,
    TeamSnapshot,
    sha256_json,
)

DSH_UPSTREAM_REPOSITORY = "deepseek-ai/deepseek-harness"
DSH_UPSTREAM_REF = "b150a551b8d465e31e418e1b2eaf5e79bbb7d28e"
DSH_RELEASE_LABEL = "dsh@0.1.1-rc.2"
DSH_PROFILE_ID = "DEEPSEEK_HARNESS_PINNED_INSPECTION_V0.1.0"

_DURABLE_PREFIXES = ("turn/", "step/", "assistant/", "tool/")
_DURABLE_EXACT = frozenset({"user/message"})


def profile() -> SubstrateProfile:
    return SubstrateProfile(
        profile_id=DSH_PROFILE_ID,
        adapter_id="dsh-durable-session-event-adapter-v0.1.0",
        upstream_repository=DSH_UPSTREAM_REPOSITORY,
        upstream_ref=DSH_UPSTREAM_REF,
        developer_preview=True,
        live_execution=False,
        network_access=False,
        capabilities=tuple(Capability),
        nonclaims=(
            "TRAJECTORY != TRUTH",
            "FORK_LINEAGE != IDENTITY_CONTINUITY",
            "AGENT_TEAM != COLLECTIVE_IDENTITY",
            "PLUGIN_CREATION != SELF_AUTHORIZATION",
            "PROVIDER_EXPOSED_REASONING != COMPLETE_INTERNAL_COGNITION",
        ),
    )


def _family(event_type: str) -> EventFamily:
    if event_type.startswith("turn/"):
        return EventFamily.TURN
    if event_type.startswith("step/"):
        return EventFamily.STEP
    if event_type == "user/message":
        return EventFamily.USER_MESSAGE
    if event_type.startswith("assistant/"):
        return EventFamily.ASSISTANT
    if event_type.startswith("tool/"):
        return EventFamily.TOOL
    raise SubstrateError(f"event is not an admitted durable DSH session event: {event_type}")


def _payload(raw: Mapping[str, Any]) -> Mapping[str, Any]:
    value = raw.get("payload", {})
    if not isinstance(value, Mapping):
        raise SubstrateError("DSH event payload must be an object")
    return value


def normalize_event(
    raw: Mapping[str, Any],
    *,
    binding: RuntimeBinding,
    sequence: int,
) -> NormalizedEvent:
    if sequence < 1:
        raise SubstrateError("event sequence must be positive")
    event_type = str(raw.get("type", "")).strip()
    if not event_type:
        raise SubstrateError("DSH event type is required")
    if event_type not in _DURABLE_EXACT and not event_type.startswith(_DURABLE_PREFIXES):
        raise SubstrateError(f"live/transient DSH event is not admitted as durable evidence: {event_type}")

    source_session = str(raw.get("sessionId") or raw.get("session_id") or binding.session_id).strip()
    if source_session != binding.session_id:
        raise SubstrateError("DSH event session does not match the bound runtime substrate session")

    payload = _payload(raw)
    keys = tuple(sorted(str(key) for key in payload))
    reasoning_visibility = (
        "PROVIDER_EXPOSED_ONLY"
        if any(key in payload for key in ("reasoning", "reasoning_content", "analysis"))
        else "NOT_ESTABLISHED"
    )
    return NormalizedEvent(
        sequence=sequence,
        source=f"{DSH_UPSTREAM_REPOSITORY}@{DSH_UPSTREAM_REF}",
        source_event_type=event_type,
        family=_family(event_type),
        session_id=binding.session_id,
        payload_sha256=sha256_json(payload),
        payload_keys=keys,
        reasoning_visibility=reasoning_visibility,
    )


def normalize_trajectory(
    events: Iterable[Mapping[str, Any]],
    *,
    binding: RuntimeBinding,
) -> tuple[NormalizedEvent, ...]:
    normalized = tuple(
        normalize_event(raw, binding=binding, sequence=index)
        for index, raw in enumerate(events, start=1)
    )
    if not normalized:
        raise SubstrateError("trajectory requires at least one durable event")
    return normalized


def fork_lineage(raw: Mapping[str, Any]) -> ForkLineage:
    parent = str(raw.get("parentSession") or raw.get("parent_session_id") or "").strip()
    child = str(raw.get("childSession") or raw.get("child_session_id") or "").strip()
    boundary = str(raw.get("boundary") or raw.get("seedLength") or "").strip()
    return ForkLineage(parent, child, boundary)


def team_snapshot(raw: Mapping[str, Any]) -> TeamSnapshot:
    team_id = str(raw.get("teamId") or raw.get("team_id") or "").strip()
    members = raw.get("members")
    if not isinstance(members, list):
        raise SubstrateError("team snapshot members must be an array")
    session_ids: list[str] = []
    for member in members:
        if not isinstance(member, Mapping):
            raise SubstrateError("team member must be an object")
        session_id = str(member.get("id") or member.get("sessionId") or "").strip()
        if not session_id:
            raise SubstrateError("team member session id is required")
        session_ids.append(session_id)
    return TeamSnapshot(team_id=team_id, member_session_ids=tuple(session_ids))
