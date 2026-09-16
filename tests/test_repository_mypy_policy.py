from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_repository_mypy.py"
DISCOVERY_ROOTS = ["components", "examples", "experiments", "research-labs"]


def _write_toolchains(root: Path) -> None:
    ci = root / ".github" / "ci"
    ci.mkdir(parents=True, exist_ok=True)
    for name in ("quality-toolchain.txt", "runtime-strong-qa-toolchain.txt"):
        (ci / name).write_text("mypy==2.3.1\n", encoding="utf-8")


def _write_project(root: Path, relative: str, *, strict: bool | None) -> None:
    package_root = root / relative
    (package_root / "src" / "sample_pkg").mkdir(parents=True, exist_ok=True)
    (package_root / "src" / "sample_pkg" / "__init__.py").write_text(
        "VALUE: int = 1\n", encoding="utf-8"
    )
    content = [
        "[project]",
        'name = "sample-pkg"',
        'version = "0.1.0"',
        'requires-python = ">=3.11"',
    ]
    if strict is not None:
        content.extend(["", "[tool.mypy]", 'python_version = "3.11"'])
        if strict:
            content.append("strict = true")
    (package_root / "pyproject.toml").write_text(
        "\n".join(content) + "\n", encoding="utf-8"
    )


def _write_policy(root: Path, packages: list[dict[str, object]]) -> None:
    for discovery_root in DISCOVERY_ROOTS:
        (root / discovery_root).mkdir(parents=True, exist_ok=True)
    policy = {
        "schema_version": "0.1.0",
        "mypy_version": "2.3.1",
        "discovery_roots": DISCOVERY_ROOTS,
        "packages": packages,
    }
    path = root / ".github" / "ci" / "mypy-policy.json"
    path.write_text(json.dumps(policy, indent=2) + "\n", encoding="utf-8")


def _validate(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(root),
            "--policy",
            ".github/ci/mypy-policy.json",
            "--validate-only",
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def test_policy_accepts_explicit_strict_and_exempt_dispositions(tmp_path: Path) -> None:
    _write_toolchains(tmp_path)
    _write_project(tmp_path, "components/strict_pkg", strict=True)
    _write_project(tmp_path, "research-labs/exempt_pkg", strict=None)
    _write_policy(
        tmp_path,
        [
            {
                "root": "components/strict_pkg",
                "disposition": "MYPY_REQUIRED_STRICT",
                "config": "pyproject.toml",
                "target": "src",
            },
            {
                "root": "research-labs/exempt_pkg",
                "disposition": "EXEMPT_WITH_EXPLICIT_REASON",
                "reason": (
                    "Baseline package intentionally remains outside executable mypy "
                    "coverage until a typed migration is completed."
                ),
            },
        ],
    )

    completed = _validate(tmp_path)

    assert completed.returncode == 0, completed.stderr
    assert "MYPY_POLICY_VALIDATION=PASS" in completed.stdout
    assert "MYPY_POLICY_STRICT_COUNT=1" in completed.stdout
    assert "MYPY_POLICY_EXEMPT_COUNT=1" in completed.stdout


def test_policy_fails_closed_when_new_package_has_no_disposition(tmp_path: Path) -> None:
    _write_toolchains(tmp_path)
    _write_project(tmp_path, "components/known_pkg", strict=True)
    _write_project(tmp_path, "components/unclassified_pkg", strict=True)
    _write_policy(
        tmp_path,
        [
            {
                "root": "components/known_pkg",
                "disposition": "MYPY_REQUIRED_STRICT",
                "config": "pyproject.toml",
                "target": "src",
            }
        ],
    )

    completed = _validate(tmp_path)

    assert completed.returncode == 2
    assert "unclassified packages: components/unclassified_pkg" in completed.stderr


def test_strict_disposition_requires_strict_mypy_config(tmp_path: Path) -> None:
    _write_toolchains(tmp_path)
    _write_project(tmp_path, "components/not_strict", strict=False)
    _write_policy(
        tmp_path,
        [
            {
                "root": "components/not_strict",
                "disposition": "MYPY_REQUIRED_STRICT",
                "config": "pyproject.toml",
                "target": "src",
            }
        ],
    )

    completed = _validate(tmp_path)

    assert completed.returncode == 2
    assert "strict disposition requires strict = true" in completed.stderr
