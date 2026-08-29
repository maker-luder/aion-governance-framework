from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_main_transition_authority_receipt as generator  # noqa: E402
import validate_main_transition_authority as gate  # noqa: E402

HEAD = "a" * 40
WHEN = datetime(2026, 8, 28, 8, 30, tzinfo=timezone.utc)


def test_generated_receipt_round_trips_through_authority_validator() -> None:
    record = generator.build_receipt(
        repository="maker-luder/aion-governance-framework",
        target_pr=70,
        target_head=HEAD,
        approval_id="12345678-1234-4234-8234-123456789abc",
        approval_time=WHEN,
    )

    result = gate.validate_record(
        record,
        expected_repository="maker-luder/aion-governance-framework",
        expected_pr=70,
        expected_head=HEAD,
        expected_ref="https://github.com/maker-luder/aion-governance-framework/pull/70",
        approval_event_time=WHEN,
        event_action="edited",
        body_was_edited=True,
        event_sender="maker-luder",
        human_owner_login="maker-luder",
    )

    assert result.status == "PASS"
    rendered = generator.render_receipt(record)
    extracted, error = gate._extract_receipt(rendered)
    assert error is None
    assert extracted == record


def test_cli_writes_deterministic_valid_block(tmp_path: Path) -> None:
    output = tmp_path / "receipt.md"
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate_main_transition_authority_receipt.py"),
            "--pr",
            "70",
            "--head",
            HEAD,
            "--approval-id",
            "12345678-1234-4234-8234-123456789abc",
            "--approval-time",
            "2026-08-28T08:30:00Z",
            "--output",
            str(output),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    record, error = gate._extract_receipt(output.read_text(encoding="utf-8"))
    assert error is None
    assert record is not None
    assert record["target_pr"] == 70
    assert record["target_head"] == HEAD
    assert record["approval_time"] == "2026-08-28T08:30:00Z"


def test_cli_rejects_non_exact_head() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate_main_transition_authority_receipt.py"),
            "--pr",
            "70",
            "--head",
            "not-a-sha",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 2
    assert "exact lowercase 40-hex" in completed.stderr


def test_generated_receipt_conforms_to_schema() -> None:
    from jsonschema import Draft202012Validator, FormatChecker

    record = generator.build_receipt(
        repository="maker-luder/aion-governance-framework",
        target_pr=70,
        target_head=HEAD,
        approval_id="12345678-1234-4234-8234-123456789abc",
        approval_time=WHEN,
    )
    schema = json.loads(
        (ROOT / "schemas" / "main_transition_authority_receipt_v0.1.0.schema.json").read_text(
            encoding="utf-8"
        )
    )

    assert list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record)) == []
