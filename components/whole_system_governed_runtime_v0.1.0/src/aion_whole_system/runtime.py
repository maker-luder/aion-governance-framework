from __future__ import annotations

import hashlib
import multiprocessing
from dataclasses import dataclass
from datetime import UTC, datetime
from time import monotonic
from typing import Any, Callable, Mapping, Protocol

from aion_memory_recall.models import RecallRequest
from aion_memory_recall.store import MemoryWriteDenied, SQLiteMemoryStore, StoredMemory

from .models import (
    MemoryContext,
    ProvenanceStatus,
    RecoveryRecord,
    TrustedApprovalRecord,
    TrustedProvenanceRecord,
    WholeSystemEvent,
    WholeSystemRequest,
    WholeSystemResponse,
    WholeSystemStage,
    WholeSystemStatus,
    WholeSystemValidationError,
)
from .storage import SQLiteWholeSystemStore


@dataclass(frozen=True, slots=True)
class GenerationConfig:
    max_output_tokens: int = 256
    temperature: float = 0.0
    seed: int = 0


@dataclass(frozen=True, slots=True)
class GenerationResponse:
    text: str
    token_count: int = 0


class LanguageAdapter(Protocol):
    def generate(self, prompt: str, config: GenerationConfig) -> Any: ...


class WholeSystemInterrupted(RuntimeError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


class _WorkerFailure(RuntimeError):
    def __init__(self, error_type: str, detail: str) -> None:
        super().__init__(detail)
        self.error_type = error_type
        self.detail = detail


def _call_worker(connection: Any, callable_object: Callable[..., Any], args: tuple[Any, ...]) -> None:
    """Fork worker used to enforce a killable provider/tool boundary."""
    try:
        connection.send(("ok", callable_object(*args)))
    except BaseException as exc:  # noqa: BLE001 - child boundary serializes provider failures
        try:
            connection.send(("error", type(exc).__name__, str(exc)))
        except Exception:
            pass
    finally:
        connection.close()


@dataclass(frozen=True, slots=True)
class _ValidatedContext:
    recalled_ids: tuple[str, ...]
    memory_contexts: tuple[MemoryContext, ...]
    denied_namespace_count: int
    provenance_record: TrustedProvenanceRecord
    provenance_status: ProvenanceStatus


class WholeSystemRuntime:
    """Local, candidate-only governed composition root.

    The runtime uses v2 authoritative memory storage and explicit registries. A
    request's ``approved`` or ``provenance_verified`` booleans are untrusted
    claims and never create authority. Provider and tool calls run in a forked
    child that is terminated at the global deadline; no runtime writeback is
    performed after timeout/cancellation. Cross-store writeback uses a durable
    intent and deterministic restart reconciliation rather than claiming true
    SQLite cross-database atomicity.
    """

    def __init__(
        self,
        *,
        memory: SQLiteMemoryStore,
        state: SQLiteWholeSystemStore,
        language: LanguageAdapter,
        tools: Mapping[str, Callable[[Mapping[str, Any]], Any]] | None = None,
        agent_id: str = "AION",
        branch_id: str = "review/aion-astra-whole-system-completion-v2",
        source_revision: str = "formal-research-plus-selective-replay",
        generation_retries: int = 1,
        fallback_language: LanguageAdapter | None = None,
        memory_context_limit: int = 512,
    ) -> None:
        if not agent_id.strip() or not branch_id.strip() or not source_revision.strip():
            raise WholeSystemValidationError("agent_id, branch_id and source_revision are required")
        if generation_retries < 1:
            raise WholeSystemValidationError("generation_retries must be positive")
        if memory_context_limit < 32:
            raise WholeSystemValidationError("memory_context_limit is too small")
        self.memory = memory
        self.state = state
        self.language = language
        self.fallback_language = fallback_language
        self.tools = dict(tools or {})
        self.agent_id = agent_id
        self.branch_id = branch_id
        self.source_revision = source_revision
        self.generation_retries = generation_retries
        self.memory_context_limit = memory_context_limit
        self._approvals: dict[str, TrustedApprovalRecord] = {}
        self._provenance: dict[str, TrustedProvenanceRecord] = {}
        self._writeback_authorizations: set[tuple[str, str, str]] = set()

    def register_approval(self, record: TrustedApprovalRecord) -> None:
        if not record.approval_id.strip() or not record.approver.strip():
            raise WholeSystemValidationError("trusted approval record requires approval_id and approver")
        self._approvals[record.approval_id] = record

    def register_provenance(self, record: TrustedProvenanceRecord) -> None:
        if record.branch_id != self.branch_id:
            raise WholeSystemValidationError("provenance record branch does not match runtime branch")
        self._provenance[record.source_id] = record

    def register_writeback_authorization(self, *, run_id: str, requester: str, namespace: str) -> None:
        self._writeback_authorizations.add((run_id, requester, namespace))

    def run(self, request: WholeSystemRequest) -> WholeSystemResponse:
        deadline = request.deadline()
        tx_id: str | None = None
        context: _ValidatedContext | None = None
        try:
            self._check(request, deadline)
            self._emit(request, WholeSystemStage.INPUT, WholeSystemStatus.COMPLETED, {"prompt_present": bool(request.prompt)})
            context = self._context_intake(request, deadline)
            self._emit(
                request,
                WholeSystemStage.MEMORY_RECALL,
                WholeSystemStatus.COMPLETED,
                {
                    "result_count": len(context.recalled_ids),
                    "memory_ids": list(context.recalled_ids),
                    "authorized_payload_count": len(context.memory_contexts),
                    "denied_namespace_count": context.denied_namespace_count,
                },
            )
            self._emit(
                request,
                WholeSystemStage.PROVENANCE_VALIDATION,
                WholeSystemStatus.COMPLETED,
                {"record_id": context.provenance_record.record_id, "status": context.provenance_status.value},
            )
            self._check(request, deadline)
            self._emit(request, WholeSystemStage.PLANNED, WholeSystemStatus.COMPLETED, {"tool_required": bool(request.tool_calls)})

            if request.tool_calls:
                tool_results = self._run_tools(request, deadline)
            else:
                tool_results = ()
            generated_prompt = self._assemble_prompt(request, context.memory_contexts, tool_results)
            text, generation_meta = self._generate_bounded(request, generated_prompt, deadline)
            self._emit(request, WholeSystemStage.GENERATION, WholeSystemStatus.COMPLETED, generation_meta)
            self._check(request, deadline)
            self._emit(request, WholeSystemStage.RESPONSE_BUILT, WholeSystemStatus.COMPLETED, {"text_length": len(text)})

            writeback_allowed = False
            if request.requests_writeback:
                writeback_allowed = self._writeback_authorized(request)
            self._emit(
                request,
                WholeSystemStage.WRITEBACK_DECIDED,
                WholeSystemStatus.COMPLETED if writeback_allowed or not request.requests_writeback else WholeSystemStatus.BLOCKED,
                {"allowed": writeback_allowed, "reason": "trusted_writeback_authorization" if writeback_allowed else "trusted_writeback_authorization_required"},
            )
            if request.requests_writeback and not writeback_allowed:
                return self._finish(
                    request,
                    status=WholeSystemStatus.BLOCKED,
                    error_code="WRITEBACK_AUTHORIZATION_REQUIRED",
                    error_detail="owner_approved is an untrusted claim; a registered writeback authorization is required",
                    context=context,
                )

            writeback_id: str | None = None
            if writeback_allowed:
                self._check(request, deadline)
                writeback_id = request.writeback_memory_id or f"{request.run_id}:memory"
                tx_id = self.state.begin_writeback_intent(run_id=request.run_id, memory_id=writeback_id, content=text)
                try:
                    self.memory.write(
                        memory_id=writeback_id,
                        namespace=request.namespace,
                        user_id=request.user_id,
                        agent_id=request.agent_id,
                        content=text,
                        entities=request.entity_cues,
                        topics=request.topic_cues,
                        access_scope=request.requester_scopes,
                        provenance_source=context.provenance_record.source_locator,
                        provenance_verified=True,
                        writeback_approved=True,
                    )
                except (MemoryWriteDenied, ValueError, KeyError) as exc:
                    self.state.mark_writeback_intent(tx_id, status="ABORTED", reason=f"memory write failed: {type(exc).__name__}")
                    self._emit(request, WholeSystemStage.FAILED, WholeSystemStatus.FAILED, {"error_code": "MEMORY_WRITEBACK_FAILED"})
                    return self._finish(request, status=WholeSystemStatus.FAILED, error_code="MEMORY_WRITEBACK_FAILED", error_detail=type(exc).__name__, context=context)
                self._emit(request, WholeSystemStage.MEMORY_UPDATED, WholeSystemStatus.COMPLETED, {"memory_id": writeback_id, "transaction_id": tx_id})

            self._check(request, deadline)
            self._emit(request, WholeSystemStage.OUTPUT, WholeSystemStatus.COMPLETED, {"writeback_memory_id": writeback_id})
            return self._finish(
                request,
                status=WholeSystemStatus.COMPLETED,
                text=text,
                recalled_ids=context.recalled_ids,
                memory_contexts=context.memory_contexts,
                writeback_allowed=writeback_allowed,
                writeback_id=writeback_id,
                transaction_id=tx_id,
                context=context,
            )
        except WholeSystemInterrupted as exc:
            return self._finish(
                request,
                status=WholeSystemStatus.CANCELLED if exc.code == "CANCELLED" else WholeSystemStatus.TIMED_OUT,
                error_code=exc.code,
                error_detail=exc.detail,
                context=context,
                transaction_id=tx_id,
            )
        except WholeSystemValidationError as exc:
            return self._finish(request, status=WholeSystemStatus.BLOCKED, error_code="VALIDATION_ERROR", error_detail=str(exc), context=context)
        except _WorkerFailure as exc:
            return self._finish(request, status=WholeSystemStatus.FAILED, error_code="CONTROLLED_RUNTIME_ERROR", error_detail=exc.error_type, context=context)
        except Exception as exc:  # noqa: BLE001 - boundary normalizes provider/tool/storage failures
            return self._finish(request, status=WholeSystemStatus.FAILED, error_code="CONTROLLED_RUNTIME_ERROR", error_detail=type(exc).__name__, context=context, transaction_id=tx_id)

    def recover(self, run_id: str) -> RecoveryRecord:
        if not run_id.strip():
            raise WholeSystemValidationError("run_id is required")
        for intent in self.state.pending_intents(run_id):
            try:
                record = self.memory.get(str(intent["memory_id"]))
            except KeyError:
                self.state.mark_writeback_intent(str(intent["transaction_id"]), status="RECONCILED_ABORTED", reason="memory write was not present after restart")
                continue
            digest = hashlib.sha256(record.content.encode("utf-8")).hexdigest()
            if digest == str(intent["content_digest"]) and record.namespace:
                self.state.mark_writeback_intent(str(intent["transaction_id"]), status="RECONCILED_COMMITTED", reason="memory write and intent digest match after restart")
            else:
                self.state.mark_writeback_intent(str(intent["transaction_id"]), status="RECONCILED_ABORTED", reason="memory write digest mismatch after restart")
        return self.state.recover(run_id)

    def _context_intake(self, request: WholeSystemRequest, deadline: float) -> _ValidatedContext:
        self._check(request, deadline)
        if request.agent_id != self.agent_id:
            raise WholeSystemValidationError("identity mismatch: request agent is not bound runtime agent")
        if request.namespace != request.agent_id:
            raise WholeSystemValidationError("identity and namespace binding mismatch")
        self._emit(request, WholeSystemStage.CONTEXT_INTAKE, WholeSystemStatus.COMPLETED, {"user_id_present": bool(request.user_id)})
        self._emit(request, WholeSystemStage.IDENTITY_RESOLUTION, WholeSystemStatus.COMPLETED, {"agent_id": request.agent_id})
        self._emit(request, WholeSystemStage.NAMESPACE_RESOLUTION, WholeSystemStatus.COMPLETED, {"namespace": request.namespace})

        source = self._verify_provenance(request)
        if source is None:
            raise WholeSystemValidationError("provenance evidence is unavailable or invalid; caller claim was not promoted")
        recall_request = RecallRequest(
            user_id=request.user_id,
            agent_id=request.agent_id,
            requester_scopes=request.requester_scopes,
            entity_cues=request.entity_cues,
            topic_cues=request.topic_cues,
        )
        all_identity_records = self.memory.list_for_identity(user_id=request.user_id, agent_id=request.agent_id)
        records = self.memory.recall(recall_request, limit=8)
        allowed_records = [item for item in records if item.namespace == request.namespace and item.provenance_verified and not item.tombstoned and not item.superseded and not item.conflict]
        contexts = tuple(self._to_memory_context(item) for item in allowed_records)
        denied_namespace_count = sum(1 for item in all_identity_records if item.namespace != request.namespace)
        return _ValidatedContext(
            recalled_ids=tuple(item.memory_id for item in allowed_records),
            memory_contexts=contexts,
            denied_namespace_count=denied_namespace_count,
            provenance_record=source,
            provenance_status=ProvenanceStatus.VERIFIED,
        )

    def _verify_provenance(self, request: WholeSystemRequest) -> TrustedProvenanceRecord | None:
        record = self._provenance.get(request.source_id)
        if record is None or not record.valid:
            return None
        if record.source_kind != request.source_kind or record.source_locator != request.source_locator:
            return None
        if record.source_digest != request.source_digest:
            return None
        return record

    def _to_memory_context(self, item: StoredMemory) -> MemoryContext:
        return MemoryContext(
            memory_id=item.memory_id,
            content=item.content[: self.memory_context_limit],
            namespace=item.namespace,
            authority="OBSERVATION",
            confidence=1.0 if item.provenance_verified else 0.0,
            revision=1,
            timestamp=item.recorded_at,
            provenance_source=item.provenance_source,
            provenance_status=ProvenanceStatus.VERIFIED if item.provenance_verified else ProvenanceStatus.UNVERIFIED,
            supersession_status="ACTIVE",
        )

    def _run_tools(self, request: WholeSystemRequest, deadline: float) -> tuple[Mapping[str, Any], ...]:
        results: list[Mapping[str, Any]] = []
        for invocation in request.tool_calls:
            self._check(request, deadline)
            approval = self._approvals.get(invocation.approval_id)
            if approval is None or not approval.valid_for(invocation):
                self._emit(request, WholeSystemStage.TOOL_APPROVAL, WholeSystemStatus.BLOCKED, {"tool_name": invocation.name, "reason": "trusted_approval_invalid"})
                raise WholeSystemValidationError(f"tool approval denied: {invocation.name}")
            tool = self.tools.get(invocation.name)
            if tool is None:
                raise WholeSystemValidationError(f"tool is not registered: {invocation.name}")
            remaining = max(0.001, min(invocation.timeout_ms / 1000.0, deadline - monotonic()))
            try:
                result = self._run_killable(
                    tool,
                    (invocation.arguments,),
                    timeout=remaining,
                    request=request,
                    operation=f"tool:{invocation.name}",
                )
            except WholeSystemInterrupted:
                raise
            self._emit(request, WholeSystemStage.TOOL_APPROVAL, WholeSystemStatus.COMPLETED, {"tool_name": invocation.name, "approver": approval.approver, "authority": approval.authority})
            results.append({"tool_name": invocation.name, "content": result, "provenance": f"tool://{invocation.name}"})
        return tuple(results)

    def _generate_bounded(self, request: WholeSystemRequest, prompt: str, deadline: float) -> tuple[str, Mapping[str, Any]]:
        config = GenerationConfig()
        last_failure: _WorkerFailure | None = None
        retries = 0
        for attempt in range(1, self.generation_retries + 1):
            remaining = deadline - monotonic()
            if remaining <= 0:
                raise WholeSystemInterrupted("TIMEOUT", "global request deadline expired before generation")
            try:
                raw = self._run_killable(self.language.generate, (prompt, config), timeout=remaining, request=request, operation="generation")
                return self._response_text(raw), {"retry_count": retries, "fallback_used": False, "bounded_execution": "PROCESS_TERMINATED_ON_BOUNDARY"}
            except WholeSystemInterrupted:
                raise
            except _WorkerFailure as exc:
                last_failure = exc
                if exc.error_type not in {"TimeoutError", "ConnectionError"} or attempt == self.generation_retries:
                    break
                retries += 1
                self._emit(request, WholeSystemStage.GENERATION, WholeSystemStatus.FAILED, {"error_code": "GENERATION_RETRY", "attempt": attempt})
        if self.fallback_language is not None:
            remaining = deadline - monotonic()
            if remaining <= 0:
                raise WholeSystemInterrupted("TIMEOUT", "global request deadline expired before fallback")
            raw = self._run_killable(self.fallback_language.generate, (prompt, config), timeout=remaining, request=request, operation="fallback_generation")
            return self._response_text(raw), {"retry_count": retries, "fallback_used": True, "bounded_execution": "PROCESS_TERMINATED_ON_BOUNDARY"}
        if last_failure is not None:
            raise last_failure
        raise WholeSystemValidationError("generation did not return a response")

    def _run_killable(self, callable_object: Callable[..., Any], args: tuple[Any, ...], *, timeout: float, request: WholeSystemRequest, operation: str) -> Any:
        context = multiprocessing.get_context("fork")
        parent, child = context.Pipe(duplex=False)
        process = context.Process(target=_call_worker, args=(child, callable_object, args), daemon=True)
        process.start()
        child.close()
        started = monotonic()
        try:
            while True:
                if request.cancellation is not None and request.cancellation.cancelled:
                    process.terminate()
                    process.join(timeout=0.2)
                    raise WholeSystemInterrupted("CANCELLED", f"mid-flight cancellation terminated {operation}")
                remaining = timeout - (monotonic() - started)
                if remaining <= 0:
                    process.terminate()
                    process.join(timeout=0.2)
                    raise WholeSystemInterrupted("TIMEOUT", f"bounded {operation} deadline exceeded and child was terminated")
                if parent.poll(min(0.01, remaining)):
                    message = parent.recv()
                    if message[0] == "ok":
                        process.join(timeout=0.2)
                        return message[1]
                    raise _WorkerFailure(str(message[1]), str(message[2]))
                if not process.is_alive() and not parent.poll():
                    raise _WorkerFailure("WorkerExit", f"{operation} exited without a result")
        finally:
            parent.close()
            if process.is_alive():
                process.terminate()
            process.join(timeout=0.2)

    @staticmethod
    def _response_text(raw: Any) -> str:
        if isinstance(raw, str):
            return raw
        text = getattr(raw, "text", None)
        if isinstance(text, str):
            return text
        raise WholeSystemValidationError("language adapter returned no text field")

    @staticmethod
    def _assemble_prompt(request: WholeSystemRequest, contexts: tuple[MemoryContext, ...], tool_results: tuple[Mapping[str, Any], ...]) -> str:
        memory_payload = [
            {
                "memory_id": item.memory_id,
                "content": item.content,
                "namespace": item.namespace,
                "authority": item.authority,
                "confidence": item.confidence,
                "revision": item.revision,
                "timestamp": item.timestamp,
                "provenance_source": item.provenance_source,
                "supersession_status": item.supersession_status,
            }
            for item in contexts
        ]
        return f"{request.prompt}\n[authorized_memory_context={memory_payload!r}; tool_results={tool_results!r}]"

    def _writeback_authorized(self, request: WholeSystemRequest) -> bool:
        return (request.run_id, request.user_id, request.namespace) in self._writeback_authorizations

    def _finish(
        self,
        request: WholeSystemRequest,
        *,
        status: WholeSystemStatus,
        context: _ValidatedContext | None,
        text: str = "",
        error_code: str | None = None,
        error_detail: str | None = None,
        recalled_ids: tuple[str, ...] = (),
        memory_contexts: tuple[MemoryContext, ...] = (),
        writeback_allowed: bool = False,
        writeback_id: str | None = None,
        transaction_id: str | None = None,
    ) -> WholeSystemResponse:
        provenance_record_id = context.provenance_record.record_id if context else None
        provenance_status = context.provenance_status if context else ProvenanceStatus.UNVERIFIED
        checkpoint_id: str | None = None
        persistence_error: str | None = None
        try:
            self._emit(request, WholeSystemStage.AUDIT, status, {"error_code": error_code, "canonical_effect": "NONE", "transaction_id": transaction_id})
            checkpoint_id = f"{request.run_id}:checkpoint:{self.state.next_sequence(request.run_id) - 1}"
            self.state.save_checkpoint(
                run_id=request.run_id,
                checkpoint_id=checkpoint_id,
                state={
                    "status": status.value,
                    "error_code": error_code,
                    "recalled_memory_ids": list(recalled_ids),
                    "writeback_memory_id": writeback_id,
                    "pending_transaction_id": transaction_id,
                    "provenance_record_id": provenance_record_id,
                    "canonical_effect": "NONE",
                    "deployment": False,
                },
            )
            if transaction_id:
                self.state.mark_writeback_intent(transaction_id, status="COMMITTED", reason="audit and checkpoint persisted")
        except Exception as exc:  # fail closed; pending intent is explicit for deterministic reconciliation
            persistence_error = type(exc).__name__
            checkpoint_id = None
        if persistence_error is not None:
            status = WholeSystemStatus.PENDING_RECONCILIATION if transaction_id else WholeSystemStatus.FAILED
            error_code = error_code or "STATE_PERSISTENCE_FAILED"
            error_detail = error_detail or persistence_error
            writeback_allowed = False
        return WholeSystemResponse(
            run_id=request.run_id,
            status=status,
            text=text if status is WholeSystemStatus.COMPLETED else "",
            error_code=error_code,
            error_detail=error_detail,
            recalled_memory_ids=recalled_ids or (context.recalled_ids if context else ()),
            authorized_memory_contexts=memory_contexts or (context.memory_contexts if context else ()),
            writeback_allowed=writeback_allowed,
            writeback_memory_id=writeback_id,
            pending_transaction_id=transaction_id if persistence_error else None,
            events=self.state.events(request.run_id),
            provenance_record_id=provenance_record_id,
            provenance_status=provenance_status,
            state_checkpoint_id=checkpoint_id,
        )

    def _emit(self, request: WholeSystemRequest, stage: WholeSystemStage, status: WholeSystemStatus, payload: Mapping[str, Any]) -> WholeSystemEvent:
        sequence = self.state.next_sequence(request.run_id)
        return self.state.append(
            WholeSystemEvent(
                event_id=f"{request.run_id}:event-{sequence}",
                run_id=request.run_id,
                sequence=sequence,
                stage=stage,
                status=status,
                payload=dict(payload),
                occurred_at=datetime.now(UTC).isoformat(),
            )
        )

    @staticmethod
    def _check(request: WholeSystemRequest, deadline: float) -> None:
        if request.cancellation is not None and request.cancellation.cancelled:
            raise WholeSystemInterrupted("CANCELLED", "request cancellation was observed at the governed boundary")
        if monotonic() > deadline:
            raise WholeSystemInterrupted("TIMEOUT", "request exceeded the global bounded runtime deadline")
