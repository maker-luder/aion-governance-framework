
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Mapping

class SourceType(str, Enum):
    API = "API"
    CLI = "CLI"
    USER = "USER"
    INTERNAL = "INTERNAL"
    TEST = "TEST"

class ActionType(str, Enum):
    ANALYZE_DOCUMENT = "ANALYZE_DOCUMENT"
    READ_FILE = "READ_FILE"
    WRITE_FILE = "WRITE_FILE"
    MODIFY_PROJECT = "MODIFY_PROJECT"
    RUN_TESTS = "RUN_TESTS"
    NETWORK_REQUEST = "NETWORK_REQUEST"
    ACCESS_CREDENTIALS = "ACCESS_CREDENTIALS"
    DELETE_DATA = "DELETE_DATA"
    DISABLE_LOGGING = "DISABLE_LOGGING"
    BYPASS_AUDIT = "BYPASS_AUDIT"
    UNKNOWN = "UNKNOWN"

class Environment(str, Enum):
    SANDBOX = "SANDBOX"
    PROJECT_WORKTREE = "PROJECT_WORKTREE"
    PRODUCTION = "PRODUCTION"

class AuthorizationState(str, Enum):
    NONE = "NONE"
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"

class Decision(str, Enum):
    ALLOW = "ALLOW"
    REQUIRE_HUMAN = "REQUIRE_HUMAN"
    STOP = "STOP"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass(frozen=True, slots=True)
class OperationRequest:
    request_id: str
    source_type: SourceType
    action: ActionType
    target: str
    environment: Environment
    authorization: AuthorizationState
    destructive: bool
    network_access: bool
    description: str
    metadata: Mapping[str, str]
    created_at: str

    @staticmethod
    def freeze_metadata(value: Mapping[str, str]) -> Mapping[str, str]:
        return MappingProxyType(dict(value))

@dataclass(frozen=True, slots=True)
class RiskDecision:
    decision: Decision
    risk_level: RiskLevel
    policy_version: str
    rule_ids: tuple[str, ...]
    reason_code: str
    target_class: str

@dataclass(frozen=True, slots=True)
class PipelineResponse:
    request_id: str
    decision: str
    risk_level: str
    status: str
    reason_code: str
    policy_version: str | None
    rule_ids: tuple[str, ...]
    audit_event_id: int | None
    input_hash: str | None
    error_code: str | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "request_id": self.request_id,
            "decision": self.decision,
            "risk_level": self.risk_level,
            "status": self.status,
            "reason_code": self.reason_code,
            "policy_version": self.policy_version,
            "rule_ids": list(self.rule_ids),
            "audit_event_id": self.audit_event_id,
            "input_hash": self.input_hash,
            "error_code": self.error_code,
        }
