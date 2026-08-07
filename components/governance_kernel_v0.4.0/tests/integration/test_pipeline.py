
import sqlite3
from aion_governance_kernel.audit.db import init_schema, open_database
from aion_governance_kernel.audit.repository import fetch_events
from aion_governance_kernel.pipeline import run_pipeline

def request(**kw):
    d={"request_id":"pipe-1","source_type":"api","action":"analyze_document","target":"report.md","environment":"sandbox","authorization":"none","destructive":False,"network_access":False,"description":"malware analysis"}; d.update(kw); return d

def test_pipeline_allows_nonexecuting_analysis_and_records_audit(tmp_path):
    db=tmp_path/"p.db"; result=run_pipeline(request(),str(db))
    assert result["decision"]=="ALLOW" and result["status"]=="COMPLETED" and result["audit_event_id"]
    with open_database(str(db)) as c:
        init_schema(c); rows=fetch_events(c,"pipe-1")
        assert len(rows)==1 and rows[0]["action"]=="ANALYZE_DOCUMENT"

def test_pipeline_unknown_action_requires_human(tmp_path):
    result=run_pipeline(request(action="do_something_new"),str(tmp_path/"u.db"))
    assert result["decision"]=="REQUIRE_HUMAN"

def test_pipeline_rejects_invalid_input_fail_closed(tmp_path):
    result=run_pipeline(request(source_type="bad"),str(tmp_path/"v.db"))
    assert result["decision"]=="STOP" and result["status"]=="FAILED_CLOSED" and result["error_code"]=="INPUT_VALIDATION_FAILED"

def test_pipeline_database_open_failure_is_controlled(tmp_path):
    bad=tmp_path/"missing"/"db.sqlite"
    result=run_pipeline(request(),str(bad))
    assert result["decision"]=="STOP" and result["error_code"]=="AUDIT_DATABASE_FAILED"

def test_pipeline_schema_version_failure_is_controlled(tmp_path):
    path=tmp_path/"version.db"
    c=sqlite3.connect(path); c.execute("CREATE TABLE schema_metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL)"); c.execute("INSERT INTO schema_metadata VALUES('schema_version','999')"); c.commit(); c.close()
    result=run_pipeline(request(),str(path))
    assert result["error_code"]=="AUDIT_SCHEMA_VERSION_FAILED"

def test_approved_project_change_is_allowed(tmp_path):
    result=run_pipeline(request(action="modify_project",environment="project_worktree",authorization="approved"),str(tmp_path/"a.db"))
    assert result["decision"]=="ALLOW" and result["risk_level"]=="MEDIUM"

def test_production_change_is_stopped(tmp_path):
    result=run_pipeline(request(action="modify_project",environment="production",authorization="approved"),str(tmp_path/"s.db"))
    assert result["decision"]=="STOP" and result["reason_code"]=="PRODUCTION_MUTATION_FORBIDDEN"
