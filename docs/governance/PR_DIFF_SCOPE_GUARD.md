# PR Diff Scope Guard

Purpose: prevent a small research change from appearing as a multi-thousand-line PR
because the wrong base/head relationship exposed cumulative branch history.

## Mandatory main-PR rules

1. A durable research lane must never be used directly as the head of a PR into `main`.
2. A PR into `main` must use an approved transient prefix.
3. The current `main` base SHA must be an ancestor of the PR head.
4. A PR is considered unexpectedly large when it exceeds either:
   - 2,000 added+deleted lines; or
   - 30 changed files.
5. A cumulative amplification warning also triggers when a multi-commit PR contains
   at least 1,200 changed lines and the cumulative diff is at least 4x the final
   commit's changed-line count.

Unexpectedly large or amplified PRs fail closed unless the PR body contains both:

```text
LARGE_PR_EXPECTED = TRUE
LARGE_PR_REASON = <specific human-readable reason>
```

This is not a ban on large PRs. It is a ban on **surprise** large PRs.

## Expected behavior

A bounded promotion such as a ~700-line implementation can pass normally.

A case like the earlier cumulative research-lane diff:

```text
19 commits
34 files
+4721 lines
```

will fail before review unless it is explicitly acknowledged as intentional.

## Interpretation

```text
PR_DIFF_SIZE != AMOUNT_WRITTEN_THIS_TURN
CUMULATIVE_BRANCH_DIFF != CURRENT_CHANGE
DURABLE_RESEARCH_LANE != MAIN_PROMOTION_BRANCH
SURPRISE_LARGE_DIFF = FAIL_CLOSED
```
