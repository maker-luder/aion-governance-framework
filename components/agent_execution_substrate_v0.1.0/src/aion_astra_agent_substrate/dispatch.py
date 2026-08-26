"""Mandatory registry-backed dispatch through the shared AION/Astra substrate."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generic, TypeVar

from .durable import (
    DurableLogSummary,
    persist_execution_event_log,
    persist_execution_evidence,
)
from .models import (
    Capability,
    Decision,
    NormalizedEvent,
    PolicyDecision,
    PolicyRequest,
    RuntimeBinding,
    SubstrateError,
    canonical_json_bytes,
    sha256_json,
)
from .native import normalize_trajectory
from .policy import evaluate
from .registry import (
    NATIVE_ADAPTER_ID,
    NATIVE_EXECUTION_KIND,
    AdapterRegistration,
    AdapterRegistry,
    AdapterRegistryError,
    build_default_registry,
)

T = TypeVar("T")
RECEIPT_FILENAME = "substrate_execution_receipt.json"


class SubstratePolicyHold(SubstrateError):
    """Raised before execution when the mandatory substrate policy returns HOLD."""

    def __init__(self, decision: PolicyDecision) -> None:
        self.decision = decision
        reasons = "; ".join(decision.reasons) or "unspecified substrate policy hold"
        super().__init__(f"substrate policy HOLD for {decision.capability.value}: {reasons}")


@dataclass(frozen=True, slots=True)
class NativeDispatchOutcome(Generic[T]):
    """Bounded execution result plus content-minimized durable substrate evidence."""

    result: T
    binding: RuntimeBinding
    policy_decision: PolicyDecision
    events: tuple[NormalizedEvent, ...]
    adapter: AdapterRegistration
    receipt_path: Path
    receipt_sha256: str
    event_log_path: Path
    event_log_sha256: str
    evidence_path: Path
    evidence_sha256: str


def _context_mapping(context: Mapping[str, Any] | Any) -> Mapping[str, Any]:
    if isinstance(context, Mapping):
        return context
    if hasattr(context, "to_dict"):
        converted = context.to_dict()
        if isinstance(converted, Mapping):
            return converted
    raise SubstrateError("runtime context must be a mapping or expose to_dict()")


def _session_id(context: Mapping[str, Any] | Any, task_id: str) -> str:
    raw = _context_mapping(context)
    runtime_instance_id = str(raw.get("runtime_instance_id", "")).strip()
    if not runtime_instance_id:
        raise SubstrateError("runtime_instance_id is required for substrate dispatch")
    if not task_id.strip():
        raise SubstrateError("task_id is required for substrate dispatch")
    return f"{runtime_instance_id}:{task_id}"


def _load_native_audit(path: Path) -> tuple[tuple[Mapping[str, Any], ...], bytes]:
    try:
        raw_bytes = path.read_bytes()
        text = raw_bytes.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise SubstrateError("native runtime audit is unreadable") from exc

    records: list[Mapping[str, Any]] = []
    for line in text.splitlines():
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SubstrateError("native runtime audit contains invalid JSON") from exc
        if not isinstance(record, Mapping):
            raise SubstrateError("native runtime audit records must be objects")
        records.append(record)
    if not records:
        raise SubstrateError("native runtime audit contains no durable events")
    return tuple(records), raw_bytes


def _status_value(result: Any) -> str:
    status = getattr(result, "status", "")
    return str(getattr(status, "value", status))


class SubstrateDispatcher:
    """Shared AION/Astra dispatcher with deterministic adapter selection."""

    def __init__(self, registry: AdapterRegistry | None = None) -> None:
        self.registry = registry or build_default_registry()

    def dispatch_native(
        self,
        *,
        context: Mapping[str, Any] | Any,
        task_id: str,
        owner_approved: bool,
        authority_reference: str | None,
        network_access: bool,
        execute: Callable[[], T],
        adapter_id: str = NATIVE_ADAPTER_ID,
        capability: Capability = Capability.SANDBOX_WRITE,
        canonical_effect: str = "NONE",
        deployment: bool = False,
    ) -> NativeDispatchOutcome[T]:
        """Resolve one registered adapter, gate it, execute it, and close evidence."""

        registration = self.registry.resolve(adapter_id, require_executable=True)
        if registration.execution_kind != NATIVE_EXECUTION_KIND:
            raise AdapterRegistryError(
                f"registered adapter cannot service native bounded execution: {adapter_id}"
            )

        binding = RuntimeBinding.from_runtime_context(
            context,
            substrate_id=registration.profile_id,
            session_id=_session_id(context, task_id),
        )
        request = PolicyRequest(
            binding=binding,
            capability=capability,
            owner_approved=owner_approved,
            authority_reference=authority_reference,
            network_access=network_access,
            deployment=deployment,
            canonical_effect=canonical_effect,
        )
        decision = evaluate(request)
        if decision.decision is Decision.HOLD:
            raise SubstratePolicyHold(decision)

        result = execute()

        if getattr(result, "audit_chain_valid", False) is not True:
            raise SubstrateError("native runtime audit chain was not verified")
        if str(getattr(result, "canonical_effect", "NONE")) != "NONE":
            raise SubstrateError("native runtime result attempted a canonical effect")
        if bool(getattr(result, "deployment", False)):
            raise SubstrateError("native runtime result attempted deployment")

        audit_path = Path(str(getattr(result, "audit_path", "")))
        raw_audit, audit_bytes = _load_native_audit(audit_path)
        events = normalize_trajectory(raw_audit, binding=binding)

        output_root = Path(str(getattr(result, "output_root", "")))
        if not output_root.is_dir():
            raise SubstrateError("native runtime output_root is unavailable for substrate evidence")

        registry_snapshot = self.registry.snapshot()
        registry_snapshot_sha256 = sha256_json(registry_snapshot)
        request_view = {
            "task_id": task_id,
            "binding": binding.to_dict(),
            "adapter_id": registration.adapter_id,
            "registry_snapshot_sha256": registry_snapshot_sha256,
            "capability": capability.value,
            "owner_approved": owner_approved,
            "network_access": network_access,
            "deployment": deployment,
            "canonical_effect": canonical_effect,
        }
        request_sha256 = sha256_json(request_view)
        result_view = {
            "task_id": str(getattr(result, "task_id", task_id)),
            "status": _status_value(result),
            "steps_executed": int(getattr(result, "steps_executed", 0)),
            "output_sha256": getattr(result, "output_sha256", None),
            "audit_chain_valid": bool(getattr(result, "audit_chain_valid", False)),
            "baseline_unchanged": bool(getattr(result, "baseline_unchanged", False)),
            "canonical_effect": str(getattr(result, "canonical_effect", "NONE")),
            "deployment": bool(getattr(result, "deployment", False)),
        }
        runtime_result_sha256 = sha256_json(result_view)
        policy_decision_sha256 = sha256_json(decision.to_dict())
        trajectory_sha256 = sha256_json([event.to_dict() for event in events])
        runtime_audit_sha256 = hashlib.sha256(audit_bytes).hexdigest()

        durable_log: DurableLogSummary = persist_execution_event_log(
            output_root,
            (
                (
                    "substrate.dispatch.requested",
                    {
                        "task_id": task_id,
                        "agent_id": binding.agent_id.value,
                        "runtime_instance_id": binding.runtime_instance_id,
                        "session_id": binding.session_id,
                        "request_sha256": request_sha256,
                    },
                ),
                (
                    "substrate.adapter.resolved",
                    {
                        "adapter_id": registration.adapter_id,
                        "profile_id": registration.profile_id,
                        "execution_kind": registration.execution_kind,
                        "registry_snapshot_sha256": registry_snapshot_sha256,
                    },
                ),
                (
                    "substrate.policy.allowed",
                    {
                        "decision": decision.decision.value,
                        "capability": decision.capability.value,
                        "policy_decision_sha256": policy_decision_sha256,
                    },
                ),
                (
                    "substrate.adapter.completed",
                    {
                        "status": result_view["status"],
                        "steps_executed": result_view["steps_executed"],
                        "runtime_audit_sha256": runtime_audit_sha256,
                        "runtime_result_sha256": runtime_result_sha256,
                    },
                ),
                (
                    "substrate.trajectory.normalized",
                    {
                        "normalized_event_count": len(events),
                        "trajectory_sha256": trajectory_sha256,
                    },
                ),
            ),
        )

        evidence_path, evidence_sha256 = persist_execution_evidence(
            output_root,
            binding=binding.to_dict(),
            adapter=registration.to_dict(),
            registry_snapshot_sha256=registry_snapshot_sha256,
            policy_decision_sha256=policy_decision_sha256,
            request_sha256=request_sha256,
            runtime_audit_sha256=runtime_audit_sha256,
            runtime_result_sha256=runtime_result_sha256,
            trajectory_sha256=trajectory_sha256,
            event_log=durable_log,
            receipt_filename=RECEIPT_FILENAME,
        )

        receipt = {
            "schema_version": "0.1.0",
            "record_type": "AION_ASTRA_SUBSTRATE_EXECUTION_RECEIPT",
            "binding": binding.to_dict(),
            "adapter": registration.to_dict(),
            "registry_snapshot_sha256": registry_snapshot_sha256,
            "policy_decision": decision.to_dict(),
            "policy_decision_sha256": policy_decision_sha256,
            "authority_reference_sha256": (
                sha256_json(authority_reference) if authority_reference else None
            ),
            "request_sha256": request_sha256,
            "runtime_audit_sha256": runtime_audit_sha256,
            "runtime_result": result_view,
            "runtime_result_sha256": runtime_result_sha256,
            "trajectory_sha256": trajectory_sha256,
            "normalized_events": [event.to_dict() for event in events],
            "durable_event_log": durable_log.to_dict(),
            "evidence_envelope": {
                "path": evidence_path.name,
                "sha256": evidence_sha256,
                "record_type": "AION_ASTRA_SUBSTRATE_EXECUTION_EVIDENCE",
            },
            "boundaries": {
                "canonical_effect": "NONE",
                "deployment": False,
                "network_access": False,
                "live_dsh_execution": False,
                "subjectivity_conclusion": "NOT_ESTABLISHED",
                "consciousness_conclusion": "NOT_ESTABLISHED",
                "identity_continuity_conclusion": "NOT_ESTABLISHED",
                "independent_ivv": "NOT_ACHIEVED",
            },
        }
        receipt_bytes = canonical_json_bytes(receipt) + b"\n"
        receipt_path = output_root / RECEIPT_FILENAME
        try:
            receipt_path.write_bytes(receipt_bytes)
        except OSError as exc:
            raise SubstrateError("substrate execution receipt could not be persisted") from exc
        receipt_sha256 = hashlib.sha256(receipt_bytes).hexdigest()

        return NativeDispatchOutcome(
            result=result,
            binding=binding,
            policy_decision=decision,
            events=events,
            adapter=registration,
            receipt_path=receipt_path,
            receipt_sha256=receipt_sha256,
            event_log_path=durable_log.path,
            event_log_sha256=durable_log.sha256,
            evidence_path=evidence_path,
            evidence_sha256=evidence_sha256,
        )


def dispatch_native_execution(
    *,
    context: Mapping[str, Any] | Any,
    task_id: str,
    owner_approved: bool,
    authority_reference: str | None,
    network_access: bool,
    execute: Callable[[], T],
    adapter_id: str = NATIVE_ADAPTER_ID,
    registry: AdapterRegistry | None = None,
    capability: Capability = Capability.SANDBOX_WRITE,
    canonical_effect: str = "NONE",
    deployment: bool = False,
) -> NativeDispatchOutcome[T]:
    """Compatibility entry point used by both AIONRuntime and AstraRuntime."""

    return SubstrateDispatcher(registry).dispatch_native(
        context=context,
        task_id=task_id,
        owner_approved=owner_approved,
        authority_reference=authority_reference,
        network_access=network_access,
        execute=execute,
        adapter_id=adapter_id,
        capability=capability,
        canonical_effect=canonical_effect,
        deployment=deployment,
    )
