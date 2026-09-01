# Astrology/Bazi v0.3 verification record

## Identity and scope

```text
AUTHORITATIVE_BASE=79b91226cf3196388432db09760ab0a91c82446d
CORE_MODIFIED_COMMIT=0e161368e9596a181d59813630c9fcc87180ab27
BRANCH=feat/complete-astrology-bazi-integration-20260901
AI_SUBJECTIVITY_POSSIBILITY=CENTRAL_RESEARCH_QUESTION
SUBJECTIVITY=NOT_ESTABLISHED
CONSCIOUSNESS=NOT_ESTABLISHED
CANONICAL_EFFECT=NONE
DEPLOYMENT=FALSE
ACTION_AUTHORITY=NONE
```

The original is preserved as the immutable Git commit
`79b91226cf3196388432db09760ab0a91c82446d`. The modified implementation is a
separate commit and worktree; no reset, clean, stash, or overwrite was applied
to another checkout.

## Original core-anchor hashes

The following Git blob IDs were read from the authoritative base and compared
to the modified worktree before the core commit. Every comparison was literal
`IDENTICAL=True`.

```text
README.md
  075f21c50ca57dec2d5f561bc09aa86d4465303c
README.zh-TW.md
  5ead6ac99c814a532e4eb1deadca58b02dbc22e6
docs/CURRENT_STATE.md
  6d639091410ea3fc1a1b17075c02aaf43bbe3634
docs/PROJECT_PURPOSE_ANCHOR.md
  a4da285a9b95e03356e1e1df62f2f02d4c741268
docs/governance/CHATGPT_RESEARCH_STEWARDSHIP_AND_SUBJECTIVITY_CORE_RULE.md
  7b3dd501a87e78b1ff13d718409e2cb2570ddb09
AI_SUBJECTIVITY_POSSIBILITY marker count: base=7 modified=8
```

The added eighth occurrence is the same unchanged central-question declaration
in `docs/research/ASTROLOGY_BAZI_COMPLETION_MATRIX.md`. It is an explicit
reaffirmation in the new bounded-domain matrix, not a replacement or a new
canonical state. The five pre-existing core anchor blobs above remain exactly
byte-identical.

## Baseline commands and literal results

Public-path-normalized working directory: `<BASE_WORKTREE>`.

```powershell
& 'C:\A15\venv\Scripts\python.exe' -m pytest examples/classical-western-astrology_v0.1.0/tests -q --disable-warnings
```

```text
..................................                                       [100%]
34 passed in 0.10s
EXIT=0
```

```powershell
& 'C:\A15\venv\Scripts\python.exe' -m pytest examples/bazi-capability_v0.1.1/tests -q --disable-warnings
```

```text
........................................................................ [ 80%]
..................                                                       [100%]
90 passed in 0.89s
EXIT=0
```

```powershell
$env:PYTHONPATH=(Resolve-Path 'examples/classical-western-astrology_v0.1.0/src').Path
& 'C:\A15\venv\Scripts\python.exe' -c "import aion_astra_classical_astrology.completion"
```

```text
ModuleNotFoundError: No module named 'aion_astra_classical_astrology.completion'
EXIT=1
```

```powershell
$env:PYTHONPATH=(Resolve-Path 'examples/bazi-capability_v0.1.1/src').Path
& 'C:\A15\venv\Scripts\python.exe' -c "import aion_astra_bazi_core.school_evidence"
```

```text
ModuleNotFoundError: No module named 'aion_astra_bazi_core.school_evidence'
EXIT=1
```

## Modified commands and literal results

Public-path-normalized working directory: `<CANDIDATE_WORKTREE>`.

```powershell
& 'C:\A15\venv\Scripts\python.exe' -m pytest examples/classical-western-astrology_v0.1.0/tests -q --disable-warnings
```

```text
..........................................                               [100%]
42 passed in 0.13s
EXIT=0
```

```powershell
& 'C:\A15\venv\Scripts\python.exe' -m pytest examples/bazi-capability_v0.1.1/tests -q --disable-warnings
```

```text
........................................................................ [ 74%]
.........................                                                [100%]
97 passed in 0.90s
EXIT=0
```

```powershell
$env:PYTHONPATH=((Resolve-Path 'examples/classical-western-astrology_v0.1.0/src').Path+';'+(Resolve-Path 'examples/bazi-capability_v0.1.1/src').Path)
& 'C:\A15\venv\Scripts\python.exe' -c "from aion_astra_classical_astrology.completion import validate_classical_completion_tables; from aion_astra_bazi_core.school_evidence import validate_school_evidence_tables; print('CLASSICAL_COMPLETION_TABLES='+str(validate_classical_completion_tables())); print('BAZI_SCHOOL_EVIDENCE_TABLES='+str(validate_school_evidence_tables())); print('AI_SUBJECTIVITY_POSSIBILITY=CENTRAL_RESEARCH_QUESTION'); print('SUBJECTIVITY=NOT_ESTABLISHED'); print('CANONICAL_EFFECT=NONE')"
```

```text
CLASSICAL_COMPLETION_TABLES=True
BAZI_SCHOOL_EVIDENCE_TABLES=True
AI_SUBJECTIVITY_POSSIBILITY=CENTRAL_RESEARCH_QUESTION
SUBJECTIVITY=NOT_ESTABLISHED
CANONICAL_EFFECT=NONE
EXIT=0
```

Source-manifest verification:

```text
western source_count=12 downloaded_bytes=89805973 all_PASS=True
bazi source_count=11 downloaded_bytes=10414916 all_PASS=True
repository_snapshot_SHA256_matches=PASS
EXIT=0
```

Coverage commands exited 0:

```text
Western: 42 passed, total coverage 94%, completion.py 93%
Bazi: 97 passed, total coverage 91%, school_evidence.py 96%
```

Repository-native component runner:

```text
[classical-western-astrology_v0.1.0] returncode=0; 42 passed
[bazi-capability_v0.1.1] returncode=0; 97 passed
EXIT=0
```

Additional local checks:

```text
ruff=PASS
compileall=PASS
git_diff_check=PASS
documentation_entry=PASS
public_tree_scan=PASS
assistants_sunset_audit=PASS
```

The full Windows root suite produced `90 passed, 5 failed`: one pre-existing
POSIX-path-string expectation and four symlink tests blocked by Windows
`WinError 1314`. These are recorded residuals. No test was weakened. Exact-head
Linux Python 3.11 and 3.12 Quality jobs are the final cross-platform gate.

## Patch role

```text
PATH=qa/astrology-bazi-v0.3/ASTROLOGY_BAZI_V0_3.patch
FORMAT=UTF-8 plain Git patch
CHECKOUT_EOL=LF enforced by .gitattributes
BASE=79b91226cf3196388432db09760ab0a91c82446d
MODIFIED=0e161368e9596a181d59813630c9fcc87180ab27
BYTES=251369
SHA256=7f763ebae15d2e2618dfb697d77928d73060402b1fb5bf7ca5cd962c6ae26811
APPLY_CHECK_OPTION=--unidiff-zero
FORWARD_CHECK_ON_BASE=PASS
REVERSE_CHECK_ON_MODIFIED_INDEX=PASS
```

## Rollback role

```text
PATH=scripts/rollback_astrology_bazi_v0_3.ps1
DEFAULT_MODE=DRY_RUN
APPLY_OPERATION=git revert --no-edit 0e161368e9596a181d59813630c9fcc87180ab27
```

Dry-run verification:

```text
ROLLBACK_VERIFY=PASS base=79b91226cf3196388432db09760ab0a91c82446d core=0e161368e9596a181d59813630c9fcc87180ab27 patch_sha256=7f763ebae15d2e2618dfb697d77928d73060402b1fb5bf7ca5cd962c6ae26811
ROLLBACK_MODE=DRY_RUN
EXIT=0
```

Actual-apply verification was executed after reopening packaged candidate
`b55334d62c0224afcad79b1fbc45bb8da67bbdb3` in a separate disposable worktree:

```text
PATCH_SHA256_CHECKOUT=7f763ebae15d2e2618dfb697d77928d73060402b1fb5bf7ca5cd962c6ae26811
PRE_STATUS_COUNT=0
ROLLBACK_VERIFY=PASS
ROLLBACK_MODE=APPLY
ROLLBACK_REVERT_COMMIT=942990d9c1fad8c6ee519d6fa9b27314bd9ca9fd
ROLLBACK_REVERTED_CORE=0e161368e9596a181d59813630c9fcc87180ab27
ROLLBACK_APPLY_EXIT=0
POST_STATUS_COUNT=0
ROLLBACK_CORE_TREE_EQUALS_BASE=PASS
Western baseline after rollback: 34 passed, EXIT=0
Bazi baseline after rollback: 90 passed, EXIT=0
ROLLBACK_BASELINE_BEHAVIOR=PASS
```

The only files remaining beyond the base after rollback were the four packaging
roles: `.gitattributes`, this patch, this verification record, and the rollback
script. No core implementation residue remained.
