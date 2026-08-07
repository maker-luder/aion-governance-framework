"""Read-only self-host HTTP entry point for the AION Runtime candidate."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Type
from urllib.parse import urlparse

from .runtime import AIONRuntime

_LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}


def handler_for(runtime: AIONRuntime) -> Type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        server_version = "AIONRuntime/0.1.0"

        def _send_json(self, status: int, payload: object) -> None:
            body = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
            path = urlparse(self.path).path
            if path == "/healthz":
                self._send_json(200, {"status": "ok", "service": "aion-runtime"})
                return
            if path == "/v1/status":
                self._send_json(200, runtime.status().to_dict())
                return
            self._send_json(404, {"error": "not_found"})

        def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
            self._send_json(
                405,
                {
                    "error": "state_changing_http_disabled",
                    "reason": "public/self-host HTTP surface is read-only in v0.1.0",
                },
            )

        def log_message(self, format: str, *args: object) -> None:
            return

    return Handler


def serve(
    runtime: AIONRuntime,
    *,
    host: str = "127.0.0.1",
    port: int = 8080,
    allow_non_loopback: bool = False,
) -> None:
    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    if host not in _LOOPBACK_HOSTS and not allow_non_loopback:
        raise ValueError("non-loopback binding requires explicit allow_non_loopback=True")
    httpd = ThreadingHTTPServer((host, port), handler_for(runtime))
    try:
        httpd.serve_forever()
    finally:
        httpd.server_close()
