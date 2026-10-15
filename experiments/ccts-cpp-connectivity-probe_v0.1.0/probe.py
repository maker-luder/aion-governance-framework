"""CCTS C++ bounded parity/performance probe / CCTS C++ 有界一致性與效能試驗。"""

from __future__ import annotations

import argparse
import ctypes
import json
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from time import perf_counter

# 使用當前 checkout 的既有 Python 函式為基準，不重新定義研究准入規則。
ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).with_name("connectivity.cpp")
PY_SRC = ROOT / "research-labs" / "human-ai-longitudinal-study_v0.1.0" / "src"
sys.path.insert(0, str(PY_SRC))
from aion_human_ai_longitudinal.co_constructed_thinking_space import (  # noqa: E402
    RevisionEdge,
    RevisionRelation,
    _revision_graph_is_connected,
)


def build_native(output: Path) -> None:
    """以本機 C++17 編譯器建立暫存共享程式庫，不寫入 Git 倉庫。"""
    compiler = shutil.which("g++")
    if compiler is None:
        raise RuntimeError("g++ is required; C++ probe has NOT been verified")
    if not sys.platform.startswith("linux"):
        raise RuntimeError("first prototype is Linux-only; cross-platform status unknown")
    subprocess.run(
        [compiler, "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
         "-fPIC", "-shared", str(SOURCE), "-o", str(output)],
        check=True,
        capture_output=True,
        text=True,
    )


def load_native(path: Path) -> ctypes._CFuncPtr:
    """載入函式並指定 32 位元整數及指標邊界；禁止隱式型別猜測。"""
    function = ctypes.CDLL(str(path)).ccts_graph_connected
    function.argtypes = (
        ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)
    )
    function.restype = ctypes.c_int
    return function


def encode_edges(edges: list[tuple[int, int]]) -> ctypes.Array[ctypes.c_uint32]:
    """轉換整數邊列表為原生連續陣列；Python 型別檢查另由原系統維持。"""
    flat = [value for pair in edges for value in pair]
    return (ctypes.c_uint32 * len(flat))(*flat)


def native_result(
    function: ctypes._CFuncPtr, n: int, edges: list[tuple[int, int]]
) -> int:
    """呼叫 C++ 函式；返回 1／0／-1，不提升為 CCTS 准入結論。"""
    values = encode_edges(edges)
    return int(function(n, len(edges), values))


def reference_result(n: int, edges: list[tuple[int, int]]) -> int:
    """透過正式 Python 參考函式檢查合成圖的連通性。"""
    ids = {f"node-{i}" for i in range(n)}
    relations = tuple(
        RevisionEdge(f"node-{a}", f"node-{b}", RevisionRelation.CLARIFIES)
        for a, b in edges
    )
    return int(_revision_graph_is_connected(ids, relations))


def fixtures(total_random: int) -> list[tuple[int, list[tuple[int, int]]]]:
    """產生固定種子的合成案例，包含連通、斷開、環與重複邊。"""
    cases: list[tuple[int, list[tuple[int, int]]]] = [
        (1, []),
        (2, []),
        (2, [(0, 1)]),
        (5, [(0, 1), (1, 2), (2, 3), (3, 4)]),
        (5, [(0, 1), (1, 2), (3, 4)]),
        (5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]),
        (3, [(0, 1), (0, 1), (1, 2)]),
    ]
    rng = random.Random(20261016)
    for _ in range(total_random):
        n = rng.randint(1, 90)
        pairs = []
        for _ in range(rng.randrange(0, 3 * n)):
            if n == 1:
                break
            a, b = rng.sample(range(n), 2)
            pairs.append((a, b))
        cases.append((n, pairs))
    return cases


def check_parity(function: ctypes._CFuncPtr, random_cases: int) -> int:
    """逐筆要求 C++ 與正式 Python 基準相同；不相同即停止並報錯。"""
    data = fixtures(random_cases)
    for index, (n, edges) in enumerate(data):
        expected = reference_result(n, edges)
        observed = native_result(function, n, edges)
        if observed != expected:
            raise AssertionError(
                f"case {index}: Python={expected}, C++={observed}, n={n}, edges={edges}"
            )

    # C++ FFI 必須拒絕空圖、自連線、越界節點及空指標。
    invalid = [
        int(function(0, 0, None)),
        native_result(function, 2, [(0, 0)]),
        native_result(function, 2, [(0, 2)]),
        int(function(2, 1, None)),
    ]
    if invalid != [-1] * len(invalid):
        raise AssertionError(f"fail-closed negative cases failed: {invalid}")
    return len(data)


def benchmark(function: ctypes._CFuncPtr, iterations: int) -> dict[str, float | int]:
    """報告局部效能，不把微型測試視為整個 CCTS 的速度改進。"""
    n = 90
    edges = [(i, i + 1) for i in range(n - 1)]
    edges.extend((i, (i + 3) % n) for i in range(n))
    prebuilt = encode_edges(edges)
    ids = {f"node-{i}" for i in range(n)}
    reference_edges = tuple(
        RevisionEdge(f"node-{a}", f"node-{b}", RevisionRelation.CLARIFIES)
        for a, b in edges
    )
    reference_result(n, edges)
    native_result(function, n, edges)

    start = perf_counter()
    for _ in range(iterations):
        reference_result(n, edges)
    python_seconds = perf_counter() - start

    start = perf_counter()
    for _ in range(iterations):
        if not _revision_graph_is_connected(ids, reference_edges):
            raise AssertionError("unexpected Python benchmark result")
    python_kernel_only_seconds = perf_counter() - start

    start = perf_counter()
    for _ in range(iterations):
        native_result(function, n, edges)
    native_with_marshalling_seconds = perf_counter() - start

    start = perf_counter()
    for _ in range(iterations):
        if function(n, len(edges), prebuilt) != 1:
            raise AssertionError("unexpected native benchmark result")
    native_kernel_only_seconds = perf_counter() - start
    return {
        "iterations": iterations,
        "nodes": n,
        "edges": len(edges),
        "python_with_model_construction_ms": round(python_seconds * 1000, 3),
        "python_preconstructed_kernel_ms": round(python_kernel_only_seconds * 1000, 3),
        "cpp_with_ctypes_marshalling_ms": round(native_with_marshalling_seconds * 1000, 3),
        "cpp_pre_marshaled_kernel_ms": round(native_kernel_only_seconds * 1000, 3),
    }


def main() -> int:
    """只輸出合成實驗 JSON；不執行真實人機研究或改變 repo。"""
    parser = argparse.ArgumentParser(description="CCTS C++ bounded graph probe")
    parser.add_argument("--random-cases", type=int, default=300)
    parser.add_argument("--benchmark-iterations", type=int, default=1200)
    args = parser.parse_args()
    if not 0 <= args.random_cases <= 10000 or not 0 <= args.benchmark_iterations <= 100000:
        parser.error("case/iteration counts out of permitted range")

    with tempfile.TemporaryDirectory(prefix="ccts-cpp-probe-") as tmp:
        library = Path(tmp) / "libccts_connectivity.so"
        build_native(library)
        function = load_native(library)
        count = check_parity(function, args.random_cases)
        perf = benchmark(function, args.benchmark_iterations) if args.benchmark_iterations else None
    print(json.dumps({
        "status": "LOCAL_SYNTHETIC_PARITY_PASS",
        "case_count": count,
        "invalid_input_checks": 4,
        "cpp_standard": "C++17",
        "benchmark": perf,
        "scope": "UNDIRECTED_GRAPH_CONNECTIVITY_ONLY",
        "ccts_admission_unchanged": True,
        "scientific_validation": "NOT_ESTABLISHED",
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
