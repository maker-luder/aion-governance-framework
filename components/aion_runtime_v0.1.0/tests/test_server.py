from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

import pytest

from aion_runtime.runtime import AIONRuntime
from aion_runtime.server import handler_for, serve


def test_handler_exposes_read_only_health_and_status(tmp_path):
    runtime = AIONRuntime(memory_db=tmp_path / "memory.sqlite3")
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(runtime))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address
    connection = HTTPConnection(host, port, timeout=2)
    try:
        connection.request("GET", "/healthz")
        health = connection.getresponse()
        assert health.status == 200
        assert json.loads(health.read())["status"] == "ok"

        connection.request("GET", "/v1/status")
        status = connection.getresponse()
        payload = json.loads(status.read())
        assert status.status == 200
        assert payload["runtime"] == "AION_RUNTIME_IMPLEMENTATION_CANDIDATE"
        assert payload["public_ablation_execution"] == "DISABLED"

        connection.request("POST", "/v1/status", body=b"{}")
        denied = connection.getresponse()
        denied_payload = json.loads(denied.read())
        assert denied.status == 405
        assert denied_payload["error"] == "state_changing_http_disabled"
    finally:
        connection.close()
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def test_non_loopback_requires_explicit_opt_in(tmp_path):
    runtime = AIONRuntime(memory_db=tmp_path / "memory.sqlite3")
    with pytest.raises(ValueError, match="non-loopback"):
        serve(runtime, host="0.0.0.0", port=8080)
