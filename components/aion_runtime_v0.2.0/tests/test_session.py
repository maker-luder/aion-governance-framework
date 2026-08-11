from aion_runtime_v2.session import SessionContextManager


def test_session_is_working_context_and_snapshot_is_noncanonical():
    session = SessionContextManager("S1")
    session.append(kind="message", role="user", content="hello")
    snap = session.snapshot()
    assert snap.canonical_effect == "NONE"
    assert snap.items[0].content == "hello"


def test_interrupt_roundtrip():
    session = SessionContextManager("S1")
    session.add_interrupt(interrupt_id="I1", call_id="C1", tool_name="danger", arguments={"x": 1}, reason="approval")
    assert session.get_interrupt("I1").call_id == "C1"
    session.resolve_interrupt("I1")
    assert session.snapshot().pending_interrupts == ()


def test_context_budget_selects_recent_content():
    session = SessionContextManager("S1")
    session.append(kind="message", role="user", content="old-" + "x" * 50)
    session.append(kind="message", role="user", content="new")
    assembled = session.assemble_messages(max_chars=10)
    assert assembled[-1]["content"] == "new"
