from __future__ import annotations

import pytest

from aion_trace_crosswalk import (
    AIONTraceEvent,
    TracePolicy,
    from_openinference_attributes,
    to_openinference_attributes,
)


def event() -> AIONTraceEvent:
    return AIONTraceEvent(
        session_id="s1",
        user_id="u1",
        agent_name="AION",
        span_kind="AGENT",
        runtime_event_id="evt-1",
        subject_id="AION",
        input_value="private input",
        output_value="private output",
        tool_name="search",
        tool_parameters='{"q":"x"}',
        retrieval_documents=("doc:1", "doc:2"),
        evaluation_name="gate",
        evaluation_score=1.0,
        evaluation_label="pass",
        evaluation_explanation="synthetic fixture",
        graph_node_id="n2",
        graph_parent_id="n1",
        metadata={"fixture": True},
        source_ref="src-1",
        approval_ref="apr-1",
    )


def test_core_identity_trace_keys_map() -> None:
    attrs = to_openinference_attributes(event())
    assert attrs["session.id"] == "s1"
    assert attrs["user.id"] == "u1"
    assert attrs["agent.name"] == "AION"


def test_raw_input_and_output_are_redacted_by_default() -> None:
    attrs = to_openinference_attributes(event())
    assert "input.value" not in attrs
    assert "output.value" not in attrs


def test_raw_content_requires_explicit_policy() -> None:
    attrs = to_openinference_attributes(event(), TracePolicy(include_input_value=True, include_output_value=True))
    assert attrs["input.value"] == "private input"
    assert attrs["output.value"] == "private output"


def test_tool_parameters_are_redacted_by_default() -> None:
    attrs = to_openinference_attributes(event())
    assert attrs["tool.name"] == "search"
    assert "tool.parameters" not in attrs


def test_tool_parameters_require_explicit_policy() -> None:
    attrs = to_openinference_attributes(event(), TracePolicy(include_tool_parameters=True))
    assert attrs["tool.parameters"] == '{"q":"x"}'


def test_retrieval_refs_are_exported_without_claiming_memory_truth() -> None:
    attrs = to_openinference_attributes(event())
    assert attrs["retrieval.documents"] == ["doc:1", "doc:2"]
    assert attrs["aion.canonical_effect"] == "NONE"


def test_evaluation_and_graph_keys_map() -> None:
    attrs = to_openinference_attributes(event())
    assert attrs["evaluation.name"] == "gate"
    assert attrs["evaluation.score"] == 1.0
    assert attrs["graph.node.id"] == "n2"
    assert attrs["graph.node.parent_id"] == "n1"


def test_aion_provenance_fields_remain_namespaced() -> None:
    attrs = to_openinference_attributes(event())
    assert attrs["aion.source_ref"] == "src-1"
    assert attrs["aion.approval_ref"] == "apr-1"


def test_external_import_never_inherits_aion_authority() -> None:
    observation = from_openinference_attributes({
        "session.id": "s",
        "aion.approval_ref": "forged",
        "aion.canonical_effect": "WRITE",
    })
    assert observation.authority == "EXTERNAL_OBSERVATION_ONLY"
    assert observation.canonical_effect == "NONE"
    assert "aion.approval_ref" not in observation.extras


def test_unknown_external_attributes_are_preserved_as_extras() -> None:
    observation = from_openinference_attributes({"session.id": "s", "vendor.custom": 7})
    assert observation.extras == {"vendor.custom": 7}


def test_invalid_external_score_is_rejected() -> None:
    with pytest.raises(ValueError):
        from_openinference_attributes({"evaluation.score": 4.0})


def test_trace_event_cannot_write_canonical_state() -> None:
    with pytest.raises(ValueError):
        AIONTraceEvent(
            session_id="s",
            user_id="u",
            agent_name="AION",
            span_kind="AGENT",
            runtime_event_id="e",
            subject_id="AION",
            canonical_effect="WRITE",
        )
