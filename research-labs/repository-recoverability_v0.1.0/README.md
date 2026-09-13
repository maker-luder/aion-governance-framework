# Repository Recoverability v0.1.0

Status: `BOUNDED_IMPLEMENTATION / SYNTHETICALLY_TESTED`

This lab implements the P0/P1 repository recoverability surface proposed by
Draft PR #102. It creates a fresh Git mirror, archives it outside the source
working tree, records SHA-256 and exact commit/tree/ref provenance, then verifies
checksum, archive extraction, Git integrity, refs, HEAD, tree, and required files
inside a temporary isolated restore.

```text
IMPLEMENTATION_BASE_COMMIT_SHA = d95bc2625e71f1c85a725aaba78cb0feccfc0668
IMPLEMENTATION_BASE_TREE_SHA = 77470062979df1db2f17c3a2a396891d1e910f98
UNMERGED_SPECIFICATION_DEPENDENCY = PR #102 @ 3ce4f759caf662a53f0d1f3a54709bc482d7df5e
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
  that this utility reproduced the declared Git objects and refs.
- LFS applicability is explicitly `NOT_ASSESSED` in v0.1.0 and remains an
  unresolved warning.
- Optional test-suite execution, malware scanning, account backup, credential
  rotation, deployment, and cloud automation are outside this bounded surface.
- The utility performs no `main` write and no repository merge.
- Receipts contain no credentials or recovery secrets.
- `CANONICAL_EFFECT = NONE`; `DEPLOYMENT = FALSE`.

## Verification

The synthetic tests create an isolated repository with a commit, branch, tag,
and required files. They verify successful backup/restore, exact commit and tree
SHA separation, exact ref comparison, checksum tamper rejection, destination
separation, traversal rejection, and non-secret receipts.
