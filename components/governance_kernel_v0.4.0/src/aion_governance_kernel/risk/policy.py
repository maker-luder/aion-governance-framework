
from __future__ import annotations
from ..models import ActionType, AuthorizationState, Decision, Environment, OperationRequest, RiskDecision, RiskLevel

POLICY_VERSION = "AION-RISK-POLICY-0.4.0"

def _target_class(action: ActionType) -> str:
    return {
        ActionType.ANALYZE_DOCUMENT: "DOCUMENT",
        ActionType.READ_FILE: "FILE",
        ActionType.WRITE_FILE: "FILE",
        ActionType.MODIFY_PROJECT: "PROJECT",
        ActionType.RUN_TESTS: "TEST_EXECUTION",
        ActionType.NETWORK_REQUEST: "NETWORK",
        ActionType.ACCESS_CREDENTIALS: "CREDENTIALS",
        ActionType.DELETE_DATA: "DATA",
        ActionType.DISABLE_LOGGING: "AUDIT_SYSTEM",
        ActionType.BYPASS_AUDIT: "AUDIT_SYSTEM",
        ActionType.UNKNOWN: "UNKNOWN",
    }[action]

def _decision(
    decision: Decision,
    level: RiskLevel,
    rule: str,
    reason: str,
    target: str,
) -> RiskDecision:
    return RiskDecision(decision, level, POLICY_VERSION, (rule,), reason, target)

def evaluate_risk(request: OperationRequest) -> RiskDecision:
    target = _target_class(request.action)
    if request.action in {ActionType.DISABLE_LOGGING, ActionType.BYPASS_AUDIT}:
        return _decision(Decision.STOP, RiskLevel.CRITICAL, "GK-STOP-AUDIT-001", "AUDIT_BYPASS_FORBIDDEN", target)
    if request.action is ActionType.ACCESS_CREDENTIALS:
        return _decision(Decision.STOP, RiskLevel.CRITICAL, "GK-STOP-CREDENTIAL-001", "CREDENTIAL_ACCESS_FORBIDDEN", target)
    if request.environment is Environment.PRODUCTION and (request.destructive or request.action in {ActionType.DELETE_DATA, ActionType.MODIFY_PROJECT, ActionType.WRITE_FILE}):
        return _decision(Decision.STOP, RiskLevel.CRITICAL, "GK-STOP-PRODUCTION-001", "PRODUCTION_MUTATION_FORBIDDEN", target)
    if request.action is ActionType.DELETE_DATA or request.destructive:
        return _decision(Decision.REQUIRE_HUMAN, RiskLevel.HIGH, "GK-REVIEW-DESTRUCTIVE-001", "DESTRUCTIVE_ACTION_REQUIRES_REVIEW", target)
    if request.action is ActionType.NETWORK_REQUEST or request.network_access:
        return _decision(Decision.REQUIRE_HUMAN, RiskLevel.HIGH, "GK-REVIEW-NETWORK-001", "NETWORK_ACCESS_REQUIRES_REVIEW", target)
    if request.action is ActionType.UNKNOWN:
        return _decision(Decision.REQUIRE_HUMAN, RiskLevel.MEDIUM, "GK-REVIEW-UNKNOWN-001", "UNKNOWN_ACTION_REQUIRES_REVIEW", target)
    if request.action in {ActionType.WRITE_FILE, ActionType.MODIFY_PROJECT, ActionType.RUN_TESTS}:
        if request.environment in {Environment.SANDBOX, Environment.PROJECT_WORKTREE} and request.authorization is AuthorizationState.APPROVED:
            return _decision(Decision.ALLOW, RiskLevel.MEDIUM, "GK-ALLOW-APPROVED-WRITE-001", "APPROVED_SANDBOX_MUTATION", target)
        return _decision(Decision.REQUIRE_HUMAN, RiskLevel.MEDIUM, "GK-REVIEW-WRITE-001", "MUTATION_REQUIRES_APPROVAL", target)
    if request.action is ActionType.READ_FILE and request.environment is Environment.PRODUCTION:
        return _decision(Decision.REQUIRE_HUMAN, RiskLevel.MEDIUM, "GK-REVIEW-PRODUCTION-READ-001", "PRODUCTION_READ_REQUIRES_REVIEW", target)
    if request.action is ActionType.READ_FILE:
        return _decision(Decision.ALLOW, RiskLevel.LOW, "GK-ALLOW-READ-001", "SANDBOX_READ_ALLOWED", target)
    return _decision(Decision.ALLOW, RiskLevel.LOW, "GK-ALLOW-ANALYSIS-001", "NON_EXECUTING_ANALYSIS_ALLOWED", target)
