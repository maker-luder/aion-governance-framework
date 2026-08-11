from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class TracePolicy:
    include_input_value: bool = False
    include_output_value: bool = False
    include_tool_parameters: bool = False
    include_retrieval_documents: bool = True


@dataclass(frozen=True)
class AIONTraceEvent:
    session_id: str
    user_id: str
    agent_name: str
    span_kind: str
    runtime_event_id: str
    subject_id: str
    input_value: str | None = None
    output_value: str | None = None
    tool_name: str | None = None
    tool_parameters: str | None = None
    retrieval_documents: tuple[str, ...] = ()
    evaluation_name: str | None = None
    evaluation_score: float | None = None
    evaluation_label: str | None = None
    evaluation_explanation: str | None = None
    graph_node_id: str | None = None
    graph_parent_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    source_ref: str | None = None
    approval_ref: str | None = None
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        for name in ("session_id", "user_id", "agent_name", "span_kind", "runtime_event_id", "subject_id"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if self.evaluation_score is not None and not 0.0 <= self.evaluation_score <= 1.0:
            raise ValueError("evaluation_score must be between 0.0 and 1.0")
        if self.canonical_effect != "NONE":
            raise ValueError("trace export cannot change canonical state")


@dataclass(frozen=True)
class ImportedTraceObservation:
    session_id: str | None
    user_id: str | None
    agent_name: str | None
    span_kind: str | None
    tool_name: str | None
    graph_node_id: str | None
    graph_parent_id: str | None
    evaluation_name: str | None
    evaluation_score: float | None
    evaluation_label: str | None
    extras: Mapping[str, Any]
    authority: str = "EXTERNAL_OBSERVATION_ONLY"
    canonical_effect: str = "NONE"


_OPEN_KEYS = {
    "session.id",
    "user.id",
    "agent.name",
    "openinference.span.kind",
    "input.value",
    "output.value",
    "tool.name",
    "tool.parameters",
    "retrieval.documents",
    "evaluation.name",
    "evaluation.score",
    "evaluation.label",
    "evaluation.explanation",
    "graph.node.id",
    "graph.node.parent_id",
    "metadata",
}


def to_openinference_attributes(event: AIONTraceEvent, policy: TracePolicy | None = None) -> dict[str, Any]:
    policy = policy or TracePolicy()
    attrs: dict[str, Any] = {
        "session.id": event.session_id,
        "user.id": event.user_id,
        "agent.name": event.agent_name,
        "openinference.span.kind": event.span_kind,
        "aion.runtime_event_id": event.runtime_event_id,
        "aion.subject_id": event.subject_id,
        "aion.canonical_effect": "NONE",
    }
    if event.tool_name is not None:
        attrs["tool.name"] = event.tool_name
    if policy.include_tool_parameters and event.tool_parameters is not None:
        attrs["tool.parameters"] = event.tool_parameters
    if policy.include_input_value and event.input_value is not None:
        attrs["input.value"] = event.input_value
    if policy.include_output_value and event.output_value is not None:
        attrs["output.value"] = event.output_value
    if policy.include_retrieval_documents and event.retrieval_documents:
        attrs["retrieval.documents"] = list(event.retrieval_documents)
    if event.evaluation_name is not None:
        attrs["evaluation.name"] = event.evaluation_name
    if event.evaluation_score is not None:
        attrs["evaluation.score"] = event.evaluation_score
    if event.evaluation_label is not None:
        attrs["evaluation.label"] = event.evaluation_label
    if event.evaluation_explanation is not None:
        attrs["evaluation.explanation"] = event.evaluation_explanation
    if event.graph_node_id is not None:
        attrs["graph.node.id"] = event.graph_node_id
    if event.graph_parent_id is not None:
        attrs["graph.node.parent_id"] = event.graph_parent_id
    if event.metadata:
        attrs["metadata"] = dict(event.metadata)
    if event.source_ref is not None:
        attrs["aion.source_ref"] = event.source_ref
    if event.approval_ref is not None:
        attrs["aion.approval_ref"] = event.approval_ref
    return attrs


def from_openinference_attributes(attributes: Mapping[str, Any]) -> ImportedTraceObservation:
    score = attributes.get("evaluation.score")
    if score is not None:
        score = float(score)
        if not 0.0 <= score <= 1.0:
            raise ValueError("external evaluation.score must be between 0.0 and 1.0")
    extras = {
        key: value
        for key, value in attributes.items()
        if key not in _OPEN_KEYS and not key.startswith("aion.")
    }
    return ImportedTraceObservation(
        session_id=_optional_str(attributes.get("session.id")),
        user_id=_optional_str(attributes.get("user.id")),
        agent_name=_optional_str(attributes.get("agent.name")),
        span_kind=_optional_str(attributes.get("openinference.span.kind")),
        tool_name=_optional_str(attributes.get("tool.name")),
        graph_node_id=_optional_str(attributes.get("graph.node.id")),
        graph_parent_id=_optional_str(attributes.get("graph.node.parent_id")),
        evaluation_name=_optional_str(attributes.get("evaluation.name")),
        evaluation_score=score,
        evaluation_label=_optional_str(attributes.get("evaluation.label")),
        extras=extras,
    )


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)
