"""Task-bound, expiring approval requests and grants."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from datetime import datetime

from .enums import ApprovalDecision, PermissionLevel, RiskLevel
from .errors import ApprovalError
from .models import ApprovalGrant, ApprovalRequest


def _parse(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ApprovalError("approval timestamp must be ISO-8601") from exc


def approval_request_hash(
    *,
    task_id: str,
    operation_type: PermissionLevel,
    affected_paths: tuple[str, ...],
    proposed_commands: tuple[tuple[str, ...], ...],
    expires_at: str,
) -> str:
    payload = {
        "task_id": task_id,
        "operation_type": operation_type.value,
        "affected_paths": affected_paths,
        "proposed_commands": proposed_commands,
        "expires_at": expires_at,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def create_approval_request(
    *,
    approval_request_id: str,
    task_id: str,
    operation_type: PermissionLevel,
    reason: str,
    affected_paths: tuple[str, ...],
    proposed_commands: tuple[tuple[str, ...], ...],
    expected_effect: str,
    risk_level: RiskLevel,
    data_exposure: str,
    rollback_plan: str,
    requested_at: str,
    expires_at: str,
) -> ApprovalRequest:
    if not task_id or not approval_request_id or _parse(expires_at) <= _parse(requested_at):
        raise ApprovalError("approval request identity or expiry is invalid")
    request_hash = approval_request_hash(
        task_id=task_id,
        operation_type=operation_type,
        affected_paths=affected_paths,
        proposed_commands=proposed_commands,
        expires_at=expires_at,
    )
    return ApprovalRequest(
        approval_request_id=approval_request_id,
        task_id=task_id,
        operation_type=operation_type,
        reason=reason,
        affected_paths=affected_paths,
        proposed_commands=proposed_commands,
        expected_effect=expected_effect,
        risk_level=risk_level,
        data_exposure=data_exposure,
        rollback_plan=rollback_plan,
        requested_at=requested_at,
        expires_at=expires_at,
        request_hash=request_hash,
    )


def grant_approval(
    request: ApprovalRequest,
    *,
    grant_id: str,
    decision: ApprovalDecision,
    approved_by: str,
    approved_at: str,
    conditions: tuple[str, ...] = (),
) -> ApprovalGrant:
    if decision not in {
        ApprovalDecision.APPROVED,
        ApprovalDecision.APPROVED_WITH_CONDITIONS,
    }:
        raise ApprovalError("only an explicit approval decision can create a grant")
    if not approved_by or _parse(approved_at) > _parse(request.expires_at):
        raise ApprovalError("approver is missing or request already expired")
    return ApprovalGrant(
        grant_id=grant_id,
        approval_request_id=request.approval_request_id,
        task_id=request.task_id,
        operation_type=request.operation_type,
        decision=decision,
        conditions=conditions,
        approved_by=approved_by,
        approved_at=approved_at,
        expires_at=request.expires_at,
        request_hash=request.request_hash,
    )


def validate_grant(
    request: ApprovalRequest,
    grant: ApprovalGrant,
    *,
    task_id: str,
    required_permission: PermissionLevel,
    now: str,
) -> None:
    expected = approval_request_hash(
        task_id=request.task_id,
        operation_type=request.operation_type,
        affected_paths=request.affected_paths,
        proposed_commands=request.proposed_commands,
        expires_at=request.expires_at,
    )
    if (
        request.task_id != task_id
        or grant.task_id != task_id
        or grant.approval_request_id != request.approval_request_id
        or request.operation_type is not required_permission
        or grant.operation_type is not required_permission
        or grant.request_hash != request.request_hash
        or request.request_hash != expected
    ):
        raise ApprovalError("approval does not match task, operation or request hash")
    if grant.decision not in {
        ApprovalDecision.APPROVED,
        ApprovalDecision.APPROVED_WITH_CONDITIONS,
    }:
        raise ApprovalError("approval grant is not approved")
    if _parse(now) > _parse(grant.expires_at):
        raise ApprovalError("approval grant expired")


def approval_as_dict(grant: ApprovalGrant) -> dict[str, object]:
    return asdict(grant)
