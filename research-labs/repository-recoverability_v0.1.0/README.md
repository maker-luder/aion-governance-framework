# Repository Recoverability v0.1.0

Status: `BOUNDED_IMPLEMENTATION / SYNTHETICALLY_TESTED`

This lab implements the P0/P1 repository recoverability surface proposed by
merged PR #102. It creates a fresh Git mirror, archives it outside the source
working tree, records SHA-256 and exact commit/tree/ref provenance, then verifies
checksum, archive extraction, Git integrity, refs, symbolic HEAD, HEAD commit,
HEAD tree, and required files inside a temporary isolated restore.

```text
IMPLEMENTATION_BASE_COMMIT_SHA = d95bc2625e71f1c85a725aaba78cb0feccfc0668
IMPLEMENTATION_BASE_TREE_SHA = 77470062979df1db2f17c3a2a396891d1e910f98
ORIGINAL_SPECIFICATION_REVIEW = PR #102 @ 3ce4f759caf662a53f0d1f3a54709bc482d7df5e
CURRENT_SPECIFICATION_STATUS = MERGED @ 2b151df564d753d6ce978a319a99959b864f7309
HISTORICAL_SYNCED_MAIN_COMMIT_SHA = 6e0ae579da9d09b3ba4041d52a7e9833ceb10ca1
PR102_USED_AS_IMPLEMENTATION_BASE = FALSE
```

## Use

Run from this lab directory, with an output directory outside the source repo:

```powershell
python scripts/create_backup.py <SOURCE_REPOSITORY> <OUTPUT_DIRECTORY> --required-file README.md
python scripts/verify_restore.py <OUTPUT_DIRECTORY>/repository-mirror.zip <OUTPUT_DIRECTORY>/backup-receipt.json <OUTPUT_DIRECTORY>/restore-receipt.json
```

The source may be a local Git repository or a Git URL supported by the installed
Git client. Credentials are handled by Git's configured transport and are not
copied into receipts. URL user information, query strings, and fragments are
removed from the recorded repository identifier.

## Boundaries

- `BACKUP_EXISTS != RESTORE_WORKS`; only a successful restore receipt establishes
  that this utility reproduced the declared Git objects, refs, and HEAD binding.
- The symbolic `HEAD` target is preserved and compared separately from HEAD's
  commit/tree SHAs. Two branches pointing to the same commit are therefore not
  treated as interchangeable default-branch state.
- v0.1.0 does **not** fetch or package the external Git LFS object store. Instead,
  it scans all objects reachable from captured refs and fails closed if a Git LFS
  pointer blob is found. A successful v0.1.0 receipt therefore means the captured
  reachable history has no detected LFS pointer dependency; it is not a claim
  that arbitrary LFS repositories are recoverable by this utility.
- Optional test-suite execution, malware scanning, account backup, credential
  rotation, deployment, and cloud automation are outside this bounded surface.
- The utility performs no `main` write and no repository merge.
- Receipts contain no credentials or recovery secrets.
- `CANONICAL_EFFECT = NONE`; `DEPLOYMENT = FALSE`.

## Verification

The synthetic tests create an isolated repository with a commit, branch, tag,
and required files. They verify successful backup/restore, exact commit/tree
separation, exact symbolic-HEAD and ref comparison, checksum tamper rejection,
destination separation, required-path traversal/duplication rejection,
fail-closed reachable-LFS-pointer detection, and non-secret receipts.
