from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable, Iterable, Mapping

from .deployment import DeploymentEventType, DeploymentLedger
from .loop import AgentRunner, RunBudget, RunResult
from .provider import ProviderAdapter
from .service import RuntimeServiceEnvelope
from .session import SessionContextManager
from .tools import ToolExecutionBridge, ToolRegistry


@dataclass(frozen=True)
class RuntimeV2Status:
    runtime: str = "AION_RUNTIME_V0_2_RESEARCH_CANDIDATE"
    agent_loop: str = "ENABLED_GOVERNED_CANDIDATE"
    model_provider_adapter: str = "ENABLED_LOCAL_FIRST"
    session_context: str = "ENABLED_NONCANONICAL_WORKING_STATE"
    governed_tool_bridge: str = "ENABLED"
    synthetic_executor: str = "ENABLED_FOR_TESTS"
    os_process_sandbox: str = "NOT_IMPLEMENTED"
    deployment_service_envelope: str = "ENABLED_CONTROL_PLANE_CANDIDATE"
    deployment_instance_lineage: str = "ENABLED_RESEARCH_CANDIDATE"
    state_changing_http_api: str = "DISABLED"
    external_framework_runtime_dependency: str = "NONE"
    automatic_remote_model_fallback: str = "DISABLED"
    automatic_canonical_writeback: str = "DISABLED"
    deployment: str = "FALSE"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


class AIONRuntimeV2Candidate:
    """Research-only composition root for the new agent/deployment control plane."""

    def __init__(self, *, provider: ProviderAdapter, registry: ToolRegistry, bridge: ToolExecutionBridge, approval_resolver: Callable[[Any], Mapping[str, Any]], memory_projection: Callable[[str], Iterable[Mapping[str, Any]]] | None = None, max_concurrency: int = 1) -> None:
        self.provider = provider
        self.registry = registry
        self.bridge = bridge
        self.approval_resolver = approval_resolver
        self.memory_projection = memory_projection or (lambda _session_id: ())
        self.service = RuntimeServiceEnvelope(max_concurrency=max_concurrency)
        self.deployments = DeploymentLedger()
        self._sessions: dict[str, SessionContextManager] = {}

    @staticmethod
    def status() -> RuntimeV2Status:
        return RuntimeV2Status()

    def start_service(self) -> None:
        self.service.start()

    def record_deployment(self, *, event_type: DeploymentEventType, deployment_id: str, runtime_instance_id: str, lineage_id: str, source_checkpoint_id: str | None = None, source_lineage_id: str | None = None) -> None:
        self.deployments.append(event_type=event_type, deployment_id=deployment_id, runtime_instance_id=runtime_instance_id, lineage_id=lineage_id, source_checkpoint_id=source_checkpoint_id, source_lineage_id=source_lineage_id)

    def session(self, session_id: str) -> SessionContextManager:
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionContextManager(session_id)
        return self._sessions[session_id]

    def run_turn(self, *, session_id: str, user_input: str, budget: RunBudget | None = None) -> RunResult:
        self.service.begin_request()
        try:
            session = self.session(session_id)
            session.append(kind="message", role="user", content=user_input)
            projection = tuple(self.memory_projection(session_id))
            if projection:
                session.append(kind="runtime_note", role="system", content=f"governed memory projection available: {len(projection)} item(s)", metadata={"memory_projection_count": len(projection)})
            runner = AgentRunner(provider=self.provider, session=session, registry=self.registry, bridge=self.bridge, approval_resolver=self.approval_resolver, budget=budget)
            return runner.run()
        finally:
            self.service.end_request()
