import json, sys
from aion_governance_kernel.cli import main

def test_cli_outputs_json(monkeypatch,capsys):
    payload={"request_id":"cli-1","source_type":"cli","action":"analyze_document","target":"x","environment":"sandbox","authorization":"none","destructive":False,"network_access":False}
    monkeypatch.setattr(sys,"argv",["prog",json.dumps(payload),"--db",":memory:"])
    assert main()==0
    assert '"decision": "ALLOW"' in capsys.readouterr().out
