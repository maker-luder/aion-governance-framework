
from __future__ import annotations
import json, sqlite3
from ..models import OperationRequest, RiskDecision

def write_decision(connection: sqlite3.Connection, request: OperationRequest, decision: RiskDecision, input_hash: str) -> int:
    cursor = connection.execute(
        """
        INSERT INTO audit_events (
            request_id,stage,decision,risk_level,status,policy_version,rule_ids,
            source_type,action,target_class,environment,authorization_state,
            input_hash,reason_code,error_code
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            request.request_id, "RISK_GATE", decision.decision.value,
            decision.risk_level.value, "RECORDED", decision.policy_version,
            json.dumps(decision.rule_ids), request.source_type.value,
            request.action.value, decision.target_class, request.environment.value,
            request.authorization.value, input_hash, decision.reason_code, None,
        ),
    )
    if cursor.lastrowid is None:
        raise RuntimeError("audit insert did not return a row id")
    return cursor.lastrowid

def fetch_events(connection: sqlite3.Connection, request_id: str) -> list[dict[str, object]]:
    rows = connection.execute("SELECT * FROM audit_events WHERE request_id=? ORDER BY id", (request_id,)).fetchall()
    return [dict(row) for row in rows]
