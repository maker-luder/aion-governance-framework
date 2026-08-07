
from __future__ import annotations
import sqlite3
from . import repository
from ..models import OperationRequest, RiskDecision

class AuditService:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def record_decision(self, request: OperationRequest, decision: RiskDecision, input_hash: str) -> int:
        with self._connection:
            return repository.write_decision(self._connection, request, decision, input_hash)
