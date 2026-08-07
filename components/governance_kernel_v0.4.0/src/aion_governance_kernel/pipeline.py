
from __future__ import annotations
from typing import Any, Mapping
from .audit.db import init_schema, open_database
from .audit.service import AuditService
from .errors import AuditDatabaseError, InputValidationError, RiskEvaluationError, SchemaVersionError
from .hashing import canonical_request_hash
from .models import Decision, PipelineResponse, RiskLevel
from .risk.policy import evaluate_risk
from .validation import validate_operation_request

def _failed(request_id: str, reason: str, error: str) -> dict[str, object]:
    return PipelineResponse(
        request_id=request_id, decision=Decision.STOP.value,
        risk_level=RiskLevel.CRITICAL.value, status="FAILED_CLOSED",
        reason_code=reason, policy_version=None, rule_ids=(),
        audit_event_id=None, input_hash=None, error_code=error,
    ).as_dict()

def run_pipeline(request_payload: Mapping[str, Any], db_path: str) -> dict[str, object]:
    fallback_id = request_payload.get("request_id", "UNAVAILABLE") if isinstance(request_payload, Mapping) else "UNAVAILABLE"
    fallback_id = fallback_id if isinstance(fallback_id, str) else "UNAVAILABLE"
    try:
        request = validate_operation_request(request_payload)
    except InputValidationError:
        return _failed(fallback_id, "INPUT_VALIDATION_FAILED", "INPUT_VALIDATION_FAILED")

    input_hash = canonical_request_hash(request)
    try:
        decision = evaluate_risk(request)
    except Exception:
        return _failed(request.request_id, "RISK_EVALUATION_FAILED", "RISK_EVALUATION_FAILED")

    try:
        with open_database(db_path) as connection:
            init_schema(connection)
            event_id = AuditService(connection).record_decision(request, decision, input_hash)
    except SchemaVersionError:
        return _failed(request.request_id, "AUDIT_SCHEMA_VERSION_FAILED", "AUDIT_SCHEMA_VERSION_FAILED")
    except AuditDatabaseError:
        return _failed(request.request_id, "AUDIT_DATABASE_FAILED", "AUDIT_DATABASE_FAILED")
    except Exception:
        return _failed(request.request_id, "AUDIT_WRITE_FAILED", "AUDIT_WRITE_FAILED")

    return PipelineResponse(
        request_id=request.request_id,
        decision=decision.decision.value,
        risk_level=decision.risk_level.value,
        status="COMPLETED",
        reason_code=decision.reason_code,
        policy_version=decision.policy_version,
        rule_ids=decision.rule_ids,
        audit_event_id=event_id,
        input_hash=input_hash,
    ).as_dict()
