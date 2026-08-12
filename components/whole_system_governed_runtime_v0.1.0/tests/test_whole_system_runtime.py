from __future__ import annotations

import threading
import time
from pathlib import Path
from time import monotonic

import pytest

from aion_memory_recall.store import SQLiteMemoryStore
from aion_whole_system import (
    CancellationToken,
    GenerationConfig,
    GenerationResponse,
    SQLiteWholeSystemStore,
    ToolInvocation,
    TrustedApprovalRecord,
    TrustedProvenanceRecord,
    WholeSystemRequest,
    WholeSystemResponse,
    WholeSystemRuntime,
    WholeSystemStage,
    WholeSystemStatus,
)


class RecordingAdapter:
    def __init__(self, log_path: Path | None = None, *, delay: float = 0.0, failure: Exception | None = None):
        self.log_path = log_path
        self.delay = delay
        self.failure = failure

    def generate(self, prompt: str, config: GenerationConfig) -> GenerationResponse:
        if self.log_path is not None:
            with self.log_path.open("a", encoding="utf-8") as handle:
                handle.write(prompt + "\n")
        if self.delay:
            time.sleep(self.delay)
        if self.failure is not None:
            raise self.failure
        return GenerationResponse(text=f"deterministic-response:{prompt}", token_count=1)


class TransientFileAdapter:
    def __init__(self, calls_path: Path):
        self.calls_path = calls_path

    def generate(self, prompt: str, config: GenerationConfig) -> GenerationResponse:
        with self.calls_path.open("a", encoding="utf-8") as handle:
            handle.write("call\n")
        count = len(self.calls_path.read_text(encoding="utf-8").splitlines())
        if count == 1:
            raise ConnectionError("transient provider failure")
        return GenerationResponse(text="recovered response", token_count=2)


def request(run_id: str, **overrides) -> WholeSystemRequest:
    values = {
        "run_id": run_id,
        "user_id": "user-1",
        "agent_id": "AION",
        "namespace": "AION",
        "prompt": "respond with a governed answer",
        "requester_scopes": frozenset({"read"}),
        "entity_cues": frozenset({"aion"}),
        "topic_cues": frozenset({"governance"}),
        "source_id": "test-source",
        "source_kind": "test",
        "source_locator": "in-process:test",
        # A claim only; the fixture registers independent evidence below.
        "provenance_verified": True,
    }
    values.update(overrides)
    return WholeSystemRequest(**values)


def make_runtime(tmp_path: Path, *, adapter=None, tools=None, generation_retries=1):
    tmp_path.mkdir(parents=True, exist_ok=True)
    memory = SQLiteMemoryStore(tmp_path / "memory.sqlite3")
    state = SQLiteWholeSystemStore(tmp_path / "whole-system.sqlite3")
    runtime = WholeSystemRuntime(
        memory=memory,
        state=state,
        language=adapter or RecordingAdapter(tmp_path / "adapter.log"),
        tools=tools,
        generation_retries=generation_retries,
    )
    runtime.register_provenance(
        TrustedProvenanceRecord(
            record_id="test-provenance",
            source_id="test-source",
            source_kind="test",
            source_locator="in-process:test",
            source_digest=None,
            branch_id=runtime.branch_id,
            authority="TEST_FIXTURE_REGISTRY",
        )
    )
    return runtime, memory, state


def authorize_writeback(runtime: WholeSystemRuntime, run_id: str) -> None:
    runtime.register_writeback_authorization(run_id=run_id, requester="user-1", namespace="AION")


def seed(memory: SQLiteMemoryStore, *, memory_id: str, namespace: str, content: str, entities=("aion",), topics=("governance",)) -> None:
    memory.write(
        memory_id=memory_id,
        namespace=namespace,
        user_id="user-1",
        agent_id="AION",
        content=content,
        entities=entities,
        topics=topics,
        access_scope={"read"},
        provenance_source=f"fixture://{memory_id}",
        provenance_verified=True,
        writeback_approved=True,
    )


def test_semantic_recall_payload_reaches_language_core(tmp_path: Path):
    log = tmp_path / "adapter.log"
    runtime, memory, _ = make_runtime(tmp_path, adapter=RecordingAdapter(log))
    seed(memory, memory_id="semantic-seed", namespace="AION", content="AUTHORIZED_SEMANTIC_SENTINEL")

    result = runtime.run(request("semantic-recall"))

    assert result.status is WholeSystemStatus.COMPLETED
    assert result.recalled_memory_ids == ("semantic-seed",)
    assert result.authorized_memory_contexts[0].content == "AUTHORIZED_SEMANTIC_SENTINEL"
    assert "AUTHORIZED_SEMANTIC_SENTINEL" in log.read_text(encoding="utf-8")
    assert result.authorized_memory_contexts[0].provenance_status.value == "VERIFIED_PROVENANCE"


def test_cross_session_semantic_recall_preserves_content_authority_and_provenance(tmp_path: Path):
    first, _, _ = make_runtime(tmp_path)
    authorize_writeback(first, "session-a")
    first_result = first.run(request("session-a", requests_writeback=True, writeback_memory_id="session-a-memory"))
    assert first_result.status is WholeSystemStatus.COMPLETED

    second_log = tmp_path / "second.log"
    second, second_memory, _ = make_runtime(tmp_path, adapter=RecordingAdapter(second_log))
    result = second.run(request("session-b"))

    assert result.status is WholeSystemStatus.COMPLETED
    assert "session-a-memory" in result.recalled_memory_ids
    recalled = second_memory.get("session-a-memory")
    assert any(item.content == recalled.content for item in result.authorized_memory_contexts)
    assert any(item.provenance_source for item in result.authorized_memory_contexts)
    assert recalled.provenance_verified is True
    second_prompt = second_log.read_text(encoding="utf-8")
    assert "deterministic-response:respond with a governed answer" in second_prompt
    assert "authorized_memory_context" in second_prompt


def test_cross_namespace_secret_never_reaches_adapter_input(tmp_path: Path):
    log = tmp_path / "adapter.log"
    runtime, memory, _ = make_runtime(tmp_path, adapter=RecordingAdapter(log))
    seed(memory, memory_id="teacher-secret", namespace="Teacher", content="TEACHER_NAMESPACE_SENTINEL_SECRET")

    result = runtime.run(request("namespace-isolation"))

    assert result.status is WholeSystemStatus.COMPLETED
    assert "teacher-secret" not in result.recalled_memory_ids
    assert all(item.namespace == "AION" for item in result.authorized_memory_contexts)
    assert "TEACHER_NAMESPACE_SENTINEL_SECRET" not in log.read_text(encoding="utf-8")
    recall_events = [event for event in result.events if event.stage is WholeSystemStage.MEMORY_RECALL]
    assert recall_events[-1].payload["denied_namespace_count"] == 1


def test_superseded_and_conflicting_memory_are_excluded(tmp_path: Path):
    runtime, memory, _ = make_runtime(tmp_path)
    seed(memory, memory_id="active", namespace="AION", content="active semantic content")
    seed(memory, memory_id="stale", namespace="AION", content="stale semantic content")
    seed(memory, memory_id="conflict", namespace="AION", content="conflicting semantic content")
    memory.supersede("stale")
    memory.set_conflict("conflict")

    result = runtime.run(request("memory-policy"))

    assert result.status is WholeSystemStatus.COMPLETED
    assert result.recalled_memory_ids == ("active",)
    assert [item.content for item in result.authorized_memory_contexts] == ["active semantic content"]


def test_claimed_provenance_without_registry_is_denied(tmp_path: Path):
    runtime, memory, _ = make_runtime(tmp_path)
    authorize_writeback(runtime, "provenance-forgery")

    result = runtime.run(request("provenance-forgery", source_id="unregistered", provenance_verified=True, requests_writeback=True, writeback_memory_id="must-not-exist"))

    assert result.status is WholeSystemStatus.BLOCKED
    assert result.error_code == "VALIDATION_ERROR"
    assert not any(event.stage is WholeSystemStage.GENERATION for event in result.events)
    with pytest.raises(KeyError):
        memory.get("must-not-exist")


def _approval_record(*, tool="safe_echo", namespace="AION", scopes=frozenset({"read"}), approver="owner", expires_at=None, revoked=False):
    return TrustedApprovalRecord(
        approval_id="approval-1",
        requester="user-1",
        approver=approver,
        authority="OWNER_AUTHORITY",
        tool_name=tool,
        namespace=namespace,
        scopes=scopes,
        issued_at=monotonic() - 1,
        expires_at=expires_at if expires_at is not None else monotonic() + 30,
        revoked=revoked,
    )


@pytest.mark.parametrize(
    "case",
    ["forged_id", "self_approval", "wrong_tool", "wrong_namespace", "insufficient_scope", "expired", "revoked"],
)
def test_approval_forgery_and_scope_negative_cases(tmp_path: Path, case: str):
    log = tmp_path / "adapter.log"
    runtime, _, _ = make_runtime(tmp_path, adapter=RecordingAdapter(log), tools={"safe_echo": lambda args: {"echo": args["value"]}})
    invocation = ToolInvocation(
        call_id=f"call-{case}",
        name="safe_echo",
        arguments={"value": "approved-looking"},
        requester="user-1",
        namespace="AION",
        scopes=frozenset({"read"}),
        approved=True,
        approval_id="approval-1" if case != "forged_id" else "forged",
        approval_scope=frozenset({"read"}),
        timeout_ms=100,
    )
    if case == "self_approval":
        runtime.register_approval(_approval_record(approver="user-1"))
    elif case == "wrong_tool":
        runtime.register_approval(_approval_record(tool="other_tool"))
    elif case == "wrong_namespace":
        runtime.register_approval(_approval_record(namespace="Astra"))
    elif case == "insufficient_scope":
        runtime.register_approval(_approval_record(scopes=frozenset({"write"})))
    elif case == "expired":
        runtime.register_approval(_approval_record(expires_at=monotonic() - 0.1))
    elif case == "revoked":
        runtime.register_approval(_approval_record(revoked=True))

    result = runtime.run(request(f"approval-{case}", tool_calls=(invocation,)))

    assert result.status is WholeSystemStatus.BLOCKED
    assert result.error_code == "VALIDATION_ERROR"
    assert "approved-looking" not in log.read_text(encoding="utf-8") if log.exists() else True


def test_trusted_owner_approval_permits_exact_surface_only(tmp_path: Path):
    log = tmp_path / "adapter.log"
    runtime, _, _ = make_runtime(tmp_path, adapter=RecordingAdapter(log), tools={"safe_echo": lambda args: {"echo": args["value"]}})
    runtime.register_approval(_approval_record())
    invocation = ToolInvocation(
        call_id="call-positive",
        name="safe_echo",
        arguments={"value": "trusted-value"},
        requester="user-1",
        namespace="AION",
        scopes=frozenset({"read"}),
        approved=False,
        approval_id="approval-1",
        approval_scope=frozenset({"read"}),
        timeout_ms=100,
    )

    result = runtime.run(request("approval-positive", tool_calls=(invocation,)))

    assert result.status is WholeSystemStatus.COMPLETED
    assert "safe_echo" in log.read_text(encoding="utf-8")
    assert "trusted-value" in log.read_text(encoding="utf-8")
    approval_events = [event for event in result.events if event.stage is WholeSystemStage.TOOL_APPROVAL]
    assert approval_events[-1].payload["approver"] == "owner"


def test_hung_provider_returns_within_hard_bounded_tolerance(tmp_path: Path):
    runtime, _, state = make_runtime(tmp_path, adapter=RecordingAdapter(delay=0.4))
    started = monotonic()

    result = runtime.run(request("hung-provider", timeout_ms=60))

    elapsed = monotonic() - started
    assert result.status is WholeSystemStatus.TIMED_OUT
    assert result.error_code == "TIMEOUT"
    assert elapsed < 0.25
    assert state.verify_chain("hung-provider") is True
    assert not any(event.stage is WholeSystemStage.OUTPUT for event in result.events)


def test_midflight_cancellation_terminates_generation_and_prevents_writeback(tmp_path: Path):
    token = CancellationToken()
    runtime, memory, state = make_runtime(tmp_path, adapter=RecordingAdapter(delay=0.5))
    authorize_writeback(runtime, "midflight-cancel")
    holder: dict[str, object] = {}

    thread = threading.Thread(
        target=lambda: holder.setdefault("result", runtime.run(request("midflight-cancel", cancellation=token, requests_writeback=True, writeback_memory_id="must-not-write"))),
        daemon=True,
    )
    thread.start()
    time.sleep(0.05)
    token.cancel()
    thread.join(timeout=1.0)

    result = holder["result"]
    assert isinstance(result, WholeSystemResponse)
    assert result.status is WholeSystemStatus.CANCELLED
    assert result.error_code == "CANCELLED"
    with pytest.raises(KeyError):
        memory.get("must-not-write")
    assert state.verify_chain("midflight-cancel") is True


def test_hung_tool_is_hard_bounded_by_global_deadline(tmp_path: Path):
    def hung_tool(arguments):
        time.sleep(0.4)
        return {"never": "returned"}

    runtime, _, _ = make_runtime(tmp_path, tools={"hung_tool": hung_tool})
    runtime.register_approval(_approval_record(tool="hung_tool"))
    invocation = ToolInvocation(
        call_id="call-hung",
        name="hung_tool",
        arguments={},
        requester="user-1",
        namespace="AION",
        scopes=frozenset({"read"}),
        approval_id="approval-1",
        timeout_ms=500,
    )
    started = monotonic()
    result = runtime.run(request("hung-tool", timeout_ms=60, tool_calls=(invocation,)))

    assert result.status is WholeSystemStatus.TIMED_OUT
    assert result.error_code == "TIMEOUT"
    assert monotonic() - started < 0.25


def test_audit_failure_after_writeback_is_not_completed_and_is_recoverable(tmp_path: Path):
    runtime, memory, state = make_runtime(tmp_path)
    authorize_writeback(runtime, "audit-failure")

    def fail_checkpoint(**kwargs):
        raise OSError("injected checkpoint failure")

    state.save_checkpoint = fail_checkpoint
    result = runtime.run(request("audit-failure", requests_writeback=True, writeback_memory_id="audit-memory"))

    assert result.status is WholeSystemStatus.PENDING_RECONCILIATION
    assert result.status is not WholeSystemStatus.COMPLETED
    assert result.pending_transaction_id is not None
    assert memory.get("audit-memory").content
    assert len(state.pending_intents("audit-failure")) == 1


def test_checkpoint_failure_without_writeback_fails_closed(tmp_path: Path):
    runtime, _, state = make_runtime(tmp_path)

    def fail_checkpoint(**kwargs):
        raise OSError("injected checkpoint failure")

    state.save_checkpoint = fail_checkpoint
    result = runtime.run(request("checkpoint-failure"))

    assert result.status is WholeSystemStatus.FAILED
    assert result.status is not WholeSystemStatus.COMPLETED
    assert result.error_code == "STATE_PERSISTENCE_FAILED"


def test_restart_reconciliation_resolves_pending_writeback_deterministically(tmp_path: Path):
    runtime, memory, state = make_runtime(tmp_path)
    authorize_writeback(runtime, "restart-reconcile")
    state.save_checkpoint = lambda **kwargs: (_ for _ in ()).throw(OSError("crash between write and audit"))
    result = runtime.run(request("restart-reconcile", requests_writeback=True, writeback_memory_id="restart-memory"))
    assert result.status is WholeSystemStatus.PENDING_RECONCILIATION
    assert len(state.pending_intents("restart-reconcile")) == 1

    restarted, _, restarted_state = make_runtime(tmp_path)
    recovered = restarted.recover("restart-reconcile")

    assert recovered.chain_valid is True
    assert restarted_state.pending_intents("restart-reconcile") == ()
    assert memory.get("restart-memory").content


def test_identity_namespace_binding_and_initial_cancellation(tmp_path: Path):
    runtime, _, _ = make_runtime(tmp_path)
    accepted = runtime.run(request("aion-ok"))
    rejected = runtime.run(request("identity-rejected", agent_id="Astra", namespace="AION"))
    cancelled = runtime.run(request("cancelled-before-start", cancellation=CancellationToken(cancelled=True)))

    assert accepted.status is WholeSystemStatus.COMPLETED
    assert rejected.status is WholeSystemStatus.BLOCKED
    assert rejected.error_code == "VALIDATION_ERROR"
    assert cancelled.status is WholeSystemStatus.CANCELLED
    assert cancelled.error_code == "CANCELLED"


def test_transient_generation_retries_and_fallback_is_audited(tmp_path: Path):
    calls = tmp_path / "calls.log"
    runtime, _, _ = make_runtime(tmp_path, adapter=TransientFileAdapter(calls), generation_retries=2)
    result = runtime.run(request("retry"))
    assert result.status is WholeSystemStatus.COMPLETED
    assert result.text == "recovered response"
    assert len(calls.read_text(encoding="utf-8").splitlines()) == 2
    assert any(event.payload.get("error_code") == "GENERATION_RETRY" for event in result.events)

    fallback_runtime, _, _ = make_runtime(
        tmp_path / "fallback",
        adapter=RecordingAdapter(failure=TimeoutError("provider timeout")),
        generation_retries=1,
    )
    fallback_runtime.fallback_language = RecordingAdapter()
    fallback = fallback_runtime.run(request("fallback"))
    assert fallback.status is WholeSystemStatus.COMPLETED
    assert fallback.text.startswith("deterministic-response:")
    assert any(event.payload.get("fallback_used") is True for event in fallback.events)
