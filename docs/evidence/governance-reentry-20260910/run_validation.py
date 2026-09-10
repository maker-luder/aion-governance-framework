"""Capture literal commands/output outside the candidate; never rewrite QA snapshots."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
root = Path(sys.argv[1]).resolve()
label = sys.argv[2]
spec = importlib.util.spec_from_file_location("component_runner", root / "scripts/run_component_tests.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
env = os.environ.copy()
env["PYTHONPATH"] = os.pathsep.join(map(str, runner.discover_source_roots(root)))
env["PYTHONIOENCODING"] = "utf-8"
checks = [
    ("quality_factory", [sys.executable, "-m", "pytest", "-q", "-o", "addopts=", "research-labs/coupled-cognition-quality-factory_v0.1.0/tests"]),
    ("incident_controller", [sys.executable, "-m", "pytest", "-q", "-o", "addopts=", "components/upstream_security_v0.1.0/tests"]),
    ("root_controls", [sys.executable, "-m", "pytest", "-q", "tests"]),
    ("lint", [sys.executable, "-m", "ruff", "check", "--config", "ruff.toml", "."]),
    ("documentation", [sys.executable, "scripts/validate_documentation_entry.py", "--root", "."]),
]
results = []
for name, cmd in checks:
    p = subprocess.run(cmd, cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    results.append(dict(name=name, command=cmd, cwd=str(root), inputs="checkout plus repository fixtures", output=p.stdout, exit_status=p.returncode))
    (HERE / f"{label}-{name}.txt").write_text(p.stdout, encoding="utf-8")
    (HERE / f"{label}-verification.json").write_text(json.dumps(dict(label=label, pythonpath=env["PYTHONPATH"], results=results), ensure_ascii=False, indent=2), encoding="utf-8")
    print(label, name, "exit", p.returncode, p.stdout[-400:], flush=True)
