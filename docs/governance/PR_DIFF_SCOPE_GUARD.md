# PR Diff Scope Guard

Purpose: prevent a small change from appearing as a multi-thousand-line pull request
because the wrong base/head relationship exposed cumulative branch history.

## Why this guard exists

GitHub pull requests use a three-dot comparison: the diff is calculated from the
merge base (latest common ancestor) to the topic branch head. If a durable research
lane diverged long ago and is used as the head of a new PR, GitHub can legitimately
display the entire accumulated branch delta even when the current task changed only a
small amount.

Authoritative references:

- GitHub: About comparing branches in pull requests
  https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-comparing-branches-in-pull-requests
- Git: git-merge-base --is-ancestor
  https://git-scm.com/docs/git-merge-base

## Governed durable branches

The guard applies whenever the PR base is one of:

- `main`
- `research/ccts-human-ai-learning-lane`
- `research/embodiment-lane`
- `research/legacy-uncertainty-hold`

A transient-to-transient stacked PR is outside this guard.

## Hard invariants

For every PR targeting a governed durable branch:

1. The head must come from the same repository.
2. A durable branch must not be used directly as the head of another durable-branch PR.
3. The head must use an approved transient prefix.
4. The selected durable base SHA must be an ancestor of the PR head.
5. Git failures while checking ancestry are errors, not silently interpreted as
   "not an ancestor."

These invariants cannot be bypassed with a large-PR acknowledgement.

## Large-diff visibility gate

A PR is considered unexpectedly large when it exceeds either:

- 2,000 added+deleted lines; or
- 30 changed files.

A genuinely intentional large PR may proceed only when its body contains both:

```text
LARGE_PR_EXPECTED = TRUE
LARGE_PR_REASON = <specific reason of at least 24 characters>
```

The acknowledgement exempts **only the size warning**. It does not override wrong
ancestry, wrong branch class, wrong repository, required checks, human merge authority,
or any other governance control.

```text
LARGE_PR_ACKNOWLEDGEMENT != MERGE_AUTHORITY
```

## Why the "final commit ratio" is not a hard gate

An earlier draft compared the full PR diff with the final commit size. Adversarial
review removed that rule because a healthy multi-commit PR can end with a very small
cleanup commit, producing a large ratio without any base/head error.

The hard ancestry test directly targets the failure mode that caused the historical
cumulative diff and has a precise Git definition.

## Machine-readable evidence

Each PR run records:

- exact base SHA;
- exact head SHA;
- exact merge-base SHA;
- base/head refs;
- same-repository status;
- ancestry status;
- changed files;
- additions/deletions/total lines;
- commit count;
- large-diff acknowledgement state;
- violations.

The report is written to the GitHub Actions step summary so a reviewer can see why the
guard passed or failed without reverse-engineering logs.

## Regression target

A historical cumulative shape such as:

```text
19 commits
34 files
+4721 lines
```

must not silently pass as an ordinary bounded PR.

A bounded promotion around 700 changed lines with correct ancestry and branch provenance
passes normally.

## Interpretation

```text
PR_DIFF_SIZE != AMOUNT_WRITTEN_THIS_TURN
GITHUB_PR_DIFF = THREE_DOT_MERGE_BASE_DIFF
CUMULATIVE_BRANCH_DIFF != CURRENT_TASK_DELTA
DURABLE_BRANCH != TRANSIENT_PR_HEAD
SURPRISE_LARGE_DIFF = FAIL_CLOSED
UNKNOWN_GIT_ANCESTRY = ERROR
```
