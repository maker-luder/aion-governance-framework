from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = sorted(
    [p for p in (ROOT / "components").iterdir() if (p / "tests").is_dir()]
    + [p for p in (ROOT / "examples").iterdir() if (p / "tests").is_dir()]
    + [p for p in (ROOT / "research-labs").iterdir() if (p / "tests").is_dir()]
)

source_roots = [
    ROOT / "research-labs" / "language-core-g1_v0.2.1" / "src",
    ROOT / "components" / "governance_kernel_v0.4.0" / "src",
    ROOT / "components" / "astra_workbench_v1.0.0" / "src",
] + sorted(ROOT.glob("components/*/src")) + sorted(ROOT.glob("examples/*/src")) + sorted(ROOT.glob("research-labs/*/src"))

results: list[dict[str, object]] = []
for target in TARGETS:
    target_src = target / "src"
    ordered = [target_src] + [path for path in source_roots if path != target_src and path.is_dir()]
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(str(path) for path in ordered)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-o", "addopts="], cwd=target, text=True, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    results.append({"target": str(target.relative_to(ROOT)), "returncode": proc.returncode, "output": proc.stdout})
    print(f"[{target.name}] returncode={proc.returncode}")
    print(proc.stdout)

out = ROOT / "qa" / "CURRENT_TEST_RESULTS.json"
out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
raise SystemExit(0 if all(item["returncode"] == 0 for item in results) else 1)
