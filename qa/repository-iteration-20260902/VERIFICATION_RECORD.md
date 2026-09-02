# Repository iteration verification — 2026-09-02

```text
BASE=8ca9f5fe47a38726c64928b164c0f41f84e69dc7
CORE=73d4ffb6e9155208d0587b62e69a19b1d10066f9
CORE_TREE=29bcf1225e0871f136994405023b7a7a6b56c7c9
AI_SUBJECTIVITY_POSSIBILITY=CENTRAL_RESEARCH_QUESTION
SUBJECTIVITY=NOT_ESTABLISHED
CANONICAL_EFFECT=NONE
DEPLOYMENT=FALSE
```

Commands below run at the repository root. `python` denotes the explicitly selected
CPython 3.12.13 test venv, with pytest 9.1.1, jsonschema 4.26.0 and lunar-python
1.4.8. Full command argv, local paths and failure traces are retained in the local
evidence bundle rather than exposing workstation paths in this public record.
Summary lines below are literal output, with elapsed-time suffixes omitted.

## Baseline and modified behavior

At BASE:

```powershell
python -m pytest -q tests
```

```text
5 failed, 90 passed
EXIT=1
```

Failures: the component-result target path assertion and four WinError 1314
symlink setups. The target producer returned a Windows separator instead of
`components/demo`.

At the modified core:

```powershell
python -m pytest -q tests/test_component_runner.py tests/test_subjectivity_sources.py tests/test_local_prerequisites.py tests/test_workflow_integrity.py
python -m pytest -q tests
```

```text
29 passed
EXIT=0
4 failed, 118 passed
EXIT=1
```

The path assertion now passes without changing its expected value. All four
remaining root failures are real WinError 1314 symlink setups. No tests or
security assertions were skipped, replaced with mock links or weakened.
The exact-head Linux Quality job now runs the entire root suite on Python
3.11 and 3.12, including these symlink cases.

## Source intake and boundary checks

```powershell
python scripts/fetch_subjectivity_sources.py
python scripts/fetch_subjectivity_sources.py --download-cache ../aion-reference-cache
```

```text
status=PASS
sources=4
mode=OFFLINE_VERIFY
downloaded_or_verified_cache=0
EXIT=0
status=PASS
sources=4
mode=DOWNLOAD
downloaded_or_verified_cache=4
EXIT=0
```

The first three original bodies were re-downloaded with matching bytes/digests;
the fourth Crossref metadata snapshot was downloaded separately and then verified
from cache. Two CC BY converted texts are retained. The TICS 2026 publisher
full-page fetch returned HTTP 403: its scope remains metadata-only.
All four candidate records validate against the unchanged existing governed
source schema. Offline verification makes no network call. Negative tests cover
tampering, source path escape, duplicate IDs, changed boundaries, invalid license
retention, authority promotion and cache overwrite rejection.

## Repository checks and environment distinction

```powershell
python scripts/validate_documentation_entry.py --root .
python -m ruff check --config ruff.toml .
python scripts/scan_public_tree.py
python -m compileall -q components examples research-labs scripts
python scripts/check_local_prerequisites.py --profile python
```

```text
Documentation entry and convergence checks: PASS
EXIT=0
All checks passed!
EXIT=0
{"status": "PASS", "errors": []}
EXIT=0
(compileall: no output)
EXIT=0
status=HOLD
problems=[FULL_ROOT_QA_SYMLINK_PREREQUISITE_MISSING]
winerror=1314
EXIT=2
```

The prerequisite HOLD is not a hardware benchmark or research conclusion.
See `docs/LOCAL_RESOURCE_AND_ENVIRONMENT.md` for measured RAM/CPU/GPU/disk,
missing-dependency distinctions and unperformed large-model workloads.

`python scripts/run_component_tests.py` discovered 30 Python targets. Initial
Windows run: 29 targets succeeded; Evidence Interop had 83 passed / 3 failed
(one raw-byte protocol binding and two symlink privileges). After materializing
the exact committed Git blobs in the owned clean worktree, the Interop rerun
reported `2 failed, 84 passed`; both failures were WinError 1314.
The original tracked `qa/CURRENT_TEST_RESULTS.json` was byte-backed-up and
restored after the component run. Unrelated checkouts were untouched.

Raw Git-blob materialization repaired only checkout-byte representation. The
initial exact-tree check failed under CRLF conversion. The repeated command:

```powershell
python scripts/verify_release.py --baseline current-head
```

reported `status=PASS`, `errors=[]`, `files=986`, baseline commit equal to CORE,
exit 0. Rebuilding index stat entries left the Git tree unchanged:
`29bcf1225e0871f136994405023b7a7a6b56c7c9`. This is not a change to Git global
configuration or the source verifier. Linux CI remains the final portable check.

## Core preservation

Exact base/core tree IDs are unchanged for the entire `components`,
`research-labs`, `schemas` and `examples` trees, and for
`docs/PROJECT_PURPOSE_ANCHOR.md` and `docs/CURRENT_STATE.md`.
The protocol's sole edit corrects an already-merged bridge's stale branch-only
wording; its six dimensions, inference method and non-claims are unchanged.

## Preserved original, patch and rollback

The baseline Git archive was reopened with `zipfile.testzip()` and its
`scripts/run_component_tests.py` member compared to BASE's Git blob.

```text
BASELINE_ARCHIVE_SHA256=0d523834bec2647274b833dba96c2bcfedac5d7a9062e41490ef07579d24a214
```

Patch generation and reverse check:

```powershell
git diff --unified=0 --binary --no-ext-diff --output=qa/repository-iteration-20260902/REPOSITORY_ITERATION.patch 8ca9f5fe47a38726c64928b164c0f41f84e69dc7 73d4ffb6e9155208d0587b62e69a19b1d10066f9
git apply --cached --reverse --check --unidiff-zero qa/repository-iteration-20260902/REPOSITORY_ITERATION.patch
```

```text
PATCH_BYTES=283170
PATCH_SHA256=c550115ca4da0af1632ec88beafab2088257f7ff08b7749dbcb2a4cf74e53f4f
PATCH_REVERSE_EXIT=0
```

Forward replay uses an isolated temporary Git index initialized from BASE:
`git read-tree BASE`, `git apply --cached --unidiff-zero PATCH`, `git write-tree`.
The resulting tree must equal CORE_TREE exactly before this record is packaged.

```powershell
python scripts/rollback_repository_iteration_20260902.py
```

The default mode verifies the exact base, core ancestry and patch hash, then
reverse-checks the index. `--apply` requires a clean tree and makes a local
revert commit only. It never pushes, force-updates main or unarchives GitHub.
Actual apply verification is confined to a disposable local worktree.

## Remote completion evidence

This record binds implementation and local checks, not a future CI status.
The PR approval receipt and exact-head checks, merge result and final branch
enumeration are recorded separately after they occur. Required checks and
Human Owner approval are distinct from scientific validation or release approval.

## Packaging replay results

The first archive had checkout CRLF conversion; a separate archive made with
`git -c core.autocrlf=false archive` was reopened and matched the raw BASE blob.
The earlier archive is preserved separately.

```text
BASELINE_ZIP_INTEGRITY=PASS
BASELINE_ARCHIVE_SHA256=0d523834bec2647274b833dba96c2bcfedac5d7a9062e41490ef07579d24a214
PATCH_FORWARD_TREE=29bcf1225e0871f136994405023b7a7a6b56c7c9
PATCH_FORWARD_REPLAY=PASS
ROLLBACK_VERIFY=PASS
ROLLBACK_MODE=DRY_RUN
EXIT=0
```

## Executed rollback verification

In a detached disposable checkout, `python scripts/rollback_repository_iteration_20260902.py --apply`
returned exit 0. Every path changed by CORE was compared with BASE at Git-blob
level; additions were confirmed absent. The baseline runner test was then rerun.

```text
ROLLBACK_APPLY=PASS
RESTORED_CORE_PATHS=25
ROLLBACK_HEAD=55a0960e052b7e9f798ac59e59008ed6f93e0510
REMOTE_PUSH_PERFORMED=false
1 failed, 1 passed
ROLLBACK_BEHAVIOR_EXIT=1
```

The deliberately restored baseline again exhibits its original Windows path
separator failure; the second runner test passes. The active implementation
checkout remains on the modified behavior. Final full root rerun: `4 failed,
118 passed in 13.69s`, exit 1, all four failures WinError 1314.
