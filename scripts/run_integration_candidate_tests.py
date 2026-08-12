from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research-labs" / "integration-candidates"


def count(pattern: str, text: str) -> int:
    found = re.findall(pattern, text)
    return int(found[-1]) if found else 0


def main() -> int:
    results = []
    for tests_dir in sorted(BASE.glob("*/tests")):
        package = tests_dir.parent
        env = os.environ.copy()
        src = package / "src"
        env["PYTHONPATH"] = os.pathsep.join([str(src), env.get("PYTHONPATH", "")]) if src.is_dir() else env.get("PYTHONPATH", "")
        proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-o", "addopts="], cwd=package, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        output = proc.stdout.replace(str(ROOT), "<RESEARCH_ROOT>")
        results.append({"target": str(package.relative_to(ROOT)), "status": "PASS" if proc.returncode == 0 else "FAIL", "returncode": proc.returncode, "passed": count(r"(\d+) passed", output), "failed": count(r"(\d+) failed", output), "output": output})
    summary = {"target_count": len(results), "failed_target_count": sum(item["status"] == "FAIL" for item in results), "total_passed": sum(item["passed"] for item in results), "total_failed": sum(item["failed"] for item in results)}
    target_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    payload = {"schema_version": "1.0", "scope": "FINAL_RESEARCH_HEAD_INTEGRATION_CANDIDATES", "target_head": target_head, "summary": summary, "targets": results}
    (ROOT / "qa" / "INTEGRATION_CANDIDATE_TEST_RESULTS.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["failed_target_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
