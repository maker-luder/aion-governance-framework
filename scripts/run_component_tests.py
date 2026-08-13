from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def discover_targets(root: Path = ROOT) -> list[Path]:
    return sorted(
        [path for path in (root / "components").iterdir() if (path / "tests").is_dir()]
        + [path for path in (root / "examples").iterdir() if (path / "tests").is_dir()]
        + [path for path in (root / "research-labs").iterdir() if (path / "tests").is_dir()]
    )


def discover_source_roots(root: Path = ROOT) -> list[Path]:
    return [
        root / "research-labs" / "language-core-g1_v0.2.1" / "src",
        root / "components" / "governance_kernel_v0.4.0" / "src",
        root / "components" / "astra_workbench_v1.0.0" / "src",
    ] + sorted(root.glob("components/*/src")) + sorted(root.glob("examples/*/src")) + sorted(root.glob("research-labs/*/src"))


TARGETS = discover_targets()
source_roots = discover_source_roots()


def _normalize_test_output(output: str) -> str:
    lines = output.splitlines(keepends=True)
    for index in range(len(lines) - 1, -1, -1):
        if lines[index].strip():
            lines[index] = re.sub(
                r"[ \t]+in[ \t]+\d+(?:\.\d+)?s(?=\r?\n?$)",
                "",
                lines[index],
            )
            break
    return "".join(lines)


def run_component_tests(
    targets: list[Path],
    root: Path = ROOT,
    roots: list[Path] | None = None,
) -> list[dict[str, object]]:
    ordered_roots = source_roots if roots is None else roots
    results: list[dict[str, object]] = []
    for target in targets:
        target_src = target / "src"
        ordered = [target_src] + [path for path in ordered_roots if path != target_src and path.is_dir()]
        env = os.environ.copy()
        env["PYTHONPATH"] = os.pathsep.join(str(path) for path in ordered)
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-o", "addopts="],
            cwd=target,
            text=True,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        output = _normalize_test_output(proc.stdout)
        results.append(
            {
                "target": str(target.relative_to(root)),
                "returncode": proc.returncode,
                "output": output,
            }
        )
        print(f"[{target.name}] returncode={proc.returncode}")
        print(output)
    return results


def write_results(root: Path, results: list[dict[str, object]]) -> None:
    out = root / "qa" / "CURRENT_TEST_RESULTS.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    targets = list(TARGETS)
    if not targets:
        write_results(ROOT, [])
        print("[component-test-runner] no test targets discovered")
        return 1
    results = run_component_tests(targets, ROOT)
    write_results(ROOT, results)
    return 0 if all(item["returncode"] == 0 for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
