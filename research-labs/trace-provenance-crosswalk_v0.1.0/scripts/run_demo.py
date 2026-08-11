from aion_trace_crosswalk import AIONTraceEvent, to_openinference_attributes

event = AIONTraceEvent(
    session_id="demo-session",
    user_id="demo-user",
    agent_name="AION",
    span_kind="AGENT",
    runtime_event_id="evt-demo",
    subject_id="AION",
    input_value="redacted by default",
    tool_name="synthetic_tool",
    retrieval_documents=("fixture:doc-1",),
    evaluation_name="synthetic_gate",
    evaluation_score=1.0,
)
print(to_openinference_attributes(event))
