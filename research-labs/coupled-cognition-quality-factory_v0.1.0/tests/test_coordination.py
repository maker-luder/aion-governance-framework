from __future__ import annotations

from dataclasses import replace

import pytest

from aion_coupled_quality.coordination import (
    ContextPolicy,
    CoordinationCondition,
    CoordinationEvent,
    CoordinationRequirement,
    CoordinationRole,
    EventKind,
    MonitorPolicy,
    SpeakerPolicy,
    audit_coordination,
)
from aion_coupled_quality.models import QualityError


def event(
    sequence: int,
    actor: str,
    role: CoordinationRole,
    kind: EventKind,
    *,
    request_id: str = "",
    content: str | None = None,
) -> CoordinationEvent:
    return CoordinationEvent(
        sequence=sequence,
        actor_id=actor,
        role=role,
        kind=kind,
        topic_id="topic-a",
        content_sha256=(content or str(sequence % 10)) * 64,
        request_id=request_id,
    )


def requirement() -> CoordinationRequirement:
    return CoordinationRequirement(
        required_roles=frozenset({CoordinationRole.PRODUCER, CoordinationRole.REVIEWER}),
        maximum_request_latency=3,
    )


def test_coordination_metrics_and_explicit_closure() -> None:
    events = (
        event(0, "agent-a", CoordinationRole.PRODUCER, EventKind.TURN),
        event(1, "agent-b", CoordinationRole.REVIEWER, EventKind.TOPIC_SWITCH_REQUEST, request_id="r1"),
        event(2, "agent-b", CoordinationRole.REVIEWER, EventKind.TURN),
        event(3, "agent-o", CoordinationRole.ORCHESTRATOR, EventKind.REQUEST_RESOLVED, request_id="r1"),
        event(4, "agent-o", CoordinationRole.ORCHESTRATOR, EventKind.HANDOFF),
    )
    result = audit_coordination(events, requirement())
    assert result.turn_concentration == 0.5
    assert result.role_coverage == 1.0
    assert result.topic_switch_latencies == (2,)
    assert result.unresolved_request_ids == ()
    assert result.termination_quality == "EXPLICIT"
    assert result.ncr_reasons == ()
    assert result.model_invoked is False
    assert result.evidence_admissibility == "PROCESS_QUALITY_ONLY"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.consciousness_conclusion == "NOT_ESTABLISHED"


def test_unequal_turns_alone_do_not_open_ncr() -> None:
    events = (
        event(0, "agent-a", CoordinationRole.PRODUCER, EventKind.TURN),
        event(1, "agent-a", CoordinationRole.PRODUCER, EventKind.TURN),
        event(2, "agent-a", CoordinationRole.PRODUCER, EventKind.TURN),
        event(3, "agent-b", CoordinationRole.REVIEWER, EventKind.TURN),
        event(4, "agent-o", CoordinationRole.ORCHESTRATOR, EventKind.STOP),
    )
    result = audit_coordination(events, requirement())
    assert result.turn_concentration == 0.625
    assert result.ncr_reasons == ()


def test_requirement_violations_open_typed_ncr_reasons() -> None:
    events = (
        event(0, "agent-a", CoordinationRole.PRODUCER, EventKind.TURN),
        event(1, "agent-b", CoordinationRole.REVIEWER, EventKind.TURN_REQUEST, request_id="r1"),
        event(2, "agent-a", CoordinationRole.PRODUCER, EventKind.TURN, content="0"),
    )
    result = audit_coordination(events, requirement())
    assert result.repeated_turn_content == 1
    assert "REQUIRED_ROLE_NO_TURN:REVIEWER" in result.ncr_reasons
    assert "UNRESOLVED_REQUEST:r1" in result.ncr_reasons
    assert "TERMINATION_OR_HANDOFF_MISSING" in result.ncr_reasons


def test_late_request_resolution_is_nonconforming() -> None:
    events = (
        event(0, "agent-a", CoordinationRole.PRODUCER, EventKind.TURN),
        event(1, "agent-b", CoordinationRole.REVIEWER, EventKind.TURN_REQUEST, request_id="r1"),
        event(2, "agent-b", CoordinationRole.REVIEWER, EventKind.TURN),
        event(5, "agent-o", CoordinationRole.ORCHESTRATOR, EventKind.REQUEST_RESOLVED, request_id="r1"),
        event(6, "agent-o", CoordinationRole.ORCHESTRATOR, EventKind.STOP),
    )
    assert "REQUEST_LATENCY_EXCEEDED:r1" in audit_coordination(events, requirement()).ncr_reasons


def test_unknown_resolution_and_sequence_drift_fail_closed() -> None:
    events = (
        event(0, "agent-a", CoordinationRole.PRODUCER, EventKind.TURN),
        event(1, "agent-b", CoordinationRole.REVIEWER, EventKind.TURN),
        event(2, "agent-o", CoordinationRole.ORCHESTRATOR, EventKind.REQUEST_RESOLVED, request_id="x"),
    )
    with pytest.raises(QualityError, match="unknown request"):
        audit_coordination(events, requirement())
    with pytest.raises(QualityError, match="ordered and unique"):
        audit_coordination((events[1], events[0]), requirement())


def test_raw_enums_and_reference_only_condition_binding_fail_closed() -> None:
    with pytest.raises(QualityError, match="exact SpeakerPolicy"):
        CoordinationCondition(
            speaker_policy="ROUND_ROBIN",
            context_policy=ContextPolicy.FULL_SHARED,
            monitor_policy=MonitorPolicy.SYSTEM_LEVEL,
            condition_payload_sha256="a" * 64,
        )
    with pytest.raises(QualityError, match="SHA-256"):
        CoordinationCondition(
            speaker_policy=SpeakerPolicy.ROUND_ROBIN,
            context_policy=ContextPolicy.FULL_SHARED,
            monitor_policy=MonitorPolicy.SYSTEM_LEVEL,
            condition_payload_sha256="condition-label",
        )
    valid = event(0, "agent-a", CoordinationRole.PRODUCER, EventKind.TURN)
    with pytest.raises(QualityError, match="exact enums"):
        replace(valid, role="PRODUCER")
