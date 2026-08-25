from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from aion_evidence_interop import cli
from aion_evidence_interop.canonical import InteropError


COMPONENT = Path(__file__).resolve().parents[1]
ROOT = COMPONENT.parents[1]
RECORD = COMPONENT / "fixtures" / "valid_minimal.json"


def _head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def _result(capsys: pytest.CaptureFixture[str]) -> dict[str, object]:
    captured = capsys.readouterr()
    assert "Traceback" not in captured.out
    assert "Traceback" not in captured.err
    return json.loads(captured.out)


def test_cli_distinguishes_source_validation_failure(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    rc = cli.main(
        [
            "--root",
            str(ROOT),
            "--record",
            "missing.json",
            "--expected-head",
            _head(),
            "--output",
            str(tmp_path / "output"),
        ]
    )
    assert rc == 10
    assert _result(capsys)["error_category"] == "source_validation_failure"


def test_cli_distinguishes_path_confinement_failure(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    outside = tmp_path / "outside.json"
    outside.write_text("{}")
    rc = cli.main(
        [
            "--root",
            str(ROOT),
            "--record",
            str(outside),
            "--expected-head",
            _head(),
            "--output",
            str(tmp_path / "output"),
        ]
    )
    assert rc == 10
    assert _result(capsys)["error_category"] == "path_confinement_failure"


def test_cli_distinguishes_invalid_expected_head(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    rc = cli.main(
        [
            "--root",
            str(ROOT),
            "--record",
            str(RECORD),
            "--expected-head",
            "main",
            "--output",
            str(tmp_path / "output"),
        ]
    )
    assert rc == 10
    assert _result(capsys)["error_category"] == "invalid_expected_head"


def test_cli_distinguishes_write_failure_without_overwrite(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    output = tmp_path / "output"
    output.mkdir()
    (output / "existing.txt").write_text("preserve")
    rc = cli.main(
        [
            "--root",
            str(ROOT),
            "--record",
            str(RECORD),
            "--expected-head",
            _head(),
            "--output",
            str(output),
        ]
    )
    assert rc == 12
    assert _result(capsys)["error_category"] == "write_failure"
    assert (output / "existing.txt").read_text() == "preserve"


def test_cli_distinguishes_policy_boundary_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fail_policy(*args: object, **kwargs: object) -> dict[str, bytes]:
        raise InteropError(
            "interop policy boundary failed closed",
            category="policy_boundary_failure",
        )

    monkeypatch.setattr(cli, "build_bundle", fail_policy)
    rc = cli.main(
        [
            "--root",
            str(ROOT),
            "--record",
            str(RECORD),
            "--expected-head",
            _head(),
            "--output",
            str(tmp_path / "output"),
        ]
    )
    assert rc == 10
    assert _result(capsys)["error_category"] == "policy_boundary_failure"


def test_cli_success_does_not_echo_machine_specific_output_path(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    output = tmp_path / "private-user-path" / "output"
    rc = cli.main(
        [
            "--root",
            str(ROOT),
            "--record",
            str(RECORD),
            "--expected-head",
            _head(),
            "--output",
            str(output),
        ]
    )
    assert rc == 0
    result = _result(capsys)
    assert result["output"] == "WRITTEN"
    assert str(tmp_path) not in json.dumps(result)
