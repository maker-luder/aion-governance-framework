# Western Astrology v0.2 / Bazi v0.2 Verification Record

## Bound state

- Baseline commit: `5eae99d67f7d5cc763c4e3361e072d8b7a18688c`
- Modified core commit: `fe309c5dea63d6d3e60c7103dd5f26abcfe54ab2`
- Branch: `feat/classical-western-astrology-capability-20260830`
- Date: `2026-08-30` (`Asia/Taipei`)
- Runtime: `C:\A15\venv\Scripts\python.exe`, Python 3.12

## Baseline behavior (exit 0)

Commands were run in a detached temporary worktree at the exact baseline and
the worktree was then removed.

```powershell
git worktree add --detach $tmp 5eae99d67f7d5cc763c4e3361e072d8b7a18688c
& C:\A15\venv\Scripts\python.exe -m pytest -q  # cwd: examples/classical-western-astrology_v0.1.0
& C:\A15\venv\Scripts\python.exe -m pytest -q  # cwd: examples/bazi-capability_v0.1.1
git worktree remove --force $tmp
```

Literal output:

```text
..........................                                               [100%]
26 passed in 0.14s
........................................................................ [ 87%]
..........                                                               [100%]
82 passed in 1.14s
BASELINE_WESTERN_EXIT=0 BASELINE_BAZI_EXIT=0
```

## Modified behavior (exit 0)

Commands:

```powershell
& C:\A15\venv\Scripts\python.exe -m pytest -q
# separately in each component directory
```

Literal output:

```text
..................................                                       [100%]
34 passed in 0.10s
........................................................................ [ 80%]
..................                                                       [100%]
90 passed in 0.89s
```

Coverage commands and literal results:

```text
Western: 34 passed; total coverage 92.59%; required 90%; exit 0
Bazi:    90 passed; total coverage 87.19%; required 85%; exit 0
```

Static verification:

```text
ruff check --config ruff.toml [both components and fetch script]
All checks passed!
RUFF_EXIT=0 COMPILE_EXIT=0

mypy --config-file [component pyproject] [component src]
Success: no issues found in 9 source files
Success: no issues found in 14 source files

SOURCE_MANIFEST_VERIFY=PASS sources=14 vendored=7 hash_only=7
Documentation entry and convergence checks: PASS
PUBLIC_SCAN_EXIT=0
```

Source fetch command:

```powershell
& C:\A15\venv\Scripts\python.exe scripts\fetch_astrology_bazi_sources.py
```

Literal status: `FETCH_EXIT=0`. All 14 entries have `download_status=PASS`;
all 7 retained payloads reopen to their recorded SHA-256; the other 7 were
downloaded, hashed, and discarded. The lunar-python 1.4.8 sdist SHA-256 matched
`3aa11cc73c25e70ddf0ba5bdac7398c03acc9491a3aa512a91c9642973b669d6`.

## Full-repository residuals

`scripts/run_component_tests.py` ran every discovered component. The two changed
components passed. The Windows run retained four unrelated pre-existing
residuals rather than weakening their tests:

1. one Evidence Interop raw-byte `protocol_hash` mismatch on Windows line endings;
2. two `WinError 1314` failures because the current account cannot create test
   symlinks;
3. one historical-branch assertion because the intentionally retired remote
   branch ref is absent (the frozen commit object itself remains available).

Linux CI remains the authoritative exact-head check for the CRLF and symlink
cases. After explicit Human Owner merge authorization, the retired-branch test
was corrected in a follow-up commit to verify the frozen commit object directly;
the parallel remote branch was not recreated.

## Patch and rollback

- Patch archive: `qa/astrology-bazi-v0.2/ASTROLOGY_BAZI_V0_2.patch.gz`
- Patch SHA-256: `f148bbffd18096bc3a88c9e691b904917efb7d6fa88dd32bbf46d10cdbde96ac`
- Uncompressed patch bytes: `1048409`
- Rollback: `scripts/rollback_astrology_bazi_v0_2.ps1`

Default invocation is verification-only. `-Apply` requires a clean, named,
non-`main` branch and creates a `git revert` of the exact core commit.

```powershell
& .\scripts\rollback_astrology_bazi_v0_2.ps1
& .\scripts\rollback_astrology_bazi_v0_2.ps1 -Apply
```

The `-Apply` path was also executed in a disposable named worktree branch and
that worktree/branch was removed after verification. Literal output:

```text
ROLLBACK_VERIFY=PASS base=5eae99d67f7d5cc763c4e3361e072d8b7a18688c core=fe309c5dea63d6d3e60c7103dd5f26abcfe54ab2
ROLLBACK_APPLY=PASS reverted=fe309c5dea63d6d3e60c7103dd5f26abcfe54ab2 branch=verify/astrology-bazi-rollback-20260830
26 passed in 0.14s
82 passed in 1.01s
ROLLBACK_APPLY_EXIT=0
ROLLBACK_BASELINE_WESTERN_EXIT=0 ROLLBACK_BASELINE_BAZI_EXIT=0
```
