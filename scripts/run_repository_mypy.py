#!/usr/bin/env python3
"""Validate repository mypy dispositions and execute required package checks.

The policy is intentionally fail-closed for package discovery: every pyproject.toml
under the configured discovery roots must have exactly one explicit disposition.
Existing exemptions are visible debt, not evidence of a repository-wide mypy pass.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tomllib
from typing import Any

ALLOWED_DISPOSITIONS = {
    "MYPY_REQUIRED_STRICT",
    "MYPY_REQUIRED_CONFIGURED",
    "EXEMPT_WITH_EXPLICIT_REASON",
}
REQUIRED_DISPOSITIONS = {
    "MYPY_REQUIRED_STRICT",
    "MYPY_REQUIRED_CONFIGURED",
}
TOOLCHAIN_FILES = (
    Path(".github/ci/quality-toolchain.txt"),
    Path(".github/ci/runtime-strong-qa-toolchain.txt"),
)


class PolicyError(RuntimeError):
    """Raised when repository mypy governance is incomplete or inconsistent."""


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise PolicyError(f"policy must be a JSON object: {path}")
    return data


def _read_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    if not isinstance(data, dict):
        raise PolicyError(f"TOML root must be a table: {path}")
    return data


def discover_packages(root: Path, discovery_roots: list[str]) -> set[str]:
    discovered: set[str] = set()
    for relative_root in discovery_roots:
        base = root / relative_root
        if not base.is_dir():
            raise PolicyError(f"discovery root does not exist: {relative_root}")
        for pyproject in base.rglob("pyproject.toml"):
            if any(part.startswith(".") for part in pyproject.relative_to(root).parts):
                continue
            discovered.add(pyproject.parent.relative_to(root).as_posix())
    return discovered


def _policy_entries(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw_entries = policy.get("packages")
    if not isinstance(raw_entries, list) or not raw_entries:
        raise PolicyError("policy packages must be a non-empty list")

    entries: dict[str, dict[str, Any]] = {}
    for raw in raw_entries:
        if not isinstance(raw, dict):
            raise PolicyError("each package policy entry must be an object")
        package_root = raw.get("root")
        if not isinstance(package_root, str) or not package_root:
            raise PolicyError("each package policy entry requires a non-empty root")
        if package_root in entries:
            raise PolicyError(f"duplicate package policy entry: {package_root}")
        entries[package_root] = raw
    return entries


def _validate_toolchain_pins(root: Path, expected_version: str) -> None:
    expected = f"mypy=={expected_version}"
    for relative_path in TOOLCHAIN_FILES:
        path = root / relative_path
        if not path.is_file():
            raise PolicyError(f"missing QA toolchain file: {relative_path.as_posix()}")
        pins = {
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        if expected not in pins:
            raise PolicyError(
                f"{relative_path.as_posix()} must contain exact pin {expected}"
            )


def validate_policy(root: Path, policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    schema_version = policy.get("schema_version")
    if schema_version != "0.1.0":
        raise PolicyError(f"unsupported policy schema_version: {schema_version!r}")

    mypy_version = policy.get("mypy_version")
    if not isinstance(mypy_version, str) or not mypy_version:
        raise PolicyError("policy requires a non-empty mypy_version")

    raw_discovery_roots = policy.get("discovery_roots")
    if not isinstance(raw_discovery_roots, list) or not raw_discovery_roots:
        raise PolicyError("policy discovery_roots must be a non-empty list")
    if not all(isinstance(item, str) and item for item in raw_discovery_roots):
        raise PolicyError("every discovery root must be a non-empty string")
    discovery_roots = list(raw_discovery_roots)

    entries = _policy_entries(policy)
    discovered = discover_packages(root, discovery_roots)
    declared = set(entries)
    missing = sorted(discovered - declared)
    stale = sorted(declared - discovered)
    if missing or stale:
        parts: list[str] = []
        if missing:
            parts.append("unclassified packages: " + ", ".join(missing))
        if stale:
            parts.append("policy entries without pyproject.toml: " + ", ".join(stale))
        raise PolicyError("; ".join(parts))

    for package_root, entry in sorted(entries.items()):
        disposition = entry.get("disposition")
        if disposition not in ALLOWED_DISPOSITIONS:
            raise PolicyError(
                f"{package_root}: invalid disposition {disposition!r}; "
                f"allowed={sorted(ALLOWED_DISPOSITIONS)}"
            )

        absolute_root = root / package_root
        if not absolute_root.is_dir():
            raise PolicyError(f"{package_root}: package root does not exist")

        if disposition == "EXEMPT_WITH_EXPLICIT_REASON":
            reason = entry.get("reason")
            if not isinstance(reason, str) or len(reason.strip()) < 24:
                raise PolicyError(
                    f"{package_root}: exemption requires a substantive explicit reason"
                )
            continue

        config_name = entry.get("config")
        target_name = entry.get("target")
        if not isinstance(config_name, str) or not config_name:
            raise PolicyError(f"{package_root}: required mypy entry needs config")
        if not isinstance(target_name, str) or not target_name:
            raise PolicyError(f"{package_root}: required mypy entry needs target")

        config_path = absolute_root / config_name
        target_path = absolute_root / target_name
        if not config_path.is_file():
            raise PolicyError(f"{package_root}: missing mypy config {config_name}")
        if not target_path.exists():
            raise PolicyError(f"{package_root}: missing mypy target {target_name}")

        config = _read_toml(config_path)
        tool = config.get("tool")
        mypy_config = tool.get("mypy") if isinstance(tool, dict) else None
        if not isinstance(mypy_config, dict):
            raise PolicyError(f"{package_root}: config has no [tool.mypy] table")
        if disposition == "MYPY_REQUIRED_STRICT" and mypy_config.get("strict") is not True:
            raise PolicyError(f"{package_root}: strict disposition requires strict = true")

        raw_mypy_path = entry.get("mypy_path", [])
        if not isinstance(raw_mypy_path, list) or not all(
            isinstance(item, str) and item for item in raw_mypy_path
        ):
            raise PolicyError(f"{package_root}: mypy_path must be a list of paths")
        for source_path in raw_mypy_path:
            if not (root / source_path).exists():
                raise PolicyError(
                    f"{package_root}: declared mypy_path does not exist: {source_path}"
                )

    _validate_toolchain_pins(root, mypy_version)
    return entries


def _exact_head(root: Path) -> str:
    github_sha = os.environ.get("GITHUB_SHA")
    if github_sha:
        return github_sha
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    return "UNKNOWN"


def _installed_mypy_version() -> str:
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--version"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise PolicyError("mypy is not executable in the current Python environment")
    output = result.stdout.strip()
    parts = output.split()
    if len(parts) < 2:
        raise PolicyError(f"unexpected mypy --version output: {output!r}")
    return parts[1]


def run_required_checks(
    root: Path,
    policy: dict[str, Any],
    entries: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], bool]:
    expected_version = str(policy["mypy_version"])
    installed_version = _installed_mypy_version()
    if installed_version != expected_version:
        raise PolicyError(
            f"installed mypy version {installed_version} != policy {expected_version}"
        )

    results: list[dict[str, Any]] = []
    all_passed = True
    for package_root, entry in sorted(entries.items()):
        disposition = str(entry["disposition"])
        if disposition == "EXEMPT_WITH_EXPLICIT_REASON":
            results.append(
                {
                    "root": package_root,
                    "disposition": disposition,
                    "status": "EXEMPT",
                    "reason": entry["reason"],
                }
            )
            continue

        absolute_root = root / package_root
        config_name = str(entry["config"])
        target_name = str(entry["target"])
        env = os.environ.copy()
        raw_paths = entry.get("mypy_path", [])
        resolved_paths = [str((root / item).resolve()) for item in raw_paths]
        own_src = absolute_root / "src"
        if own_src.exists():
            own_src_resolved = str(own_src.resolve())
            if own_src_resolved not in resolved_paths:
                resolved_paths.insert(0, own_src_resolved)
        if resolved_paths:
            env["MYPYPATH"] = os.pathsep.join(resolved_paths)
        else:
            env.pop("MYPYPATH", None)

        command = [
            sys.executable,
            "-m",
            "mypy",
            "--config-file",
            config_name,
            target_name,
        ]
        print(f"== mypy: {package_root} ({disposition}) ==", flush=True)
        completed = subprocess.run(
            command,
            cwd=absolute_root,
            env=env,
            check=False,
        )
        status = "PASS" if completed.returncode == 0 else "FAIL"
        if completed.returncode != 0:
            all_passed = False
        results.append(
            {
                "root": package_root,
                "disposition": disposition,
                "status": status,
                "returncode": completed.returncode,
                "config": config_name,
                "target": target_name,
                "mypy_path": list(raw_paths),
            }
        )

    return results, all_passed


def _write_evidence(
    output_path: Path,
    *,
    head: str,
    policy: dict[str, Any],
    results: list[dict[str, Any]],
    passed: bool,
) -> None:
    required_count = sum(
        1 for item in results if item["disposition"] in REQUIRED_DISPOSITIONS
    )
    exempt_count = sum(
        1 for item in results if item["disposition"] == "EXEMPT_WITH_EXPLICIT_REASON"
    )
    payload = {
        "schema_version": "0.1.0",
        "record_type": "REPOSITORY_MYPY_EXACT_HEAD_EVIDENCE",
        "target_head": head,
        "mypy_version": policy["mypy_version"],
        "package_count": len(results),
        "required_check_count": required_count,
        "exempt_count": exempt_count,
        "all_required_checks_passed": passed,
        "repository_wide_mypy_pass": passed and exempt_count == 0,
        "results": results,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--policy", default=".github/ci/mypy-policy.json")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--evidence-output")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    policy_path = root / args.policy
    try:
        policy = _read_json(policy_path)
        entries = validate_policy(root, policy)
        strict_count = sum(
            1
            for entry in entries.values()
            if entry["disposition"] == "MYPY_REQUIRED_STRICT"
        )
        configured_count = sum(
            1
            for entry in entries.values()
            if entry["disposition"] == "MYPY_REQUIRED_CONFIGURED"
        )
        exempt_count = sum(
            1
            for entry in entries.values()
            if entry["disposition"] == "EXEMPT_WITH_EXPLICIT_REASON"
        )
        print(f"MYPY_POLICY_PACKAGE_COUNT={len(entries)}")
        print(f"MYPY_POLICY_STRICT_COUNT={strict_count}")
        print(f"MYPY_POLICY_CONFIGURED_COUNT={configured_count}")
        print(f"MYPY_POLICY_EXEMPT_COUNT={exempt_count}")

        if args.validate_only:
            print("MYPY_POLICY_VALIDATION=PASS")
            return 0

        head = _exact_head(root)
        print(f"MYPY_EXACT_HEAD={head}")
        results, passed = run_required_checks(root, policy, entries)
        if args.evidence_output:
            _write_evidence(
                Path(args.evidence_output),
                head=head,
                policy=policy,
                results=results,
                passed=passed,
            )
        print(f"MYPY_REQUIRED_CHECKS={'PASS' if passed else 'FAIL'}")
        print(
            "REPOSITORY_WIDE_MYPY_PASS="
            + ("PASS" if passed and exempt_count == 0 else "NOT_ESTABLISHED")
        )
        return 0 if passed else 1
    except (OSError, ValueError, PolicyError) as exc:
        print(f"MYPY_POLICY_ERROR={exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
