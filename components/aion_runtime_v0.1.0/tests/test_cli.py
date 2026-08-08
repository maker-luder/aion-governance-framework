from __future__ import annotations

import json
from pathlib import Path

import aion_runtime.cli as cli


def base_args(memory_db: Path) -> list[str]:
    return [
        "--memory-db",
        str(memory_db),
        "--runtime-instance-id",
        "AION-I-CLI-001",
        "--memory-stream-id",
        "AION-MEMORY-CLI-001",
        "--event-lineage-id",
        "AION-EVENTS-CLI-001",
        "--canonical-state-reference",
        "AION-CANONICAL-CLI",
        "--genesis-root-id",
        "TWIN-GENESIS-CLI-001",
    ]


def test_status_outputs_bound_runtime_context(tmp_path, capsys):
    result = cli.main([*base_args(tmp_path / "memory.sqlite3"), "status"])
    assert result == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["runtime"] == "AION_RUNTIME_IMPLEMENTATION_CANDIDATE"
    assert payload["runtime_context"]["agent_id"] == "AION"
    assert payload["runtime_context"]["runtime_instance_id"] == "AION-I-CLI-001"


def test_remember_then_recall_round_trip(tmp_path, capsys):
    memory_db = tmp_path / "memory.sqlite3"
    common = base_args(memory_db)

    result = cli.main(
        [
            *common,
            "remember",
            "--memory-id",
            "CLI-MEM-001",
            "--user-id",
            "USER-001",
            "--content",
            "governed memory",
            "--source",
            "cli-test",
            "--topic",
            "runtime",
            "--scope",
            "private",
            "--provenance-verified",
            "--approve-writeback",
        ]
    )
    assert result == 0
    written = json.loads(capsys.readouterr().out)
    assert written == {"memory_id": "CLI-MEM-001", "canonical_effect": "NONE"}

    result = cli.main(
        [
            *common,
            "recall",
            "--user-id",
            "USER-001",
            "--topic",
            "runtime",
            "--scope",
            "private",
            "--limit",
            "4",
        ]
    )
    assert result == 0
    recalled = json.loads(capsys.readouterr().out)
    assert [item["memory_id"] for item in recalled] == ["CLI-MEM-001"]
    assert recalled[0]["namespace"] == "AION-MEMORY-CLI-001"
    assert recalled[0]["provenance_source"] == "cli-test"


def test_serve_delegates_without_starting_real_server(tmp_path, monkeypatch):
    observed: dict[str, object] = {}

    def fake_serve(runtime, *, host: str, port: int, allow_non_loopback: bool) -> None:
        observed["agent_id"] = runtime.context.agent_id
        observed["host"] = host
        observed["port"] = port
        observed["allow_non_loopback"] = allow_non_loopback

    monkeypatch.setattr(cli, "serve", fake_serve)
    result = cli.main(
        [
            *base_args(tmp_path / "memory.sqlite3"),
            "serve",
            "--host",
            "127.0.0.1",
            "--port",
            "8091",
        ]
    )
    assert result == 0
    assert observed == {
        "agent_id": "AION",
        "host": "127.0.0.1",
        "port": 8091,
        "allow_non_loopback": False,
    }
