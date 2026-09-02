# Local resource and environment diagnosis

Run `python scripts/check_local_prerequisites.py --profile all` first. Profiles
`python` and `ziwei` narrow prerequisite reporting. Exit 0 means the inspected
prerequisites passed, not that the test suite passed. Exit 2 means HOLD. The
probe is CPU-only, creates one disposable symlink fixture, makes no network call,
does not install packages and does not request elevation. It is not a benchmark.

## Distinguish four different causes

| Observation | Classification | Response |
|---|---|---|
| Windows `WinError 1314` creating a symlink | OS privilege prerequisite | retain the real symlink tests; run the unchanged suite on Linux CI |
| `ModuleNotFoundError` for `lunar_python` / `jsonschema` | Python environment dependency | use the intended venv and install declared requirements, not more RAM |
| Node below 22.13 with pinned pnpm 11.19.0 | toolchain mismatch | use Node 24 as in Zi Wei CI |
| Backslash target labels in QA JSON | program portability defect | fixed by POSIX serialization in `run_component_tests.py` |
| OOM, measured memory pressure, disk exhaustion | resource constraint only if measured | reduce a bounded workload or move it to appropriately sized compute |
| TLS issuer failure in one Python environment | trust-store configuration | use verified system TLS; never disable certificate verification |

Python's official `os.symlink` documentation explains the Windows Developer Mode
or symlink privilege requirement:
https://docs.python.org/3/library/os.html#os.symlink
No repository script changes that system setting. Tests are not made green by
silently replacing symlinks with ordinary files or suppressing their assertions.

## Observed workstation, 2026-09-02 (not a supported-hardware minimum)

- Windows 10 Pro; Intel Core i7-870; 4 physical / 8 logical cores.
- Visible RAM: 8,346,676 KiB (about 7.96 GiB); available at sampling:
  2,685,252 KiB (about 2.56 GiB).
- GPU: NVIDIA GeForce GT 430, reported 1,073,741,824 bytes (1 GiB) VRAM.
- Free C: space at sampling: 48,551,342,080 bytes (about 45.22 GiB).

The bounded unit tests and small source downloads ran without an observed OOM.
This machine was not benchmarked for model training or large-model inference.
Do not infer suitability for those workloads from a CPU test pass. No model
weights, large neuroimaging datasets or GPU training jobs were downloaded/run.
The four known Windows root-suite symlink failures are privilege limitations,
not evidence of insufficient CPU/RAM. Available memory is a time-varying snapshot.

Large-model mechanistic work, dataset access and genuinely independent replication
remain separate workload/design questions. Neither a faster machine nor more
downloads alone establishes AI subjectivity.
