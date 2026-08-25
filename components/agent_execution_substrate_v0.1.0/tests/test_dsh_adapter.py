from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from aion_astra_agent_substrate import (
    DSH_RELEASE_LABEL,
    DSH_UPSTREAM_REF,
    RuntimeBinding,
    SubstrateError,
    dsh_profile,
    fork_lineage,
    normalize_dsh_trajectory,
    team_snapshot,
    trajectory_digest,
)


COMPONENT = Path(__file__).resolve().parents[1]
FIXTURE = COMPONENT / "fixtures/dsh_session_events.json"


def _binding(session_id: str = "dsh-aion-session-001") -> RuntimeBinding:
    return RuntimeBinding.from_runtime_context(
        {
            "agent_id": "AION",
            "runtime_instance_id": "AION-I-001",
            "memory_stream_id": "AION-MEM-001",
            "event_lineage_id": "AION-EVT-001",
            "canonical_state_reference": "AION-CANONICAL",
            "genesis_root_id": "GENESIS-001",
        },
        substrate_id="dsh-pinned",
        session_id=session_id,
    )


def _events() -> list[dict[str, object]]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_dsh_profile_is_exact_ref_pinned_and_inspection_only() -> None:
    value = dsh_profile()
    assert value.upstream_ref == "b150a551b8d465e31e418e1b2eaf5e79bbb7d28e"
    assert value.upstream_ref == DSH_UPSTREAM_REF
    assert DSH_RELEASE_LABEL == "dsh@0.1.1-rc.2"
    assert value.developer_preview is True
    assert value.live_execution is False
    assert value.network_access is False


def test_durable_dsh_trajectory_is_deterministic_and_content_minimized() -> None:
    events = _events()
    first = normalize_dsh_trajectory(events, binding=_binding())
    second = normalize_dsh_trajectory(deepcopy(events), binding=_binding())
    assert first == second
    assert trajectory_digest(first) == trajectory_digest(second)

    original_text = "redacted-fixture-request"
    normalized_json = json.dumps([item.to_dict() for item in first], ensure_ascii=False)
    assert original_text not in normalized_json
    assert all(len(item.payload_sha256) == 64 for item in first)


def test_live_extension_event_is_not_upgraded_to_durable_evidence() -> None:
    with pytest.raises(SubstrateError, match="live/transient"):
        normalize_dsh_trajectory(
            [{"type": "agent/request", "sessionId": "dsh-aion-session-001", "payload": {}}],
            binding=_binding(),
        )


def test_session_mismatch_fails_closed() -> None:
    events = _events()
    events[0]["sessionId"] = "other-session"
    with pytest.raises(SubstrateError, match="does not match"):
        normalize_dsh_trajectory(events, binding=_binding())


def test_provider_exposed_reasoning_is_not_claimed_as_complete_internal_cognition() -> None:
    normalized = normalize_dsh_trajectory(
        [
            {
                "type": "assistant/message",
                "sessionId": "dsh-aion-session-001",
                "payload": {"analysis": "provider-visible-summary"},
            }
        ],
        binding=_binding(),
    )
    assert normalized[0].reasoning_visibility == "PROVIDER_EXPOSED_ONLY"
    assert "provider-visible-summary" not in json.dumps(normalized[0].to_dict())


def test_fork_lineage_preserves_identity_nonclaim() -> None:
    value = fork_lineage(
        {
            "parentSession": "session-parent",
            "childSession": "session-child",
            "boundary": "event-17",
        }
    )
    assert value.identity_continuity_conclusion == "NOT_ESTABLISHED"
    assert value.parent_session_id != value.child_session_id


def test_fork_rejects_same_session_as_parent_and_child() -> None:
    with pytest.raises(SubstrateError, match="must differ"):
        fork_lineage(
            {
                "parentSession": "same",
                "childSession": "same",
                "boundary": "event-1",
            }
        )


def test_agent_team_snapshot_preserves_collective_identity_nonclaim() -> None:
    value = team_snapshot(
        {
            "teamId": "team-1",
            "members": [
                {"id": "session-a", "name": "A"},
                {"id": "session-b", "name": "B"},
            ],
        }
    )
    assert value.member_session_ids == ("session-a", "session-b")
    assert value.collective_identity_conclusion == "NOT_ESTABLISHED"
