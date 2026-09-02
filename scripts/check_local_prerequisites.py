"""Small local environment probe; no package install, network, elevation or model load."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile


def node_supported(version: str) -> bool:
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", version.strip())
    return bool(match and tuple(map(int, match.groups())) >= (22, 13, 0))


def probe_symlinks() -> dict[str, object]:
    try:
        with tempfile.TemporaryDirectory(prefix="aion-prerequisite-") as raw:
            root = Path(raw)
            target = root / "target"
            target.write_text("fixture", encoding="utf-8")
            (root / "link").symlink_to(target)
            return {"supported": (root / "link").read_text() == "fixture", "winerror": None}
    except OSError as exc:
        # Do not put a private temp path in the public diagnostic.
        return {"supported": False, "winerror": getattr(exc, "winerror", None), "errno": exc.errno}


def classify(profile: str, modules: dict[str, str | None], tools: dict[str, object], symlinks: dict[str, object]) -> list[str]:
    problems = []
    if not tools["git"]:
        problems.append("GIT_MISSING")
    if profile in {"python", "all"}:
        problems.extend("DEPENDENCY_MISSING:" + key for key, value in modules.items() if value is None)
        if not symlinks["supported"]:
            problems.append("FULL_ROOT_QA_SYMLINK_PREREQUISITE_MISSING")
    if profile in {"ziwei", "all"}:
        if not node_supported(str(tools.get("node_version", ""))):
            problems.append("NODE_22_13_OR_NEWER_REQUIRED")
        if not tools.get("pnpm"):
            problems.append("PNPM_MISSING")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=["python", "ziwei", "all"], default="all")
    args = parser.parse_args(argv)
    modules = {}
    for name in ("pytest", "jsonschema", "lunar-python"):
        try:
            modules[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            modules[name] = None
    tools = {"git": bool(shutil.which("git")), "pnpm": bool(shutil.which("pnpm")), "node_version": ""}
    node = shutil.which("node")
    if node:
        try:
            result = subprocess.run([node, "--version"], capture_output=True, text=True, timeout=10, check=True)
            tools["node_version"] = result.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            tools["node_version"] = "PROBE_FAILED"
    symlinks = probe_symlinks()
    problems = classify(args.profile, modules, tools, symlinks)
    report = {"status": "HOLD" if problems else "PASS", "profile": args.profile,
              "python_version": platform.python_version(), "python_implementation": platform.python_implementation(),
              "os": platform.system(), "logical_cpus": os.cpu_count(),
              "disk_free_bytes": shutil.disk_usage(Path.cwd()).free,
              "modules": modules, "tools": tools, "symlinks": symlinks, "problems": problems,
              "hardware_benchmark": "NOT_RUN", "model_training_capacity": "NOT_ESTABLISHED",
              "automatic_install": False, "automatic_elevation": False,
              "canonical_effect": "NONE", "subjectivity": "NOT_ESTABLISHED"}
    if sys.version_info < (3, 11):
        report["status"] = "HOLD"
        problems.append("PYTHON_3_11_OR_NEWER_REQUIRED")
    print(json.dumps(report, indent=2))
    return 2 if report["status"] == "HOLD" else 0


if __name__ == "__main__":
    raise SystemExit(main())
