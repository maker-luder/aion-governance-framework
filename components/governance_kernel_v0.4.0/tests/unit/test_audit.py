
import sqlite3, pytest
from aion_governance_kernel.audit.db import init_schema, open_database
from aion_governance_kernel.audit.repository import fetch_events
from aion_governance_kernel.audit.service import AuditService
from aion_governance_kernel.errors import SchemaVersionError
from aion_governance_kernel.hashing import canonical_request_hash
from aion_governance_kernel.risk.policy import evaluate_risk
from aion_governance_kernel.validation import validate_operation_request

def request(): return validate_operation_request({"request_id":"audit-1","source_type":"test","action":"read_file","target":"x","environment":"sandbox","authorization":"none","destructive":False,"network_access":False})

def test_schema_and_audit_roundtrip(tmp_path):
    with open_database(str(tmp_path/"a.db")) as c:
        init_schema(c); r=request(); d=evaluate_risk(r)
        event=AuditService(c).record_decision(r,d,canonical_request_hash(r))
        rows=fetch_events(c,r.request_id)
        assert event>0 and rows[0]["policy_version"]==d.policy_version and "GK-ALLOW-READ-001" in rows[0]["rule_ids"]

def test_schema_version_mismatch_fails():
    c=sqlite3.connect(":memory:"); c.row_factory=sqlite3.Row
    c.execute("CREATE TABLE schema_metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL)")
    c.execute("INSERT INTO schema_metadata VALUES('schema_version','999')")
    with pytest.raises(SchemaVersionError): init_schema(c)
    c.close()

def test_database_connection_is_closed(tmp_path):
    path=tmp_path/"closed.db"
    with open_database(str(path)) as c: init_schema(c)
    with pytest.raises(sqlite3.ProgrammingError): c.execute("SELECT 1")
