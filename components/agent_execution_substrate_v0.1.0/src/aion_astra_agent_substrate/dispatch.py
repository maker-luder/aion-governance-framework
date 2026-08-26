"""Mandatory native-runtime dispatch through the shared AION/Astra substrate."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generic, TypeVar

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
from .native import NATIVE_PROFILE_ID, normalize_trajectory
from .policy import evaluate

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
    """Bounded execution result plus content-minimized substrate evidence."""

    result: T
    binding: RuntimeBinding
    policy_decision: PolicyDecision
    events: tuple[NormalizedEvent, ...]
    receipt_path: Path
    receipt_sha256: str


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


def _load_native_audit(path: Path) -> tuple[Mapping[str, Any], ...]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise SubstrateError("native runtime audit is unreadable") from exc

    records: list[Mapping[str, Any]] = []
    for line in lines:
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
    return tuple(records)


def _status_value(result: Any) -> str:
    status = getattr(result, "status", "")
    return str(getattr(status, "value", status))


def dispatch_native_execution(
    *,
    context: Mapping[str, Any] | Any,
    task_id: str,
    owner_approved: bool,
    authority_reference: str | None,
    network_access: bool,
    execute: Callable[[], T],
    capability: Capability = Capability.SANDBOX_WRITE,
    canonical_effect: str = "NONE",
    deployment: bool = False,
) -> NativeDispatchOutcome[T]:
    """Gate one native bounded execution, then persist normalized trajectory evidence.

    The callable is never invoked unless policy returns ALLOW. The receipt contains
    structural metadata and hashes only; raw prompts, tool payloads, and authority
    reference strings are not copied into it.
    """

    binding = RuntimeBinding.from_runtime_context(
        context,
        substrate_id=NATIVE_PROFILE_ID,
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
    events = normalize_trajectory(_load_native_audit(audit_path), binding=binding)

    output_root = Path(str(getattr(result, "output_root", "")))
    if not output_root.is_dir():
        raise SubstrateError("native runtime output_root is unavailable for substrate receipt")

    request_view = {
        "task_id": task_id,
        "binding": binding.to_dict(),
        "capability": capability.value,
        "owner_approved": owner_approved,
        "network_access": network_access,
        "deployment": deployment,
        "canonical_effect": canonical_effect,
    }
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
    receipt = {
        "schema_version": "0.1.0",
        "record_type": "AION_ASTRA_SUBSTRATE_EXECUTION_RECEIPT",
        "binding": binding.to_dict(),
        "adapter": {
            "adapter_id": "native-bounded-runtime",
            "profile_id": NATIVE_PROFILE_ID,
            "live_dsh_execution": False,
            "network_access": False,
        },
        "policy_decision": decision.to_dict(),
        "authority_reference_sha256": (
            sha256_json(authority_reference) if authority_reference else None
        ),
        "request_sha256": sha256_json(request_view),
        "runtime_result": result_view,
        "runtime_result_sha256": sha256_json(result_view),
        "trajectory_sha256": sha256_json([event.to_dict() for event in events]),
        "normalized_events": [event.to_dict() for event in events],
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

    return NativeDispatchOutcome(
        result=result,
        binding=binding,
        policy_decision=decision,
        events=events,
        receipt_path=receipt_path,
        receipt_sha256=hashlib.sha256(receipt_bytes).hexdigest(),
    )
